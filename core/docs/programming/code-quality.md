# Clean Code e Code Quality - Boas Práticas

**Última atualização:** Dezembro 2025  
**Baseado em:** Experiência prática e princípios de Clean Code

---

## Por que Clean Code?

Código limpo não é apenas "bonito". É código que:
- **Outras pessoas conseguem entender** rapidamente
- **Você consegue entender** quando voltar depois de meses
- **É fácil de modificar** sem quebrar outras partes
- **Tem menos bugs** porque é mais claro

A diferença entre código limpo e código "funcional" é a diferença entre um projeto que escala e um que vira uma bagunça impossível de manter.

---

## Nomenclatura - Nomes que Falam por Si

### O Problema Real

Nomes ruins são a causa número um de código difícil de entender. Quando você lê `x`, `temp`, `data`, você não sabe o que é. Quando você lê `user_email`, `total_price`, `is_active`, fica claro.

### Regras de Ouro

**1. Nomes Descritivos**

```python
# ❌ Ruim - não diz nada
def process(d):
    return d * 1.1

# ✅ Bom - fica claro o que faz
def calculate_price_with_tax(price: float) -> float:
    """Calculate final price including 10% tax."""
    return price * 1.1
```

**2. Evitar Abreviações**

```python
# ❌ Ruim - abreviação confusa
def calc_usr_tot(usr_id):
    pass

# ✅ Bom - nome completo
def calculate_user_total(user_id: int) -> float:
    pass
```

**3. Nomes de Funções são Verbos**

```python
# ✅ Bom - função faz algo
def get_user_by_id(user_id: int) -> User:
    pass

def validate_email(email: str) -> bool:
    pass

def send_notification(message: str) -> None:
    pass
```

**4. Nomes de Classes são Substantivos**

```python
# ✅ Bom - classe representa algo
class UserRepository:
    pass

class EmailValidator:
    pass

class PaymentProcessor:
    pass
```

**5. Booleanos são Perguntas**

```python
# ✅ Bom - lê como pergunta
is_active: bool
has_permission: bool
can_edit: bool

# ❌ Ruim - não é claro
active: bool  # É ativo? Está ativo? Ativa algo?
```

### Convenções Python

```python
# Variáveis e funções: snake_case
user_name = "João"
def calculate_total():
    pass

# Classes: PascalCase
class UserController:
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Privado (convenção): _leading_underscore
def _internal_helper():
    pass
```

---

## Funções - Pequenas e com Uma Responsabilidade

### A Regra dos 20 Linhas

Funções devem ser pequenas. Se uma função tem mais de 20 linhas, provavelmente está fazendo mais de uma coisa.

```python
# ❌ Ruim - função gigante fazendo tudo
def process_order(order_data):
    # Validar dados
    if not order_data.get('items'):
        return {'error': 'No items'}
    if not order_data.get('customer_id'):
        return {'error': 'No customer'}
    
    # Calcular total
    total = 0
    for item in order_data['items']:
        total += item['price'] * item['quantity']
    
    # Aplicar desconto
    if order_data.get('discount_code'):
        discount = calculate_discount(order_data['discount_code'])
        total = total * (1 - discount)
    
    # Criar pedido
    order = Order.objects.create(
        customer_id=order_data['customer_id'],
        total=total
    )
    
    # Enviar email
    send_order_confirmation(order.id)
    
    return {'order_id': order.id}

# ✅ Bom - funções pequenas, cada uma faz uma coisa
def validate_order_data(order_data: dict) -> dict:
    """Validate order data and return validation result."""
    if not order_data.get('items'):
        return {'valid': False, 'error': 'No items'}
    if not order_data.get('customer_id'):
        return {'valid': False, 'error': 'No customer'}
    return {'valid': True, 'error': None}

def calculate_order_total(items: list, discount_code: str = None) -> float:
    """Calculate total price with optional discount."""
    total = sum(item['price'] * item['quantity'] for item in items)
    if discount_code:
        discount = calculate_discount(discount_code)
        total = total * (1 - discount)
    return total

def create_order(customer_id: int, total: float) -> Order:
    """Create order in database."""
    return Order.objects.create(
        customer_id=customer_id,
        total=total
    )

def process_order(order_data: dict) -> dict:
    """Process order: validate, calculate, create, notify."""
    # Validar
    validation = validate_order_data(order_data)
    if not validation['valid']:
        return {'error': validation['error']}
    
    # Calcular
    total = calculate_order_total(
        order_data['items'],
        order_data.get('discount_code')
    )
    
    # Criar
    order = create_order(order_data['customer_id'], total)
    
    # Notificar
    send_order_confirmation(order.id)
    
    return {'order_id': order.id}
```

