from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum as SQLEnum,
    Boolean,
    SmallInteger,
    TIMESTAMP,
)
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.user import UserStatusEnum


class AdminUserStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    pending = "pending"


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role_id = Column(SmallInteger, nullable=False, default=3)
    status = Column(
        SQLEnum(AdminUserStatusEnum), default=UserStatusEnum.active, nullable=False
    )
    last_login_at = Column(TIMESTAMP, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )
