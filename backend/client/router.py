from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db.engine import get_db
from client.schemas import LPRCreate, LPRUpdate, LPRInDB, ClientCreate
from client.operation import get_lpr, get_lprs, create_lpr, update_lpr, delete_lpr, create_client


client_router = APIRouter()

@client_router.post("/clients/")
async def api_create_client(client: ClientCreate, db: AsyncSession = Depends(get_db)):
    return await create_client(db, client)


lpr_router = APIRouter()


@lpr_router.post("/lprs/", response_model=LPRInDB)
async def api_create_lpr(lpr: LPRCreate, db: AsyncSession = Depends(get_db)):
    return await create_lpr(db, lpr)

@lpr_router.get("/lprs/", response_model=List[LPRInDB])
async def api_get_lprs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_lprs(db, skip, limit)

@lpr_router.get("/lprs/{lpr_id}", response_model=LPRInDB)
async def api_read_lpr(lpr_id: int, db: AsyncSession=Depends(get_db)):
    return await get_lpr(db, lpr_id)

@lpr_router.put("/lprs/{lpr_id}", response_model=LPRInDB)
async def api_update_lpr(lpr_id: int, lpr: LPRUpdate, db:AsyncSession=Depends(get_db)):
    return await update_lpr(db, lpr_id, lpr)

@lpr_router.delete("/lprs/{lpr_id}", response_model=LPRInDB)
async def api_delete_lpr(lpr_id: int, db:AsyncSession=Depends(get_db)):
    return await delete_lpr(db, lpr_id)
