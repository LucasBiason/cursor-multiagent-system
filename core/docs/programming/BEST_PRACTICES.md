# Boas Práticas de Programação - Guia Completo

**Última atualização:** Dezembro 2025  
**Baseado em:** Experiência prática e padrões da comunidade

---

## Sobre Este Guia

Este guia reúne práticas que aprendi trabalhando com Python, Django, FastAPI e desenvolvimento de software em geral. Não são apenas "boas práticas" teóricas - são lições aprendidas na prática, quando projetos crescem e a manutenção fica difícil.

Cada padrão aqui foi testado em projetos reais e provou seu valor quando precisamos escalar, refatorar ou adicionar novas features.

---

## Python

### Type Hints - Não é Opcional

Type hints não são apenas "nice to have". Eles são essenciais para manutenibilidade. Quando você volta a um código depois de meses, type hints te dizem exatamente o que cada função espera e retorna.

```python
# Sem type hints - você precisa ler o código inteiro para entender
def process_data(data, count):
    return []

# Com type hints - fica claro na assinatura
def process_data(data: Dict[str, Any], count: int) -> List[str]:
    """Process data and return list of strings."""
    return []
```

### Docstrings - Documentação Viva

Docstrings são sua documentação. Elas ficam no código, então não ficam desatualizadas como documentação separada.

Use padrão Google Style - é o mais comum e bem suportado por ferramentas:

```python
def calculate_total(items: List[Item], discount: float = 0.0) -> float:
    """Calculate total price with optional discount.
    
    This function sums all item prices and applies discount if provided.
    Used in checkout process and order summary.
    
    Args:
        items: List of items with price attribute
        discount: Discount percentage (0.0 to 1.0). Defaults to 0.0.
        
    Returns:
        Total price after discount
        
    Raises:
        ValueError: If discount is negative or greater than 1.0
        
    Example:
        >>> items = [Item(price=10.0), Item(price=20.0)]
        >>> total = calculate_total(items, discount=0.1)
        >>> print(total)  # 27.0
    """
    if discount < 0 or discount > 1.0:
        raise ValueError("Discount must be between 0.0 and 1.0")
    
    subtotal = sum(item.price for item in items)
    return subtotal * (1 - discount)
```

### Classes vs Funções - Quando Usar Cada Um

Prefira funções quando não há estado. Classes apenas quando você precisa manter estado entre chamadas.

```python
# Função é suficiente - sem estado
def calculate_tax(price: float, rate: float = 0.1) -> float:
    return price * rate

# Classe quando há estado
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, item: Item):
        self.items.append(item)
    
    def get_total(self) -> float:
        return sum(item.price for item in self.items)
```

---

## Django

### Repository Pattern - Centralizar Acesso ao Banco

O problema que o Repository Pattern resolve: quando você precisa mudar uma query, não quer procurar em 10 arquivos diferentes.

```python
# Antes - queries espalhadas
# Em views.py
users = User.objects.filter(is_active=True)

# Em services.py  
user = User.objects.get(id=user_id)

# Em controllers.py
User.objects.create(name="John")

# Depois - tudo centralizado
# Em repositories/user_repository.py
class UserRepository:
    @staticmethod
    def get_active_users():
        return User.objects.filter(is_active=True)
    
    @staticmethod
    def get_by_id(user_id: int):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def create(data: dict):
        return User.objects.create(**data)

# Agora todos usam o repository
users = UserRepository.get_active_users()
user = UserRepository.get_by_id(user_id)
```

### Controller Pattern - Orquestração de Lógica

Controllers orquestram o fluxo. Eles não fazem validação (usam validators), não acessam banco (usam repositories), não enviam emails (usam services). Eles apenas coordenam.

```python
class UserController:
    @staticmethod
    def create_user(data: dict) -> Optional[User]:
        # 1. Validar (delega para validator)
        validation = UserValidator.validate(data)
        if not validation['valid']:
            return None
        
        # 2. Criar (delega para repository)
        user = UserRepository.create(validation['data'])
        
        # 3. Ações adicionais (delega para service)
        EmailService.send_welcome_email(user.email)
        
        # 4. Retornar
        return user
```

### Views - Separação Clara

Template views servem HTML. API views retornam JSON. Nunca misture os dois.

```python
# Template view - apenas HTML
class UserListView(View):
    def get(self, request):
        context = {'total': UserRepository.count_all()}
        return render(request, 'users/list.html', context)

# API view - apenas JSON
class UserListAPIView(APIView):
    def get(self, request):
        users = UserController.list_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
```

