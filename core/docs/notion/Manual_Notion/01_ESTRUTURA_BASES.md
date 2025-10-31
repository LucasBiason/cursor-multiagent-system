# 📊 Estrutura Detalhada das Bases Notion

**Data:** 11/10/2025  
**Versão:** 1.0  
**Status:** Completo e validado

---

## 🎯 VISÃO GERAL

O sistema Notion do Lucas é organizado em **4 bases principais**, cada uma com estrutura e propósito específicos.

---

## 1️⃣ BASE TRABALHO (WORK)

### Informações Gerais
- **ID da Database:** `1f9962a7-693c-80a3-b947-c471a975acb0`
- **Campo de Título:** `Nome do projeto`
- **Campo de Relação:** `item principal`
- **Uso:** Projetos profissionais da Astracode (ExpenseIQ, HubTravel, etc.)

### Propriedades Disponíveis

| Propriedade | Tipo | Obrigatório | Descrição |
|-------------|------|-------------|-----------|
| `Nome do projeto` | title | ✅ Sim | Título do card |
| `Status` | status | ✅ Sim | Estado atual do projeto |
| `Cliente` | select | Não | Cliente do projeto |
| `Projeto` | select | Não | Projeto relacionado |
| `Prioridade` | select | Não | Nível de prioridade |
| `Periodo` | date | Não | Data/hora de execução |
| `item principal` | relation | Não | Vínculo com card pai |
| `Subitem` | relation | Não | Vínculo com sub-cards |
| `Sprint` | relation | Não | Sprint relacionada |
| `Subtarefa` | relation | Não | Subtarefas |
| `tarefa principal` | relation | Não | Tarefa principal |
| `Bloqueando` | relation | Não | Cards bloqueados |
| `Bloqueado por` | relation | Não | Cards que bloqueiam |
| `Responsável` | people | Não | Responsável pela tarefa |
| `ID` | unique_id | Auto | ID único gerado |
| `Progresso` | rollup | Auto | Progresso calculado |
| `Pull Requests do GitHub` | relation | Não | PRs relacionadas |

### Status Disponíveis
- `Não iniciado` (padrão)
- `Em Andamento`
- `Em Revisão`
- `Concluído`
- `Pausado`
- `Cancelado`

### Clientes Comuns
- `Astracode` (padrão)
- `Pessoal`
- `FIAP`

### Projetos Comuns
- `ExpenseIQ`
- `HubTravel`
- `Avulso` (padrão quando não especificado)

### Prioridades
- `Baixa`
- `Normal` (padrão)
- `Média`
- `Alta`
- `Urgente`

---

## 2️⃣ BASE PESSOAL (PERSONAL)

### Informações Gerais
- **ID da Database:** `1fa962a7-693c-8032-8996-dd9cd2607dbf`
- **Campo de Título:** `Nome da tarefa`
- **Campo de Relação:** `tarefa principal`
- **Uso:** Tarefas pessoais, organização, hábitos

### Propriedades Disponíveis

| Propriedade | Tipo | Obrigatório | Descrição |
|-------------|------|-------------|-----------|
| `Nome da tarefa` | title | ✅ Sim | Título da tarefa |
| `Status` | status | ✅ Sim | Estado atual |
| `Atividade` | select | Não | Tipo de atividade |
| `Data` | date | Não | Data da tarefa |
| `Descrição` | rich_text | Não | Descrição detalhada |
| `Responsável` | people | Não | Responsável |
| `Subtarefa` | relation | Não | Subtarefas vinculadas |
| `tarefa principal` | relation | Não | Tarefa principal (vínculo pai) |

### Status Disponíveis
- `Não iniciado` (padrão)
- `Em Andamento`
- `Concluído`
- `Cancelado`

### Atividades Comuns
- `Desenvolvimento`
- `Organização`
- `Estudo`
- `Teste`
- `Planejamento`

### Observações Importantes
- Campo de data é `Data` (não `Periodo`)
- Base mais simples, sem muitas propriedades complexas
- Foco em tarefas rápidas e objetivas

