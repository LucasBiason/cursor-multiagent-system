# Django Service Template

**Template de código para copiar e colar ao criar novos serviços Django.**

---

## 📁 Arquivos Disponíveis

- `Dockerfile` - Dockerfile multi-stage
- `entrypoint.sh` - Entrypoint flexível (dev, test, prod, migrate)
- `Makefile` - Comandos úteis
- `pyproject.toml` - Configuração Poetry
- `pytest.ini` - Configuração pytest
- `conftest.py` - Fixtures pytest
- `.dockerignore` - Arquivos ignorados no Docker
- `.editorconfig` - Configuração editor
- `.flake8` - Configuração flake8
- `configs/` - Templates de configuração (docker-compose, nginx, .env)

---

## 🚀 Como Usar

```bash
# Copiar template
cp -r core/templates/django my-django-service
cd my-django-service

# Personalizar arquivos conforme necessário
```

---

## 📖 Documentação

**Para instruções completas sobre como criar um serviço Django, consulte:**
- **Django Skill:** `skills/backend/django/SKILL.md`

**Para detalhes sobre arquivos específicos:**
- **Dockerfile:** `skills/infrastructure/dockerfile-generator/SKILL.md`
- **Entrypoint:** `skills/infrastructure/docker-entrypoint/SKILL.md`
- **Makefile:** `skills/infrastructure/makefile/SKILL.md`
- **Testes:** `skills/workflow/test-runner/SKILL.md`

---

**Última Atualização:** 2026-01-22
