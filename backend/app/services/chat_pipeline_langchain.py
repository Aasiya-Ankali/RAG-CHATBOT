# backend/app/services/chat_pipeline_langchain.py
"""
LangChain-based Chat Pipeline
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.services.embedding_service import createEmbedding
from app.services.reranker import Reranker
from app.services.groq_client import GroqClient
from app.services.vector_store import search
from app.services.data_query import answer_from_data
from app.logger import get_logger
from typing import List, Dict, Optional

logger = get_logger(__name__)
reranker = Reranker()
client = GroqClient()

class LangChainChatRAG:
    """LangChain-powered RAG Chat with Strict Context Control"""

    def __init__(self):
        self.system_prompt = """You are a helpful assistant for Global power plant information.

CRITICAL RULES:
1. Answer ONLY using information from the CURRENT CONTEXT below
2. If the current context doesn't contain the answer, say: "I don't have that information in the current context"
3. DO NOT use information from previous messages or conversations
4. DO NOT make up or hallucinate information
5. When listing items, ONLY list what's in the CURRENT CONTEXT
6. If asked about a specific country/location, verify the context is about that location
7. Give all the answers in professional format  
8. Don't use markdown syntax like "**"

CONVERSATION HISTORY:
Use the conversation history ONLY to understand what the user is asking about (pronouns, references).
DO NOT use facts from history - only use facts from CURRENT CONTEXT.

Example:
User: "How many plants in India?"
You: [Check CURRENT CONTEXT for India plants, answer based on that]

User: "List them"
You: [Understand "them" = India plants from history, but LIST ONLY what's in CURRENT CONTEXT]"""

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="history"),
                (
                    "human",
                    """CURRENT CONTEXT (use ONLY this for facts):
{context}

QUESTION: {question}

Remember: Answer using ONLY the CURRENT CONTEXT above. Do not use information from conversation history.""",
                ),
            ]
        )

    def _convert_history_to_langchain(self, history: List[Dict]) -> List:
        """
        Convert history to LangChain messages
        """
        messages = []
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        return messages

    def _build_search_query(self, question: str, last_answer: str = None) -> str:
        """
        Build search query by combining last answer with new question
        
        Args:
            question: Current user question
            last_answer: Previous assistant answer (if any)
            
        Returns:
            Enhanced search query
        """
        if not last_answer:
            logger.info("No previous answer - using question only")
            return question
      
        # Combine previous answer + new question
        enhanced_query = f"{last_answer} {question}"
        
        logger.info(f"Original question: {question}")
        logger.info(f"Previous answer: {last_answer}")
        logger.info(f"Enhanced query: {enhanced_query[:150]}...")
        
        return enhanced_query

    def answer(self, question: str, last_answer: str = None) -> str:
        # First try direct data query for aggregation questions (count, list, types)
        direct = answer_from_data(question)
        if direct:
            logger.info("Answered from direct data query (not RAG)")
            return direct

        # Fall through to RAG for specific/descriptive questions
        search_query = self._build_search_query(question, last_answer)
        logger.info(f"Search query: {search_query}")

        query_vector = createEmbedding(search_query)

        result = search(query_vector, limit=5)
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        if not documents:
            logger.warning("No documents found")
            return "I don't have relevant information to answer that question."

        rerank_results = reranker.rerank(
            query=search_query,
            documents=documents,
            metadatas=metadatas,
        )

        context_parts = []
        for i, (text, metadata) in enumerate(rerank_results):
            country = metadata.get("country_name", "Unknown")
            name = metadata.get("name", "Unknown")
            fuel = metadata.get("primary_fuel", "Unknown")
            capacity = metadata.get("capacity_mw", "Unknown")
            context_parts.append(
                f"[Document {i+1}]\n"
                f"Country: {country}\n"
                f"Plant: {name}\n"
                f"Fuel: {fuel}\n"
                f"Capacity: {capacity} MW\n"
                f"Info: {text}\n"
            )

        context = "\n".join(context_parts)

        logger.info(
            f"Context countries: {[m.get('country_name', 'Unknown') for _, m in rerank_results]}"
        )

        # Build history (only last Q&A if exists)
        langchain_history = []
        if last_answer:
            langchain_history = [
                HumanMessage(content="Previous question"), 
                AIMessage(content=last_answer)
            ]

        formatted_messages = self.prompt.format_messages(
            history=langchain_history, 
            context=context, 
            question=question
        )

        # Convert to API format
        api_messages = []
        for msg in formatted_messages:
            if hasattr(msg, "type"):
                if msg.type == "system":
                    api_messages.append({"role": "system", "content": msg.content})
                elif msg.type == "human":
                    api_messages.append({"role": "user", "content": msg.content})
                elif msg.type == "ai":
                    api_messages.append({"role": "assistant", "content": msg.content})

        # Call LLM
        try:
            response = client.chat_completion(api_messages)

            if not response or len(response.strip()) == 0:
                return "I couldn't generate a proper response. Please try again."

            return str(response).strip()

        except Exception as e:
            logger.error(f"LLM error: {e}", exc_info=True)
            return "Sorry, I encountered an error. Please try again."

chat_rag = LangChainChatRAG()

def AnswerChatQuery(question: str, last_answer:  Optional[str]  = None) -> str:
    """
    Answer chat query using only the last answer for context
    
    Frontend only needs to track the last answer (not full history)

    Args:
        question: User's question
        last_answer: Previous bot answer (optional)

    Returns:
        str: Answer based on current context
        
    Example:
        # First question
        answer1 = AnswerChatQuery("How many plants in India?")
        # Returns: "There are 450 power plants in India"
        
        # Second question (pass last answer)
        answer2 = AnswerChatQuery("List them", last_answer=answer1)
        # Search uses: "There are 450 power plants in India. List them"
    """
    return chat_rag.answer(question, last_answer)