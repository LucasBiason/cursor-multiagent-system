# Templates

**Templates de código e configuração para copiar e colar ao criar novos projetos ou configurar o sistema.**

---

## 📁 Templates Disponíveis

### Configuração
- **`config.template.json`** - Template de configuração do sistema multiagent
  - Estrutura de agents, Notion, environment, logging
  - Copiar para `config/` e personalizar conforme necessário

### Agent
- **`agent-template.mdc`** - Template para criar novos agents

### Django
- **`django/`** - Template completo de serviço Django

### FastAPI
- **`fastapi-project/`** - Templates de projeto FastAPI (basic e with-framework)

### Entrypoint Scripts
- **`entrypoint/`** - Templates de entrypoint.sh para diferentes stacks

### Snippets
- **`cache/`** - Snippets de cache Redis
- **`database/`** - Snippets de banco de dados (SQL puro)

### Postman
- **`postman-collection/`** - Templates de coleção Postman

---

## 🚀 Como Usar

```bash
# Copiar template de configuração
cp core/templates/config.template.json config/config.json

# Copiar template de agent
cp core/templates/agent-template.mdc core/agents/my-agent.mdc

# Copiar template Django
cp -r core/templates/django my-django-service

# Copiar template FastAPI
cp -r core/templates/fastapi-project/basic my-fastapi-service
```

---

## 📖 Documentação

**Para instruções completas sobre como usar cada template, consulte as skills:**
- **Django:** `skills/backend/django/SKILL.md`
- **FastAPI:** `skills/backend/fastapi/SKILL.md`
- **Configuração:** `config/README.md`

---

**Última Atualização:** 2026-01-22
