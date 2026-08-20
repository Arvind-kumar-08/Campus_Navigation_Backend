from app.services.embedding_service import (
    generate_document_embedding,
)


def main():
    text = (
        "Students are expected to follow "
        "the institute code of conduct."
    )

    embedding = generate_document_embedding(
        text=text,
        title="Student Conduct",
    )

    print(
        "Embedding dimension:",
        len(embedding),
    )

    print(
        "First 5 values:",
        embedding[:5],
    )


if __name__ == "__main__":
    main()