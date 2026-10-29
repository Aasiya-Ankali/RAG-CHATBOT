# Take the preprocessed chunks , create embeddings for them and store in the chroma DB
# Parallel processing

from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from app.logger import get_logger
from app.services.embedding_service import createBatchEmbeddings
from app.services.vector_store import addDocuments
from app.config import LOCAL_EMBED_MODEL

import time


logger = get_logger(__name__)

chunk_file = "./data/chunks.csv"
batch_size = 5  # 50 chunks per API call
max_worker = 3  # in parallel 3 threads
MAX_RETRIES = 3  # Define max retries for embedding
RETRY_DELAY_SECONDS = 5


def load_chunks(df):
    return [
        {
            "id": str(row.chunk_id),
            "description": str(row.chunk_text),
            "country": str(row.country) if hasattr(row, "country") else "",
            "country_long": str(row.country_long) if hasattr(row, "country_long") else "",
            "name": str(row.name) if hasattr(row, "name") else "",
            "primary_fuel": str(row.primary_fuel) if hasattr(row, "primary_fuel") else "",
            "capacity_mw": str(row.capacity_mw) if hasattr(row, "capacity_mw") else "",
        }
        for row in df.itertuples()
    ]


def embed_batch(texts):
    """Generate embeddings for multiple texts at once."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            vectors = createBatchEmbeddings(texts)
            return list(range(len(texts))), vectors

        except Exception as e:
            retries += 1
            logger.warning(f"Embedding failed (Attempt {retries}/{MAX_RETRIES}): {e}")
            if retries < MAX_RETRIES:
                logger.info(
                    f"Retrying embedding after {RETRY_DELAY_SECONDS} seconds..."
                )
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.error(
                    f"Embedding failed after {MAX_RETRIES} attempts. Skipping this batch. Error: {e}"
                )
                return [], []


def process_batch(batch_idx, batch):
    """Process a batch of chunks: create embeddings and store in vector DB."""
    texts = [x["description"] for x in batch]
    successful_indices, vectors = embed_batch(texts)

    if not vectors:
        logger.warning(f"Batch {batch_idx}: all embeddings failed, skipping")
        return 0, len(batch)

    successful_batch = [batch[j] for j in successful_indices]

    addDocuments(
        ids=[x["id"] for x in successful_batch],
        texts=[x["description"] for x in successful_batch],
        vectors=vectors,
        metadatas=[
            {
                "chunk_id": str(x["id"]),
                "country": x.get("country", ""),
                "country_name": x.get("country_long", ""),
                "name": x.get("name", ""),
                "primary_fuel": x.get("primary_fuel", ""),
                "capacity_mw": x.get("capacity_mw", ""),
            }
            for x in successful_batch
        ],
    )

    return len(successful_batch), len(batch)


def run(limit=None):
    """Main function to load chunks, create embeddings, and store in ChromaDB."""
    logger.info(f"Model used for embedding: {LOCAL_EMBED_MODEL}")
    logger.info(f"Loading chunks from {chunk_file}")

    df = pd.read_csv(chunk_file)

    if limit:
        df = df.head(limit)
        logger.info(f"Using first {limit} chunks")

    chunks = load_chunks(df)
    logger.info(f"Loaded {len(chunks)} chunks for embedding")

    if not chunks:
        logger.warning("No chunks loaded for ingestion. Exiting.")
        return

    # Create batches
    batches = [
        (batch_idx // batch_size, chunks[batch_idx : batch_idx + batch_size])
        for batch_idx in range(0, len(chunks), batch_size)
    ]

    total_stored = 0
    total_chunks_processed = 0

    # Parallel execution
    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        futures = {
            executor.submit(process_batch, batch_idx, batch_data): batch_idx
            for batch_idx, batch_data in batches
        }

        for future in as_completed(futures):
            batch_idx = futures[future]
            stored, total_in_batch = future.result()
            total_stored += stored
            total_chunks_processed += total_in_batch

            logger.info(
                f"Stored {stored} chunks from batch {batch_idx} "
                f"(running total: {total_stored} / {total_chunks_processed} chunks processed)"
            )

    logger.info(
        f"Finished processing all batches. Total chunks successfully stored: "
        f"{total_stored} out of {len(chunks)}"
    )


if __name__ == "__main__":
    run()
