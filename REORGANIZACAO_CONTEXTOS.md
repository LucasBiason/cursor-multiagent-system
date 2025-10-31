# Plano de Reorganizacao de Contextos

**Data:** 01/11/2025  
**Status:** Em execucao  
**Objetivo:** Consolidar TUDO de Contextos de IA no novo sistema multiagente

---

## ANALISE DO CONTEUDO ATUAL

### Localizacao: `/home/lucas-biason/Projetos/Contextos de IA`

**Estrutura encontrada:**
- 00-Geral/ - 70+ arquivos
- 01-Estudos/ - 50+ arquivos
- 02-Trabalho/ - 100+ arquivos
- 03-Pessoal/ - Vazio
- 04-Canal/ - 35+ arquivos
- 05-Sistema/ - 1 arquivo

**Total:** ~250+ arquivos de contexto!

---

## ESTRATEGIA DE MIGRACAO

### PUBLICO (Framework) → core/

Migrar:
- Templates genericos
- Regras reutilizaveis
- Arquitetura de sistemas
- Exemplos didaticos
- Guias de uso

### PRIVADO (Configs) → config/private/

Migrar:
- IDs do Notion (ja feito)
- Contextos especificos
- Dados pessoais
- Informacoes de trabalho
- Detalhes de projetos

### AGENTES → config/agents/

Consolidar por agente:
- Personal Assistant: Regras gerais + agenda
- Studies Coach: Contexto FIAP + projetos
- Work Coach: ExpenseIQ + cliente
- Social Media Coach: YouTube + Instagram

---

## MAPEAMENTO DE MIGRACAO

### 00-Geral/ → Destinos

