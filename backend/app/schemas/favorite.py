from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FavoriteBase(BaseModel):
    user_id: int
    product_id: int
    market_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteUpdate(FavoriteBase):
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    market_id: Optional[int] = None

class FavoriteInDB(FavoriteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Favorite(FavoriteInDB):
    pass 