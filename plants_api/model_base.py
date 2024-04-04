from sqlmodel import SQLModel as _SQLModel
from sqlalchemy.orm import declared_attr

from plants_api.utils import snake_case


class SQLModel(_SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return snake_case(cls.__name__)
