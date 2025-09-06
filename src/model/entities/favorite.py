from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.model.entities.base import BaseModel

class Favorite(BaseModel):
    __table_name__ = "favorites"

    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.customer_id'), nullable=False, primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('customers.customer_id'), nullable=False, primary_key=True)

    customer = relationship("Customer", back_populates="favorites")
    product = relationship("Product", back_populates="favorites")