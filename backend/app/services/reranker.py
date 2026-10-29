"""
Reranker using sentence-transformers CrossEncoder (open source, runs locally).
Model is downloaded automatically from HuggingFace on first use.
"""
from app.config import LOCAL_RERANK_MODEL
from sentence_transformers import CrossEncoder
from app.logger import get_logger

logger = get_logger(__name__)

_reranker = None


def _get_reranker():
    global _reranker
    if _reranker is None:
        logger.info(f"Loading reranker model: {LOCAL_RERANK_MODEL}")
        _reranker = CrossEncoder(LOCAL_RERANK_MODEL)
        logger.info("Reranker model loaded.")
    return _reranker


class Reranker:

    def rerank(self, query: str, documents: list, metadatas: list = None, top_k: int = 5):
        if not documents:
            return []

        reranker = _get_reranker()
        pairs = [(query, doc) for doc in documents]
        scores = reranker.predict(pairs)

        ranked = sorted(zip(scores, range(len(documents))), reverse=True)
        return [
            (documents[i], metadatas[i] if metadatas else {})
            for _, i in ranked[:top_k]
        ]
