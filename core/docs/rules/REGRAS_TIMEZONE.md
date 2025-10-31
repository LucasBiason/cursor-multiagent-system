# ⏰ REGRAS DE TIMEZONE - SISTEMA COMPLETO

**Data:** 22/10/2025  
**Versão:** 2.0  
**Status:** Regra Obrigatória

---

## 🎯 REGRA DE OURO

**SEMPRE GMT-3 (São Paulo, Brazil)**  
**NUNCA UTC**

---

## 📋 FORMATO CORRETO

### Com Horário
```python
'start': '2025-10-22T19:00:00-03:00'
'end': '2025-10-22T21:00:00-03:00'
```

### Sem Horário (apenas data)
```python
'start': '2025-10-22'
'end': '2025-10-30'
```

---

## 💻 CÓDIGO PYTHON

### Criar Timezone GMT-3
```python
from datetime import datetime, timezone, timedelta

# Timezone correto
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

# Criar datetime
dt = datetime(2025, 10, 22, 19, 0, 0, tzinfo=SAO_PAULO_TZ)

# Formatar para Notion
data_notion = dt.isoformat()  
# Resultado: '2025-10-22T19:00:00-03:00'
```

### Data Atual em GMT-3
```python
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone(timedelta(hours=-3)))
print(now.strftime('%d/%m/%Y %H:%M'))
```

---

## ⚠️ ERROS COMUNS

### ❌ ERRADO
```python
# UTC
'start': '2025-10-22T22:00:00Z'  # ← Z indica UTC

# Sem timezone
'start': '2025-10-22T19:00:00'   # ← Sem indicação de timezone

# Timezone errado
'start': '2025-10-22T19:00:00+00:00'  # ← +00:00 é UTC
```

### ✅ CORRETO
```python
# GMT-3
'start': '2025-10-22T19:00:00-03:00'  # ← -03:00 é GMT-3
```

---

## 🔍 VALIDAÇÃO

### Função de Validação
```python
def validar_timezone(data_str: str) -> bool:
    """Valida se a data está em GMT-3"""
    if 'T' in data_str:  # Se tem horário
        if '-03:00' not in data_str:
            raise ValueError(f"Data {data_str} não está em GMT-3!")
    return True
```

---

## 📊 QUANDO USAR HORÁRIO

| Tipo de Card | Incluir Horário? | Exemplo |
|--------------|------------------|---------|
| Aula (STUDIES) | ✅ Sim | `2025-10-22T19:00:00-03:00` |
| Seção/Módulo | ❌ Não | `2025-10-22` |
| Curso | ❌ Não | `2025-10-22` |
| Episódio YouTube | ✅ Sim | `2025-10-22T21:00:00-03:00` |
| Série YouTube | ✅ Sim | `2025-10-22T21:00:00-03:00` |
| Tarefa Trabalho | ✅ Sim | `2025-10-22T09:00:00-03:00` |
| Tarefa Pessoal | ✅ Sim | `2025-10-22T19:00:00-03:00` |

---

## ✅ CHECKLIST

Antes de criar qualquer card:

- [ ] Data tem timezone `-03:00` se incluir horário
- [ ] Horário apenas onde necessário
- [ ] Nunca usar UTC (Z ou +00:00)
- [ ] Sempre usar `timezone(timedelta(hours=-3))`

---

**Última Atualização:** 22/10/2025  
**Autor:** Sistema de Automação Notion













