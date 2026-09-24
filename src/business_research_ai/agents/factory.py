from collections.abc import Sequence

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_core.tools import BaseTool

from business_research_ai.llm.openai import get_openai_model


def create_agent_instance(
    *,
    system_prompt: str,
    tools: Sequence[BaseTool] | None = None,
    middleware: Sequence[AgentMiddleware] | None = None,
    name: str | None = None,
):
    """
    Create a LangChain agent using the shared OpenAI model.

    Args:
        system_prompt: Instructions for the agent.
        tools: Tools available to the agent.
        middleware: Middleware applied around model and tool calls.
        name: Optional agent name.

    Returns:
        Configured LangChain agent.
    """

    model = get_openai_model()

    agent = create_agent(
        model=model,
        tools=list(tools or []),
        system_prompt=system_prompt,
        middleware=list(middleware or []),
        name=name,
    )

    return agent