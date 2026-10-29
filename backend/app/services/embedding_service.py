"""
Embedding service using sentence-transformers (open source, runs locally).
Model is downloaded automatically from HuggingFace on first use.
"""
from app.config import LOCAL_EMBED_MODEL
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

_model = None


def _get_model():
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {LOCAL_EMBED_MODEL}")
        _model = SentenceTransformer(LOCAL_EMBED_MODEL)
        logger.info("Embedding model loaded.")
    return _model


def createEmbedding(text: str) -> list:
    return _get_model().encode(text).tolist()


def createBatchEmbeddings(texts: list) -> list:
    return _get_model().encode(texts).tolist()
