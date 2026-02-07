from fastapi import APIRouter, Depends
from app.domain.models import ChatRequest, ChatResponse, FeedbackRequest, FeedbackResponse
from app.application.chat_service import ChatService
from app.application.feedback_service import feedback_service
from app.infrastructure.external.flask_gateway import FlaskBackendGateway
from app.infrastructure.agent.pydantic_agent import PydanticChatAgent

router = APIRouter()

# Dependency Injection setup
def get_chat_service() -> ChatService:
    gateway = FlaskBackendGateway()
    agent = PydanticChatAgent(gateway)
    return ChatService(agent)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, service: ChatService = Depends(get_chat_service)):
    """
    Chat endpoint - processes messages and returns agent response.
    """
    return await service.process_message(request)

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Feedback endpoint - receives user corrections and saves them to the knowledge base.
    This allows the chatbot to learn from user feedback and improve future responses.
    """
    return feedback_service.save_feedback(request)

@router.get("/feedback/history")
async def get_feedback_history():
    """
    Get feedback history - returns all stored corrections.
    """
    content = feedback_service.get_feedback_context()
    return {
        "status": "success",
        "content": content
    }

@router.get("/health")
async def health(service: ChatService = Depends(get_chat_service)):
    """
    Health check endpoint.
    """
    is_backend_up = await service.chat_agent.backend_gateway.check_health()
    return {
        "status": "healthy",
        "service": "chatbot-support-api",
        "backend_connected": is_backend_up
    }

