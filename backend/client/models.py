from sqlalchemy import Column, Float, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from db.engine import Base



class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String, nullable=False, index=True)
    port = Column(Integer, nullable=False)
    auth_token = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    # Foreign key for LPR
    lpr_id = Column(Integer, ForeignKey('lprs.id'), nullable=False)
    lpr = relationship('LPR', back_populates='clients')

    # Relationship to hold multiple cameras
    cameras = relationship('Camera', back_populates='client')


class LPR(Base):
    __tablename__ = 'lprs'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    # ip = Column(String, nullable=False, index=True)
    # port = Column(Integer, nullable=False)
    # auth_token = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    clients = relationship('Client', back_populates='lpr')
    # gate_id = Column(Integer, ForeignKey('gates.id'), nullable=False)
    # gate = relationship('Gate', back_populates='lprs')


class PlateData(Base):
    __tablename__ = 'plate_data'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # timestamp = Column(String, nullable=False, default=func.now())
    timestamp = Column(DateTime, nullable=False, default=func.now())
    plate_number = Column(String, nullable=False)
    ocr_accuracy = Column(Float, nullable=True)
    vision_speed = Column(Float, nullable=True)
    gate = Column(String, nullable=True)


class ImageData(Base):
    __tablename__ = 'image_data'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plate_number = Column(String, nullable=False)
    gate = Column(String, nullable=True)
    file_path = Column(String, nullable=False)  # Path to the saved image
    timestamp = Column(DateTime, nullable=False, default=func.now())
