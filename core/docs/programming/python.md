# python - padrões e boas práticas

**última atualização:** 2025-12-08  
**aplicável a:** todos os projetos python (django, fastapi, scripts)

---

## regras gerais

### código
- **sem emojis** em código python (pode corromper arquivos)
- **comentários e docstrings em inglês** (exceto notebooks de ensino)
- **type hints obrigatórios** em todas as funções
- **pep 8** - seguir guia de estilo python
- **linha máxima 79 caracteres** - obrigatório (PEP 8 E501)
- **código limpo** - profissional e manutenível

### organização de arquivos
- **project readme.md:** apenas um na raiz do projeto
- **documentação:** `docs/` ou `docs-private/` dentro do projeto
- **test files:** `Scripts e Deploys/` (nunca na raiz do projeto)
- **shell scripts:** `Scripts e Deploys/` (nunca na raiz do projeto)
- **nunca criar** múltiplos readme ou scripts de teste na raiz

### organização de classes e módulos
- **uma classe por arquivo:** cada classe deve estar em seu próprio arquivo
- **módulos com __init__.py:** usar estrutura de módulo onde `__init__.py` exporta todas as classes
- **nunca colocar múltiplas classes no mesmo arquivo:** isso torna o código difícil de navegar e manter
- **estrutura recomendada:**
  ```
  module_name/
    __init__.py          # Exporta todas as classes
    base.py              # Classe base (se houver)
    class_a.py           # Classe A
    class_b.py           # Classe B
    class_c.py           # Classe C
  ```

---

## type hints

### obrigatório em todas as funções

```python
# ✅ correto
def process_data(data: Dict[str, Any], count: int) -> List[str]:
    """Process data and return list of strings."""
    return []

# ❌ errado - sem type hints
def process_data(data, count):
    return []
```

### tipos comuns

```python
from typing import List, Dict, Any, Optional, Union, Tuple

# listas
def get_items() -> List[str]:
    return ["a", "b"]

# dicionários
def get_config() -> Dict[str, Any]:
    return {"key": "value"}

# opcionais
def find_user(user_id: int) -> Optional[User]:
    return User.objects.get(id=user_id) if exists else None

# union
def process(value: Union[str, int]) -> str:
    return str(value)

# tuplas
def get_coords() -> Tuple[float, float]:
    return (10.5, 20.3)
```

### type hints em classes

```python
class UserService:
    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
    
    def get_user(self, user_id: int) -> Optional[User]:
        return User.objects.get(id=user_id)
```

---

## docstrings

### padrão google style

```python
def process_video(
    video_path: str,
    scene_threshold: float = 0.5,
    sample_rate: int = 5
) -> List[SceneResult]:
    """Process a video file and return analysis results.
    
    This function orchestrates the complete video analysis pipeline:
    1. Video loading and validation
    2. Scene detection
    3. Face, emotion, and activity detection
    4. Result aggregation
    
    Args:
        video_path: Path to the video file
        scene_threshold: Threshold for scene detection (0.0-1.0). Defaults to 0.5.
        sample_rate: Frame sampling rate (process 1 every N frames). Defaults to 5.
        
    Returns:
        List of SceneResult objects with analysis data
        
    Raises:
        FileNotFoundError: If video file does not exist
        ValueError: If video cannot be processed
        
    Example:
        >>> results = process_video("video.mp4", scene_threshold=0.7)
        >>> print(f"Found {len(results)} scenes")
    """
    pass
```

### docstrings em classes

```python
class VideoProcessingService:
    """Service for processing videos and generating analysis results.
    
    This service orchestrates the complete video analysis pipeline:
    1. Video loading and validation
    2. Scene detection
    3. Face, emotion, and activity detection
    4. Result aggregation
    
    Attributes:
        scene_threshold: Threshold for scene detection
        sample_rate: Frame sampling rate
        
    Example:
        >>> service = VideoProcessingService(scene_threshold=0.5)
        >>> results = service.process_video("video.mp4")
    """
    
    def __init__(self, scene_threshold: float = 0.5, sample_rate: int = 5) -> None:
        """Initialize the video processing service.
        
        Args:
            scene_threshold: Threshold for scene detection (0.0-1.0)
            sample_rate: Frame sampling rate (process 1 every N frames)
        """
        self.scene_threshold = scene_threshold
        self.sample_rate = sample_rate
```

