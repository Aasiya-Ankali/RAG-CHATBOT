"""
Groq cloud API client for chat completions.
Uses open source models (Llama3, Mixtral) hosted on Groq's free cloud.
Get your free API key at: https://console.groq.com
"""
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_CHAT_MODEL
from app.logger import get_logger

logger = get_logger(__name__)


class GroqClient:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_CHAT_MODEL
        logger.info(f"GroqClient initialized with model: {self.model}")

    def chat_completion(self, messages: list) -> str:
        """
        Call Groq chat API.
        Args:
            messages: [{"role": "system/user/assistant", "content": "..."}]
        Returns:
            str: model response
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )
        return response.choices[0].message.content
