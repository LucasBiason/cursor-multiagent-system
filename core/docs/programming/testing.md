# testing - padrões e boas práticas

**última atualização:** 2025-12-08  
**aplicável a:** todos os projetos

---

## tdd approach

### desenvolvimento orientado por testes

1. escrever teste primeiro
2. implementar código mínimo para passar
3. refatorar
4. repetir

---

## tipos de testes

### unit tests

**testar componentes isolados:**

```python
# tests/test_validators.py
def test_user_validator_valid_email():
    result = UserValidator.validate_email("user@example.com")
    assert result['valid'] is True

def test_user_validator_invalid_email():
    result = UserValidator.validate_email("invalid-email")
    assert result['valid'] is False
```

### integration tests

**testar fluxo completo:**

```python
# tests/test_integration.py
def test_create_user_flow():
    # 1. Validar
    validation = UserValidator.validate(user_data)
    assert validation['valid'] is True
    
    # 2. Criar
    user = UserController.create_user(validation['data'])
    assert user is not None
    
    # 3. Verificar
    created = UserRepository.get_by_id(user.id)
    assert created.email == user_data['email']
```

---

## cobertura mínima

### 80% de cobertura obrigatório

```bash
# rodar coverage
pytest --cov=app --cov-report=html

# verificar cobertura
coverage report
```

---

## organização de testes

### estrutura

```
tests/
├── test_validators.py
├── test_repositories.py
├── test_controllers.py
├── test_services.py
└── test_integration.py
```

### nomenclatura

```python
# arquivo: test_user_validator.py
# função: test_user_validator_valid_email
def test_user_validator_valid_email():
    pass
```

---

## regras gerais

### sempre fazer

- ✅ testes antes de commit
- ✅ todos os testes passando antes de merge
- ✅ cobertura mínima de 80%
- ✅ testes isolados (não dependem uns dos outros)

### nunca fazer

- ❌ commitar testes quebrados
- ❌ testes que dependem de ordem de execução
- ❌ testes que dependem de estado externo
- ❌ testes sem assertions

---

**estas regras são obrigatórias para qualidade do código.**

