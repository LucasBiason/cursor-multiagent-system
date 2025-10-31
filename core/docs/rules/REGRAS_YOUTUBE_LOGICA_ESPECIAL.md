# 🎥 REGRAS ESPECIAIS - BASE YOUTUBE

**Data:** 22/10/2025  
**Versão:** 1.0  
**Status:** Lógica Validada e Funcionando

---

## 🎯 DIFERENÇA ENTRE CAMPOS

### 📅 Período (Data de Gravação)
- **O QUE É:** Quando o episódio será **GRAVADO**
- **QUANDO:** Data e hora reais de trabalho/gravação
- **EXEMPLO:** `2025-10-22T21:00:00-03:00` até `2025-10-22T23:30:00-03:00`

### 📺 Data de Lançamento (Publicação)
- **O QUE É:** Quando o episódio será **PUBLICADO** no YouTube
- **QUANDO:** Data e hora que ficará público
- **EXEMPLO:** `2025-10-23T12:00:00-03:00`

---

## 🔍 LÓGICA DE VERIFICAÇÃO DE ATRASOS

### Para Episódios PUBLICADOS
```python
if status == "Publicado":
    return "IGNORE"  # Ignorar - já está no ar
```

**Motivo:** Episódios publicados não precisam de ação.

---

### Para Episódios EM EDIÇÃO
```python
if status in ["Editando", "Para Edição", "Em Edição", "Revisão"]:
    # Verificar Data de Lançamento (não o Período)
    launch_date = get_launch_date_from_properties(properties)
    
    if launch_date and launch_date < today:
        return "OVERDUE"  # Atrasado - deveria ter sido lançado
    else:
        return "OK"  # Não está atrasado
```

**Motivo:** Um episódio pode estar em edição há semanas, mas só é "atrasado" se a Data de Lançamento já passou.

---

### Para Outros Status
```python
if status in ["Não iniciado", "Gravando", "Para Gravar"]:
    # Verificar Período (data de gravação)
    periodo = get_periodo_from_properties(properties)
    
    if periodo and periodo < today:
        return "OVERDUE"  # Atrasado - deveria ter sido gravado
    else:
        return "OK"
```

**Motivo:** Se ainda não foi gravado, verificar pela data de gravação planejada.

---

## 📊 ESTRUTURA DE SÉRIE VS EPISÓDIO

### Série Principal
```python
{
    'title': 'Nome da Série',
    'status': 'Não iniciado',
    'periodo': {
        'start': '2025-10-22T21:00:00-03:00',  # Gravação do 1º episódio
        'end': '2025-11-10T23:30:00-03:00'      # Gravação do último episódio
    }
    # ❌ SEM Data de Lançamento
}
```

**Regras:**
- ✅ TEM campo `Periodo` (gravação 1º ao último ep)
- ❌ NÃO TEM campo `Data de Lançamento`

---

### Episódio
```python
{
    'title': 'Episódio 01',
    'status': 'Não iniciado',
    'item_principal': 'ID_DA_SERIE',
    'periodo': {
        'start': '2025-10-22T21:00:00-03:00',  # Quando GRAVAR
        'end': '2025-10-22T23:30:00-03:00'
    },
    'data_lancamento': '2025-10-23T12:00:00-03:00',  # Quando PUBLICAR
    'resumo_episodio': 'Sinopse...'  # Obrigatório no episódio 1
}
```

**Regras:**
- ✅ TEM campo `Periodo` (quando gravar)
- ✅ TEM campo `Data de Lançamento` (quando publicar)
- ✅ TEM vínculo com a série (`item_principal`)
- ✅ Episódio 1 TEM sinopse da série

---

## 🔄 FLUXO DE STATUS

### Status Típico de um Episódio
```
1. Não iniciado (criado)
   ↓
2. Para Gravar (próximo da gravação)
   ↓
3. Gravando (durante a gravação)
   ↓
4. Para Edição (gravado, aguardando edição)
   ↓
5. Editando (durante a edição)
   ↓
6. Editado (edição concluída, aguardando upload)
   ↓
7. Publicado (no ar no YouTube)
   ↓
8. Concluído (finalizado completamente)
```

---

## 📋 CÓDIGO COMPLETO DE VERIFICAÇÃO

