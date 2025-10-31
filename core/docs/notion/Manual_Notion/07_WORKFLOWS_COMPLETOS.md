# 🔄 Workflows Completos - End-to-End

**Data:** 11/10/2025  
**Versão:** 1.0  
**Status:** Todos os workflows testados

---

## 🎯 OBJETIVO

Este arquivo mostra **fluxos completos de trabalho** do início ao fim, incluindo:
- Estruturas de cursos extraídas por IA
- Criação de projetos de trabalho
- Organização de séries YouTube
- Tarefas semanais recorrentes

---

## 📚 WORKFLOW 1: Criar Curso a Partir de Extração de IA

### Cenário Real
Você usa uma IA para extrair a estrutura de um curso e ela retorna algo assim:

```
Curso: Python Avançado para Data Science
Duração Total: 15:30:00

Módulo 1: Fundamentos Python Avançado
* Duração: 05:00:00
* Aulas:
    - Aula 1: Decorators e Context Managers: 01:30:00
    - Aula 2: Generators e Iterators: 01:15:00
    - Aula 3: Meta Classes e Descriptors: 02:15:00

Módulo 2: NumPy e Pandas Avançado
* Duração: 06:30:00
* Aulas:
    - Aula 1: NumPy Avançado: 02:00:00
    - Aula 2: Pandas Performance: 02:30:00
    - Aula 3: Visualização de Dados: 02:00:00

Módulo 3: Machine Learning Prático
* Duração: 04:00:00
* Aulas:
    - Aula 1: Scikit-learn Fundamentos: 01:30:00
    - Aula 2: Projeto Prático: 02:30:00
```

### Script Completo

