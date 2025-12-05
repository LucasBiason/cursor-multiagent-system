# 📝 NOMENCLATURA: Services vs Processors

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: ALTA

---

## 🎯 REGRA DE OURO

**"Service" = Conexão com API/Sistema Externo. Processamento interno = "Processor".**

---

## ✅ USAR "Service"

### Quando Usar
- Integração com APIs externas
- Conexão com serviços de terceiros
- Cliente de microserviços

### Exemplos Corretos
```python
# ✅ CORRETO - External API
class EmailService:
    """Send emails via SendGrid API."""
    
class PaymentService:
    """Process payments via Stripe API."""
    
class StorageService:
    """Upload files to AWS S3."""
    
class NotificationService:
    """Send push notifications via Firebase."""
```

---

## ✅ USAR "Processor"

### Quando Usar
- Processamento de arquivos
- Transformação de dados (ETL)
- Cálculos complexos
- Parsing de formatos

### Exemplos Corretos
```python
# ✅ CORRETO - Internal processing
class ExcelProcessor:
    """Process Excel files and import data."""
    
class PDFProcessor:
    """Generate PDF reports from data."""
    
class ImageProcessor:
    """Resize and optimize images."""
    
class DataTransformer:
    """Transform data between formats."""
```

---

## 🏗️ ESTRUTURA

```
app/
├── services/              # External integrations
│   ├── email_service.py
│   ├── payment_service.py
│   └── storage_service.py
├── processors/            # Internal processing
│   ├── excel_processor.py
│   ├── pdf_processor.py
│   └── data_transformer.py
├── controllers/           # Business logic orchestration
├── repositories/          # Data access
└── utils/                 # Helpers
```

---

## 📋 NOMENCLATURA COMPLETA

### Services (External)
```
{Integration}Service
- EmailService
- SMSService  
- PaymentService
- StorageService
- SearchService (Elasticsearch)
- CacheService (Redis)
```

### Processors (Internal)
```
{DataType}Processor
- ExcelProcessor
- CSVProcessor
- JSONProcessor
- XMLProcessor
- ImageProcessor
- VideoProcessor
```

### Transformers
```
{Purpose}Transformer
- DataTransformer
- FormatTransformer
- SchemaTransformer
```

### Generators
```
{Output}Generator
- PDFGenerator
- ReportGenerator
- ChartGenerator
- InvoiceGenerator
```

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: Service para Processamento Interno
```python
# ❌ ERRADO
class ExcelService:  # "Service" mas não é API externa
    def process_excel(file):
        # Processa arquivo local
        pass

# ✅ CORRETO
class ExcelProcessor:
    def process_excel(file):
        pass
```

### ❌ Exemplo 2: Processor para API Externa
```python
# ❌ ERRADO
class EmailProcessor:  # "Processor" mas chama API externa
    def send_email(to, subject, body):
        sendgrid_client.send(...)  # API externa!

# ✅ CORRETO
class EmailService:
    def send_email(to, subject, body):
        sendgrid_client.send(...)
```

### ❌ Exemplo 3: Nome Genérico
```python
# ❌ ERRADO
class DataService:  # Genérico demais
class FileService:  # O que faz com arquivo?

# ✅ CORRETO
class ExcelProcessor:     # Específico e claro
class StorageService:     # Integração com storage externo
```

---

## 📚 REFERÊNCIAS

- Controller Pattern: `CONTROLLER_PATTERN_OBRIGATORIO.md`
- Repository Pattern: `REPOSITORY_PATTERN_OBRIGATORIO.md`

---

**Service = External. Processor = Internal.**

