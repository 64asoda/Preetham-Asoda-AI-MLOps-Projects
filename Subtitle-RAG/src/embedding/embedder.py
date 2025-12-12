"""
Embedding utilities using HuggingFace models.
"""
import logging
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings

from src.config import get_settings

logger = logging.getLogger(__name__)

_embeddings_model: Optional[HuggingFaceEmbeddings] = None

def get_embeddings_model() -> HuggingFaceEmbeddings:
    """Get or create the embeddings model (singleton)."""
    global _embeddings_model

    if _embeddings_model is None:
        settings = get_settings()
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")

        _embeddings_model = HuggingFaceEmbeddings(
            model_name = settings.EMBEDDING_MODEL,
            model_kwargs = {'device' : 'cpu'},
            encode_kwargs = {'normalize_embeddings' : True}
        )

        logger.info("Encoding model loaded successfully")

    return _embeddings_model
    

def embed_query(query: str) -> list[float]:
    """Embed a single query string."""
    model = get_embeddings_model()
    return model.embed_query(query)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed multiple documents."""
    model = get_embeddings_model()
    logger.info(f"Embedding {len(texts)} documents")
    return model.embed_documents(texts)


def get_embedding_dimension() -> int:
    """Get the dimension of the embedding vectors."""
    model = get_embeddings_model()
    test_embedding = model.embed_query("test")
    return len(test_embedding)

                

