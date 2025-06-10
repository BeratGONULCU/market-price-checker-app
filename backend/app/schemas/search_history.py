from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base import BaseSchema

class SearchHistoryBase(BaseModel):
    user_id: int
    query: str

class SearchHistoryCreate(SearchHistoryBase):
    pass

class SearchHistoryUpdate(SearchHistoryBase):
    user_id: Optional[int] = None
    query: Optional[str] = None

class SearchHistoryInDB(SearchHistoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SearchHistory(SearchHistoryInDB):
    pass 