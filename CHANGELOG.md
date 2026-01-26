# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-01-26

### Changed
- **Reorganização completa de estudos:** Estrutura de estudos completamente reorganizada e consolidada
  - LeetCode consolidado em arquivo único (`config/studies/leetcode/README.md`)
  - Projetos consolidados em catálogo único (`config/studies/projetos/CATALOGO_PROJETOS.md`)
  - Knowledge Bases reorganizado com estrutura padrão de projeto (README.md, requisitos-tecnicos/, requisitos-processos/, arquitetura-diagramas/, consulta/)
  - Social focado apenas em YouTube (automações quando necessário)
  - Personal: Cards semanais consolidados em arquivo único (`config/personal/CARDS_SEMANAIS.md`)
- **Reorganização completa de scripts:** Scripts movidos de `scripts/` para `core/scripts/` organizados por temática (git, notion, projects, infrastructure, workflow)
- **Templates movidos:** Utils (database, base_repository, cache_system) movidos de `core/utils/` para `core/templates/` como snippets reutilizáveis
- **Documentação:** Criados README.md detalhados para cada categoria de scripts e templates
- **Referências atualizadas:** Todas as referências no projeto atualizadas para novos caminhos
- **Contexto geral:** Atualizado com regras de agendamento, timezone e horários detalhados
- **Agentes atualizados:** Referências a idiomas removidas (acompanhamento apenas via aplicativos)

### Removed
- **Pasta idiomas:** Removida `config/studies/idiomas/` (acompanhamento apenas via aplicativos)
- **Pasta notion-data:** Removida `config/studies/notion-data/` (dados ficam no MCP do Notion)
- **Pasta pesquisas:** Removida `config/studies/pesquisas/` (portfolio fica em `config/personal/portfolio/`)
- **Arquivos duplicados:** Removidos arquivos duplicados de leetcode (CONTEXTO_COMPLETO.md, ESTADO_ATUAL.md, rules.md)
- **Pasta templates personal:** Removida `config/personal/templates/` (conteúdo consolidado em CARDS_SEMANAIS.md)
- **Documentação privada:** Removido `docs/CLAUDE_CODE_TEMPLATES_INTEGRATION.md` (conteúdo privado não deve estar em repositório público)
- **Pastas antigas knowledge-bases:** Removidas pastas antigas (ia-ml-kb/, programming-kb/, data-science-kb/) reorganizadas em estrutura padrão

### Added
- **Estrutura padrão de projeto:** Aplicada estrutura padrão (README.md, requisitos-tecnicos/, requisitos-processos/, arquitetura-diagramas/, consulta/) para Knowledge Bases
- **Catálogo consolidado de projetos:** Criado `config/studies/projetos/CATALOGO_PROJETOS.md` consolidando todos os projetos (concluídos, em andamento, para fazer)
- **Cards semanais consolidados:** Criado `config/personal/CARDS_SEMANAIS.md` com todos os cards semanais detalhados
- **Subsídios Stuffscode:** Conteúdo do Stuffscode (pausado) movido para `config/studies/projetos/knowledge-bases/consulta/stuffscode-content/` como subsídios
- **Skills de organização:** Criadas skills `workflow/project-organization/SKILL.md` e `workflow/scripts-logs/SKILL.md` para organização de projetos e logs
- **CHANGELOG obrigatório:** Skill `workflow/changelog/SKILL.md` para gerenciamento obrigatório de CHANGELOG em todos os projetos
- **Templates de banco de dados e cache em `core/templates/`:**
  - `database/django-sql-snippets.py` - Funções genéricas para SQL puro (Django) com proteção contra SQL injection
  - `database/fastapi-repository-snippet.py` - Base repository genérico (FastAPI/SQLAlchemy) com métodos `_query_one`, `_query_list`, `_query_scalar`
  - `cache/redis-cache-snippet.py` - Sistema de cache Redis genérico (Django e standalone)
- **Documentação organizada:** README.md detalhados para `core/scripts/` e `core/templates/`
- **Diagram Generator reativado:** Sistema completo em `core/utils/diagram_generator/` para geração de diagramas ilustrativos usando OpenAI DALL-E ou Google Gemini
- **Postman Development:** Skill completa `documentation/postman/SKILL.md` com automação, CI/CD, templates e geração a partir de OpenAPI
- **Postman Execution:** Skill `documentation/postman-execution/SKILL.md` com comandos documentados para agentes executarem operações Postman
- **Makefile Postman:** Comandos `postman-generate`, `postman-test`, `postman-validate`, `postman-update` adicionados ao Makefile
- **Templates Postman:** Collection template, environment template, scripts Newman (`run_newman.sh` para executar testes) e script de conversão (`generate-from-openapi.sh` para converter OpenAPI → Postman), GitHub Actions workflow em `core/templates/postman-collection/`
- **Regras de CHANGELOG:** Adicionadas em `core/agents/programming.mdc` e `core/agents/general-context.mdc`

### Changed
- **.gitignore:** Simplificado usando pastas (`logs/`, `@temp/`) ao invés de listar arquivos individuais
- **skills/README.md:** Atualizado para referenciar templates em `core/templates/` ao invés de projetos de trabalho
- **skills/workflow/commit-workflow/SKILL.md:** Adicionado checklist obrigatório de CHANGELOG antes de commitar
- **skills/documentation/diagram-generation/SKILL.md:** Atualizada referência para `core/utils/diagram_generator/` (reativado e melhorado)
- **Reorganização de scripts:** Scripts movidos de `scripts/` para `core/scripts/` organizados por temática (git, notion, projects, infrastructure, workflow)
- **Templates reorganizados:** Utils movidos de `core/utils/` para `core/templates/` como snippets (database, cache)
- **Referências atualizadas:** Todas as referências no projeto atualizadas para novos caminhos

### Removed
- **Referências a projetos de trabalho:** Removidas referências diretas a `expenseiq` em `skills/README.md`
- **Documentação privada:** Removido `docs/CLAUDE_CODE_TEMPLATES_INTEGRATION.md` (conteúdo privado não deve estar em repositório público)

## [1.2.0] - 2025-12-08

### Added
- Initial public release of Cursor Multiagent System
- Core agent framework with 4 specialized agents:
  - Personal Assistant
  - Studies Coach
  - Work Coach
  - Social Media Assistant
- Notion integration via MCP
- Claude Code integration workflow
- Skills library organized by topic
- Configuration management with private submodule
- Auto-save context system
- Cleanup utilities for temporary files

### Security
- Private configuration stored in separate git submodule
- `.env.passwords` gitignored
- Sensitive data never committed to public repository

## [1.1.0] - 2025-11-XX

### Added
- Pilot phase implementation
- Notion workspace integration
- Task management automation
- Calendar and timebox management

## [1.0.0] - 2025-10-XX

### Added
- Initial project structure
- Basic agent definitions
- Core framework architecture

---

[Unreleased]: https://github.com/LucasBiason/cursor-multiagent-system/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/LucasBiason/cursor-multiagent-system/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/LucasBiason/cursor-multiagent-system/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/LucasBiason/cursor-multiagent-system/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/LucasBiason/cursor-multiagent-system/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/LucasBiason/cursor-multiagent-system/releases/tag/v1.0.0
