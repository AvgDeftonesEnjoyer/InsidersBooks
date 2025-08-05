from fastapi import APIRouter, Depends
from ..dependencies.auth import require_role
from ..schemas.user import UserRole

router = APIRouter(prefix='/books', tags = ['books'])

@router.get('/')
def read_books():
    return {'message': 'List of books'}

@router.post('/')
def create_book(user =Depends(require_role(UserRole.writer))):
    return {'message' : f'Book created by {user.username}'}

@router.delete('/{book_id}')
def delete_book(book_id: int, user = Depends(require_role(UserRole.admin))):
    return {'message': f'Book with ID {book_id} deleted by {user.username}'}