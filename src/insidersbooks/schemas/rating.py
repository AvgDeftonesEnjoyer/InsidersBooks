from pydantic import BaseModel, Field

class RatingCreate(BaseModel):
    value : int = Field(..., ge = 1, le = 5)
    
class RatingRead(RatingCreate):
    id : int
    user_id : int
    book_id : int
    
    class Config:
        orm_mode = True

