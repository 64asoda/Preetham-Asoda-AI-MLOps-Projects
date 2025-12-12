"""
API route definitions for SubtitleRAG.
"""

import time
import logging

from fastapi import APIRouter, HTTPException, Query

from src.api.schemas import (
    QueryRequest, QueryResponse, SearchResult,
    HealthResponse, StatsResponse, ErrorResponse
)

from src.retrieval.search import search_similar, get_collection_stats, get_chroma_db
from src.embedding import embed_query, get_embedding_dimension
from src.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    settings = get_settings()

    try:
        stats = get_collection_stats()
        chroma_connected = True
        doc_count = stats["total_documents"]
    except Exception as e:
        logger.error(f"ChromaDB health check failed: {e}")
        chroma_connected = False
        doc_count = 0

    return HealthResponse(
        status="healthy" if chroma_connected else "degraded",
        chroma_connected=chroma_connected,
        document_count=doc_count,
        embedding_model=settings.EMBEDDING_MODEL
    )

@router.get("/live", tags=["Health"])
async def liveness_check():
    """Liveness probe - checks if the service is alive."""
    return {"status": "alive"}


@router.post("/query", response_model=QueryResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}, tags=["Search"])
async def search_subtitles(request: QueryRequest):
        """
    Search for subtitles matching the query.
    
    - **query**: The search text (required)
    - **top_k**: Number of results to return (default: 5, max: 50)
    - **score_threshold**: Minimum similarity score (optional, 0-1)
    """
        start_time = time.time()

        try:
             results = search_similar(
                  query=request.query,
                  top_k=request.top_k,
                  score_threshold=request.score_threshold
             )
             search_results=[
                  SearchResult(
                       content=r["content"],
                       metadata=r["metadata"],
                       similarity_score=r.get("similarity_score")
                  )
                  for r in results
             ]
             elapsed_time = time.time() - start_time
             logger.info(f"Search completed in {elapsed_time:.3f}s ")

             return QueryResponse(
                  query=request.query,
                  results=search_results,
                  total_results=len(search_results)
             )
        
        except Exception as e:
             logger.error(f"Search failed: {e}")
             raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=QueryResponse, tags=["Search"])
async def search_subtitles_get(
     q: str = Query(..., min_length=1, max_length=1000, description="Search query"),
     top_k: int = Query(default=5, ge=1, le=50, description="Number of results")
):
      """Search for subtitles (GET method). Example: /search?q=I'll be back&top_k=10"""
      request = QueryRequest(query=q, top_k=top_k)
      return await search_subtitles(request)

@router.get("/stats", response_model=StatsResponse, tags=["Info"])
async def get_stats():
     """Get collection statistics."""
     try:
          stats = get_collection_stats()
          return StatsResponse(**stats)
     except Exception as e:
          logger.error(f"Stats retrieval failed: {e}")
          raise HTTPException(status_code=500, detail=str(e))
