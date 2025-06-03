from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user_setting import UserSetting
from app.schemas.user_setting import UserSetting as UserSettingSchema, UserSettingCreate, UserSettingUpdate

router = APIRouter()

@router.post("/", response_model=UserSettingSchema)
def create_user_setting(user_setting: UserSettingCreate, db: Session = Depends(get_db)):
    # Check if setting already exists for this user and key
    existing_setting = db.query(UserSetting).filter(
        UserSetting.user_id == user_setting.user_id,
        UserSetting.setting_key == user_setting.setting_key
    ).first()
    
    if existing_setting:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Setting already exists for this user and key"
        )
    
    db_user_setting = UserSetting(**user_setting.dict())
    db.add(db_user_setting)
    db.commit()
    db.refresh(db_user_setting)
    return db_user_setting

@router.get("/user/{user_id}", response_model=List[UserSettingSchema])
def read_user_settings(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_settings = db.query(UserSetting).filter(
        UserSetting.user_id == user_id
    ).offset(skip).limit(limit).all()
    return user_settings

@router.get("/{user_setting_id}", response_model=UserSettingSchema)
def read_user_setting(user_setting_id: int, db: Session = Depends(get_db)):
    db_user_setting = db.query(UserSetting).filter(UserSetting.id == user_setting_id).first()
    if db_user_setting is None:
        raise HTTPException(status_code=404, detail="User setting not found")
    return db_user_setting

@router.put("/{user_setting_id}", response_model=UserSettingSchema)
def update_user_setting(user_setting_id: int, user_setting: UserSettingUpdate, db: Session = Depends(get_db)):
    db_user_setting = db.query(UserSetting).filter(UserSetting.id == user_setting_id).first()
    if db_user_setting is None:
        raise HTTPException(status_code=404, detail="User setting not found")
    
    for key, value in user_setting.dict(exclude_unset=True).items():
        setattr(db_user_setting, key, value)
    
    db.commit()
    db.refresh(db_user_setting)
    return db_user_setting

@router.delete("/{user_setting_id}", response_model=UserSettingSchema)
def delete_user_setting(user_setting_id: int, db: Session = Depends(get_db)):
    db_user_setting = db.query(UserSetting).filter(UserSetting.id == user_setting_id).first()
    if db_user_setting is None:
        raise HTTPException(status_code=404, detail="User setting not found")
    
    db.delete(db_user_setting)
    db.commit()
    return db_user_setting 