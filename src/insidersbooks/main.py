from fastapi import FastAPI
from .database import SessionLocal, Base, engine
from .routes import auth, book, rating, comment, comment_rating
from .models import User, Book, Comment, CommentReaction
from .models import rating as rating_model

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
