from typing import Any

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ResearchSessionState(BaseModel):
    session_id: str

    business_idea: str | None = None

    conversation_history: list[ChatMessage] = Field(
        default_factory=list
    )

    selected_areas: list[str] = Field(
        default_factory=list
    )

    completed_areas: list[str] = Field(
        default_factory=list
    )

    research_results: dict[str, str] = Field(
        default_factory=dict
    )

    current_step: str = "business_understanding"

    status: str = "active"

    synthesized_research: dict[str, Any] | None = None

    final_report: dict[str, Any] | None = None

    pdf_path: str | None = None