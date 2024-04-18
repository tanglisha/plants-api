import logging
from uuid import UUID
from uuid import uuid4

from plants_api.model_base import SQLModel
from sqlalchemy import UniqueConstraint
from sqlmodel import Field
from sqlmodel import Relationship

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
    common_names: list["CommonName"] = Relationship(back_populates="plant")


class PlantCreate(PlantBase):
    _sa_instance_state = None

    common_names: list[str] = Field(default=[])


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
    pk: UUID

    common_names: list["CommonNameRead"] = []


class CommonNameBase(SQLModel):
    name: str = Field(index=True)

    plant_id: UUID = Field(foreign_key="plant.pk", nullable=False)


class CommonName(BaseTable, CommonNameBase, table=True):
    __table_args__ = (UniqueConstraint("plant_id", "name"),)
    plant: Plant = Relationship(back_populates="common_names")


class CommonNameCreate(SQLModel):
    name: str = Field(index=True)
    plant_id: UUID | None = Field(foreign_key="plant.pk")


class CommonNameRead(SQLModel):
    name: str = Field(index=True)