---

## FastAPI

### Pydantic - Validação Automática

Pydantic valida automaticamente baseado em type hints. Você define o schema, FastAPI valida automaticamente.

```python
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr  # Validação de email automática
    age: Optional[int] = Field(None, ge=0, le=150)
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v.strip().title()

# FastAPI valida automaticamente
@router.post("/users/")
async def create_user(user_data: UserCreate):
    # user_data já está validado aqui
    user = UserController.create_user(user_data.dict())
    return user
```

### Dependency Injection - Poder do FastAPI

Dependency injection permite reutilizar lógica comum (autenticação, database session) de forma elegante.

```python
# Dependência de database
@router.get("/items")
async def list_items(db: Session = Depends(get_db)):
    return ItemRepository.get_all(db)

# Dependência de autenticação
@router.post("/items")
async def create_item(
    item_data: ItemCreate,
    current_user: User = Depends(get_current_user),  # Automático
    db: Session = Depends(get_db)
):
    # current_user já está validado
    return ItemController.create(item_data.dict(), current_user.id, db)
```

---

## Testes

### TDD - Desenvolvimento Orientado por Testes

TDD parece trabalhoso, mas economiza tempo depois. Você escreve o teste primeiro, depois implementa o mínimo para passar.

```python
# 1. Escrever teste (vai falhar)
def test_validate_email():
    assert validate_email("user@example.com") == True
    assert validate_email("invalid") == False

# 2. Implementar mínimo
def validate_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[1]

# 3. Refatorar e adicionar mais testes
def test_validate_email_edge_cases():
    assert validate_email("") == False
    assert validate_email("@example.com") == False
```

### Cobertura - 80% é Meta, Não Regra

80% de cobertura é uma boa meta, mas qualidade importa mais que quantidade. É melhor ter 70% de testes bem feitos do que 90% de testes ruins.

Teste:
- Validators (lógica de validação)
- Controllers (orquestração)
- Funções complexas (cálculos, transformações)

Não precisa testar:
- Getters/setters simples
- Métodos que apenas chamam outros métodos

---

## Git

### Commits Descritivos

Commits são histórico. Mensagens claras ajudam quando você precisa entender o que mudou e por quê.

```bash
# Bom
git commit -m "feat: adicionar autenticação via JWT"

git commit -m "fix: corrigir validação de email no formulário

A validação estava permitindo emails inválidos.
Agora valida formato e domínio corretamente."

# Ruim
git commit -m "update"
git commit -m "fix"
```

### Feature Branches

Sempre use feature branches. Nunca commite direto em main.

```bash
git checkout -b feature/nome-da-feature
# Desenvolver
git commit -m "feat: implementar feature"
git push origin feature/nome-da-feature
# Criar pull request
```

---

## Docker e DevOps

### Dockerfile - Base Otimizada

Dockerfile bem feito é rápido de build e seguro:

```dockerfile
FROM python:3.11-slim

# Criar usuário não-root (segurança)
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copiar requirements primeiro (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose - Orquestração

Docker Compose organiza todos os serviços:

```yaml
services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy
  
  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
```

### Entrypoint - Inicialização

Entrypoint aguarda dependências e prepara ambiente:

```bash
#!/bin/bash
set -e

# Aguardar banco
until pg_isready -h db; do
  sleep 2
done

# Rodar migrations
python manage.py migrate

# Executar comando
exec "$@"
```

### Makefile - Automação

Makefile documenta e automatiza tarefas:

```makefile
up: ## Inicia serviços
	docker-compose up -d

test: ## Roda testes
	docker-compose exec backend pytest

shell: ## Abre shell
	docker-compose exec backend bash
```

**Documentação completa:** `core/docs/programming/devops/docker-best-practices.md`

---

## Clean Code e Qualidade

### Nomenclatura Descritiva

Nomes ruins são a causa número um de código difícil de entender:

```python
# ❌ Ruim
def process(d):
    return d * 1.1

# ✅ Bom
def calculate_price_with_tax(price: float) -> float:
    """Calculate final price including 10% tax."""
    return price * 1.1
```

### Funções Pequenas

Funções devem ser pequenas. Se tem mais de 20 linhas, provavelmente está fazendo mais de uma coisa:

```python
# ❌ Ruim - função gigante
def process_order(order_data):
    # 50 linhas de código...

# ✅ Bom - funções pequenas
def validate_order_data(data: dict) -> dict:
    pass

