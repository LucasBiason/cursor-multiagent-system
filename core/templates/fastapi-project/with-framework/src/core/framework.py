"""
Framework Integration

Integration with fastapi-microservice-framework.

This module re-exports the MicroserviceBuilder from the library.
The actual implementation is in the fastapi-microservice-framework repository.

Installation:
    pip install git+https://github.com/LucasBiason/fastapi-microservice-framework.git

The MicroserviceBuilder centralizes all microservice infrastructure:
- Environment variable validation
- FastAPI app creation (factory pattern)
- Structured logging (compatible with Grafana/Prometheus)
- Exception handlers
- Middleware (logging, auth, CORS)
- Health check endpoint
- OpenAPI/Swagger/ReDoc documentation
- Startup/shutdown events
- Uvicorn server startup
"""
from fastapi_microservice_framework import MicroserviceBuilder

__all__ = ["MicroserviceBuilder"]
