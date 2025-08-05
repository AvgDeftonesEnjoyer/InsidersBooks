from fastapi import FastAPI
from .database import SessionLocal, Base, engine
from .routes import auth, book
from .models import User, Book

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth.router)
app.include_router(book.router)

@app.get('/')
def root():
    return {'message': 'Hello from InsidersBooks'}
