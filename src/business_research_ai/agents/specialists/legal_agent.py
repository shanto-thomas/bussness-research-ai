from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.agents.specialist_middleware import (
    build_specialist_middleware,
)
from business_research_ai.prompts.legal_agent import LEGAL_AGENT_PROMPT
from business_research_ai.tools import (
    web_search,
    news_search,
    website_reader,
)


def create_legal_agent():
    return create_agent_instance(
        system_prompt=LEGAL_AGENT_PROMPT,
        tools=[
            web_search,
            news_search,
            website_reader,
        ],
        middleware=build_specialist_middleware(),
        name="legal_research_agent",
    )


legal_agent = create_legal_agent()