### docstrings em módulos

```python
"""
Video Processing Service

Service layer for video processing operations.
Handles video analysis orchestration and result aggregation.
"""
```

---

## classes vs funções

### preferir funções quando possível

```python
# ✅ preferir função
def calculate_total(items: List[Item]) -> float:
    return sum(item.price for item in items)

# ❌ classe desnecessária
class Calculator:
    def calculate_total(self, items: List[Item]) -> float:
        return sum(item.price for item in items)
```

### usar classes quando necessário

```python
# ✅ classe quando há estado
class VideoProcessor:
    def __init__(self, video_path: str) -> None:
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
    
    def get_info(self) -> Dict[str, Any]:
        return {"width": self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)}
    
    def release(self) -> None:
        self.cap.release()
```

### métodos estáticos

```python
class ContainerController:
    """Handles container-related business logic."""
    
    @staticmethod
    def list_all(repository: DockerRepository, all: bool = True) -> List[ContainerInfo]:
        """List all Docker containers.
        
        Args:
            repository: Docker repository instance
            all: Include stopped containers. Defaults to True.
            
        Returns:
            List of ContainerInfo models
        """
        containers = repository.list_containers(all=all)
        return [ContainerInfo(**c) for c in containers]
```

---

## django patterns

### estrutura de projeto

```
app_name/
├── models/
│   └── user.py
├── repositories/
│   ├── __init__.py
│   └── user_repository.py
├── validators/
│   └── user_validator.py
├── controllers/
│   └── user_controller.py
├── services/
│   └── email_service.py
├── views.py                    # template views apenas
├── api/
│   ├── views.py               # api views
│   ├── serializers.py
│   └── validators.py
└── management/
    └── commands/
        └── populate_data.py
```

### repository pattern (obrigatório)

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
            return User.objects.select_related('profile').get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_active_users() -> QuerySet[User]:
        """Buscar todos os usuários ativos.
        
        Uso select_related quando sei que vou precisar de relacionamentos.
        Isso evita N+1 queries.
        """
        return User.objects.filter(is_active=True).select_related('profile')
    
    @staticmethod
    def search_by_name(name: str) -> QuerySet[User]:
        """Busca usuários por nome (case-insensitive).
        
        Uso Q objects para queries mais complexas.
        """
        from django.db.models import Q
        return User.objects.filter(
            Q(first_name__icontains=name) | Q(last_name__icontains=name)
        )
    
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

### quando usar select_related e prefetch_related

```python
# ❌ Lento - N+1 queries
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # Query adicional para cada usuário!

# ✅ Rápido - Uma query com JOIN
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.bio)  # Dados já carregados
```

**select_related**: Para ForeignKey e OneToOne (JOIN SQL)  
**prefetch_related**: Para ManyToMany e Reverse ForeignKey (query separada otimizada)

### controller pattern (obrigatório)

```python
from typing import Dict, Any, Optional
from app.repositories import UserRepository
from app.validators import UserValidator
from app.services import EmailService
import logging

logger = logging.getLogger(__name__)


class UserController:
    """Orquestra toda lógica relacionada a usuários.
    
    Controllers não fazem validação (usam validators).
    Controllers não acessam ORM diretamente (usam repositories).
    Controllers não enviam emails (usam services).
    
    Eles apenas orquestram o fluxo.
    """
    
    @staticmethod
    def create_user(data: Dict[str, Any]) -> Optional[User]:
        """Cria novo usuário seguindo o fluxo completo.
        
        Fluxo:
        1. Validar dados
        2. Criar no banco
        3. Enviar email de boas-vindas
        4. Retornar usuário criado
        
        Se qualquer passo falhar, retorna None.
        """
        # 1. Validar
        validation = UserValidator.validate(data)
        if not validation['valid']:
            logger.warning(f"Validation failed: {validation['error']}")
            return None
        
        # 2. Criar
        try:
            user = UserRepository.create(validation['data'])
            logger.info(f"User created: {user.id}")
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return None
        
        # 3. Ações adicionais (não bloqueiam criação)
        try:
            EmailService.send_welcome_email(user.email)
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")
            # Não falha a criação se email falhar
        
        # 4. Retornar
        return user
    
    @staticmethod
    def update_user(user_id: int, data: Dict[str, Any]) -> Optional[User]:
        """Atualiza usuário existente."""
        # Validar
        validation = UserValidator.validate_update(data)
        if not validation['valid']:
            return None
        
        # Atualizar
        user = UserRepository.update(user_id, validation['data'])
        return user
```

