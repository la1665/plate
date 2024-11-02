from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from building_gate.operation import get_gate
from camera.models import Camera
from client.models import LPR, Client


async def create_client(db: AsyncSession, client_data):
    # Ensure the LPR exists
    db_lpr = await get_lpr(db, client_data.lpr_id)

    # Create the new Client instance
    new_client = Client(
        ip=client_data.ip,
        port=client_data.port,
        auth_token=client_data.auth_token,
        lpr_id=db_lpr.id
    )

    # Assign cameras to the client
    if client_data.camera_ids:
        # Fetch the camera objects
        camera_result = await db.execute(select(Camera).where(Camera.id.in_(client_data.camera_ids)))
        cameras = camera_result.scalars().all()

        # Ensure all requested cameras are found
        if len(cameras) != len(client_data.camera_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more cameras not found")

        new_client.cameras = cameras

    # Add the client to the database
    try:
        db.add(new_client)
        await db.commit()
        await db.refresh(new_client)
        return new_client
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_lpr(db: AsyncSession, lpr_id: int):
    result = await db.execute(select(LPR).where(LPR.id == lpr_id))
    lpr =  result.unique().scalars().first()

    if lpr is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="lpr not found")
    return lpr

async def get_lprs(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(LPR).offset(skip).limit(limit))
    return result.unique().scalars().all()

async def create_lpr(db: AsyncSession, lpr):
    new_lpr = LPR(name=lpr.name,
        description=lpr.description
)
    try:
        db.add(new_lpr)
        await db.commit()
        await db.refresh(new_lpr)
        return new_lpr
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def update_lpr(db: AsyncSession, lpr_id: int, lpr):
    db_lpr = await get_lpr(db, lpr_id)
    update_data = lpr.dict(exclude_unset=True)

    for key, value in lpr.dict(exclude_unset=True).items():
        setattr(db_lpr, key, value)
    try:
        await db.commit()
        await db.refresh(db_lpr)
        return db_lpr
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def delete_lpr(db: AsyncSession, lpr_id: int):
    db_lpr = await get_lpr(db, lpr_id)
    try:
        await db.delete(db_lpr)
        await db.commit()
        return db_lpr
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
