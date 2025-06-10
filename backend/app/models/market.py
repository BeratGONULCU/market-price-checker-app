from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Market(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    website = Column(String(255))
    address = Column(String(255))
    phone = Column(String(20))
    open_hours = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    product_details = relationship("ProductDetail", back_populates="market", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="market", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="market") 