import chromadb
from app.infrastructure.common.config import config
from pathlib import Path
from openai import OpenAI
from chromadb.api.types import Documents, Embeddings, EmbeddingFunction

class NvidiaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_key: str, model_name: str):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        self.model_name = model_name

    def __call__(self, input: Documents) -> Embeddings:
        # Para ChromaDB, recibimos una lista de textos
        responses = self.client.embeddings.create(
            input=input,
            model=self.model_name,
            extra_body={"input_type": "query"} # Requerido por modelos de Nvidia
        )
        return [res.embedding for res in responses.data]

class VectorStore:
    def __init__(self, persist_directory: str = None):
        if persist_directory is None:
            base_path = Path(__file__).parent.parent.parent.parent
            self.persist_directory = str(base_path / "vector_db")
        else:
            self.persist_directory = persist_directory
            
        # Inicializar cliente de ChromaDB persistente
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Nueva función de embeddings corregida para Nvidia
        self.embedding_fn = NvidiaEmbeddingFunction(
            api_key=config.NVIDIA_API_KEY,
            model_name="nvidia/nv-embedqa-e5-v5"
        )
        
        # Obtener o crear la colección
        self.collection = self.client.get_or_create_collection(
            name="knowledge_corrections",
            embedding_function=self.embedding_fn
        )

    def add_feedback(self, feedback_id: str, text: str, metadata: dict = None):
        """Añade una corrección al índice vectorial."""
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[feedback_id]
        )
        print(f"[VECTOR REAL] Documento {feedback_id} indexado en ChromaDB.")

    def query_similar(self, query_text: str, n_results: int = 3):
        """Busca información relacionada semánticamente."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

vector_store = VectorStore()
