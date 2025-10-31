# 📋 Regras Obrigatórias para Criação de Cards

**Data:** 11/10/2025  
**Versão:** 1.0  
**Status:** Validado com testes reais

---

## 🎯 REGRAS UNIVERSAIS

Estas regras se aplicam a **TODAS as bases** sem exceção.

---

## 1️⃣ TIMEZONE

### Regra de Ouro
**SEMPRE GMT-3 (São Paulo)**  
**NUNCA UTC**

### Formatos Corretos

#### Com Horário
```python
'start': '2025-10-16T19:00:00-03:00'
'end': '2025-10-16T21:00:00-03:00'
```

#### Sem Horário (apenas data)
```python
'start': '2025-10-16'
'end': '2025-10-30'
```

### Código Python
```python
from datetime import datetime, timezone, timedelta

# Criar timezone GMT-3
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

# Criar datetime com timezone
dt = datetime(2025, 10, 16, 19, 0, 0, tzinfo=SAO_PAULO_TZ)

# Formatar para Notion
data_notion = dt.isoformat()  # '2025-10-16T19:00:00-03:00'
```

---

## 2️⃣ ÍCONES E EMOJIS

### Regra de Ouro
**Emojis SEMPRE como ícone da página**  
**NUNCA no título do card**

### Formato Correto

```python
payload = {
    "parent": {"database_id": "..."},
    "icon": {"emoji": "🎓"},  # ✅ Ícone aqui
    "properties": {
        "Project name": {
            "title": [{"text": {"content": "Meu Curso"}}]  # ✅ Sem emoji
        }
    }
}
```

### Erros Comuns

```python
# ❌ ERRADO
"title": [{"text": {"content": "🎓 Meu Curso"}}]

# ✅ CORRETO
"icon": {"emoji": "🎓"},
"title": [{"text": {"content": "Meu Curso"}}]
```

### Emojis Recomendados por Base

#### WORK
- Projetos: `🚀`, `💼`, `🏢`
- Sub-itens: `📋`, `✅`, `🔧`

#### PERSONAL
- Tarefas: `👤`, `📝`, `🎯`
- Subtarefas: `✅`, `📌`, `⚡`

#### STUDIES
- Cursos: `🎓`, `📚`, `🎯`
- Fases: `📖`, `📑`
- Seções: `📑`, `📂`
- Aulas: `🎯`, `📝`, `💡`

#### YOUTUBER
- Séries: `🎬`, `🎮`, `📺`
- Episódios: `📺`, `🎥`, `▶️`

---

## 3️⃣ HIERARQUIAS E VÍNCULOS

### Regra de Ouro
**Sub-itens DEVEM ter campo de relação preenchido**

### Como Criar Hierarquia

#### BASE WORK
```python
# 1. Criar projeto principal
projeto_id = engine.create_card('WORK', {
    'title': 'Projeto Principal',
    'status': 'Não iniciado'
})

# 2. Criar sub-item LINKADO
subitem_id = engine.create_card('WORK', {
    'title': 'Sub-item 1',
    'status': 'Não iniciado',
    'item_principal': projeto_id  # ← VÍNCULO
})
```

#### BASE PERSONAL
```python
# 1. Criar tarefa principal
tarefa_id = engine.create_card('PERSONAL', {
    'title': 'Tarefa Principal',
    'status': 'Não iniciado'
})

# 2. Criar subtarefa LINKADA
subtarefa_id = engine.create_card('PERSONAL', {
    'title': 'Subtarefa 1',
    'status': 'Não iniciado',
    'tarefa_principal': tarefa_id  # ← VÍNCULO
})
```

