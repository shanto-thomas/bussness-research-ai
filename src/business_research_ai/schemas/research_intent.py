from typing import Literal

from pydantic import BaseModel


ResearchIntentType = Literal[
    "business_understanding",
    "market",
    "competitors",
    "customers",
    "pricing",
    "finance",
    "legal",
    "technology",
    "complete_research",
    "generate_report",
    "unknown",
]


class ResearchIntent(BaseModel):
    intent: ResearchIntentType

    message: str