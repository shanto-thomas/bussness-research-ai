from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.agents.specialist_middleware import (
    build_specialist_middleware,
)
from business_research_ai.prompts.technology_agent import (
    TECHNOLOGY_AGENT_PROMPT,
)
from business_research_ai.tools import (
    web_search,
    website_reader,
)


def create_technology_agent():
    return create_agent_instance(
        system_prompt=TECHNOLOGY_AGENT_PROMPT,
        tools=[
            web_search,
            website_reader,
        ],
        middleware=build_specialist_middleware(),
        name="technology_research_agent",
    )


technology_agent = create_technology_agent()