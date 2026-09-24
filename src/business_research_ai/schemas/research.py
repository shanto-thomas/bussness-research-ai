from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):

    business_idea: str = Field(
        ...,
        min_length=5,
        description="Business idea provided by the user",
    )


class ResearchResponse(BaseModel):

    business_idea: str
    response: str