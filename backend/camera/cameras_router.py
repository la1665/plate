from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db.engine import get_db
from camera.models import Camera, CameraSetting
from camera.schemas import (CameraSettingCreate, CameraSettingUpdate, CameraSettingInDB,
    CameraCreate, CameraUpdate, CameraInDB)
from camera.operation import get_setting, create_camera, get_cameras, get_camera, update_camera, delete_camera

camera_router = APIRouter()


@camera_router.post("/cameras/", response_model=CameraInDB)
async def api_create_camera(camera: CameraCreate, db: AsyncSession=Depends(get_db)):
    """
    Adds a new camera and establishes a TCP connection.
    """
    return await create_camera(db, camera)

@camera_router.get("/cameras/", response_model=List[CameraInDB])
async def api_read_cameras(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Lists all the registered cameras.
    """
    cameras = await get_cameras(db, skip=skip, limit=limit)
    return cameras

@camera_router.get("/cameras/{camera_id}", response_model=CameraInDB)
async def api_read_camera(camera_id: int, db: AsyncSession = Depends(get_db)):
    db_camera = await get_camera(db, camera_id=camera_id)
    return db_camera


@camera_router.put("/cameras/{camera_id}", response_model=CameraInDB)
async def api_update_camera(camera_id: int, camera: CameraUpdate, db: AsyncSession = Depends(get_db)):
    db_camera = await update_camera(db, camera_id, camera)
    return db_camera

@camera_router.delete("/cameras/{camera_id}", response_model=CameraInDB)
async def api_delete_camera(camera_id: int, db: AsyncSession = Depends(get_db)):
    db_camera = await delete_camera(db, camera_id)
    return db_camera
