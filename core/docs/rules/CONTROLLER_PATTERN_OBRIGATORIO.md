# 🎯 CONTROLLER PATTERN - REGRA OBRIGATÓRIA

**Data**: 04/Dez/2025  
**Versão**: 1.0  
**Aplicável**: TODOS os projetos Python/Django/FastAPI  
**Prioridade**: CRÍTICA

---

## REGRA DE OURO

**TODA lógica de negócio DEVE estar em Controllers!**

**Views, APIs e Commands são APENAS pontos de entrada.**

---

## ARQUITETURA OBRIGATÓRIA

```
Requisição/Comando
      ↓
View/API/Command (Entry Point)
      ↓
Controller (Business Logic)
      ↓
├── Validators (Validação de entrada)
├── Repositories (Acesso a dados/ORM)
├── Services (APIs externas)
└── Utils (Funções auxiliares)
```

---

## RESPONSABILIDADES

### Entry Points (Views/APIs/Commands)
**APENAS**:
- Receber requisição/parâmetros
- Chamar Controller
- Retornar resposta

**NUNCA**:
- Lógica de negócio
- Acesso direto ao ORM
- Validações complexas

### Controllers
**RESPONSÁVEL POR**:
- Toda lógica de negócio
- Orquestração de fluxo
- Chamar Validators
- Chamar Repositories
- Chamar Services
- Tratar exceções
- Retornar resultados

### Validators
**RESPONSÁVEL POR**:
- Validação de entrada
- Regras de validação de negócio
- Retornar erros formatados

### Repositories
**RESPONSÁVEL POR**:
- Acesso ao ORM
- Queries
- CRUD operations

### Services
**RESPONSÁVEL POR**:
- Integração com APIs externas
- Lógica de comunicação externa
- Tratamento de respostas externas

---

## ESTRUTURA DE PASTAS

### Django
```
app_name/
├── models/
├── repositories/
├── validators/
├── controllers/
│   ├── __init__.py
│   └── file_upload_controller.py
├── services/
├── views.py
├── api/
│   └── views.py
└── management/
    └── commands/
```

### FastAPI
```
app/
├── models/
├── repositories/
├── validators/
├── controllers/
│   ├── __init__.py
│   └── file_upload_controller.py
├── services/
└── routers/
```

---

## EXEMPLO COMPLETO

### 1. Command (Entry Point)
```python
from django.core.management.base import BaseCommand
from kpi.controllers import FileUploadController


class Command(BaseCommand):
    help = 'Process pending file uploads'

    def handle(self, *args, **options):
        self.stdout.write("Worker started. Waiting for files...")
        
        while True:
            FileUploadController.process_pending_files()
            time.sleep(5)
```

### 2. Controller (Business Logic)
```python
from typing import Optional, Dict, Any
from kpi.repositories import FileUploadRepository, CompanyRepository
from kpi.validators import FileUploadValidator
from kpi.services import ExcelProcessingService


class FileUploadController:
    """
    Controller para gerenciar uploads de arquivos.
    
    Responsabilidades:
    - Orquestrar o processamento de arquivos
    - Validar dados
    - Chamar repositories
    - Chamar services
    - Tratar exceções
    """
    
    @staticmethod
    def process_pending_files() -> None:
        """Processar arquivos pendentes."""
        pending_files = FileUploadRepository.get_pending()
        
        if not pending_files.exists():
            return
        
        for upload in pending_files:
            FileUploadController.process_single_file(upload.id)
    
    @staticmethod
    def process_single_file(upload_id: str) -> Dict[str, Any]:
        """
        Processar um arquivo específico.
        
        Args:
            upload_id: ID do upload
            
        Returns:
            Dict com resultado do processamento
        """
        upload = FileUploadRepository.get_by_id(upload_id)
        if not upload:
            return {"success": False, "error": "Upload não encontrado"}
        
        # Validar
        validation = FileUploadValidator.validate_file(upload.file)
        if not validation["valid"]:
            FileUploadRepository.update_status(
                upload, 
                'FAILED', 
                validation["error"]
            )
            return {"success": False, "error": validation["error"]}
        
        # Atualizar status
        FileUploadRepository.update_status(upload, 'PROCESSING')
        
        try:
            # Buscar empresa
            company = CompanyRepository.get_first()
            if not company:
                company, _ = CompanyRepository.get_or_create(
                    name="Comunita",
                    slug="comunita"
                )
            
            # Processar arquivo
            result = ExcelProcessingService.process_excel(
                upload.file,
                company.id
            )
            
            if result["success"]:
                FileUploadRepository.update_status(
                    upload,
                    'COMPLETED',
                    result["message"]
                )
            else:
                FileUploadRepository.update_status(
                    upload,
                    'FAILED',
                    result["error"]
                )
            
            return result
            
        except Exception as e:
            FileUploadRepository.update_status(
                upload,
                'FAILED',
                str(e)
            )
            return {"success": False, "error": str(e)}
```

