from app.scrapers.base import BaseScraper
from app.scrapers.reuters import ReutersScraper
from app.scrapers.bbc import BBCScraper


class ScraperFactory:
    """Factory class to create and manage news scrapers"""
    
    _scrapers = {
        'reuters': ReutersScraper,
        'bbc': BBCScraper,
    }
    
    @classmethod
    def get_scraper(cls, source: str) -> BaseScraper:
        """
        Get a scraper instance for the specified news source
        
        Args:
            source: The name of the news source (e.g., 'reuters', 'bbc')
            
        Returns:
            An instance of the appropriate scraper class
            
        Raises:
            ValueError: If the source is not supported
        """
        scraper_class = cls._scrapers.get(source.lower())
        if not scraper_class:
            available = ', '.join(cls._scrapers.keys())
            raise ValueError(
                f"Unknown source: '{source}'. Available sources: {available}"
            )
        return scraper_class()
    
    @classmethod
    def get_available_sources(cls) -> list[str]:
        """
        Get a list of all available news sources
        
        Returns:
            List of source names
        """
        return list(cls._scrapers.keys())
    
    @classmethod
    def register_scraper(cls, name: str, scraper_class: type[BaseScraper]) -> None:
        """
        Register a new scraper dynamically
        
        Args:
            name: The name to register the scraper under
            scraper_class: The scraper class (must inherit from BaseScraper)
        """
        if not issubclass(scraper_class, BaseScraper):
            raise TypeError(f"{scraper_class} must inherit from BaseScraper")
        cls._scrapers[name.lower()] = scraper_class
