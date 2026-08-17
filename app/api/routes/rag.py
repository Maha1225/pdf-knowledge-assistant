from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.rag.service import answer_question
from app.schemas.ask import AskRequest, AskResponse


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/ask",
    response_model=AskResponse,
)
def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db),
):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    return answer_question(
        db=db,
        question=question,
        limit=request.limit,
    )
