from sqlalchemy import Column, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class CommentReaction(Base):
    __tablename__ = 'comment_reactions'
    __table_args__ = (UniqueConstraint('user_id', 'comment_id', name = 'unique_user_comment'), )
    
    id = Column(Integer, primary_key = True, index = True)
    is_like = Column(Boolean, nullable = False)
    
    user_id = Column(Integer, ForeignKey('users.id', on_delete='CASCADE'))
    comment_id = Column(Integer, ForeignKey('comments.id', on_delete='CASCADE'))
    
    user = relationship('User', back_populates='comment_reactions')
    comment = relationship('Comment', back_populates='reactions')