from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Boolean, func
from sqlalchemy import Enum as sqlEnum
from sqlalchemy.orm import relationship
from enum import Enum

from db.engine import Base


class GateType(Enum):
    ENTRANCE = 0
    EXIT = 1
    BOTH = 2



class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False)

    gates = relationship('Gate', back_populates='building', cascade='all, delete-orphan')

class Gate(Base):
    __tablename__ = 'gates'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    gate_type = Column(sqlEnum(GateType), default=GateType.BOTH, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False)

    building_id = Column(Integer, ForeignKey('buildings.id'), nullable=False)
    building = relationship('Building', back_populates='gates')
    cameras = relationship("Camera", back_populates="gate", cascade="all, delete-orphan")
