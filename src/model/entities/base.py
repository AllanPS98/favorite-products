from sqlalchemy import Column, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base
from src.common.functions import timezone_br

Base = declarative_base()

class BaseModel(Base):

    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now(timezone_br()))
    updated_at = Column(DateTime, default=datetime.now(timezone_br()), onupdate=datetime.now(timezone_br()))