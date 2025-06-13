from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    rating: float = Field(..., ge=1, le=5)
    product_id: int

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[float] = Field(None, ge=1, le=5)

class Comment(CommentBase):
    id: int
    user_id: int
    user_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 