# 🔧 Guia Completo - NotionEngine

**Data:** 11/10/2025  
**Versão:** 1.0  
**Arquivo:** `/home/user/Projetos/Automações/notion-automations/notion-automation-scripts/core/notion_engine.py`

---

## 🎯 O QUE É O NOTIONENGINE

O `NotionEngine` é um **motor centralizado** para criar cards no Notion de forma simples e padronizada.

### Principais Vantagens
- ✅ Recebe JSONs simples
- ✅ Adapta automaticamente para cada base
- ✅ Garante campos corretos
- ✅ Valida propriedades
- ✅ Simplifica criação de sub-itens

---

## 📦 INSTALAÇÃO E SETUP

### 1. Importar
```python
import sys
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importar motor
from core.notion_engine import NotionEngine
```

### 2. Inicializar
```python
TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
engine = NotionEngine(TOKEN)
```

### 3. Usar
```python
card_id = engine.create_card('WORK', {
    'title': 'Minha Tarefa',
    'status': 'Não iniciado'
})

print(f'Card criado: {card_id}')
```

---

## 🔨 MÉTODOS DISPONÍVEIS

### 1. create_card()

**Assinatura:**
```python
def create_card(self, base: str, data: Dict[str, Any]) -> Optional[str]
```

**Parâmetros:**
- `base` (str): `'WORK'`, `'PERSONAL'`, `'STUDIES'` ou `'YOUTUBER'`
- `data` (dict): Dados do card em formato simplificado

**Retorna:**
- `str`: ID do card criado
- `None`: Se houver erro

**Exemplo:**
```python
card_id = engine.create_card('WORK', {
    'title': 'Implementar Feature',
    'status': 'Não iniciado',
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'priority': 'Alta'
})

if card_id:
    print(f'✅ Card criado: {card_id}')
else:
    print('❌ Erro ao criar card')
```

---

### 2. create_subitems_only()

**Assinatura:**
```python
def create_subitems_only(self, base: str, parent_id: str, 
                        subitems: List[Dict[str, Any]]) -> Dict[str, Any]
```

**Parâmetros:**
- `base` (str): Base de destino
- `parent_id` (str): ID do card pai
- `subitems` (list): Lista de dicts com dados dos sub-itens

**Retorna:**
```python
{
    'created': int,  # Quantidade criada
    'failed': int,   # Quantidade com erro
    'ids': List[str] # IDs dos cards criados
}
```

**Exemplo:**
```python
result = engine.create_subitems_only('WORK', projeto_id, [
    {
        'title': 'Sub-item 1',
        'status': 'Não iniciado',
        'cliente': 'Astracode',
        'projeto': 'ExpenseIQ'
    },
    {
        'title': 'Sub-item 2',
        'status': 'Não iniciado',
        'cliente': 'Astracode',
        'projeto': 'ExpenseIQ'
    }
])

print(f'✅ Criados: {result["created"]}')
print(f'❌ Falhas: {result["failed"]}')
print(f'📋 IDs: {result["ids"]}')
```

---

## 📋 FORMATO DE DADOS POR BASE

### BASE WORK

```python
card_data = {
    # Obrigatório
    'title': str,           # Título do card
    'status': str,          # Status válido da base
    
    # Recomendado
    'emoji': str,           # Emoji para ícone (ex: '🚀')
    'cliente': str,         # 'Astracode', 'Pessoal', 'FIAP'
    'projeto': str,         # 'ExpenseIQ', 'HubTravel', 'Avulso'
    'priority': str,        # 'Baixa', 'Normal', 'Média', 'Alta', 'Urgente'
    
    # Opcional
    'periodo': dict,        # {'start': '...', 'end': '...'}
    'item_principal': str,  # ID do card pai (para sub-itens)
}
```

---

### BASE PERSONAL

```python
card_data = {
    # Obrigatório
    'title': str,              # Título da tarefa
    'status': str,             # Status válido
    
    # Recomendado
    'emoji': str,              # Emoji para ícone
    'atividade': str,          # 'Desenvolvimento', 'Organização', etc
    
    # Opcional
    'periodo': dict,           # {'start': '...', 'end': '...'} → vai para campo 'Data'
    'description': str,        # Descrição detalhada
    'tarefa_principal': str,   # ID da tarefa pai (para subtarefas)
}
```