```python
#!/usr/bin/env python3
"""
Criar curso no Notion a partir de extração de IA
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# 1. Dados extraídos (copie da saída da IA)
curso_info = {
    'titulo': 'Python Avançado para Data Science',
    'duracao_total': '15:30:00',
    'data_inicio': datetime(2025, 11, 10, tzinfo=SAO_PAULO_TZ),
    'categorias': ['Python', 'Data Science', 'Cursos'],
    'instituicao': 'Udemy',
    'modulos': [
        {
            'titulo': 'Módulo 1: Fundamentos Python Avançado',
            'duracao': '05:00:00',
            'aulas': [
                {'titulo': 'Aula 1: Decorators e Context Managers', 'duracao': '01:30:00'},
                {'titulo': 'Aula 2: Generators e Iterators', 'duracao': '01:15:00'},
                {'titulo': 'Aula 3: Meta Classes e Descriptors', 'duracao': '02:15:00'}
            ]
        },
        {
            'titulo': 'Módulo 2: NumPy e Pandas Avançado',
            'duracao': '06:30:00',
            'aulas': [
                {'titulo': 'Aula 1: NumPy Avançado', 'duracao': '02:00:00'},
                {'titulo': 'Aula 2: Pandas Performance', 'duracao': '02:30:00'},
                {'titulo': 'Aula 3: Visualização de Dados', 'duracao': '02:00:00'}
            ]
        },
        {
            'titulo': 'Módulo 3: Machine Learning Prático',
            'duracao': '04:00:00',
            'aulas': [
                {'titulo': 'Aula 1: Scikit-learn Fundamentos', 'duracao': '01:30:00'},
                {'titulo': 'Aula 2: Projeto Prático', 'duracao': '02:30:00'}
            ]
        }
    ]
}

# 2. Calcular data de término
def calcular_dias_necessarios(modulos):
    """Calcula quantos dias de estudo serão necessários"""
    total_aulas = sum(len(m['aulas']) for m in modulos)
    # Assumindo 1 aula a cada 2 dias
    return total_aulas * 2

dias_necessarios = calcular_dias_necessarios(curso_info['modulos'])
data_fim = curso_info['data_inicio'] + timedelta(days=dias_necessarios)

# 3. Criar curso principal (SEM horário)
print(f'📚 Criando curso: {curso_info["titulo"]}\n')

curso_id = engine.create_card('STUDIES', {
    'title': curso_info['titulo'],
    'emoji': '🎓',
    'status': 'Para Fazer',
    'categorias': curso_info['categorias'] + [curso_info['instituicao']],
    'prioridade': 'Alta',
    'tempo_total': curso_info['duracao_total'],
    'periodo': {
        'start': curso_info['data_inicio'].strftime('%Y-%m-%d'),
        'end': data_fim.strftime('%Y-%m-%d')
    }
})

print(f'✅ Curso criado: https://www.notion.so/{curso_id}')

# 4. Criar módulos e aulas
data_aula_atual = curso_info['data_inicio']

for modulo_info in curso_info['modulos']:
    # Calcular período do módulo
    total_aulas = len(modulo_info['aulas'])
    dias_modulo = total_aulas * 2
    data_fim_modulo = data_aula_atual + timedelta(days=dias_modulo)
    
    # Criar módulo (SEM horário)
    modulo_id = engine.create_card('STUDIES', {
        'title': modulo_info['titulo'],
        'emoji': '📑',
        'status': 'Para Fazer',
        'categorias': curso_info['categorias'],
        'prioridade': 'Alta',
        'tempo_total': modulo_info['duracao'],
        'parent_item': curso_id,  # Link para curso
        'periodo': {
            'start': data_aula_atual.strftime('%Y-%m-%d'),
            'end': data_fim_modulo.strftime('%Y-%m-%d')
        }
    })
    
    print(f'\n  📑 {modulo_info["titulo"]}')
    print(f'     Período: {data_aula_atual.strftime("%d/%m")} - {data_fim_modulo.strftime("%d/%m")}')
    
    # Criar aulas (COM horário)
    for aula_info in modulo_info['aulas']:
        # Pular finais de semana
        while data_aula_atual.weekday() >= 5:
            data_aula_atual += timedelta(days=1)
        
        # Horário: 19:00-21:00 (ou 19:30 se terça)
        e_terca = data_aula_atual.weekday() == 1
        hora_inicio = 19 if not e_terca else 19.5
        hora_inicio_int = int(hora_inicio)
        minuto_inicio = 30 if e_terca else 0
        
        aula_id = engine.create_card('STUDIES', {
            'title': aula_info['titulo'],
            'emoji': '🎯',
            'status': 'Para Fazer',
            'categorias': curso_info['categorias'] + ['Aula'],
            'prioridade': 'Alta',
            'tempo_total': aula_info['duracao'],
            'parent_item': modulo_id,  # Link para módulo
            'periodo': {
                'start': data_aula_atual.replace(hour=hora_inicio_int, minute=minuto_inicio, second=0).isoformat(),
                'end': data_aula_atual.replace(hour=21, minute=0, second=0).isoformat()
            }
        })
        
        print(f'     ✅ {aula_info["titulo"]}')
        print(f'        📅 {data_aula_atual.strftime("%d/%m %H:%M")} - 21:00')
        
        # Próxima aula: 2 dias depois
        data_aula_atual += timedelta(days=2)

print(f'\n🎉 Curso completo criado no Notion!')
print(f'📊 Total: {len(curso_info["modulos"])} módulos')
total_aulas = sum(len(m["aulas"]) for m in curso_info["modulos"])
print(f'📚 Total: {total_aulas} aulas')
```

---

## 🎬 WORKFLOW 2: Criar Série YouTube Completa

### Cenário Real
Criar uma série de jogo com cronograma de gravação e lançamento.

### Especificações
```
Série: Persona 6 Gameplay
Início: 20/10/2025
Total de Episódios: 30
Lançamento: Diário às 12:00
Gravação: Noturna 21:00-23:30
Padrão: 1 episódio por dia
```

### Script Completo