### tratamento de erros em controllers

```python
# ✅ Controller retorna None
user = UserController.create_user(data)
if not user:
    return Response({'error': 'Failed'}, status=400)

# ❌ Controller não decide status HTTP
result = UserController.create_user(data)
if result['status'] == 'error':  # Controller não deveria saber de HTTP
    return Response(result, status=400)
```

### validators (obrigatório)

```python
from typing import Dict, Any
import re


class UserValidator:
    """Valida dados de usuário.
    
    Validators são stateless - não dependem de estado.
    Apenas validam dados e retornam resultado padronizado.
    """
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados para criação de usuário.
        
        Retorna sempre o mesmo formato:
        {
            'valid': bool,
            'error': str | None,
            'data': dict | None
        }
        
        Isso facilita o tratamento em controllers.
        """
        errors = []
        
        # Email
        email = data.get('email', '').strip()
        if not email:
            errors.append('Email é obrigatório')
        elif not UserValidator._is_valid_email(email):
            errors.append('Email inválido')
        
        # Nome
        name = data.get('name', '').strip()
        if not name:
            errors.append('Nome é obrigatório')
        elif len(name) < 2:
            errors.append('Nome deve ter pelo menos 2 caracteres')
        
        # Idade (opcional, mas se fornecida deve ser válida)
        age = data.get('age')
        if age is not None:
            try:
                age_int = int(age)
                if age_int < 0 or age_int > 150:
                    errors.append('Idade deve estar entre 0 e 150')
            except (ValueError, TypeError):
                errors.append('Idade deve ser um número')
        
        if errors:
            return {
                'valid': False,
                'error': '; '.join(errors),
                'data': None
            }
        
        # Retorna dados limpos e validados
        return {
            'valid': True,
            'error': None,
            'data': {
                'email': email.lower(),
                'name': name.title(),
                'age': int(age) if age is not None else None
            }
        }
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Valida formato de email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
```

### validação de arquivos

```python
import os

class FileValidator:
    """Valida uploads de arquivos."""
    
    @staticmethod
    def validate_file(file_obj, max_size_mb: int = 10) -> Dict[str, Any]:
        """Valida arquivo de upload.
        
        Args:
            file_obj: Django UploadedFile
            max_size_mb: Tamanho máximo em MB
            
        Returns:
            {'valid': bool, 'error': str | None, 'data': dict | None}
        """
        if not file_obj:
            return {
                'valid': False,
                'error': 'Nenhum arquivo fornecido',
                'data': None
            }
        
        # Tamanho
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_obj.size > max_size_bytes:
            return {
                'valid': False,
                'error': f'Arquivo muito grande (máx {max_size_mb}MB)',
                'data': None
            }
        
        # Extensão
        allowed_extensions = ['.xlsx', '.xls', '.csv']
        file_ext = os.path.splitext(file_obj.name)[1].lower()
        if file_ext not in allowed_extensions:
            return {
                'valid': False,
                'error': f'Extensão não permitida. Use: {", ".join(allowed_extensions)}',
                'data': None
            }
        
        return {
            'valid': True,
            'error': None,
            'data': {
                'filename': file_obj.name,
                'size': file_obj.size,
                'extension': file_ext
            }
        }
```

### separação views (template vs api)

