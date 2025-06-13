from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .base import BaseSchema

# Schema for user creation (signup)
class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: str

# Schema for user response (without password)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