### Uma Função, Uma Coisa

Cada função deve fazer apenas uma coisa. Se você consegue descrever o que a função faz sem usar "e" ou "ou", ela provavelmente está fazendo uma coisa só.

```python
# ❌ Faz duas coisas: valida E cria
def validate_and_create_user(data):
    if not data.get('email'):
        return None
    return User.objects.create(**data)

# ✅ Faz uma coisa: valida
def validate_user_data(data: dict) -> dict:
    if not data.get('email'):
        return {'valid': False, 'error': 'Email required'}
    return {'valid': True, 'data': data}

# ✅ Faz uma coisa: cria
def create_user(data: dict) -> User:
    return User.objects.create(**data)

# Uso
validation = validate_user_data(data)
if validation['valid']:
    user = create_user(validation['data'])
```

---

## Comentários - Quando e Como

### Comentários são um Aviso

Comentários são necessários quando o código não é auto-explicativo. Mas se você precisa de muitos comentários, talvez o código precise ser mais claro.

### ❌ Comentários Ruins

```python
# Incrementa i
i += 1

# Loop pelos usuários
for user in users:
    pass

# Retorna o usuário
return user
```

Esses comentários não ajudam. O código já diz isso.

### ✅ Comentários Úteis

```python
# Aguardar 2 segundos para evitar rate limit da API
time.sleep(2)

# Ordenar por data mais recente primeiro (mais relevante para usuário)
users.sort(key=lambda u: u.created_at, reverse=True)

# Usar cache se disponível, senão buscar do banco
# Cache expira em 5 minutos para balancear performance e dados atualizados
user = cache.get(f'user:{user_id}')
if not user:
    user = UserRepository.get_by_id(user_id)
    cache.set(f'user:{user_id}', user, timeout=300)
```

### Comentários TODO

```python
# TODO: Implementar cache Redis quando tivermos mais de 1000 usuários
# FIXME: Este cálculo está incorreto para valores negativos
# NOTE: Esta função é chamada 1000x por segundo, otimizar se possível
```

---

## Tratamento de Erros - Explícito e Claro

### Nunca Ignorar Erros Silenciosamente

```python
# ❌ Ruim - esconde erros
try:
    user = User.objects.get(id=user_id)
except:
    pass  # O que aconteceu? Não sabemos.

# ✅ Bom - trata erros explicitamente
try:
    user = User.objects.get(id=user_id)
except User.DoesNotExist:
    logger.warning(f"User {user_id} not found")
    return None
except Exception as e:
    logger.error(f"Error getting user {user_id}: {e}")
    raise
```

### Exceções Específicas

```python
# ❌ Ruim - captura genérica
try:
    result = process_data(data)
except Exception:
    return None

# ✅ Bom - captura específica
try:
    result = process_data(data)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    return {'error': str(e)}
except ProcessingError as e:
    logger.error(f"Processing failed: {e}")
    raise  # Re-raise se não soubermos tratar
```

---

## DRY - Don't Repeat Yourself

### O Problema da Duplicação

Código duplicado é código que precisa ser atualizado em vários lugares. Se você esquece de atualizar um, cria bugs.

