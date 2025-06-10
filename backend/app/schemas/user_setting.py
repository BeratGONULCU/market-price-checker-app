from pydantic import BaseModel
from .base import BaseSchema
from datetime import datetime
from typing import Optional

class UserSettingBase(BaseModel):
    user_id: int
    setting_key: str
    value: str

class UserSettingCreate(UserSettingBase):
    pass

class UserSettingUpdate(UserSettingBase):
    user_id: Optional[int] = None
    setting_key: Optional[str] = None
    value: Optional[str] = None

class UserSettingInDB(UserSettingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserSetting(UserSettingInDB):
    pass 