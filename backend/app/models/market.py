from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Market(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255))
    phone = Column(String(20))
    open_hours = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    website = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product_details = relationship("ProductDetail", back_populates="market")
    price_history = relationship("PriceHistory", back_populates="market") 