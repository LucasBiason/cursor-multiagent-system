# 🔒 SQL PURO - APENAS PARA SELECT

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: CRÍTICA - SEGURANÇA

---

## 🎯 REGRA DE OURO

**SQL puro APENAS para SELECT. INSERT/UPDATE/DELETE via ORM + Repository.**

---

## ✅ PERMITIDO

### SELECT Queries (Otimização)
```python
from app.utils.database import execute_query

# Read-only queries via database.py
results = execute_query(
    """
    SELECT u.name, SUM(r.amount) as total
    FROM units u
    JOIN revenues r ON u.id = r.unit_id
    WHERE u.company_id = %s
    GROUP BY u.name
    """,
    [company_id]
)
```

**Razão**: Performance otimizada, agregações complexas.

---

## ❌ PROIBIDO

### INSERT via SQL Puro
```python
# ❌ NUNCA FAZER
cursor.execute("""
    INSERT INTO fato_receita (valor, data, projeto_id)
    VALUES (%s, %s, %s)
""", [valor, data, projeto_id])

# ✅ CORRETO - Via ORM + Repository
FatoReceitaRepository.create(
    valor=valor,
    data=data,
    projeto_id=projeto_id
)
```

### UPDATE via SQL Puro
```python
# ❌ NUNCA FAZER
cursor.execute("""
    UPDATE file_upload SET status = %s WHERE id = %s
""", ['COMPLETED', upload_id])

# ✅ CORRETO - Via ORM + Repository
FileUploadRepository.update_status(upload, 'COMPLETED')
```

### DELETE via SQL Puro
```python
# ❌ NUNCA FAZER
cursor.execute("DELETE FROM fato_receita WHERE data < %s", [old_date])

# ✅ CORRETO - Via ORM + Repository
FatoReceitaRepository.delete_older_than(old_date)
```

---

## 🛡️ RAZÕES DE SEGURANÇA

### 1. SQL Injection
```python
# ❌ VULNERÁVEL
query = f"INSERT INTO table VALUES ('{user_input}')"
cursor.execute(query)

# ✅ SEGURO
Repository.create(value=user_input)  # ORM sanitiza
```

### 2. Validação
```python
# ❌ SEM VALIDAÇÃO
cursor.execute("INSERT INTO table (email) VALUES (%s)", [email])

# ✅ COM VALIDAÇÃO
# Model valida, Repository usa ORM
FatoReceitaRepository.create(email=email)
```

### 3. Auditoria
```python
# ❌ SEM RASTREAMENTO
cursor.execute("UPDATE table SET value = %s", [new_value])

# ✅ COM AUDITORIA
# Django signals, updated_at, modified_by
Repository.update(obj, value=new_value)
```

### 4. Integridade
```python
# ❌ SEM CONSTRAINTS
cursor.execute("DELETE FROM parent WHERE id = %s", [id])
# Filhos órfãos!

# ✅ COM CASCADE
# Django ORM respeita ON DELETE CASCADE
ParentRepository.delete(parent)
```

---

## 📁 MÓDULO database.py

### Localização
```
app/
└── utils/
    └── database.py  # Módulo compartilhado para SQL puro
```

### Uso Correto
```python
from app.utils.database import execute_query

class FatoReceitaRepository:
    
    @staticmethod
    def get_aggregated_by_month(year):
        """
        Complex aggregation - use raw SQL for performance.
        READ-ONLY operation.
        """
        query = """
            SELECT 
                EXTRACT(MONTH FROM data) as month,
                SUM(valor_receita) as total
            FROM fato_receita
            WHERE EXTRACT(YEAR FROM data) = %s
            GROUP BY EXTRACT(MONTH FROM data)
            ORDER BY month
        """
        return execute_query(query, [year])
    
    @staticmethod
    def create(valor, data, projeto_id):
        """
        Insert via ORM - NEVER use raw SQL.
        """
        from app.models import FatoReceita
        
        return FatoReceita.objects.create(
            valor_receita=valor,
            data=data,
            projeto_id=projeto_id
        )
```

---

## 🔧 TEMPLATE database.py

```python
"""
Database utilities for raw SQL queries.
ONLY for SELECT operations - never use for INSERT/UPDATE/DELETE.
"""
from django.db import connection
from typing import List, Dict, Any


def execute_query(query: str, params: List[Any] = None) -> List[Dict[str, Any]]:
    """
    Execute read-only SQL query.
    
    Args:
        query: SQL SELECT query
        params: Query parameters (for %s placeholders)
        
    Returns:
        List of dictionaries with results
        
    Example:
        results = execute_query(
            "SELECT id, name FROM users WHERE status = %s",
            ['active']
        )
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def execute_scalar(query: str, params: List[Any] = None) -> Any:
    """
    Execute query and return single value.
    
    Example:
        count = execute_scalar("SELECT COUNT(*) FROM users")
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        result = cursor.fetchone()
        return result[0] if result else None
```

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: INSERT Direto
```python
# ❌ ERRADO
with connection.cursor() as cursor:
    cursor.execute("""
        INSERT INTO fato_receita (valor, data)
        VALUES (%s, %s)
    """, [1000, '2024-12-05'])

# ✅ CORRETO
FatoReceitaRepository.create(
    valor_receita=1000,
    data='2024-12-05'
)
```

### ❌ Exemplo 2: UPDATE em Loop
```python
# ❌ ERRADO
for item in items:
    cursor.execute("""
        UPDATE fato_despesa 
        SET classificacao = %s 
        WHERE id = %s
    """, [item.classif, item.id])

# ✅ CORRETO
for item in items:
    FatoDespesaRepository.update_classificacao(item.id, item.classif)

# OU (bulk update)
FatoDespesaRepository.bulk_update_classificacao(items)
```

### ❌ Exemplo 3: Buscar ID via SQL para Inserir
```python
# ❌ ERRADO
cursor.execute("SELECT id FROM dim_projeto WHERE nome = %s", [name])
projeto_id = cursor.fetchone()[0]

cursor.execute("""
    INSERT INTO fato_receita (projeto_id, valor)
    VALUES (%s, %s)
""", [projeto_id, valor])

# ✅ CORRETO
projeto = DimProjetoRepository.get_by_name(name)
FatoReceitaRepository.create(
    projeto_id=projeto.projeto_id,
    valor_receita=valor
)
```

---

## ✅ CHECKLIST

### Ao Escrever Código com Banco

- [ ] É SELECT? → Pode usar SQL puro (via database.py)
- [ ] É INSERT/UPDATE/DELETE? → DEVE usar ORM + Repository
- [ ] SQL puro tem parâmetros? → Usar %s (nunca f-string)
- [ ] Está em repository? → OK
- [ ] Está fora de repository? → MOVER para repository

### Ao Revisar Código

- [ ] Nenhum `cursor.execute` com INSERT/UPDATE/DELETE
- [ ] Nenhum `.objects.create()` fora de repository
- [ ] Nenhum `.objects.filter()` para modificar dados
- [ ] SQL puro apenas em métodos de repository
- [ ] Todos os INSERTs via ORM

---

## 📚 REFERÊNCIAS

- Repository Pattern: `REPOSITORY_PATTERN_OBRIGATORIO.md`
- Controller Pattern: `CONTROLLER_PATTERN_OBRIGATORIO.md`
- Database Utils: `{project}/app/utils/database.py`

---

**SELECT = SQL Puro (performance). INSERT/UPDATE/DELETE = ORM (segurança).**

