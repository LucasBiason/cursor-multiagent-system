# ⚖️ SEPARAÇÃO: Views de Template vs Views de API

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: CRÍTICA

---

## 🎯 REGRA DE OURO

**Views de Template** e **Views de API** devem estar em arquivos separados com responsabilidades claras.

---

## 📁 ESTRUTURA OBRIGATÓRIA

```
app/
├── views.py                    # Views de Template APENAS
├── api/
│   ├── __init__.py
│   ├── views.py               # Views de API (endpoints REST)
│   ├── serializers.py         # Serializers DRF
│   └── validators.py          # Validadores de entrada
├── controllers/
│   └── {model}_controller.py  # Business logic
├── repositories/
│   └── {model}_repository.py  # Data access
└── urls.py                     # Rotas (templates + API)
```

---

## 📄 VIEWS DE TEMPLATE

### Responsabilidades
✅ **Apenas servir templates HTML**  
✅ **Passar dados básicos** (dropdowns, filtros)  
✅ **Autenticação/Autorização** (decorators/mixins)  
✅ **Renderizar** template com context

❌ **NUNCA** fazer processamento de dados  
❌ **NUNCA** fazer queries complexas  
❌ **NUNCA** fazer cálculos  
❌ **NUNCA** acessar ORM diretamente (usar repositories)

### Estrutura
```python
# app/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

class DashboardView(LoginRequiredMixin, View):
    """Serve dashboard template with basic data."""
    
    def get(self, request):
        # Only basic data for dropdowns/filters
        context = {
            'years': [2024, 2025],
            'units': UnitRepository.get_all(),
        }
        return render(request, 'dashboard.html', context)
```

### O que NÃO fazer
```python
# ❌ ERRADO - Processamento na view
def get(self, request):
    # Processamento pesado
    data = compute_kpis()
    charts = generate_charts()
    return render(request, 'dashboard.html', {'data': data})

# ❌ ERRADO - ORM direto
def get(self, request):
    uploads = FileUpload.objects.filter(status='PENDING')  # ❌
    return render(request, 'uploads.html', {'uploads': uploads})

# ❌ ERRADO - POST com lógica de negócio
def post(self, request):
    file = request.FILES['file']
    # Validação inline
    if not file.name.endswith('.xlsx'):
        return redirect('error')
    # Processamento inline
    process_file(file)
    return redirect('success')
```

---

## 🔌 VIEWS DE API

### Responsabilidades
✅ **Receber dados** do request  
✅ **Chamar controller** com dados  
✅ **Serializar resposta**  
✅ **Retornar JSON**  
✅ **Tratar erros** (HTTP status codes)

❌ **NUNCA** acessar ORM diretamente  
❌ **NUNCA** fazer validação inline  
❌ **NUNCA** fazer lógica de negócio

### Estrutura
```python
# app/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import FileUploadSerializer
from ..controllers import FileUploadController

class FileUploadAPIView(APIView):
    """
    API endpoint for file uploads.
    POST /api/v1/uploads/ - Create upload
    """
    
    def post(self, request):
        # 1. Get data from request
        file_obj = request.FILES.get('file')
        
        # 2. Call controller
        result = FileUploadController.create_upload(file_obj)
        
        # 3. Handle result
        if not result['success']:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 4. Serialize and return
        serializer = FileUploadSerializer(result['upload'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

---

## 🔄 FLUXO COMPLETO

### Template View (GET)
```
Request → View → Repository.get_basic_data() → Context → Render Template
```

### API View (POST)
```
Request → API View → Controller → Validator → Repository → ORM
                  ↓
            Serializer → Response JSON
```

### Frontend (JavaScript)
```
User Action → Fetch API → JSON → Alpine.js → Update DOM
```

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: View com Lógica de Negócio
```python
# ❌ ERRADO
class UploadView(View):
    def post(self, request):
        file = request.FILES['file']
        
        # Validação inline ❌
        if not file.name.endswith('.xlsx'):
            return HttpResponse('Invalid file', status=400)
        
        # ORM direto ❌
        upload = FileUpload.objects.create(file=file)
        
        # Processamento ❌
        process_excel(upload.file.path)
        
        return redirect('success')

# ✅ CORRETO
class UploadView(View):
    def get(self, request):
        context = {}
        return render(request, 'upload.html', context)
    
    # POST via API, não via template view
```

### ❌ Exemplo 2: API sem Serializer
```python
# ❌ ERRADO
class UploadAPIView(APIView):
    def post(self, request):
        file = request.FILES['file']
        upload = FileUpload.objects.create(file=file)  # ORM direto ❌
        
        return Response({
            'id': upload.id,  # Serialização manual ❌
            'status': upload.status
        })

# ✅ CORRETO
class UploadAPIView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        result = FileUploadController.create_upload(file)
        
        serializer = FileUploadSerializer(result['upload'])
        return Response(serializer.data, status=201)
```

### ❌ Exemplo 3: View com Filtros Complexos
```python
# ❌ ERRADO
class ListUploadsView(View):
    def get(self, request):
        # Filtros complexos na view ❌
        uploads = FileUpload.objects.filter(status='COMPLETED')
        if request.GET.get('month'):
            uploads = uploads.filter(uploaded_at__month=...)
        
        context = {'uploads': uploads}
        return render(request, 'list.html', context)

# ✅ CORRETO
class ListUploadsView(View):
    def get(self, request):
        # Apenas serve template, dados via API
        return render(request, 'list.html', {})

# API separada
class ListUploadsAPIView(APIView):
    def get(self, request):
        filters = request.GET.dict()
        result = FileUploadController.list_uploads(filters)
        serializer = FileUploadSerializer(result, many=True)
        return Response(serializer.data)
```

---

## ✅ CHECKLIST

### Antes de Criar View

- [ ] É template ou API?
- [ ] Template: Apenas GET com dados básicos?
- [ ] API: Usa controller + serializer?
- [ ] Não tem ORM direto?
- [ ] Não tem lógica de negócio?

### Estrutura de Arquivos

- [ ] `views.py` - Apenas templates
- [ ] `api/views.py` - Apenas APIs REST
- [ ] `api/serializers.py` - Existe
- [ ] `controllers/` - Existe
- [ ] `repositories/` - Existe
- [ ] URLs separadas (templates vs API)

---

## 📚 REFERÊNCIAS

- Controller Pattern: `CONTROLLER_PATTERN_OBRIGATORIO.md`
- Repository Pattern: `REPOSITORY_PATTERN_OBRIGATORIO.md`
- API Versioning: `API_VERSIONING_OBRIGATORIO.md`

---

**VIEWS = THIN LAYER. CONTROLLERS = BUSINESS LOGIC.**

