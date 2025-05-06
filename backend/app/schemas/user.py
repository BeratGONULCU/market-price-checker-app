from pydantic import BaseModel, EmailStr

# Schema for user creation (signup)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Schema for user response (without password)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
