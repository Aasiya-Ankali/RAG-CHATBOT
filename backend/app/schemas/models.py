# # BaseModel is the base class

# # Pydantic model will come here
# # data validation , check for datatype of data
# # ex question: str , if give num convert in string , or for empty convert in empty string

from pydantic import BaseModel ,Field
from typing import List ,Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    id: str
    distance: float
    description: str

class QueryResponseWithAnswer(BaseModel):
    answer: str
    sources: List[dict]  

class ChatMessage(BaseModel):
    """Single message in conversation"""
    role: str  
    content: str

class ChatRequest(BaseModel):
    """Chat request with history"""
    question: str = Field(
        ...,
        description="User's current question",
        min_length=1
    )
    last_answer: Optional[str] = Field(
        None,  #Default value
        description="Previous bot answer (optional, for context)"
    )

class ChatResponse(BaseModel):
    """Simple chat response - NO SOURCES"""
    answer: str = Field(
        ...,
        description="Bot's answer based on retrieved context"
    )