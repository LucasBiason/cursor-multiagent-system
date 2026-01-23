# FastAPI Template com Framework

**Template de código FastAPI usando a biblioteca padrão `fastapi-microservice-framework`.**

---

## 📁 Estrutura

```
fastapi-project/
├── alembic/          # Migrations
├── src/              # Código fonte (com framework.py)
├── tests/            # Testes
├── requirements/     # Dependências (inclui framework)
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── alembic.ini
```

---

## 🚀 Como Usar

```bash
# Copiar template
cp -r core/templates/fastapi-project/with-framework my-project
cd my-project

# Configurar .env
cp .env.example .env

# Instalar e executar
make install
make db-up
make migrate
make up
```

---

## 📖 Documentação

**Para instruções completas, consulte:**
- **FastAPI Skill:** `skills/backend/fastapi/SKILL.md`
- **Framework Library:** `core/templates/fastapi-project/FRAMEWORK_LIBRARY.md`
- **Template Principal:** `core/templates/fastapi-project/README.md`

---

**Última Atualização:** 2026-01-22
