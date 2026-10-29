# chroma_db related code
# like utilities conflicts or helper fucntions come here
import chromadb
from chromadb.config import Settings

chroma_client = chromadb.PersistentClient(
    path="./chroma_data", settings=Settings(anonymized_telemetry=False)
)
# collection = chroma_client.get_or_create_collection(name="Powerplant")
collection = chroma_client.get_or_create_collection(name="Powerplant_384")

def addDocuments(ids, texts, vectors, metadatas=None):
    collection.upsert(ids=ids, documents=texts, embeddings=vectors, metadatas=metadatas)


def search(query_vector, limit=5):
    # perform semantic search , cosine similarity search then return results
    result = collection.query(query_embeddings=[query_vector], n_results=limit)
    return result


__all__ = ["collection", "addDocuments", "search"]