---

### BASE STUDIES

```python
card_data = {
    # Obrigatório
    'title': str,           # Nome do curso/aula
    'status': str,          # Status válido
    
    # Recomendado
    'emoji': str,           # Emoji para ícone
    'categorias': list,     # ['FIAP', 'IA', 'Cursos']
    'prioridade': str,      # 'Normal', 'Alta', etc
    'tempo_total': str,     # 'HH:MM:SS'
    
    # Opcional
    'periodo': dict,        # {'start': '...', 'end': '...'}
    'description': str,     # Descrição do conteúdo
    'parent_item': str,     # ID do curso/seção pai
}
```

**Importante:** 
- Aulas (nível mais baixo): `periodo` COM horário
- Seções/Módulos: `periodo` SEM horário
- Cursos: `periodo` SEM horário

---

### BASE YOUTUBER

```python
# Para SÉRIE
serie_data = {
    'title': str,           # Nome da série
    'status': str,          # Status válido
    'emoji': str,           # Emoji para ícone
    'periodo': dict,        # Gravação 1º ao último ep
    # NÃO incluir 'data_lancamento'
}

# Para EPISÓDIO
episodio_data = {
    'title': str,              # 'Episódio 01', 'Episódio 02', etc
    'status': str,             # Status válido
    'emoji': str,              # Emoji para ícone
    'item_principal': str,     # ID da série
    'periodo': dict,           # Quando GRAVAR
    'data_lancamento': str,    # Quando PUBLICAR
    'resumo_episodio': str,    # Sinopse (obrigatório no ep 1)
}
```

---

## 🔄 MAPEAMENTO AUTOMÁTICO

O NotionEngine **mapeia automaticamente** campos simplificados para os campos reais do Notion:

### Mapeamentos WORK
```python
# Você passa:
'title' → 'Nome do projeto'
'status' → 'Status'
'cliente' → 'Cliente'
'projeto' → 'Projeto'
'priority' → 'Prioridade'
'periodo' → 'Periodo'
'item_principal' → 'item principal'
```

### Mapeamentos PERSONAL
```python
# Você passa:
'title' → 'Nome da tarefa'
'status' → 'Status'
'atividade' → 'Atividade'
'periodo' → 'Data'  # ← Mapeamento especial
'description' → 'Descrição'
'tarefa_principal' → 'tarefa principal'
```

### Mapeamentos STUDIES
```python
# Você passa:
'title' → 'Project name'
'status' → 'Status'
'categorias' → 'Categorias'
'prioridade' → 'Prioridade'
'tempo_total' → 'Tempo Total'
'periodo' → 'Período'  # ← Com acento
'parent_item' → 'Parent item'
```

### Mapeamentos YOUTUBER
```python
# Você passa:
'title' → 'Nome do projeto'
'status' → 'Status'
'periodo' → 'Periodo'
'data_lancamento' → 'Data de Lançamento'
'resumo_episodio' → 'Resumo do Episodio'
'item_principal' → 'item principal'
```

---

## 💡 EXEMPLOS PRÁTICOS

### Criar Projeto com Sub-itens (WORK)

```python
from core.notion_engine import NotionEngine

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
engine = NotionEngine(TOKEN)

# 1. Criar projeto principal
projeto_id = engine.create_card('WORK', {
    'title': 'Implementar Dashboard',
    'emoji': '📊',
    'status': 'Não iniciado',
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'priority': 'Alta',
    'periodo': {
        'start': '2025-10-16T09:00:00-03:00',
        'end': '2025-10-16T17:00:00-03:00'
    }
})

print(f'✅ Projeto criado: {projeto_id}')

# 2. Criar sub-itens
subitems_data = [
    {
        'title': 'Criar componentes React',
        'emoji': '⚛️',
        'status': 'Não iniciado',
        'cliente': 'Astracode',
        'projeto': 'ExpenseIQ',
        'priority': 'Alta',
        'periodo': {
            'start': '2025-10-16T09:00:00-03:00',
            'end': '2025-10-16T12:00:00-03:00'
        }
    },
    {
        'title': 'Integrar com API',
        'emoji': '🔌',
        'status': 'Não iniciado',
        'cliente': 'Astracode',
        'projeto': 'ExpenseIQ',
        'priority': 'Alta',
        'periodo': {
            'start': '2025-10-16T13:00:00-03:00',
            'end': '2025-10-16T17:00:00-03:00'
        }
    }
]

result = engine.create_subitems_only('WORK', projeto_id, subitems_data)

print(f'✅ Sub-itens criados: {result["created"]}/{len(subitems_data)}')
for card_id in result['ids']:
    print(f'   - https://www.notion.so/{card_id}')
```