```python
#!/usr/bin/env python3
"""
Criar série YouTube completa com cronograma
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# Configurações da série
nome_serie = 'Persona 6 Gameplay'
data_inicio = datetime(2025, 10, 20, tzinfo=SAO_PAULO_TZ)
total_episodios = 30
horario_lancamento = 12  # 12:00
horario_gravacao_inicio = 21  # 21:00
horario_gravacao_fim = 23.5  # 23:30

# Sinopse da série
sinopse = '''
Bem-vindos à nossa jornada através de Persona 6!

Nesta série completa, vamos explorar cada aspecto deste RPG japonês incrível,
desde os sistemas de social link até as batalhas estratégicas contra as Shadows.

Acompanhe nossa aventura enquanto desvendamos os mistérios da Velvet Room,
formamos laços profundos com os personagens e salvamos o mundo da escuridão.

Prepare-se para uma experiência inesquecível cheia de emoção, estratégia e história envolvente!
'''

print(f'🎬 Criando série: {nome_serie}')
print(f'📅 Período: {data_inicio.strftime("%d/%m/%Y")} - {total_episodios} episódios')
print(f'⏰ Gravação: {int(horario_gravacao_inicio)}:00 - {int(horario_gravacao_fim)}:{int((horario_gravacao_fim%1)*60):02d}')
print(f'📺 Lançamento: {horario_lancamento}:00 diário\n')

# 1. Calcular período da série
primeiro_ep_gravacao = data_inicio.replace(
    hour=int(horario_gravacao_inicio),
    minute=0,
    second=0
)

ultimo_ep_date = data_inicio + timedelta(days=total_episodios-1)
ultimo_ep_gravacao = ultimo_ep_date.replace(
    hour=int(horario_gravacao_fim),
    minute=int((horario_gravacao_fim % 1) * 60),
    second=0
)

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

print(f'✅ Série criada: {serie_id}')
print(f'   Período: {primeiro_ep_gravacao.strftime("%d/%m %H:%M")} - {ultimo_ep_gravacao.strftime("%d/%m %H:%M")}\n')

# 3. Criar episódios
print(f'📺 Criando {total_episodios} episódios...\n')

episodios_criados = []

for i in range(1, total_episodios + 1):
    ep_date = data_inicio + timedelta(days=i-1)
    
    # Gravação
    gravacao_inicio = ep_date.replace(
        hour=int(horario_gravacao_inicio),
        minute=0,
        second=0
    )
    gravacao_fim = ep_date.replace(
        hour=int(horario_gravacao_fim),
        minute=int((horario_gravacao_fim % 1) * 60),
        second=0
    )
    
    # Lançamento: dia seguinte ao meio-dia
    lancamento = (ep_date + timedelta(days=1)).replace(
        hour=horario_lancamento,
        minute=0,
        second=0
    )
    
    # Criar episódio
    ep_id = engine.create_card('YOUTUBER', {
        'title': f'Episódio {i:02d}',
        'emoji': '📺',
        'status': 'Não iniciado',
        'item_principal': serie_id,  # Link para série
        'periodo': {
            'start': gravacao_inicio.isoformat(),
            'end': gravacao_fim.isoformat()
        },
        'data_lancamento': lancamento.isoformat(),
        'resumo_episodio': sinopse if i == 1 else f'Episódio {i} da nossa jornada em Persona 6!'
    })
    
    if ep_id:
        episodios_criados.append(ep_id)
        if i <= 5 or i > total_episodios - 2:  # Mostrar apenas primeiros 5 e últimos 2
            print(f'✅ Ep. {i:02d}: Grav {gravacao_inicio.strftime("%d/%m %H:%M")} | Lanç {lancamento.strftime("%d/%m %H:%M")}')
        elif i == 6:
            print(f'   ... (episódios {i} a {total_episodios-2})')

print(f'\n🎉 Série completa!')
print(f'📊 {len(episodios_criados)}/{total_episodios} episódios criados')
print(f'🔗 Série: https://www.notion.so/{serie_id}')
```

---

## 💼 WORKFLOW 2: Criar Projeto de Trabalho com Subtarefas

### Cenário Real
Novo projeto da Astracode precisa ser organizado no Notion.

### Especificações
```
Projeto: Implementar Sistema de Relatórios
Cliente: Astracode
Projeto: ExpenseIQ
Prazo: 2 semanas
Escopo:
  - Backend: Criar endpoints de relatórios (3 dias)
  - Frontend: Componentes de visualização (5 dias)
  - Testes: Testes automatizados (2 dias)
  - Deploy: Deploy e validação (2 dias)
```

