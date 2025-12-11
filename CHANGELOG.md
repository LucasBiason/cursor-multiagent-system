# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-01

### Added

#### Project Structure
- Created complete project structure
- Added core framework directories
- Set up configuration system
- Implemented .gitignore for privacy

#### Agents
- Personal Assistant agent (coordinator)
- Studies Coach agent (teaching specialist)
- Work Coach agent (development specialist)
- Social Media Coach agent (content specialist)

#### Documentation
- README.md with project overview
- ARCHITECTURE.md with system design
- GETTING_STARTED.md guide (redirects to README)
- CONTRIBUTING.md guidelines
- Rules consolidated in agents (notion-agent.mdc, general-context.mdc) and config/notion/

#### Configuration
- config.json for system settings
- Agent configuration files
- Private context separation
- Notion IDs management

#### Scripts
- setup.sh for initial setup
- validate.sh for configuration validation

#### Templates
- Agent template for creating new agents
- Configuration examples

### Security
- .gitignore configured to protect sensitive data
- Separation of public framework and private configs
- Environment variable support for secrets

## [1.1.0] - 2025-10-31

### Added
- Script de automação para commits e push (commit-and-push.sh)
- Proteção contra commit de tokens sensíveis
- Guia completo de segurança (SECURITY.md)
- Guia de versionamento (VERSIONING_GUIDE.md)

### Changed
- Removidos arquivos de sessão temporários (ACTIVATION_STATUS, INDICE_MESTRE, etc)
- Atualizada documentação principal (README, ARCHITECTURE, PROJECT_SUMMARY)
- Melhorada estrutura de guias (COMO_COMECAR, CONTRIBUTING)
- Atualizadas configurações de agentes e exemplos
- Todos os caminhos pessoais substituídos por placeholders genéricos

### Security
- Removidos todos os tokens Notion da documentação
- Removida pasta config/backups/ com IDs sensíveis do Notion
- Substituídos por placeholders seguros (ntn_YOUR_NOTION_TOKEN_HERE)
- Histórico git reescrito para remover tokens sensíveis
- Caminhos pessoais (/home/lucas-biason) substituídos por genéricos
- Script de commit aprimorado para detectar apenas adições de tokens
- .gitignore atualizado para proteger config/backups/

### Infrastructure
- Repositório configurado no GitHub: https://github.com/LucasBiason/cursor-multiagent-system
- Sistema de versionamento e controle configurado
- Push protection ativado para prevenir vazamento de secrets
- Verificação automática de segurança em cada commit

## [1.3.0] - 2025-12-10

### Added
- **Programming Documentation**: Complete programming best practices documentation
  - `core/docs/programming/BEST_PRACTICES.md` - Comprehensive programming guide
  - `core/docs/programming/CODE_MODIFICATION_RULES.md` - Rules for code modification
  - `core/docs/programming/CSS_RULES.md` - CSS file organization rules
  - `core/docs/programming/DJANGO_RULES.md` - Django-specific rules and patterns
  - `core/docs/programming/EMOJIS_RULES.md` - Explicit emoji usage rules
  - `core/docs/programming/TESTING_RULES.md` - Testing standards and practices
  - `core/docs/programming/GENERATIVE_AI_PROJECT_STRUCTURE.md` - Generative AI project structure guide
  - `core/docs/programming/` - Complete programming documentation structure
- **Django Templates**: Complete Django service templates
  - `core/templates/django/` - Full Django project template structure
  - `core/templates/django/DJANGO_SERVICE_TEMPLATE.md` - Django service template guide
  - `core/templates/django/Dockerfile.dev` and `Dockerfile.prod` - Docker templates
  - `core/templates/django/entrypoint.sh` - Entrypoint script template
  - `core/templates/django/pytest.ini` and `conftest.py` - Testing templates
  - `core/templates/django/.editorconfig` and `.flake8` - Code quality templates
  - `core/templates/django/pyproject.toml` - Python project configuration
  - `core/templates/django/configs/` - Configuration templates
- **Diagram Generator**: Complete diagram generation system
  - `scripts/diagram-generator/` - Full diagram generator implementation
  - `scripts/diagram-generator/prompt_engineering/` - Prompt engineering module
  - `scripts/diagram-generator/prompt_engineering/base.py` - Base prompt classes
  - `scripts/diagram-generator/prompt_engineering/chainer.py` - Prompt chaining
  - `scripts/diagram-generator/prompt_engineering/few_shot.py` - Few-shot examples
  - `scripts/diagram-generator/prompt_engineering/templates/` - Prompt templates
  - `scripts/diagram-generator/generators/` - Image generation clients
- **Agent Improvements**: Enhanced agent system
  - `core/agents/agent-behavior.mdc` - General agent behavior rules
  - `core/agents/cicd-agent.mdc` - CI/CD agent
  - `core/agents/general-context.mdc` - General context rules
  - `core/agents/notion-agent.mdc` - Notion integration agent
  - `core/agents/programming.mdc` - Programming rules (v3.0)
- **Scripts**: Enhanced utility scripts
  - `scripts/save_context.py` - Dynamic paths (no hardcoded paths)
  - `scripts/save-context.sh` - Dynamic paths implementation
  - `core/config/load_env_example.py` - Environment loading helper

### Changed
- **README.md**: Added emojis for better visual appeal and navigation
- **Scripts**: All scripts now use dynamic paths (no hardcoded `/home/lucas-biason`)
  - `scripts/save_context.py` - Uses `Path(__file__).resolve().parent`
  - `scripts/save-context.sh` - Uses `${BASH_SOURCE[0]}` for dynamic paths
  - `scripts/diagram-generator/config.py` - Dynamic output directory
