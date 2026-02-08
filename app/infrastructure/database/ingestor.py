import os
from pathlib import Path
from app.infrastructure.database.vector_store import vector_store

class KnowledgeIngestor:
    """
    Utility to migrate Markdown knowledge base into ChromaDB.
    This enables real RAG without overloading the system prompt.
    """
    def __init__(self, knowledge_dir: str = None):
        if knowledge_dir is None:
            base_path = Path(__file__).parent.parent.parent.parent
            self.knowledge_dir = base_path / "knowledge" / "modules"
        else:
            self.knowledge_dir = Path(knowledge_dir)

    def run_migration(self):
        print(f"--- 🚀 Starting Ingestion from {self.knowledge_dir} ---")
        
        # Iterar sobre todos los archivos .md en modules
        for md_file in self.knowledge_dir.glob("*.md"):
            print(f"Indexing: {md_file.name}...")
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Divide el contenido en chunks por secciones (H2 o H3)
            # Para una implementación simple, dividiremos por párrafos o bloques marcados
            chunks = self._chunk_text(content)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"doc_{md_file.stem}_{i}"
                vector_store.add_feedback(
                    feedback_id=chunk_id,
                    text=chunk,
                    metadata={"source": md_file.name, "type": "base_knowledge"}
                )
        
        print("--- ✅ Ingestion Complete ---")

    def _chunk_text(self, text: str, max_chunk_size: int = 1500) -> list:
        """
        Divide el texto en fragmentos manejables. 
        En producción se usarían librerías como LangChain RecursiveCharacterTextSplitter.
        """
        # Una división simple por encabezados o bloques de texto
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""
        
        for p in paragraphs:
            if len(current_chunk) + len(p) < max_chunk_size:
                current_chunk += p + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = p + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

if __name__ == "__main__":
    ingestor = KnowledgeIngestor()
    ingestor.run_migration()
