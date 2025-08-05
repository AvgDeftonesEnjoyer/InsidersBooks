from fastapi import FastAPI
from .database import SessionLocal, Base, engine
from .routes import auth

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.icnlude_router(auth.router)

@app.get('/')
def root():
    return {'message': 'Hello from InsidersBooks'}
