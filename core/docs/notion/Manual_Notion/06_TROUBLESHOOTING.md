# 🐛 Troubleshooting - Erros Comuns e Soluções

**Data:** 11/10/2025  
**Versão:** 1.0  
**Status:** Baseado em erros reais encontrados e corrigidos

---

## 🎯 OBJETIVO

Este guia lista **todos os erros comuns** que podem ocorrer ao criar cards no Notion e suas soluções.

Todos os erros aqui foram **encontrados e resolvidos** durante os testes.

---

## ❌ ERRO 1: Status Inválido

### Mensagem de Erro
```
Invalid status option. Status option "Para Fazer" does not exist
```

### Causa
Você tentou usar um status que não existe naquela base específica.

### Exemplo do Erro
```python
# ❌ ERRADO - Base YOUTUBER
engine.create_card('YOUTUBER', {
    'title': 'Minha Série',
    'status': 'Para Fazer'  # ← Este status não existe em YOUTUBER
})
```

### Solução
Verificar status válidos da base em `05_STATUS_E_PROPRIEDADES.md`

```python
# ✅ CORRETO - Base YOUTUBER
engine.create_card('YOUTUBER', {
    'title': 'Minha Série',
    'status': 'Não iniciado'  # ← Status válido
})
```

### Status Válidos por Base
- **WORK:** `Não iniciado`, `Em Andamento`, `Em Revisão`, `Concluído`, `Pausado`, `Cancelado`
- **PERSONAL:** `Não iniciado`, `Em Andamento`, `Concluído`, `Cancelado`
- **STUDIES:** `Não Adquirido`, `Para Fazer`, `Em Revisão`, `Em Pausa`, `Em Andamento`, `Descontinuado`, `Concluido`
- **YOUTUBER:** `Para Gravar`, `Não iniciado`, `Editado`, `Editando`, `Para Edição`, `Gravando`, `Publicado`, `Concluído`

---

## ❌ ERRO 2: Campo de Propriedade Não Existe

### Mensagem de Erro
```
Periodo is not a property that exists.
```

### Causa
O nome do campo está errado ou a base não tem essa propriedade.

### Exemplo do Erro
```python
# ❌ ERRADO - Base PERSONAL
engine.create_card('PERSONAL', {
    'title': 'Minha Tarefa',
    'periodo': {...}  # ← Campo 'Periodo' não existe em PERSONAL
})
```

### Solução
Verificar nome correto do campo para cada base:

```python
# ✅ CORRETO - Base PERSONAL
engine.create_card('PERSONAL', {
    'title': 'Minha Tarefa',
    'periodo': {...}  # ← NotionEngine mapeia para 'Data' automaticamente
})
```

### Campos de Data por Base
- **WORK:** `Periodo` (sem acento)
- **PERSONAL:** `Data` (NotionEngine mapeia `periodo` → `Data`)
- **STUDIES:** `Período` (com acento)
- **YOUTUBER:** `Periodo` (sem acento)

---

## ❌ ERRO 3: Campo de Relação Errado

### Mensagem de Erro
```
item principal is not a property that exists.
```

### Causa
Você usou o campo de relação errado para aquela base.

### Exemplo do Erro
```python
# ❌ ERRADO - Base STUDIES
engine.create_card('STUDIES', {
    'title': 'Aula 1',
    'item_principal': 'id-do-curso'  # ← Campo errado
})
```

### Solução
Usar campo correto para cada base:

```python
# ✅ CORRETO - Base STUDIES
engine.create_card('STUDIES', {
    'title': 'Aula 1',
    'parent_item': 'id-do-curso'  # ← Campo correto
})
```

### Campos de Relação por Base
- **WORK:** `item_principal` (para sub-itens)
- **PERSONAL:** `tarefa_principal` (para subtarefas)
- **STUDIES:** `parent_item` (para aulas/seções)
- **YOUTUBER:** `item_principal` (para episódios)

---

## ❌ ERRO 4: Timezone Incorreto

### Mensagem de Erro
```
Data não está em GMT-3
```

### Causa
Você usou UTC ou outro timezone em vez de GMT-3.

