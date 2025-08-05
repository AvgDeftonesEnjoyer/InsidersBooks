# DB config will go here

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:qwerty12345@localhost/insidersbooks_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush = False, autocommit = False)

Base = declarative_base()