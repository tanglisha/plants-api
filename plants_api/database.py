from functools import lru_cache
from typing import Iterable, Iterator
from pytest import param
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from sqlmodel.ext.asyncio.session import AsyncSession
import os


import logging

logger = logging.getLogger(__name__)


DATABASE_URL = os.environ.get("DATABASE_URL", "db")

db_name="app"
user="postgres"
password="postgres"

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
    def __init__(self):
        print("creating real database session")
        
    def __new__(cls):
        # Sets up the current session with the engine info
        session = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine())
        
        return session()
        
    @classmethod
    def _engine(cls) -> Engine:
        result = create_engine(
            url=f"postgresql+pg8000://{user}:{password}@{DATABASE_URL}/{db_name}",
            echo=True,
        )
        return result
    
    @classmethod
    def init_db(cls):
        with cls._engine().begin() as conn:
            SQLModel.metadata.create_all(conn)
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
   