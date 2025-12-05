# 🏛️ REPOSITORY PATTERN - REGRA OBRIGATÓRIA

**Data**: 04/Dez/2025  
**Versão**: 1.0  
**Aplicável**: TODOS os projetos Python/Django/FastAPI  
**Prioridade**: CRÍTICA ⚠️

---

## ⚠️ REGRA DE OURO

**TODO acesso ao ORM DEVE ser feito através de um Repository!**

**NUNCA**:
```python
# ❌ ERRADO - ORM direto na view/controller
def get_users():
    return User.objects.filter(is_active=True)
```

**SEMPRE**:
```python
# ✅ CORRETO - ORM no Repository
class UserRepository:
    @staticmethod
    def get_active_users():
        return User.objects.filter(is_active=True)
```

---

## 📁 ESTRUTURA OBRIGATÓRIA

### Django
```
app_name/
├── models/
│   └── user.py
├── repositories/
│   ├── __init__.py
│   └── user_repository.py      ← Toda manipulação de User
├── services/
│   └── user_service.py          ← Lógica de negócio
├── views.py                      ← Apenas chamadas aos services
└── api/
    └── user_views.py             ← API endpoints
```

### FastAPI
```
app/
├── models/
│   └── user.py
├── repositories/
│   ├── __init__.py
│   └── user_repository.py
├── controllers/
│   └── user_controller.py       ← Lógica de negócio
└── routers/
    └── user_router.py            ← Endpoints
```

---

## 📝 TEMPLATE DE REPOSITORY

```python
from typing import List, Optional
from django.db.models import QuerySet

from app.models import ModelName


class ModelNameRepository:
    """
    Repository para manipulação de ModelName.
    
    Responsabilidades:
    - CRUD operations
    - Queries complexas
    - Agregações
    - Filtros customizados
    """
    
    @staticmethod
    def get_by_id(model_id: int) -> Optional[ModelName]:
        """Buscar por ID."""
        try:
            return ModelName.objects.get(id=model_id)
        except ModelName.DoesNotExist:
            return None
    
    @staticmethod
    def get_all() -> QuerySet[ModelName]:
        """Buscar todos os registros."""
        return ModelName.objects.all()
    
    @staticmethod
    def filter_by_status(status: str) -> QuerySet[ModelName]:
        """Filtrar por status."""
        return ModelName.objects.filter(status=status)
    
    @staticmethod
    def create(data: dict) -> ModelName:
        """Criar novo registro."""
        return ModelName.objects.create(**data)
    
    @staticmethod
    def update(model_id: int, data: dict) -> Optional[ModelName]:
        """Atualizar registro existente."""
        instance = ModelNameRepository.get_by_id(model_id)
        if not instance:
            return None
        
        for key, value in data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance
    
    @staticmethod
    def delete(model_id: int) -> bool:
        """Deletar registro."""
        instance = ModelNameRepository.get_by_id(model_id)
        if not instance:
            return False
        
        instance.delete()
        return True
    
    @staticmethod
    def count_by_status(status: str) -> int:
        """Contar registros por status."""
        return ModelName.objects.filter(status=status).count()
```

---

## 🎯 RESPONSABILIDADES

### Repository (Data Access Layer)
✅ **PODE**:
- `Model.objects.get()`
- `Model.objects.filter()`
- `Model.objects.create()`
- `Model.objects.update()`
- `Model.objects.delete()`
- `Model.objects.aggregate()`
- `Model.objects.annotate()`
- Queries complexas com JOINs

❌ **NÃO PODE**:
- Lógica de negócio
- Validações complexas (use Services)
- Cálculos (use Services)
- Chamadas a APIs externas

### Service (Business Logic Layer)
✅ **PODE**:
- Lógica de negócio
- Validações complexas
- Cálculos
- Orquestração entre múltiplos repositories
- Chamadas a APIs externas

❌ **NÃO PODE**:
- `Model.objects.xxx()` direto (use Repository)

### View/Controller (Presentation Layer)
✅ **PODE**:
- Request/Response handling
- Validação de entrada (básica)
- Chamadas aos Services
- Serialização

❌ **NÃO PODE**:
- `Model.objects.xxx()` direto (use Repository)
- Lógica de negócio (use Service)

---

## 🔍 EXEMPLO COMPLETO

