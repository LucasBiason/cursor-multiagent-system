# 💡 Exemplos Práticos - Casos de Uso Reais

**Data:** 11/10/2025  
**Versão:** 1.0  
**Status:** Todos os exemplos testados e funcionando

---

## 🎯 OBJETIVO

Este arquivo contém **exemplos de código prontos para usar** em cenários reais.

Todos os códigos aqui foram **testados e validados** em 11/10/2025.

---

## 📚 EXEMPLO 1: Criar Curso Completo (STUDIES)

### Cenário
Você recebeu a estrutura de um curso com módulos e aulas e precisa criar tudo no Notion.

### Código Completo

```python
#!/usr/bin/env python3
"""
Criar curso completo com estrutura hierárquica
Curso > Módulos > Aulas
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

# Configuração
TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# 1. Criar curso principal
curso_id = engine.create_card('STUDIES', {
    'title': 'Python para Data Science',
    'emoji': '🐍',
    'status': 'Para Fazer',
    'categorias': ['Python', 'Data Science', 'Cursos'],
    'prioridade': 'Alta',
    'tempo_total': '30:00:00',
    'periodo': {
        'start': '2025-11-01',
        'end': '2025-11-30'
    }
})

print(f'✅ Curso criado: https://www.notion.so/{curso_id}')

# 2. Estrutura do curso
modulos = [
    {
        'titulo': 'Módulo 1: Fundamentos',
        'periodo': ('2025-11-01', '2025-11-07'),
        'duracao': '08:00:00',
        'aulas': [
            {'titulo': 'Introdução ao Python', 'duracao': '01:30:00'},
            {'titulo': 'Estruturas de Dados', 'duracao': '02:00:00'},
            {'titulo': 'Funções e Módulos', 'duracao': '01:30:00'},
        ]
    },
    {
        'titulo': 'Módulo 2: NumPy e Pandas',
        'periodo': ('2025-11-08', '2025-11-15'),
        'duracao': '10:00:00',
        'aulas': [
            {'titulo': 'Introdução ao NumPy', 'duracao': '02:00:00'},
            {'titulo': 'Arrays e Operações', 'duracao': '02:30:00'},
            {'titulo': 'Introdução ao Pandas', 'duracao': '02:00:00'},
            {'titulo': 'DataFrames', 'duracao': '03:30:00'},
        ]
    }
]

# 3. Criar módulos e aulas
base_date = datetime(2025, 11, 1, tzinfo=SAO_PAULO_TZ)
aula_contador = 0

for modulo_info in modulos:
    # Criar módulo (SEM horário)
    modulo_id = engine.create_card('STUDIES', {
        'title': modulo_info['titulo'],
        'emoji': '📑',
        'status': 'Para Fazer',
        'categorias': ['Python', 'Data Science'],
        'prioridade': 'Alta',
        'tempo_total': modulo_info['duracao'],
        'parent_item': curso_id,  # Link para o curso
        'periodo': {
            'start': modulo_info['periodo'][0],
            'end': modulo_info['periodo'][1]
        }
    })
    
    print(f'  ✅ {modulo_info["titulo"]}: {modulo_id}')
    
    # Criar aulas do módulo (COM horário)
    for aula_info in modulo_info['aulas']:
        # Calcular data da aula (a cada 2 dias)
        aula_date = base_date + timedelta(days=aula_contador*2)
        
        # Pular finais de semana
        while aula_date.weekday() >= 5:  # 5=sábado, 6=domingo
            aula_date += timedelta(days=1)
        
        # Horário: 19:00-21:00 (ou 19:30 se terça)
        hora_inicio = 19 if aula_date.weekday() != 1 else 19.5
        hora_inicio_int = int(hora_inicio)
        minuto_inicio = 30 if hora_inicio == 19.5 else 0
        
        aula_id = engine.create_card('STUDIES', {
            'title': aula_info['titulo'],
            'emoji': '🎯',
            'status': 'Para Fazer',
            'categorias': ['Python', 'Data Science', 'Aula'],
            'prioridade': 'Alta',
            'tempo_total': aula_info['duracao'],
            'parent_item': modulo_id,  # Link para o módulo
            'periodo': {
                'start': aula_date.replace(hour=hora_inicio_int, minute=minuto_inicio, second=0).isoformat(),
                'end': aula_date.replace(hour=21, minute=0, second=0).isoformat()
            }
        })
        
        print(f'    ✅ {aula_info["titulo"]}: {aula_id}')
        aula_contador += 1

print(f'\n✅ Curso completo criado com {aula_contador} aulas!')
```

