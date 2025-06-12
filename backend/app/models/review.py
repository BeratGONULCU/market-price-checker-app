from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    content = Column(String)
    rating = Column(Float, nullable=False)  # 1-5 arası puan
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

    @property
    def user_name(self):
        return self.user.username if self.user else None 