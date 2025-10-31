# 📊 Status e Propriedades Completas por Base

**Data:** 11/10/2025  
**Versão:** 1.0  
**Fonte:** API Notion (dados reais)

---

## 🎯 OBJETIVO

Este arquivo lista **TODOS os status e propriedades disponíveis** em cada base do Notion.

Use como referência sempre que criar ou atualizar cards.

---

## 1️⃣ BASE TRABALHO (WORK)

### Status Disponíveis

| Status | Quando Usar | Cor |
|--------|-------------|-----|
| `Não iniciado` | Tarefa ainda não começou (PADRÃO) | Cinza |
| `Em Andamento` | Tarefa em execução | Azul |
| `Em Revisão` | Aguardando code review / validação | Amarelo |
| `Concluído` | Tarefa finalizada | Verde |
| `Pausado` | Temporariamente parada | Laranja |
| `Cancelado` | Não será mais feita | Vermelho |

**Status Padrão:** `Não iniciado`

---

### Propriedades Completas

| Propriedade | Tipo | Descrição | Exemplo |
|-------------|------|-----------|---------|
| `Nome do projeto` | title | Título do card | "Implementar Dashboard" |
| `Status` | status | Estado atual | "Em Andamento" |
| `Cliente` | select | Cliente do projeto | "Astracode", "Pessoal", "FIAP" |
| `Projeto` | select | Projeto relacionado | "ExpenseIQ", "HubTravel", "Avulso" |
| `Prioridade` | select | Nível de prioridade | "Baixa", "Normal", "Média", "Alta", "Urgente" |
| `Prioridade 2` | select | Segunda prioridade | (mesmo que Prioridade) |
| `Periodo` | date | Data/hora de execução | `{'start': '...', 'end': '...'}` |
| `item principal` | relation | Card pai (para sub-itens) | ID do card |
| `Subitem` | relation | Sub-cards | IDs dos cards filhos |
| `Sprint` | relation | Sprint relacionada | ID da sprint |
| `Subtarefa` | relation | Subtarefas | IDs das subtarefas |
| `tarefa principal` | relation | Tarefa principal | ID da tarefa |
| `Bloqueando` | relation | Cards bloqueados por este | IDs de cards |
| `Bloqueado por` | relation | Cards que bloqueiam este | IDs de cards |
| `Responsável` | people | Quem é responsável | @usuario |
| `Pull Requests do GitHub` | relation | PRs relacionadas | IDs de PRs |
| `ID` | unique_id | ID único auto-gerado | Gerado automaticamente |
| `Progresso` | rollup | Progresso calculado | Calculado automaticamente |

---

## 2️⃣ BASE PESSOAL (PERSONAL)

### Status Disponíveis

| Status | Quando Usar | Cor |
|--------|-------------|-----|
| `Não iniciado` | Tarefa ainda não começou (PADRÃO) | Cinza |
| `Em Andamento` | Tarefa em execução | Azul |
| `Concluído` | Tarefa finalizada | Verde |
| `Cancelado` | Não será mais feita | Vermelho |

**Status Padrão:** `Não iniciado`

---

### Propriedades Completas

| Propriedade | Tipo | Descrição | Exemplo |
|-------------|------|-----------|---------|
| `Nome da tarefa` | title | Título da tarefa | "Organizar Documentos" |
| `Status` | status | Estado atual | "Em Andamento" |
| `Atividade` | select | Tipo de atividade | "Desenvolvimento", "Organização", "Estudo", "Teste" |
| `Data` | date | Data da tarefa | `{'start': '...', 'end': '...'}` |
| `Descrição` | rich_text | Descrição detalhada | Texto livre |
| `Responsável` | people | Quem é responsável | @usuario |
| `Subtarefa` | relation | Subtarefas vinculadas | IDs de subtarefas |
| `tarefa principal` | relation | Tarefa principal (pai) | ID da tarefa pai |

**Nota:** Campo de data é `Data` (não `Periodo`)

---

## 3️⃣ BASE CURSOS (STUDIES)

### Status Disponíveis

| Status | Quando Usar | Cor |
|--------|-------------|-----|
| `Não Adquirido` | Curso ainda não comprado | Cinza |
| `Para Fazer` | Curso adquirido, não iniciado (PADRÃO) | Cinza |
| `Em Revisão` | Revisando conteúdo | Amarelo |
| `Em Pausa` | Temporariamente pausado | Laranja |
| `Em Andamento` | Estudando ativamente | Azul |
| `Descontinuado` | Abandonado | Vermelho |
| `Concluido` | Finalizado | Verde |

**Status Padrão:** `Para Fazer`

---

### Propriedades Completas