### Exemplo do Erro
```python
# ❌ ERRADO
'periodo': {
    'start': '2025-10-16T19:00:00Z'  # ← UTC (Z no final)
}
```

### Solução
**SEMPRE** usar GMT-3 com `-03:00`:

```python
# ✅ CORRETO
from datetime import datetime, timezone, timedelta

SAO_PAULO_TZ = timezone(timedelta(hours=-3))
dt = datetime(2025, 10, 16, 19, 0, 0, tzinfo=SAO_PAULO_TZ)

'periodo': {
    'start': dt.isoformat()  # '2025-10-16T19:00:00-03:00'
}
```

---

## ❌ ERRO 5: Emoji no Título

### Mensagem de Erro
```
Título contém emojis (não permitido)
```

### Causa
Você colocou emoji no título em vez de usar como ícone.

### Exemplo do Erro
```python
# ❌ ERRADO
engine.create_card('WORK', {
    'title': '🚀 Meu Projeto'  # ← Emoji no título
})
```

### Solução
Usar emoji na propriedade `emoji`:

```python
# ✅ CORRETO
engine.create_card('WORK', {
    'title': 'Meu Projeto',  # ← Sem emoji
    'emoji': '🚀'             # ← Emoji aqui
})
```

---

## ❌ ERRO 6: Sub-item Sem Vínculo

### Sintoma
Sub-item criado mas não aparece linkado ao pai.

### Causa
Você não preencheu o campo de relação.

### Exemplo do Erro
```python
# ❌ ERRADO - Sub-item sem vínculo
engine.create_card('WORK', {
    'title': 'Sub-item',
    'status': 'Não iniciado'
    # SEM 'item_principal'
})
```

### Solução
Sempre preencher campo de relação para sub-itens:

```python
# ✅ CORRETO - Sub-item com vínculo
projeto_id = engine.create_card('WORK', {
    'title': 'Projeto Principal',
    'status': 'Não iniciado'
})

subitem_id = engine.create_card('WORK', {
    'title': 'Sub-item',
    'status': 'Não iniciado',
    'item_principal': projeto_id  # ← Vínculo com o pai
})
```

---

## ❌ ERRO 7: Horário em Card Errado

### Sintoma
Erro ao criar seção de curso com horário.

### Causa
Seções/Módulos não devem ter horário, apenas aulas.

### Exemplo do Erro
```python
# ❌ ERRADO - Seção com horário
engine.create_card('STUDIES', {
    'title': 'Módulo 1',
    'periodo': {
        'start': '2025-10-16T19:00:00-03:00',  # ← Não deve ter horário
        'end': '2025-10-30T21:00:00-03:00'
    }
})
```

### Solução
Seções/Módulos/Cursos SEM horário, apenas Aulas COM horário:

```python
# ✅ CORRETO - Seção sem horário
engine.create_card('STUDIES', {
    'title': 'Módulo 1',
    'periodo': {
        'start': '2025-10-16',  # ← Apenas data
        'end': '2025-10-30'
    }
})

# ✅ CORRETO - Aula com horário
engine.create_card('STUDIES', {
    'title': 'Aula 1',
    'parent_item': modulo_id,
    'periodo': {
        'start': '2025-10-16T19:00:00-03:00',  # ← COM horário
        'end': '2025-10-16T21:00:00-03:00'
    }
})
```

---

## ❌ ERRO 8: ID do Pai Inválido

### Mensagem de Erro
```
404: Page not found
```

### Causa
O ID do card pai está errado ou o card não existe.

### Exemplo do Erro
```python
# ❌ ERRADO - ID inválido
engine.create_card('WORK', {
    'title': 'Sub-item',
    'item_principal': 'id-inventado-123'  # ← ID não existe
})
```

### Solução
Sempre verificar que o ID do pai é válido:

```python
# ✅ CORRETO - Verificar antes de usar
projeto_id = engine.create_card('WORK', {
    'title': 'Projeto Principal',
    'status': 'Não iniciado'
})

if projeto_id:  # ← Verifica se foi criado
    subitem_id = engine.create_card('WORK', {
        'title': 'Sub-item',
        'item_principal': projeto_id  # ← Usa ID válido
    })
else:
    print('❌ Erro ao criar projeto pai')
```

