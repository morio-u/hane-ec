from sqlalchemy import Column, SmallInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Size(Base):
    __tablename__ = "sizes"

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    skus = relationship("Sku", back_populates="size")
