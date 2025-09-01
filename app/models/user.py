from sqlalchemy import Column, Integer, String, Enum, Boolean, SmallInteger, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy_utils import CIText
from enum import Enum


class GenderEnum(Enum):
    man = 0
    woman = 1
    other = 2
    na = 3

class UserStatusEnum(Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    pending = "pending"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    phone_number = Column(String(15), nullable=False)
    email = Column(CIText(), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(SmallInteger, default=0, nullable=False)
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.active, nullable=False)
    is_send_newsletter = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)