from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseSchema

class CommentBase(BaseModel):
    user_id: int
    product_id: int
    content: str
    created_at: datetime
    updated_at: datetime

class CommentCreate(BaseModel):
    product_id: int
    content: str

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentInDB(CommentBase, BaseSchema):
    pass

class Comment(CommentInDB):
    pass 