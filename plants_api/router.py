import logging
from enum import Enum
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from plants_api.database import db
from plants_api.plants.models import Plant
from plants_api.plants.models import PlantCreate
from plants_api.plants.models import PlantListItem
from plants_api.plants.models import PlantRead
from plants_api.plants.models import PlantUpdate
from plants_api.tags import Tags
from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from sqlmodel import Session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/plants")
tags: list[str | Enum] = [
    Tags.plant,
]


@router.post("/", response_model=PlantRead, tags=tags)
def create_plant(plant: PlantCreate, db_conn=Depends(db)):
    if plant.min_germination_temp == 0:
        plant.min_germination_temp = None
    if plant.max_germination_temp == 0:
        plant.max_germination_temp = None
    if plant.min_soil_temp_transplant == 0:
        plant.min_soil_temp_transplant = None
    if plant.max_soil_temp_transplant == 0:
        plant.max_soil_temp_transplant = None

    db_plant = Plant.model_validate(plant)

    db_conn.add(db_plant)
    db_conn.commit()
    return db_plant


@router.patch("/{plant_id}", response_model=PlantRead, tags=tags)
def plant_update(
    plant_id: UUID,
    plant: PlantUpdate,
    db_conn: Session = Depends(db),
):
    plant.pk = plant.pk or plant_id

    try:
        db_plant: Plant = db_conn.get_one(Plant, plant_id)  # , with_for_update=True)

    except NoResultFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="plant not found")
    data = plant.model_dump(exclude_defaults=True, exclude_unset=True)
    for k, v in data.items():
        if v:
            db_plant.__setattr__(k, v)
    db_conn.commit()
    db_conn.refresh(db_plant)
    return db_plant


@router.get("/", response_model=list[PlantListItem], tags=tags)
def plant_list(db: Session = Depends(db)):
    resp = db.exec(select(Plant).limit(100).offset(0)).all()
    return resp


@router.get("/{plant_id}", response_model=PlantRead, tags=tags)
def plant_read(plant_id: UUID, db: Session = Depends(db)):
    resp = db.get_one(Plant, plant_id)
    if not resp:
        raise HTTPException(404)
    return resp
