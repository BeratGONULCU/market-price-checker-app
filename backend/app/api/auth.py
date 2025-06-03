from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)
from app.database import get_db
from app import crud, schemas

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/api/v1/auth/token")
async def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    # Trim whitespace from email
    email = login_data.email.strip()
    
    # Validate email format
    if '@' not in email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format. Please provide a valid email address."
        )
    
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/api/v1/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/api/v1/auth/me", response_model=schemas.User)
async def read_users_me(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=current_user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user 