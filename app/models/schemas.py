from pydantic import BaseModel, Field
from typing import Optional


class PageItem(BaseModel):
    """Model for a page/category item"""
    id: str = Field(description="Unique identifier (content-based hash)")
    name: Optional[str] = None
    description: Optional[str] = None
    query: Optional[str] = None


class PagesResponse(BaseModel):
    """Response model for pages endpoint"""
    total: int
    page: str
    items: list[PageItem]


class FeedItem(BaseModel):
    """Model for a news feed item"""
    id: str = Field(description="Unique identifier (content-based hash of link)")
    category: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None
    image: Optional[str] = None
    datetime: Optional[str] = None


class FeedsResponse(BaseModel):
    """Response model for feeds endpoint"""
    total: int
    source: str
    page: str
    category: str
    items: list[FeedItem]


class SourcesResponse(BaseModel):
    """Response model for available sources"""
    sources: list[str]
    total: int = Field(description="Total number of available sources")


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
