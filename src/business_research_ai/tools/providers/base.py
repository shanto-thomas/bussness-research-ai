from abc import ABC, abstractmethod
from typing import Any


class SearchProvider(ABC):
    """Abstract interface for search providers."""

    @abstractmethod
    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """Perform a general web search."""
        raise NotImplementedError

    @abstractmethod
    def news_search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """Perform a news search."""
        raise NotImplementedError

    @abstractmethod
    def business_search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """Search for businesses."""
        raise NotImplementedError