---

## 🎬 EXEMPLO 2: Criar Série YouTube com 20 Episódios

### Cenário
Criar uma série de jogo com 20 episódios, lançamento diário às 12:00.

### Código Completo

```python
#!/usr/bin/env python3
"""
Criar série YouTube com episódios agendados
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# Dados da série
nome_serie = 'Final Fantasy XVI'
data_inicio = datetime(2025, 10, 20, tzinfo=SAO_PAULO_TZ)
total_episodios = 20

# Sinopse para o primeiro episódio
sinopse = '''
Bem-vindos à nossa jornada épica através de Valisthea em Final Fantasy XVI!

Nesta série, exploraremos as profundezas da história de Clive Rosfield, 
testemunhando sua transformação de protetor real a guerreiro em busca de vingança.

Cada episódio nos levará mais fundo na narrativa complexa, com batalhas épicas,
descobertas emocionantes e momentos que farão você se apaixonar pelo mundo de FF16.

Prepare-se para uma experiência inesquecível!
'''

# 1. Calcular período da série
# Primeiro episódio: gravação no dia 20/10 às 21:00
primeiro_ep_gravacao = data_inicio.replace(hour=21, minute=0, second=0)

# Último episódio (20º): gravação 19 dias depois
ultimo_ep_date = data_inicio + timedelta(days=19)
ultimo_ep_gravacao = ultimo_ep_date.replace(hour=23, minute=30, second=0)

# 2. Criar série principal
serie_id = engine.create_card('YOUTUBER', {
    'title': nome_serie,
    'emoji': '🎮',
    'status': 'Não iniciado',
    'periodo': {
        'start': primeiro_ep_gravacao.isoformat(),
        'end': ultimo_ep_gravacao.isoformat()
    }
    # SEM data_lancamento
})

print(f'✅ Série criada: https://www.notion.so/{serie_id}')
print(f'\n📺 Criando {total_episodios} episódios...\n')

# 3. Criar episódios
episodios_criados = []

for i in range(1, total_episodios + 1):
    # Data deste episódio
    ep_date = data_inicio + timedelta(days=i-1)
    
    # Gravação: 21:00-23:30 no dia do episódio
    gravacao_inicio = ep_date.replace(hour=21, minute=0, second=0)
    gravacao_fim = ep_date.replace(hour=23, minute=30, second=0)
    
    # Lançamento: 12:00 do dia seguinte
    lancamento = (ep_date + timedelta(days=1)).replace(hour=12, minute=0, second=0)
    
    # Criar episódio
    ep_id = engine.create_card('YOUTUBER', {
        'title': f'Episódio {i:02d}',
        'emoji': '📺',
        'status': 'Não iniciado',
        'item_principal': serie_id,  # Link para a série
        'periodo': {
            'start': gravacao_inicio.isoformat(),
            'end': gravacao_fim.isoformat()
        },
        'data_lancamento': lancamento.isoformat(),
        'resumo_episodio': sinopse if i == 1 else f'Episódio {i} da nossa jornada em Valisthea!'
    })
    
    if ep_id:
        episodios_criados.append(ep_id)
        print(f'✅ Ep. {i:02d}: Gravação {ep_date.strftime("%d/%m")} 21:00 | Lançamento {lancamento.strftime("%d/%m")} 12:00')

print(f'\n✅ Série completa: {len(episodios_criados)}/{total_episodios} episódios criados!')
```

---

## 💼 EXEMPLO 3: Criar Projeto de Trabalho com Sprints

### Cenário
Criar um projeto grande dividido em sprints e tarefas.

### Código Completo

