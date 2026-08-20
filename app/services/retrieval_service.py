from sqlalchemy import select
from sqlmodel import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import (
    generate_query_embedding,
)


MAX_COSINE_DISTANCE = 0.45


def retrieve_relevant_chunks(
    session: Session,
    question: str,
    top_k: int = 5,
):
    query_embedding = generate_query_embedding(
        question
    )

    distance = (
        DocumentChunk.embedding
        .cosine_distance(
            query_embedding
        )
        .label("distance")
    )

    statement = (
        select(
            DocumentChunk,
            distance,
        )
        .where(
            DocumentChunk.embedding != None
        )
        .order_by(distance)
        .limit(top_k)
    )

    results = session.exec(
        statement
    ).all()

    filtered_results = []

    for chunk, score in results:
        if score <= MAX_COSINE_DISTANCE:
            filtered_results.append(
                (chunk, score)
            )

    return filtered_results