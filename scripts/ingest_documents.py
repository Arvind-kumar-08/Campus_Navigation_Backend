from pathlib import Path

from sqlmodel import Session, select

from app.db.database import engine
from app.models.document import Document

from app.services.pdf_service import extract_pdf_pages
from app.services.chunk_service import split_text
from app.services.document_service import (
    create_document,
    create_document_chunk,
)


DOCUMENTS_FOLDER = Path("documents")


def ingest_document(
    session: Session,
    file_path: Path,
):
    print(
        f"\nProcessing: {file_path.name}"
    )

    # Avoid duplicate ingestion
    existing_document = session.exec(
        select(Document).where(
            Document.filename == file_path.name
        )
    ).first()

    if existing_document:
        print(
            f"Skipping {file_path.name} "
            "- already exists in database."
        )
        return

    pages = extract_pdf_pages(
        str(file_path)
    )

    if not pages:
        print(
            f"No readable text found in "
            f"{file_path.name}"
        )
        return

    full_text = "\n\n".join(
        page["text"]
        for page in pages
    )

    document = create_document(
        session=session,
        file_path=str(file_path),
        extracted_text=full_text,
    )

    chunk_index = 0

    for page in pages:
        page_number = page[
            "page_number"
        ]

        page_text = page[
            "text"
        ]

        chunks = split_text(
            text=page_text,
            chunk_size=1000,
            overlap=150,
        )

        for chunk_text in chunks:
            create_document_chunk(
                session=session,
                document_id=document.id,
                page_number=page_number,
                chunk_index=chunk_index,
                content=chunk_text,
            )

            chunk_index += 1

    session.commit()

    print(
        f"Document stored successfully."
    )

    print(
        f"Total chunks created: "
        f"{chunk_index}"
    )


def main():
    if not DOCUMENTS_FOLDER.exists():
        print(
            "Documents folder does not exist."
        )
        return

    pdf_files = list(
        DOCUMENTS_FOLDER.glob("*.pdf")
    )

    if not pdf_files:
        print(
            "No PDF files found in documents/."
        )
        return

    print(
        f"Found {len(pdf_files)} PDF files."
    )

    with Session(engine) as session:
        for pdf_file in pdf_files:
            try:
                ingest_document(
                    session,
                    pdf_file,
                )

            except Exception as error:
                session.rollback()

                print(
                    f"Failed to process "
                    f"{pdf_file.name}"
                )

                print(
                    f"Error: {error}"
                )


if __name__ == "__main__":
    main()