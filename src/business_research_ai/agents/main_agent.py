from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.agents.specialist_tools import (
    analyze_finances,
    research_competitors,
    research_customers,
    research_legal,
    research_market,
    research_pricing,
    research_technology,
)
from business_research_ai.prompts.main_agent import MAIN_AGENT_PROMPT


def create_main_agent():
    return create_agent_instance(
        system_prompt=MAIN_AGENT_PROMPT,
        tools=[
            research_market,
            research_competitors,
            research_customers,
            research_pricing,
            analyze_finances,
            research_legal,
            research_technology,
        ],
        name="business_research_orchestrator",
    )


main_agent = create_main_agent()