# quick start - criar api do zero

**última atualização:** 2025-12-08  
**aplicável a:** todos os agentes criando apis (django, fastapi)

---

## objetivo

**este guia mostra passo a passo como criar uma api completa seguindo a estrutura padrão.**

quando o usuário pedir uma api, os agentes devem seguir esta estrutura exata.

---

## estrutura completa de uma api

### django rest framework

```
app_name/
├── models/
│   └── resource.py              # model django
├── repositories/
│   └── resource_repository.py  # acesso ao orm
├── validators/
│   └── resource_validator.py   # validação de entrada
├── controllers/
│   └── resource_controller.py  # lógica de negócio
├── api/
│   ├── __init__.py
│   ├── urls.py                  # rotas da api
│   ├── views.py                 # views da api
│   ├── serializers.py           # serializers drf
│   └── validators.py            # validators de api
├── views.py                      # views de template (se necessário)
└── urls.py                       # urls principais (templates + api)
```

### fastapi

```
app/
├── models/
│   └── resource.py              # model sqlalchemy
├── repositories/
│   └── resource_repository.py  # acesso ao orm
├── validators/
│   └── resource_validator.py   # validação de entrada
├── controllers/
│   └── resource_controller.py  # lógica de negócio
├── schemas/
│   ├── request.py               # pydantic request models
│   └── response.py              # pydantic response models
└── routers/
    └── resource_router.py       # rotas da api
```

---

## passo a passo: criar api django

### 1. model

```python
# app/models/resource.py
from django.db import models
from typing import Optional


class Resource(models.Model):
    """Resource model."""
    
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    status = models.CharField(
        max_length=50,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active',
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return self.name
```

### 2. repository

```python
# app/repositories/resource_repository.py
from typing import List, Optional
from django.db.models import QuerySet
from app.models import Resource


class ResourceRepository:
    """Repository para manipulação de Resource."""
    
    @staticmethod
    def get_by_id(resource_id: int) -> Optional[Resource]:
        """Buscar por ID."""
        try:
            return Resource.objects.get(id=resource_id)
        except Resource.DoesNotExist:
            return None
    
    @staticmethod
    def get_all() -> QuerySet[Resource]:
        """Buscar todos os registros."""
        return Resource.objects.all()
    
    @staticmethod
    def filter_by_status(status: str) -> QuerySet[Resource]:
        """Filtrar por status."""
        return Resource.objects.filter(status=status)
    
    @staticmethod
    def create(data: dict) -> Resource:
        """Criar novo registro."""
        return Resource.objects.create(**data)
    
    @staticmethod
    def update(resource_id: int, data: dict) -> Optional[Resource]:
        """Atualizar registro existente."""
        instance = ResourceRepository.get_by_id(resource_id)
        if not instance:
            return None
        
        for key, value in data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance
    
    @staticmethod
    def delete(resource_id: int) -> bool:
        """Deletar registro."""
        instance = ResourceRepository.get_by_id(resource_id)
        if not instance:
            return False
        
        instance.delete()
        return True
```

### 3. validator

```python
# app/validators/resource_validator.py
from typing import Dict, Any


class ResourceValidator:
    """Validates resource data."""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data for creating resource.
        
        Returns:
            dict: {'valid': bool, 'error': str|None, 'data': dict}
        """
        errors = []
        
        # Check required fields
        if not data.get('name'):
            errors.append('Name is required')
        
        if data.get('name') and len(data['name']) > 255:
            errors.append('Name must be 255 characters or less')
        
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
                'name': data['name'],
                'description': data.get('description', ''),
                'status': data.get('status', 'active')
            }
        }
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for updating resource."""
        errors = []
        
        if 'name' in data and len(data['name']) > 255:
            errors.append('Name must be 255 characters or less')
        
        if 'status' in data and data['status'] not in ['active', 'inactive']:
            errors.append('Status must be active or inactive')
        
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

### 4. controller

```python
# app/controllers/resource_controller.py
from typing import Optional, List
from django.db.models import QuerySet
from app.models import Resource
from app.repositories import ResourceRepository
from app.validators import ResourceValidator


