from langchain_openai import ChatOpenAI

from business_research_ai.config import settings


def get_openai_model() -> ChatOpenAI:
    """
    Create and return the configured OpenAI chat model.
    """

    return ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
        timeout=settings.llm_timeout,
        max_retries=settings.llm_max_retries,
        use_responses_api=True,
        output_version="responses/v1",
    )