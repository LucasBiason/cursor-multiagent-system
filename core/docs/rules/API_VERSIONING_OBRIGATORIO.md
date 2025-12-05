# 🔢 API VERSIONING - OBRIGATÓRIO

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: CRÍTICA

---

## 🎯 REGRA DE OURO

**TODAS as APIs REST devem ter versionamento explícito no path.**

---

## ✅ PADRÃO OBRIGATÓRIO

### Estrutura de URLs
```
/{app}/api/v1/{resource}/
```

### Exemplos Corretos
```python
# ✅ CORRETO
/kpi/api/v1/uploads/
/kpi/api/v1/uploads/{id}/
/dashboard/api/v1/stats/
/dashboard/api/v1/charts/
/users/api/v1/profile/
```

### Exemplos Errados
```python
# ❌ ERRADO - Sem versionamento
/api/uploads/
/kpi/api/uploads/
/dashboard/stats/

# ❌ ERRADO - Versionamento no header
Headers: { 'API-Version': 'v1' }

# ❌ ERRADO - Versionamento no query param
/api/uploads/?version=v1
```

---

## 📁 ESTRUTURA DE ARQUIVOS

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

---

## 🔧 IMPLEMENTAÇÃO

### URLs Principais
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
```

### URLs da API
```python
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

### API Views
```python
# app/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import FileUploadSerializer
from ..controllers import FileUploadController

class FileUploadCreateAPIView(APIView):
    """
    POST /app/api/v1/uploads/create/
    Create new file upload
    """
    
    def post(self, request):
        file_obj = request.FILES.get('file')
        
        result = FileUploadController.create_upload(file_obj)
        
        if not result['success']:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = FileUploadSerializer(result['upload'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

---

## 🔄 MIGRAÇÃO DE VERSÕES

### Quando Criar Nova Versão?

Crie `v2` quando:
- Breaking changes na API
- Mudança de estrutura de response
- Remoção de campos
- Mudança de tipos de dados

### Como Manter Múltiplas Versões
```python
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

---

## 📊 VERSIONAMENTO NO SISTEMA

### Config URLs
```python
# config/urls.py
urlpatterns = [
    path('kpi/', include('kpi.urls')),
    path('dashboard/', include('dashboard.urls')),
]
```

### App URLs
```python
# kpi/urls.py
urlpatterns = [
    # Templates
    path('upload/', UploadView.as_view()),
    
    # API v1
    path('api/v1/', include('kpi.api.urls')),
]
```

### Resultado Final
```
/kpi/upload/              → Template
/kpi/api/v1/uploads/      → API v1
/dashboard/               → Template
/dashboard/api/v1/stats/  → API v1
```

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: API sem Versão
```python
# ❌ ERRADO
path('api/uploads/', UploadAPIView)

# ✅ CORRETO
path('api/v1/uploads/', UploadAPIView)
```

### ❌ Exemplo 2: Versão no Nome
```python
# ❌ ERRADO
path('api/uploads/', UploadV1APIView)  # Versão no nome da classe

# ✅ CORRETO
path('api/v1/uploads/', UploadAPIView)  # Versão no path
```

### ❌ Exemplo 3: Misturar Templates e API
```python
# ❌ ERRADO
urlpatterns = [
    path('uploads/', UploadView),        # Template
    path('uploads/create/', UploadAPI),  # API sem /api/v1/
]

# ✅ CORRETO
urlpatterns = [
    path('upload/', UploadView),              # Template
    path('api/v1/uploads/', UploadListAPI),   # API
    path('api/v1/uploads/create/', UploadCreateAPI),
]
```

---

## 📝 DOCUMENTAÇÃO DE API

### Swagger/OpenAPI
Todas as APIs devem ser documentadas:
```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="KPI API",
        default_version='v1',
    ),
)

urlpatterns = [
    path('api/v1/docs/', schema_view.with_ui('swagger')),
]
```

---

## ✅ CHECKLIST

### Estrutura
- [ ] APIs em `app/api/`
- [ ] Templates em `app/views.py`
- [ ] Versionamento `api/v1/`
- [ ] Serializers criados
- [ ] Controllers existem
- [ ] Repositories existem

### URLs
- [ ] Templates: `/{app}/{page}/`
- [ ] APIs: `/{app}/api/v1/{resource}/`
- [ ] Sem mistura de concerns

### Código
- [ ] Views de template sem lógica
- [ ] API views usam controllers
- [ ] Serializers para todos os responses
- [ ] Sem ORM direto nas views

---

**API = /api/v1/. TEMPLATES = SEM /api/.**

