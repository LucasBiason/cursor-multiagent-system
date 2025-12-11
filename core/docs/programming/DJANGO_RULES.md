# Regras Específicas para Django

**Última Atualização:** 2025-12-08

---

## estrutura obrigatória

**seguir estrutura do User Service do ExpenseIQ:**

```
app/
├── src/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── handlers.py
│   ├── views/
│   │   ├── health.py
│   │   └── swagger.py
│   ├── utils/
│   │   ├── cache_system.py
│   │   └── database.py
│   └── serializers/
│       └── health.py
├── [domain]/
│   ├── models/
│   ├── repositories/
│   ├── validators/
│   ├── controllers/
│   ├── serializers/
│   ├── views/
│   └── urls.py
└── manage.py
```

---

## static files

**desenvolvimento:**
- adicionar em `urls.py` principal:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**produção:**
- usar `collectstatic`:
```bash
python manage.py collectstatic
```
- servir via nginx (Django não serve estáticos em produção)

---

## documentação (swagger/redoc)

**sempre incluir em `urls.py`:**

```python
from .views import schema_view

urlpatterns = [
    # DOC URLs
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # ...
]
```

**configurar em `views/swagger.py`:**

```python
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

API_TITLE = "Service Name"
API_VERSION = os.getenv("SYSTEM_VERSION", "1.0.0")
API_DESCRIPTION = "Service Description"

schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version=API_VERSION,
        description=API_DESCRIPTION,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
```

---

## admin

**sempre incluir admin em `urls.py`:**

```python
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    # ...
]
```

---

## error handlers

**sempre usar handler customizado:**

**em `settings.py`:**
```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'src.handlers.exception_handler',
    # ...
}
```

**template em `src/handlers.py`:**
- usar template do ExpenseIQ User Service
- retornar JSON padronizado
- não retornar HTML de erro 500

---

## health check

**sempre implementar endpoint de health check:**

**em `src/views/health.py`:**
```python
from django.utils.timezone import now
from rest_framework import views
from rest_framework.response import Response
import os

SERVICE_NAME = "Service Name"
DEFAULT_VERSION = "1.0.0"

class HealthView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        return Response({
            "service": SERVICE_NAME,
            "version": os.getenv("SYSTEM_VERSION", DEFAULT_VERSION) or DEFAULT_VERSION,
            "dt": now(),
        })
```

**em `urls.py`:**
```python
from .views import health_view

urlpatterns = [
    path("", health_view, name="health-root"),
    path("health", health_view, name="health"),
    path("health/", health_view, name="health-slash"),
    # ...
]
```

---

## arquivos padronizados

**sempre usar estes arquivos como base:**

1. **cache_system.py:**
   - `/home/lucas-biason/Projetos/Trabalho/Astracode/expenseiq/user-service/app/src/utils/cache_system.py`
   - usar para todas as operações de cache com Redis

2. **database.py:**
   - `/home/lucas-biason/Projetos/Trabalho/Astracode/expenseiq/user-service/app/src/utils/database.py`
   - usar para consultas SQL puro (não usar biblioteca de conexão diretamente)

3. **handlers.py:**
   - `/home/lucas-biason/Projetos/Trabalho/Astracode/expenseiq/user-service/app/src/handlers.py`
   - usar como template para error handlers

---

## migrations

**nunca modificar migrations manualmente:**
- sempre usar `makemigrations`
- Django gerencia migrations automaticamente
- não criar ou editar migrations manualmente

---

---

## regras críticas de organização de código

### uma view por arquivo (obrigatório)

**regra crítica:** cada view deve estar em seu próprio arquivo. nunca colocar múltiplas views no mesmo arquivo.

**estrutura obrigatória:**
```
app/
├── views/
│   ├── __init__.py           # Exporta todas as views
│   ├── list_view.py          # ListView
│   ├── create_view.py        # CreateView
│   ├── retrieve_view.py      # RetrieveView
│   ├── update_view.py        # UpdateView
│   └── delete_view.py        # DeleteView
```

**exemplo:**
```python
# ❌ errado - múltiplas views no mesmo arquivo
# views.py
class UserListView(APIView):
    pass

class UserCreateView(APIView):
    pass

# ✅ correto - uma view por arquivo
# views/list_view.py
class UserListView(APIView):
    pass

# views/create_view.py
class UserCreateView(APIView):
    pass
```

**exceção:** apenas views combinadas para roteamento (list_create_view, retrieve_update_delete_view) podem ter múltiplos métodos HTTP (GET, POST, PUT, DELETE) no mesmo arquivo, mas devem delegar para views individuais.

---

### um serializer por arquivo (obrigatório)

**regra crítica:** cada serializer deve estar em seu próprio arquivo dentro do módulo `serializers/`.