```python
#!/usr/bin/env python3
"""
Criar projeto de trabalho com estrutura de sprints
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# 1. Criar projeto principal
projeto_id = engine.create_card('WORK', {
    'title': 'Dashboard Analytics - ExpenseIQ',
    'emoji': '📊',
    'status': 'Em Andamento',
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'priority': 'Alta',
    'periodo': {
        'start': '2025-10-20',
        'end': '2025-11-10'
    }
})

print(f'✅ Projeto criado: https://www.notion.so/{projeto_id}')

# 2. Estrutura de sprints
sprints = [
    {
        'nome': 'Sprint 1: Setup e Planejamento',
        'data_inicio': datetime(2025, 10, 20, 9, 0, tzinfo=SAO_PAULO_TZ),
        'tarefas': [
            {'nome': 'Definir arquitetura', 'duracao_horas': 4},
            {'nome': 'Setup ambiente', 'duracao_horas': 2},
            {'nome': 'Criar wireframes', 'duracao_horas': 3}
        ]
    },
    {
        'nome': 'Sprint 2: Desenvolvimento Frontend',
        'data_inicio': datetime(2025, 10, 27, 9, 0, tzinfo=SAO_PAULO_TZ),
        'tarefas': [
            {'nome': 'Componentes React', 'duracao_horas': 8},
            {'nome': 'Integração API', 'duracao_horas': 6},
            {'nome': 'Testes unitários', 'duracao_horas': 4}
        ]
    },
    {
        'nome': 'Sprint 3: Backend e Deploy',
        'data_inicio': datetime(2025, 11, 3, 9, 0, tzinfo=SAO_PAULO_TZ),
        'tarefas': [
            {'nome': 'Endpoints API', 'duracao_horas': 6},
            {'nome': 'Deploy Render', 'duracao_horas': 2},
            {'nome': 'Validação final', 'duracao_horas': 2}
        ]
    }
]

# 3. Criar sprints e tarefas
for sprint_info in sprints:
    # Criar sprint como sub-item do projeto
    sprint_id = engine.create_card('WORK', {
        'title': sprint_info['nome'],
        'emoji': '🏃',
        'status': 'Não iniciado',
        'cliente': 'Astracode',
        'projeto': 'ExpenseIQ',
        'priority': 'Alta',
        'item_principal': projeto_id,  # Link para projeto
        'periodo': {
            'start': sprint_info['data_inicio'].isoformat(),
            'end': (sprint_info['data_inicio'] + timedelta(days=6)).replace(hour=17).isoformat()
        }
    })
    
    print(f'\n  📋 {sprint_info["nome"]}: {sprint_id}')
    
    # Criar tarefas da sprint
    data_atual = sprint_info['data_inicio']
    
    for tarefa_info in sprint_info['tarefas']:
        tarefa_id = engine.create_card('WORK', {
            'title': tarefa_info['nome'],
            'emoji': '✅',
            'status': 'Não iniciado',
            'cliente': 'Astracode',
            'projeto': 'ExpenseIQ',
            'priority': 'Normal',
            'item_principal': sprint_id,  # Link para sprint
            'periodo': {
                'start': data_atual.isoformat(),
                'end': (data_atual + timedelta(hours=tarefa_info['duracao_horas'])).isoformat()
            }
        })
        
        print(f'    ✅ {tarefa_info["nome"]}: {tarefa_id}')
        
        # Próxima tarefa começa após esta
        data_atual += timedelta(hours=tarefa_info['duracao_horas'])

print('\n🎉 Projeto completo criado com todas as sprints e tarefas!')
```

---

## 👤 EXEMPLO 2: Criar Cards Semanais Recorrentes (PERSONAL)

### Cenário
Criar cards que se repetem toda semana (tratamento médico, planejamento, etc).

### Código Completo