### Script Completo

```python
#!/usr/bin/env python3
"""
Criar projeto de trabalho estruturado
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# Dados do projeto
projeto_info = {
    'titulo': 'Implementar Sistema de Relatórios',
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'data_inicio': datetime(2025, 10, 21, 9, 0, tzinfo=SAO_PAULO_TZ),
    'tarefas': [
        {
            'titulo': 'Backend: Criar Endpoints de Relatórios',
            'prioridade': 'Alta',
            'dias_estimados': 3,
            'subtarefas': [
                {'nome': 'Endpoint de relatório financeiro', 'horas': 8},
                {'nome': 'Endpoint de relatório de despesas', 'horas': 8},
                {'nome': 'Endpoint de relatório customizado', 'horas': 8}
            ]
        },
        {
            'titulo': 'Frontend: Componentes de Visualização',
            'prioridade': 'Alta',
            'dias_estimados': 5,
            'subtarefas': [
                {'nome': 'Componente de tabela dinâmica', 'horas': 16},
                {'nome': 'Gráficos e dashboards', 'horas': 16},
                {'nome': 'Filtros e exportação', 'horas': 8}
            ]
        },
        {
            'titulo': 'Testes: Testes Automatizados',
            'prioridade': 'Média',
            'dias_estimados': 2,
            'subtarefas': [
                {'nome': 'Testes unitários backend', 'horas': 8},
                {'nome': 'Testes integração frontend', 'horas': 8}
            ]
        },
        {
            'titulo': 'Deploy: Deploy e Validação',
            'prioridade': 'Alta',
            'dias_estimados': 2,
            'subtarefas': [
                {'nome': 'Deploy Render', 'horas': 4},
                {'nome': 'Validação em produção', 'horas': 4},
                {'nome': 'Documentação final', 'horas': 4}
            ]
        }
    ]
}

# 1. Criar projeto principal
print(f'💼 Criando projeto: {projeto_info["titulo"]}\n')

# Calcular data final
total_dias = sum(t['dias_estimados'] for t in projeto_info['tarefas'])
data_fim = projeto_info['data_inicio'] + timedelta(days=total_dias)

projeto_id = engine.create_card('WORK', {
    'title': projeto_info['titulo'],
    'emoji': '📊',
    'status': 'Em Andamento',
    'cliente': projeto_info['cliente'],
    'projeto': projeto_info['projeto'],
    'priority': 'Alta',
    'periodo': {
        'start': projeto_info['data_inicio'].isoformat(),
        'end': data_fim.isoformat()
    }
})

print(f'✅ Projeto principal criado: {projeto_id}')
print(f'   Período: {projeto_info["data_inicio"].strftime("%d/%m")} - {data_fim.strftime("%d/%m")}\n')

# 2. Criar tarefas principais
data_tarefa_atual = projeto_info['data_inicio']

for tarefa_info in projeto_info['tarefas']:
    data_fim_tarefa = data_tarefa_atual + timedelta(days=tarefa_info['dias_estimados'])
    
    # Criar tarefa como sub-item do projeto
    tarefa_id = engine.create_card('WORK', {
        'title': tarefa_info['titulo'],
        'emoji': '📋',
        'status': 'Não iniciado',
        'cliente': projeto_info['cliente'],
        'projeto': projeto_info['projeto'],
        'priority': tarefa_info['prioridade'],
        'item_principal': projeto_id,  # Link para projeto
        'periodo': {
            'start': data_tarefa_atual.isoformat(),
            'end': data_fim_tarefa.isoformat()
        }
    })
    
    print(f'  📋 {tarefa_info["titulo"]}: {tarefa_id}')
    
    # 3. Criar subtarefas
    data_subtarefa_atual = data_tarefa_atual
    
    for subtarefa_info in tarefa_info['subtarefas']:
        horas = subtarefa_info['horas']
        data_fim_subtarefa = data_subtarefa_atual + timedelta(hours=horas)
        
        subtarefa_id = engine.create_card('WORK', {
            'title': subtarefa_info['nome'],
            'emoji': '✅',
            'status': 'Não iniciado',
            'cliente': projeto_info['cliente'],
            'projeto': projeto_info['projeto'],
            'priority': 'Normal',
            'item_principal': tarefa_id,  # Link para tarefa
            'periodo': {
                'start': data_subtarefa_atual.isoformat(),
                'end': data_fim_subtarefa.isoformat()
            }
        })
        
        print(f'     ✅ {subtarefa_info["nome"]}: {horas}h')
        
        # Próxima subtarefa
        data_subtarefa_atual = data_fim_subtarefa
    
    # Próxima tarefa
    data_tarefa_atual = data_fim_tarefa
    print()

print(f'🎉 Projeto completo criado!')
total_subtarefas = sum(len(t['subtarefas']) for t in projeto_info['tarefas'])
print(f'📊 {len(projeto_info["tarefas"])} tarefas + {total_subtarefas} subtarefas')
```

