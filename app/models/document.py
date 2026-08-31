from datetime import datetime

from sqlalchemy import LargeBinary, Text
from sqlmodel import SQLModel, Field
class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    title: str

    filename: str

    file_type: str = "pdf"

    file_data: bytes = Field(
        sa_type=LargeBinary,
    )

    extracted_text: str | None = Field(
        default=None,
        sa_type=Text,
    )

    uploaded_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    is_active: bool = True