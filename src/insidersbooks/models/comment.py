from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key = True, index = True)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id', on_delete='CASCADE'))
    book_id = Column(Integer, ForeignKey('books.id', on_delete='CASCADE'))
    
    user = relationship('User', back_populates = 'comments')
    book = relationship('Book', back_populates = 'comments')
    reactions = relationship('CommentReaction', back_populates='comment', cascade='all, delete-orphan')
