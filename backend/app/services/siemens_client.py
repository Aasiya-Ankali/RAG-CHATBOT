import json
import os
import requests
from app.config import (
    CHAT_MODEL,
    EMBED_MODEL,
    RERANK_MODEL,
    SIEMENS_API_KEY,
    SIEMENS_BASE_URL,
)
from app.logger import get_logger

logger = get_logger(__name__)


class SiemensClient:

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {SIEMENS_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        logger.info("SiemensClient initialized.")

    def getModels(self):
        """Retrieves a list of available models from the Siemens LLM API."""
        r = requests.get(
            f"{SIEMENS_BASE_URL}/v1/models", headers=self.headers, timeout=60
        )
        r.raise_for_status()
        return r.json()

    def embeddings(self, text):
        """Generates embeddings for a single text input."""
        payload = {"model": EMBED_MODEL, "input": text}
        endpoint = "v1/embeddings"

        r = requests.post(
            f"{SIEMENS_BASE_URL}/{endpoint}",
            headers=self.headers,
            timeout=60,
            json=payload,
        )

        r.raise_for_status()
        data = r.json()
        return data["data"][0]["embedding"]

    def batch_embeddings(self, texts):
        """Generates embeddings for multiple text inputs."""
        payload = {"model": EMBED_MODEL, "input": texts}
        endpoint = "v1/embeddings"

        r = requests.post(
            f"{SIEMENS_BASE_URL}/{endpoint}",
            headers=self.headers,
            timeout=120,
            json=payload,
        )

        r.raise_for_status()
        data = r.json()
        return [
            item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])
        ]

    def chat_completion(self, messages, model=None):
        """
        Call Siemens chat completion API.

        Args:
            messages: List of message dicts [{"role": "user", "content": "..."}]
            model: Model name (defaults to CHAT_MODEL from config)

        Returns:
            String response from the model
        """
        payload = {
            "model": model or CHAT_MODEL,
            "messages": messages,
            "temperature": 0.2,
        }
        endpoint = "v1/chat/completions"

        r = requests.post(
            f"{SIEMENS_BASE_URL}/{endpoint}",
            headers=self.headers,
            timeout=120,
            json=payload,
        )

        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

    def rerank_documents(self, query, documents):
        """Rerank documents based on relevance to query."""
        payload = {
            "model": RERANK_MODEL,
            "query": query,
            "documents": documents,
        }
        endpoint = "v1/rerank"

        r = requests.post(
            f"{SIEMENS_BASE_URL}/{endpoint}",
            headers=self.headers,
            timeout=60,
            json=payload,
        )

        r.raise_for_status()
        data = r.json()
        return data["results"]

    def chat(self, messages, model=None):

        payload = {
            "model": model or CHAT_MODEL,
            "messages": messages,
            "temperature": 0.2,
        }
        endpoint = "v1/chat/completions"

        r = requests.post(
            f"{SIEMENS_BASE_URL}/{endpoint}",
            headers=self.headers,
            timeout=120,
            json=payload,
        )

        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

    def rag_chat_with_history(
        self,
        user_message: str,
        collection,
        conversation_history: list = None,
        n_context_chunks: int = 3,
    ):
        """
        RAG Chat with conversation context.

        How it works:
        1. User asks: "What are power plants in India?"
        → Search ChromaDB → Answer

        2. User asks: "What about their capacity?"
        → LLM sees previous Q&A → Knows "their" = power plants from Q1
        → Search ChromaDB → Answer with context

        Args:
            user_message: Current question
            collection: ChromaDB collection
            conversation_history: Previous messages in THIS conversation
                Format: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
            n_context_chunks: Number of chunks to retrieve

        Returns:
            String answer
        """

        print(f"\n{'='*50}")
        print(f"Question: {user_message}")
        print(
            f"History: {len(conversation_history) if conversation_history else 0} messages"
        )
        print(f"{'='*50}")

        print("Searching ChromaDB...")
        try:
            search_results = collection.query(
                query_texts=[user_message], n_results=n_context_chunks
            )

            context_chunks = []
            if search_results and search_results.get("documents"):
                context_chunks = search_results["documents"][0]

            context_text = "\n\n".join(context_chunks)
            print(f"Found {len(context_chunks)} chunks")

        except Exception as e:
            print(f"ChromaDB Error: {e}")
            context_text = ""

        # STEP 2: Build prompt with context AND history
        system_prompt = f"""You are a helpful assistant for power plant data analysis.

    Answer based on the following context from the knowledge base:

    CONTEXT:
    {context_text}

    INSTRUCTIONS:
    - Be conversational and natural
    - Use the context to answer questions
    - If referring to previous conversation, be clear
    - If context doesn't have the answer, say "I don't have that information"
    - Keep answers concise
    - Give every answer in professional format 
    """

        # Build message list
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history (if exists)
        if conversation_history:
            messages.extend(conversation_history)

        # Add current question
        messages.append({"role": "user", "content": user_message})

        # STEP 3: Call LLM
        print("Calling LLM...")
        try:
            answer = self.chat_completion(messages)
            print(f"Got answer: {answer[:100]}...")
            return answer

        except Exception as e:
            print(f"LLM Error: {e}")
            logger.error(f"LLM Error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