### 1. Repository (`repositories/file_upload_repository.py`)
```python
from typing import List, Optional
from django.db.models import QuerySet, Q, Count

from kpi.models import FileUpload


class FileUploadRepository:
    """Repository para FileUpload."""
    
    @staticmethod
    def get_by_id(upload_id: str) -> Optional[FileUpload]:
        try:
            return FileUpload.objects.get(id=upload_id)
        except FileUpload.DoesNotExist:
            return None
    
    @staticmethod
    def get_pending() -> QuerySet[FileUpload]:
        return FileUpload.objects.filter(status='PENDING')
    
    @staticmethod
    def get_all_ordered() -> QuerySet[FileUpload]:
        return FileUpload.objects.all().order_by('-uploaded_at')
    
    @staticmethod
    def create(file, status='PENDING') -> FileUpload:
        return FileUpload.objects.create(file=file, status=status)
    
    @staticmethod
    def update_status(
        upload_id: str,
        status: str,
        log: str = None
    ) -> Optional[FileUpload]:
        upload = FileUploadRepository.get_by_id(upload_id)
        if not upload:
            return None
        
        upload.status = status
        if log:
            upload.log = log
        upload.save()
        return upload
    
    @staticmethod
    def get_stats() -> dict:
        return FileUpload.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            failed=Count('id', filter=Q(status='FAILED'))
        )
```

### 2. Service (`services/file_upload_service.py`)
```python
from kpi.repositories import FileUploadRepository
from kpi.services import process_excel


class FileUploadService:
    """Service para lógica de negócio de FileUpload."""
    
    @staticmethod
    def process_pending_file(upload_id: str, company_id: int) -> bool:
        """Processar arquivo pendente."""
        upload = FileUploadRepository.get_by_id(upload_id)
        if not upload:
            return False
        
        # Atualizar para PROCESSING
        FileUploadRepository.update_status(
            upload_id, 
            'PROCESSING'
        )
        
        try:
            success, message, stats = process_excel(
                upload.file,
                company_id
            )
            
            if success:
                FileUploadRepository.update_status(
                    upload_id,
                    'COMPLETED',
                    message
                )
            else:
                FileUploadRepository.update_status(
                    upload_id,
                    'FAILED',
                    message
                )
            
            return success
            
        except Exception as e:
            FileUploadRepository.update_status(
                upload_id,
                'FAILED',
                str(e)
            )
            return False
```

### 3. View (`views.py`)
```python
from kpi.repositories import FileUploadRepository
from kpi.services import FileUploadService


class UploadManagerView(LoginRequiredMixin, View):
    def get(self, request):
        # ✅ Usa Repository
        stats = FileUploadRepository.get_stats()
        uploads = FileUploadRepository.get_all_ordered()
        
        # Filtros
        status_filter = request.GET.get('status')
        if status_filter:
            uploads = uploads.filter(status=status_filter)
        
        context = {
            'uploads': uploads,
            'stats': stats
        }
        return render(request, 'upload_manager.html', context)
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return self.get(request)
        
        # ✅ Usa Repository
        FileUploadRepository.create(file=file)
        
        return redirect('upload_manager')
```

### 4. Management Command (`management/commands/process_files.py`)
```python
from django.core.management.base import BaseCommand

from kpi.repositories import FileUploadRepository
from kpi.services import FileUploadService


class Command(BaseCommand):
    help = 'Process pending file uploads'

    def handle(self, *args, **options):
        # ✅ Usa Repository
        pending_files = FileUploadRepository.get_pending()
        
        for upload in pending_files:
            # ✅ Usa Service
            FileUploadService.process_pending_file(
                upload.id,
                company_id=1
            )
```

---

## ✅ BENEFÍCIOS

1. **Separação de responsabilidades** - Cada camada tem seu papel
2. **Reusabilidade** - Queries usadas em vários lugares
3. **Testabilidade** - Fácil mockar repositories em testes
4. **Manutenibilidade** - Mudanças no ORM centralizadas
5. **Rastreabilidade** - Sabe onde está cada query
6. **Performance** - Otimizações centralizadas (select_related, prefetch_related)

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ ERRADO #1: ORM na View
```python
def get_uploads(request):
    uploads = FileUpload.objects.filter(status='PENDING')  # ❌
```

### ❌ ERRADO #2: ORM no Service
```python
class UploadService:
    def process(self, upload_id):
        upload = FileUpload.objects.get(id=upload_id)  # ❌
```

### ❌ ERRADO #3: Lógica de Negócio no Repository
```python
class FileUploadRepository:
    @staticmethod
    def process_file(upload_id):  # ❌ Lógica de negócio!
        upload = FileUpload.objects.get(id=upload_id)
        # ... cálculos, validações, etc
```

---

## 🎓 QUANDO CRIAR REPOSITORY

**SEMPRE** que tiver um Model Django/SQLAlchemy:
- ✅ `User` → `UserRepository`
- ✅ `FileUpload` → `FileUploadRepository`
- ✅ `Company` → `CompanyRepository`
- ✅ `BudgetMonth` → `BudgetMonthRepository`
- ✅ `FatoReceita` → `FatoReceitaRepository`
- ✅ Todos os models sem exceção!

---

## 📚 REFERÊNCIAS

- **Repository Pattern**: Martin Fowler
- **Clean Architecture**: Robert C. Martin
- **DDD**: Domain-Driven Design

---

**ESTE PADRÃO É OBRIGATÓRIO EM TODOS OS PROJETOS!** ⚠️