#### BASE STUDIES
```python
# 1. Criar curso
curso_id = engine.create_card('STUDIES', {
    'title': 'Meu Curso',
    'status': 'Para Fazer',
    'periodo': {
        'start': '2025-10-16',  # Sem horário
        'end': '2025-12-15'
    }
})

# 2. Criar seção
secao_id = engine.create_card('STUDIES', {
    'title': 'Seção 1',
    'status': 'Para Fazer',
    'parent_item': curso_id,  # ← VÍNCULO
    'periodo': {
        'start': '2025-10-16',  # Sem horário
        'end': '2025-10-30'
    }
})

# 3. Criar aula
aula_id = engine.create_card('STUDIES', {
    'title': 'Aula 1',
    'status': 'Para Fazer',
    'parent_item': secao_id,  # ← VÍNCULO
    'periodo': {
        'start': '2025-10-16T19:00:00-03:00',  # COM horário
        'end': '2025-10-16T21:00:00-03:00'
    }
}
)
```

#### BASE YOUTUBER
```python
# 1. Criar série
serie_id = engine.create_card('YOUTUBER', {
    'title': 'Minha Série',
    'status': 'Não iniciado',
    'periodo': {
        'start': '2025-10-16T21:00:00-03:00',  # Gravação 1º ep
        'end': '2025-11-04T23:30:00-03:00'      # Gravação último ep
    }
    # SEM data_lancamento
})

# 2. Criar episódio
ep_id = engine.create_card('YOUTUBER', {
    'title': 'Episódio 01',
    'status': 'Não iniciado',
    'item_principal': serie_id,  # ← VÍNCULO
    'periodo': {
        'start': '2025-10-16T21:00:00-03:00',  # Gravação
        'end': '2025-10-16T23:30:00-03:00'
    },
    'data_lancamento': '2025-10-17T12:00:00-03:00',  # Publicação
    'resumo_episodio': 'Sinopse da série...'  # Apenas ep 1
})
```

---

## 4️⃣ HORÁRIOS E PERÍODOS

### Regras de Horários de Estudo (STUDIES)
- **Horário padrão:** 19:00-21:00 (segunda a sexta)
- **Terças:** 19:30-21:00 (após tratamento médico)
- **LIMITE MÁXIMO:** 21:00 (NUNCA ultrapassar)
- **Se passar das 21:00:** Mover aula para próximo dia útil às 19:00

### Quando Incluir Horário

| Tipo de Card | Incluir Horário? | Exemplo |
|--------------|------------------|---------|
| Curso/Formação | ❌ Não | `2025-10-16` até `2025-12-15` |
| Fase/Bloco | ❌ Não | `2025-10-16` até `2025-10-30` |
| Seção/Módulo | ❌ Não | `2025-10-16` até `2025-10-22` |
| Aula | ✅ Sim | `2025-10-16T19:00:00-03:00` |
| Episódio YouTube | ✅ Sim | `2025-10-16T21:00:00-03:00` |
| Tarefa Trabalho | ✅ Sim | `2025-10-16T09:00:00-03:00` |
| Tarefa Pessoal | ✅ Sim | `2025-10-16T19:00:00-03:00` |

---

## 5️⃣ STATUS E PRIORIDADES

### Status por Base

#### WORK
- `Não iniciado` ← Padrão
- `Em Andamento`
- `Em Revisão`
- `Concluído`
- `Pausado`
- `Cancelado`

#### PERSONAL
- `Não iniciado` ← Padrão
- `Em Andamento`
- `Concluído`
- `Cancelado`

#### STUDIES
- `Não Adquirido`
- `Para Fazer` ← Padrão
- `Em Revisão`
- `Em Pausa`
- `Em Andamento`
- `Descontinuado`
- `Concluido`

#### YOUTUBER
- `Para Gravar`
- `Não iniciado` ← Padrão
- `Editado`
- `Editando`
- `Para Edição`
- `Gravando`
- `Publicado`
- `Concluído`

### Prioridade Padrão
- **WORK:** `Normal`
- **STUDIES:** `Normal`
- **PERSONAL:** Não tem campo de prioridade

---

## 6️⃣ CATEGORIAS E TAGS

### WORK
- **Cliente:** `Astracode` (padrão), `Pessoal`, `FIAP`
- **Projeto:** `ExpenseIQ`, `HubTravel`, `Avulso`

