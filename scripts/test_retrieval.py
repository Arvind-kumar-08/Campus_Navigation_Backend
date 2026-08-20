from sqlmodel import Session

from app.db.database import engine
from app.services.retrieval_service import (
    retrieve_relevant_chunks,
)


def main():

    question = input(
        "Ask a question: "
    )

    with Session(engine) as session:

        chunks = retrieve_relevant_chunks(
            session=session,
            question=question,
            top_k=5,
        )

        print(
            "\nTop relevant chunks:\n"
        )

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):
            print(
                f"--- RESULT {index} ---"
            )

            print(
                f"Document ID: "
                f"{chunk.document_id}"
            )

            print(
                f"Page: "
                f"{chunk.page_number}"
            )

            print(
                f"Chunk: "
                f"{chunk.chunk_index}"
            )

            print()

            print(
                chunk.content[:500]
            )

            print()


if __name__ == "__main__":
    main()