---

### Criar Curso com Estrutura (STUDIES)

```python
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
engine = NotionEngine(TOKEN)
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

# 1. Criar curso principal (SEM horário)
curso_id = engine.create_card('STUDIES', {
    'title': 'Python Avançado',
    'emoji': '🐍',
    'status': 'Para Fazer',
    'categorias': ['Cursos', 'Python', 'Programação'],
    'prioridade': 'Normal',
    'tempo_total': '20:00:00',
    'periodo': {
        'start': '2025-10-16',  # SEM horário
        'end': '2025-11-15'
    }
})

# 2. Criar seção (SEM horário)
secao_id = engine.create_card('STUDIES', {
    'title': 'Seção 1: Fundamentos Avançados',
    'emoji': '📑',
    'status': 'Para Fazer',
    'categorias': ['Python', 'Fundamentos'],
    'prioridade': 'Normal',
    'tempo_total': '04:00:00',
    'parent_item': curso_id,  # ← Vínculo
    'periodo': {
        'start': '2025-10-16',  # SEM horário
        'end': '2025-10-22'
    }
})

# 3. Criar aulas (COM horário)
base_date = datetime(2025, 10, 16, tzinfo=SAO_PAULO_TZ)

aulas = []
for i in range(3):
    aula_date = base_date + timedelta(days=i*2)  # Aulas a cada 2 dias
    
    aula_id = engine.create_card('STUDIES', {
        'title': f'Aula {i+1}: Decorators e Generators',
        'emoji': '🎯',
        'status': 'Para Fazer',
        'categorias': ['Python', 'Avançado', 'Programação'],
        'prioridade': 'Normal',
        'tempo_total': '01:20:00',
        'parent_item': secao_id,  # ← Vínculo
        'periodo': {
            'start': aula_date.replace(hour=19, minute=0).isoformat(),  # COM horário
            'end': aula_date.replace(hour=21, minute=0).isoformat()
        }
    })
    
    aulas.append(aula_id)
    print(f'✅ Aula {i+1} criada: {aula_id}')
```

---

### Criar Série YouTube com Episódios

```python
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
engine = NotionEngine(TOKEN)
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

# 1. Criar série principal
base_date = datetime(2025, 10, 16, tzinfo=SAO_PAULO_TZ)

# Calcular período da série
primeiro_ep_gravacao = base_date.replace(hour=21, minute=0)
ultimo_ep_gravacao = (base_date + timedelta(days=19)).replace(hour=23, minute=30)

serie_id = engine.create_card('YOUTUBER', {
    'title': 'Final Fantasy XVI',
    'emoji': '🎮',
    'status': 'Não iniciado',
    'periodo': {
        'start': primeiro_ep_gravacao.isoformat(),
        'end': ultimo_ep_gravacao.isoformat()
    }
    # SEM data_lancamento
})

print(f'✅ Série criada: {serie_id}')

# 2. Criar episódios
sinopse = '''
Bem-vindos à nossa jornada épica através de Valisthea!
Nesta série de Final Fantasy XVI, exploraremos...
'''

episodios = []

for i in range(1, 6):  # 5 episódios
    ep_date = base_date + timedelta(days=i-1)
    
    # Gravação: 21:00-23:30
    gravacao_inicio = ep_date.replace(hour=21, minute=0)
    gravacao_fim = ep_date.replace(hour=23, minute=30)
    
    # Lançamento: 12:00 do dia seguinte
    lancamento = (ep_date + timedelta(days=1)).replace(hour=12, minute=0)
    
    ep_id = engine.create_card('YOUTUBER', {
        'title': f'Episódio {i:02d}',
        'emoji': '📺',
        'status': 'Não iniciado',
        'item_principal': serie_id,  # ← Vínculo
        'periodo': {
            'start': gravacao_inicio.isoformat(),
            'end': gravacao_fim.isoformat()
        },
        'data_lancamento': lancamento.isoformat(),
        'resumo_episodio': sinopse if i == 1 else f'Episódio {i} da nossa aventura em Valisthea!'
    })
    
    episodios.append(ep_id)
    print(f'✅ Episódio {i:02d} criado: {ep_id}')
```

