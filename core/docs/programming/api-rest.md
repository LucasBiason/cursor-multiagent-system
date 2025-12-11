# api rest - padrões e boas práticas

**última atualização:** 2025-12-08  
**aplicável a:** todas as apis rest (django rest framework, fastapi)

---

## versionamento obrigatório

### estrutura de urls

```
/{app}/api/v1/{resource}/
```

### exemplos corretos

```python
# ✅ correto
/kpi/api/v1/uploads/
/kpi/api/v1/uploads/{id}/
/dashboard/api/v1/stats/
/dashboard/api/v1/charts/
```

### exemplos errados

```python
# ❌ errado - sem versionamento
/api/uploads/
/kpi/api/uploads/

# ❌ errado - versionamento no header
Headers: { 'API-Version': 'v1' }

# ❌ errado - versionamento no query param
/api/uploads/?version=v1
```

### implementação

```python
# app/urls.py
urlpatterns = [
    # template views (sem /api/)
    path('', DashboardView.as_view(), name='dashboard'),
    
    # api routes (com versionamento)
    path('api/v1/', include('app.api.urls')),
]
```

---

## estrutura de urls

### resource-oriented design

```python
# ✅ correto - recursos, não ações
GET /api/v1/users/123        # get user
POST /api/v1/users            # create user
PUT /api/v1/users/123         # update user
DELETE /api/v1/users/123      # delete user

# ❌ errado - ações na url
POST /api/v1/users/create
GET /api/v1/getUser?id=123
```

### naming

- usar **plural nouns** para coleções (`/api/v1/users`, não `/api/v1/user`)
- versionamento obrigatório: `/{app}/api/v1/{resource}/`

---

## http methods

### métodos e semântica

- **GET**: read-only, idempotent, no side effects
- **POST**: create new resources, non-idempotent
- **PUT**: full resource replacement, idempotent
- **PATCH**: partial resource update, idempotent
- **DELETE**: remove resource, idempotent (returns 204 no content)

---

## request/response formats

### content-type

- sempre `application/json`

### field naming

- escolher uma convenção (snake_case para python, camelcase para node.js)
- **crítico:** nunca misturar convenções na mesma api

### data types

- tipos consistentes (iso 8601 dates, json numbers, json booleans)

---

## error handling (rfc 7807)

### formato padrão de erro

```json
{
  "type": "https://example.com/probs/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "Invalid input data",
  "instance": "/api/v1/users/123"
}
```

### http status codes

- `200 OK`: successful get, put, patch
- `201 Created`: successful post (include `Location` header)
- `204 No Content`: successful delete
- `400 Bad Request`: invalid request (validation errors)
- `401 Unauthorized`: missing or invalid authentication
- `403 Forbidden`: authenticated but not authorized
- `404 Not Found`: resource doesn't exist
- `409 Conflict`: resource conflict
- `422 Unprocessable Entity`: valid format but business logic error
- `429 Too Many Requests`: rate limit exceeded
- `500 Internal Server Error`: server error (never expose internals)

---

## paginação obrigatória

### cursor-based (preferido)

```python
# query parameters
?limit=20&cursor=eyJpZCI6MTIzfQ

# response
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTQ1fQ",
    "has_more": true
  }
}
```

### offset-based (aceitável)

```python
# query parameters
?limit=20&offset=40

# response
{
  "data": [...],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 40,
    "has_more": true
  }
}
```

### parâmetros padrão

- `limit`: default 20, max 100
- `offset` ou `cursor`: para paginação

---

## segurança

### authentication

```python
# bearer tokens
Authorization: Bearer <token>
```

### rate limiting

- implementar em todos os endpoints

### cors

- configurar corretamente (nunca `*` em produção)

### security headers

```python
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

### input sanitization

- nunca confiar em input do cliente
- validar na camada de validator

---

## versionamento

### url versioning (obrigatório)

- versão no path da url (`/api/v1/users`, `/api/v2/users`)
- breaking changes requerem nova versão
- non-breaking changes podem estar na mesma versão
- migration strategy: expand and contract

### estrutura de arquivos

```
app/
├── urls.py
│   └── urlpatterns = [
│         path('', TemplateView),           # Template
│         path('api/v1/', include('app.api.urls')),  # API v1
│       ]
├── api/
│   ├── __init__.py
│   ├── urls.py                 # URLs da API
│   │   └── urlpatterns = [
│   │         path('resource/', ResourceListView),
│   │         path('resource/<id>/', ResourceDetailView),
│   │       ]
│   ├── views.py                # API Views
│   ├── serializers.py          # Serializers DRF
│   └── validators.py           # Validators
```

### implementação completa

```python
# app/urls.py
from django.urls import path, include

urlpatterns = [
    # Template views (sem /api/)
    path('', DashboardView.as_view(), name='dashboard'),
    path('upload/', UploadView.as_view(), name='upload'),
    
    # API routes (com versionamento)
    path('api/v1/', include('app.api.urls')),
]

# app/api/urls.py
from django.urls import path
from .views import (
    FileUploadListAPIView,
    FileUploadDetailAPIView,
    FileUploadCreateAPIView,
)

