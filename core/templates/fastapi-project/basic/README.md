# FastAPI Basic Template

**Template de código FastAPI do zero com esqueleto básico.**

---

## 📁 Estrutura

```
fastapi-project/
├── alembic/          # Migrations
├── src/              # Código fonte
├── tests/            # Testes
├── requirements/     # Dependências
├── scripts/          # Scripts utilitários
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── alembic.ini
```

---

## 🚀 Como Usar

```bash
# Copiar template
cp -r core/templates/fastapi-project/basic my-project
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
- **Template Principal:** `core/templates/fastapi-project/README.md`

---

**Última Atualização:** 2026-01-22
