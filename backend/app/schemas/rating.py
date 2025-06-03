from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseSchema

class RatingBase(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None

class RatingCreate(BaseModel):
    product_id: int
    rating: int
    comment: Optional[str] = None

class RatingUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

class RatingInDB(RatingBase, BaseSchema):
    pass

class Rating(RatingInDB):
    pass 