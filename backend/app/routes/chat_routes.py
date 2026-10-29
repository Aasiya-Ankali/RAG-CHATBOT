# backend/app/routes/chat_routes.py
from fastapi import APIRouter, HTTPException
from app.schemas.models import ChatRequest, ChatResponse
from app.services.chat_pipeline_langchain import AnswerChatQuery
from app.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    """
    Chat endpoint - uses only last answer for context
    """
    try:
        logger.info(f"Chat request - Question: '{body.question}'")
        
        # Log last answer if provided
        if body.last_answer:
            preview = body.last_answer[:100]
            logger.info(f"Last answer: '{preview}{'...' if len(body.last_answer) > 100 else ''}'")
        else:
            logger.info("No previous answer (first question)")
        
        # Call service with BOTH question and last_answer
        answer = AnswerChatQuery(
            question=body.question,       
            last_answer=body.last_answer   
        )
        
        if not isinstance(answer, str):
            logger.error(f"Expected string, got {type(answer)}: {answer}")
            answer = str(answer)
        
        logger.info(f"Response generated: {len(answer)} chars")
        
        return ChatResponse(answer=answer)
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))