def calculate_total(items: list) -> float:
    pass

def create_order(data: dict) -> Order:
    pass
```

### Tratamento de Erros Explícito

Nunca ignorar erros silenciosamente:

```python
# ❌ Ruim
try:
    user = User.objects.get(id=user_id)
except:
    pass

# ✅ Bom
try:
    user = User.objects.get(id=user_id)
except User.DoesNotExist:
    logger.warning(f"User {user_id} not found")
    return None
```

**Documentação completa:** `core/docs/programming/code-quality.md`

---

## Organização de Módulos e Classes

### Uma Classe por Arquivo (Obrigatório)

**Regra Crítica:** Cada classe deve estar em seu próprio arquivo. Nunca colocar múltiplas classes no mesmo arquivo.

**Por quê:**
- Facilita navegação (nome do arquivo = nome da classe)
- Melhora manutenibilidade (mudanças isoladas)
- Simplifica testes (classes testadas separadamente)
- Reduz conflitos em merge (arquivos diferentes)

**Estrutura Recomendada:**
```
module_name/
  __init__.py          # Exporta todas as classes
  base.py              # Classe base (se houver)
  class_a.py           # Classe A
  class_b.py           # Classe B
  class_c.py           # Classe C
```

**Exemplo:**
```python
# ❌ Ruim - múltiplas classes no mesmo arquivo
# generators.py
class ImageGenerator(ABC):
    pass

class GeminiImageGenerator(ImageGenerator):
    pass

class OpenAIDALLEGenerator(ImageGenerator):
    pass

# ✅ Bom - uma classe por arquivo
# generators/
#   __init__.py          # Exporta todas
#   base.py              # ImageGenerator
#   gemini.py            # GeminiImageGenerator
#   openai_dalle.py      # OpenAIDALLEGenerator
```

**Uso do __init__.py:**
```python
# generators/__init__.py
from .base import ImageGenerator
from .gemini import GeminiImageGenerator
from .openai_dalle import OpenAIDALLEGenerator

__all__ = [
    "ImageGenerator",
    "GeminiImageGenerator",
    "OpenAIDALLEGenerator",
]

# Uso - import simples
from generators import DiagramGenerator, GeminiImageGenerator
```

**Exceções:**
Apenas classes muito pequenas e relacionadas podem estar juntas (ex: exceptions, enums, dataclasses simples).

---

### Organização por Domínio - Apps Django Separadas (Obrigatório)

**Regra Crítica:** Cada domínio (entidade de negócio) deve ter sua própria app Django. Nunca misturar múltiplos domínios na mesma app.

**Domínios que SEMPRE devem ter apps próprias:**
- `users/` - Gerenciamento de usuários
- `company/` - Empresas/organizações
- `contracts/` ou `contratos/` - Contratos
- `log/` - Logs de ações/auditoria
- `upload/` - Uploads de arquivos
- `notifications/` - Notificações

**Por quê:**
- Separação clara de responsabilidades
- Facilita manutenção e evolução
- Permite reutilização em outros projetos
- Evita acoplamento desnecessário

**Exemplo:**
```python
# ❌ Ruim - múltiplos domínios na mesma app
# kpi/models.py
class Company(models.Model):  # Deveria estar em company/
    pass

class User(models.Model):  # Deveria estar em users/
    pass

class ActionLog(models.Model):  # Deveria estar em log/
    pass

# ✅ Bom - cada domínio em sua app
# company/models/company.py
class Company(models.Model):
    pass

# users/models/user.py
class User(models.Model):
    pass

# log/models/action_log.py
class ActionLog(models.Model):
    pass
```

**Quando mover um modelo para nova app:**
1. Criar a nova app Django (`python manage.py startapp app_name`)
2. Mover o modelo e seu repository
3. Atualizar TODAS as foreignkeys que referenciam o modelo
4. Atualizar imports em todo o projeto
5. Mover admin registrations para a nova app
6. Mover controllers, validators, serializers relacionados
7. Verificar migrations (pode precisar criar nova migration)

---

## Referências

Estas práticas vêm de:
- Experiência prática em projetos reais
- Clean Code (Robert C. Martin)
- Django Best Practices (documentação oficial)
- FastAPI Documentation (oficial)
- Docker Official Documentation
- Clean Architecture (Robert C. Martin)
- Test-Driven Development (Kent Beck)
- Padrões da comunidade Python

---

**Estas práticas não são teóricas - são lições aprendidas na prática.**

