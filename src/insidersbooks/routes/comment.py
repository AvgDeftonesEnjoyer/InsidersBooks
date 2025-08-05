from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from ..models.comment import Comment
from ..models.book import Book
from ..schemas.comment import CommentCreate, CommentUpdate, CommentRead
from ..dependencies.auth import get_current_user

router = APIRouter(prefix='/comments', tags=['comments'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post('/book/{book_id}', response_model=CommentRead)
def create_comment(book_id: int, comment_data: CommentCreate ,
                   db: Session = Depends(get_db), current_user = Depends(get_current_user) 
                   ):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail = 'Book not found')
    
    comment = Comment(
        content = comment_data.content,
        book_id = book_id,
        user_id = current_user.id
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get('/book/{book_id}', response_model = List[CommentRead])
def get_comments(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    
    comments = db.query(Comment).filter(Comment.book_id == book_id).all()
    return comments

@router.put('/{comment_id}', response_model=CommentRead)
def update_comment(comment_id: int, comment_data: CommentUpdate,
                   db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found or not authorized to edit')
    
    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return comment

@router.delete('/{comment_id}', response_model = CommentRead)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found or not authorized to delete')
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}