```python
# app/views.py - template views apenas
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from app.repositories import UserRepository


class UserListView(LoginRequiredMixin, View):
    """Lista usuários em página HTML.
    
    View de template não faz processamento pesado.
    Dados complexos vêm via API (JavaScript faz fetch).
    """
    
    def get(self, request):
        # Apenas dados básicos para dropdowns, filtros, etc.
        context = {
            'total_users': UserRepository.count_all(),
            'years': [2024, 2025]  # Para filtros
        }
        return render(request, 'users/list.html', context)

# app/api/views.py - api views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from app.controllers import UserController
from app.api.serializers import UserSerializer


class UserCreateAPIView(APIView):
    """Cria usuário via API.
    
    POST /api/v1/users/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Cria novo usuário.
        
        Fluxo:
        1. Chama controller
        2. Se sucesso: retorna 201 com dados serializados
        3. Se falha: retorna 400 com erro
        """
        user = UserController.create_user(request.data)
        
        if not user:
            return Response(
                {'error': 'Falha na validação ou criação'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

### serializers

```python
from rest_framework import serializers
from app.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializa dados de usuário para API.
    
    Usa ModelSerializer para facilitar, mas pode customizar campos.
    """
    
    # Campos customizados
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'age', 'full_name', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_full_name(self, obj):
        """Calcula nome completo."""
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def validate_email(self, value):
        """Valida email no serializer também.
        
        Validação aqui é adicional - validação principal está no validator.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email já cadastrado")
        return value.lower()
```

### sql puro apenas para select

```python
# ✅ permitido - select
from app.utils.database import execute_query

results = execute_query(
    """
    SELECT u.name, SUM(r.amount) as total
    FROM units u
    JOIN revenues r ON u.id = r.unit_id
    WHERE u.company_id = %s
    GROUP BY u.name
    """,
    [company_id]
)

# ❌ proibido - insert/update/delete
# usar repository + orm
user = UserRepository.create(data=data)
```

### templates organização

```
templates/
├── base.html
├── components/
│   ├── navbar.html
│   └── footer.html
├── authentication/
│   └── login.html
└── dashboard/
    └── analytics.html
```

**settings.py:**
```python
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': False,  # forçar uso da pasta central
}]
```

### management commands

```
core/management/commands/    # commands globais
app/management/commands/      # commands específicos do app
```

```python
from django.core.management.base import BaseCommand
from app.controllers import UserController
from app.repositories import UserRepository


class Command(BaseCommand):
    help = 'Processa usuários pendentes'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Número máximo de usuários para processar'
        )
    
    def handle(self, *args, **options):
        """Processa usuários pendentes.
        
        Command não faz lógica - apenas chama controller.
        """
        limit = options['limit']
        
        self.stdout.write(f'Processando até {limit} usuários...')
        
        pending = UserRepository.get_pending()[:limit]
        
        for user in pending:
            result = UserController.process_user(user.id)
            if result:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Processado: {user.email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'✗ Falhou: {user.email}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nProcessamento concluído!')
        )
```

### migrations - nunca editar manualmente

**regra de ouro:** nunca edite migrations manualmente. se precisar mudar algo, crie nova migration.

```bash
# ✅ correto
python manage.py makemigrations
python manage.py migrate

# ❌ nunca fazer
# editar arquivo de migration manualmente
```

migrations são histórico. se você edita uma migration antiga, outros desenvolvedores (ou produção) terão problemas ao rodar migrations.

### settings - organização por ambiente

```
core/
└── settings/
    ├── __init__.py          # importa base
    ├── base.py              # configurações comuns
    ├── development.py       # desenvolvimento local
    └── production.py        # produção
```

```python
# core/settings/base.py
# configurações comuns a todos os ambientes

# core/settings/development.py
from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# core/settings/production.py
from .base import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

### sql puro apenas para select

**regra de ouro:** sql puro apenas para select (otimização). insert/update/delete via orm + repository (segurança).

#### permitido: select queries

```python
from app.utils.database import execute_query

# read-only queries via database.py
results = execute_query(
    """
    SELECT u.name, SUM(r.amount) as total
    FROM units u
    JOIN revenues r ON u.id = r.unit_id
    WHERE u.company_id = %s
    GROUP BY u.name
    """,
    [company_id]
)
```

**razão:** performance otimizada, agregações complexas.

#### proibido: insert/update/delete via sql puro

```python
# ❌ nunca fazer
cursor.execute("""
    INSERT INTO fato_receita (valor, data, projeto_id)
    VALUES (%s, %s, %s)
""", [valor, data, projeto_id])

# ✅ correto - via orm + repository
FatoReceitaRepository.create(
    valor=valor,
    data=data,
    projeto_id=projeto_id
)
```

#### módulo database.py

**localização:** `app/utils/database.py`

