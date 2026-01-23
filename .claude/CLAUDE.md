# Cursor Multiagent System - Claude Code Integration

## Contexto do Projeto

Este é um framework de automação de desenvolvimento que integra **Cursor IDE** e **Claude Code** para maximizar produtividade. O objetivo é automatizar o máximo possível do ciclo de desenvolvimento, deixando para o humano apenas: revisão de código, aprovação de commits e testes manuais exploratórios.

## Divisão de Responsabilidades

### CURSOR (Escrita)
- Implementação de código novo
- Refatoração complexa
- Debug interativo
- Geração de documentação inicial

### CLAUDE CODE (Revisão)
- Code review (qualidade, padrões, segurança)
- Execução de testes automatizados
- Preparação de commits (COM PERMISSÃO)
- Preparação de PRs (COM PERMISSÃO)
- Validação de qualidade antes de merge

### VOCÊ (Aprovação)
- Definir requisitos
- Aprovar commits/PRs
- Revisar sugestões
- Testes manuais exploratórios

---

## Regras Críticas

### Git - OBRIGATÓRIO
- **NUNCA** fazer commit sem permissão explícita
- **NUNCA** fazer push sem permissão explícita
- **SEMPRE** mostrar preview do commit antes
- **SEMPRE** seguir conventional commits
- **SEMPRE** perguntar antes de ações destrutivas

### Arquivos - PROIBIDO CRIAR
- Arquivos na raiz de qualquer projeto
- Arquivos `RESUMO_*`, `RELATORIO_*`, `ANALISE_*` fora de `@temp/` ou `logs/`
- Scripts `.py` ou `.sh` fora de `scripts/` ou `@temp/`
- Documentação `.md` fora de `docs/` ou `config/`
- Qualquer arquivo para "guardar contexto" ou "me responder"

### Arquivos - ONDE CRIAR
| Tipo | Local Correto |
|------|---------------|
| Script temporário | `@temp/[frente]/[projeto]/` |
| Análise/relatório | `logs/[dominio]/YYYY-MM-DD_[subject].md` |
| Spec de projeto | `config/[area]/[projeto]/` |
| Documentação pública | `docs/` |
| Código do projeto | Dentro do projeto específico |

---

## Estrutura do Projeto

```
cursor-multiagent-system/
├── .claude/              # Configuração Claude Code
├── .cursor/              # Configuração Cursor
├── core/                 # Framework (agentes, docs, templates)
├── skills/               # Skills por temática
├── docs/                 # Documentação pública
├── scripts/              # Scripts permanentes
├── @temp/                # Temporários (GITIGNORED)
├── logs/                 # Logs (GITIGNORED)
└── config/               # Privado (SUBMODULE)
```

---

## Skills Disponíveis

### Backend
- `backend/fastapi/` - FastAPI best practices
- `backend/django/` - Django patterns
- `backend/python/` - Python geral

### Frontend
- `frontend/typescript/` - TypeScript patterns
- `frontend/react/` - React best practices

### Infrastructure
- `infrastructure/docker/` - Docker e Compose
- `infrastructure/cicd/` - CI/CD patterns

### Code Quality
- `code-quality/testing/` - Testing patterns
- `code-quality/review/` - Code review

### Engineering
- `engineering/git/` - Git workflow
- `engineering/architecture/` - Architecture patterns

### Workflow
- `workflow/cursor-handoff/` - Transição Cursor ↔ Claude Code
- `workflow/commit/` - Fluxo de commits

---

## Comandos Úteis

### Testes
```bash
pytest                    # Python
npm test                  # Node.js
```

### Lint/Format
```bash
ruff check . && ruff format .   # Python
eslint . && prettier --write .  # JavaScript/TypeScript
```

### Git
```bash
git status
git diff
git log --oneline -10
```

---

## Timezone

**SEMPRE GMT-3 (São Paulo)**

Formato: `2026-01-19T19:00:00-03:00`

---

## Handoff Cursor → Claude Code

Após o Cursor implementar algo, use:
```bash
claude "review as alterações e rode os testes"
claude "prepare o commit das alterações"
```

## Handoff Claude Code → Cursor

Quando encontrar issues:
```
Issues encontrados:
1. [descrição do problema] em [arquivo:linha]

Cursor: corrija X no arquivo Y
```