### 3. Validator
```python
from typing import Dict, Any


class FileUploadValidator:
    """Validação de uploads de arquivos."""
    
    @staticmethod
    def validate_file(file) -> Dict[str, Any]:
        """
        Validar arquivo de upload.
        
        Returns:
            Dict com 'valid' (bool) e 'error' (str)
        """
        if not file:
            return {"valid": False, "error": "Arquivo não fornecido"}
        
        if not file.name.endswith(('.xlsx', '.xls')):
            return {
                "valid": False, 
                "error": "Formato inválido. Use .xlsx ou .xls"
            }
        
        if file.size > 50 * 1024 * 1024:
            return {
                "valid": False, 
                "error": "Arquivo muito grande (max 50MB)"
            }
        
        return {"valid": True, "error": None}
```

### 4. Service
```python
from typing import Dict, Any
import pandas as pd


class ExcelProcessingService:
    """Service para processar planilhas Excel."""
    
    @staticmethod
    def process_excel(file, company_id: int) -> Dict[str, Any]:
        """
        Processar planilha Excel.
        
        Args:
            file: Arquivo Excel
            company_id: ID da empresa
            
        Returns:
            Dict com success, message, stats
        """
        try:
            df = pd.read_excel(file)
            
            # Lógica de processamento aqui...
            
            return {
                "success": True,
                "message": "Processado com sucesso",
                "stats": {
                    "total": len(df),
                    "receitas": 100,
                    "despesas": 50
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stats": None
            }
```

### 5. View (Entry Point)
```python
from django.shortcuts import redirect, render
from django.views import View
from kpi.controllers import FileUploadController
from kpi.repositories import FileUploadRepository


class UploadManagerView(View):
    def get(self, request):
        stats = FileUploadRepository.get_stats()
        uploads = FileUploadRepository.get_all_ordered()
        
        context = {"uploads": uploads, "stats": stats}
        return render(request, "upload_manager.html", context)
    
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return self.get(request)
        
        # Chamar Controller
        result = FileUploadController.create_upload(file)
        
        if not result["success"]:
            # Mostrar erro
            pass
        
        return redirect("upload_manager")
```

---

## VIOLAÇÕES COMUNS

### ERRADO 1: Lógica no Command
```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        uploads = FileUpload.objects.filter(status='PENDING')
        for upload in uploads:
            try:
                company = Company.objects.first()
                result = process_excel(upload.file, company.id)
                upload.status = 'COMPLETED'
                upload.save()
            except Exception as e:
                upload.status = 'FAILED'
                upload.save()
```

### CORRETO 1: Apenas Chamada
```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        FileUploadController.process_pending_files()
```

### ERRADO 2: Lógica na View
```python
class UploadView(View):
    def post(self, request):
        file = request.FILES.get("file")
        if not file.name.endswith('.xlsx'):
            return HttpResponse("Erro", status=400)
        
        upload = FileUpload.objects.create(file=file)
        
        try:
            df = pd.read_excel(file)
            # processamento...
        except Exception as e:
            upload.status = 'FAILED'
            upload.save()
```

### CORRETO 2: Apenas Entrada
```python
class UploadView(View):
    def post(self, request):
        file = request.FILES.get("file")
        result = FileUploadController.create_upload(file)
        
        if result["success"]:
            return redirect("success")
        return render(request, "error.html", {"error": result["error"]})
```

---

## BENEFÍCIOS

1. **Separação clara de responsabilidades**
2. **Código testável** - Controllers isolados
3. **Reutilização** - Controllers usados por Views, APIs, Commands
4. **Manutenibilidade** - Lógica centralizada
5. **Escalabilidade** - Fácil adicionar novos entry points

---

## CHECKLIST

- [ ] Controllers criados para cada domínio?
- [ ] Views/APIs são apenas entry points?
- [ ] Commands são apenas entry points?
- [ ] Toda lógica está em Controllers?
- [ ] Controllers chamam Validators?
- [ ] Controllers chamam Repositories?
- [ ] Controllers chamam Services?
- [ ] Sem emojis no código?
- [ ] Sem comentários desnecessários?

---

**ESTE PADRÃO É OBRIGATÓRIO EM TODOS OS PROJETOS!**

