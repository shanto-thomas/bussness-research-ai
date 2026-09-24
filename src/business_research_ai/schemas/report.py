from pydantic import BaseModel, Field


class ReportSection(BaseModel):
    title: str
    content: str


class BusinessResearchReport(BaseModel):
    title: str
    executive_summary: str
    business_overview: str

    sections: list[ReportSection] = Field(default_factory=list)

    opportunities: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    conflicting_information: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)