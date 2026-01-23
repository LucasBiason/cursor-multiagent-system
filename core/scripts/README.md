# Scripts do Cursor Multiagent System

**Scripts organizados por temática para facilitar localização e manutenção.**

---

## 📁 Estrutura Organizada

```
core/scripts/
├── git/                    # Scripts relacionados ao Git
│   └── git_multi.py        # Gerenciamento de múltiplos repositórios
│
├── notion/                  # Scripts relacionados ao Notion
│   └── notion_batch.py     # Operações em lote no Notion
│
├── projects/                # Scripts de gerenciamento de projetos
│   ├── project_status.py   # Status consolidado de projetos
│   └── daily_standup.py    # Preparação de standup/planning
│
├── infrastructure/          # Scripts de infraestrutura e setup
│   ├── ssh_utils.py        # Conexão SSH genérica
│   ├── validate.sh         # Validação de configuração e segurança
│   ├── setup.sh            # Setup inicial do projeto
│   └── load_env_example.py # Exemplo de carregamento de variáveis de ambiente
│
└── workflow/                # Scripts de workflow e automação
    ├── commit-and-push.sh  # Commit e push com validação
    ├── save-context.sh     # Salvar contexto automaticamente
    ├── cleanup_temp.py    # Limpeza de arquivos temporários
    ├── postman-generate.sh # Gerar collection Postman a partir de OpenAPI
    ├── postman-test.sh     # Executar testes Postman com Newman
    ├── postman-validate.sh # Validar estrutura da collection Postman
    └── postman-update.sh   # Atualizar collection Postman a partir de OpenAPI
```

---

## 🎯 Categorias

### Git (`git/`)

Scripts para gerenciamento de repositórios Git.

#### `git_multi.py`
**Gerenciamento de múltiplos repositórios Git simultaneamente.**

**Uso:**
```bash
python core/scripts/git/git_multi.py --status          # Status de todos os repos
python core/scripts/git/git_multi.py --fetch           # Fetch em todos
python core/scripts/git/git_multi.py --pull            # Pull em todos
python core/scripts/git/git_multi.py --stale-branches  # Branches antigas
python core/scripts/git/git_multi.py --uncommitted      # Repos com mudanças
```

**Funcionalidades:**
- Verificar status de todos os projetos de uma vez
- Fazer fetch/pull em batch
- Identificar branches antigas/esquecidas (>30 dias)
- Encontrar repositórios com mudanças não commitadas

**Escaneia:** `~/Projetos/Projetos/Ativos` e `~/Projetos/Infraestrutura` por padrão.

---

### Notion (`notion/`)

Scripts para integração com Notion.

#### `notion_batch.py`
**⚠️ PRIORIDADE: SEMPRE usar Notion MCP primeiro!**

Este script só deve ser usado quando:
- MCP não suporta a operação necessária
- Operações em lote muito grandes
- Scripts de automação específicos

**PRIORIDADE:** `@notion-automation-suite` (MCP) é sempre preferível.

**Uso (quando necessário):**
```bash
python core/scripts/notion/notion_batch.py --action list --database studies
python core/scripts/notion/notion_batch.py --action update-status --database studies --status "Concluído"
python core/scripts/notion/notion_batch.py --action archive --database personal --older-than 90
python core/scripts/notion/notion_batch.py --action stats --database all
```

---

### Projects (`projects/`)

Scripts para gerenciamento e análise de projetos.

#### `project_status.py`
**Status consolidado de todos os projetos ativos.**

Gera relatório de status de projetos rastreados, incluindo:
- Status do Git (branch, alterações não commitadas, commits não pushados)
- Métricas (arquivos Python, Markdown, testes)
- Deadlines e urgência
- Status de testes e documentação

**Uso:**
```bash
python core/scripts/projects/project_status.py                     # Print para stdout
python core/scripts/projects/project_status.py --output status.md  # Salvar em arquivo
python core/scripts/projects/project_status.py --json              # Output JSON
python core/scripts/projects/project_status.py --project hackathon # Projeto específico
```

**Configuração:** Projetos são carregados de `config/system/tracked-projects.json` (privado).

#### `daily_standup.py`
**⚠️ DEPRECADO:** Este script está sendo refatorado para uma skill/rule que usa Notion MCP.

**Nova abordagem:** Quando usuário pedir "daily", o agente deve:
1. Solicitar de qual frente (trabalho, estudos ou geral)
2. Analisar logs, temporários e contexto da conversa
3. Usar Notion MCP para buscar tarefas:
   - Atrasadas (data final < hoje e status != concluído)
   - Em andamento (pelo status)
   - Não iniciadas com atraso (data inicial < hoje e não está em andamento)
4. Fornecer review completo com proposta de cronograma e prioridades

**Tudo deve estar no Notion para melhor gerenciamento.**

Ver skill: `skills/workflow/daily-standup/SKILL.md`

---

### Infrastructure (`infrastructure/`)

Scripts de infraestrutura, validação e setup.

#### `load_env_example.py`
**Exemplo de como carregar variáveis de ambiente em scripts Python.**

**Features:**
- Verifica múltiplas localizações para `.env.passwords`
- Funções helper para credenciais comuns (deployment servers, Render, Notion, GitHub, FIAP)
- Tratamento de erros e resolução de caminhos adequada

**Uso:**
```python
from core.scripts.infrastructure.load_env_example import (
    load_env_passwords,
    get_deployment_credentials,
    get_render_credentials,
    get_notion_credentials
)

# Carregar ambiente
load_env_passwords()

# Obter credenciais
expenseiq = get_deployment_credentials("expenseiq")
render = get_render_credentials()
notion = get_notion_credentials()
```