```python
"""
Database utilities for raw SQL queries.
ONLY for SELECT operations - never use for INSERT/UPDATE/DELETE.
"""
from django.db import connection
from typing import List, Dict, Any


def execute_query(query: str, params: List[Any] = None) -> List[Dict[str, Any]]:
    """
    Execute read-only SQL query.
    
    Args:
        query: SQL SELECT query
        params: Query parameters (for %s placeholders)
        
    Returns:
        List of dictionaries with results
        
    Example:
        results = execute_query(
            "SELECT id, name FROM users WHERE status = %s",
            ['active']
        )
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def execute_scalar(query: str, params: List[Any] = None) -> Any:
    """
    Execute query and return single value.
    
    Example:
        count = execute_scalar("SELECT COUNT(*) FROM users")
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        result = cursor.fetchone()
        return result[0] if result else None
```

#### razões de segurança

1. **sql injection prevention:** orm sanitiza automaticamente
2. **validação:** models validam antes de persistir
3. **auditoria:** django signals, updated_at, modified_by
4. **integridade:** orm respeita constraints e cascades

#### exemplo de uso correto

```python
class FatoReceitaRepository:
    
    @staticmethod
    def get_aggregated_by_month(year: int) -> List[Dict[str, Any]]:
        """
        Complex aggregation - use raw SQL for performance.
        READ-ONLY operation.
        """
        from app.utils.database import execute_query
        
        query = """
            SELECT 
                EXTRACT(MONTH FROM data) as month,
                SUM(valor_receita) as total
            FROM fato_receita
            WHERE EXTRACT(YEAR FROM data) = %s
            GROUP BY EXTRACT(MONTH FROM data)
            ORDER BY month
        """
        return execute_query(query, [year])
    
    @staticmethod
    def create(valor: float, data: date, projeto_id: int) -> FatoReceita:
        """
        Insert via ORM - NEVER use raw SQL.
        """
        from app.models import FatoReceita
        
        return FatoReceita.objects.create(
            valor_receita=valor,
            data=data,
            projeto_id=projeto_id
        )
```

### templates - organização

**regra de ouro:** todos os templates em `templates/` na raiz do projeto. subpastas por app: `templates/{app_name}/`

#### estrutura obrigatória

```
project/
├── templates/                    # pasta central
│   ├── base.html                # base template
│   ├── components/              # componentes compartilhados
│   │   ├── pagination.html
│   │   ├── navbar.html
│   │   └── footer.html
│   ├── authentication/          # templates de auth
│   │   ├── login.html
│   │   ├── register.html
│   │   └── password_reset.html
│   ├── dashboard/               # templates de dashboard
│   │   ├── analytics.html
│   │   ├── kpi_financeiro.html
│   │   └── dashboard.html
│   └── kpi/                     # templates de kpi
│       ├── upload_manager.html
│       └── upload.html
├── dashboard/
│   └── templates/               # ❌ não usar
├── kpi/
│   └── templates/               # ❌ não usar
└── authentication/
    └── templates/               # ❌ não usar
```

#### django settings

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # pasta central
        'APP_DIRS': False,  # desabilitar busca em apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

#### views

```python
# ✅ correto - caminho relativo à templates/
def analytics_view(request):
    return render(request, 'dashboard/analytics.html', context)

def upload_view(request):
    return render(request, 'kpi/upload_manager.html', context)

def login_view(request):
    return render(request, 'authentication/login.html', context)

# ❌ errado - caminho duplicado
def analytics_view(request):
    return render(request, 'dashboard/templates/dashboard/analytics.html', context)
```

#### template includes

```django
{# templates/base.html #}
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}KPI Dashboard{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'styles/main.css' %}">
</head>
<body>
    {% include 'components/navbar.html' %}
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    {% include 'components/footer.html' %}
</body>
</html>
```

```django
{# templates/dashboard/analytics.html #}
{% extends 'base.html' %}

{% block title %}Analytics - KPI Dashboard{% endblock %}

{% block content %}
    <div class="container">
        {% include 'components/breadcrumb.html' %}
        {% include 'dashboard/components/kpi_card.html' %}
    </div>
{% endblock %}
```

#### benefícios

1. **centralização:** todos os templates em um lugar
2. **organização:** estrutura clara por app
3. **manutenção:** fácil encontrar e editar
4. **reutilização:** componentes compartilhados
5. **performance:** busca mais rápida (sem APP_DIRS)

### management commands - organização

