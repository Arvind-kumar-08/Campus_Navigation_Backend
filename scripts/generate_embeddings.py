from sqlmodel import Session, select

from app.db.database import engine
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import (
    generate_document_embedding,
)


def main():
    with Session(engine) as session:

        chunks = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.embedding == None
            )
        ).all()

        if not chunks:
            print(
                "No chunks without embeddings found."
            )
            return

        print(
            f"Found {len(chunks)} chunks "
            "without embeddings."
        )

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):
            try:
                document = session.get(
                    Document,
                    chunk.document_id,
                )

                title = (
                    document.title
                    if document
                    else None
                )

                embedding = (
                    generate_document_embedding(
                        text=chunk.content,
                        title=title,
                    )
                )

                chunk.embedding = embedding

                session.add(chunk)

                # Commit periodically
                if index % 10 == 0:
                    session.commit()

                print(
                    f"[{index}/{len(chunks)}] "
                    f"Embedded chunk {chunk.id}"
                )

            except Exception as error:
                session.rollback()

                print(
                    f"Failed chunk {chunk.id}"
                )

                print(
                    f"Error: {error}"
                )

        session.commit()

        print(
            "Embedding generation completed."
        )


if __name__ == "__main__":
    main()