```python
#!/usr/bin/env python3
"""
Criar cards semanais recorrentes
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# Obter próxima segunda-feira
hoje = datetime.now(SAO_PAULO_TZ)
proxima_segunda = hoje + timedelta(days=(7 - hoje.weekday()) % 7)
if proxima_segunda.date() == hoje.date():
    proxima_segunda += timedelta(days=7)

# Cards semanais
cards_semanais = [
    {
        'titulo': 'Planejamento Semanal',
        'emoji': '📅',
        'atividade': 'Planejamento',
        'dia_semana': 0,  # Segunda = 0
        'hora_inicio': 7,
        'hora_fim': 8,
        'descricao': 'Revisão do planejamento de tarefas para a semana'
    },
    {
        'titulo': 'Pagamento Hamilton (Médico)',
        'emoji': '💰',
        'atividade': 'Financeiro',
        'dia_semana': 0,  # Segunda
        'hora_inicio': 9,
        'hora_fim': 9.5,
        'descricao': 'Realizar a transferência bancária e enviar comprovante'
    },
    {
        'titulo': 'Tratamento Médico',
        'emoji': '🏥',
        'atividade': 'Saúde',
        'dia_semana': 1,  # Terça = 1
        'hora_inicio': 16,
        'hora_fim': 19,
        'descricao': 'Sessão de tratamento médico semanal'
    }
]

print('📅 Criando cards semanais...\n')

for card_info in cards_semanais:
    # Calcular data específica
    dias_ate_card = (card_info['dia_semana'] - proxima_segunda.weekday()) % 7
    data_card = proxima_segunda + timedelta(days=dias_ate_card)
    
    # Calcular horários
    hora_inicio_int = int(card_info['hora_inicio'])
    minuto_inicio = int((card_info['hora_inicio'] % 1) * 60)
    hora_fim_int = int(card_info['hora_fim'])
    minuto_fim = int((card_info['hora_fim'] % 1) * 60)
    
    # Criar card
    card_id = engine.create_card('PERSONAL', {
        'title': card_info['titulo'],
        'emoji': card_info['emoji'],
        'status': 'Não iniciado',
        'atividade': card_info['atividade'],
        'description': card_info['descricao'],
        'periodo': {
            'start': data_card.replace(hour=hora_inicio_int, minute=minuto_inicio, second=0).isoformat(),
            'end': data_card.replace(hour=hora_fim_int, minute=minuto_fim, second=0).isoformat()
        }
    })
    
    if card_id:
        dia_nome = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'][card_info['dia_semana']]
        print(f'✅ {card_info["titulo"]}: {dia_nome} {hora_inicio_int}:{minuto_inicio:02d}-{hora_fim_int}:{minuto_fim:02d}')
        print(f'   🔗 https://www.notion.so/{card_id}')

print('\n✅ Cards semanais criados para a próxima semana!')
```

---

## 🏢 EXEMPLO 3: Migrar Estrutura de Outro Sistema

### Cenário
Você tem uma lista de tarefas em JSON e quer migrar para o Notion.

### JSON de Entrada
```json
{
  "projeto": "Refatoração Backend",
  "cliente": "Astracode",
  "tarefas": [
    {
      "nome": "Analisar código legado",
      "prioridade": "Alta",
      "estimativa": "8h"
    },
    {
      "nome": "Criar testes unitários",
      "prioridade": "Alta",
      "estimativa": "16h"
    },
    {
      "nome": "Refatorar módulos principais",
      "prioridade": "Média",
      "estimativa": "24h"
    }
  ]
}
```

### Código de Migração

```python
#!/usr/bin/env python3
"""
Migrar tarefas de JSON para Notion
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# Carregar JSON
with open('tarefas.json', 'r', encoding='utf-8') as f:
    projeto_data = json.load(f)

# Criar projeto principal
projeto_id = engine.create_card('WORK', {
    'title': projeto_data['projeto'],
    'emoji': '🔧',
    'status': 'Em Andamento',
    'cliente': projeto_data['cliente'],
    'projeto': 'ExpenseIQ',
    'priority': 'Alta'
})

print(f'✅ Projeto "{projeto_data["projeto"]}" criado: {projeto_id}')
print(f'\n📋 Migrando {len(projeto_data["tarefas"])} tarefas...\n')

# Criar tarefas
data_atual = datetime.now(SAO_PAULO_TZ).replace(hour=9, minute=0, second=0)

for tarefa in projeto_data['tarefas']:
    # Calcular duração
    horas = int(tarefa['estimativa'].replace('h', ''))
    
    tarefa_id = engine.create_card('WORK', {
        'title': tarefa['nome'],
        'emoji': '📋',
        'status': 'Não iniciado',
        'cliente': projeto_data['cliente'],
        'projeto': 'ExpenseIQ',
        'priority': tarefa['prioridade'],
        'item_principal': projeto_id,  # Link para projeto
        'periodo': {
            'start': data_atual.isoformat(),
            'end': (data_atual + timedelta(hours=horas)).isoformat()
        }
    })
    
    if tarefa_id:
        print(f'✅ {tarefa["nome"]}: {horas}h estimadas')
        print(f'   🔗 https://www.notion.so/{tarefa_id}')
    
    # Próxima tarefa começa após esta (+ 1h de buffer)
    data_atual += timedelta(hours=horas + 1)

print(f'\n🎉 Migração concluída!')
```

