# ✅ VALIDATORS - CAMADA OBRIGATÓRIA

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: CRÍTICA

---

## 🎯 REGRA DE OURO

**Controllers NUNCA fazem validação inline. SEMPRE usam classes Validator.**

---

## 📁 ESTRUTURA OBRIGATÓRIA

```
app/
├── api/
│   └── validators.py          # Validators para APIs
├── controllers/
│   └── {model}_controller.py  # Usa validators
└── repositories/
    └── {model}_repository.py  # Não valida, apenas persiste
```

---

## 📝 TEMPLATE DE VALIDATOR

```python
# app/api/validators.py

class FileUploadValidator:
    """Validates file upload data."""
    
    @staticmethod
    def validate_file(file_obj):
        """
        Validate uploaded file.
        
        Args:
            file_obj: Django UploadedFile object
            
        Returns:
            dict: {'valid': bool, 'error': str|None, 'data': dict}
        """
        errors = []
        
        # Check if file exists
        if not file_obj:
            return {
                'valid': False,
                'error': 'No file provided',
                'data': None
            }
        
        # Check file extension
        allowed_extensions = ['.xlsx', '.xls']
        file_ext = file_obj.name.split('.')[-1].lower()
        
        if f'.{file_ext}' not in allowed_extensions:
            errors.append(f'Invalid file type. Allowed: {", ".join(allowed_extensions)}')
        
        # Check file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        if file_obj.size > max_size:
            errors.append(f'File too large. Max size: 50MB')
        
        # Check if file is readable
        try:
            file_obj.seek(0)
        except Exception as e:
            errors.append(f'Cannot read file: {str(e)}')
        
        if errors:
            return {
                'valid': False,
                'error': '; '.join(errors),
                'data': None
            }
        
        return {
            'valid': True,
            'error': None,
            'data': {
                'filename': file_obj.name,
                'size': file_obj.size,
                'content_type': file_obj.content_type
            }
        }
```

---

## 🎯 RESPONSABILIDADES

### Validators
✅ **Validar tipos** de dados  
✅ **Validar formatos** (extensões, regex)  
✅ **Validar tamanhos** (min, max)  
✅ **Validar regras** de negócio simples  
✅ **Retornar** `{'valid': bool, 'error': str, 'data': dict}`

❌ **NUNCA** acessar banco de dados  
❌ **NUNCA** fazer persistência  
❌ **NUNCA** fazer lógica complexa

### Controllers (usando Validators)
```python
# controllers/file_upload_controller.py

from ..api.validators import FileUploadValidator
from ..repositories import FileUploadRepository

class FileUploadController:
    
    @staticmethod
    def create_upload(file_obj):
        """
        Create new file upload.
        
        Flow: Validate → Repository → Return
        """
        # 1. Validate
        validation = FileUploadValidator.validate_file(file_obj)
        
        if not validation['valid']:
            return {
                'success': False,
                'error': validation['error'],
                'upload': None
            }
        
        # 2. Repository
        try:
            upload = FileUploadRepository.create(
                file=file_obj,
                status='PENDING'
            )
        except Exception as e:
            return {
                'success': False,
                'error': f'Database error: {str(e)}',
                'upload': None
            }
        
        # 3. Return
        return {
            'success': True,
            'error': None,
            'upload': upload
        }
```

---

## 🔍 TIPOS DE VALIDAÇÃO

### 1. Validação de Formato
```python
@staticmethod
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return {'valid': False, 'error': 'Invalid email format'}
    return {'valid': True, 'error': None}
```

### 2. Validação de Range
```python
@staticmethod
def validate_year(year):
    current_year = datetime.now().year
    if year < 2020 or year > current_year + 1:
        return {'valid': False, 'error': f'Year must be between 2020 and {current_year + 1}'}
    return {'valid': True, 'error': None}
```

### 3. Validação de Lista
```python
@staticmethod
def validate_months(months):
    if not isinstance(months, list):
        return {'valid': False, 'error': 'Months must be a list'}
    
    for month in months:
        if month < 1 or month > 12:
            return {'valid': False, 'error': f'Invalid month: {month}'}
    
    return {'valid': True, 'error': None}
```

### 4. Validação de Dependências
```python
@staticmethod
def validate_date_range(start_date, end_date):
    if end_date < start_date:
        return {'valid': False, 'error': 'End date must be after start date'}
    
    max_range = timedelta(days=365)
    if (end_date - start_date) > max_range:
        return {'valid': False, 'error': 'Date range cannot exceed 1 year'}
    
    return {'valid': True, 'error': None}
```

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: Validação no Controller
```python
# ❌ ERRADO
class FileUploadController:
    @staticmethod
    def create_upload(file_obj):
        # Validação inline ❌
        if not file_obj:
            return {'success': False, 'error': 'No file'}
        
        if file_obj.size > 50*1024*1024:
            return {'success': False, 'error': 'Too large'}
        
        upload = FileUploadRepository.create(file=file_obj)
        return {'success': True, 'upload': upload}

# ✅ CORRETO
class FileUploadController:
    @staticmethod
    def create_upload(file_obj):
        # Delega validação ✅
        validation = FileUploadValidator.validate_file(file_obj)
        
        if not validation['valid']:
            return {'success': False, 'error': validation['error']}
        
        upload = FileUploadRepository.create(file=file_obj)
        return {'success': True, 'upload': upload}
```

### ❌ Exemplo 2: Validação na View
```python
# ❌ ERRADO
class UploadAPIView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        
        # Validação na view ❌
        if not file.name.endswith('.xlsx'):
            return Response({'error': 'Invalid'}, status=400)
        
        result = FileUploadController.create_upload(file)
        return Response(result)

# ✅ CORRETO
class UploadAPIView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        
        # Controller faz validação via Validator ✅
        result = FileUploadController.create_upload(file)
        
        if not result['success']:
            return Response({'error': result['error']}, status=400)
        
        serializer = FileUploadSerializer(result['upload'])
        return Response(serializer.data, status=201)
```

---

## ✅ CHECKLIST

### Estrutura
- [ ] `api/validators.py` existe
- [ ] Cada model tem seu Validator
- [ ] Controllers usam Validators
- [ ] Views não fazem validação

### Validator
- [ ] Métodos estáticos
- [ ] Retorna dict `{'valid', 'error', 'data'}`
- [ ] Não acessa banco
- [ ] Não faz persistência
- [ ] Apenas valida dados

### Controller
- [ ] Chama Validator primeiro
- [ ] Trata resultado de validação
- [ ] Retorna dict padronizado
- [ ] Não faz validação inline

---

**VALIDATORS = INPUT VALIDATION. CONTROLLERS = ORCHESTRATION.**

