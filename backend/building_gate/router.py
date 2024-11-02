from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.engine import get_db
from building_gate.schemas import BuildingCreate, BuildingUpdate, BuildingInDB, GateCreate, GateUpdate, GateInDB
from building_gate.operation import get_building, get_buildings, create_building, update_building, delete_building
from building_gate.operation import get_gates, get_gate, create_gate, update_gate, delete_gate

building_router = APIRouter()
gate_router = APIRouter()


# Building endpoints
@building_router.post("/buildings/", response_model=BuildingInDB)
async def api_create_building(building: BuildingCreate, db: AsyncSession = Depends(get_db)):
    return await create_building(db, building)

@building_router.get("/buildings/", response_model=List[BuildingInDB])
async def api_get_buildings(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_buildings(db, skip, limit)

@building_router.get("/buildings/{building_id}", response_model=BuildingInDB)
async def api_get_building(building_id: int, db: AsyncSession = Depends(get_db)):
    return await get_building(db,building_id)


@building_router.put("/buildings/{building_id}", response_model=BuildingInDB)
async def api_update_building(building_id: int, building: BuildingUpdate, db:AsyncSession=Depends(get_db)):
    return await update_building(db, building_id, building)


@building_router.delete("/buildings/{building_id}", response_model=BuildingInDB)
async def api_delete_building(building_id: int, db:AsyncSession=Depends(get_db)):
    return await delete_building(db, building_id)


# Gate endpoints
@gate_router.post("/gates/", response_model=GateInDB)
async def api_create_gate(gate: GateCreate, db: AsyncSession = Depends(get_db)):
    return await create_gate(db, gate)

@gate_router.get("/gates/", response_model=List[GateInDB])
async def api_get_gates(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_gates(db, skip, limit)

@gate_router.get("/gates/{gate_id}", response_model=GateInDB)
async def api_get_gate(gate_id: int, db: AsyncSession = Depends(get_db)):
    return await get_gate(db, gate_id)


@gate_router.put("/gates/{gate_id}", response_model=GateInDB)
async def api_update_gate(gate_id: int, gate: GateUpdate, db:AsyncSession=Depends(get_db)):
    return await update_gate(db, gate_id, gate)


@gate_router.delete("/gates/{gate_id}", response_model=GateInDB)
async def api_delete_gate(gate_id: int, db:AsyncSession=Depends(get_db)):
    return await delete_gate(db, gate_id)
