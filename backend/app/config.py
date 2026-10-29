import os
from dotenv import load_dotenv

load_dotenv()

# Groq API - get free key at https://console.groq.com
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_CHAT_MODEL = os.getenv("GROQ_CHAT_MODEL", "qwen/qwen3.8-27b")

# Embedding model (sentence-transformers, runs locally, auto-downloaded from HuggingFace)
LOCAL_EMBED_MODEL = os.getenv("LOCAL_EMBED_MODEL", "all-MiniLM-L6-v2")

# Reranker model (sentence-transformers CrossEncoder, runs locally, auto-downloaded)
LOCAL_RERANK_MODEL = os.getenv("LOCAL_RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

# ChromaDB
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_data")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "New_Powerplant")
