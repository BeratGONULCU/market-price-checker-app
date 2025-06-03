from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class PriceAlert(BaseModel):
    __tablename__ = "price_alerts"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    target_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    last_checked = Column(DateTime)
    notified = Column(Boolean, default=False)

    # Relationships
    user = relationship("User")
    product = relationship("Product", back_populates="price_alerts") 