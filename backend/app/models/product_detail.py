from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class ProductDetail(BaseModel):
    __tablename__ = "product_details"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)
    price = Column(Float, nullable=False)
    expiration_date = Column(DateTime)
    calories = Column(Float)

    # Relationships
    product = relationship("Product", back_populates="details")
    market = relationship("Market") 