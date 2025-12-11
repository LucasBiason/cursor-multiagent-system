# arquitetura - padrões e boas práticas

**última atualização:** 2025-12-08  
**aplicável a:** todos os projetos (django, fastapi)

---

## padrões obrigatórios

### repository pattern
- **obrigatório** para todo acesso ao orm
- **nunca** acessar orm diretamente em views/controllers
- **localização:** `app/repositories/`

### controller pattern
- **obrigatório** para toda lógica de negócio
- **views/apis** são apenas entry points
- **localização:** `app/controllers/`

### validators
- **obrigatório** para toda validação de entrada
- **controllers** nunca fazem validação inline
- **localização:** `app/validators/` ou `app/api/validators.py`

---

## repository pattern

### regra de ouro

**todo acesso ao orm deve ser feito através de um repository!**

```python
# ❌ errado - orm direto na view/controller
def get_users():
    return User.objects.filter(is_active=True)

# ✅ correto - orm no repository
class UserRepository:
    @staticmethod
    def get_active_users():
        return User.objects.filter(is_active=True)
```

### estrutura

```
app/
├── models/
│   └── user.py
├── repositories/
│   ├── __init__.py
│   └── user_repository.py
```

### template

```python
from typing import List, Optional
from django.db.models import QuerySet
from app.models import User


class UserRepository:
    """Repository para manipulação de User."""
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """Buscar por ID."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_all() -> QuerySet[User]:
        """Buscar todos os registros."""
        return User.objects.all()
    
    @staticmethod
    def create(data: dict) -> User:
        """Criar novo registro."""
        return User.objects.create(**data)
    
    @staticmethod
    def update(user_id: int, data: dict) -> Optional[User]:
        """Atualizar registro existente."""
        instance = UserRepository.get_by_id(user_id)
        if not instance:
            return None
        
        for key, value in data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance
```

### responsabilidades

**repository pode:**
- `model.objects.get()`
- `model.objects.filter()`
- `model.objects.create()`
- `model.objects.update()`
- `model.objects.delete()`
- queries complexas com joins

**repository não pode:**
- lógica de negócio
- validações complexas (usar services)
- cálculos (usar services)
- chamadas a apis externas

---

## controller pattern

### regra de ouro

**toda lógica de negócio deve estar em controllers!**

### arquitetura

```
Requisição/Comando
      ↓
View/API/Command (Entry Point)
      ↓
Controller (Business Logic)
      ↓
├── Validators (Validação de entrada)
├── Repositories (Acesso a dados/ORM)
├── Services (APIs externas)
└── Utils (Funções auxiliares)
```

### estrutura

```
app/
├── controllers/
│   ├── __init__.py
│   └── user_controller.py
├── repositories/
│   └── user_repository.py
├── validators/
│   └── user_validator.py
└── services/
    └── email_service.py
```

### template

```python
from typing import Optional
from app.repositories import UserRepository
from app.validators import UserValidator
from app.services import EmailService


class UserController:
    """Controller para gerenciar usuários."""
    
    @staticmethod
    def create_user(data: dict) -> Optional[User]:
        """Criar novo usuário.
        
        Args:
            data: Dados do usuário
            
        Returns:
            User criado ou None se validação falhar
        """
        # 1. Validar
        validation = UserValidator.validate(data)
        if not validation['valid']:
            return None
        
        # 2. Criar
        user = UserRepository.create(validation['data'])
        
        # 3. Ações adicionais (opcional)
        EmailService.send_welcome_email(user.email)
        
        # 4. Retornar
        return user
```

### responsabilidades

**entry points (views/apis/commands):**
- apenas receber requisição/parâmetros
- chamar controller
- retornar resposta

**controllers:**
- toda lógica de negócio
- orquestração de fluxo
- chamar validators
- chamar repositories
- chamar services
- tratar exceções
- retornar resultados

---

## validators

### regra de ouro

**controllers nunca fazem validação inline. sempre usam classes validator.**

### estrutura

```
app/
├── api/
│   └── validators.py          # validators para apis
├── controllers/
│   └── user_controller.py     # usa validators
```

### template

```python
from typing import Dict, Any


class UserValidator:
    """Validates user data."""
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user data.
        
        Returns:
            {'valid': bool, 'error': str|None, 'data': dict}
        """
        errors = []
        
        if not data.get('email'):
            errors.append('Email is required')
        
        if not data.get('name'):
            errors.append('Name is required')
        
        if errors:
            return {
                'valid': False,
                'error': '; '.join(errors),
                'data': None
            }
        
        return {
            'valid': True,
            'error': None,
            'data': data
        }
```

