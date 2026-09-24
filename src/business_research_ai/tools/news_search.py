from langchain.tools import tool

from business_research_ai.tools.providers import search_provider


@tool
def news_search(query: str) -> str:
    """
    Search recent news related to a business, market,
    competitor, industry, policy, or technology.
    """

    if not query.strip():
        return "News search query cannot be empty."

    try:
        results = search_provider.news_search(
            query=query,
            max_results=5,
        )

        if not results:
            return "No news results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            formatted_results.append(
                f"""
News Result {index}

Title: {result.get("title", "")}
URL: {result.get("url", result.get("href", ""))}
Source: {result.get("source", "")}
Published: {result.get("date", "")}
Summary: {result.get("body", "")}
""".strip()
            )

        return "\n\n".join(formatted_results)

    except Exception as exc:
        return f"News search failed: {exc}"