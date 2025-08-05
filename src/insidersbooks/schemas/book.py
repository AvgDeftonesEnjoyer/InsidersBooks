from pydantic import BaseModel

class BookBase(BaseModel):
    title : str
    description : str | None = None
    
class BookCreate(BookBase):
    pass
    
class BookUpdate(BookBase):
    pass

class BookRead(BookBase):
    id : int
    author_id: int
    
    class Config:
        orm_mode = True