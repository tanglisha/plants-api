from enum import Enum
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import select

from plants_api.database import SessionLocal, db
from plants_api.plants.models import Plant, PlantCreate, PlantListItem, PlantRead

import logging

from plants_api.tags import Tags

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/plants")
tags: list[str|Enum] = [Tags.plant,]

@router.post("/", response_model=PlantRead, tags=tags)
def create_plant(plant: PlantCreate):
    return Plant.model_validate(plant).create()

@router.get("/", response_model=list[PlantListItem], tags=tags)
def plant_list(db=Depends(db)):
    resp = db.execute(select(Plant.id, Plant.latin_name)).all()
    return resp

@router.get("/{id}", response_model=PlantRead, tags=tags)
def plant_read(id: str, db=Depends(db)):
    return db.execute(select(Plant).where(Plant.id == id)).first()

