from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models import User  # Doğru User modelini import et
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.api import deps
from app.schemas.token import Token
from app import crud

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

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

class TokenResponse(Token):
    user: dict

class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserSchema)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db)
) -> User:
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        password=hashed_password,
        name=user_in.name,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    try:
        logger.info(f"Login attempt for user: {form_data.username}")
        
        user = crud.user.authenticate(
            db, email=form_data.username, password=form_data.password
        )
        if not user:
            logger.warning(f"Authentication failed for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif not user.is_active:
            logger.warning(f"Inactive user attempt: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        logger.info(f"Successfully generated token for user: {user.email}")
        logger.info(f"Token payload: {{'sub': '{user.id}'}}")
        
        return Token(access_token=access_token, token_type="bearer")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/test-token", response_model=UserSchema)
def test_token(current_user: User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user

@router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(deps.get_current_user)
) -> User:
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> User:
    if user_in.password is not None:
        hashed_password = get_password_hash(user_in.password)
        current_user.password = hashed_password
    
    if user_in.email is not None:
        current_user.email = user_in.email
    
    if user_in.name is not None:
        current_user.name = user_in.name
    
    if user_in.is_active is not None:
        current_user.is_active = user_in.is_active
    
    if user_in.is_superuser is not None:
        current_user.is_superuser = user_in.is_superuser
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
