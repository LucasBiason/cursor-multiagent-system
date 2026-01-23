# Skills Library

Sistema de skills organizadas por temática para uso com Cursor e Claude Code.

---

## Estrutura

```
skills/
├── workflow/           # Workflows de desenvolvimento
│   ├── cursor-handoff/
│   ├── commit-workflow/
│   ├── code-review/
│   ├── code-modification/
│   ├── test-runner/
│   ├── changelog/
│   ├── emojis/
│   ├── daily-standup/
│   ├── project-organization/  # Organização de projetos (config vs logs)
│   └── scripts-logs/          # Organização de scripts temporários e logs
├── backend/            # Backend frameworks
│   ├── fastapi/
│   ├── django/
│   ├── python/
│   └── nodejs/
├── frontend/           # Frontend frameworks
│   ├── react/
│   └── css/
├── infrastructure/     # Docker, Makefile, execução, deploy
│   ├── docker-compose/
│   ├── docker-execution/
│   ├── docker-entrypoint/
│   ├── dockerfile-generator/
│   ├── makefile/
│   └── deployment/
├── documentation/      # Documentação
│   ├── diagram-generation/
│   ├── postman/
│   └── postman-execution/
└── integration/        # Integrações externas
    └── notion/
```

---

## Formato de Skill

Cada skill segue o formato `SKILL.md`:

```markdown
---
name: skill-name
description: Quando usar esta skill
triggers: [palavras, que, ativam]
---

# Nome da Skill

## Quando Usar
- Cenário 1
- Cenário 2

## Princípios Core
[Conteúdo principal]

## Checklist
- [ ] Item 1
- [ ] Item 2
```

---

## Skills Disponíveis

### Workflow
| Skill | Descrição |
|-------|-----------|
| `cursor-handoff` | Transição Cursor ↔ Claude Code |
| `commit-workflow` | Fluxo de commits (sem co-author IA, com CHANGELOG obrigatório) |
| `changelog` | Gerenciamento obrigatório de CHANGELOG em todos os projetos |
| `code-review` | Code review patterns |
| `code-modification` | ⚠️ CRÍTICO: Regras sobre quando e como modificar código |
| `test-runner` | Execução de testes (cobertura mínima 90%, meta 100%) |
| `emojis` | Regras sobre uso de emojis em código e documentação |
| `daily-standup` | Análise completa usando Notion MCP |
| `project-organization` | ⚠️ CRÍTICO: Organização de projetos (config vs logs) - quando usar cada pasta |
| `scripts-logs` | ⚠️ CRÍTICO: Organização de scripts temporários, logs, feedbacks e planejamentos |

### Backend
| Skill | Descrição |
|-------|-----------|
| `fastapi` | FastAPI best practices (produção real) |
| `django` | Django patterns (cookiecutter-django) |
| `python` | Python best practices (type hints, styleguide) |
| `nodejs` | Node.js best practices (Express, NestJS) |

### Frontend
| Skill | Descrição |
|-------|-----------|
| `react` | React best practices (Next.js, Vite) |
| `css` | Organização, minificação e carregamento de CSS |

### Infrastructure
| Skill | Descrição |
|-------|-----------|
| `docker-compose` | Segurança: NUNCA expor variáveis sensíveis |
| `docker-execution` | Agentes DEVEM executar containers, não apenas mostrar |
| `docker-entrypoint` | Padrão para entrypoint.sh com múltiplos comandos |
| `dockerfile-generator` | Geração automática de Dockerfiles, entrypoints, Makefiles seguindo melhores práticas |
| `makefile` | Padrões e boas práticas para Makefile |
| `deployment` | Processos gerais de deploy, validação, backup e boas práticas para produção |

### Documentation
| Skill | Descrição |
|-------|-----------|
| `diagram-generation` | Diagramas ilustrativos (OpenAI/Gemini) |
| `postman` | Desenvolvimento e documentação de APIs (JWT, automação, CI/CD) |
| `postman-execution` | Comandos e automação Postman (conversão, testes, validação) |

### Integration
| Skill | Descrição |
|-------|-----------|
| `notion` | Integração completa com Notion usando MCP customizado (notion-automation-suite) |

---

## Regras Gerais Aplicáveis a Todas as Skills

### Múltiplas Classes

**Quando um módulo tem mais de uma classe, cada classe deve estar em um arquivo separado:**

```
# ❌ ERRADO
models.py:
  - User
  - Role
  - Permission

# ✅ CORRETO
models/
  ├── __init__.py      # Exporta todas
  ├── user.py          # class User
  ├── role.py          # class Role
  └── permission.py    # class Permission
```

### Sem Indícios de IA

**NUNCA adicionar co-author de IA ou qualquer indício de uso de IA no código de produção.**

### Migrations

**TODO E QUALQUER AGENTE ESTÁ PROIBIDO DE MEXER EM MIGRATIONS JÁ APLICADAS (Django ou Alembic).**

---

## Como Usar

### No Cursor
Referência em `.cursorrules` ou agentes `.mdc`:
```markdown
## Skills
- Seguir: `skills/backend/fastapi/SKILL.md`
```

### No Claude Code
Skills são lidas automaticamente via `CLAUDE.md`.

### Ativação
Skills são ativadas por:
1. Referência explícita
2. Triggers no contexto
3. Tipo de arquivo sendo editado

---

## Referências de Código

### SQL Puro
- **Django:** `core/templates/database/django-sql-snippets.py` - Funções genéricas para queries SQL puro com proteção contra SQL injection
- **FastAPI:** `core/templates/database/fastapi-repository-snippet.py` - Base repository com métodos `_query_one`, `_query_list`, `_query_scalar` usando parameter binding

### Cache System
- **Redis:** `core/templates/cache/redis-cache-snippet.py` - Sistema de cache genérico com Redis, suporta Django e standalone

**Usar quando:**
- Queries muito grandes e complexas (SQL puro)
- Consultas repetitivas que não mudam frequentemente (Cache)
