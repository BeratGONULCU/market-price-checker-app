from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ReviewBase(BaseModel):
    content: str
    rating: float = Field(..., ge=1, le=5)  # 1-5 arası puan

class ReviewCreate(ReviewBase):
    product_id: int

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    updated_at: datetime
    user_name: str

    class Config:
        from_attributes = True 