### responsabilidades

**validators podem:**
- validar tipos de dados
- validar formatos (extensões, regex)
- validar tamanhos (min, max)
- validar regras de negócio simples
- retornar `{'valid': bool, 'error': str, 'data': dict}`

**validators não podem:**
- acessar banco de dados
- fazer persistência
- fazer lógica complexa

---

## separação views (template vs api)

### regra de ouro

**views de template e views de api devem estar em arquivos separados.**

### estrutura

```
app/
├── views.py                    # views de template apenas
├── api/
│   ├── views.py               # views de api (endpoints rest)
│   ├── serializers.py
│   └── validators.py
```

### views de template

```python
# app/views.py
from django.views import View
from django.shortcuts import render
from app.repositories import UserRepository


class UserListView(View):
    """Serve template com lista de usuários."""
    
    def get(self, request):
        # apenas dados básicos
        context = {
            'users': UserRepository.get_all()
        }
        return render(request, 'users/list.html', context)
```

**responsabilidades:**
- apenas servir templates html
- passar dados básicos (dropdowns, filtros)
- autenticação/autorização
- renderizar template com context

**não pode:**
- processamento de dados
- queries complexas
- cálculos
- acesso orm direto

### views de api

```python
# app/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.controllers import UserController
from app.api.serializers import UserSerializer


class UserCreateAPIView(APIView):
    """API endpoint para criar usuário."""
    
    def post(self, request):
        user = UserController.create_user(request.data)
        
        if not user:
            return Response(
                {'error': 'Validation failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

**responsabilidades:**
- receber dados do request
- chamar controller
- serializar resposta
- retornar json
- tratar erros (http status codes)

**não pode:**
- acesso orm direto
- validação inline
- lógica de negócio

---

## nomenclatura

### services vs processors

**service = conexão com api/sistema externo**

```python
class EmailService:
    """Send emails via SendGrid API."""
    
class PaymentService:
    """Process payments via Stripe API."""
```

**processor = processamento interno**

```python
class ExcelProcessor:
    """Process Excel files and import data."""
    
class PDFProcessor:
    """Generate PDF reports from data."""
```

---

## retornos

### controllers retornam objetos

```python
# ✅ correto
def create_user(data: dict) -> Optional[User]:
    user = Repository.create(data)
    return user  # objeto, não dict

# ❌ errado
def create_user(data: dict):
    return {
        'success': True,
        'message': 'Created',
        'user': user
    }
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

---

## exemplos completos

### exemplo 1: repository completo

```python
from typing import List, Optional
from django.db.models import QuerySet, Q, Count
from app.models import FileUpload


class FileUploadRepository:
    """Repository para FileUpload."""
    
    @staticmethod
    def get_by_id(upload_id: str) -> Optional[FileUpload]:
        """Buscar por ID."""
        try:
            return FileUpload.objects.get(id=upload_id)
        except FileUpload.DoesNotExist:
            return None
    
    @staticmethod
    def get_pending() -> QuerySet[FileUpload]:
        """Buscar arquivos pendentes."""
        return FileUpload.objects.filter(status='PENDING')
    
    @staticmethod
    def get_all_ordered() -> QuerySet[FileUpload]:
        """Buscar todos ordenados por data."""
        return FileUpload.objects.all().order_by('-uploaded_at')
    
    @staticmethod
    def create(file, status='PENDING') -> FileUpload:
        """Criar novo upload."""
        return FileUpload.objects.create(file=file, status=status)
    
    @staticmethod
    def update_status(
        upload_id: str,
        status: str,
        log: str = None
    ) -> Optional[FileUpload]:
        """Atualizar status do upload."""
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
        """Obter estatísticas de uploads."""
        return FileUpload.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            failed=Count('id', filter=Q(status='FAILED'))
        )
```

### exemplo 2: controller completo

