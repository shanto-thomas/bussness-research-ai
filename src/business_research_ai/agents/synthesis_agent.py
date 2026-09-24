from business_research_ai.agents.factory import create_agent_instance
from business_research_ai.prompts.synthesis_agent import SYNTHESIS_AGENT_PROMPT


def create_synthesis_agent():
    return create_agent_instance(
        system_prompt=SYNTHESIS_AGENT_PROMPT,
        tools=[],
        name="research_synthesizer",
    )


synthesis_agent = create_synthesis_agent()