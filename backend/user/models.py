from sqlalchemy import Column, func, Enum as sqlalchemyEnum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from enum import Enum

from db.engine import Base


class UserType(Enum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"
    VIEWER = "viewer"


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255),unique=True, nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    national_id = Column(String(10), nullable=True)
    personal_number = Column(String(10), nullable=True)
    office = Column(String(255), nullable=True)
    phone_number = Column(String(10), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    user_type = Column(sqlalchemyEnum(UserType), default=UserType.USER)
    attributes = Column(JSON, default={})
    profile_image = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