| Propriedade | Tipo | Descrição | Exemplo |
|-------------|------|-----------|---------|
| `Project name` | title | Nome do curso/aula | "FIAP IA para Devs" |
| `Status` | status | Estado atual | "Em Andamento" |
| `Categorias` | multi_select | Tags do curso | ["FIAP", "IA", "Cursos"] |
| `Prioridade` | select | Nível de prioridade | "Baixa", "Normal", "Alta" |
| `Período` | date | Quando estudar | `{'start': '...', 'end': '...'}` |
| `Tempo Total` | rich_text | Duração estimada | "01:30:00", "40:00:00" |
| `Descrição` | rich_text | Descrição do conteúdo | Texto livre |
| `URL` | url | Link externo | "https://..." |
| `Parent item` | relation | Item pai (curso/seção) | ID do pai |
| `Sub-item` | relation | Sub-itens | IDs dos filhos |
| `Bloqueando` | relation | Itens bloqueados | IDs |
| `Bloqueado por` | relation | Dependências | IDs |
| `Attach file` | files | Arquivos anexos | Arquivos |
| `Progress` | rollup | Progresso calculado | Automático |

**Nota:** Campo de data é `Período` (com acento)

---

## 4️⃣ BASE YOUTUBE (YOUTUBER)

### Status Disponíveis

| Status | Quando Usar | Cor |
|--------|-------------|-----|
| `Para Gravar` | Episódio agendado para gravação | Cinza |
| `Não iniciado` | Ainda não começou (PADRÃO) | Cinza |
| `Gravando` | Gravação em andamento | Azul |
| `Para Edição` | Gravado, aguardando edição | Amarelo |
| `Editando` | Edição em andamento | Azul |
| `Editado` | Edição concluída | Amarelo |
| `Publicado` | Vídeo no ar | Verde |
| `Concluído` | Totalmente finalizado | Verde |

**Status Padrão:** `Não iniciado`

---

### Propriedades Completas

| Propriedade | Tipo | Descrição | Exemplo |
|-------------|------|-----------|---------|
| `Nome do projeto` | title | Nome da série/episódio | "The Legend of Heroes" |
| `Status` | status | Estado atual | "Para Edição" |
| `Periodo` | date | Data/hora de GRAVAÇÃO | `{'start': '...', 'end': '...'}` |
| `Data de Lançamento` | date | Data/hora de PUBLICAÇÃO | `2025-10-17T12:00:00-03:00` |
| `Resumo do Episodio` | rich_text | Sinopse do episódio/série | Texto livre |
| `Link do Video` | url | URL do vídeo publicado | "https://youtube.com/..." |
| `item principal` | relation | Série (para episódios) | ID da série |
| `Subitem` | relation | Episódios (para séries) | IDs dos episódios |

---

## 📋 REFERÊNCIA RÁPIDA: MAPEAMENTO DE CAMPOS

### Como Passar Dados para NotionEngine

| Base | Você Passa | Vira no Notion |
|------|------------|----------------|
| **WORK** | `title` | `Nome do projeto` |
| | `status` | `Status` |
| | `cliente` | `Cliente` |
| | `projeto` | `Projeto` |
| | `priority` | `Prioridade` |
| | `periodo` | `Periodo` |
| | `item_principal` | `item principal` |
| **PERSONAL** | `title` | `Nome da tarefa` |
| | `status` | `Status` |
| | `atividade` | `Atividade` |
| | `periodo` | `Data` |
| | `description` | `Descrição` |
| | `tarefa_principal` | `tarefa principal` |
| **STUDIES** | `title` | `Project name` |
| | `status` | `Status` |
| | `categorias` | `Categorias` |
| | `prioridade` | `Prioridade` |
| | `tempo_total` | `Tempo Total` |
| | `periodo` | `Período` |
| | `parent_item` | `Parent item` |
| **YOUTUBER** | `title` | `Nome do projeto` |
| | `status` | `Status` |
| | `periodo` | `Periodo` |
| | `data_lancamento` | `Data de Lançamento` |
| | `resumo_episodio` | `Resumo do Episodio` |
| | `item_principal` | `item principal` |

---

## 🎨 ÍCONES RECOMENDADOS

### Por Tipo de Card

#### Projetos e Principais
- 🚀 Novo projeto
- 🏢 Projeto corporativo
- 💼 Projeto cliente
- 🎯 Projeto pessoal
- 🎓 Curso/Formação
- 🎬 Série YouTube

#### Sub-itens e Tarefas
- ✅ Tarefa/Subtarefa
- 📋 Item de checklist
- 🔧 Tarefa técnica
- 🎯 Aula/Lição
- 📺 Episódio
- 📑 Seção/Módulo

#### Status e Contexto
- ⚡ Urgente
- 🔥 Alta prioridade
- 🧪 Teste
- 📝 Documentação
- 🐛 Bug fix
- ✨ Nova feature

---

