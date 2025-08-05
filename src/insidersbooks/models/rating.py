from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Rating(Base):
    __tablename__ = 'ratings'
    __table_args__ = (UniqueConstraint('user_id', 'book_id', name = 'unique_user_book'), )
    
    id = Column(Integer, primary_key = True, index = True)
    value = Column(Integer, nullable = False)
    
    user_id = Column(Integer, ForeignKey('user.id', on_delete='CASCADE'))
    book_id = Column(Integer, ForeignKey('books.id', on_delete='CASCADE'))
    
    user = relationship('User', back_populates='ratings')
    book = relationship('Book', back_populates='ratings')