```python
# ❌ Ruim - código duplicado
def create_user(data):
    if not data.get('email'):
        return None
    if '@' not in data['email']:
        return None
    return User.objects.create(**data)

def update_user(user_id, data):
    if not data.get('email'):
        return None
    if '@' not in data['email']:
        return None
    user = User.objects.get(id=user_id)
    user.email = data['email']
    user.save()
    return user

# ✅ Bom - validação centralizada
def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    return '@' in email and '.' in email.split('@')[1]

def create_user(data: dict) -> Optional[User]:
    """Create user with validation."""
    if not validate_email(data.get('email')):
        return None
    return User.objects.create(**data)

def update_user(user_id: int, data: dict) -> Optional[User]:
    """Update user with validation."""
    if not validate_email(data.get('email')):
        return None
    user = User.objects.get(id=user_id)
    user.email = data['email']
    user.save()
    return user
```

---

## Complexidade - Manter Simples

### Complexidade Ciclomática

Funções com muitos `if`, `for`, `while` são difíceis de entender e testar. Tente manter complexidade baixa.

```python
# ❌ Ruim - muitos ifs aninhados
def calculate_price(user, item, discount_code):
    if user.is_premium:
        if item.category == 'electronics':
            if discount_code:
                if discount_code == 'SUMMER':
                    return item.price * 0.7
                elif discount_code == 'WINTER':
                    return item.price * 0.8
                else:
                    return item.price * 0.9
            else:
                return item.price * 0.85
        else:
            return item.price * 0.9
    else:
        if discount_code:
            return item.price * 0.95
        else:
            return item.price

# ✅ Bom - lógica separada e clara
def get_premium_discount(item: Item, discount_code: str = None) -> float:
    """Get discount for premium users."""
    if item.category == 'electronics':
        base_discount = 0.15
    else:
        base_discount = 0.10
    
    code_discount = get_code_discount(discount_code)
    return base_discount + code_discount

def get_code_discount(code: str) -> float:
    """Get additional discount from code."""
    discounts = {
        'SUMMER': 0.15,
        'WINTER': 0.10,
    }
    return discounts.get(code, 0.05)

def calculate_price(user: User, item: Item, discount_code: str = None) -> float:
    """Calculate final price with all discounts."""
    if user.is_premium:
        discount = get_premium_discount(item, discount_code)
    else:
        discount = get_code_discount(discount_code) if discount_code else 0.0
    
    return item.price * (1 - discount)
```

---

## Linha Máxima de 79 Caracteres (PEP 8)

### Regra Obrigatória

**Todas as linhas de código Python devem ter no máximo 79 caracteres.** Esta é uma regra do PEP 8 (E501) e deve ser seguida rigorosamente.

### Por Que 79 Caracteres?

- **Legibilidade:** Linhas muito longas são difíceis de ler
- **Code Review:** Facilita revisão lado a lado em monitores
- **Terminais:** Funciona bem em terminais padrão de 80 colunas
- **Padrão da Comunidade:** PEP 8 é o padrão oficial do Python

### Como Quebrar Linhas

```python
# ❌ Ruim - linha muito longa (87 caracteres)
def retrieve(self, request: Any, *args: Any, **kwargs: Dict[str, Any]) -> Response:

# ✅ Bom - quebrada em múltiplas linhas
def retrieve(
    self, request: Any, *args: Any, **kwargs: Dict[str, Any]
) -> Response:
```

### Padrões de Quebra

**Assinaturas de Função:**
```python
# ✅ Bom
def process_data(
    user_id: int,
    start_date: date,
    end_date: date,
    include_deleted: bool = False
) -> List[Dict[str, Any]]:
    pass
```

**Chamadas de Função:**
```python
# ✅ Bom
result = controller.create_contract(
    kwargs.get("pk"),
    request.data,
    request=request
)
```

