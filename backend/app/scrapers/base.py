from abc import ABC, abstractmethod

from ..schemas import ScrapeResult


class BaseScraper(ABC):
    @staticmethod
    @abstractmethod
    def can_handle(url: str) -> bool:
        """Return True if this scraper can handle the given URL."""

    @abstractmethod
    async def scrape(self, url: str) -> ScrapeResult:
        """Scrape product data from the URL."""
