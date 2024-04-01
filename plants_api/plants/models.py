import logging
from typing import TYPE_CHECKING
from unittest.mock import Base
import pg8000
from pydantic import UUID4, computed_field
from pytest import param
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as sa_UUID
from sqlmodel import Field, Relationship, SQLModel, Session
from uuid import UUID, uuid4

import logging

from plants_api.database import SessionLocal

logger = logging.getLogger(__name__)


class BaseTable(SQLModel):
    pk: UUID | None = Field(
        default_factory=uuid4,
        alias="id",
        primary_key=True,
        exclude=True,
    )

    def create(self):
        logger.info("create in base class")

        # if not self.id:
        # self.id = uuid4()
        with SessionLocal() as session:
            session.add(self)
            session.commit()
            session.refresh(self)
        return self


class BaseReader(SQLModel):
    pk: UUID = Field(
        default_factory=uuid4,
        alias="id",
        primary_key=True,
        # exclude=True,
    )


class PlantBase(SQLModel):
    latin_name: str = Field(index=True, unique=True)
    min_germination_temp: int | None = Field(default=None)
    max_germination_temp: int | None = Field(default=None)
    min_soil_temp_transplant: int | None = Field(default=None)
    max_soil_temp_transplant: int | None = Field(default=None)


class Plant(BaseTable, PlantBase, table=True):
    pass


class PlantList:
    items: list[Plant]


class PlantCreate(PlantBase):
    # common_names: list["PlantName"] = Relationship(back_populates="plant")
    pass


class PlantListItem(BaseReader):
    latin_name: str = Field(index=True, unique=True)


class PlantRead(BaseReader, PlantBase):
    # common_names: list["PlantName"] = Relationship(back_populates="plant")
    pass


# class PlantNameBase(SQLModel):
#     name: str = Field(index=True)

#     plant_id: UUID | None = Field(foreign_key="plant.id")

# class PlantName(BaseTable, PlantNameBase, table=True):
#     pass

# class PlantNameCreate(PlantNameBase):
#     plant: Plant | None = Relationship(back_populates="common_names")

# class PlantNameRead(PlantNameBase, BaseReader):
#     plant: Plant | None = Relationship(back_populates="common_names")
