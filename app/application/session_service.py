from typing import List
from sqlmodel import Session, create_engine, select, desc
from app.infrastructure.database.models import SessionMessage
from pydantic_ai.messages import (
    ModelMessage, 
    ModelRequest, 
    ModelResponse, 
    UserPromptPart, 
    TextPart
)

# Reutilizamos el engine de SQLite
DATABASE_URL = "sqlite:///chatbot.db"
engine = create_engine(DATABASE_URL)

class SessionHistoryService:
    """
    Servicio para persistir y recuperar el historial de conversación desde SQLite.
    Esto permite que la 'Memoria de Sesión' sobreviva a reinicios del servidor.
    """

    def save_message(self, session_id: str, role: str, content: str):
        """Guarda un mensaje individual en la base de datos."""
        try:
            with Session(engine) as session:
                msg = SessionMessage(
                    session_id=session_id,
                    role=role,
                    content=content
                )
                session.add(msg)
                session.commit()
        except Exception as e:
            print(f"[SESSION DB ERROR] Error al guardar mensaje: {e}")

    def get_session_history(self, session_id: str, limit: int = 10) -> List[ModelMessage]:
        """
        Recupera los últimos mensajes de una sesión y los convierte al formato
        requerido por Pydantic AI (List[ModelMessage]).
        """
        try:
            with Session(engine) as session:
                statement = select(SessionMessage).where(
                    SessionMessage.session_id == session_id
                ).order_by(desc(SessionMessage.timestamp)).limit(limit)
                
                results = session.exec(statement).all()
                # Volteamos para tener orden cronológico
                results.reverse()
                
                messages = []
                for msg in results:
                    if msg.role == 'user':
                        messages.append(ModelRequest(
                            parts=[UserPromptPart(content=msg.content)]
                        ))
                    elif msg.role == 'model':
                        messages.append(ModelResponse(
                            parts=[TextPart(content=msg.content)]
                        ))
                return messages
        except Exception as e:
            print(f"[SESSION DB ERROR] Error al recuperar historial: {e}")
            return []

    def clear_session(self, session_id: str):
        """Borra el historial de una sesión."""
        try:
            with Session(engine) as session:
                statement = select(SessionMessage).where(SessionMessage.session_id == session_id)
                results = session.exec(statement).all()
                for msg in results:
                    session.delete(msg)
                session.commit()
        except Exception as e:
            print(f"[SESSION DB ERROR] Error al limpiar sesión: {e}")

# Singleton
session_history_service = SessionHistoryService()
