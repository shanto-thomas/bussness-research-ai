from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.prompts.report_agent import (
    REPORT_AGENT_PROMPT,
)


def create_report_agent():
    return create_agent_instance(
        system_prompt=REPORT_AGENT_PROMPT,
        tools=[],
        name="business_report_generator",
    )


report_agent = create_report_agent()