from pydantic import BaseModel, EmailStr
from typing import Optional
from .base import BaseSchema

# Schema for user creation (signup)
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDB(UserBase, BaseSchema):
    pass

class User(UserInDB):
    pass

# Schema for user response (without password)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
