from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

from camera.models import SettingType

class CameraSettingBase(BaseModel):
    name: str
    description: str
    value: str
    setting_type: SettingType = Field(default=SettingType.STRING)

class CameraSettingCreate(CameraSettingBase):
    pass


class CameraSettingUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    value: Optional[str] = None
    setting_type: Optional[SettingType] = None


class CameraBase(BaseModel):
    name: str
    location: str


class CameraCreate(CameraBase):
    setting_id: int
    gate_id: int


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    setting_id: Optional[int] = None
    gate_id: Optional[int] = None


class CameraInDB(CameraBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    setting_id: int
    gate_id: int

    class Config:
        from_attributes = True


class CameraSettingInDB(CameraSettingBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    cameras: Optional[List[CameraInDB]] = []

    class Config:
        from_attributes = True
