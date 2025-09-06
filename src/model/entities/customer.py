from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.common.functions import get_uuid
from src.model.entities.base import BaseModel


class Customer(BaseModel):
    __table_name__ = "customers"

    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: get_uuid(), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)

    favorites = relationship("Favorite", back_populates="customer")