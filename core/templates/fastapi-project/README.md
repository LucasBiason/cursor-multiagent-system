# FastAPI Project Template

**Template para criação de microsserviços FastAPI com ou sem a biblioteca `fastapi-microservice-framework`.**

---

## 📁 Estrutura do Template

Este template oferece duas versões:

1. **`basic/`** - Estrutura básica sem a biblioteca framework
2. **`with-framework/`** - Estrutura usando a biblioteca `fastapi-microservice-framework`

---

## 🎯 Regras para Decisão do Agente

### Use **Basic** (`basic/`) quando:

✅ Projeto simples ou MVP  
✅ Projeto de estudo/aprendizado  
✅ Quer controle total sobre dependências  
✅ Não precisa de padrões pré-implementados  
✅ Projeto único (não faz parte de ecossistema de microsserviços)  
✅ Quer começar rápido  
✅ Não precisa de autenticação via serviço externo  
✅ Não precisa de cache distribuído  
✅ Não precisa de filas (MQTT/Kafka)  

**Exemplos:**
- API REST simples
- MVP de produto
- Projeto de aprendizado
- Microserviço simples e isolado
- Projetos pessoais/portfólio

### Use **With Framework** (`with-framework/`) quando:

✅ Criando múltiplos microsserviços em um projeto  
✅ Precisa de padrões já implementados  
✅ Quer consistência entre microsserviços  
✅ Precisa de autenticação via serviço externo (JWT)  
✅ Quer configuração centralizada de banco  
✅ Precisa de cache distribuído (Redis)  
✅ Precisa de filas (MQTT/Kafka)  
✅ Precisa de observabilidade avançada (tracing, metrics)  
✅ Quer gerenciamento automático de migrations (Alembic)  
✅ Precisa de SQL puro com proteção contra SQL injection  

**Exemplos:**
- Sistema de gestão empresarial com múltiplos serviços
- Ecossistema de microsserviços
- Projetos que precisam de padrões consistentes
- Sistemas enterprise

---

## 📚 Como Usar a Biblioteca `fastapi-microservice-framework`

### Instalação

```bash
pip install git+https://github.com/LucasBiason/fastapi-microservice-framework.git
```

### Uso Básico

```python
from fastapi_microservice_framework import MicroserviceBuilder
from src.api.v1.routers import api_router

# O builder cria o FastAPI app internamente (factory pattern)
app = (
    MicroserviceBuilder(
        title="My Service",
        summary="Service description",
        description="Detailed description",
        version="1.0.0"
    )
    .with_database()              # Configuração centralizada + Alembic + Raw SQL
    .with_cache()                  # Redis (padrão), customizável
    .with_queue(broker="kafka")    # Kafka ou MQTT
    .with_observability()          # Logging estruturado, tracing, metrics
    .with_authentication()        # JWT via serviço externo
    .with_cors()                   # CORS configuration
    .with_routers([api_router])    # Include routers
    .build()                       # Retorna FastAPI app configurado
)

# Ou iniciar servidor diretamente:
if __name__ == "__main__":
    builder.run()  # Inicia uvicorn automaticamente
```

### O que o Builder Configura Automaticamente

- ✅ Criação do FastAPI app (factory pattern)
- ✅ Exception handlers (AppException, ValidationError, DatabaseError)
- ✅ Middleware de logging (request/response/error)
- ✅ Middleware de autenticação (JWT)
- ✅ CORS configuration
- ✅ Health check endpoint (`/health`)
- ✅ OpenAPI/Swagger/ReDoc (`/docs`, `/redoc`, `/openapi.json`)
- ✅ Startup/shutdown events (com handlers customizáveis)
- ✅ Validação de variáveis de ambiente
- ✅ Uvicorn server startup (método `run()`)

### Componentes da Biblioteca

- **Database Layer**: SQLAlchemy 2.0, Alembic migrations, Raw SQL com proteção
- **Cache System**: Redis (padrão), customizável
- **Queue System**: Kafka, MQTT com conexões robustas
- **Observability**: Logging estruturado (Grafana/Prometheus), tracing, metrics
- **Authentication**: JWT via serviço externo, OAuth2
- **Middleware System**: CORS, logging, custom middleware

**Documentação completa:** Ver repositório: https://github.com/LucasBiason/fastapi-microservice-framework

---

## 🏗️ Estrutura Básica (Sem Biblioteca)

### Estrutura de Diretórios

```
src/
├── api/
│   └── v1/
│       └── routers.py          # API endpoints
├── core/
│   ├── config.py               # Configurações (Pydantic Settings)
│   ├── database.py             # Conexão com banco (SQLAlchemy)
│   ├── dependencies.py         # Dependencies (get_db, etc.)
│   ├── exceptions.py           # Exception handlers
│   └── logging.py              # Configuração de logging
├── users/                      # Exemplo de domínio
│   ├── router.py               # Endpoints do domínio
│   ├── schemas.py              # Pydantic models
│   ├── models.py               # SQLAlchemy models
│   ├── service.py              # Business logic
│   └── dependencies.py         # Dependencies do domínio
└── main.py                     # Entry point
```

### Exemplo de `main.py` (Basic)

```python
from fastapi import FastAPI
from src.core.config import settings
from src.core.database import engine, Base
from src.api.v1.routers import api_router

# Criar tabelas (em desenvolvimento)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Exemplo de Router

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.dependencies import get_db
from src.users.schemas import UserCreate, UserResponse
from src.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.create_user(user_data)
```

### Exemplo de Service

```python
from sqlalchemy.orm import Session
from src.users.models import User
from src.users.schemas import UserCreate

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

---

## 📖 Referências

### Skills Relacionadas

- **FastAPI Skill:** `skills/backend/fastapi/SKILL.md`
- **Dockerfile:** `skills/infrastructure/dockerfile-generator/SKILL.md`
- **Entrypoint:** `skills/infrastructure/docker-entrypoint/SKILL.md`
- **Makefile:** `skills/infrastructure/makefile/SKILL.md`

### Templates de Código

- **Database Snippets:** `core/templates/database/`
- **Cache Snippets:** `core/templates/cache/`

### Repositório da Biblioteca

- **fastapi-microservice-framework:** https://github.com/LucasBiason/fastapi-microservice-framework

---

## 🚀 Como Usar o Template

### Copiar Template

```bash
# Versão básica
cp -r core/templates/fastapi-project/basic my-project

# Versão com framework
cp -r core/templates/fastapi-project/with-framework my-project
```

### Ou Usar Script de Geração

```bash
./core/templates/fastapi-project/GENERATE_PROJECT.sh my-project basic
./core/templates/fastapi-project/GENERATE_PROJECT.sh my-project with-framework
```

---

**Última Atualização:** 2026-01-23