- **Programming Rules**: Updated to version 3.0
  - Added emoji rules (explicit prohibition in code)
  - Added code modification rules (only change what's requested)
  - Enhanced testing rules (90% coverage per file, mocks required)
  - Added CSS rules (styles/, .min versions)
  - Added Django rules (static files, docs, error handlers)
- **Agents**: Updated with new rules
  - `work-assistant.mdc` - Updated with script/log management rules
  - `studies-assistant.mdc` - Updated with script/log management rules
  - `cicd-agent.mdc` - Updated with script/log management rules
  - `agent-behavior.mdc` - Added script/log organization rules

### Removed
- **Old Documentation**: Cleanup of outdated documentation
  - `COMO_CLONAR.md` - Content moved to README.md
  - `CONFIGURACAO_COMPLETA.md` - Content moved to README.md
  - `core/docs/rules/` - All individual rule files (consolidated)
  - `core/docs/workflows/youtube-production.md` - Moved to config
  - `docs/handbook/` - Old handbook files
  - `docs/archive/backups/` - Backup files
  - `production_plan.md` - Outdated planning document
- **Old Templates**: Cleanup of template files
  - `core/templates/GAMING_*.md` - Moved to config/gaming/
  - `core/templates/SISTEMA_*.md` - Moved to config/
  - `core/examples/task-manager/` - Removed outdated examples
- **Old Agent Files**: Removed old coach files (renamed to assistant)
  - `core/agents/social-media-coach.mdc`
  - `core/agents/studies-coach.mdc`
  - `core/agents/work-coach.mdc`

### Fixed
- **Dynamic Paths**: All scripts now work regardless of project location
- **Import Errors**: Fixed imports in prompt_engineering module
- **Documentation**: Consolidated and organized all programming documentation
- **Template Structure**: Standardized Django project templates

## [1.2.0] - 2025-12-08

### Added
- `core/config/.env.example` - Complete environment variables template
- `core/config/load_env_example.py` - Helper script for loading credentials
- `core/config/README.md` - Configuration files documentation
- `core/agents/programming.mdc` - Mandatory programming rules for all agents
- `core/agents/notion.mdc` - Mandatory Notion integration rules
- `config/gaming/GAMIFICATION_SYSTEM.md` - Consolidated gamification system documentation
- `config/cicd/projects/` - Project-specific deployment information (sensitive data)
- Logs directory structure (`logs/system/`, `logs/work/`, `logs/studies/`, etc.)

### Changed
- **Agent naming**: Renamed all agents from "Coach" to "Assistant"
  - `work-coach.mdc` → `work-assistant.mdc`
  - `studies-coach.mdc` → `studies-assistant.mdc`
  - `social-media-coach.mdc` → `social-media-assistant.mdc`
- **TECHNICAL_RULES.md** → `programming.mdc` (now mandatory for all code work)
- **Agent responsibilities**:
  - Personal Assistant: Now handles YouTube content management
  - Studies Assistant: Now handles StuffsCode (Instagram) and Knowledge Base project
  - Social Media Assistant: Currently inactive
- **Context organization**:
  - Sensitive information (IPs, servers, passwords, GitHub links) moved to `config/cicd/projects/{projeto}.md`
  - Non-sensitive deployment processes moved to `work-assistant.mdc`
  - `CONTEXTO_CICD.md` consolidated into `cicd/README.md`
- **README.md**: Integrated installation instructions from `COMO_CLONAR.md` and `CONFIGURACAO_COMPLETA.md`
- **`.cursorrules`**: Simplified to global rules and agent mapping only
- **Templates reorganization**: Moved gamification, Duolingo, and personal templates to appropriate `config/` subdirectories

### Removed
- `COMO_CLONAR.md` (content moved to README.md)
- `CONFIGURACAO_COMPLETA.md` (content moved to README.md)
- `core/agents/TECHNICAL_RULES.md` (replaced by `programming.mdc`)
- `core/agents/ATUALIZACAO_AGENTES_08DEZ.md` (no AI reports in git)
- Multiple gaming system files (consolidated into `GAMIFICATION_SYSTEM.md`)
- Templates moved from `core/templates/` to appropriate `config/` locations
- All `.bak` backup files (STATUS_MASTER, README_CONTEXTO, PROJETOS_DETALHADOS, INDICES_PRIORITARIOS, CONTEXTO_COMPLETO_ATUAL)
- `config/config.json` (duplicated `config.template.json`)
- `config/INSTRUCOES_SINCRONIZACAO.md` (consolidated into `config/README.md`)
- `config/RESUMO_REPOSITORIO.md` (consolidated into `config/README.md`)
- `config/REORGANIZACAO_CONTEXTO_08DEZ.md` (moved to CHANGELOG)

### Fixed
- Context duplication issues
- Sensitive information properly separated from non-sensitive rules
- File organization rules enforced
- Agent naming consistency
- **Major cleanup**: Removed all backup files and duplicates
- **Consolidation**: Merged synchronization and repository info into `config/README.md`
- **Minimal structure**: Reduced config root to essential files only

## [1.1.1] - 2025-11-12

### Changed
- Normalizados finais de arquivo em documentação, scripts e configurações para remover linhas em branco duplicadas e manter diffs limpos.

## [Unreleased]

### Planned
- Workflow engine implementation
- Background agent scheduler
- Metrics and analytics
- Additional integration examples
- Gmail integration
- Google Calendar sync

---

## Release Notes

### v1.0.0 - Pilot Phase

First release of the Cursor Multiagent Framework.

Focus on November 2024 pilot to validate:
- Agent coordination effectiveness
- Productivity improvements
- System stability
- Documentation completeness

Includes 4 core agents for:
- Personal organization
- Study guidance
- Work support
- Social media management

Framework ready for use and community contributions.

---

Last Updated: 2024-11-01



