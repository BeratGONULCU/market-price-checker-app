from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import logging

from app.core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)
from app.database import get_db
from app import crud, schemas

# Logger'ı yapılandır
logger = logging.getLogger(__name__)

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True

@router.post("/login", response_model=Token)
async def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        # Trim whitespace from email
        email = login_data.email.strip()
        logger.info(f"Login attempt for email: {email}")
        
        # Validate email format
        if '@' not in email:
            logger.warning(f"Invalid email format: {email}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email format. Please provide a valid email address."
            )
        
        user = crud.get_user_by_email(db, email=email)
        if not user:
            logger.warning(f"User not found: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not verify_password(login_data.password, user.password):
            logger.warning(f"Invalid password for user: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        logger.info(f"Successful login for user: {email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/register", response_model=Token)
async def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    try:
        # Trim whitespace from email and name
        user_data.email = user_data.email.strip()
        user_data.name = user_data.name.strip()
        
        logger.info(f"Registration attempt for email: {user_data.email}")
        
        # Check if user already exists
        db_user = crud.get_user_by_email(db, email=user_data.email)
        if db_user:
            logger.warning(f"User already exists: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = crud.create_user(db, user_data)
        
        # Generate access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        logger.info(f"Successful registration for user: {user_data.email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: schemas.User = Depends(get_current_user)
):
    try:
        return current_user
    except Exception as e:
        logger.error(f"Error getting user details: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 