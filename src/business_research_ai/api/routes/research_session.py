from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from business_research_ai.services.conversation_service import (
    process_message,
)
from business_research_ai.services.session_service import (
    create_session,
    get_session,
)


router = APIRouter(
    prefix="/api/v1/research",
    tags=["Research"],
)


class MessageRequest(BaseModel):
    message: str


@router.post("/session")
def create_research_session():

    session = create_session()

    return {
        "session_id": session.session_id,
        "status": session.status,
    }


@router.post("/session/{session_id}/message")
def send_message(
    session_id: str,
    request: MessageRequest,
):

    try:
        return process_message(
            session_id=session_id,
            message=request.message,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get("/session/{session_id}")
def get_research_session(
    session_id: str,
):

    try:
        session = get_session(session_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    return session