## 📅 FORMATOS DE DATA E HORA

### Timezone GMT-3 (SEMPRE)

```python
from datetime import datetime, timezone, timedelta

SAO_PAULO_TZ = timezone(timedelta(hours=-3))

# Criar datetime
dt = datetime(2025, 10, 16, 19, 0, 0, tzinfo=SAO_PAULO_TZ)

# Formatar para Notion (COM horário)
data_com_hora = dt.isoformat()
# Resultado: '2025-10-16T19:00:00-03:00'

# Formatar para Notion (SEM horário)
data_sem_hora = dt.strftime('%Y-%m-%d')
# Resultado: '2025-10-16'
```

### Quando Usar Cada Formato

| Tipo de Card | Formato | Exemplo |
|--------------|---------|---------|
| Aula (STUDIES) | COM horário | `2025-10-16T19:00:00-03:00` |
| Seção (STUDIES) | SEM horário | `2025-10-16` |
| Curso (STUDIES) | SEM horário | `2025-10-16` |
| Episódio (YOUTUBER) | COM horário | `2025-10-16T21:00:00-03:00` |
| Série (YOUTUBER) | COM horário | `2025-10-16T21:00:00-03:00` |
| Tarefa (WORK) | COM horário | `2025-10-16T09:00:00-03:00` |
| Tarefa (PERSONAL) | COM horário | `2025-10-16T19:00:00-03:00` |

---

## 🔢 CÁLCULO DE TEMPO TOTAL

### Formato
- **HH:MM:SS** - Horas, minutos, segundos
- **MM:SS** - Minutos, segundos

### Exemplos
```python
'tempo_total': '01:30:00'  # 1 hora e 30 minutos
'tempo_total': '00:45:00'  # 45 minutos
'tempo_total': '40:00:00'  # 40 horas
'tempo_total': '02:15:30'  # 2 horas, 15 min e 30 seg
```

### Calcular Duração Total

```python
def calcular_duracao_total(durações):
    """Soma durações em formato HH:MM:SS"""
    from datetime import timedelta
    
    total = timedelta()
    
    for duracao in durações:
        # Parse HH:MM:SS
        partes = duracao.split(':')
        if len(partes) == 3:
            h, m, s = map(int, partes)
            total += timedelta(hours=h, minutes=m, seconds=s)
        elif len(partes) == 2:
            m, s = map(int, partes)
            total += timedelta(minutes=m, seconds=s)
    
    # Formatar de volta
    horas = int(total.total_seconds() // 3600)
    minutos = int((total.total_seconds() % 3600) // 60)
    segundos = int(total.total_seconds() % 60)
    
    return f'{horas:02d}:{minutos:02d}:{segundos:02d}'

# Exemplo de uso
aulas = ['01:30:00', '02:00:00', '01:15:30']
total = calcular_duracao_total(aulas)
print(f'Duração total: {total}')  # 04:45:30
```

---

## 🎯 CATEGORIAS COMUNS

### STUDIES - Categorias Recomendadas

#### Por Instituição
- `FIAP`
- `Rocketseat`
- `Udemy`
- `Coursera`
- `Alura`

#### Por Tecnologia
- `Inteligência Artificial`
- `Machine Learning`
- `Python`
- `TypeScript`
- `React`
- `Node.js`

#### Por Tipo
- `Cursos`
- `Formação Completa`
- `Módulo`
- `Aula`
- `Workshop`
- `Bootcamp`

#### Por Área
- `Desenvolvimento`
- `Data Science`
- `DevOps`
- `Frontend`
- `Backend`
- `Fullstack`

### Exemplo de Uso
```python
# Curso principal
'categorias': ['FIAP', 'Inteligência Artificial', 'Formação Completa']

# Módulo
'categorias': ['FIAP', 'Machine Learning', 'Módulo']

# Aula
'categorias': ['FIAP', 'Deep Learning', 'Aula', 'Prática']
```

---

## 💼 CLIENTES E PROJETOS (WORK)

### Clientes Válidos
- `Astracode` ← **Padrão para trabalho profissional**
- `Pessoal`
- `FIAP`
- `Outros`

### Projetos Válidos
- `ExpenseIQ` ← Agente ExpenseIQ sempre usa
- `HubTravel` ← Agente HubTravel sempre usa
- `Avulso` ← Padrão quando não especificado
- `MyLocalPlace`
- `Automação`

### Quando Usar Cada Um

| Situação | Cliente | Projeto |
|----------|---------|---------|
| Trabalho Astracode - ExpenseIQ | `Astracode` | `ExpenseIQ` |
| Trabalho Astracode - HubTravel | `Astracode` | `HubTravel` |
| Trabalho Astracode - Outros | `Astracode` | `Avulso` |
| Projeto pessoal | `Pessoal` | `MyLocalPlace` |
| Automação Notion | `Pessoal` | `Automação` |
| Curso FIAP | `FIAP` | `Avulso` |

