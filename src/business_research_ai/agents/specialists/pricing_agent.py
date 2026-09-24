from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.agents.specialist_middleware import (
    build_specialist_middleware,
)
from business_research_ai.prompts.pricing_agent import PRICING_AGENT_PROMPT
from business_research_ai.tools import (
    web_search,
    business_search,
    website_reader,
)


def create_pricing_agent():
    return create_agent_instance(
        system_prompt=PRICING_AGENT_PROMPT,
        tools=[
            web_search,
            business_search,
            website_reader,
        ],
        middleware=build_specialist_middleware(),
        name="pricing_research_agent",
    )


pricing_agent = create_pricing_agent()