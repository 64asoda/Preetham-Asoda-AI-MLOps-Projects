"""
Search and retrieval utilities using ChromaDB.
"""

import logging
from typing import Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langsmith import traceable

from src.config import get_settings
from src.embedding.embedder import get_embeddings_model

logger = logging.getLogger(__name__)

_chroma_db: Optional[Chroma] = None

def get_chroma_db() -> Chroma:
    """Get or create the ChromaDB instance (singleton)."""
    global _chroma_db

    if _chroma_db is None:
        settings = get_settings()
        logger.info(f"Loading ChromaDB from : {settings.CHROMA_PERSIST_DIR}")

        _chroma_db = Chroma(
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=get_embeddings_model(),
            persist_directory=settings.CHROMA_PERSIST_DIR
        )

        doc_count = _chroma_db._collection.count()
        logger.info(f"ChromaDB loaded with {doc_count} documents")
    
    return _chroma_db

@traceable(run_type="retriever", name="subtitle_search")
def search_similar(query: str, top_k: Optional[int] = None, score_threshold: Optional[float] = None) -> list[dict]:
        """
    Search for similar documents using text query.
    
    Args:
        query: Search query text
        top_k: Number of results to return
        score_threshold: Optional minimum similarity score
        
    Returns:
        List of result dicts with content, metadata, and score
    """
        settings = get_settings()
        top_k = top_k or settings.DEFAULT_TOP_K

        db = get_chroma_db()
        results = db.similarity_search_with_score(query, k=top_k)

        formatted_results = []
        for doc, score in results:
             similarity = 1 - score if score<=1 else 1 / (1 + score)

             if score_threshold and similarity < score_threshold:
                  continue
             
             formatted_results.append({
                  "content": doc.page_content,
                  "metadata":doc.metadata,
                  "similarity_score": round(similarity, 4)
             })
        
        logger.info(f"Query: '{query[:50]}...' returned {len(formatted_results)} results")
        return formatted_results


@traceable(run_type="retriever", name="vector_search")
def search_by_vector(embedding: list[float], top_k: Optional[int] = None) -> list[dict]:
     """Search for similar documents using embedding vector."""
     settings = get_settings()
     top_k = top_k or settings.DEFAULT_TOP_K

     db = get_chroma_db()
     results = db.similarity_search_by_vector(embedding=embedding, k=top_k)

     return [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]


def get_collection_stats() -> dict:
     """Get statistics about the ChromaDB collection."""
     db = get_chroma_db()

     return {
          "total_documents": db._collection.count(),
          "collection_name": get_settings().CHROMA_COLLECTION_NAME,
          "persist_directory": get_settings().CHROMA_PERSIST_DIR
     }


def add_documents(documents: list[Document], batch_size: Optional[int] = None) -> int:
     """Add documents to ChromaDB in batches."""
     settings = get_settings()
     batch_size = batch_size or settings.BATCH_SIZE

     db = get_chroma_db()
     total_added = 0

     for i in range(0, len(documents), batch_size):
          batch = documents[i:i + batch_size]
          db.add_documents(batch)
          total_added += len(batch)
          logger.info(f"Added batch {i // batch_size + 1}: {total_added}/{len(documents)}")

     return total_added
    