```python
from typing import Optional, Dict, Any
from app.repositories import FileUploadRepository, CompanyRepository
from app.validators import FileUploadValidator
from app.services import ExcelProcessingService


class FileUploadController:
    """
    Controller para gerenciar uploads de arquivos.
    
    Responsabilidades:
    - Orquestrar o processamento de arquivos
    - Validar dados
    - Chamar repositories
    - Chamar services
    - Tratar exceções
    """
    
    @staticmethod
    def process_pending_files() -> None:
        """Processar arquivos pendentes."""
        pending_files = FileUploadRepository.get_pending()
        
        if not pending_files.exists():
            return
        
        for upload in pending_files:
            FileUploadController.process_single_file(upload.id)
    
    @staticmethod
    def process_single_file(upload_id: str) -> Dict[str, Any]:
        """
        Processar um arquivo específico.
        
        Args:
            upload_id: ID do upload
            
        Returns:
            Dict com resultado do processamento
        """
        upload = FileUploadRepository.get_by_id(upload_id)
        if not upload:
            return {"success": False, "error": "Upload não encontrado"}
        
        # Validar
        validation = FileUploadValidator.validate_file(upload.file)
        if not validation["valid"]:
            FileUploadRepository.update_status(
                upload, 
                'FAILED', 
                validation["error"]
            )
            return {"success": False, "error": validation["error"]}
        
        # Atualizar status
        FileUploadRepository.update_status(upload, 'PROCESSING')
        
        try:
            # Buscar empresa
            company = CompanyRepository.get_first()
            if not company:
                company, _ = CompanyRepository.get_or_create(
                    name="Comunita",
                    slug="comunita"
                )
            
            # Processar arquivo
            result = ExcelProcessingService.process_excel(
                upload.file,
                company.id
            )
            
            if result["success"]:
                FileUploadRepository.update_status(
                    upload,
                    'COMPLETED',
                    result["message"]
                )
            else:
                FileUploadRepository.update_status(
                    upload,
                    'FAILED',
                    result["error"]
                )
            
            return result
            
        except Exception as e:
            FileUploadRepository.update_status(
                upload,
                'FAILED',
                str(e)
            )
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def create_upload(file_obj) -> Optional[FileUpload]:
        """
        Criar novo upload.
        
        Args:
            file_obj: Arquivo enviado
            
        Returns:
            FileUpload criado ou None se validação falhar
        """
        # Validar
        validation = FileUploadValidator.validate_file(file_obj)
        if not validation["valid"]:
            return None
        
        # Criar
        upload = FileUploadRepository.create(file=file_obj)
        return upload
```

### exemplo 3: validator completo

```python
from typing import Dict, Any


class FileUploadValidator:
    """Validates file upload data."""
    
    @staticmethod
    def validate_file(file_obj) -> Dict[str, Any]:
        """
        Validate uploaded file.
        
        Args:
            file_obj: Django UploadedFile object
            
        Returns:
            dict: {'valid': bool, 'error': str|None, 'data': dict}
        """
        errors = []
        
        # Check if file exists
        if not file_obj:
            return {
                'valid': False,
                'error': 'No file provided',
                'data': None
            }
        
        # Check file extension
        allowed_extensions = ['.xlsx', '.xls']
        file_ext = file_obj.name.split('.')[-1].lower()
        
        if f'.{file_ext}' not in allowed_extensions:
            errors.append(f'Invalid file type. Allowed: {", ".join(allowed_extensions)}')
        
        # Check file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        if file_obj.size > max_size:
            errors.append(f'File too large. Max size: 50MB')
        
        # Check if file is readable
        try:
            file_obj.seek(0)
        except Exception as e:
            errors.append(f'Cannot read file: {str(e)}')
        
        if errors:
            return {
                'valid': False,
                'error': '; '.join(errors),
                'data': None
            }
        
        return {
            'valid': True,
            'error': None,
            'data': {
                'filename': file_obj.name,
                'size': file_obj.size,
                'content_type': file_obj.content_type
            }
        }
```

### exemplo 4: view de template

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from app.repositories import FileUploadRepository


class UploadManagerView(LoginRequiredMixin, View):
    """Serve template de gerenciamento de uploads."""
    
    def get(self, request):
        # Apenas dados básicos para template
        stats = FileUploadRepository.get_stats()
        uploads = FileUploadRepository.get_all_ordered()
        
        # Filtros simples
        status_filter = request.GET.get('status')
        if status_filter:
            uploads = uploads.filter(status=status_filter)
        
        context = {
            'uploads': uploads,
            'stats': stats
        }
        return render(request, 'upload_manager.html', context)
