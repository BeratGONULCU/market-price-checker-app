from typing import Generator, Optional
import logging
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

# Comment out OAuth2 for now
# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/login/access-token"
# )

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    # token: str = Depends(reusable_oauth2)
) -> models.User:
    # Temporarily return a default user with id=1
    return db.query(models.User).filter(models.User.id == 1).first()
    
    # try:
    #     logger.info(f"Request headers: {request.headers}")
    #     logger.info(f"Validating token: {token}")
        
    #     payload = jwt.decode(
    #         token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
    #     )
    #     logger.info(f"Decoded payload: {payload}")
        
    #     token_data = schemas.TokenPayload(**payload)
    #     logger.info(f"Token data: {token_data}")
        
    #     if token_data.sub is None:
    #         logger.error("Token subject is None")
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Could not validate credentials",
    #         )
        
    #     # Convert string user_id to integer
    #     try:
    #         user_id = int(token_data.sub)
    #     except ValueError:
    #         logger.error(f"Invalid user_id format: {token_data.sub}")
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Invalid user ID format",
    #         )
        
    #     logger.info(f"Extracted user_id: {user_id}")
        
    #     user = crud.user.get(db, id=user_id)
    #     if not user:
    #         logger.error(f"No user found with id: {user_id}")
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Could not validate credentials",
    #         )
        
    #     logger.info(f"Successfully validated user: {user.email}")
    #     return user
        
    # except (JWTError, ValidationError) as e:
    #     logger.error(f"Token validation error: {str(e)}", exc_info=True)
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #     )
    # except Exception as e:
    #     logger.error(f"Unexpected error in get_current_user: {str(e)}", exc_info=True)
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #     )

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    # Temporarily skip active user check
    return current_user
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    # return current_user 