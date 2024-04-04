from enum import Enum
from http import HTTPStatus
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from plants_api.database import SessionLocal, db
from plants_api.plants.models import (
    Plant,
    PlantCreate,
    PlantListItem,
    PlantRead,
    PlantUpdate,
)

import logging

from plants_api.tags import Tags

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/plants")
tags: list[str | Enum] = [
    Tags.plant,
]


@router.post("/", response_model=PlantRead, tags=tags)
def create_plant(plant: PlantCreate, db_conn=Depends(db)):
    return Plant.model_validate(plant).create(db_conn)


@router.patch("/{plant_id}", response_model=PlantRead, tags=tags)
def plant_update(
    plant_id: UUID, plant: PlantUpdate, db_conn: SessionLocal = Depends(db)
):
    plant.pk = plant.pk or plant_id

    db_plant: Plant = db_conn.get_one(Plant, plant_id)  # , with_for_update=True)

    if not db_plant:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="plant not found")
    data = plant.model_dump(exclude_defaults=True, exclude_unset=True)
    for k, v in data.items():
        if v:
            db_plant.__setattr__(k, v)
    db_conn.commit()
    db_conn.refresh(db_plant)
    return db_plant


@router.get("/", response_model=list[PlantListItem], tags=tags)
def plant_list(db=Depends(db)):
    return db.execute(select(Plant.pk, Plant.latin_name)).all()


@router.get("/{plant_id}", response_model=PlantRead, tags=tags)
def plant_read(plant_id: UUID, db=Depends(db)):
    resp = db.execute(
        (select(Plant).where(Plant.pk == plant_id).offset(0).limit(100))
    ).first()
    if not resp:
        raise HTTPException(404)
    return resp
