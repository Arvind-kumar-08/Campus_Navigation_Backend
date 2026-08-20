
from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import engine


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health_check():

    try:

        with engine.connect() as connection:

            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception as error:

        return {
            "status": "error",
            "database": "disconnected",
            "message": str(error),
        }