---

## ❌ ERRO 9: Data de Lançamento em Série

### Sintoma
Série criada mas com campo errado.

### Causa
Série não deve ter `Data de Lançamento`, apenas `Periodo`.

### Exemplo do Erro
```python
# ❌ ERRADO - Série com Data de Lançamento
engine.create_card('YOUTUBER', {
    'title': 'Minha Série',
    'status': 'Não iniciado',
    'periodo': {...},
    'data_lancamento': '2025-10-16T12:00:00-03:00'  # ← Não deve ter
})
```

### Solução
Série SEM `data_lancamento`, apenas episódios:

```python
# ✅ CORRETO - Série sem Data de Lançamento
engine.create_card('YOUTUBER', {
    'title': 'Minha Série',
    'status': 'Não iniciado',
    'periodo': {
        'start': '2025-10-16T21:00:00-03:00',  # Gravação 1º ep
        'end': '2025-11-04T23:30:00-03:00'      # Gravação último ep
    }
    # SEM 'data_lancamento'
})

# ✅ CORRETO - Episódio com Data de Lançamento
engine.create_card('YOUTUBER', {
    'title': 'Episódio 01',
    'status': 'Não iniciado',
    'item_principal': serie_id,
    'periodo': {...},                                    # Quando gravar
    'data_lancamento': '2025-10-17T12:00:00-03:00'  # Quando publicar
})
```

---

## ❌ ERRO 10: Sinopse Faltando

### Sintoma
Primeiro episódio sem sinopse.

### Causa
Esqueceu de adicionar sinopse no primeiro episódio da série.

### Exemplo do Erro
```python
# ❌ ERRADO - Primeiro episódio sem sinopse
engine.create_card('YOUTUBER', {
    'title': 'Episódio 01',
    'item_principal': serie_id
    # SEM 'resumo_episodio'
})
```

### Solução
SEMPRE adicionar sinopse no primeiro episódio:

```python
# ✅ CORRETO - Primeiro episódio com sinopse
engine.create_card('YOUTUBER', {
    'title': 'Episódio 01',
    'item_principal': serie_id,
    'resumo_episodio': '''
    Bem-vindos à nossa jornada através de [Jogo]!
    Nesta série, vamos explorar...
    '''
})
```

---

## ❌ ERRO 11: Cliente/Projeto Errado (WORK)

### Sintoma
Card criado mas com cliente/projeto incorreto.

### Causa
Não seguiu o padrão: Astracode + ExpenseIQ/HubTravel.

### Exemplo do Erro
```python
# ❌ ERRADO - Cliente e projeto genéricos
engine.create_card('WORK', {
    'title': 'Tarefa ExpenseIQ',
    'cliente': 'Pessoal',     # ← Deveria ser Astracode
    'projeto': 'Automação'    # ← Deveria ser ExpenseIQ
})
```

### Solução
Sempre usar cliente e projeto corretos:

```python
# ✅ CORRETO - Cliente e projeto adequados
engine.create_card('WORK', {
    'title': 'Tarefa ExpenseIQ',
    'cliente': 'Astracode',   # ← Correto para trabalho profissional
    'projeto': 'ExpenseIQ'    # ← Correto para agente ExpenseIQ
})
```

### Regra
- **Agente ExpenseIQ:** SEMPRE `cliente: 'Astracode'`, `projeto: 'ExpenseIQ'`
- **Agente HubTravel:** SEMPRE `cliente: 'Astracode'`, `projeto: 'HubTravel'`
- **Trabalho genérico:** `cliente: 'Astracode'`, `projeto: 'Avulso'`

---

## ❌ ERRO 12: Prioridade Errada

### Sintoma
Prioridade padrão errada.

### Causa
Usou `Média` em vez de `Normal`.

### Exemplo do Erro
```python
# ❌ ERRADO - Prioridade Média como padrão
engine.create_card('WORK', {
    'title': 'Tarefa',
    'priority': 'Média'  # ← Padrão deve ser Normal
})
```

### Solução
Prioridade padrão é **Normal**:

