from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from building_gate.models import Building, Gate

# Building operations
async def get_building(db: AsyncSession, building_id: int):
    result = await db.execute(
            select(Building)
            .where(Building.id == building_id)
            .options(selectinload(Building.gates))
        )

    building = result.unique().scalars().first()

    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")

    return building

async def get_buildings(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Building)
        .options(selectinload(Building.gates).selectinload(Gate.cameras))
        .offset(skip)
        .limit(limit))
    return result.unique().scalars().all()

async def create_building(db: AsyncSession, building):
    new_building = Building(name=building.name,
        location=building.location,
        description=building.description)
    try:
        db.add(new_building)
        await db.commit()
        await db.refresh(new_building)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    result = await db.execute(
            select(Building)
            .where(Building.id == new_building.id)
            .options(selectinload(Building.gates))
        )
    new_building = result.scalars().first()
    return new_building


async def update_building(db: AsyncSession, building_id: int, building):
    db_building = await get_building(db, building_id)
    for key, value in building.dict(exclude_unset=True).items():
        setattr(db_building, key, value)
    try:
        await db.commit()
        await db.refresh(db_building)
        return db_building
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

async def delete_building(db: AsyncSession, building_id: int):
    db_building = await get_building(db, building_id)
    try:
        await db.delete(db_building)
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_building


# Gate operations
async def get_gate(db: AsyncSession, gate_id: int):
    result = await db.execute(select(Gate)
        .where(Gate.id == gate_id)
        .options(selectinload(Gate.cameras))
    )
    db_gate =  result.unique().scalars().first()
    if db_gate is None:
        raise HTTPException(status_code=404, detail="gate not found")
    return db_gate

async def get_gates(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Gate)
        .offset(skip).limit(limit)
        .options(selectinload(Gate.cameras))
    )
    return result.unique().scalars().all()


async def create_gate(db: AsyncSession, gate):
    db_building = await get_building(db, gate.building_id)
    new_gate = Gate(name=gate.name,
        gate_type=gate.gate_type,
        description=gate.description,
        building_id=db_building.id)
    try:
        db.add(new_gate)
        await db.commit()
        await db.refresh(new_gate)
        result = await db.execute(
                select(Gate)
                .where(Gate.id == new_gate.id)
                .options(selectinload(Gate.cameras))
            )
        new_gate = result.scalars().first()
        return new_gate
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def update_gate(db: AsyncSession, gate_id: int, gate):
    db_gate = await get_gate(db, gate_id)
    update_data = gate.dict(exclude_unset=True)
    if "building_id" in update_data:
        building_id = update_data["building_id"]
        await get_building(db, building_id)

    for key, value in update_data.items():
        setattr(db_gate, key, value)
    try:
        await db.commit()
        await db.refresh(db_gate)
        return db_gate
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def delete_gate(db: AsyncSession, gate_id: int):
    db_gate = await get_gate(db, gate_id)
    try:
        await db.delete(db_gate)
        await db.commit()
        return db_gate
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