---

## 🔍 COMO FUNCIONA INTERNAMENTE

### Fluxo de Criação

```
1. Você chama: engine.create_card('WORK', data)
   ↓
2. NotionEngine valida a base
   ↓
3. Chama: _build_payload(base, data)
   ↓
4. Adapta data simples para payload Notion correto
   ↓
5. Faz POST para API Notion
   ↓
6. Retorna ID do card criado (ou None)
```

### Método _build_payload()

Este método é **interno** e adapta seus dados simples para o formato complexo da API Notion.

**Exemplo de transformação:**

```python
# Você passa:
{
    'title': 'Minha Tarefa',
    'status': 'Não iniciado',
    'priority': 'Alta'
}

# NotionEngine transforma em:
{
    "parent": {"database_id": "XXXXXXXX-XXXX-XXXX-XXXX-WORK_DB_ID"},
    "icon": {"emoji": "..."},
    "properties": {
        "Nome do projeto": {
            "title": [{"text": {"content": "Minha Tarefa"}}]
        },
        "Status": {
            "status": {"name": "Não iniciado"}
        },
        "Prioridade": {
            "select": {"name": "Alta"}
        }
    }
}
```

**Você não precisa se preocupar com isso!** O motor cuida automaticamente.

---

## ⚙️ CONFIGURAÇÕES DO MOTOR

### Bases Configuradas

```python
BASES = {
    'WORK': {
        'id': 'XXXXXXXX-XXXX-XXXX-XXXX-WORK_DB_ID',
        'title_field': 'Nome do projeto',
        'relation_field': 'Sprint'
    },
    'PERSONAL': {
        'id': 'XXXXXXXX-XXXX-XXXX-XXXX-PERSONAL_DB_ID',
        'title_field': 'Nome da tarefa',
        'relation_field': 'Subtarefa'
    },
    'STUDIES': {
        'id': 'XXXXXXXX-XXXX-XXXX-XXXX-STUDIES_DB_ID',
        'title_field': 'Project name',
        'relation_field': 'Parent item'
    },
    'YOUTUBER': {
        'id': 'XXXXXXXX-XXXX-XXXX-XXXX-YOUTUBER_DB_ID',
        'title_field': 'Nome do projeto',
        'relation_field': 'item principal'
    }
}
```

### Headers API
```python
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}
```

---

## 🐛 TRATAMENTO DE ERROS

### Retorno em Caso de Erro

```python
card_id = engine.create_card('WORK', data)

if card_id is None:
    # Houve um erro
    print('❌ Falha ao criar card')
    # Verificar logs ou debug
else:
    # Sucesso
    print(f'✅ Card criado: {card_id}')
```

### Erros Comuns

#### Status Inválido
```
Erro API: Invalid status option. Status option "Para Fazer" does not exist
```
**Solução:** Verificar status válidos da base em `05_STATUS_E_PROPRIEDADES.md`

#### Campo Não Existe
```
Erro API: Periodo is not a property that exists.
```
**Solução:** Verificar nome correto do campo para a base

#### Timezone Errado
```
Erro: Data sem timezone GMT-3
```
**Solução:** Sempre usar `-03:00` no final das datas

---

## 🎯 BOAS PRÁTICAS

### 1. Sempre Use Emoji
```python
# Sempre incluir emoji para visual melhor
card_data = {
    'title': 'Minha Tarefa',
    'emoji': '✅',  # ← Adicione sempre
    'status': 'Não iniciado'
}
```

