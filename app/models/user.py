from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Boolean, SmallInteger, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum


class GenderEnum(int, Enum):
    man = 0
    woman = 1
    other = 2
    na = 3

class UserStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    pending = "pending"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    gender = Column(SQLEnum(GenderEnum), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True,)
    password = Column(String(255), nullable=False)
    role = Column(SmallInteger, default=0, nullable=False)
    status = Column(SQLEnum(UserStatusEnum), default=UserStatusEnum.active, nullable=False)
    is_send_newsletter = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")