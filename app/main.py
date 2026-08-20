
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.init_db import init_db


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.on_event("startup")
def startup_event():

    init_db()


app.include_router(api_router)


@app.get("/")
def root():

    return {
        "message": "RGIPT Campus RAG Backend is running"
    }