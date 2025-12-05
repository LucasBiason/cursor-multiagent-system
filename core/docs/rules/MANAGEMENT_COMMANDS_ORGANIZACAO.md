# 🔧 MANAGEMENT COMMANDS - ORGANIZAÇÃO

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: MÉDIA

---

## 🎯 REGRA DE OURO

**Commands específicos de app → app/management/commands/**  
**Commands globais do sistema → core/management/commands/**

---

## 📁 ESTRUTURA

```
project/
├── core/
│   └── management/
│       └── commands/
│           ├── run_scheduler.py      # Run ALL background jobs
│           ├── health_check.py       # System health check
│           └── clear_cache.py        # Clear all caches
├── app1/
│   └── management/
│       └── commands/
│           ├── populate_app1_data.py  # App-specific data
│           ├── validate_app1.py       # App-specific validation
│           └── import_app1.py         # App-specific import
└── app2/
    └── management/
        └── commands/
            └── process_app2.py         # App-specific processing
```

---

## ✅ COMMANDS ÚTEIS (MANTER)

### Setup/Inicialização
```python
# app/management/commands/populate_{entity}_data.py
"""
Populate initial data for {entity}.
Useful for: setup, migrations, testing.
"""
```

### Validação/QA
```python
# app/management/commands/validate_{entity}.py
"""
Validate data integrity for {entity}.
Useful for: QA, debugging, data auditing.
"""
```

### Import/ETL (Dev/Debug)
```python
# app/management/commands/test_import.py
"""
Test import process with sample data.
Useful for: development, debugging, testing new ETL logic.
"""
```

### Background Jobs
```python
# core/management/commands/run_scheduler.py
"""
Run ALL background schedulers from all apps.
Useful for: production, worker containers.
"""
```

---

## ❌ COMMANDS INÚTEIS (REMOVER)

### Duplicados
```python
# ❌ app1/management/commands/run_scheduler.py
# ❌ app2/management/commands/run_jobs.py
# ✅ core/management/commands/run_scheduler.py (único)
```

### One-time Scripts
```python
# ❌ management/commands/fix_data_once.py
# ✅ Mover para scripts/ e deletar após uso
```

### Development Hacks
```python
# ❌ management/commands/quick_test.py
# ✅ Usar pytest ou django test
```

---

## 🔧 TEMPLATE: run_scheduler.py (Core)

```python
"""
Management command to run all background schedulers.
Centralizes all background jobs from different apps.
"""
import time
import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Run all background schedulers (APScheduler jobs from all apps)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting all schedulers..."))

        schedulers_started = []

        # Import and start schedulers from each app
        try:
            from kpi import scheduler as kpi_scheduler
            kpi_scheduler.start()
            schedulers_started.append('kpi')
            self.stdout.write(self.style.SUCCESS("  [OK] KPI scheduler started"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  [WARN] KPI scheduler failed: {e}"))

        # Add more app schedulers here
        # try:
        #     from dashboard import scheduler
        #     scheduler.start()
        #     schedulers_started.append('dashboard')
        # except:
        #     pass

        if not schedulers_started:
            self.stdout.write(self.style.ERROR("[ERROR] No schedulers started!"))
            return

        self.stdout.write(self.style.SUCCESS(
            f"\n[SUCCESS] {len(schedulers_started)} scheduler(s) running"
        ))

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n[STOP] Shutting down..."))
```

---

## 📋 CHECKLIST DE COMMANDS

### Antes de Criar Command

- [ ] É útil para setup/manutenção?
- [ ] Será usado mais de uma vez?
- [ ] É específico de uma app ou global?
- [ ] Já existe command similar?

### Depois de Criar

- [ ] Docstring clara com propósito
- [ ] Help text informativo
- [ ] Argumentos documentados
- [ ] Tratamento de erros
- [ ] Mensagens com self.style

### Revisão Periódica

- [ ] Command ainda é usado?
- [ ] Pode ser substituído por migration?
- [ ] Pode ser script one-time?
- [ ] Está no diretório correto?

---

## 🗂️ ORGANIZAÇÃO POR TIPO

### Core Commands
```
core/management/commands/
├── run_scheduler.py       # Background jobs
├── health_check.py        # System health
├── clear_cache.py         # Clear all caches
└── db_backup.py           # Database backup
```

### App Commands
```
app/management/commands/
├── populate_data.py       # Initial data
├── validate_data.py       # Data validation
├── import_legacy.py       # Legacy import
└── export_report.py       # Data export
```

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: Scheduler em App
```python
# ❌ ERRADO
kpi/management/commands/run_scheduler.py  # Específico de app

# ✅ CORRETO
core/management/commands/run_scheduler.py  # Central, importa de todas apps
```

### ❌ Exemplo 2: Script One-Time
```python
# ❌ ERRADO
# management/commands/migrate_old_format_2024.py
# Usado uma vez e nunca mais

# ✅ CORRETO
# scripts/migrate_old_format_2024.py
# Executar e deletar
```

### ❌ Exemplo 3: Lógica no Command
```python
# ❌ ERRADO
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 200 linhas de lógica de negócio

# ✅ CORRETO
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Apenas chamadas para controllers/services
        Controller.process_data()
```

---

**CORE = GLOBAL. APP = ESPECÍFICO. DELETE = INÚTIL.**

