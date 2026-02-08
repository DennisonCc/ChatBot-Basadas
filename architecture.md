# Documentación Técnica: Chatbot Support Assistant (Clean Architecture)

## 🏗️ Arquitectura del Sistema

El sistema sigue los principios de **Arquitectura Limpia (Clean Architecture)** y **SOLID**, permitiendo un desacoplamiento total entre la lógica de negocio, la inteligencia artificial y las interfaces externas.

### 1. Capas del Proyecto

#### 🔹 Dominio (`app/domain/`)
Es el corazón de la aplicación. Contiene las reglas de negocio puras e interfaces (contratos).
- **Models**: Definiciones de datos (`Employee`, `PauseRecord`, `ChatRequest`).
- **Interfaces**: Define qué deben hacer los componentes externos (`IBackendGateway`, `IChatAgent`) sin especificar cómo.

#### 🔹 Aplicación (`app/application/`)
Contiene los casos de uso. Orquesta el flujo de datos desde y hacia las entidades del dominio.
- **ChatService**: Recibe un mensaje, consulta al agente y devuelve la respuesta formateada. Depende de las interfaces del dominio, no de implementaciones concretas.

#### 🔹 Infraestructura (`app/infrastructure/`)
Implementaciones concretas de las interfaces del dominio.
- **Agent & Triple Memory**: 
    - **PydanticChatAgent**: El cerebro IA del sistema.
    - **Capa 1: Memoria Inmediata**: Módulos críticos (`personal.md`) cargados en el System Prompt para máxima fiabilidad.
    - **Capa 2: Memoria de Sesión**: Historial dinámico gestionado en memoria (RAM) para coherencia en la charla.
    - **Capa 3: Memoria RAG**: Búsqueda semántica en **ChromaDB** para manuales técnicos y feedback histórico.
- **Data Access**:
    - **SQLite (chatbot.db)**: Persistencia relacional para feedback y auditoría.
    - **ChromaDB (vector_db/)**: Base de datos de vectores para recuperación rápida (RAG).
- **External**:
    - **NVIDIA NIM Gateway**: Conexión con modelos LLM y de Embeddings (`nv-embedqa-e5-v5`).
    - **FlaskBackendGateway**: Conexión con el sistema legado.

---

## 🧠 Flujo de Memoria Unificado

1. **Sesión**: El sistema identifica al usuario y recupera su historial reciente.
2. **Consulta + RAG**: El usuario pregunta. Se genera un vector y se busca en **ChromaDB**.
3. **Fusión de Contexto**: Se combina el historial, el contexto RAG y las reglas maestras (System Prompt).
4. **Respuesta**: El LLM genera la respuesta con coherencia de conversación y base de conocimiento.

---

## 🚀 Guía de Ejecución

1. Asegúrate de tener las variables en `.env`.
2. Ejecuta el backend Flask (Puerto 5000).
3. Inicia el chatbot:
   ```bash
   python main.py
   ```

## 📊 Diagrama de Arquitectura Unificado (Triple Memoria)

```mermaid
graph TD
    subgraph Frontend Layer
        W[Chatbot Widget]
    end

    subgraph Chatbot_Engine
        R[API Routes] --> SVC[ChatService]
        SVC --> AGENT[Pydantic Agent]
        
        subgraph Memory_Stack
            IMM[System Prompt: Immediate]
            SESS[Session History: Short-term]
            RAG[Vector Store: Long-term]
        end
        
        AGENT --> IMM
        AGENT <--> SESS
        AGENT <--> RAG
    end

    subgraph External_AI
        NVIDIA["🟢 NVIDIA NIM API"]
    end

    W <--> R
    AGENT <--> NVIDIA
```