```python
# ✅ CORRETO - Prioridade Normal
engine.create_card('WORK', {
    'title': 'Tarefa',
    'priority': 'Normal'  # ← Padrão correto
})

# Ou deixar vazio (motor usa Normal)
engine.create_card('WORK', {
    'title': 'Tarefa'
    # Motor vai usar 'Normal' automaticamente
})
```

---

## ❌ ERRO 13: Ícone Não Aparece

### Sintoma
Card criado mas sem ícone na página.

### Causa
Emoji foi passado mas não aplicado corretamente.

### Exemplo do Erro
```python
# ❌ ERRADO - Emoji no título
engine.create_card('WORK', {
    'title': '🚀 Meu Projeto'  # ← Emoji no lugar errado
})
```

### Solução
Usar propriedade `emoji` e adicionar ícone depois se necessário:

```python
# ✅ CORRETO - Emoji separado
card_id = engine.create_card('WORK', {
    'title': 'Meu Projeto',  # ← Título limpo
    'emoji': '🚀'             # ← Emoji aqui
})

# Se o ícone não aparecer, adicionar manualmente:
import requests

url = f'https://api.notion.com/v1/pages/{card_id}'
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}
data = {'icon': {'emoji': '🚀'}}

response = requests.patch(url, headers=headers, json=data)
```

---

## ❌ ERRO 14: Link do Notion Não Funciona

### Sintoma
Link `https://notion.so/EXAMPLE_CARD_ID_1234567890` não abre.

### Causa
Formato do link está errado (com hífens).

### Exemplo do Erro
```python
# ❌ ERRADO - Link com hífens
link = f'https://notion.so/{card_id}'  # Com hífens
# Resultado: https://notion.so/EXAMPLE_CARD_ID_1234567890
```

### Solução
Buscar URL oficial da API:

```python
# ✅ CORRETO - Buscar URL oficial
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

# Usar
notion_url = get_notion_url(card_id, TOKEN)
# Resultado: https://www.notion.so/Meu-Projeto-288962a7693c812ebb43d015c7e44971
```

---

## ❌ ERRO 15: NotionEngine Não Encontrado

### Mensagem de Erro
```
ModuleNotFoundError: No module named 'core.notion_engine'
```

### Causa
Path não configurado corretamente.

### Exemplo do Erro
```python
# ❌ ERRADO - Sem configurar path
from core.notion_engine import NotionEngine  # ← Não encontra
```

### Solução
Adicionar path antes de importar:

```python
# ✅ CORRETO - Configurar path primeiro
import sys
from pathlib import Path

# Adicionar parent do script ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Agora importa corretamente
from core.notion_engine import NotionEngine
```

---

## ❌ ERRO 16: Token Inválido

### Mensagem de Erro
```
401: Unauthorized
```

### Causa
Token do Notion inválido ou expirado.

### Solução
```python
# Verificar token
TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'

# Testar conexão
import requests

url = 'https://api.notion.com/v1/users/me'
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print('✅ Token válido')
else:
    print(f'❌ Token inválido: {response.status_code}')
```

---

## ❌ ERRO 17: Categorias Vazias (STUDIES)

### Sintoma
Card criado mas sem categorias.

### Causa
Passou lista vazia ou não passou categorias.

### Exemplo do Erro
```python
# ❌ ERRADO - Sem categorias
engine.create_card('STUDIES', {
    'title': 'Meu Curso',
    'categorias': []  # ← Lista vazia
})
```

### Solução
Sempre incluir categorias relevantes:

```python
# ✅ CORRETO - Com categorias
engine.create_card('STUDIES', {
    'title': 'Meu Curso',
    'categorias': ['FIAP', 'Inteligência Artificial', 'Cursos']
})
```

---

## ❌ ERRO 18: Período da Série Errado (YOUTUBER)

### Sintoma
Período da série não corresponde aos episódios.

### Causa
Período da série deve ir do início da gravação do 1º ao fim da gravação do último episódio.

### Exemplo do Erro
```python
# ❌ ERRADO - Período arbitrário
engine.create_card('YOUTUBER', {
    'title': 'Minha Série',
    'periodo': {
        'start': '2025-10-16T00:00:00-03:00',  # ← Horário errado
        'end': '2025-11-04T23:59:59-03:00'
    }
})
```

