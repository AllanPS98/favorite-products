import enum
from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.common.functions import get_uuid, mask_email
from src.model.base import BaseModel

class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"

class Customer(BaseModel):
    __tablename__ = "customers"

    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: get_uuid(), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum, name="role_enum"), nullable=False, default=RoleEnum.user)

    favorites = relationship("Favorite", back_populates="customer", cascade="all, delete-orphan")
    
    def get(self):
        masked_email = mask_email(self.email)
        return {
            "customer_id": str(self.customer_id),
            "email": masked_email,
            "name": self.name,
            "role": self.role.value
        }