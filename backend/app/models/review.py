from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    content = Column(String, nullable=False)
    rating = Column(Numeric(2,1), nullable=False)  # 1-5 arası puan
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    user = relationship("User", back_populates="comments")
    product = relationship("Product", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.id}>" 