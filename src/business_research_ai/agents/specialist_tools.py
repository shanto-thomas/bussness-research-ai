from langchain.tools import tool

from business_research_ai.agents.specialists import (
    competitor_agent,
    customer_agent,
    finance_agent,
    legal_agent,
    market_agent,
    pricing_agent,
    technology_agent,
)
from business_research_ai.utils.text import extract_text_content


def invoke_agent(agent, business_idea: str) -> str:
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": business_idea,
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    return extract_text_content(
        final_message.content
    )


@tool
def research_market(business_idea: str) -> str:
    """
    Delegate market research to the Market Research Agent.
    """

    return invoke_agent(
        market_agent,
        business_idea,
    )


@tool
def research_competitors(business_idea: str) -> str:
    """
    Delegate competitor research to the Competitor Research Agent.
    """

    return invoke_agent(
        competitor_agent,
        business_idea,
    )


@tool
def research_customers(business_idea: str) -> str:
    """
    Delegate customer research to the Customer Research Agent.
    """

    return invoke_agent(
        customer_agent,
        business_idea,
    )


@tool
def research_pricing(business_idea: str) -> str:
    """
    Delegate pricing research to the Pricing Research Agent.
    """

    return invoke_agent(
        pricing_agent,
        business_idea,
    )


@tool
def analyze_finances(business_idea: str) -> str:
    """
    Delegate financial analysis to the Financial Analysis Agent.
    """

    return invoke_agent(
        finance_agent,
        business_idea,
    )


@tool
def research_legal(business_idea: str) -> str:
    """
    Delegate legal and regulatory research to the Legal Research Agent.
    """

    return invoke_agent(
        legal_agent,
        business_idea,
    )


@tool
def research_technology(business_idea: str) -> str:
    """
    Delegate technology research to the Technology Research Agent.
    """

    return invoke_agent(
        technology_agent,
        business_idea,
    )