### 2. Verifique ID Retornado
```python
card_id = engine.create_card('WORK', data)

if not card_id:
    print('❌ Erro ao criar card')
    return None

# Prosseguir apenas se criou com sucesso
print(f'✅ Card criado: {card_id}')
```

### 3. Use Constantes
```python
# Definir no início do script
TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
ASTRACODE = 'Astracode'
EXPENSEIQ = 'ExpenseIQ'

# Usar nas criações
card_data = {
    'cliente': ASTRACODE,
    'projeto': EXPENSEIQ
}
```

### 4. Busque URL Oficial
```python
import requests

def get_official_url(card_id, token):
    """Retorna URL oficial do Notion"""
    url = f'https://api.notion.com/v1/pages/{card_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('url')
    return f'https://www.notion.so/{card_id}'

# Usar
notion_url = get_official_url(card_id, TOKEN)
print(f'🔗 Link: {notion_url}')
```

---

## 🧪 TESTANDO O MOTOR

### Script de Teste Básico

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
engine = NotionEngine(TOKEN)

print('🧪 Testando NotionEngine...')

# Testar cada base
bases_test = {
    'WORK': {
        'title': 'Teste WORK',
        'emoji': '🧪',
        'status': 'Não iniciado',
        'cliente': 'Astracode',
        'projeto': 'Avulso',
        'priority': 'Normal'
    },
    'PERSONAL': {
        'title': 'Teste PERSONAL',
        'emoji': '🧪',
        'status': 'Não iniciado',
        'atividade': 'Teste'
    },
    'STUDIES': {
        'title': 'Teste STUDIES',
        'emoji': '🧪',
        'status': 'Para Fazer',
        'categorias': ['Teste'],
        'prioridade': 'Normal'
    },
    'YOUTUBER': {
        'title': 'Teste YOUTUBER',
        'emoji': '🧪',
        'status': 'Não iniciado'
    }
}

created_ids = {}

for base, data in bases_test.items():
    card_id = engine.create_card(base, data)
    if card_id:
        created_ids[base] = card_id
        print(f'✅ {base}: {card_id}')
    else:
        print(f'❌ {base}: Falha')

print(f'\n✅ Teste concluído: {len(created_ids)}/4 bases')
```

---

## 📊 PERFORMANCE

### Tempo Médio por Operação
- **create_card():** ~0.5-1 segundo
- **create_subitems_only():** ~0.5-1 segundo por item

### Limitações da API
- **Rate limit:** ~3 requests/segundo
- **Timeout:** 30 segundos configurado
- **Recomendação:** Adicionar delay entre criações massivas

```python
import time

# Para criações em massa
for item_data in items:
    card_id = engine.create_card('WORK', item_data)
    time.sleep(0.5)  # Evitar rate limit
```

---

## 🔒 SEGURANÇA

### Token
- **NUNCA** commitar o token
- **SEMPRE** usar variável de ambiente ou arquivo `.env`
- **NÃO** compartilhar o token

### Boas Práticas
```python
import os
from dotenv import load_dotenv

# Carregar do .env
load_dotenv()
TOKEN = os.getenv('NOTION_TOKEN')

# Verificar se existe
if not TOKEN:
    raise ValueError('NOTION_TOKEN não encontrado no .env')

# Usar
engine = NotionEngine(TOKEN)
```

---

## ✅ CHECKLIST DE USO

Antes de usar o NotionEngine:

- [ ] Token configurado
- [ ] Motor importado corretamente
- [ ] Base identificada (`WORK`, `PERSONAL`, `STUDIES`, `YOUTUBER`)
- [ ] Dados validados (status, campos, timezone)
- [ ] Emoji definido (não no título)
- [ ] Se sub-item, ID do pai conhecido

Após criar card:

- [ ] Verificar se `card_id` não é `None`
- [ ] Buscar URL oficial do Notion
- [ ] Validar card criado abrindo URL
- [ ] Verificar vínculos se for sub-item

---

**Próximo:** Leia `04_EXEMPLOS_PRATICOS.md` para ver exemplos completos de uso real














