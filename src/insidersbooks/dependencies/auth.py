from fastapi import APIRouter, HTTPException, status , Depends
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.user import User, UserRole
from ..schemas.user import UserRole as SchemaUserRole

SECRET_KEY = 'SuperSecretKey'
ALGORITHM = 'HS256'

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role == UserRole.admin:
            return current_user
        
        if required_role == UserRole.writer and current_user.role == UserRole.writer:
            return current_user
            
        if required_role == UserRole.reader:
            return current_user
            
        raise HTTPException(
            status_code=403, 
            detail=f'Not enough permissions. Required: {required_role.value}, Current: {current_user.role.value}'
        )
    return role_checker