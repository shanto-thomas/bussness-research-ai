from uuid import uuid4

from business_research_ai.schemas.research_session import (
    ChatMessage,
    ResearchSessionState,
)


_sessions: dict[str, ResearchSessionState] = {}


def create_session() -> ResearchSessionState:
    session_id = str(uuid4())

    session = ResearchSessionState(
        session_id=session_id
    )

    _sessions[session_id] = session

    return session


def get_session(
    session_id: str,
) -> ResearchSessionState:

    session = _sessions.get(session_id)

    if session is None:
        raise ValueError(
            f"Research session not found: {session_id}"
        )

    return session


def add_message(
    session: ResearchSessionState,
    role: str,
    content: str,
) -> None:

    session.conversation_history.append(
        ChatMessage(
            role=role,
            content=content,
        )
    )


def save_session(
    session: ResearchSessionState,
) -> ResearchSessionState:

    _sessions[session.session_id] = session

    return session