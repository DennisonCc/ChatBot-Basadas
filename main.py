import uvicorn
import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.api.routes import router
from app.infrastructure.common.config import config

# Initialize Logfire
# logfire.configure()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Chatbot Support API",
        description="Asistente de soporte para el Sistema de Gestión de Personal (Clean Architecture)",
        version="2.0.0"
    )
    
    # Instrument with Logfire
    # logfire.instrument_fastapi(app)

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(router)

    @app.get("/")
    async def root():
        return {
            "name": "Chatbot Support API",
            "architecture": "Clean Architecture",
            "version": "2.0.0",
            "status": "running"
        }

    return app

app = create_app()

if __name__ == "__main__":
    print(f"🚀 Starting Chatbot Support API on port {config.CHATBOT_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=config.CHATBOT_PORT)
