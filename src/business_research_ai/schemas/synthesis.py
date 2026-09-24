from pydantic import BaseModel, Field


class ResearchSection(BaseModel):
    summary: str = ""
    findings: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)


class SynthesizedResearch(BaseModel):
    business_summary: str = ""

    market: ResearchSection
    competitors: ResearchSection
    customers: ResearchSection
    pricing: ResearchSection
    finance: ResearchSection
    legal: ResearchSection
    technology: ResearchSection

    opportunities: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)

    assumptions: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    conflicting_information: list[str] = Field(default_factory=list)