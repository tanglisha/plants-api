import logging

from fastapi import FastAPI
from plants_api.router import router as plants_router

logger = logging.getLogger(__name__)


def get_app():
    app = FastAPI(
        title="Plants",
        debug=True,
    )
    app.include_router(plants_router)
    return app


app = get_app()