---

## 👤 WORKFLOW 3: Criar Cards Semanais Automaticamente

### Cenário Real
Todo domingo às 23:00, criar cards da próxima semana.

### Cards Recorrentes
```
Segunda 07:00: Planejamento Semanal
Segunda 09:00: Pagamento Hamilton (Médico)
Terça 16:00: Tratamento Médico
Dia 15: Revisão Financeira
Dia 25: Emissão de Nota Fiscal
Dia 30: Revisão Financeira - Fechamento
```

### Script Completo

```python
#!/usr/bin/env python3
"""
Criar cards semanais recorrentes - Executar todo domingo 23:00
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta
import calendar

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# Obter próxima semana
hoje = datetime.now(SAO_PAULO_TZ)
proxima_segunda = hoje + timedelta(days=(7 - hoje.weekday()) % 7 or 7)

# Cards semanais
cards_semanais = [
    {
        'titulo': 'Planejamento Semanal',
        'emoji': '📅',
        'atividade': 'Planejamento',
        'dia': 0,  # Segunda
        'hora': (7, 0),
        'duracao_horas': 1,
        'descricao': 'Revisão do planejamento de tarefas para a semana'
    },
    {
        'titulo': 'Pagamento Hamilton (Médico)',
        'emoji': '💰',
        'atividade': 'Financeiro',
        'dia': 0,  # Segunda
        'hora': (9, 0),
        'duracao_horas': 0.5,
        'descricao': 'Realizar a transferência bancária e enviar o comprovante'
    },
    {
        'titulo': 'Tratamento Médico',
        'emoji': '🏥',
        'atividade': 'Saúde',
        'dia': 1,  # Terça
        'hora': (16, 0),
        'duracao_horas': 3,
        'descricao': 'Sessão de tratamento médico semanal'
    }
]

print(f'📅 Criando cards para semana de {proxima_segunda.strftime("%d/%m/%Y")}\n')

# Criar cards semanais
for card_info in cards_semanais:
    # Calcular data específica
    data_card = proxima_segunda + timedelta(days=card_info['dia'])
    hora_inicio_h, hora_inicio_m = card_info['hora']
    duracao = card_info['duracao_horas']
    hora_fim = hora_inicio_h + int(duracao)
    minuto_fim = hora_inicio_m + int((duracao % 1) * 60)
    
    card_id = engine.create_card('PERSONAL', {
        'title': card_info['titulo'],
        'emoji': card_info['emoji'],
        'status': 'Não iniciado',
        'atividade': card_info['atividade'],
        'description': card_info['descricao'],
        'periodo': {
            'start': data_card.replace(hour=hora_inicio_h, minute=hora_inicio_m, second=0).isoformat(),
            'end': data_card.replace(hour=hora_fim, minute=minuto_fim, second=0).isoformat()
        }
    })
    
    if card_id:
        dia_nome = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'][card_info['dia']]
        print(f'✅ {card_info["titulo"]}')
        print(f'   📅 {dia_nome} {data_card.strftime("%d/%m")} às {hora_inicio_h}:{hora_inicio_m:02d}')

# Cards mensais
ano_atual = proxima_segunda.year
mes_atual = proxima_segunda.month

cards_mensais = [
    {
        'titulo': 'Revisão Financeira',
        'emoji': '💰',
        'atividade': 'Financeiro',
        'dia': 15,
        'descricao': 'Revisão quinzenal das finanças pessoais'
    },
    {
        'titulo': 'Emissão de Nota Fiscal Astracode',
        'emoji': '📝',
        'atividade': 'Financeiro',
        'dia': 25,
        'descricao': 'Emitir e enviar NF de serviços prestados'
    },
    {
        'titulo': 'Revisão Financeira - Fechamento do Mês',
        'emoji': '📊',
        'atividade': 'Financeiro',
        'dia': calendar.monthrange(ano_atual, mes_atual)[1],  # Último dia do mês
        'descricao': 'Fechamento mensal e atualização da planilha de controle'
    }
]

print(f'\n📅 Criando cards mensais...\n')

for card_info in cards_mensais:
    data_card = datetime(ano_atual, mes_atual, card_info['dia'], 19, 0, tzinfo=SAO_PAULO_TZ)
    
    # Verificar se está na próxima semana
    if data_card < proxima_segunda or data_card >= proxima_segunda + timedelta(days=7):
        continue  # Pular se não for desta semana
    
    card_id = engine.create_card('PERSONAL', {
        'title': card_info['titulo'],
        'emoji': card_info['emoji'],
        'status': 'Não iniciado',
        'atividade': card_info['atividade'],
        'description': card_info['descricao'],
        'periodo': {
            'start': data_card.isoformat(),
            'end': (data_card + timedelta(hours=1)).isoformat()
        }
    })
    
    if card_id:
        print(f'✅ {card_info["titulo"]}')
        print(f'   📅 Dia {card_info["dia"]}/{mes_atual}')

print(f'\n✅ Cards semanais e mensais criados!')
```

