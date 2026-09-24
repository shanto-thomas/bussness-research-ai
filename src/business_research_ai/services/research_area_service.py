from business_research_ai.agents.specialist_tools import (
    analyze_finances,
    research_competitors,
    research_customers,
    research_legal,
    research_market,
    research_pricing,
    research_technology,
)


RESEARCH_TOOLS = {
    "market": research_market,
    "competitors": research_competitors,
    "customers": research_customers,
    "pricing": research_pricing,
    "finance": analyze_finances,
    "legal": research_legal,
    "technology": research_technology,
}


def run_research_area(
    area: str,
    business_idea: str,
) -> str:

    tool = RESEARCH_TOOLS.get(area)

    if tool is None:
        raise ValueError(
            f"Unsupported research area: {area}"
        )

    result = tool.invoke(
        {
            "business_idea": business_idea
        }
    )

    return result