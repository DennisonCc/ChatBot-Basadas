from fastapi import APIRouter, Depends
from app.domain.models import ChatRequest, ChatResponse
from app.application.chat_service import ChatService
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