---

## 🔄 WORKFLOW 4: Reorganizar Cronograma Após Atraso

### Cenário Real
Você pulou aulas de sexta e precisa reorganizar todo o cronograma.

### Script Completo

```python
#!/usr/bin/env python3
"""
Reorganizar cronograma de curso após atraso
"""

import sys
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))
DATABASE_STUDIES = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# 1. Buscar aulas pendentes de um curso específico
url = f'https://api.notion.com/v1/databases/{DATABASE_STUDIES}/query'

# Query para buscar apenas aulas "Para Fazer" da FIAP
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
            },
            {
                "property": "Categorias",
                "multi_select": {"contains": "Aula"}  # Apenas aulas (não seções)
            }
        ]
    },
    "sorts": [{"property": "Período", "direction": "ascending"}]
}

response = requests.post(url, headers=headers, json=query)
aulas = response.json().get('results', [])

print(f'📚 Encontradas {len(aulas)} aulas pendentes')
print(f'🔄 Reorganizando a partir de hoje...\n')

# 2. Nova data de início
nova_data = datetime.now(SAO_PAULO_TZ).replace(hour=19, minute=0, second=0, microsecond=0)

# Se for após 19h, começar amanhã
if datetime.now(SAO_PAULO_TZ).hour >= 19:
    nova_data += timedelta(days=1)

# 3. Reorganizar cada aula
for i, aula in enumerate(aulas, 1):
    # Pular finais de semana
    while nova_data.weekday() >= 5:
        nova_data += timedelta(days=1)
    
    # Ajustar horário se for terça
    e_terca = nova_data.weekday() == 1
    hora_inicio = 19 if not e_terca else 19.5
    hora_inicio_int = int(hora_inicio)
    minuto_inicio = 30 if e_terca else 0
    
    # Atualizar período da aula
    aula_id = aula['id']
    titulo = aula['properties']['Project name']['title'][0]['text']['content']
    
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
        dia_nome = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'][nova_data.weekday()]
        print(f'✅ Aula {i:02d}: {titulo}')
        print(f'   📅 {dia_nome} {nova_data.strftime("%d/%m %H:%M")} - 21:00')
    else:
        print(f'❌ Erro na aula {i}: {response.status_code}')
    
    # Próxima aula: 2 dias depois (padrão)
    nova_data += timedelta(days=2)
    print()

print(f'✅ Cronograma reorganizado para {len(aulas)} aulas!')
```

