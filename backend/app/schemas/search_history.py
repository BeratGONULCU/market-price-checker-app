from pydantic import BaseModel
from datetime import datetime
from .base import BaseSchema

class SearchHistoryBase(BaseModel):
    user_id: int
    keyword: str
    searched_at: datetime

class SearchHistoryCreate(BaseModel):
    keyword: str

class SearchHistoryInDB(SearchHistoryBase, BaseSchema):
    pass

class SearchHistory(SearchHistoryInDB):
    pass 