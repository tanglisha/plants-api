import logging
import os

from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

logger = logging.getLogger(__name__)


DATABASE_URL = os.environ.get("DATABASE_URL", "db")

db_name = "app"
user = "postgres"
password = "postgres"

Base = declarative_base()


class SessionLocal(Session):
    """Database Session

    Compatible with a with block, closes when you exit the block

    Example:
        with SessionLocal() as conn:
            conn.exec()

        @router.get()
        def get(db=Depends(SessionLocal))
    """

    def __new__(cls):
        # Sets up the current session with the engine info
        return cls._create_session()

    @classmethod
    def _create_session(cls):
        return sessionmaker(autocommit=False, autoflush=False, bind=cls._engine())()

    @classmethod
    def connection_url(cls) -> str:
        return f"postgresql+pg8000://{user}:{password}@{DATABASE_URL}/{db_name}"

    @classmethod
    def _engine(cls) -> Engine:
        result = create_engine(
            url=cls.connection_url(),
            echo=True,
        )
        return result


engine = create_engine(
    url=f"postgresql+pg8000://{user}:{password}@{DATABASE_URL}/{db_name}",
    echo=True,
)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db():
    # session = SessionLocal()
    with LocalSession() as session:
        try:
            yield session
        finally:
            session.close()
