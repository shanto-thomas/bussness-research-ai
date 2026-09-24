from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.agents.specialist_middleware import (
    build_specialist_middleware,
)
from business_research_ai.prompts.market_agent import MARKET_AGENT_PROMPT
from business_research_ai.tools import (
    web_search,
    news_search,
    website_reader,
)


def create_market_agent():
    return create_agent_instance(
        system_prompt=MARKET_AGENT_PROMPT,
        tools=[
            web_search,
            news_search,
            website_reader,
        ],
        middleware=build_specialist_middleware(),
        name="market_research_agent",
    )


market_agent = create_market_agent()