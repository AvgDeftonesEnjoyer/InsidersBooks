from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    reader = "reader"
    writer = "writer"
    admin = "admin"

class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str
    
class UserRead(BaseModel):
    id : int
    username : str
    email : EmailStr
    role : UserRole
    
    class Config : 
        orm_mode = True