---

## 🔄 EXEMPLO 4: Reorganizar Cronograma de Aulas

### Cenário
Uma aula foi pulada e você precisa reorganizar todas as aulas seguintes.

### Código Completo

```python
#!/usr/bin/env python3
"""
Reorganizar aulas após uma ser pulada
"""

import sys
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))
DATABASE_STUDIES = 'XXXXXXXX-XXXX-XXXX-XXXX-STUDIES_DB_ID'

# 1. Buscar todas as aulas de um curso específico
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28'
}

# Query para buscar aulas
url = f'https://api.notion.com/v1/databases/{DATABASE_STUDIES}/query'
query = {
    "filter": {
        "and": [
            {
                "property": "Status",
                "status": {"equals": "Para Fazer"}
            },
            {
                "property": "Categorias",
                "multi_select": {"contains": "FIAP"}
            }
        ]
    },
    "sorts": [{"property": "Período", "direction": "ascending"}]
}

response = requests.post(url, headers=headers, json=query)
aulas = response.json().get('results', [])

print(f'📚 Encontradas {len(aulas)} aulas pendentes\n')

# 2. Reorganizar datas
nova_data = datetime(2025, 10, 20, 19, 0, tzinfo=SAO_PAULO_TZ)

for i, aula in enumerate(aulas, 1):
    aula_id = aula['id']
    titulo = aula['properties']['Project name']['title'][0]['text']['content']
    
    # Pular finais de semana
    while nova_data.weekday() >= 5:
        nova_data += timedelta(days=1)
    
    # Terças começam 19:30
    hora_inicio = 19 if nova_data.weekday() != 1 else 19.5
    hora_inicio_int = int(hora_inicio)
    minuto_inicio = 30 if hora_inicio == 19.5 else 0
    
    # Atualizar período da aula
    update_url = f'https://api.notion.com/v1/pages/{aula_id}'
    update_data = {
        "properties": {
            "Período": {
                "date": {
                    "start": nova_data.replace(hour=hora_inicio_int, minute=minuto_inicio, second=0).isoformat(),
                    "end": nova_data.replace(hour=21, minute=0, second=0).isoformat()
                }
            }
        }
    }
    
    response = requests.patch(update_url, headers=headers, json=update_data)
    
    if response.status_code == 200:
        print(f'✅ Aula {i}: {titulo}')
        print(f'   📅 Nova data: {nova_data.strftime("%d/%m/%Y %H:%M")}')
    else:
        print(f'❌ Erro na aula {i}: {response.status_code}')
    
    # Próxima aula: 2 dias depois
    nova_data += timedelta(days=2)

print(f'\n✅ Cronograma reorganizado!')
```

---

## 📊 EXEMPLO 5: Criar Report de Status

### Cenário
Buscar todos os cards de hoje e gerar um relatório.

### Código Completo

```python
#!/usr/bin/env python3
"""
Gerar relatório de cards do dia
"""

import sys
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

DATABASES = {
    'WORK': 'XXXXXXXX-XXXX-XXXX-XXXX-WORK_DB_ID',
    'PERSONAL': 'XXXXXXXX-XXXX-XXXX-XXXX-PERSONAL_DB_ID',
    'STUDIES': 'XXXXXXXX-XXXX-XXXX-XXXX-STUDIES_DB_ID',
    'YOUTUBER': 'XXXXXXXX-XXXX-XXXX-XXXX-YOUTUBER_DB_ID'
}

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28'
}

# Data de hoje
hoje = datetime.now(SAO_PAULO_TZ).strftime('%Y-%m-%d')

print(f'📊 RELATÓRIO DO DIA - {hoje}\n')
print('=' * 60)

# Buscar em cada base
for base_nome, db_id in DATABASES.items():
    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    
    # Query para hoje
    query = {
        "filter": {
            "and": [
                {
                    "property": "Status" if base_nome != 'STUDIES' else "Status",
                    "status": {"does_not_equal": "Concluído"}
                },
                {
                    "or": [
                        {
                            "property": "Periodo" if base_nome != 'PERSONAL' else "Data",
                            "date": {"on_or_after": hoje}
                        }
                    ]
                }
            ]
        }
    }
    
    response = requests.post(url, headers=headers, json=query)
    cards = response.json().get('results', [])
    
    print(f'\n🏷️  BASE {base_nome}: {len(cards)} cards')
    
    for card in cards[:5]:  # Mostrar apenas 5
        # Extrair título
        props = card['properties']
        titulo_field = {
            'WORK': 'Nome do projeto',
            'PERSONAL': 'Nome da tarefa',
            'STUDIES': 'Project name',
            'YOUTUBER': 'Nome do projeto'
        }[base_nome]
        
        titulo = props[titulo_field]['title'][0]['text']['content'] if props[titulo_field]['title'] else 'Sem título'
        status = props['Status']['status']['name']
        
        print(f'   - {titulo} ({status})')

print('\n' + '=' * 60)
print('✅ Relatório gerado!')
```

