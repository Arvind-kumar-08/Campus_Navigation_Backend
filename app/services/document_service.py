from pathlib import Path

from sqlmodel import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def create_document( session: Session,file_path: str,extracted_text: str,) -> Document:
    path = Path(file_path)

    with open(file_path, "rb") as file:
        file_bytes = file.read()

    document = Document(
        title=path.stem.replace("_", " "),
        filename=path.name,
        file_type=path.suffix.lower().replace(".", ""),
        file_data=file_bytes,
        extracted_text=extracted_text,
        is_active=True,
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    return document


def create_document_chunk(session: Session,document_id: int,page_number: int,chunk_index: int,content: str,) -> DocumentChunk:
    chunk = DocumentChunk(
        document_id=document_id,
        page_number=page_number,
        chunk_index=chunk_index,
        content=content,

        # embeddings will be added in Phase 1C
        embedding=None,
    )

    session.add(chunk)

    return chunk