from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.common.functions import get_uuid
from src.model.entities.base import BaseModel


class Product(BaseModel):
    __table_name__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: get_uuid(), unique=True, nullable=False)
    product_api_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    image = Column(String, nullable=False)
    rating_rate = Column(String)
    rating_count = Column(Integer)

    favorites = relationship("Favorite", back_populates="product")