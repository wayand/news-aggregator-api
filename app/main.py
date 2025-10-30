from fastapi import FastAPI, HTTPException
from app.scrapers.factory import ScraperFactory
from app.models.schemas import PagesResponse, FeedsResponse, SourcesResponse, ErrorResponse

app = FastAPI(
    title="Multi-Source News Scraper API",
    description="API for scraping news from multiple sources",
    version="2.0.0"
)


@app.get('/sources', response_model=SourcesResponse)
def get_sources():
    """Get list of all available news sources"""
    sources = ScraperFactory.get_available_sources()
    return {"sources": sources, "total": len(sources)}


@app.get('/pages/{source}', response_model=PagesResponse, responses={404: {"model": ErrorResponse}})
def get_pages(source: str, page: str = 'world'):
    """
    Get available pages/categories from a specific news source

    Args:
        source: News source (e.g., 'reuters', 'bbc')
        page: Page identifier (default: 'world')
    """
    try:
        scraper = ScraperFactory.get_scraper(source)
        data = scraper.scrape_pages(page)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping {source}: {str(e)}")


@app.get('/news/{source}', response_model=FeedsResponse, responses={404: {"model": ErrorResponse}})
def get_news(source: str, page: str = 'world', category: str = ''):
    """
    Get news feeds from a specific source, page, and category

    Args:
        source: News source (e.g., 'reuters', 'bbc')
        page: Page identifier (default: 'world')
        category: Category identifier (default: 'africa')
    """
    try:
        scraper = ScraperFactory.get_scraper(source)
        data = scraper.scrape_feeds(page, category)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping {source}: {str(e)}")


@app.get('/')
def root():
    """API root with basic information"""
    return {
        "message": "Multi-Source News Scraper API",
        "version": "2.0.0",
        "endpoints": {
            "/sources": "Get available news sources",
            "/pages/{source}": "Get pages/categories for a source",
            "/news/{source}": "Get news feeds from a source",
            "/docs": "API documentation"
        }
    }
