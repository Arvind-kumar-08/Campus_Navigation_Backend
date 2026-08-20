from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=1000,
    )


class SourceResponse(BaseModel):
    document: str
    page: int | None = None


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]
    retrieved_chunks: int