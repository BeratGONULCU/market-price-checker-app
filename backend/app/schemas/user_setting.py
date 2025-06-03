from pydantic import BaseModel
from .base import BaseSchema

class UserSettingBase(BaseModel):
    user_id: int
    setting_key: str
    value: str

class UserSettingCreate(BaseModel):
    setting_key: str
    value: str

class UserSettingUpdate(BaseModel):
    value: str

class UserSettingInDB(UserSettingBase, BaseSchema):
    pass

class UserSetting(UserSettingInDB):
    pass 