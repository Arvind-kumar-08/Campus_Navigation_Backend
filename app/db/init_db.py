from sqlalchemy import text
from sqlmodel import SQLModel

from app.db.database import engine

# Important imports so metadata sees these tables
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def init_db():
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS vector"
            )
        )

    SQLModel.metadata.create_all(engine)

    print("Database initialized successfully.")