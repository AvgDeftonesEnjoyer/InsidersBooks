from pydantic import BaseModel

class CommentReactionCreate(BaseModel):
    is_like : bool
    
class CommentReactionRead(BaseModel):
    id : int
    is_like : bool
    user_id : int
    comment_id : int
    
    class Config:
        orm_mode = True
        
        
    