urlpatterns = [
    path('uploads/', FileUploadListAPIView.as_view(), name='api_uploads_list'),
    path('uploads/<uuid:id>/', FileUploadDetailAPIView.as_view(), name='api_uploads_detail'),
    path('uploads/create/', FileUploadCreateAPIView.as_view(), name='api_uploads_create'),
]
```

### migração de versões

**quando criar nova versão?**

crie `v2` quando:
- breaking changes na api
- mudança de estrutura de response
- remoção de campos
- mudança de tipos de dados

**como manter múltiplas versões:**

```
app/
├── api/
│   ├── v1/
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── serializers.py
│   └── v2/
│       ├── urls.py
│       ├── views.py
│       └── serializers.py
```

**config urls:**

```python
# config/urls.py
urlpatterns = [
    path('kpi/', include('kpi.urls')),
    path('dashboard/', include('dashboard.urls')),
]

# kpi/urls.py
urlpatterns = [
    # Templates
    path('upload/', UploadView.as_view()),
    
    # API v1
    path('api/v1/', include('kpi.api.urls')),
]

# Resultado final:
# /kpi/upload/              → Template
# /kpi/api/v1/uploads/      → API v1
# /dashboard/               → Template
# /dashboard/api/v1/stats/  → API v1
```

### violações comuns

```python
# ❌ errado - api sem versão
path('api/uploads/', UploadAPIView)

# ✅ correto
path('api/v1/uploads/', UploadAPIView)
```

```python
# ❌ errado - versão no nome
path('api/uploads/', UploadV1APIView)  # versão no nome da classe

# ✅ correto
path('api/v1/uploads/', UploadAPIView)  # versão no path
```

```python
# ❌ errado - misturar templates e api
urlpatterns = [
    path('uploads/', UploadView),        # template
    path('uploads/create/', UploadAPI),  # api sem /api/v1/
]

# ✅ correto
urlpatterns = [
    path('upload/', UploadView),              # template
    path('api/v1/uploads/', UploadListAPI),   # api
    path('api/v1/uploads/create/', UploadCreateAPI),
]
```

---

## observability

### request ids

- incluir em todas as requests/responses (`X-Request-ID` header)

### structured logging

- usar logs estruturados (formato json)

### distributed tracing

- usar opentelemetry para microserviços

---

## framework-specific

### django rest framework

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
```

### fastapi

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    user = UserController.create_user(user_data.dict())
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation failed"
        )
    
    return UserResponse.from_orm(user)
```

---

## anti-patterns (nunca fazer)

- ❌ action verbs in urls
- ❌ mixed naming conventions
- ❌ generic error messages
- ❌ returning html on api errors
- ❌ exposing stack traces
- ❌ inconsistent response formats
- ❌ no pagination on list endpoints
- ❌ n+1 queries (use select_related/prefetch_related)
- ❌ no rate limiting
- ❌ versioning in headers

---

## retornos de controllers e apis

### controllers retornam objetos

```python
# ✅ correto
def create_user(data: dict) -> Optional[User]:
    validation = Validator.validate(data)
    if not validation['valid']:
        return None
    
    user = Repository.create(validation['data'])
    return user  # objeto, não dict
```

### apis serializam e definem status

```python
# ✅ correto
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate) -> UserResponse:
    user = UserController.create_user(user_data.dict())
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation failed"
        )
    
    return UserResponse.from_orm(user)
```

### tabela de retornos

| operação | controller retorna | api status | api response |
|----------|-------------------|------------|--------------|
| create | objeto ou none | 201 created ou 400 | serializer(objeto).data |
| update | objeto ou none | 200 ok ou 404 | serializer(objeto).data |
| delete | true/false/none | 204 no content ou 404 | vazio |
| list | queryset/list | 200 ok | serializer(lista, many=true).data |
| retrieve | objeto ou none | 200 ok ou 404 | serializer(objeto).data |

---

## boas práticas adicionais

### clareza e legibilidade

**código deve ser fácil de ler e entender:**
- nomes descritivos para variáveis, funções e classes
- estrutura de código organizada
- indentação adequada
- comentários quando necessário (explicar "porquê", não "o quê")

### documentação

**manter documentação atualizada:**
- swagger/openapi para todas as apis
- exemplos de request/response
- descrição de cada endpoint
- códigos de erro documentados

### desenvolvimento orientado por testes

**tdd quando possível:**
- escrever testes antes da implementação
- garantir que funcionalidades atendem requisitos
- facilitar detecção de erros

### revisão de código

**sempre revisar antes de merge:**
- verificar padrões de código
- verificar segurança
- verificar performance
- verificar testes

### integração contínua

**pipelines de ci:**
- rodar testes automaticamente
- verificar linting
- verificar cobertura de testes
- detectar erros precocemente

---

## referências

- api versioning → `api-rest.md` (seção versionamento)
- retornos controllers/apis → `architecture.md` (seção retornos)
- separação views → `architecture.md` (seção separação views)
- boas práticas gerais → pesquisas web sobre api rest best practices

---

**estas regras são obrigatórias em todas as apis rest.**