---

## 3️⃣ BASE CURSOS (STUDIES)

### Informações Gerais
- **ID da Database:** `1fa962a7-693c-80de-b90b-eaa513dcf9d1`
- **Campo de Título:** `Project name`
- **Campo de Relação:** `Parent item`
- **Uso:** Cursos, formações, aulas, estudos

### Propriedades Disponíveis

| Propriedade | Tipo | Obrigatório | Descrição |
|-------------|------|-------------|-----------|
| `Project name` | title | ✅ Sim | Nome do curso/aula |
| `Status` | status | ✅ Sim | Estado atual |
| `Categorias` | multi_select | Não | Tags do curso |
| `Prioridade` | select | Não | Nível de prioridade |
| `Período` | date | Não | Data/hora de estudo |
| `Tempo Total` | rich_text | Não | Duração estimada |
| `Descrição` | rich_text | Não | Descrição do conteúdo |
| `URL` | url | Não | Link externo |
| `Parent item` | relation | Não | Item pai (curso/seção) |
| `Sub-item` | relation | Não | Sub-itens |
| `Bloqueando` | relation | Não | Itens bloqueados |
| `Bloqueado por` | relation | Não | Dependências |
| `Attach file` | files | Não | Arquivos anexos |
| `Progress` | rollup | Auto | Progresso calculado |

### Status Disponíveis
- `Não Adquirido`
- `Para Fazer` (padrão)
- `Em Revisão`
- `Em Pausa`
- `Em Andamento`
- `Descontinuado`
- `Concluido`

### Categorias Comuns
- `FIAP`
- `Rocketseat`
- `Cursos`
- `Inteligência Artificial`
- `Machine Learning`
- `Desenvolvimento`
- `Fundamentos`

### Estrutura Hierárquica Típica
```
Formação/Curso (sem horário)
├── Fase/Bloco (sem horário)
│   ├── Seção/Módulo (sem horário)
│   │   ├── Aula 1 (COM horário 19:00-21:00)
│   │   ├── Aula 2 (COM horário 19:00-21:00)
│   │   └── Aula 3 (COM horário 19:00-21:00)
```

### Regra de Horários
- **Aulas (nível mais baixo):** COM horário específico
- **Seções/Módulos:** SEM horário (apenas data)
- **Cursos/Formações:** SEM horário (apenas data)

---

## 4️⃣ BASE YOUTUBE (YOUTUBER)

### Informações Gerais
- **ID da Database:** `1fa962a7-693c-80ce-9f1d-ff86223d6bda`
- **Campo de Título:** `Nome do projeto`
- **Campo de Relação:** `item principal`
- **Uso:** Séries de jogos e episódios do canal

### Propriedades Disponíveis

| Propriedade | Tipo | Obrigatório | Descrição |
|-------------|------|-------------|-----------|
| `Nome do projeto` | title | ✅ Sim | Nome da série/episódio |
| `Status` | status | ✅ Sim | Estado atual |
| `Periodo` | date | Não | Data/hora de GRAVAÇÃO |
| `Data de Lançamento` | date | Não | Data de PUBLICAÇÃO |
| `Resumo do Episodio` | rich_text | Não | Sinopse do episódio |
| `Link do Video` | url | Não | URL do vídeo publicado |
| `item principal` | relation | Não | Série (para episódios) |
| `Subitem` | relation | Não | Episódios (para séries) |

### Status Disponíveis
- `Para Gravar`
- `Não iniciado` (padrão)
- `Editado`
- `Editando`
- `Para Edição`
- `Gravando`
- `Publicado`
- `Concluído`

### Diferença Entre Campos de Data

#### `Periodo` (Data de Gravação)
- **O QUE É:** Quando o episódio será GRAVADO
- **QUANDO:** Data e hora reais de trabalho
- **EXEMPLO:** `2025-10-16T21:00:00-03:00` até `2025-10-16T23:30:00-03:00`