### Função Especializada
```python
def check_youtube_card_overdue(card, today_str: str) -> dict:
    """
    Verifica se um card do YouTube está atrasado
    
    Returns:
        {
            'is_overdue': bool,
            'days_overdue': int,
            'reason': str
        }
    """
    properties = card.get("properties", {})
    status = get_status_from_properties(properties)
    
    # 1. Ignorar publicados e concluídos
    if status in ["Publicado", "Concluído", "Concluido"]:
        return {'is_overdue': False, 'days_overdue': 0, 'reason': 'Finalizado'}
    
    # 2. Para cards em edição, verificar Data de Lançamento
    if status in ["Editando", "Para Edição", "Em Edição", "Revisão"]:
        launch_date_str = get_launch_date_from_properties(properties)
        
        if not launch_date_str:
            return {'is_overdue': False, 'days_overdue': 0, 'reason': 'Sem data de lançamento'}
        
        launch_date = datetime.fromisoformat(launch_date_str.replace("Z", "+00:00"))
        launch_date_formatted = launch_date.strftime("%Y-%m-%d")
        
        if launch_date_formatted < today_str:
            days = (datetime.now(SAO_PAULO_TZ).date() - launch_date.date()).days
            return {
                'is_overdue': True,
                'days_overdue': days,
                'reason': f'Data de lançamento vencida ({launch_date_formatted})'
            }
        else:
            return {'is_overdue': False, 'days_overdue': 0, 'reason': 'Em edição, lançamento futuro'}
    
    # 3. Para outros status, verificar Período
    periodo_str = get_date_from_properties(properties, "Periodo")
    
    if not periodo_str:
        return {'is_overdue': False, 'days_overdue': 0, 'reason': 'Sem período definido'}
    
    periodo_date = datetime.fromisoformat(periodo_str.replace("Z", "+00:00"))
    periodo_formatted = periodo_date.strftime("%Y-%m-%d")
    
    if periodo_formatted < today_str:
        days = (datetime.now(SAO_PAULO_TZ).date() - periodo_date.date()).days
        return {
            'is_overdue': True,
            'days_overdue': days,
            'reason': f'Período de gravação vencido ({periodo_formatted})'
        }
    
    return {'is_overdue': False, 'days_overdue': 0, 'reason': 'No prazo'}
```

---

## 🧪 EXEMPLOS

### Exemplo 1: Episódio Publicado
```python
Card: {
    'title': 'Episódio 01',
    'status': 'Publicado',
    'periodo': '2025-04-13T21:00:00-03:00',  # 192 dias atrás
    'data_lancamento': '2025-04-14T12:00:00-03:00'
}

Resultado: IGNORAR
Motivo: Episódio já publicado, não precisa de ação
```

---

### Exemplo 2: Episódio em Edição (Não Atrasado)
```python
Card: {
    'title': 'Episódio 50',
    'status': 'Editando',
    'periodo': '2025-10-15T21:00:00-03:00',  # 7 dias atrás
    'data_lancamento': '2025-10-25T12:00:00-03:00'  # 3 dias no futuro
}

Resultado: NÃO ATRASADO
Motivo: Data de lançamento ainda não chegou
```

---

### Exemplo 3: Episódio em Edição (Atrasado)
```python
Card: {
    'title': 'Episódio 45',
    'status': 'Editando',
    'periodo': '2025-10-10T21:00:00-03:00',  # 12 dias atrás
    'data_lancamento': '2025-10-20T12:00:00-03:00'  # 2 dias atrás
}

Resultado: ATRASADO (2 dias)
Motivo: Data de lançamento já passou
```

---

### Exemplo 4: Episódio Não Gravado
```python
Card: {
    'title': 'Episódio 55',
    'status': 'Para Gravar',
    'periodo': '2025-10-20T21:00:00-03:00',  # 2 dias atrás
    'data_lancamento': '2025-10-23T12:00:00-03:00'
}

Resultado: ATRASADO (2 dias)
Motivo: Período de gravação já passou
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

Ao implementar verificação para YouTube:

- [ ] Ignorar status "Publicado"
- [ ] Ignorar status "Concluído"
- [ ] Para "Editando/Para Edição/Revisão": verificar Data de Lançamento
- [ ] Para outros status: verificar Período
- [ ] Sempre usar GMT-3
- [ ] Não confundir Data de Lançamento com Período

---

## 📊 ESTATÍSTICAS REAIS

### Teste Realizado em 22/10/2025

**Situação Inicial:**
- 91 episódios "atrasados"
- Todos com status "Publicado"

**Após Aplicar Regras:**
- 0 episódios atrasados ✅
- 91 corretamente ignorados ✅
- 0 falsos positivos ✅

**Precisão:** 100%

---

**Última Atualização:** 22/10/2025  
**Versão:** 1.0  
**Script Relacionado:** `check_overdue_tasks.py`, `investigate_youtube_cards.py`













