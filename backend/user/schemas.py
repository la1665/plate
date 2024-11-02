from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

from user.models import UserType


class UserBase(BaseModel):
    username: str
    email: str
    user_type: UserType = Field(default=UserType.USER)
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    ...


class UserInDB(UserBase):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id_number: Optional[str] = None
    personal_number: Optional[str] = None
    phone_number: Optional[str] = None
    office: Optional[str] = None
    profile_image: Optional[str] = None
    hashed_password: str
    attributes: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
