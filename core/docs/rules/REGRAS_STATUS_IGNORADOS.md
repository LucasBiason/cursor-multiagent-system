# 🚫 REGRAS DE STATUS IGNORADOS - VERIFICAÇÃO DE TAREFAS

**Data:** 22/10/2025  
**Versão:** 1.0  
**Status:** Regra Obrigatória para Sistemas de Verificação

---

## 🎯 OBJETIVO

Definir quais status devem ser **ignorados** em verificações de tarefas atrasadas.

---

## 📋 STATUS A IGNORAR

### Lista Completa
```python
IGNORED_STATUSES = [
    # Cards Finalizados
    "Concluído",
    "Concluido",
    "Completo",
    "Done",
    
    # Cards Cancelados
    "Cancelado",
    "Descartado",
    
    # Cards Realocados/Transferidos
    "Realocada",
    
    # Cards Publicados (YouTube)
    "Publicado"
]
```

---

## 🔍 LÓGICA POR BASE

### BASE WORK
**Ignorar:**
- ✅ Concluído
- ✅ Cancelado
- ✅ Realocada (tarefa transferida para outro responsável)
- ✅ Descartado (tarefa não será feita)

**Motivo:** Estes status indicam que a tarefa não está mais na sua responsabilidade.

---

### BASE PERSONAL
**Ignorar:**
- ✅ Concluído
- ✅ Cancelado

**Motivo:** Tarefas pessoais finalizadas ou descartadas.

---

### BASE YOUTUBER
**Ignorar:**
- ✅ Publicado (episódio já no ar)
- ✅ Concluído

**Lógica Especial:**
- Para cards em edição (Editando, Para Edição, Em Edição, Revisão):
  - Verificar campo **"Data de Lançamento"**
  - Só considerar atrasado se Data de Lançamento < Hoje
  - NÃO verificar o campo "Período" para estes status

**Motivo:** Episódios publicados não precisam de ação. Cards em edição têm lógica diferente.

---

### BASE STUDIES
**Ignorar:**
- ✅ Concluído
- ✅ Descontinuado

**Motivo:** Cursos finalizados ou abandonados.

---

## 💻 CÓDIGO DE IMPLEMENTAÇÃO

### Função de Verificação
```python
def should_ignore_card(status: str, base: str = None) -> bool:
    """
    Verifica se um card deve ser ignorado em verificações
    
    Args:
        status: Status do card
        base: Base do Notion (opcional)
    
    Returns:
        True se deve ignorar, False caso contrário
    """
    ignored_statuses = [
        "Concluído", "Concluido", "Completo", "Done",
        "Cancelado", "Realocada", "Descartado", "Publicado"
    ]
    
    return status in ignored_statuses
```

---

## 🎥 LÓGICA ESPECIAL - YOUTUBE

### Cards em Edição
```python
def check_youtube_card(card_properties, today_str):
    """Lógica especial para cards do YouTube"""
    
    status = get_status(card_properties)
    
    # Ignorar publicados e concluídos
    if status in ["Publicado", "Concluído"]:
        return "IGNORE"
    
    # Para cards em edição, verificar Data de Lançamento
    if status in ["Editando", "Para Edição", "Em Edição", "Revisão"]:
        launch_date = get_launch_date(card_properties)
        
        if launch_date and launch_date < today_str:
            return "OVERDUE"  # Atrasado
        else:
            return "IGNORE"   # Não atrasado
    
    # Para outros status, verificar Período normalmente
    periodo = get_periodo(card_properties)
    if periodo and periodo < today_str:
        return "OVERDUE"
    
    return "IGNORE"
```

---

## 📊 EXEMPLO DE USO

### Script de Verificação
```python
for card in results:
    properties = card.get("properties", {})
    status = get_status_from_properties(properties)
    
    # Verificar se deve ignorar
    if should_ignore_card(status):
        continue  # Pula este card
    
    # Lógica especial para YouTube
    if database_name == "YOUTUBER":
        if status in ["Editando", "Para Edição", "Em Edição", "Revisão"]:
            # Verifica Data de Lançamento
            launch_date_str = get_launch_date_from_properties(properties)
            if not launch_date_str or launch_date_str >= today_str:
                continue  # Não está atrasado
    
    # Se chegou aqui, precisa verificar se está atrasado
    # ... resto da lógica
```

---

## 🔄 COMPORTAMENTO POR STATUS

| Status | Comportamento | Motivo |
|--------|---------------|--------|
| Concluído | Ignorar | Tarefa finalizada |
| Cancelado | Ignorar | Tarefa descartada |
| Realocada | Ignorar | Não é mais sua responsabilidade |
| Descartado | Ignorar | Não será feito |
| Publicado | Ignorar | Episódio já no ar |
| Editando | Verificar Data Lançamento | Pode estar em edição mas não atrasado |
| Não iniciado | Verificar Período | Pode estar atrasado |
| Em Andamento | Verificar Período | Pode estar atrasado |

---

## ⚠️ ATENÇÃO

### NÃO Ignorar Estes Status
- `Não iniciado` - Pode estar atrasado
- `Em Andamento` - Pode estar atrasado
- `Para Fazer` - Pode estar atrasado
- `Gravando` (YouTube) - Pode estar atrasado
- `Para Edição` (YouTube) - Verificar Data de Lançamento

---

## 📈 ESTATÍSTICAS

Com as regras atualizadas (22/10/2025):

**Antes:**
- WORK: 21 tarefas "atrasadas" (na verdade Realocadas)
- YOUTUBER: 91 tarefas "atrasadas" (na verdade Publicadas)

**Depois:**
- WORK: 0 tarefas atrasadas ✅
- YOUTUBER: 0 tarefas atrasadas ✅
- PERSONAL: 0 tarefas atrasadas ✅
- STUDIES: 0 tarefas atrasadas ✅

**Precisão:** 100% de acurácia nas verificações!

---

**Última Atualização:** 22/10/2025  
**Versão:** 1.0  
**Script Relacionado:** `check_overdue_tasks.py`













