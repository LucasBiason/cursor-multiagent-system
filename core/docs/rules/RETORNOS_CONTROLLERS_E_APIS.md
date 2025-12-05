# 📤 RETORNOS: Controllers e APIs

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: CRÍTICA

---

## 🎯 REGRA DE OURO

**Controllers retornam OBJETOS. APIs serializam e definem HTTP status.**

---

## ✅ PADRÃO OBRIGATÓRIO

### Controllers (Business Logic)

**INSERT/CREATE**:
```python
# ✅ CORRETO - Retorna objeto ou None
def create_upload(file_obj):
    validation = Validator.validate(file_obj)
    if not validation['valid']:
        return None  # Ou raise ValidationError
    
    upload = Repository.create(file=file_obj)
    return upload  # Retorna o objeto criado
```

**UPDATE**:
```python
# ✅ CORRETO - Retorna objeto atualizado
def update_status(upload_id, new_status):
    upload = Repository.get_by_id(upload_id)
    if not upload:
        return None
    
    upload.status = new_status
    Repository.save(upload)
    return upload  # Retorna o objeto atualizado
```

**DELETE**:
```python
# ✅ CORRETO - Retorna None ou booleano
def delete_upload(upload_id):
    upload = Repository.get_by_id(upload_id)
    if not upload:
        return False
    
    Repository.delete(upload)
    return True  # Ou None
```

**LIST**:
```python
# ✅ CORRETO - Retorna QuerySet ou lista de objetos
def list_uploads(filters):
    return Repository.filter(**filters)  # QuerySet
```

**RETRIEVE**:
```python
# ✅ CORRETO - Retorna objeto ou None
def get_upload(upload_id):
    return Repository.get_by_id(upload_id)  # Objeto ou None
```

---

## 🔌 API Views (Serialização e Status)

### POST (CREATE) - 201 Created
```python
class CreateAPIView(APIView):
    def post(self, request):
        file_obj = request.FILES.get('file')
        
        # Controller retorna objeto ou None
        upload = FileUploadController.create_upload(file_obj)
        
        if not upload:
            return Response(
                {'error': 'Validation failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Serializar objeto
        serializer = FileUploadSerializer(upload, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

### GET (LIST) - 200 OK
```python
class ListAPIView(APIView):
    def get(self, request):
        # Controller retorna QuerySet ou lista
        uploads = FileUploadController.list_uploads(request.GET.dict())
        
        # Serializar
        serializer = FileUploadSerializer(uploads, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### GET (RETRIEVE) - 200 OK ou 404 Not Found
```python
class DetailAPIView(APIView):
    def get(self, request, upload_id):
        # Controller retorna objeto ou None
        upload = FileUploadController.get_upload(upload_id)
        
        if not upload:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serializar
        serializer = FileUploadSerializer(upload, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### PUT/PATCH (UPDATE) - 200 OK ou 404 Not Found
```python
class UpdateAPIView(APIView):
    def patch(self, request, upload_id):
        # Controller retorna objeto atualizado ou None
        upload = FileUploadController.update_upload(upload_id, request.data)
        
        if not upload:
            return Response(
                {'error': 'Not found or validation failed'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serializar
        serializer = FileUploadSerializer(upload, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### DELETE - 204 No Content ou 404 Not Found
```python
class DeleteAPIView(APIView):
    def delete(self, request, upload_id):
        # Controller retorna True/False ou None
        deleted = FileUploadController.delete_upload(upload_id)
        
        if not deleted:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Sem conteúdo
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: Controller com Dict de Status
```python
# ❌ ERRADO
def create_upload(file_obj):
    upload = Repository.create(file=file_obj)
    return {
        'success': True,  # ❌ Não precisa
        'message': 'Created',  # ❌ Não precisa
        'upload': upload,
        'error': None  # ❌ Não precisa
    }

# ✅ CORRETO
def create_upload(file_obj):
    validation = Validator.validate(file_obj)
    if not validation['valid']:
        return None  # Ou raise exception
    
    upload = Repository.create(file=file_obj)
    return upload  # Apenas o objeto
```

### ❌ Exemplo 2: API sem Serializer
```python
# ❌ ERRADO
def post(self, request):
    upload = Controller.create_upload(file)
    return Response({
        'id': upload.id,  # Serialização manual
        'status': upload.status
    }, status=201)

# ✅ CORRETO
def post(self, request):
    upload = Controller.create_upload(file)
    if not upload:
        return Response({'error': 'Failed'}, status=400)
    
    serializer = FileUploadSerializer(upload, context={'request': request})
    return Response(serializer.data, status=201)
```

### ❌ Exemplo 3: Controller Define HTTP Status
```python
# ❌ ERRADO
def create_upload(file_obj):
    if not file_obj:
        return {'status': 400, 'error': 'No file'}  # ❌
    
    upload = Repository.create(file=file_obj)
    return {'status': 201, 'data': upload}  # ❌

# ✅ CORRETO
def create_upload(file_obj):
    if not file_obj:
        return None  # API decide status
    
    upload = Repository.create(file=file_obj)
    return upload  # API decide status
```

---

## 📋 TABELA DE RETORNOS

| Operação | Controller Retorna | API Status | API Response |
|----------|-------------------|------------|--------------|
| **CREATE** | Objeto ou None | 201 Created ou 400 Bad Request | Serializer(objeto).data |
| **UPDATE** | Objeto ou None | 200 OK ou 404 Not Found | Serializer(objeto).data |
| **DELETE** | True/False/None | 204 No Content ou 404 Not Found | Vazio |
| **LIST** | QuerySet/List | 200 OK | Serializer(lista, many=True).data |
| **RETRIEVE** | Objeto ou None | 200 OK ou 404 Not Found | Serializer(objeto).data |

---

## ✅ CHECKLIST

### Controller
- [ ] Retorna objeto (não dict com 'success')
- [ ] Retorna None em caso de falha (não dict com 'error')
- [ ] Não define HTTP status
- [ ] Não cria mensagens de resposta
- [ ] Foca em lógica de negócio

### API View
- [ ] Verifica se controller retornou None
- [ ] Define HTTP status apropriado
- [ ] Usa serializer para resposta
- [ ] Cria mensagens de erro quando necessário
- [ ] Não faz lógica de negócio

---

## 🔄 TRATAMENTO DE ERROS

### Controller - Exceptions
```python
def create_upload(file_obj):
    validation = Validator.validate(file_obj)
    if not validation['valid']:
        # Opção 1: Retornar None
        return None
        
        # Opção 2: Raise exception (preferível)
        raise ValidationError(validation['error'])
    
    upload = Repository.create(file=file_obj)
    return upload
```

### API View - HTTP Status
```python
def post(self, request):
    try:
        upload = Controller.create_upload(file)
        
        if not upload:
            return Response({'error': 'Validation failed'}, status=400)
        
        serializer = Serializer(upload, context={'request': request})
        return Response(serializer.data, status=201)
        
    except ValidationError as e:
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return Response({'error': 'Internal error'}, status=500)
```

---

**CONTROLLERS = OBJETOS. APIs = SERIALIZAÇÃO + STATUS.**

