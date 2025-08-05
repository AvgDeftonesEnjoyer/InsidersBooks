from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.rating import Rating
from ..models.book import Book
from ..database import SessionLocal
from ..schemas.rating import RatingCreate, RatingRead
from ..dependencies.auth import get_current_user

router = APIRouter(prefix='/rating', tags=['ratings'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/book/{book_id}', response_model = RatingRead)
def rate_book(book_id : int, rating_data: RatingCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    
    rating = db.query(Rating).filter_by(user_id = user.id, book_id = book_id).first()
    if rating:
        rating.value = rating_data.value
    else:
        rating = Rating(value=rating_data.value, book_id = book_id, user_id = user.id)
        db.add(rating)
        
    db.commit()
    db.refresh(rating)
    return rating