**regra de ouro:** commands específicos de app → `app/management/commands/`. commands globais do sistema → `core/management/commands/`

#### estrutura

```
project/
├── core/
│   └── management/
│       └── commands/
│           ├── run_scheduler.py      # run all background jobs
│           ├── health_check.py        # system health check
│           └── clear_cache.py        # clear all caches
├── app1/
│   └── management/
│       └── commands/
│           ├── populate_app1_data.py  # app-specific data
│           ├── validate_app1.py      # app-specific validation
│           └── import_app1.py        # app-specific import
└── app2/
    └── management/
        └── commands/
            └── process_app2.py         # app-specific processing
```

#### template: run_scheduler.py (core)

```python
"""
Management command to run all background schedulers.
Centralizes all background jobs from different apps.
"""
import time
import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Run all background schedulers (APScheduler jobs from all apps)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting all schedulers..."))

        schedulers_started = []

        # Import and start schedulers from each app
        try:
            from kpi import scheduler as kpi_scheduler
            kpi_scheduler.start()
            schedulers_started.append('kpi')
            self.stdout.write(self.style.SUCCESS("  [OK] KPI scheduler started"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  [WARN] KPI scheduler failed: {e}"))

        if not schedulers_started:
            self.stdout.write(self.style.ERROR("[ERROR] No schedulers started!"))
            return

        self.stdout.write(self.style.SUCCESS(
            f"\n[SUCCESS] {len(schedulers_started)} scheduler(s) running"
        ))

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n[STOP] Shutting down..."))
```

#### commands úteis (manter)

- **setup/inicialização:** `populate_{entity}_data.py`
- **validação/qa:** `validate_{entity}.py`
- **import/etl (dev/debug):** `test_import.py`
- **background jobs:** `run_scheduler.py` (core)

#### commands inúteis (remover)

- **duplicados:** múltiplos schedulers em apps diferentes
- **one-time scripts:** mover para `scripts/` e deletar após uso
- **development hacks:** usar pytest ou django test

#### violações comuns

```python
# ❌ errado - scheduler em app
kpi/management/commands/run_scheduler.py  # específico de app

# ✅ correto
core/management/commands/run_scheduler.py  # central, importa de todas apps
```

```python
# ❌ errado - lógica no command
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 200 linhas de lógica de negócio

# ✅ correto
class Command(BaseCommand):
    def handle(self, *args, **options):
        # apenas chamadas para controllers/services
        Controller.process_data()
```

---

## fastapi patterns

### estrutura

```
app/
├── __init__.py
├── main.py                 # entry point
├── core/
│   ├── config.py           # configurações
│   ├── database.py         # database setup
│   └── security.py         # auth, jwt, etc.
├── models/
│   └── user.py             # sqlalchemy models
├── schemas/
│   └── user.py             # pydantic models
├── repositories/
│   └── user_repository.py
├── controllers/
│   └── user_controller.py
├── routers/
│   └── user_router.py
└── services/
    └── email_service.py
```

### pydantic models

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema para criação de usuário.
    
    Pydantic valida automaticamente baseado nos tipos.
    """
    name: str = Field(..., min_length=2, max_length=100, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email válido")
    age: Optional[int] = Field(None, ge=0, le=150, description="Idade (0-150)")
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        """Validação customizada."""
        if not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v.strip().title()
    
    class Config:
        schema_extra = {
            "example": {
                "name": "João Silva",
                "email": "joao@example.com",
                "age": 30
            }
        }


class UserResponse(BaseModel):
    """Schema para resposta de usuário.
    
    Usa from_attributes para converter SQLAlchemy models automaticamente.
    """
    id: int
    name: str
    email: str
    age: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True  # antes era orm_mode
```

### validação customizada

```python
from pydantic import validator, root_validator

class UserUpdate(BaseModel):
    """Schema para atualização parcial."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    
    @root_validator
    def at_least_one_field(cls, values):
        """Garante que pelo menos um campo foi fornecido."""
        if not any(values.values()):
            raise ValueError('Pelo menos um campo deve ser fornecido')
        return values