### Solução
Calcular período correto baseado nos episódios:

```python
# ✅ CORRETO - Período calculado
from datetime import datetime, timezone, timedelta

SAO_PAULO_TZ = timezone(timedelta(hours=-3))
base_date = datetime(2025, 10, 16, tzinfo=SAO_PAULO_TZ)

# Primeiro episódio: gravação 21:00
primeiro_ep = base_date.replace(hour=21, minute=0)

# Último episódio (20º): 19 dias depois, gravação até 23:30
ultimo_ep = (base_date + timedelta(days=19)).replace(hour=23, minute=30)

engine.create_card('YOUTUBER', {
    'title': 'Minha Série',
    'periodo': {
        'start': primeiro_ep.isoformat(),  # Início 1º ep
        'end': ultimo_ep.isoformat()        # Fim último ep
    }
})
```

---

## 🔧 FERRAMENTAS DE DEBUG

### 1. Verificar se Card Existe

```python
import requests

def verificar_card(card_id, token):
    """Verifica se card existe e retorna propriedades"""
    url = f'https://api.notion.com/v1/pages/{card_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Card existe')
        print(f'   URL: {data.get("url")}')
        print(f'   Criado: {data.get("created_time")}')
        return True
    else:
        print(f'❌ Card não encontrado: {response.status_code}')
        return False

# Usar
verificar_card('EXAMPLE_CARD_ID_1234567890', TOKEN)
```

---

### 2. Verificar Vínculos de Sub-item

```python
import requests

def verificar_vinculos(card_id, token):
    """Verifica vínculos de um card"""
    url = f'https://api.notion.com/v1/pages/{card_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        props = data['properties']
        
        # Verificar campos de relação
        relation_fields = ['item principal', 'tarefa principal', 'Parent item', 'Sprint', 'Subtarefa']
        
        print(f'🔗 Vínculos do card:')
        for field in relation_fields:
            if field in props:
                relations = props[field].get('relation', [])
                if relations:
                    print(f'   ✅ {field}: {len(relations)} vínculo(s)')
                    for rel in relations:
                        print(f'      - {rel["id"]}')
                else:
                    print(f'   ⚠️  {field}: VAZIO')
    else:
        print(f'❌ Erro ao buscar card: {response.status_code}')

# Usar
verificar_vinculos('EXAMPLE_CARD_ID_0987654321', TOKEN)
```

---

### 3. Adicionar Debug ao NotionEngine

```python
# Abrir: core/notion_engine.py
# Adicionar após linha 69:

if response.status_code == 200:
    return response.json()['id']
else:
    # DEBUG - mostrar erro
    print(f'❌ Erro ao criar card {base}: {response.status_code}')
    print(f'DEBUG - Resposta: {response.text}')
return None
```

---

## 📋 CHECKLIST DE DEBUGGING

Quando algo não funcionar:

### 1. Verificar Basics
- [ ] Token correto e válido
- [ ] Base correta (`WORK`, `PERSONAL`, `STUDIES`, `YOUTUBER`)
- [ ] Campo `title` preenchido
- [ ] Import do NotionEngine funcionando

### 2. Verificar Status
- [ ] Status existe na base de destino
- [ ] Escrito exatamente como na lista (case-sensitive)
- [ ] Status padrão apropriado se não especificar

### 3. Verificar Campos
- [ ] Nomes de campos corretos para a base
- [ ] Timezone GMT-3 em todas as datas
- [ ] Emoji separado do título
- [ ] Campo de relação correto se for sub-item

### 4. Verificar Hierarquia
- [ ] ID do pai válido
- [ ] Campo de relação preenchido
- [ ] Campo correto para a base

### 5. Verificar Propriedades Especiais
- [ ] STUDIES: horário apenas em aulas
- [ ] YOUTUBER: série SEM data de lançamento
- [ ] YOUTUBER: episódio 1 COM sinopse
- [ ] PERSONAL: campo `Data` não `Periodo`

---

## 🔍 COMO INVESTIGAR ERROS