**Comentários Longos:**
```python
# ✅ Bom - quebrar comentário
# Check if inactive record was found
# (returns dict instead of contract)
if isinstance(result, dict) and 'error' in result:
    pass
```

**Strings Longas:**
```python
# ✅ Bom - usar parênteses para continuar
message = (
    "This is a very long message that needs to be "
    "broken into multiple lines for readability."
)
```

### Verificação

Use `flake8` para verificar violações:

```bash
# Verificar todos os arquivos
flake8 --select=E501 --exclude=migrations,__pycache__,venv,env .

# Verificar arquivo específico
flake8 --select=E501 arquivo.py
```

### Exceções

- **Imports longos:** Aceitável em alguns casos, mas preferir múltiplas linhas
- **URLs longas:** Aceitável se não houver alternativa prática
- **Comentários:** Podem exceder 79 se necessário para clareza

**Mas sempre prefira quebrar a linha quando possível.**

---

## Organização de Código

### Ordem de Imports

```python
# 1. Standard library
import os
import sys
from typing import List, Dict

# 2. Third-party
import django
from rest_framework import status

# 3. Local
from app.models import User
from app.repositories import UserRepository
```

### Agrupar por Responsabilidade

```python
# ✅ Bom - agrupado logicamente
class UserController:
    # Métodos de criação
    @staticmethod
    def create_user(data: dict) -> User:
        pass
    
    # Métodos de leitura
    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        pass
    
    @staticmethod
    def list_users() -> List[User]:
        pass
    
    # Métodos de atualização
    @staticmethod
    def update_user(user_id: int, data: dict) -> Optional[User]:
        pass
    
    # Métodos de exclusão
    @staticmethod
    def delete_user(user_id: int) -> bool:
        pass
```

---

## Magic Numbers - Evitar

```python
# ❌ Ruim - números mágicos
if len(password) < 8:
    return False
if user.age < 18:
    return False

# ✅ Bom - constantes nomeadas
MIN_PASSWORD_LENGTH = 8
MIN_AGE = 18

if len(password) < MIN_PASSWORD_LENGTH:
    return False
if user.age < MIN_AGE:
    return False
```

---

## Princípios SOLID (Resumo)

### Single Responsibility

Uma classe/função deve ter apenas uma razão para mudar.

```python
# ❌ Ruim - faz duas coisas
class User:
    def save(self):
        # Salva no banco
        pass
    
    def send_email(self):
        # Envia email
        pass

# ✅ Bom - responsabilidades separadas
class User:
    def save(self):
        pass

class EmailService:
    def send_to_user(self, user: User):
        pass
```

### Open/Closed

Aberto para extensão, fechado para modificação.

```python
# ✅ Bom - extensível sem modificar código existente
class PaymentProcessor:
    def process(self, payment: Payment):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process(self, payment: Payment):
        # Implementação específica
        pass

class PayPalProcessor(PaymentProcessor):
    def process(self, payment: Payment):
        # Implementação específica
        pass
```

---

## Checklist de Code Review

Antes de fazer merge, verificar:

- [ ] Nomes descritivos (sem abreviações confusas)
- [ ] Funções pequenas (< 20 linhas quando possível)
- [ ] Uma função, uma responsabilidade
- [ ] Sem código duplicado (DRY)
- [ ] Erros tratados explicitamente
- [ ] Sem números mágicos (usar constantes)
- [ ] Comentários apenas quando necessário
- [ ] Complexidade baixa (poucos ifs aninhados)
- [ ] Type hints em todas as funções
- [ ] Docstrings em funções públicas

---

## Referências

Estas práticas vêm de:
- Clean Code (Robert C. Martin)
- The Pragmatic Programmer
- Refactoring (Martin Fowler)
- Experiência prática em projetos reais

---

**Código limpo não é luxo - é necessidade. Projetos que não seguem essas práticas viram bagunça impossível de manter.**


