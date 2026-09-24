from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.agents.specialist_middleware import (
    build_specialist_middleware,
)
from business_research_ai.prompts.finance_agent import FINANCE_AGENT_PROMPT
from business_research_ai.tools import web_search


def create_finance_agent():
    return create_agent_instance(
        system_prompt=FINANCE_AGENT_PROMPT,
        tools=[
            web_search,
        ],
        middleware=build_specialist_middleware(),
        name="financial_analysis_agent",
    )


finance_agent = create_finance_agent()