#### `Data de Lançamento` (Publicação)
- **O QUE É:** Quando o episódio será PUBLICADO
- **QUANDO:** Data e hora que ficará público no YouTube
- **EXEMPLO:** `2025-10-17T12:00:00-03:00`

### Estrutura Hierárquica
```
Série Principal (sem Data de Lançamento)
  └─ Periodo: início da gravação do 1º ep → fim da gravação do último ep
├── Episódio 01 (com Periodo E Data de Lançamento)
├── Episódio 02 (com Periodo E Data de Lançamento)
└── Episódio 03 (com Periodo E Data de Lançamento)
```

### Regras Especiais
- **Série:** Tem `Periodo` (gravação), NÃO tem `Data de Lançamento`
- **Episódios:** Tem AMBOS (`Periodo` e `Data de Lançamento`)
- **Primeiro episódio:** Deve ter sinopse da série em `Resumo do Episodio`

---

## 🔄 CAMPOS DE RELAÇÃO

### Resumo Rápido

| Base | Para Criar Sub-item | Campo a Usar | Valor |
|------|---------------------|--------------|-------|
| WORK | Sub-item de projeto | `item_principal` | ID do projeto pai |
| PERSONAL | Subtarefa | `tarefa_principal` | ID da tarefa pai |
| STUDIES | Aula de curso | `parent_item` | ID do curso/seção |
| YOUTUBER | Episódio de série | `item_principal` | ID da série |

---

## 📝 EXEMPLO COMPLETO DE CADA BASE

### WORK
```python
# Projeto principal
{
    'title': 'Implementar Feature X',
    'status': 'Não iniciado',
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'priority': 'Normal',
    'periodo': {
        'start': '2025-10-15T09:00:00-03:00',
        'end': '2025-10-15T17:00:00-03:00'
    }
}

# Sub-item linkado
{
    'title': 'Tarefa Específica',
    'status': 'Não iniciado',
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'priority': 'Normal',
    'item_principal': 'ID_DO_PROJETO_PAI',  # Vínculo
    'periodo': {
        'start': '2025-10-15T09:00:00-03:00',
        'end': '2025-10-15T12:00:00-03:00'
    }
}
```

### PERSONAL
```python
# Tarefa principal
{
    'title': 'Organizar Documentos',
    'status': 'Não iniciado',
    'atividade': 'Organização',
    'periodo': {
        'start': '2025-10-15T19:00:00-03:00',
        'end': '2025-10-15T20:00:00-03:00'
    }
}

# Subtarefa linkada
{
    'title': 'Escanear Documentos',
    'status': 'Não iniciado',
    'atividade': 'Organização',
    'tarefa_principal': 'ID_DA_TAREFA_PAI',  # Vínculo
    'periodo': {
        'start': '2025-10-15T19:00:00-03:00',
        'end': '2025-10-15T19:30:00-03:00'
    }
}
```

### STUDIES
```python
# Curso principal (SEM horário)
{
    'title': 'FIAP IA para Devs',
    'status': 'Para Fazer',
    'categorias': ['FIAP', 'Inteligência Artificial'],
    'prioridade': 'Normal',
    'tempo_total': '40:00:00',
    'periodo': {
        'start': '2025-10-16',  # Apenas data
        'end': '2025-12-15'
    }
}

# Seção (SEM horário)
{
    'title': 'Seção 1: Fundamentos',
    'status': 'Para Fazer',
    'categorias': ['FIAP', 'Fundamentos'],
    'prioridade': 'Normal',
    'tempo_total': '08:00:00',
    'parent_item': 'ID_DO_CURSO',  # Vínculo
    'periodo': {
        'start': '2025-10-16',  # Apenas data
        'end': '2025-10-30'
    }
}

# Aula (COM horário)
{
    'title': 'Aula 1: Introdução',
    'status': 'Para Fazer',
    'categorias': ['FIAP', 'Introdução', 'Teoria'],
    'prioridade': 'Normal',
    'tempo_total': '01:30:00',
    'parent_item': 'ID_DA_SECAO',  # Vínculo
    'periodo': {
        'start': '2025-10-16T19:00:00-03:00',  # COM horário
        'end': '2025-10-16T21:00:00-03:00'
    }
}
```

