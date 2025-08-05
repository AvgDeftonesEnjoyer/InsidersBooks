from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserRead
from ..models.user import User, UserRole
from ..database import SessionLocal
from ..dependencies.auth import get_current_user
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=['auth'])

SECRET_KEY = 'SuperSecretKey'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/register', response_model = UserRead)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == user_data.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail ='Email already registered')
    
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_password,
        role = UserRole.reader
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code = 400, detail = 'Invalid credentials')
    
    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return {'access_token': token, 'token_type': 'bearer'}

@router.get('/me')
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role.value
    }