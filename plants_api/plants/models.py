import logging
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import Field
from uuid import UUID, uuid4

import logging

from plants_api.database import SessionLocal
from plants_api.model_base import SQLModel

logger = logging.getLogger(__name__)


class BaseTable(SQLModel):
    pk: UUID | None = Field(
        default_factory=uuid4,
        alias="id",
        primary_key=True,
        exclude=True,
    )

    def create(self, session: SessionLocal):
        logger.info("create in base class")

        session.add(self)
        session.commit()
        session.refresh(self)
        return self


class PlantBase(SQLModel):
    latin_name: str = Field(index=True, unique=True)
    min_germination_temp: int | None = Field(
        default=None,
        title="max germination temperature in f",
        gt=0,
        lt=100,
    )
    max_germination_temp: int | None = Field(default=None)
    min_soil_temp_transplant: int | None = Field(default=None)
    max_soil_temp_transplant: int | None = Field(default=None)


class Plant(PlantBase, BaseTable, table=True):
    pass


class PlantList:
    items: list[Plant]


class PlantCreate(PlantBase):
    # common_names: list["PlantName"] = Relationship(back_populates="plant")
    pass


class PlantUpdate(BaseTable, table=False):
    latin_name: str | None = None
    min_germination_temp: int | None = None
    max_germination_temp: int | None = None
    min_soil_temp_transplant: int | None = None
    max_soil_temp_transplant: int | None = None


class PlantListItem(SQLModel):
    pk: UUID
    latin_name: str


class PlantRead(PlantBase):
    # common_names: list["PlantName"] = Relationship(back_populates="plant")
    pk: UUID


# class PlantNameBase(SQLModel):
#     name: str = Field(index=True)

#     plant_id: UUID | None = Field(foreign_key="plant.id")

# class PlantName(BaseTable, PlantNameBase, table=True):
#     pass

# class PlantNameCreate(PlantNameBase):
#     plant: Plant | None = Relationship(back_populates="common_names")

# class PlantNameRead(PlantNameBase, BaseReader):
#     plant: Plant | None = Relationship(back_populates="common_names")
