from sqlalchemy import Column, SmallInteger, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint('department_id', 'name'),
    )

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    department_id = Column(SmallInteger, ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    department = relationship("Department", back_populates="categories")
    subcategories = relationship("Subcategory", back_populates="category")