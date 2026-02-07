from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default-session"
    current_screen: Optional[str] = "Principal"

class ChatResponse(BaseModel):
    response: str
    session_id: str

class Employee(BaseModel):
    id: str
    name: str
    role: str

class PauseRecord(BaseModel):
    id: int
    tipo: str
    sub_tipo: Optional[str] = None
    empleado_id: str
    empleado_nombre: str
    fecha: str
    hora_inicio: str
    hora_fin: Optional[str] = None
    observacion: Optional[str] = None

class FeedbackRequest(BaseModel):
    """Modelo para la retroalimentación del usuario"""
    original_question: str
    original_response: str
    corrected_response: str
    category: Optional[str] = "general"  # Categoría del feedback (personal, turnos, recesos, etc.)
    session_id: str = "default-session"

class FeedbackResponse(BaseModel):
    """Respuesta del sistema de feedback"""
    success: bool
    message: str
    feedback_id: Optional[str] = None
