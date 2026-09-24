from fastapi import FastAPI

from business_research_ai.config import settings
from business_research_ai.logging import configure_logging
from business_research_ai.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)
from business_research_ai.services.research_service import (
    research_business,
)
from business_research_ai.api.routes.research_session import (
    router as research_session_router,
)

configure_logging()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AI Business Research & Validation Platform",
)


@app.get("/")
def root():
    return {
        "message": "Business Research AI API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


@app.post(
    "/api/v1/research",
    response_model=ResearchResponse,
)
def create_research(
    request: ResearchRequest,
):
    return research_business(request)

app.include_router(
    research_session_router
)