from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.book import BookCreate, BookRead, BookUpdate
from ..models.book import Book
from ..models.user import UserRole
from ..database import SessionLocal
from ..dependencies.auth import get_current_user, require_role

router = APIRouter(prefix='/books', tags = ['books'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

      
@router.get('/', response_model = list[BookRead])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books


@router.get('/{book_id}', response_model = BookRead)
def get_book(book_id:int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    
    return book


@router.post('', response_model = BookRead)
def create_book(book_data: BookCreate, 
                db: Session = Depends(get_db),
                user = Depends(require_role(UserRole.writer))
                ):
    try:
        book = Book(
            title=book_data.title,
            description=book_data.description,
            author_id=user.id
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating book: {str(e)}")

@router.put('/{book_id}', response_model = BookRead)
def update_book(book_id: int,
                book_data: BookUpdate,
                db : Session = Depends(get_db),
                user = Depends(require_role(UserRole.writer))
                ):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code = 404, detail = 'Book not foind')
    
    for field, value in book_data.dict().items():
        setattr(book, field, value)
    
    db.commit()
    db.refresh(book)
    return book

@router.delete('/{book_id}')
def delete_book(book_id: int, db : Session = Depends(get_db), user = Depends(require_role(UserRole.admin))):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code = 404, detail = 'Book not found')
    
    db.delete(book)
    db.commit()
    return {'message' : f'Book {book.title} deleted successfully'}
        
    
    