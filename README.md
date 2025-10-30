# Multi-Source News Scraper API

A scalable FastAPI application for scraping news from multiple sources using a factory pattern architecture.

## Features

- **Multi-source support**: Scrape news from Reuters, BBC, and easily add more sources
- **Factory pattern**: Clean, maintainable architecture for managing multiple scrapers
- **Type safety**: Pydantic models for request/response validation
- **RESTful API**: Well-documented endpoints with automatic OpenAPI documentation
- **Extensible**: Easy to add new news sources without modifying existing code

## Current Supported Sources

- **Reuters** (`reuters`)
- **BBC News** (`bbc`)

## Architecture

```
news-scraper/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application & routes
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py            # Abstract base scraper class
│   │   ├── factory.py         # Scraper factory
│   │   ├── reuters.py         # Reuters scraper
│   │   └── bbc.py             # BBC scraper
│   └── models/
│       ├── __init__.py
│       └── schemas.py         # Pydantic response models
├── requirements.txt
├── main.py                    # Application entry point
└── README.md
```

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Get Available Sources
```bash
GET /sources
```
Returns a list of all available news sources.

**Example:**
```bash
curl http://localhost:8000/sources
```

### Get Pages/Categories
```bash
GET /pages/{source}?page=world
```
Get available pages/categories from a specific news source.

**Parameters:**
- `source` (path): News source name (e.g., `reuters`, `bbc`)
- `page` (query, optional): Page identifier (default: `world`)

**Example:**
```bash
curl http://localhost:8000/pages/reuters?page=world
```

### Get News Feeds
```bash
GET /news/{source}?page=world&category=africa
```
Get news articles from a specific source, page, and category.

**Parameters:**
- `source` (path): News source name (e.g., `reuters`, `bbc`)
- `page` (query, optional): Page identifier (default: `world`)
- `category` (query, optional): Category identifier (default: `africa`)

**Example:**
```bash
curl http://localhost:8000/news/reuters?page=world&category=africa
```

### API Documentation
```bash
GET /docs
```
Interactive API documentation (Swagger UI)

```bash
GET /redoc
```
Alternative API documentation (ReDoc)

## Adding a New News Source

To add a new news source, follow these steps:

### 1. Create a New Scraper Class

Create a new file in `app/scrapers/` (e.g., `cnn.py`):

```python
from app.scrapers.base import BaseScraper

class CNNScraper(BaseScraper):
    """Scraper for CNN News"""
    
    def __init__(self):
        super().__init__(base_url='https://www.cnn.com')
    
    def scrape_pages(self, page: str) -> dict:
        html = self._fetch_html(f'{self.base_url}/{page}')
        # Implement CNN-specific scraping logic
        # Return: {'total': int, 'page': str, 'items': list}
        pass
    
    def scrape_feeds(self, page: str, category: str) -> dict:
        html = self._fetch_html(f'{self.base_url}/{page}/{category}')
        # Implement CNN-specific feed scraping
        # Return: {'total': int, 'source': str, 'page': str, 'category': str, 'items': list}
        pass
```

### 2. Register the Scraper

Add your scraper to the factory in `app/scrapers/factory.py`:

```python
from app.scrapers.cnn import CNNScraper

class ScraperFactory:
    _scrapers = {
        'reuters': ReutersScraper,
        'bbc': BBCScraper,
        'cnn': CNNScraper,  # Add your scraper here
    }
```

### 3. Update the __init__.py

Add imports to `app/scrapers/__init__.py`:

```python
from app.scrapers.cnn import CNNScraper

__all__ = [
    'BaseScraper',
    'ScraperFactory',
    'ReutersScraper',
    'BBCScraper',
    'CNNScraper',  # Add here
]
```

That's it! Your new source is now available through the API.

## Development

### Base Scraper Class

All scrapers inherit from `BaseScraper` which provides:
- `_fetch_html(url)`: Fetches and parses HTML
- `_get_default_headers()`: Returns HTTP headers
- Common initialization and utilities

### Abstract Methods to Implement

When creating a new scraper, you must implement:
1. `scrape_pages(page: str) -> dict`: Scrape available categories
2. `scrape_feeds(page: str, category: str) -> dict`: Scrape news articles

## Response Models

### PagesResponse
```json
{
  "total": 10,
  "page": "world",
  "items": [
    {
      "id": 1,
      "name": "africa",
      "description": "Africa News",
      "query": "?page=world&category=africa"
    }
  ]
}
```

### FeedsResponse
```json
{
  "total": 20,
  "source": "https://www.reuters.com",
  "page": "world",
  "category": "africa",
  "items": [
    {
      "id": 1,
      "category": "africa",
      "title": "News headline",
      "link": "/world/africa/article-123",
      "image": "https://...",
      "datetime": "2025-10-30T12:00:00Z"
    }
  ]
}
```

## Error Handling

The API returns standard HTTP error responses:
- `404`: Source not found or invalid parameters
- `500`: Internal server error during scraping

## Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP requests
- **Pydantic**: Data validation

## Notes

- The BBC scraper is provided as an example and may need selector adjustments based on BBC's current HTML structure
- Always respect robots.txt and terms of service when scraping websites
- Consider adding rate limiting for production use
- Add appropriate error handling and logging for production deployments

## License

This project is for educational purposes.