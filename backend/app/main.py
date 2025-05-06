from fastapi import FastAPI
from app.api.endpoints import auth
from app.db.session import engine, Base

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include authentication endpoints
app.include_router(auth.router, prefix="/auth", tags=["auth"])