### STUDIES
Usar `multi_select` com categorias relevantes:
- Instituição: `FIAP`, `Rocketseat`, `Udemy`
- Tecnologia: `Inteligência Artificial`, `Machine Learning`, `Python`
- Tipo: `Cursos`, `Aula`, `Módulo`, `Formação Completa`

### Exemplo STUDIES
```python
'categorias': ['FIAP', 'Inteligência Artificial', 'Fundamentos']
```

---

## 7️⃣ TEMPO TOTAL

### Formato
- **HH:MM:SS** para durações longas
- **MM:SS** para durações curtas

### Exemplos
```python
'tempo_total': '01:30:00'  # 1 hora e 30 minutos
'tempo_total': '00:45:30'  # 45 minutos e 30 segundos
'tempo_total': '40:00:00'  # 40 horas
```

### Cálculo para Cursos
```python
# Curso = soma das seções
# Seção = soma das aulas
# Aula = duração do vídeo
```

---

## 8️⃣ CAMPOS ESPECIAIS

### YOUTUBER - Resumo do Episódio
- **Obrigatório:** Apenas no PRIMEIRO episódio de cada série
- **Conteúdo:** Sinopse da série completa
- **Demais episódios:** Descrição do episódio específico

```python
# Episódio 1
'resumo_episodio': '''
Bem-vindos à nossa jornada através de [Nome do Jogo]!
Nesta série, vamos explorar...
[Sinopse completa da série]
'''

# Episódios seguintes
'resumo_episodio': 'Episódio 2: Exploramos a cidade X e enfrentamos o chefe Y.'
```

### YOUTUBER - Data de Lançamento
- **Série:** NÃO tem `Data de Lançamento`
- **Episódios:** TEM `Data de Lançamento`

### YOUTUBER - Período da Série
- **Início:** Data/hora de gravação do PRIMEIRO episódio
- **Fim:** Data/hora de gravação do ÚLTIMO episódio

---

## 9️⃣ VALIDAÇÕES OBRIGATÓRIAS

### Antes de Criar Qualquer Card

```python
def validar_card(base, data):
    """Valida dados antes de criar card"""
    
    # 1. Verificar título
    if 'title' not in data:
        raise ValueError("Campo 'title' obrigatório")
    
    # 2. Verificar status válido
    status_validos = {
        'WORK': ['Não iniciado', 'Em Andamento', 'Em Revisão', 'Concluído', 'Pausado', 'Cancelado'],
        'PERSONAL': ['Não iniciado', 'Em Andamento', 'Concluído', 'Cancelado'],
        'STUDIES': ['Não Adquirido', 'Para Fazer', 'Em Revisão', 'Em Pausa', 'Em Andamento', 'Descontinuado', 'Concluido'],
        'YOUTUBER': ['Para Gravar', 'Não iniciado', 'Editado', 'Editando', 'Para Edição', 'Gravando', 'Publicado', 'Concluído']
    }
    
    if data.get('status') not in status_validos[base]:
        raise ValueError(f"Status '{data.get('status')}' inválido para base {base}")
    
    # 3. Verificar timezone
    if 'periodo' in data:
        periodo = data['periodo']
        if 'start' in periodo and isinstance(periodo['start'], str):
            if 'T' in periodo['start'] and '-03:00' not in periodo['start']:
                raise ValueError("Timezone deve ser GMT-3 (-03:00)")
    
    # 4. Verificar emoji não está no título
    if any(char in data['title'] for char in '🎓📚🎯🚀💼'):
        raise ValueError("Não use emojis no título! Use a propriedade 'emoji' para ícones")
    
    return True
```

---

## 🔟 REGRAS ESPECÍFICAS POR BASE

### BASE WORK

#### Obrigatório
- ✅ `title` - Título do projeto/tarefa
- ✅ `status` - Estado atual

