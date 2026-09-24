from typing import Any

from ddgs import DDGS

from business_research_ai.tools.providers.base import SearchProvider


class DDGSProvider(SearchProvider):
    """Search provider implementation using DDGS."""

    def __init__(self) -> None:
        self.client = DDGS()

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            return []

        results = self.client.text(
            query,
            max_results=max_results,
        )

        return list(results or [])

    def news_search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            return []

        results = self.client.news(
            query,
            max_results=max_results,
        )

        return list(results or [])

    def business_search(
        self,
        query: str,
        max_results: int = 3,
    ) -> list[dict[str, Any]]:
        """
        DDGS does not provide a dedicated Google-Maps-style
        business API, so business discovery currently uses
        local/business-focused web search.
        """

        if not query.strip():
            return []

        business_query = f"{query} businesses locations ratings reviews"

        results = self.client.text(
            business_query,
            max_results=max_results,
        )

        return list(results or [])