```

### exemplo 5: view de api

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.controllers import FileUploadController
from app.api.serializers import FileUploadSerializer


class FileUploadAPIView(APIView):
    """
    API endpoint for file uploads.
    POST /api/v1/uploads/ - Create upload
    """
    
    def post(self, request):
        # 1. Get data from request
        file_obj = request.FILES.get('file')
        
        # 2. Call controller
        upload = FileUploadController.create_upload(file_obj)
        
        # 3. Handle result
        if not upload:
            return Response(
                {'error': 'Validation failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 4. Serialize and return
        serializer = FileUploadSerializer(upload, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

---

## violações comuns

### ❌ exemplo 1: orm direto na view
```python
# ❌ errado
def get_uploads(request):
    uploads = FileUpload.objects.filter(status='PENDING')  # ❌
    return render(request, 'uploads.html', {'uploads': uploads})

# ✅ correto
def get_uploads(request):
    uploads = FileUploadRepository.get_pending()  # ✅
    return render(request, 'uploads.html', {'uploads': uploads})
```

### ❌ exemplo 2: lógica de negócio no command
```python
# ❌ errado
class Command(BaseCommand):
    def handle(self, *args, **options):
        uploads = FileUpload.objects.filter(status='PENDING')
        for upload in uploads:
            try:
                company = Company.objects.first()
                result = process_excel(upload.file, company.id)
                upload.status = 'COMPLETED'
                upload.save()
            except Exception as e:
                upload.status = 'FAILED'
                upload.save()

# ✅ correto
class Command(BaseCommand):
    def handle(self, *args, **options):
        FileUploadController.process_pending_files()  # ✅
```

### ❌ exemplo 3: validação inline no controller
```python
# ❌ errado
class FileUploadController:
    @staticmethod
    def create_upload(file_obj):
        # Validação inline ❌
        if not file_obj:
            return None
        if file_obj.size > 50*1024*1024:
            return None
        
        upload = FileUploadRepository.create(file=file_obj)
        return upload

# ✅ correto
class FileUploadController:
    @staticmethod
    def create_upload(file_obj):
        # Delega validação ✅
        validation = FileUploadValidator.validate_file(file_obj)
        if not validation['valid']:
            return None
        
        upload = FileUploadRepository.create(file=file_obj)
        return upload
```

### ❌ exemplo 4: controller retorna dict com status
```python
# ❌ errado
def create_upload(file_obj):
    upload = Repository.create(file=file_obj)
    return {
        'success': True,  # ❌ não precisa
        'message': 'Created',  # ❌ não precisa
        'upload': upload
    }

# ✅ correto
def create_upload(file_obj):
    validation = Validator.validate(file_obj)
    if not validation['valid']:
        return None  # ou raise exception
    
    upload = Repository.create(file=file_obj)
    return upload  # apenas o objeto
```

---

## benefícios

1. **separação clara de responsabilidades** - cada camada tem seu papel
2. **código testável** - controllers isolados, fácil mockar
3. **reutilização** - controllers usados por views, apis, commands
4. **manutenibilidade** - lógica centralizada
5. **escalabilidade** - fácil adicionar novos entry points
6. **rastreabilidade** - sabe onde está cada query
7. **performance** - otimizações centralizadas (select_related, prefetch_related)

---

## checklist

### estrutura
- [ ] repositories criados para cada model
- [ ] controllers criados para cada domínio
- [ ] validators criados para validações
- [ ] views de template separadas de views de api
- [ ] services para apis externas
- [ ] processors para processamento interno

### repository
- [ ] métodos estáticos
- [ ] apenas acesso ao orm
- [ ] sem lógica de negócio
- [ ] sem validações complexas

### controller
- [ ] métodos estáticos
- [ ] toda lógica de negócio
- [ ] chama validators primeiro
- [ ] chama repositories
- [ ] chama services/processors
- [ ] retorna objetos (não dicts)

### validator
- [ ] métodos estáticos
- [ ] retorna `{'valid', 'error', 'data'}`
- [ ] não acessa banco
- [ ] não faz persistência

### view de template
- [ ] apenas serve templates
- [ ] dados básicos apenas
- [ ] sem processamento pesado
- [ ] sem orm direto

### view de api
- [ ] chama controller
- [ ] usa serializer
- [ ] define http status
- [ ] sem orm direto
- [ ] sem lógica de negócio

---

## referências

- python patterns → `python.md`
- api rest → `api-rest.md`
- testing → `testing.md`
- security → `security.md`

---

**estes padrões são obrigatórios em todos os projetos.**

