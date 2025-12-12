"""
Pydantic schemas for SubtitleRAG API request/response validation.
"""
from typing import Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """Request schema for search queries."""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query text")
    top_k: Optional[int] = Field(default=5, ge=1, le=50, description="Number of results to return")
    score_threshold: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Minimum similarity score")

    class Config:
        json_schema_extra = {"example": {"query": "I'll be back", "top_k":5, "score_threshold": 0.5}}


class SearchResult(BaseModel):
    """Single search result."""
    content: str = Field(..., description="Matched content snippet")
    metadata: dict = Field(default_factory=dict, description="Document metadata")
    similarity_score: Optional[float] = Field(default=None, description="Similarity score (0-1)")


class QueryResponse(BaseModel):
    """Response schema for search queries."""
    query: str = Field(..., description="Original query")
    results: list[SearchResult] = Field(default_factory=list, description="List of search results")
    total_results: int = Field(..., description="Number of results returned")


class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str = Field(..., description="Hralth status")
    chroma_connected: bool = Field(..., description="Chroma connection status")
    document_count: int = Field(..., description="Number of documents in index")
    embedding_model: str = Field(..., description="Embedding model name")


class StatsResponse(BaseModel):
    """Response schema for collection statistics."""
    total_documents: int
    collection_name: str
    persist_directory: str


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Error details")

