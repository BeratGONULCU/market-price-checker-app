from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Debug: Print the database URL
print("Database URL:", settings.SQLALCHEMY_DATABASE_URL)

# SQLAlchemy database engine
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

# SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
