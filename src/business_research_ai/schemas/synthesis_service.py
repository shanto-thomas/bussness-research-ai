from pydantic import BaseModel, Field


class ResearchSection(BaseModel):
    summary: str = ""
    findings: list[str] = Field(
        default_factory=list
    )
    uncertainties: list[str] = Field(
        default_factory=list
    )


class SynthesizedResearch(BaseModel):

    business_summary: str = ""

    market: ResearchSection | None = None

    competitors: ResearchSection | None = None

    customers: ResearchSection | None = None

    pricing: ResearchSection | None = None

    finance: ResearchSection | None = None

    legal: ResearchSection | None = None

    technology: ResearchSection | None = None

    opportunities: list[str] = Field(
        default_factory=list
    )

    risks: list[str] = Field(
        default_factory=list
    )

    assumptions: list[str] = Field(
        default_factory=list
    )

    missing_information: list[str] = Field(
        default_factory=list
    )

    conflicting_information: list[str] = Field(
        default_factory=list
    )