---

## 🔄 WORKFLOW 5: Migração de Dados Externos

### Cenário Real
Você tem uma planilha Excel/CSV com tarefas e quer migrar para Notion.

### CSV de Entrada
```csv
titulo,prioridade,categoria,horas_estimadas
Implementar Login,Alta,Backend,8
Criar Tela Dashboard,Alta,Frontend,16
Testes Unitários,Média,QA,12
Documentação API,Baixa,Docs,6
```

### Script Completo

```python
#!/usr/bin/env python3
"""
Migrar tarefas de CSV para Notion
"""

import sys
import csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

engine = NotionEngine(TOKEN)

# 1. Ler CSV
print('📂 Lendo tarefas do CSV...\n')

tarefas = []
with open('tarefas.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tarefas.append(row)

print(f'📊 {len(tarefas)} tarefas encontradas')

# 2. Criar projeto principal
projeto_id = engine.create_card('WORK', {
    'title': 'Migração de Tarefas - CSV',
    'emoji': '📦',
    'status': 'Em Andamento',
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'priority': 'Alta'
})

print(f'✅ Projeto criado: {projeto_id}\n')

# 3. Migrar tarefas
emojis_por_categoria = {
    'Backend': '🔧',
    'Frontend': '🎨',
    'QA': '🧪',
    'Docs': '📝'
}

data_atual = datetime.now(SAO_PAULO_TZ).replace(hour=9, minute=0, second=0, microsecond=0)

# Começar segunda próxima se for fim de semana
while data_atual.weekday() >= 5:
    data_atual += timedelta(days=1)

criados = 0
falhas = 0

for tarefa in tarefas:
    emoji = emojis_por_categoria.get(tarefa['categoria'], '📋')
    horas = int(tarefa['horas_estimadas'])
    
    card_id = engine.create_card('WORK', {
        'title': tarefa['titulo'],
        'emoji': emoji,
        'status': 'Não iniciado',
        'cliente': 'Astracode',
        'projeto': 'ExpenseIQ',
        'priority': tarefa['prioridade'],
        'item_principal': projeto_id,  # Link para projeto
        'periodo': {
            'start': data_atual.isoformat(),
            'end': (data_atual + timedelta(hours=horas)).isoformat()
        }
    })
    
    if card_id:
        criados += 1
        print(f'✅ {tarefa["titulo"]}: {horas}h ({tarefa["prioridade"]})')
    else:
        falhas += 1
        print(f'❌ Falha: {tarefa["titulo"]}')
    
    # Próxima tarefa (+ 1h de buffer)
    data_atual += timedelta(hours=horas + 1)
    
    # Pular finais de semana
    while data_atual.weekday() >= 5:
        data_atual += timedelta(days=1)
        data_atual = data_atual.replace(hour=9, minute=0)

print(f'\n📊 Migração concluída:')
print(f'   ✅ Criados: {criados}')
print(f'   ❌ Falhas: {falhas}')
print(f'   🔗 Projeto: https://www.notion.so/{projeto_id}')
```

---

## ✅ CHECKLIST DE WORKFLOW

Ao executar qualquer workflow:

### Antes de Executar
- [ ] Token configurado
- [ ] NotionEngine importado
- [ ] Path configurado corretamente
- [ ] Dados de entrada validados
- [ ] Timezone GMT-3 configurado

### Durante Execução
- [ ] Logs claros de progresso
- [ ] Tratamento de erros
- [ ] Validação de retorno
- [ ] Contador de sucesso/falha

### Após Execução
- [ ] Verificar quantidade criada
- [ ] Abrir links no Notion
- [ ] Validar vínculos
- [ ] Verificar ícones e propriedades

---

**Fim do Manual!** Agora você sabe tudo sobre criação de cards no Notion.














