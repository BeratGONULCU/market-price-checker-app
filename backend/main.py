from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, shopping_lists, categories, products
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(shopping_lists.router)
app.include_router(categories.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Market Price Checker API"} 