from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class UserRole(enum.Enum):
    reader = "reader"
    writer = "writer"
    admin = "admin"
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.reader, nullable=False)
    
    books = relationship("Book", back_populates="author")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    comment_reactions = relationship('CommentReaction', back_populates='user', cascade='all, delete-orphan')
