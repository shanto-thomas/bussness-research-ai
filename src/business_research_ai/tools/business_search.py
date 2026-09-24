from langchain.tools import tool

from business_research_ai.tools.providers import search_provider


@tool
def business_search(query: str) -> str:
    """
    Search for real-world businesses and local competitors.

    Use this for:
    - local businesses
    - restaurants
    - shops
    - service providers
    - competitor locations
    - local market discovery
    """

    if not query.strip():
        return "Business search query cannot be empty."

    try:
        results = search_provider.business_search(
            query=query,
            max_results=5,
        )

        if not results:
            return "No businesses found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            formatted_results.append(
                f"""
Business Result {index}

Name/Title: {result.get("title", "")}
URL: {result.get("href", result.get("url", ""))}
Description: {result.get("body", result.get("snippet", ""))}
""".strip()
            )

        return "\n\n".join(formatted_results)

    except Exception as exc:
        return f"Business search failed: {exc}"