```

### routers

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List, Optional
from app.controllers import UserController
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.core.security import get_current_user

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário",
    description="Cria um novo usuário no sistema"
)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Cria novo usuário.
    
    Endpoint autenticado que cria usuário seguindo o fluxo:
    1. Validação (automática via Pydantic)
    2. Criação via controller
    3. Retorno serializado
    """
    user = UserController.create_user(user_data.dict())
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Falha na criação do usuário"
        )
    
    return UserResponse.from_orm(user)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuários"
)
async def list_users(
    skip: int = Query(0, ge=0, description="Pular registros"),
    limit: int = Query(20, ge=1, le=100, description="Limite de registros"),
    search: Optional[str] = Query(None, description="Buscar por nome"),
    current_user: User = Depends(get_current_user)
) -> List[UserResponse]:
    """Lista usuários com paginação e busca.
    
    Query parameters são validados automaticamente pelo FastAPI.
    """
    users = UserController.list_users(
        skip=skip,
        limit=limit,
        search=search
    )
    
    return [UserResponse.from_orm(user) for user in users]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obter usuário"
)
async def get_user(
    user_id: int = Path(..., description="ID do usuário"),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Obtém usuário por ID."""
    user = UserController.get_user(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário {user_id} não encontrado"
        )
    
    return UserResponse.from_orm(user)
```

### dependency injection

```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.repositories import UserRepository


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Dependência para obter usuário atual.
    
    Valida token e retorna usuário.
    Se token inválido, lança HTTPException automaticamente.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token, credentials_exception)
    user = UserRepository.get_by_email(db, email=payload.get("sub"))
    
    if user is None:
        raise credentials_exception
    
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependência para verificar se usuário é admin.
    
    Reutiliza get_current_user e adiciona verificação de admin.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
```

### async/await

```python
# ✅ async para i/o (banco, apis, arquivos)
@router.get("/users")
async def list_users(db: Session = Depends(get_db)):
    users = await db.execute(select(User))
    return users.scalars().all()

# ✅ sync para processamento cpu-bound (mas pode bloquear)
@router.post("/process")
def process_data(data: Data):
    # processamento pesado
    result = heavy_computation(data)
    return result

# ✅ async para múltiplas operações i/o
@router.get("/user-with-posts")
async def get_user_with_posts(
    user_id: int,
    db: Session = Depends(get_db)
):
    # executa em paralelo
    import asyncio
    user, posts = await asyncio.gather(
        UserRepository.get_by_id(db, user_id),
        PostRepository.get_by_user(db, user_id)
    )
    return {"user": user, "posts": posts}
```

### error handling

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions import NotFoundError, ValidationError

app = FastAPI()


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    """Handler para recursos não encontrados."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    """Handler para erros de validação."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)}
    )


