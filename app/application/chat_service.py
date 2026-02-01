from app.domain.interfaces import IChatAgent
from app.domain.models import ChatRequest, ChatResponse

class ChatService:
    def __init__(self, chat_agent: IChatAgent):
        self.chat_agent = chat_agent

    async def process_message(self, request: ChatRequest) -> ChatResponse:
        try:
            response_text = await self.chat_agent.get_response(
                request.message, 
                current_screen=request.current_screen
            )
            return ChatResponse(
                response=response_text,
                session_id=request.session_id
            )
        except Exception as e:
            # Here we could map exceptions to domain-specific error messages
            return ChatResponse(
                response=f"Lo siento, ocurrió un error procesando tu mensaje: {str(e)}",
                session_id=request.session_id
            )