#### Recomendado
- ✅ `cliente` - Sempre `Astracode` para trabalho profissional
- ✅ `projeto` - `ExpenseIQ`, `HubTravel` ou `Avulso`
- ✅ `priority` - Padrão `Normal`

#### Para Sub-itens
- ✅ `item_principal` - ID do projeto pai

---

### BASE PERSONAL

#### Obrigatório
- ✅ `title` - Título da tarefa
- ✅ `status` - Estado atual

#### Recomendado
- ✅ `atividade` - Tipo de atividade
- ✅ `periodo` - Quando fazer (será mapeado para campo `Data`)

#### Para Subtarefas
- ✅ `tarefa_principal` - ID da tarefa pai

---

### BASE STUDIES

#### Obrigatório
- ✅ `title` - Nome do curso/aula
- ✅ `status` - Estado atual

#### Recomendado
- ✅ `categorias` - Lista de tags relevantes
- ✅ `prioridade` - Padrão `Normal`
- ✅ `tempo_total` - Duração em HH:MM:SS
- ✅ `periodo` - Quando estudar

#### Para Sub-itens (Aulas/Seções)
- ✅ `parent_item` - ID do curso/seção pai

#### Regra de Horários
- **Aulas:** COM horário específico (19:00-21:00)
- **Seções/Módulos:** SEM horário (apenas datas)
- **Cursos:** SEM horário (apenas datas)

---

### BASE YOUTUBER

#### Obrigatório
- ✅ `title` - Nome da série/episódio
- ✅ `status` - Estado atual

#### Para Séries
- ✅ `periodo` - Início/fim da GRAVAÇÃO (primeiro ao último episódio)
- ❌ NÃO incluir `data_lancamento`

#### Para Episódios
- ✅ `item_principal` - ID da série
- ✅ `periodo` - Quando GRAVAR
- ✅ `data_lancamento` - Quando PUBLICAR
- ✅ `resumo_episodio` - Sinopse (obrigatório no episódio 1)

---

## 1️⃣1️⃣ PADRÕES DE NOMENCLATURA

### Títulos

#### Projetos/Cursos
```
✅ "ExpenseIQ - Implementação de Testes"
✅ "FIAP IA para Devs - Formação Completa"
✅ "The Legend of Heroes - Trails Series"
```

#### Sub-itens
```
✅ "Implementar Service X"
✅ "Aula 1: Introdução ao Conceito"
✅ "Episódio 01"
```

### Campos de Descrição
- Ser objetivo e claro
- Incluir contexto necessário
- Evitar informações redundantes

---

## 1️⃣2️⃣ REGRAS DE ESTUDOS

### Horários Fixos
- **Segunda, Quarta, Quinta, Sexta:** 19:00-21:00
- **Terça:** 19:30-21:00 (após tratamento)
- **NUNCA passar das 21:00**

### Se Aula Passa das 21:00
```python
# Lógica de overflow
if hora_fim > 21:00:
    # Mover para próximo dia útil
    proxima_data = obter_proximo_dia_util(data_atual)
    hora_inicio = 19:00  # ou 19:30 se for terça
```

### Revisões
- **15 minutos** entre aulas
- **30 minutos** entre módulos/seções
- Incluir no cálculo do `periodo`

---

## 1️⃣3️⃣ CHECKLIST PRÉ-CRIAÇÃO

Antes de executar `engine.create_card()`:

### Verificações Básicas
- [ ] Base correta identificada
- [ ] Campo `title` preenchido (sem emojis)
- [ ] Campo `emoji` definido (para ícone)
- [ ] Status válido para a base
- [ ] Timezone GMT-3 em todas as datas

### Se For Sub-item
- [ ] ID do pai conhecido
- [ ] Campo de relação correto usado
- [ ] Campo correto para a base:
  - WORK → `item_principal`
  - PERSONAL → `tarefa_principal`
  - STUDIES → `parent_item`
  - YOUTUBER → `item_principal`

### Se For STUDIES
- [ ] Horário apenas em aulas (nível mais baixo)
- [ ] Seções/Cursos sem horário
- [ ] Categorias preenchidas
- [ ] Tempo total calculado

