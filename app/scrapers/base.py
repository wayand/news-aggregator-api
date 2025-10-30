from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as Soup
import requests
import hashlib


class BaseScraper(ABC):
    """Abstract base class for all news scrapers"""

    def __init__(self, base_url: str, timezone: str = 'Europe/Copenhagen'):
        self.base_url = base_url
        self.timezone = timezone
        self.headers = self._get_default_headers()

    def _get_default_headers(self) -> dict:
        """Returns default HTTP headers for requests"""
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "da,en-US;q=0.9,en;q=0.8,fi;q=0.7,nb;q=0.6,sv;q=0.5,fr;q=0.4,fa;q=0.3,de;q=0.2",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }

    def _fetch_html(self, url: str) -> Soup:
        """Fetches and parses HTML from the given URL"""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return Soup(response.content, 'html.parser')

    @abstractmethod
    def scrape_pages(self, page: str) -> dict:
        """
        Scrape available pages/categories from the news site

        Args:
            page: The page identifier (e.g., 'world', 'business')

        Returns:
            Dictionary with total, page, and items list
        """
        pass

    @abstractmethod
    def scrape_feeds(self, page: str, category: str, subcategory: str) -> dict:
        """
        Scrape news feeds from a specific page and category

        Args:
            page: The page identifier
            category: The category identifier
            subcategory: The subcategory identifier if any

        Returns:
            Dictionary with total, source, page, category, subcategory and items list
        """
        pass

    def get_source_name(self) -> str:
        """Returns the name of the news source"""
        return self.__class__.__name__.replace('Scraper', '').lower()

    def generate_article_id(self, link: str, fallback_index: int = None) -> str:
        """
        Generate a deterministic ID for an article

        Args:
            link: Article link/URL
            fallback_index: Index to use if link is invalid

        Returns:
            A unique identifier for the article
        """
        if link and link not in ['NO-Link-Found', None, '']:
            # Use content-based hash for deduplication
            content = f"{self.base_url}:{link}"
            return hashlib.sha256(content.encode()).hexdigest()[:16]
        elif fallback_index is not None:
            # Fallback to enumeration
            return f"{self.get_source_name()}_{fallback_index}"
        else:
            return None

    def generate_page_id(self, name: str, page: str) -> str:
        """
        Generate a deterministic ID for a page/category item

        Args:
            name: Category name
            page: Page identifier

        Returns:
            A unique identifier for the page item
        """
        content = f"{self.base_url}:{page}:{name}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]
