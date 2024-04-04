from plants_api.utils import snake_case
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel as _SQLModel


class SQLModel(_SQLModel):
    @declared_attr  # type:ignore
    def __tablename__(cls) -> str:  # type:ignore
        return snake_case(cls.__name__)
