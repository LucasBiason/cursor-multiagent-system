# Template Completo de Serviço Django

**Última Atualização:** 2025-12-08

**Baseado em:** User Service do ExpenseIQ

---

## estrutura completa

```
service-name/
├── app/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   ├── handlers.py
│   │   ├── schemas.py
│   │   ├── test_settings.py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   └── swagger.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── cache_system.py
│   │   │   └── database.py
│   │   └── serializers/
│   │       ├── __init__.py
│   │       └── health.py
│   ├── [domain]/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── [model].py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── [repository].py
│   │   ├── validators/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   └── [validator].py
│   │   ├── controllers/
│   │   │   ├── __init__.py
│   │   │   └── [controller].py
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   └── [serializer].py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── schemas/
│   │   │   └── [view].py
│   │   ├── urls.py
│   │   └── migrations/
│   ├── manage.py
│   ├── conftest.py
│   └── pytest.ini
├── tests/
│   ├── __init__.py
│   ├── src/
│   │   ├── __init__.py
│   │   ├── test_handlers.py
│   │   ├── test_health.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── test_cache_system.py
│   └── [domain]/
│       ├── __init__.py
│       ├── models/
│       │   └── test_[model].py
│       ├── repositories/
│       │   └── test_[repository].py
│       ├── validators/
│       │   └── test_[validator].py
│       ├── controllers/
│       │   └── test_[controller].py
│       └── views/
│           └── test_[view].py
├── configs/
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── nginx.conf
│   ├── .env.development
│   ├── .env.production
│   └── .env.database
├── Dockerfile.dev
├── Dockerfile.prod
├── entrypoint.sh
├── requirements.txt
├── .editorconfig
├── .flake8
├── .gitignore
└── pyproject.toml
```

---

## arquivos obrigatórios

### src/settings.py
- configurações Django
- database, redis, cors
- rest framework
- swagger
- logging

### src/urls.py
- swagger, redoc, admin
- health check
- static files (DEBUG)
- rotas do domínio

### src/handlers.py
- exception handler customizado
- formato JSON padronizado
- logging completo

### src/views/health.py
- endpoint de health check
- retorna service, version, dt

### src/utils/cache_system.py
- usar template do ExpenseIQ
- operações com Redis

### src/utils/database.py
- usar template do ExpenseIQ
- consultas SQL puro

---

## domínio

**estrutura por domínio (ex: users, products, etc.):**

1. **models/** - modelos Django
2. **repositories/** - acesso ao ORM
3. **validators/** - validação de entrada
4. **controllers/** - lógica de negócio
5. **serializers/** - serializers DRF
6. **views/** - views da API
7. **urls.py** - rotas do domínio

---

## testes

**estrutura espelhada:**
- `app/[domain]/controllers/[controller].py`
- `tests/[domain]/controllers/test_[controller].py`

**coverage:** mínimo 90% por arquivo

---

## referências

- base: User Service do ExpenseIQ
- templates: `core/templates/django/`
- regras: `core/docs/programming/DJANGO_RULES.md`

---

**este template deve ser seguido para todos os serviços Django.**