**Localizações verificadas (em ordem):**
1. `config/.env.passwords` (preferido - subrepositório privado)
2. `.env.passwords` na raiz do projeto
3. `.env.passwords` no diretório atual

**Referência:** `config/README.md` para detalhes completos sobre variáveis de ambiente.

#### `ssh_utils.py`
**Conexão SSH genérica para projetos remotos.**

**Uso:**
```python
from core.scripts.infrastructure.ssh_utils import SSHConnection

with SSHConnection(project="myproject") as ssh:
    status, stdout, stderr = ssh.execute_command("docker ps")
    print(stdout)
```

**Carrega credenciais de variáveis de ambiente:**
- `DEPLOYMENT_MYPROJECT_SSH_HOST`
- `DEPLOYMENT_MYPROJECT_SSH_USER`
- `DEPLOYMENT_MYPROJECT_PASSWORD`

#### `validate.sh`
**Validação de configuração e segurança.**

**Uso:**
```bash
make validate
# ou
./core/scripts/infrastructure/validate.sh
```

**Verifica:**
- Arquivos obrigatórios
- Configuração privada
- Variáveis de ambiente
- Dados sensíveis em arquivos públicos
- Docker Compose (variáveis expostas)
- Sintaxe JSON

#### `setup.sh`
**Setup inicial do projeto.**

**Uso:**
```bash
make setup
# ou
./core/scripts/infrastructure/setup.sh
```

---

### Workflow (`workflow/`)

Scripts de workflow e automação.

#### `commit-and-push.sh`
**Commit e push com validação de segurança.**

**Uso:**
```bash
./core/scripts/workflow/commit-and-push.sh "feat: nova funcionalidade"
```

**Validações:**
- Detecta tokens Notion, GitHub, IPs, senhas conhecidas
- Bloqueia commit se encontrar dados sensíveis

#### `save-context.sh`
**Salvar contexto automaticamente após cada interação.**

**Uso:** Executado automaticamente pelo sistema.

#### `cleanup_temp.py`
**⚠️ EM REFATORAÇÃO:** Este script será atualizado para:
1. **Logs diários:** Ao final do dia, agentes elaboram relatório de tudo que foi pedido, falado, respondido e feito
2. **Logs mensais:** Após fechamento do mês, consolidar logs diários em arquivo único
3. **Retenção:** Manter contexto por 6 meses, depois remover
4. **Análise de scripts temporários:** Identificar scripts recorrentes que podem virar comandos, skills ou scripts genéricos

**Uso atual:**
```bash
python core/scripts/workflow/cleanup_temp.py           # Dry run
python core/scripts/workflow/cleanup_temp.py --execute # Executa limpeza
```

#### `postman-generate.sh`
**Gerar collection Postman a partir de OpenAPI/Swagger.**

**Uso:**
```bash
make postman-generate
# ou
./core/scripts/workflow/postman-generate.sh openapi.json postman
```

**Funcionalidades:**
- Busca automaticamente arquivo OpenAPI em locais comuns
- Instala `openapi-to-postmanv2` se necessário
- Gera collection Postman completa

#### `postman-test.sh`
**Executar testes Postman com Newman.**

**Uso:**
```bash
make postman-test
# ou
./core/scripts/workflow/postman-test.sh postman/collection.json postman/environment.json
```

**Funcionalidades:**
- Executa todos os requests da collection
- Gera relatórios (CLI, JUnit XML, HTML)
- Retorna código de saída apropriado

#### `postman-validate.sh`
**Validar estrutura da collection Postman.**

**Uso:**
```bash
make postman-validate
# ou
./core/scripts/workflow/postman-validate.sh postman/collection.json
```

**Funcionalidades:**
- Valida JSON válido
- Verifica campos obrigatórios (info, item)
- Conta número de requests

#### `postman-update.sh`
**Atualizar collection Postman a partir de OpenAPI.**

**Uso:**
```bash
make postman-update
# ou
./core/scripts/workflow/postman-update.sh openapi.json
```

**Funcionalidades:**
- Atualiza collection existente ou cria nova
- Preserva scripts customizados quando possível

---

## 📋 Uso via Makefile

**SEMPRE usar Makefile quando disponível:**

```bash
make validate    # Validação
make setup       # Setup
make clean       # Limpeza
```

---

## 🔧 Configuração

### Variáveis de ambiente

```bash
NOTION_API_KEY=secret_xxx

# SSH por projeto
DEPLOYMENT_MYPROJECT_SSH_HOST=server.example.com
DEPLOYMENT_MYPROJECT_SSH_USER=root
DEPLOYMENT_MYPROJECT_PASSWORD=***
```

### Projetos

Os scripts `daily_standup.py` e `project_status.py` carregam projetos de `config/system/tracked-projects.json`:

```json
{
  "meu-projeto": {
    "name": "Meu Projeto",
    "path": "~/Projetos/meu-projeto",
    "type": "microservice",
    "priority": "ALTA"
  }
}
```

---

## 📦 Dependências

```bash
pip install requests python-dotenv paramiko
```

---

## 🗑️ Deprecated

Scripts deprecated estão em `scripts/_deprecated/`:
- `diagram_generator/` - Reativado como skill (ver `skills/documentation/diagram-generation/`)
- `save_context.py` - Substituído por `save-context.sh`

---

**Última Atualização:** 2026-01-20