---

## 👤 ATIVIDADES (PERSONAL)

### Atividades Comuns
- `Desenvolvimento`
- `Organização`
- `Estudo`
- `Teste`
- `Planejamento`
- `Financeiro`
- `Saúde`
- `Lazer`

### Quando Usar
```python
# Tarefas técnicas
'atividade': 'Desenvolvimento'

# Organização pessoal
'atividade': 'Organização'

# Aprender algo
'atividade': 'Estudo'

# Pagar contas, transferências
'atividade': 'Financeiro'
```

---

## 🎮 CAMPOS ESPECIAIS DO YOUTUBE

### Resumo do Episódio

#### Para Primeiro Episódio
```python
'resumo_episodio': '''
Bem-vindos à nossa jornada através de [Nome do Jogo]!

Nesta série, vamos explorar [descrição do jogo], enfrentando
desafios únicos e descobrindo segredos escondidos.

Cada episódio nos levará mais fundo na história, com [características
especiais da série].

Prepare-se para [expectativa da experiência]!
'''
```

#### Para Episódios Seguintes
```python
'resumo_episodio': f'Episódio {numero}: [Descrição breve do que acontece neste episódio específico]'
```

### Data de Lançamento vs Período

```python
# SÉRIE (sem Data de Lançamento)
{
    'periodo': {
        'start': '2025-10-16T21:00:00-03:00',  # Gravação 1º ep
        'end': '2025-11-04T23:30:00-03:00'      # Gravação último ep
    }
    # SEM 'data_lancamento'
}

# EPISÓDIO (com ambos)
{
    'periodo': {
        'start': '2025-10-16T21:00:00-03:00',  # Quando GRAVAR
        'end': '2025-10-16T23:30:00-03:00'
    },
    'data_lancamento': '2025-10-17T12:00:00-03:00'  # Quando PUBLICAR
}
```

---

## ⚙️ VALORES PADRÃO

### Quando Não Especificar

| Base | Propriedade | Valor Padrão | Definido No |
|------|-------------|--------------|-------------|
| WORK | `status` | `Não iniciado` | NotionEngine |
| WORK | `cliente` | `Pessoal` | NotionEngine |
| WORK | `projeto` | `Automação` | NotionEngine |
| WORK | `priority` | `Normal` | NotionEngine |
| PERSONAL | `status` | `Não iniciado` | NotionEngine |
| PERSONAL | `atividade` | `Desenvolvimento` | NotionEngine |
| STUDIES | `status` | `Para Fazer` | NotionEngine |
| YOUTUBER | `status` | `Não iniciado` | NotionEngine |

### Como Funcionam
```python
# Se você não passar 'status'
card_data = {
    'title': 'Minha Tarefa'
    # SEM 'status'
}

# NotionEngine usa o padrão
engine.create_card('WORK', card_data)
# → Status será 'Não iniciado'
```

---

## 🔍 VALIDAÇÃO DE PROPRIEDADES

### Como Verificar se Propriedade Existe

```python
import requests

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
DATABASE_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-WORK_DB_ID'  # WORK

url = f'https://api.notion.com/v1/databases/{DATABASE_ID}'
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    print('📊 Propriedades da base WORK:\n')
    
    for prop_name, prop_data in data['properties'].items():
        prop_type = prop_data.get('type')
        print(f'  {prop_name}: {prop_type}')
```

---

## ✅ CHECKLIST DE PROPRIEDADES

### WORK
- [ ] `title` definido
- [ ] `status` válido
- [ ] `cliente` apropriado (padrão: Astracode)
- [ ] `projeto` correto
- [ ] `priority` Normal ou especificada
- [ ] Se sub-item: `item_principal` preenchido

### PERSONAL
- [ ] `title` definido
- [ ] `status` válido
- [ ] `atividade` apropriada
- [ ] Se subtarefa: `tarefa_principal` preenchido

### STUDIES
- [ ] `title` definido
- [ ] `status` válido
- [ ] `categorias` relevantes
- [ ] `prioridade` Normal ou especificada
- [ ] `tempo_total` calculado
- [ ] Se aula: `periodo` COM horário
- [ ] Se seção/curso: `periodo` SEM horário
- [ ] Se sub-item: `parent_item` preenchido

### YOUTUBER
- [ ] `title` definido
- [ ] `status` válido
- [ ] Se série: `periodo` SEM `data_lancamento`
- [ ] Se episódio: TEM `data_lancamento`
- [ ] Se episódio 1: `resumo_episodio` com sinopse
- [ ] Se episódio: `item_principal` preenchido

---

**Próximo:** Leia `06_TROUBLESHOOTING.md` para resolver erros comuns














