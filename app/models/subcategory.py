from sqlalchemy import Column, SmallInteger, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Subcategory(Base):
    __tablename__ = "subcategories"
    __table_args__ = (
        UniqueConstraint('category_id', 'name'),
    )

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    category_id = Column(SmallInteger, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="subcategories")