import asyncio
import os
import sys

# Añadir el directorio raíz al path para importar app
sys.path.append(os.getcwd())

from app.infrastructure.agent.pydantic_agent import PydanticChatAgent
from app.infrastructure.external.flask_gateway import FlaskBackendGateway

async def test_flask_integration():
    print("\n--- PRUEBA DE INTEGRACIÓN: CHATBOT <-> FLASK API ---")
    
    gateway = FlaskBackendGateway()
    agent = PydanticChatAgent(gateway)
    
    # Preguntamos algo que requiera consultar el backend de Flask
    print("Usuario: ¿Me puedes decir quiénes son los empleados registrados?")
    
    # Nota: El agente usará la herramienta 'list_employees' que llama a http://localhost:5000/api/empleados
    response = await agent.get_response("¿Me puedes decir quiénes son los empleados registrados?")
    
    print(f"\nRespuesta del Bot:\n{response}")
    
    if "YANET" in response or "ANDRES" in response or "DAVID" in response:
        print("\n✅ ÉXITO: El chatbot consultó exitosamente la Flask API y recuperó los datos REALES.")
    else:
        print("\n❌ FALLO: El chatbot no parece haber recuperado los datos reales de la base de datos.")


if __name__ == "__main__":
    asyncio.run(test_flask_integration())