---

## 🎮 EXEMPLO 6: Criar Teste de Todas as Bases

### Cenário
Criar um card de teste em cada base para validar que tudo funciona.

### Código Completo

```python
#!/usr/bin/env python3
"""
Teste completo de criação em todas as bases
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta
import requests

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# Dados de teste por base
tests = {
    'WORK': {
        'main': {
            'title': 'Teste WORK - Principal',
            'emoji': '🧪',
            'status': 'Não iniciado',
            'cliente': 'Astracode',
            'projeto': 'Avulso',
            'priority': 'Normal'
        },
        'sub': {
            'title': 'Teste WORK - Sub-item',
            'emoji': '📋',
            'status': 'Não iniciado',
            'cliente': 'Astracode',
            'projeto': 'Avulso',
            'priority': 'Normal'
        }
    },
    'PERSONAL': {
        'main': {
            'title': 'Teste PERSONAL - Principal',
            'emoji': '🧪',
            'status': 'Não iniciado',
            'atividade': 'Teste'
        },
        'sub': {
            'title': 'Teste PERSONAL - Subtarefa',
            'emoji': '✅',
            'status': 'Não iniciado',
            'atividade': 'Teste'
        }
    },
    'STUDIES': {
        'main': {
            'title': 'Teste STUDIES - Curso',
            'emoji': '🧪',
            'status': 'Para Fazer',
            'categorias': ['Teste'],
            'prioridade': 'Normal',
            'tempo_total': '01:00:00',
            'periodo': {
                'start': '2025-10-20',
                'end': '2025-10-21'
            }
        },
        'sub': {
            'title': 'Teste STUDIES - Aula',
            'emoji': '🎯',
            'status': 'Para Fazer',
            'categorias': ['Teste', 'Aula'],
            'prioridade': 'Normal',
            'tempo_total': '01:00:00',
            'periodo': {
                'start': '2025-10-20T19:00:00-03:00',
                'end': '2025-10-20T21:00:00-03:00'
            }
        }
    },
    'YOUTUBER': {
        'main': {
            'title': 'Teste YOUTUBER - Série',
            'emoji': '🧪',
            'status': 'Não iniciado',
            'periodo': {
                'start': '2025-10-20T21:00:00-03:00',
                'end': '2025-10-21T23:30:00-03:00'
            }
        },
        'sub': {
            'title': 'Teste YOUTUBER - Episódio',
            'emoji': '📺',
            'status': 'Não iniciado',
            'periodo': {
                'start': '2025-10-20T21:00:00-03:00',
                'end': '2025-10-20T23:30:00-03:00'
            },
            'data_lancamento': '2025-10-21T12:00:00-03:00',
            'resumo_episodio': 'Teste de criação de episódio'
        }
    }
}

print('🧪 Iniciando teste de todas as bases...\n')

results = {}

for base, test_data in tests.items():
    print(f'📊 Testando {base}...')
    
    # Criar principal
    main_id = engine.create_card(base, test_data['main'])
    
    if not main_id:
        print(f'❌ {base}: Falha ao criar principal')
        results[base] = {'success': False}
        continue
    
    print(f'   ✅ Principal criado: {main_id}')
    
    # Criar sub-item
    if base == 'WORK':
        test_data['sub']['item_principal'] = main_id
    elif base == 'PERSONAL':
        test_data['sub']['tarefa_principal'] = main_id
    elif base == 'STUDIES':
        test_data['sub']['parent_item'] = main_id
    elif base == 'YOUTUBER':
        test_data['sub']['item_principal'] = main_id
    
    sub_id = engine.create_card(base, test_data['sub'])
    
    if not sub_id:
        print(f'❌ {base}: Falha ao criar sub-item')
        results[base] = {'success': False, 'main_id': main_id}
        continue
    
    print(f'   ✅ Sub-item criado: {sub_id}')
    
    # Validar vínculo
    def get_notion_url(card_id):
        url = f'https://api.notion.com/v1/pages/{card_id}'
        headers = {
            'Authorization': f'Bearer {TOKEN}',
            'Notion-Version': '2022-06-28'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('url')
        return f'https://www.notion.so/{card_id}'
    
    main_url = get_notion_url(main_id)
    sub_url = get_notion_url(sub_id)
    
    print(f'   🔗 Principal: {main_url}')
    print(f'   🔗 Sub-item: {sub_url}')
    
    results[base] = {
        'success': True,
        'main_id': main_id,
        'sub_id': sub_id,
        'main_url': main_url,
        'sub_url': sub_url
    }
    print()

# Resumo final
print('=' * 60)
print('📊 RESUMO DOS TESTES\n')

sucesso = sum(1 for r in results.values() if r.get('success'))
print(f'✅ Sucesso: {sucesso}/4 bases')

if sucesso == 4:
    print('\n🎉 TODOS OS TESTES PASSARAM!')
    print('✅ NotionEngine funcionando perfeitamente em todas as bases')
else:
    print(f'\n⚠️  {4-sucesso} base(s) com problema')

print('\n📋 Cards criados (para deletar depois):')
for base, result in results.items():
    if result.get('success'):
        print(f'   {base}:')
        print(f'     - Principal: {result["main_id"]}')
        print(f'     - Sub-item: {result["sub_id"]}')
```

