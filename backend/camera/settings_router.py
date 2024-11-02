from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from camera.operation import get_setting, get_settings, create_setting, update_setting, delete_setting
from camera.schemas import CameraSettingCreate, CameraSettingUpdate, CameraSettingInDB
from db.engine import get_db

settings_router = APIRouter()

@settings_router.post("/camera-settings/", response_model=CameraSettingInDB)
async def api_create_setting(setting: CameraSettingCreate, db: AsyncSession = Depends(get_db)):
    return await create_setting(db, setting)

@settings_router.get("/camera-settings/", response_model=List[CameraSettingInDB])
async def api_read_settings(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    settings = await get_settings(db, skip=skip, limit=limit)
    return settings

@settings_router.get("/camera-settings/{setting_id}", response_model=CameraSettingInDB)
async def api_read_setting(setting_id: int, db: AsyncSession = Depends(get_db)):
    db_setting = await get_setting(db, setting_id=setting_id)
    return db_setting

@settings_router.put("/camera-settings/{setting_id}", response_model=CameraSettingInDB)
async def api_update_setting(setting_id: int, setting: CameraSettingUpdate, db: AsyncSession = Depends(get_db)):
    db_setting = await update_setting(db, setting_id, setting)
    return db_setting

@settings_router.delete("/camera-settings/{setting_id}", response_model=CameraSettingInDB)
async def api_delete_setting(setting_id: int, db: AsyncSession = Depends(get_db)):
    db_setting = await delete_setting(db, setting_id)
    return db_setting
