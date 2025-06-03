from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseSchema

class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

class NotificationCreate(BaseModel):
    title: str
    message: str
    type: str

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
    read_at: Optional[datetime] = None

class NotificationInDB(NotificationBase, BaseSchema):
    pass

class Notification(NotificationInDB):
    pass 