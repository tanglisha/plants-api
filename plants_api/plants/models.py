import logging
from uuid import UUID
from uuid import uuid4

from plants_api.model_base import SQLModel
from sqlmodel import Field

# from sqlalchemy.dialects.postgresql import UUID

logger = logging.getLogger(__name__)


class BaseTable(SQLModel):
    pk: UUID | None = Field(
        default_factory=uuid4,
        alias="id",
        primary_key=True,
        exclude=True,
    )


class PlantBase(SQLModel):
    latin_name: str = Field(index=True, unique=True)
    min_germination_temp: int | None = Field(
        default=None,
        title="max germination temperature in f",
        ge=0,
        le=100,
        nullable=True,
    )
    max_germination_temp: int | None = Field(
        default=None,
        title="min germination temp in f",
        ge=0,
        le=100,
        nullable=True,
    )
    min_soil_temp_transplant: int | None = Field(
        default=None,
        title="min soil temp for transplaning in f",
        ge=0,
        le=100,
        nullable=True,
    )
    max_soil_temp_transplant: int | None = Field(
        default=None,
        title="max germination temp for transplanting in f",
        ge=0,
        le=100,
        nullable=True,
    )


class Plant(PlantBase, BaseTable, table=True):
    pass


class PlantCreate(PlantBase):
    min_germination_temp: int | None = None
    # common_names: list["PlantName"] = Relationship(back_populates="plant")


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
