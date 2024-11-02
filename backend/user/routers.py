from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum

from db.engine import get_db
from user.operations import UserOperation
from user.schemas import UserInDB, UserCreate, UserUpdate
from authentication.access_level import (get_user,
    get_current_user,
    get_admin_user,
    get_admin_or_staff_user,
)


class TagType(Enum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"
    VIEWER = "viewer"


admin_router = APIRouter()


@admin_router.post("/v1/users", response_model=UserInDB)
async def api_create_user(user: UserCreate, db: AsyncSession=Depends(get_db), current_user: UserInDB=Depends(get_admin_user)):
    db_user = await UserOperation(db).check_for_user(user.username, user.email)
    if db_user:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "Username/Email already exists.")
    return await UserOperation(db).create_user(user)


@admin_router.get("/v1/users", response_model=List[UserInDB])
async def api_read_all_users(db: AsyncSession=Depends(get_db), current_user: UserInDB=Depends(get_admin_user)):
    return await UserOperation(db).get_all_users()

@admin_router.get("/v1/users/{user_id}")
async def api_read_user(user_id: int, db: AsyncSession=Depends(get_db), current_user: UserInDB=Depends(get_admin_user)):
    user = await UserOperation(db).get_user(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found!")
    return user

@admin_router.delete("/v1/users/{user_id}")
async def api_delete_user(user_id: int, db:AsyncSession=Depends(get_db), current_user: UserInDB=Depends(get_admin_user)):
    user = await UserOperation(db).delete_user(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return user


@admin_router.patch("/v1/users/{user_id}")
async def api_change_user_activation(user_id: int, db:AsyncSession=Depends(get_db), current_user:UserInDB=Depends(get_admin_or_staff_user)):
    user = await UserOperation(db).update_user_activate_status(user_id)
    return {"msg": f"User with id:{user.id} is_active status updated to {user.is_active} successfully"}
