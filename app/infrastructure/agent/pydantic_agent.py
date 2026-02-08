from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.domain.interfaces import IChatAgent, IBackendGateway
from app.infrastructure.common.config import config
import logfire

from app.infrastructure.common.context_loader import loader
from app.infrastructure.database.vector_store import vector_store

class PydanticChatAgent(IChatAgent):
    def __init__(self, backend_gateway: IBackendGateway):
        self.backend_gateway = backend_gateway
        
        # Load system prompt from modular markdown files (including user corrections)
        self.SYSTEM_PROMPT = loader.load_full_context("main.md")
        
        # Initialize Provider and Model
        provider = OpenAIProvider(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=config.NVIDIA_API_KEY,
        )
        model = OpenAIModel(config.MODEL_NAME, provider=provider)

        self.agent = Agent(
            model,
            system_prompt=self.SYSTEM_PROMPT,
            deps_type=IBackendGateway,
        )

        # Register tools
        self._register_tools()

    def _register_tools(self):
        @self.agent.tool
        async def list_employees(ctx: RunContext[IBackendGateway]) -> str:
            """Obtiene la lista de todos los empleados desde el backend Flask."""
            employees = await ctx.deps.get_employees()
            if not employees:
                return "No se pudieron recuperar los empleados o la lista está vacía."
            return str([e.dict() for e in employees])

        @self.agent.tool
        async def get_pause_history(ctx: RunContext[IBackendGateway], ci: str = '%', fecha: str = None) -> str:
            """Consulta el historial de pausas desde el backend Flask."""
            pauses = await ctx.deps.get_pause_history(ci, fecha)
            if not pauses:
                return "No se encontraron registros de pausas para los criterios especificados."
            return str([p.dict() for p in pauses])

        @self.agent.tool
        def get_navigation_guide(ctx: RunContext[IBackendGateway], screen_name: str) -> str:
            """Proporciona instrucciones sobre cómo llegar o qué hacer en una pantalla específica."""
            guides = {
                "Login": "Pantalla inicial. Si tienes problemas para entrar, verifica que tu usuario y contraseña sean los correctos.",
                "Personal": "Aquí puedes ver la lista de empleados. Si un empleado no aparece en 'Tiempos Fuera', asegúrate de que esté registrado y ACTIVO aquí.",
                "Tiempos Fuera": "Pantalla de Pausas Activas. Si cometiste un error en un registro, busca la tabla de 'Historial' abajo, usa la papelera para borrarlo y regístralo de nuevo.",
                "Historial": "Se encuentra en la parte inferior de 'Tiempos Fuera'. Aquí puedes 'Actualizar' una pausa para ponerle la hora de fin si el empleado ya regresó.",
            }
            return guides.get(screen_name, "Pantalla no reconocida. Las opciones principales son: Login, Personal, Tiempos Fuera, Historial.")

        @self.agent.tool
        def save_user_feedback(ctx: RunContext[IBackendGateway], info_tipo: str, info_contenido: str, contexto: str = "") -> str:
            """
            Guarda información adicional proporcionada por el usuario durante la conversación.
            
            Args:
                info_tipo: Tipo de información
                info_contenido: El contenido a guardar
                contexto: Contexto adicional
            """
            from app.application.feedback_service import feedback_service
            from app.domain.models import FeedbackRequest
            
            feedback = FeedbackRequest(
                original_question=f"[{info_tipo.upper()}]",
                original_response=contexto,
                corrected_response=info_contenido,
                category=info_tipo,
                session_id="organic-feedback"
            )
            
            result = feedback_service.save_feedback(feedback)
            
            if result.success:
                return f"✅ Información guardada e indexada en ChromaDB (ID: {result.feedback_id})."
            else:
                return f"❌ Error al guardar: {result.message}"

    async def get_response(self, message: str, current_screen: str = "Principal") -> str:
        # Búsqueda Semántica Real (RAG)
        additional_context = ""
        try:
            search_results = vector_store.query_similar(message, n_results=2)
            if search_results and search_results['documents'] and search_results['documents'][0]:
                relevant_docs = search_results['documents'][0]
                additional_context = "\n### 🧠 MEMORIA VECTORIAL (Recuperado):\n"
                for doc in relevant_docs:
                    additional_context += f"- {doc}\n"
        except Exception as e:
            print(f"[RAG ERROR] {e}")

        full_message = f"[PANTALLA: {current_screen}]\n{additional_context}\nUsuario: {message}"
        result = await self.agent.run(full_message, deps=self.backend_gateway)
        return result.output
