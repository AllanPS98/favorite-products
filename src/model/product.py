from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.common.functions import get_uuid
from src.model.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: get_uuid(), unique=True, nullable=False)
    product_api_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    image = Column(String, nullable=False)
    rating_rate = Column(Float)
    rating_count = Column(Integer)

    favorites = relationship("Favorite", back_populates="product")

    def get(self) -> dict:
        return {
            "product_id": str(self.product_id),
            "product_api_id": self.product_api_id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "image": self.image,
            "rating_rate": self.rating_rate,
            "rating_count": self.rating_count
        }