### Se For YOUTUBER
- [ ] Série SEM `data_lancamento`
- [ ] Episódios COM `data_lancamento`
- [ ] Episódio 1 COM sinopse da série
- [ ] Período da série = gravação 1º ao último ep

---

## 1️⃣4️⃣ ERROS MAIS COMUNS

### Erro 1: Status Inválido
```
❌ {"status": "Para Fazer"}  # Em base YOUTUBER
✅ {"status": "Não iniciado"}
```

### Erro 2: Campo de Data Errado
```
❌ PERSONAL: 'Periodo': {...}  # Campo não existe
✅ PERSONAL: 'periodo': {...}  # Será mapeado para 'Data'
```

### Erro 3: Campo de Relação Errado
```
❌ STUDIES: 'item_principal': 'id'  # Campo errado
✅ STUDIES: 'parent_item': 'id'     # Campo correto
```

### Erro 4: Emoji no Título
```
❌ 'title': '🎓 Meu Curso'
✅ 'title': 'Meu Curso', 'emoji': '🎓'
```

### Erro 5: Horário em Card Errado
```
❌ Seção: '2025-10-16T19:00:00-03:00'  # Não deve ter horário
✅ Seção: '2025-10-16'                  # Apenas data
```

---

## 1️⃣5️⃣ BOAS PRÁTICAS

### 1. Sempre Validar Antes
```python
# Antes de criar
validar_card(base, data)

# Depois de criar
verificar_no_notion(card_id)
```

### 2. Usar Constantes
```python
# Definir constantes
ASTRACODE = 'Astracode'
EXPENSEIQ = 'ExpenseIQ'
STATUS_NAO_INICIADO = 'Não iniciado'
PRIORIDADE_NORMAL = 'Normal'

# Usar nas criações
card_data = {
    'title': 'Minha Tarefa',
    'status': STATUS_NAO_INICIADO,
    'cliente': ASTRACODE,
    'projeto': EXPENSEIQ,
    'priority': PRIORIDADE_NORMAL
}
```

### 3. Documentar Decisões
```python
# Comentar escolhas importantes
card_data = {
    'title': 'Implementar Feature X',
    'cliente': 'Astracode',  # Sempre Astracode para trabalho profissional
    'priority': 'Alta',       # Alta pois é bloqueante
    'periodo': {...}          # Agendado para amanhã
}
```

### 4. Buscar URL Correto
```python
import requests

def get_notion_url(card_id, token):
    """Retorna URL oficial do Notion"""
    url = f'https://api.notion.com/v1/pages/{card_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('url', f'https://www.notion.so/{card_id}')
    return f'https://www.notion.so/{card_id}'
```

---

## 📝 TEMPLATE COMPLETO

### Card Completo de Exemplo (WORK)
```python
card_data = {
    # Obrigatório
    'title': 'Implementar Feature X',
    'emoji': '🚀',  # Ícone da página
    'status': 'Não iniciado',
    
    # Recomendado
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'priority': 'Normal',
    
    # Opcional
    'periodo': {
        'start': '2025-10-16T09:00:00-03:00',
        'end': '2025-10-16T17:00:00-03:00'
    },
    
    # Se for sub-item
    'item_principal': 'ID_DO_PROJETO_PAI'
}

# Criar
card_id = engine.create_card('WORK', card_data)
```

---

## ✅ VALIDAÇÃO FINAL

### Como Verificar se Card Foi Criado Corretamente

1. **Abrir URL no Notion**
2. **Verificar:**
   - [ ] Ícone aparece na página (não no título)
   - [ ] Título está limpo (sem emojis)
   - [ ] Status está correto
   - [ ] Se for sub-item, vínculo aparece
   - [ ] Propriedades preenchidas corretamente
   - [ ] Timezone GMT-3 nas datas

---

**Próximo:** Leia `03_NOTION_ENGINE_GUIA.md` para aprender a usar o motor de criação














