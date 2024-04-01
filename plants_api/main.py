from fastapi import FastAPI
from plants_api.database import SessionLocal
from plants_api.router import router as plants_router

import logging

logger = logging.getLogger(__name__)

def get_app():
    app = FastAPI(
        title="Plants",
        debug=True,
    )
    app.include_router(plants_router)
    return app

app = get_app()


SessionLocal.init_db()