**estrutura obrigatória:**
```
app/
├── serializers/
│   ├── __init__.py              # Exporta todos os serializers
│   ├── user_serializer.py       # UserSerializer
│   ├── user_create_serializer.py    # UserCreateSerializer
│   ├── user_update_serializer.py    # UserUpdateSerializer
│   └── user_list_serializer.py      # UserListSerializer
```

**exemplo:**
```python
# ❌ errado - múltiplos serializers no mesmo arquivo
# serializers.py
class UserSerializer(serializers.ModelSerializer):
    pass

class UserCreateSerializer(serializers.Serializer):
    pass

# ✅ correto - um serializer por arquivo
# serializers/user_serializer.py
class UserSerializer(serializers.ModelSerializer):
    pass

# serializers/user_create_serializer.py
class UserCreateSerializer(serializers.Serializer):
    pass
```

---

### organização por domínio (obrigatório)

**regra crítica:** cada domínio (entidade) deve ter sua própria app django. nunca colocar múltiplos domínios na mesma app.

**domínios comuns que devem ter apps próprias:**
- `users/` - gerenciamento de usuários
- `company/` - empresas/organizações
- `contracts/` ou `contratos/` - contratos
- `log/` - logs de ações/auditoria
- `upload/` - uploads de arquivos
- `notifications/` - notificações

**exemplo:**
```python
# ❌ errado - múltiplos domínios na mesma app
# kpi/models.py
class Company(models.Model):
    pass

class User(models.Model):
    pass

class ActionLog(models.Model):
    pass

# ✅ correto - cada domínio em sua app
# company/models/company.py
class Company(models.Model):
    pass

# users/models/user.py
class User(models.Model):
    pass

# log/models/action_log.py
class ActionLog(models.Model):
    pass
```

---

### registros duplicados no admin (proibido)

**regra crítica:** nunca registrar o mesmo modelo no admin em múltiplos arquivos. cada modelo deve ser registrado apenas uma vez, na app onde está definido.

**exemplo:**
```python
# ❌ errado - modelo registrado em dois lugares
# kpi/admin.py
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

# company/admin.py
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

# ✅ correto - modelo registrado apenas onde está definido
# company/admin.py (Company está em company/models/)
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

# kpi/admin.py - não registra Company, apenas modelos de kpi/
```

---

### foreignkeys devem referenciar apps corretas (obrigatório)

**regra crítica:** quando um modelo é movido para uma nova app, todas as foreignkeys que referenciam esse modelo devem ser atualizadas.

**estrutura:**
```python
# ❌ errado - foreignkey com referência antiga
# kpi/models/unit.py (após Company ter sido movido para company/)
company = models.ForeignKey("kpi.Company", on_delete=models.CASCADE)

# ✅ correto - foreignkey atualizada
# kpi/models/unit.py
company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
```

**checklist após mover modelo:**
1. atualizar todas as foreignkeys que referenciam o modelo
2. atualizar imports em todo o projeto
3. atualizar registros no admin
4. verificar migrations (se necessário)

---

### controllers não acessam orm diretamente (obrigatório)

**regra crítica:** controllers nunca devem acessar orm diretamente. sempre usar repositories.

**exemplo:**
```python
# ❌ errado - orm direto no controller
class UserController:
    @staticmethod
    def get_user(user_id):
        return User.objects.get(id=user_id)  # ERRADO

# ✅ correto - usa repository
class UserController:
    @staticmethod
    def get_user(user_id):
        return UserRepository.get_by_id(user_id)  # CORRETO
```

---

### processors não acessam dados diretamente (obrigatório)

**regra crítica:** processors (processamento de dados) nunca devem acessar banco diretamente. sempre usar repositories.

**exemplo:**
```python
# ❌ errado - acesso direto no processor
def process_excel(file_path):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM ...")  # ERRADO
    model.objects.create(...)  # ERRADO

# ✅ correto - delega para repository
def process_excel(file_path):
    data = extract_data(file_path)
    CompanyRepository.create(data)  # CORRETO
    UnitRepository.create(data)  # CORRETO
```

---

### urls rest api (obrigatório)

**regra crítica:** urls de api devem seguir padrão rest api:
- usar plural nouns (`contracts`, não `contract`)
- usar inglês
- não usar prefixos desnecessários (`cadastros/`, `api/`)
- seguir padrão: `/{app}/api/v1/{resource}/`

**estrutura:**
```python
# ❌ errado
path('cadastros/contratos/', ...)  # português, prefixo desnecessário
path('api/uploads/', ...)  # sem versionamento

# ✅ correto
path('contracts/', ...)  # inglês, plural
path('uploads/', ...)  # inglês, plural
# incluído em: path("kpi/api/v1/", include("app.urls"))
```

---

## referências

- estrutura completa: User Service do ExpenseIQ
- templates: `core/templates/django/`
- regras gerais: `core/agents/programming.mdc`
- arquitetura: `core/docs/programming/architecture.md`

---

**estas regras são obrigatórias para todos os projetos Django. violações podem quebrar o sistema e atrasar projetos significativamente.**