@app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação do Pydantic."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )
```

### database - sqlalchemy

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # verifica conexão antes de usar
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency para obter database session.
    
    Garante que session é fechada após request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### middleware

```python
import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log todas as requests com tempo de resposta."""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### testing

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    """Testa criação de usuário."""
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "João Silva",
            "email": "joao@example.com",
            "age": 30
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "joao@example.com"
    assert "id" in data
```

---

## testing - boas práticas python

### tdd - desenvolvimento orientado por testes

1. escrever teste primeiro
2. implementar código mínimo para passar
3. refatorar
4. repetir

### tipos de testes

**unit tests** - testar componentes isolados:

```python
# tests/test_validators.py
import pytest
from app.validators import UserValidator


def test_user_validator_valid_email():
    """Testa validação de email válido."""
    result = UserValidator.validate_email("user@example.com")
    assert result['valid'] is True
    assert result['error'] is None


def test_user_validator_invalid_email():
    """Testa validação de email inválido."""
    result = UserValidator.validate_email("invalid-email")
    assert result['valid'] is False
    assert 'email' in result['error'].lower()


@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("test.user@domain.co.uk", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
])
def test_user_validator_multiple_emails(email, expected):
    """Testa múltiplos casos de email."""
    result = UserValidator.validate_email(email)
    assert result['valid'] == expected
```

**integration tests** - testar fluxo completo:

```python
# tests/test_integration.py
import pytest
from django.test import TestCase
from app.controllers import UserController
from app.repositories import UserRepository


class UserIntegrationTest(TestCase):
    """Testa fluxo completo de criação de usuário."""
    
    def test_create_user_flow(self):
        """Testa fluxo completo: validar -> criar -> verificar."""
        # 1. dados de entrada
        user_data = {
            'name': 'João Silva',
            'email': 'joao@example.com',
            'age': 30
        }
        
        # 2. criar via controller
        user = UserController.create_user(user_data)
        
        # 3. verificar resultado
        assert user is not None
        assert user.email == 'joao@example.com'
        
        # 4. verificar no banco
        created = UserRepository.get_by_id(user.id)
        assert created is not None
        assert created.name == 'João Silva'
```

**api tests** - testar endpoints:

```python
# tests/test_api.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class UserAPITest(TestCase):
    """Testa endpoints da API de usuários."""
    
    def setUp(self):
        """Setup antes de cada teste."""
        self.client = APIClient()
        self.url = '/api/v1/users/'
    
    def test_create_user_success(self):
        """Testa criação de usuário via API."""
        data = {
            'name': 'João Silva',
            'email': 'joao@example.com',
            'age': 30
        }
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['email'] == 'joao@example.com'
```

### organização de testes

```
tests/
├── conftest.py              # fixtures compartilhadas
├── test_validators.py
├── test_repositories.py
├── test_controllers.py
├── test_services.py
├── test_api/
│   ├── test_user_api.py
│   └── test_auth_api.py
└── test_integration/
    └── test_user_flow.py
```

### fixtures compartilhadas

```python
# tests/conftest.py
import pytest
from app.models import User


@pytest.fixture
def sample_user_data():
    """Dados de exemplo para criar usuário."""
    return {
        'name': 'João Silva',
        'email': 'joao@example.com',
        'age': 30
    }


@pytest.fixture
def created_user(db, sample_user_data):
    """Cria usuário no banco de teste."""
    return User.objects.create(**sample_user_data)
```

### cobertura mínima - 80%

```bash
# instalar
pip install pytest-cov

# rodar com cobertura
pytest --cov=app --cov-report=html --cov-report=term

# ver relatório html
open htmlcov/index.html
```

**sempre testar:**
- validators (lógica de validação)
- controllers (orquestração)
- endpoints de api (request/response)
- funções complexas (cálculos, transformações)

**não precisa testar:**
- getters/setters simples
- métodos que apenas chamam outros métodos
- código de terceiros (bibliotecas)

### mocks e stubs

```python
from unittest.mock import patch, MagicMock

def test_send_email_with_mock():
    """Testa envio de email sem realmente enviar."""
    with patch('app.services.EmailService.send') as mock_send:
        mock_send.return_value = True
        
        result = UserController.create_user({
            'name': 'João',
            'email': 'joao@example.com'
        })
        
        # verifica que email foi "enviado" (mockado)
        mock_send.assert_called_once_with('joao@example.com')
        assert result is not None
```

### boas práticas

**nomes descritivos:**
```python
# ✅ bom
def test_user_validator_rejects_invalid_email_format():
    pass

# ❌ ruim
def test_email():
    pass
```

**arrange-act-assert:**
```python
def test_user_update():
    # arrange - preparar
    user = User.objects.create(name='João', email='joao@example.com')
    new_data = {'name': 'João Santos'}
    
    # act - executar
    updated = UserController.update_user(user.id, new_data)
    
    # assert - verificar
    assert updated.name == 'João Santos'
    assert updated.email == 'joao@example.com'  # não mudou
```

---

## imports e organização

### ordem de imports

```python
# 1. standard library
import os
import sys
from typing import List, Dict, Any

# 2. third-party
import django
from rest_framework import status
from fastapi import APIRouter

# 3. local
from app.models import User
from app.repositories import UserRepository
from app.controllers import UserController
```

### imports absolutos

```python
# ✅ correto
from app.repositories.user_repository import UserRepository
from app.controllers.user_controller import UserController

# ❌ errado - relativo
from ..repositories.user_repository import UserRepository
```

---

## tratamento de erros

### exceptions customizadas

```python
class ValidationError(Exception):
    """Raised when validation fails."""
    pass

class NotFoundError(Exception):
    """Raised when resource not found."""
    pass
```

### tratamento em controllers

```python
@staticmethod
def get_user(user_id: int) -> Optional[User]:
    """Get user by ID."""
    try:
        return UserRepository.get_by_id(user_id)
    except User.DoesNotExist:
        return None
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise
```

---

**estas regras são obrigatórias em todos os projetos python.**

