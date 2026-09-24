from langchain.tools import tool

from business_research_ai.tools.providers import search_provider


@tool
def web_search(query: str) -> str:
    """
    Search the web for current general information.

    Use this tool for:
    - market information
    - industry trends
    - statistics
    - general business information
    - competitor discovery
    """

    if not query.strip():
        return "Search query cannot be empty."

    try:
        results = search_provider.search(
            query=query,
            max_results=5,
        )

        if not results:
            return "No search results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            formatted_results.append(
                f"""
Result {index}

Title: {result.get("title", "")}
URL: {result.get("href", result.get("url", ""))}
Summary: {result.get("body", result.get("snippet", ""))}
""".strip()
            )

        return "\n\n".join(formatted_results)

    except Exception as exc:
        return f"Web search failed: {exc}"