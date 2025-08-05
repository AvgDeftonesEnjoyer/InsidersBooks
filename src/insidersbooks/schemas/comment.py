from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    content: str
    
class CommentUpdate(BaseModel):
    content : str
    
class CommentRead(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    book_id: int
    
    class Config:
        orm_mode = True