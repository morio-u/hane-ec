from sqlalchemy import Column, SmallInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="brand")