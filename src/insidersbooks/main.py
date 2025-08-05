from fastapi import FastAPI
from .database import SessionLocal, Base, engine
from .models.user import User, UserRole
from .models.book import Book  
from .models.comment import Comment
from .models.comment_reaction import CommentReaction
from .models.rating import Rating
from .routes import auth, book, rating, comment, comment_rating


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(rating.router)
app.include_router(comment.router)
app.include_router(comment_rating.router)

@app.get('/')
def root():
    return {'message': 'Hello from InsidersBooks'}