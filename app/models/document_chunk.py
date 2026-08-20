from sqlalchemy import Text
from pgvector.sqlalchemy import VECTOR
from sqlmodel import SQLModel, Field


class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunks"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    document_id: int = Field(
        foreign_key="documents.id",
        index=True,
    )

    page_number: int | None = None

    chunk_index: int

    content: str = Field(
        sa_type=Text,
    )

    embedding: list[float] | None = Field(
        default=None,
        sa_type=VECTOR(768),
        nullable=True,
    )