from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from camera.schemas import CameraInDB


class ClientBase(BaseModel):
    ip: str
    port: int
    auth_token: str

class ClientCreate(ClientBase):
    lpr_id: int
    camera_ids: List[int] = []

class ClientUpdate(BaseModel):
    ip: str
    port: int
    auth_token: str
    lpr_id: int


class LPRBase(BaseModel):
    name: str
    # ip: str
    # port: int
    # auth_token: str
    description: Optional[str] = None

class LPRCreate(LPRBase):
    # gate_id: int
    pass

class LPRUpdate(BaseModel):
    name: Optional[str] = None
    # ip: Optional[str] = None
    # port: Optional[int] = None
    # auth_token: Optional[str] = None
    description: Optional[str] = None
    # gate_id: Optional[int] = None

class LPRInDB(LPRBase):
    id: int
    # gate_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class ClientInDB(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    cameras: List[CameraInDB] = []
    lprs: List[LPRInDB] = []
