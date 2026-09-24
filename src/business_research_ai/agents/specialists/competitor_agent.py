from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.agents.specialist_middleware import (
    build_specialist_middleware,
)
from business_research_ai.prompts.competitor_agent import COMPETITOR_AGENT_PROMPT
from business_research_ai.tools import (
    web_search,
    business_search,
    website_reader,
)


def create_competitor_agent():
    return create_agent_instance(
        system_prompt=COMPETITOR_AGENT_PROMPT,
        tools=[
            web_search,
            business_search,
            website_reader,
        ],
        middleware=build_specialist_middleware(),
        name="competitor_research_agent",
    )


competitor_agent = create_competitor_agent()