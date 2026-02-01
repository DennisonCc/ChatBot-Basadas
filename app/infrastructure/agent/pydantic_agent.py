from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.domain.interfaces import IChatAgent, IBackendGateway
from app.infrastructure.common.config import config
import logfire

from app.infrastructure.common.context_loader import loader

class PydanticChatAgent(IChatAgent):
    def __init__(self, backend_gateway: IBackendGateway):
        self.backend_gateway = backend_gateway
        
        # Load system prompt from modular markdown files
        self.SYSTEM_PROMPT = loader.load_context("main.md")
        
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
        async def check_backend_health(ctx: RunContext[IBackendGateway]) -> str:
            """Verifica si el backend Flask está respondiendo correctamente."""
            is_healthy = await ctx.deps.check_health()
            if is_healthy:
                return "El backend Flask está ONLINE y respondiendo correctamente."
            else:
                return "El backend Flask parece estar OFFLINE o con errores."

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

    async def get_response(self, message: str, current_screen: str = "Principal") -> str:
        full_message = f"[Contexto: El usuario está en la pantalla '{current_screen}']\nUsuario: {message}"
        result = await self.agent.run(full_message, deps=self.backend_gateway)
        return result.output
