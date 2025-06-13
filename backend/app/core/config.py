from typing import List, Union, Any, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator, PostgresDsn
import secrets
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Market Price Comparison"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "market_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def get_database_url(self) -> str:
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # JWT settings
    SECRET_KEY: str = "your-super-secret-key-here"  # Sabit bir değer kullanıyoruz
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
