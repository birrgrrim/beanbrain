from .base import BaseScraper
from .madheads import MadHeadsScraper
from ..schemas import ScrapeResult

SCRAPERS: list[type[BaseScraper]] = [
    MadHeadsScraper,
]


async def scrape_url(url: str) -> ScrapeResult:
    for scraper_cls in SCRAPERS:
        if scraper_cls.can_handle(url):
            scraper = scraper_cls()
            return await scraper.scrape(url)
    raise ValueError(f"No scraper available for URL: {url}")