class ResourceController:
    """Controller para gerenciar resources."""
    
    @staticmethod
    def create_resource(data: dict) -> Optional[Resource]:
        """
        Create new resource.
        
        Args:
            data: Resource data
            
        Returns:
            Resource criado ou None se validação falhar
        """
        # 1. Validate
        validation = ResourceValidator.validate_create(data)
        if not validation['valid']:
            return None
        
        # 2. Create
        resource = ResourceRepository.create(validation['data'])
        return resource
    
    @staticmethod
    def update_resource(resource_id: int, data: dict) -> Optional[Resource]:
        """
        Update existing resource.
        
        Args:
            resource_id: ID do resource
            data: Dados para atualizar
            
        Returns:
            Resource atualizado ou None se não encontrado
        """
        # 1. Validate
        validation = ResourceValidator.validate_update(data)
        if not validation['valid']:
            return None
        
        # 2. Update
        resource = ResourceRepository.update(resource_id, validation['data'])
        return resource
    
    @staticmethod
    def get_resource(resource_id: int) -> Optional[Resource]:
        """Get resource by ID."""
        return ResourceRepository.get_by_id(resource_id)
    
    @staticmethod
    def list_resources(filters: dict = None) -> QuerySet[Resource]:
        """List all resources."""
        if filters and filters.get('status'):
            return ResourceRepository.filter_by_status(filters['status'])
        return ResourceRepository.get_all()
    
    @staticmethod
    def delete_resource(resource_id: int) -> bool:
        """Delete resource."""
        return ResourceRepository.delete(resource_id)
```

### 5. serializer

```python
# app/api/serializers.py
from rest_framework import serializers
from app.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    """Serializer for Resource."""
    
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### 6. api view

```python
# app/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.controllers import ResourceController
from app.api.serializers import ResourceSerializer


class ResourceListAPIView(APIView):
    """
    API endpoint for listing and creating resources.
    GET /api/v1/resources/ - List resources
    POST /api/v1/resources/ - Create resource
    """
    
    def get(self, request):
        """List all resources."""
        filters = request.GET.dict()
        resources = ResourceController.list_resources(filters)
        
        serializer = ResourceSerializer(resources, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Create new resource."""
        resource = ResourceController.create_resource(request.data)
        
        if not resource:
            return Response(
                {'error': 'Validation failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ResourceSerializer(resource, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResourceDetailAPIView(APIView):
    """
    API endpoint for retrieving, updating and deleting resources.
    GET /api/v1/resources/{id}/ - Get resource
    PUT /api/v1/resources/{id}/ - Update resource
    DELETE /api/v1/resources/{id}/ - Delete resource
    """
    
    def get(self, request, resource_id: int):
        """Get resource by ID."""
        resource = ResourceController.get_resource(resource_id)
        
        if not resource:
            return Response(
                {'error': 'Resource not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ResourceSerializer(resource, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, resource_id: int):
        """Update resource."""
        resource = ResourceController.update_resource(resource_id, request.data)
        
        if not resource:
            return Response(
                {'error': 'Resource not found or validation failed'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ResourceSerializer(resource, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, resource_id: int):
        """Delete resource."""
        deleted = ResourceController.delete_resource(resource_id)
        
        if not deleted:
            return Response(
                {'error': 'Resource not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### 7. api urls

```python
# app/api/urls.py
from django.urls import path
from app.api.views import (
    ResourceListAPIView,
    ResourceDetailAPIView,
)

urlpatterns = [
    path('resources/', ResourceListAPIView.as_view(), name='api_resources_list'),
    path('resources/<int:resource_id>/', ResourceDetailAPIView.as_view(), name='api_resources_detail'),
]
```

### 8. app urls (com versionamento)

```python
# app/urls.py
from django.urls import path, include

urlpatterns = [
    # Template views (sem /api/)
    path('', DashboardView.as_view(), name='dashboard'),
    
    # API routes (com versionamento obrigatório)
    path('api/v1/', include('app.api.urls')),
]
```

### 9. config urls

```python
# config/urls.py
from django.urls import path, include

urlpatterns = [
    path('app/', include('app.urls')),
]
```

**resultado final:**
- templates: `/app/`
- api: `/app/api/v1/resources/`

---

## passo a passo: criar api fastapi

### 1. model

```python
# app/models/resource.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Resource(Base):
    """Resource model."""
    
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default='active', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

### 2. repository

```python
# app/repositories/resource_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.resource import Resource


class ResourceRepository:
    """Repository para manipulação de Resource."""
    
    @staticmethod
    def get_by_id(db: Session, resource_id: int) -> Optional[Resource]:
        """Buscar por ID."""
        return db.query(Resource).filter(Resource.id == resource_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Resource]:
        """Buscar todos os registros."""
        return db.query(Resource).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, data: dict) -> Resource:
        """Criar novo registro."""
        resource = Resource(**data)
        db.add(resource)
        db.commit()
        db.refresh(resource)
        return resource
    
    @staticmethod
    def update(db: Session, resource_id: int, data: dict) -> Optional[Resource]:
        """Atualizar registro existente."""
        resource = ResourceRepository.get_by_id(db, resource_id)
        if not resource:
            return None
        
        for key, value in data.items():
            setattr(resource, key, value)
        
        db.commit()
        db.refresh(resource)
        return resource
    
    @staticmethod
    def delete(db: Session, resource_id: int) -> bool:
        """Deletar registro."""
        resource = ResourceRepository.get_by_id(db, resource_id)
        if not resource:
            return False
        
        db.delete(resource)
        db.commit()
        return True
```