### YOUTUBER
```python
# Série principal
{
    'title': 'The Legend of Heroes',
    'status': 'Não iniciado',
    'periodo': {
        'start': '2025-10-16T21:00:00-03:00',  # Gravação 1º ep
        'end': '2025-11-04T23:30:00-03:00'      # Gravação último ep
    }
    # SEM Data de Lançamento
}

# Episódio linkado
{
    'title': 'Episódio 01',
    'status': 'Não iniciado',
    'periodo': {
        'start': '2025-10-16T21:00:00-03:00',  # Gravação
        'end': '2025-10-16T23:30:00-03:00'
    },
    'data_lancamento': '2025-10-17T12:00:00-03:00',  # Publicação
    'item_principal': 'ID_DA_SERIE',  # Vínculo
    'resumo_episodio': 'Sinopse da série...'  # Apenas no 1º episódio
}
```

---

## 🔍 DIFERENÇAS IMPORTANTES

### Campos de Título
- **WORK:** `Nome do projeto`
- **PERSONAL:** `Nome da tarefa`
- **STUDIES:** `Project name`
- **YOUTUBER:** `Nome do projeto`

### Campos de Relação para Vínculo Pai
- **WORK:** `item principal`
- **PERSONAL:** `tarefa principal`
- **STUDIES:** `Parent item`
- **YOUTUBER:** `item principal`

### Campos de Data
- **WORK:** `Periodo` (com 'o')
- **PERSONAL:** `Data`
- **STUDIES:** `Período` (com acento)
- **YOUTUBER:** `Periodo` (com 'o') + `Data de Lançamento`

### Status Padrão
- **WORK:** `Não iniciado`
- **PERSONAL:** `Não iniciado`
- **STUDIES:** `Para Fazer`
- **YOUTUBER:** `Não iniciado`

---

## ⚠️ ARMADILHAS COMUNS

### 1. Campo de Data Errado
```python
# ❌ ERRADO - PERSONAL
'periodo': {...}  # Campo não existe

# ✅ CORRETO - PERSONAL
'periodo': {...}  # Será mapeado para 'Data' pelo NotionEngine
```

### 2. Campo de Relação Errado
```python
# ❌ ERRADO - STUDIES
'item_principal': 'id123'  # Campo errado

# ✅ CORRETO - STUDIES
'parent_item': 'id123'  # Campo correto
```

### 3. Status Inválido
```python
# ❌ ERRADO - YOUTUBER
'status': 'Para Fazer'  # Não existe nesta base

# ✅ CORRETO - YOUTUBER
'status': 'Não iniciado'  # Status válido
```

### 4. Horário em Campo Errado
```python
# ❌ ERRADO - Seção de curso
'periodo': {
    'start': '2025-10-16T19:00:00-03:00',  # Não deve ter horário
    'end': '2025-10-30T21:00:00-03:00'
}

# ✅ CORRETO - Seção de curso
'periodo': {
    'start': '2025-10-16',  # Apenas data
    'end': '2025-10-30'
}
```

---

## 📋 CHECKLIST DE VALIDAÇÃO

Antes de criar um card, verifique:

- [ ] Base correta identificada (WORK, PERSONAL, STUDIES, YOUTUBER)
- [ ] Campo de título usando nome correto da base
- [ ] Status existe na base de destino
- [ ] Campo de data correto (`Data`, `Periodo`, `Período`)
- [ ] Se for sub-item, campo de relação correto preenchido
- [ ] Timezone GMT-3 em todas as datas
- [ ] Horários apenas onde necessário (aulas, episódios)

---

**Próximo:** Leia `02_REGRAS_CRIACAO_CARDS.md` para aprender as regras obrigatórias












