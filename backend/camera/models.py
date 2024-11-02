from enum import Enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, UUID, func
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as sqlEnum

from db.engine import Base


class SettingType(Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"


class CameraSetting(Base):
    __tablename__ = 'camera_settings'

    # uuid = Column(UUID, primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    value = Column(String(255), nullable=False)
    setting_type = Column(sqlEnum(SettingType), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    cameras = relationship("Camera", back_populates="setting", cascade='all, delete-orphan')

class Camera(Base):
    __tablename__ = 'cameras'

    # uuid = Column(UUID, primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    location = Column(String, nullable=True)
    # latitude = Column(String, nullable=False)
    # longitude = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    setting_id = Column(Integer, ForeignKey('camera_settings.id'))
    setting = relationship("CameraSetting", back_populates="cameras")

    gate_id = Column(Integer, ForeignKey('gates.id'), nullable=False)
    gate = relationship("Gate", back_populates="cameras")
    # Foreign key for Client
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True)
    client = relationship('Client', back_populates='cameras')
    # plate_data = relationship("PlateData", back_populates="camera", cascade="all, delete-orphan")
    # live_data = relationship("LiveData", back_populates="camera", cascade="all, delete-orphan")