### 3. validator

```python
# app/validators/resource_validator.py
from typing import Dict, Any


class ResourceValidator:
    """Validates resource data."""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating resource."""
        errors = []
        
        if not data.get('name'):
            errors.append('Name is required')
        
        if data.get('name') and len(data['name']) > 255:
            errors.append('Name must be 255 characters or less')
        
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
                'name': data['name'],
                'description': data.get('description', ''),
                'status': data.get('status', 'active')
            }
        }
```

### 4. controller

```python
# app/controllers/resource_controller.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.resource import Resource
from app.repositories import ResourceRepository
from app.validators import ResourceValidator


class ResourceController:
    """Controller para gerenciar resources."""
    
    @staticmethod
    def create_resource(db: Session, data: dict) -> Optional[Resource]:
        """Create new resource."""
        validation = ResourceValidator.validate_create(data)
        if not validation['valid']:
            return None
        
        return ResourceRepository.create(db, validation['data'])
    
    @staticmethod
    def get_resource(db: Session, resource_id: int) -> Optional[Resource]:
        """Get resource by ID."""
        return ResourceRepository.get_by_id(db, resource_id)
    
    @staticmethod
    def list_resources(db: Session, skip: int = 0, limit: int = 100) -> List[Resource]:
        """List all resources."""
        return ResourceRepository.get_all(db, skip=skip, limit=limit)
```

### 5. schemas (pydantic)

```python
# app/schemas/request.py
from pydantic import BaseModel, Field
from typing import Optional


class ResourceCreate(BaseModel):
    """Request model for creating resource."""
    name: str = Field(..., max_length=255, description="Resource name")
    description: Optional[str] = Field(None, description="Resource description")
    status: Optional[str] = Field('active', description="Resource status")


class ResourceUpdate(BaseModel):
    """Request model for updating resource."""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
```

```python
# app/schemas/response.py
from pydantic import BaseModel
from datetime import datetime


class ResourceResponse(BaseModel):
    """Response model for resource."""
    id: int
    name: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### 6. router

```python
# app/routers/resource_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.controllers import ResourceController
from app.schemas.request import ResourceCreate, ResourceUpdate
from app.schemas.response import ResourceResponse
from app.core.database import get_db

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])


@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db)
) -> ResourceResponse:
    """Create new resource."""
    resource = ResourceController.create_resource(db, resource_data.dict())
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation failed"
        )
    
    return ResourceResponse.from_orm(resource)


@router.get("/", response_model=List[ResourceResponse])
async def list_resources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[ResourceResponse]:
    """List all resources."""
    resources = ResourceController.list_resources(db, skip=skip, limit=limit)
    return [ResourceResponse.from_orm(r) for r in resources]


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_db)
) -> ResourceResponse:
    """Get resource by ID."""
    resource = ResourceController.get_resource(db, resource_id)
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    return ResourceResponse.from_orm(resource)
```

### 7. main app

```python
# app/main.py
from fastapi import FastAPI
from app.routers import resource_router

app = FastAPI(title="My API", version="1.0.0")

app.include_router(resource_router.router)
```

---

## checklist: criar api completa

### estrutura
- [ ] model criado em `models/`
- [ ] repository criado em `repositories/`
- [ ] validator criado em `validators/`
- [ ] controller criado em `controllers/`
- [ ] serializer/schema criado
- [ ] api view/router criado
- [ ] urls configuradas com versionamento (`/api/v1/`)

### código
- [ ] repository usa apenas orm (sem lógica)
- [ ] validator valida entrada (sem acesso a banco)
- [ ] controller orquestra (chama validator, repository)
- [ ] api view/router apenas serializa e define status
- [ ] type hints em todas as funções
- [ ] docstrings em padrão google

### padrões
- [ ] versionamento obrigatório (`/api/v1/`)
- [ ] resource-oriented urls
- [ ] status codes apropriados
- [ ] paginação em list endpoints
- [ ] error handling adequado

---

## referências

- architecture completa → `architecture.md`
- api rest → `api-rest.md`
- python → `python.md`
- typescript → `typescript.md`

---

**siga esta estrutura exata ao criar qualquer api. não criar arquivos aleatórios ou fora do padrão.**


