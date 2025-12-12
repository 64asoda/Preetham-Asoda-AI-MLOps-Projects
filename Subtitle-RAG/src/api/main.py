"""
FastAPI application for SubtitleRAG.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.config import get_settings
from src.retrieval.search import get_chroma_db
from src.embedding.embedder import get_embeddings_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler. Preloads models on startup."""
    logger.info("Starting SubtitleRAG....")

    logger.info("Loading embedding model....")
    get_embeddings_model()

    logger.info("Connecting to ChromaDB...")
    db = get_chroma_db()
    doc_count = db._collection.count() 
    logger.info(f"ChromaDB ready with {doc_count} documents")

    logger.info("Subtitle RAG ready")

    yield

    logger.info("Shutting down SubtitleRAG....")


def create_app() -> FastAPI:
     """Application factory."""
     settings = get_settings()

     app = FastAPI(
          title="SubtitleRAG",
          description="""
        A production-grade RAG system for semantic subtitle search.
        
        ## Features
        - Semantic search across 89K+ subtitles
        - Fast similarity matching using ChromaDB
        - RESTful API with OpenAPI documentation
        
        ## Endpoints
        - `POST /query` - Search with full options
        - `GET /search` - Simple search
        - `GET /health` - Health check
        - `GET /stats` - Collection statistics
        """,
        version = "1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
     )

     app.add_middleware(
          CORSMiddleware,
          allow_origins=["*"],
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
     )

     app.include_router(router, prefix="/api/v1")

     @app.get("/", tags=["Root"])
     async def root():
          return {
               "message": "SubtitleRAG API",
               "description": "Semantic search across 89k+ subtitles",
               "docs": "/docs",
               "health": "/api/v1/health"
          }
     return app

app = create_app()

if __name__ == "__main__":
     import uvicorn

     settings = get_settings()
     uvicorn.run(
          "src.api.main:app",
          host=settings.API_HOST,
          port=settings.API_PORT,
          reload=False
     )



