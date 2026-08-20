from google import genai
from google.genai import types

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)


EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSION = 768


def generate_document_embedding(
    text: str,title: str | None = None,) -> list[float]:
    """
    Generate an embedding for a stored document chunk.
    """

    if not text.strip():
        raise ValueError(
            "Cannot create embedding for empty text."
        )

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            title=title,
            output_dimensionality=EMBEDDING_DIMENSION,
        ),
    )

    if not result.embeddings:
        raise RuntimeError(
            "Gemini returned no embeddings."
        )

    return result.embeddings[0].values


def generate_query_embedding(
    text: str,
) -> list[float]:
    """
    Generate an embedding for a user's search query.
    """

    if not text.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIMENSION,
        ),
    )

    if not result.embeddings:
        raise RuntimeError(
            "Gemini returned no query embedding."
        )

    return result.embeddings[0].values