### Passo 1: Habilitar Debug
```python
# Adicionar print antes de criar
print(f'DEBUG - Criando card na base {base}')
print(f'DEBUG - Dados: {data}')

card_id = engine.create_card(base, data)

print(f'DEBUG - ID retornado: {card_id}')
```

### Passo 2: Verificar Response da API
```python
# Modificar NotionEngine temporariamente
else:
    print(f'❌ Erro: {response.status_code}')
    print(f'Resposta: {response.text}')  # ← Ver mensagem de erro
    return None
```

### Passo 3: Testar Chamada Direta
```python
import requests

# Testar criação direta na API
url = 'https://api.notion.com/v1/pages'
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

payload = {
    "parent": {"database_id": "..."},
    "properties": {
        "Nome do projeto": {
            "title": [{"text": {"content": "Teste"}}]
        }
    }
}

response = requests.post(url, headers=headers, json=payload)
print(f'Status: {response.status_code}')
print(f'Resposta: {response.text}')
```

---

## ✅ SOLUÇÕES RÁPIDAS

### Card não criado
1. Verificar retorno: `if not card_id: print('Erro')`
2. Verificar status é válido
3. Verificar token está correto

### Sub-item não vinculado
1. Verificar campo de relação está preenchido
2. Verificar nome do campo está correto
3. Verificar ID do pai é válido

### Ícone não aparece
1. Adicionar propriedade `emoji` no payload
2. Ou adicionar depois via PATCH request
3. Nunca colocar emoji no título

### Horário errado
1. Verificar timezone `-03:00`
2. Verificar formato ISO
3. Verificar se deve ter horário (aulas sim, seções não)

### Link não abre
1. Buscar URL oficial da API
2. Usar `data.get('url')` do response
3. Remover hífens do ID se necessário

---

## 📞 SCRIPT DE TESTE COMPLETO

Use este script para testar se tudo está funcionando:

```python
#!/usr/bin/env python3
"""
Script de teste e validação do NotionEngine
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'

def test_engine():
    """Testa criação em todas as bases"""
    engine = NotionEngine(TOKEN)
    
    tests = {
        'WORK': {
            'title': 'Teste Debug',
            'emoji': '🧪',
            'status': 'Não iniciado',
            'cliente': 'Astracode',
            'projeto': 'Avulso',
            'priority': 'Normal'
        },
        'PERSONAL': {
            'title': 'Teste Debug',
            'emoji': '🧪',
            'status': 'Não iniciado',
            'atividade': 'Teste'
        },
        'STUDIES': {
            'title': 'Teste Debug',
            'emoji': '🧪',
            'status': 'Para Fazer',
            'categorias': ['Teste'],
            'prioridade': 'Normal'
        },
        'YOUTUBER': {
            'title': 'Teste Debug',
            'emoji': '🧪',
            'status': 'Não iniciado'
        }
    }
    
    results = {}
    
    for base, data in tests.items():
        print(f'\n🧪 Testando {base}...')
        
        card_id = engine.create_card(base, data)
        
        if card_id:
            results[base] = {'success': True, 'id': card_id}
            print(f'   ✅ Sucesso: {card_id}')
        else:
            results[base] = {'success': False}
            print(f'   ❌ Falha')
    
    # Resumo
    print('\n' + '='*50)
    sucesso = sum(1 for r in results.values() if r.get('success'))
    print(f'📊 Resultado: {sucesso}/4 bases funcionando')
    
    if sucesso == 4:
        print('✅ TUDO OK! NotionEngine funcionando perfeitamente')
    else:
        print(f'⚠️  {4-sucesso} base(s) com problema')
        for base, result in results.items():
            if not result.get('success'):
                print(f'   ❌ {base} não funcionou')
    
    return results

if __name__ == "__main__":
    test_engine()
```

---

## 🎯 QUANDO PEDIR AJUDA

Se você tentou tudo e ainda não funciona:

1. **Copie a mensagem de erro completa**
2. **Copie o código que você está usando**
3. **Descreva o que você esperava vs o que aconteceu**
4. **Verifique se seguiu todas as regras deste manual**

---

**Próximo:** Leia `07_WORKFLOWS_COMPLETOS.md` para ver fluxos end-to-end completos














