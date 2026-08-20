from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
)
from app.services.rag_service import (
    generate_rag_answer,
)


router = APIRouter(
    prefix="/api/chat",
    tags=["AI Guide"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    session: Session = Depends(
        get_session
    ),
):
    try:
        result = generate_rag_answer(
            session=session,
            question=request.question,
        )

        return result

    except Exception as error:
        print(
            "Chat API error:",
            error,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate "
                "AI response."
            ),
        )