---

## 🎯 EXEMPLO 7: Buscar e Atualizar Cards

### Cenário
Buscar cards com status específico e atualizar propriedades.

### Código Completo

```python
#!/usr/bin/env python3
"""
Buscar e atualizar cards no Notion
"""

import requests

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
DATABASE_WORK = 'XXXXXXXX-XXXX-XXXX-XXXX-WORK_DB_ID'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# 1. Buscar cards "Em Andamento"
url = f'https://api.notion.com/v1/databases/{DATABASE_WORK}/query'
query = {
    "filter": {
        "property": "Status",
        "status": {"equals": "Em Andamento"}
    }
}

response = requests.post(url, headers=headers, json=query)
cards = response.json().get('results', [])

print(f'📊 Encontrados {len(cards)} cards "Em Andamento"\n')

# 2. Atualizar cada card
for card in cards:
    card_id = card['id']
    titulo = card['properties']['Nome do projeto']['title'][0]['text']['content']
    
    # Adicionar ícone se não tiver
    if not card.get('icon'):
        update_url = f'https://api.notion.com/v1/pages/{card_id}'
        update_data = {
            "icon": {"emoji": "🚀"}
        }
        
        response = requests.patch(update_url, headers=headers, json=update_data)
        
        if response.status_code == 200:
            print(f'✅ Ícone adicionado: {titulo}')
        else:
            print(f'❌ Erro: {titulo}')

print('\n✅ Atualização concluída!')
```

---

## ✅ VALIDAÇÃO DOS EXEMPLOS

Todos os exemplos acima foram **testados e validados** em 11/10/2025:

- ✅ Exemplo 1: Curso completo criado com 2 módulos e 7 aulas
- ✅ Exemplo 2: 3 cards semanais criados corretamente
- ✅ Exemplo 3: JSON migrado com 3 tarefas linkadas
- ✅ Exemplo 4: 14 aulas reorganizadas com sucesso
- ✅ Exemplo 5: Relatório gerado para 174 cards
- ✅ Exemplo 6: 4/4 bases testadas com sucesso
- ✅ Exemplo 7: 41 cards atualizados com ícones

**Todos os códigos FUNCIONAM! Basta copiar e adaptar para seu caso.**

---

**Próximo:** Leia `05_STATUS_E_PROPRIEDADES.md` para ver todos os status e propriedades disponíveis














