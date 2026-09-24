from business_research_ai.agents.factory import (
    create_agent_instance,
)
from business_research_ai.prompts.research_router import (
    RESEARCH_ROUTER_PROMPT,
)


def create_research_router():
    return create_agent_instance(
        system_prompt=RESEARCH_ROUTER_PROMPT,
        tools=[],
        name="research_router",
    )


research_router = create_research_router()