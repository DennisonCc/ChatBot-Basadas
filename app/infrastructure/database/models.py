from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Feedback(SQLModel, table=True):
    """
    Modelo de persistencia para el Feedback de usuarios.
    En producción (PostgreSQL), esta tabla alimentará el Dashboard de Admin y el RAG.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    feedback_id: str = Field(index=True, unique=True)  # UUID generado
    
    # Datos de la consulta
    user_question: str
    original_response: str
    user_correction: str
    category: str
    
    # Metadatos RAG
    vector_id: Optional[str] = None  # ID del vector en Pinecone/Chroma
    embedding_status: str = Field(default="PENDING")  # PENDING, EMBEDDED, FAILED
    
    # Auditoría
    status: str = Field(default="APPROVED")  # PENDING_REVIEW, APPROVED, REJECTED
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
