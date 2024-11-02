from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

from building_gate.models import GateType
from camera.schemas import CameraInDB


class BuildingBase(BaseModel):
    name: str
    location: Optional[str] = None
    description: Optional[str] = None

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class GateBase(BaseModel):
    name: str
    description: Optional[str] = None
    gate_type: GateType = Field(default=GateType.BOTH)

class GateCreate(GateBase):
    building_id: int

class GateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    building_id: Optional[int] = None

class GateInDB(GateBase):
    id: int
    building_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    cameras: List[CameraInDB] = []

    class Config:
        from_attributes = True


class BuildingInDB(BuildingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    gates: Optional[List[GateInDB]] = []

    class Config:
        from_attributes = True
