from app.infrastructure.database.vector_store import vector_store
from app.infrastructure.database.models import Feedback
from sqlmodel import Session, create_engine, select
import os

# Configuración de BD
DATABASE_URL = "sqlite:///chatbot.db"
engine = create_engine(DATABASE_URL)

def cleanup_sergio():
    print("--- 🗑️ Iniciando limpieza de Sergio Mendez ---")
    
    # 1. Limpiar SQL
    with Session(engine) as session:
        statement = select(Feedback).where(Feedback.user_correction.contains("Sergio Mendez"))
        results = session.exec(statement).all()
        
        for record in results:
            print(f"[SQL] Borrando registro ID: {record.id}, FeedbackID: {record.feedback_id}")
            session.delete(record)
            
            # 2. Limpiar Vector DB
            try:
                vector_store.collection.delete(ids=[record.feedback_id])
                print(f"[VECTOR] Borrado ID {record.feedback_id} de ChromaDB.")
            except Exception as e:
                print(f"[VECTOR ERROR] No se pudo borrar de ChromaDB: {e}")
                
        session.commit()

    # 3. Limpiar MD (por si acaso hubiera algo)
    md_path = "knowledge/user_feedback/corrections.md"
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(md_path, 'w', encoding='utf-8') as f:
            skip = False
            for line in lines:
                if "Sergio Mendez" in line:
                    skip = True # Empezar a saltar este bloque
                if skip and "---" in line:
                    skip = False
                    continue
                if not skip:
                    f.write(line)
        print("[MD] Limpieza de archivo Markdown completada.")

if __name__ == "__main__":
    cleanup_sergio()
