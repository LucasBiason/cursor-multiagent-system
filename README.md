# Cursor Multiagent System

Framework para coordenação de agentes IA no Cursor IDE.

## O que é

Sistema modular que permite criar e gerenciar múltiplos agentes especializados trabalhando juntos. Cada agente tem um domínio específico (trabalho, estudos, pessoal) e compartilham contexto entre si.

## Por que usar

- Manter contexto entre sessões de trabalho
- Separar responsabilidades por domínio
- Integrar com Notion para gestão de tarefas
- Workflow padronizado entre Cursor e Claude Code

## Estrutura

```
cursor-multiagent-system/
├── .claude/              # Integração com Claude Code CLI
│   ├── CLAUDE.md         # Instruções globais
│   └── commands/         # Comandos customizados
│
├── core/
│   ├── agents/           # Definições dos agentes (.mdc)
│   └── templates/        # Templates de projeto
│
├── skills/               # Biblioteca de skills reutilizáveis
│   ├── workflow/         # Handoff, commits, review, test-runner
│   ├── backend/          # FastAPI, Django, Python, Node.js
│   ├── frontend/         # React, Next.js, Vite
│   ├── infrastructure/   # Docker, Makefile, execução
│   └── documentation/    # Diagramas, docs técnicos
│
├── core/
│   ├── scripts/          # Scripts organizados por temática
│   └── templates/        # Templates e snippets reutilizáveis
│   ├── cleanup_temp.py   # Limpeza de temporários
│   ├── notion_batch.py   # Operações batch no Notion
│   └── ...
│
├── @temp/                # Arquivos temporários (gitignored)
├── logs/                 # Logs de sessão (gitignored)
└── config/               # Configuração privada (submodule)
```

## Workflow: Cursor + Claude Code

| Ferramenta | Responsabilidade |
|------------|------------------|
| Cursor | Escrita de código, refatoração |
| Claude Code | Review, testes, commits |
| Você | Aprovação, requisitos |

Fluxo básico:
```
Cursor (implementa) → Claude Code (revisa) → Você (aprova) → Commit
```

Comandos de handoff:
```bash
claude "review as alterações e rode os testes"
claude "prepare o commit"
```

## Instalação

```bash
git clone https://github.com/LucasBiason/cursor-multiagent-system.git
cd cursor-multiagent-system

# Inicializar submodule privado (requer acesso)
git submodule update --init --recursive

# Instalar dependências
pip install -r requirements.txt

# Configurar
make setup
```

O diretório `config/` é um submodule privado. Sem acesso, o sistema funciona mas sem as configurações pessoais.

## Agentes

O sistema tem 4 agentes principais:

**Personal Assistant** - Ponto de entrada. Gerencia agenda, tarefas, coordena outros agentes.

**Studies Assistant** - Suporte para aprendizado e projetos de estudo.

**Work Assistant** - Desenvolvimento profissional. Code review, deploy, git workflow.

**Social Media Assistant** - Gestão de conteúdo técnico.

Cada agente:
- Acessa Notion para criar/atualizar cards
- Respeita timeboxes e agenda
- Compartilha contexto com outros agentes

## Uso básico

Falar naturalmente com o Cursor:
```
"mostra minha agenda de hoje"
"ajuda com esse projeto"
"cria uma tarefa pra amanhã"
```

Ou chamar agente específico:
```
@personal-assistant criar tarefa
@work-assistant revisar esse código
```

## Scripts disponíveis

Scripts organizados por categoria. **SEMPRE usar Makefile quando disponível.**

Ver `core/scripts/README.md` para documentação completa de cada script.

**Principais categorias:**
- **Git:** `commit-and-push.sh`, `git_multi.py`
- **Notion:** `notion_batch.py` (priorizar MCP quando possível)
- **Projetos:** `project_status.py`, `daily_standup.py`
- **Limpeza:** `cleanup_temp.py`
- **Validação:** `validate.sh`

## Configuração

### Variáveis de ambiente

```bash
# Notion (opcional)
export NOTION_API_KEY="secret_xxx"
```

### Notion

Se usar integração com Notion, configurar IDs em:
Database IDs estão no projeto do MCP (`my-local-place/services/external/notion-automation-suite/config/.env` - gitignored)

### Cursor IDE

Os agentes ficam em `core/agents/`. O Cursor carrega automaticamente arquivos `.mdc`.

## Criar novo agente

1. Copiar template:
```bash
cp core/templates/agent-template.mdc core/agents/meu-agente.mdc
```

2. Editar o arquivo com as responsabilidades do agente

3. Testar no Cursor

## Troubleshooting

**Submodule vazio após clone**
```bash
git submodule update --init --recursive
```

**Agente não ativa**
- Verificar se arquivo existe em `core/agents/`
- Verificar sintaxe do arquivo `.mdc`
- Reiniciar Cursor

**Erro no Notion**
- Verificar `NOTION_API_KEY`
- Verificar IDs das databases

## Privacidade

Dados sensíveis ficam em `config/` (submodule privado, nunca commitado no repo público).

O repo público contém apenas:
- Templates genéricos
- Documentação
- Scripts utilitários

## Contribuindo

1. Fork o repositório
2. Criar branch para feature
3. Testar alterações
4. Abrir PR

## Licença

MIT