| Origem | Destino | Tipo |
|--------|---------|------|
| Regras/*.md | core/docs/rules/ | Publico |
| Templates/*.md | core/templates/ | Publico |
| Configuracoes/BASES_NOTION_CONTEXTO.md | config/private/notion-schema.md | Privado |
| Configuracoes/HORARIOS_PESSOAIS_CORRETOS.md | config/private/schedule.md | Privado |
| PROMPT_RECONSTRUCAO_COMPLETO.md | config/private/personal-assistant-full.md | Privado |
| GUIA_COMPLETO_SISTEMA_NOTION.md | core/docs/notion-integration.md | Publico |
| Manual_Notion/*.md | core/docs/notion/ | Publico |

### 01-Estudos/ → Destinos

| Origem | Destino | Tipo |
|--------|---------|------|
| PROMPT_COACH_ESTUDOS_IA.md | config/agents/studies-coach-extended.md | Privado |
| FIAP_CONTEXTO.md | config/private/studies/fiap-context.md | Privado |
| CONTEXTO_PROJETO.md | config/private/studies/projects-context.md | Privado |
| Cronogramas/*.md | config/private/studies/schedules/ | Privado |
| IA Knowledge Base Plan/*.md | config/private/studies/ia-kb-plan/ | Privado |

### 02-Trabalho/ → Destinos

| Origem | Destino | Tipo |
|--------|---------|------|
| ExpenseIQ/*.md | config/private/work/expenseiq/ | Privado |
| HubTravel/*.md | config/private/work/archive/hubtravel/ | Privado |
| Infraestrutura/*.md | config/private/work/infrastructure/ | Privado |

### 04-Canal/ → Destinos

| Origem | Destino | Tipo |
|--------|---------|------|
| LOGICA_PRODUCAO_YOUTUBE.md | core/docs/workflows/youtube-production.md | Publico |
| PROJETO_STUFFSCODE_COMPLETO.md | config/private/social/stuffscode.md | Privado |
| StuffsCode/*.md | config/private/social/stuffscode/ | Privado |

### 05-Sistema/ → Destinos

| Origem | Destino | Tipo |
|--------|---------|------|
| CONTEXTO_GERAL.md | config/private/system-context.md | Privado |

---

## NOVA ESTRUTURA ORGANIZADA

```
cursor-multiagent-system/
│
├── core/                           # PUBLICO (Framework)
│   ├── docs/
│   │   ├── GETTING_STARTED.md
│   │   ├── ARCHITECTURE.md
│   │   ├── RULES_SYSTEM.md
│   │   ├── notion-integration.md       ← NOVO (do Guia Completo)
│   │   ├── rules/
│   │   │   ├── timezone.md             ← Consolidado
│   │   │   ├── status-management.md    ← Consolidado
│   │   │   └── task-verification.md    ← Consolidado
│   │   ├── workflows/
│   │   │   ├── youtube-production.md   ← Do Canal
│   │   │   ├── study-scheduling.md     ← Novo
│   │   │   └── weekly-planning.md      ← Novo
│   │   └── notion/
│   │       ├── databases.md            ← Do Manual
│   │       ├── properties.md           ← Do Manual
│   │       └── best-practices.md       ← Do Manual
│   │
│   ├── templates/
│   │   ├── agent-template.mdc
│   │   ├── weekly-cards-template.md    ← Dos Templates
│   │   └── lesson-review-template.md   ← Dos Templates
│   │
│   └── examples/
│       ├── task-manager/
│       ├── notion-integration/         ← Novo exemplo
│       └── youtube-automation/         ← Novo exemplo
│
├── config/                         # PRIVADO (Suas configs)
│   ├── agents/
│   │   ├── personal-assistant.mdc      ✅ Criado
│   │   ├── studies-coach.mdc           ✅ Criado
│   │   ├── work-coach.mdc              ✅ Criado
│   │   └── social-media-coach.mdc      ✅ Criado
│   │
│   ├── private/
│   │   ├── notion-ids.json             ✅ Criado
│   │   ├── user-context.md             ✅ Criado
│   │   ├── system-context.md           ← Migrar de 05-Sistema
│   │   │
│   │   ├── studies/
│   │   │   ├── fiap-context.md         ← Migrar FIAP_CONTEXTO
│   │   │   ├── projects-active.md      ← Projetos ativos
│   │   │   ├── projects-completed.md   ← Projetos concluidos
│   │   │   ├── schedules/              ← Todos cronogramas
│   │   │   └── ia-kb-plan/             ← IA Knowledge Base Plan
│   │   │
│   │   ├── work/
│   │   │   ├── expenseiq/              ← Todo contexto ExpenseIQ
│   │   │   ├── client-astracode.md     ← Info do cliente
│   │   │   └── archive/
│   │   │       └── hubtravel/          ← HubTravel (cancelado)
│   │   │
│   │   ├── social/
│   │   │   ├── youtube-series.md       ← Series ativas
│   │   │   ├── production-schedule.md  ← Calendario producao
│   │   │   └── stuffscode/             ← Projeto Instagram
│   │   │
│   │   ├── personal/
│   │   │   ├── medical.md              ← Tratamento medico
│   │   │   ├── finance.md              ← Detalhes financeiros
│   │   │   └── recurring-tasks.md      ← Cards recorrentes
│   │   │
│   │   └── gaming/
│   │       ├── gamification-system.md  ← Sistema gaming
│   │       └── duolingo-tracking.md    ← Duolingo
│   │
│   ├── workflows/
│   │   ├── morning-routine.yml
│   │   ├── weekly-planning.yml
│   │   ├── recording-sprint.yml
│   │   └── study-session.yml
│   │
│   └── backups/
│       ├── sessions/                   ← Resumos de sessoes
│       └── historical/                 ← Documentos historicos
│
└── docs/                           # Documentacao do projeto
    ├── pilot/
    │   ├── daily-logs/                 ← Logs diarios novembro
    │   └── metrics/                    ← Metricas do piloto
    └── archive/                        ← Docs obsoletos
```

---

## ACAO IMEDIATA

Vou criar essa estrutura e migrar TUDO de forma organizada!

### Fase 1: Estrutura (Fazendo agora)
- Criar diretorios organizados
- Migrar regras publicas
- Consolidar contextos privados

### Fase 2: Consolidacao (Proxima)
- Unificar documentos similares
- Remover duplicacoes
- Criar indices mestres

### Fase 3: Limpeza (Depois)
- Arquivar obsoletos
- Organizar historicos
- README em cada pasta

---

Iniciando migracao agora...

