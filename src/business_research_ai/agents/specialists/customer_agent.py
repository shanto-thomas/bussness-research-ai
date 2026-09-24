from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.agents.specialist_middleware import (
    build_specialist_middleware,
)
from business_research_ai.prompts.customer_agent import CUSTOMER_AGENT_PROMPT
from business_research_ai.tools import (
    web_search,
    news_search,
)


def create_customer_agent():
    return create_agent_instance(
        system_prompt=CUSTOMER_AGENT_PROMPT,
        tools=[
            web_search,
            news_search,
        ],
        middleware=build_specialist_middleware(),
        name="customer_research_agent",
    )


customer_agent = create_customer_agent()