"""
FastAPI Application Entry Point

Template com fastapi-microservice-framework.
Usa MicroserviceBuilder da biblioteca como fábrica para centralizar toda a infraestrutura.

O builder centraliza TUDO:
- Validação de variáveis de ambiente
- Criação do FastAPI app (factory pattern)
- Setup de logging estruturado (compatível com Grafana/Prometheus)
- Exception handlers
- Middleware (logging, auth, CORS)
- Health check endpoint
- OpenAPI/Swagger/ReDoc
- Startup/shutdown events
- Uvicorn server startup
"""
from fastapi_microservice_framework import MicroserviceBuilder

from src.core.config import settings
from src.api.v1.routers import api_router

# O logging é configurado automaticamente pelo builder via with_observability()

# Create and configure FastAPI app using MicroserviceBuilder factory
# O builder cria o app FastAPI internamente e configura TUDO automaticamente
builder = (
    MicroserviceBuilder(
        title=settings.PROJECT_NAME,
        summary=settings.DESCRIPTION,
        description=settings.DESCRIPTION,
        version=settings.VERSION
    )
    .with_database()              # Centralized DB config + Alembic migrations + Raw SQL
    .with_cache()                  # Cache system (Redis padrão, customizável) - valida env vars
    # .with_queue(broker="kafka", config={"bootstrap_servers": "localhost:9092"})  # Kafka - valida env vars
    # .with_queue(broker="mqtt", config={"broker": "localhost", "port": 1883})     # MQTT - valida env vars
    .with_observability()         # Logging, tracing, metrics
    .with_authentication()        # JWT via external service
    .with_cors()                  # CORS configuration
    # .with_custom_middleware(...)  # Add custom middleware if needed
    # .with_cqrs()                 # Uncomment for CQRS support (future)
    .with_routers([api_router])   # Include routers (lista de routers)
    # .with_startup_handler(async def custom_startup(): ...)  # Custom startup handlers
    # .with_shutdown_handler(async def custom_shutdown(): ...)  # Custom shutdown handlers
)

# Build the FastAPI app (factory pattern - app criado internamente pelo builder)
app = builder.build()

# O builder já configura:
# - Health check endpoint (/health)
# - OpenAPI/Swagger/ReDoc (/docs, /redoc, /openapi.json)
# - Startup/shutdown events (pode adicionar handlers customizados via with_startup_handler/with_shutdown_handler)
# - Exception handlers
# - Middleware (logging, auth, CORS)

# Para iniciar o servidor, use o método run() do builder:
if __name__ == "__main__":
    builder.run()  # Inicia uvicorn automaticamente
