# Regras de Testes Unitários

**Última Atualização:** 2025-12-08

---

## framework obrigatório

**usar pytest para todos os testes:**
- pytest em funções (não classes)
- pytest-django para projetos Django
- pytest-asyncio para código assíncrono

---

## estrutura de testes

**a estrutura dos testes deve espelhar a estrutura da aplicação:**

```
app/
├── users/
│   ├── controllers/
│   │   └── user_controller.py
│   └── models/
│       └── user.py

tests/
├── users/
│   ├── controllers/
│   │   └── test_user_controller.py
│   └── models/
│       └── test_user.py
```

**regra:** quando procurar um teste de um arquivo, ele deve estar na mesma estrutura relativa.

---

## mocks obrigatórios

**todos os acessos externos devem ser mockados:**

1. **banco de dados:**
   - usar fixtures do pytest-django
   - mockar queries complexas quando necessário
   - não usar banco real em testes

2. **sistema de fila (redis, rabbitmq, etc.):**
   - mockar todas as operações de fila
   - não enviar mensagens reais

3. **cache (redis, memcached, etc.):**
   - mockar operações de cache
   - não usar cache real

4. **APIs externas:**
   - usar `responses` ou `httpx` para mockar requisições HTTP
   - não fazer chamadas reais a APIs externas

5. **sistema de arquivos:**
   - usar `tempfile` ou mockar operações de arquivo
   - não criar arquivos reais no sistema

---

## coverage obrigatório

**cada arquivo precisa ter pelo menos 90% de coverage:**
- não é média entre arquivos
- cada arquivo individualmente deve ter 90%+
- configurar no `pytest.ini` ou `pyproject.toml`

**configuração exemplo:**
```ini
[tool.pytest.ini_options]
addopts = "-v --cov=app --cov-report=html --cov-report=term --cov-fail-under=90"
```

---

## nomenclatura

**arquivos de teste:**
- `test_*.py` ou `*_test.py`
- exemplo: `test_user_controller.py`

**funções de teste:**
- `test_*`
- exemplo: `test_create_user_success()`

**descritivo:**
- `test_create_user_with_valid_data_success()`
- `test_create_user_with_invalid_email_fails()`

---

## estrutura de teste

**cada teste deve ter:**
1. arrange (setup)
2. act (execução)
3. assert (verificação)

**exemplo:**
```python
def test_create_user_success():
    # arrange
    user_data = {"email": "test@example.com", "name": "Test User"}
    
    # act
    result = create_user(user_data)
    
    # assert
    assert result.email == "test@example.com"
    assert result.id is not None
```

---

## fixtures e conftest.py

**usar fixtures para setup comum:**
- criar fixtures em `conftest.py`
- reutilizar fixtures entre testes
- fixtures devem ser específicas e isoladas

**exemplo:**
```python
@pytest.fixture
def user_data():
    return {"email": "test@example.com", "name": "Test User"}

@pytest.fixture
def mock_redis(monkeypatch):
    mock_redis = Mock()
    monkeypatch.setattr("app.utils.cache_system.CacheSystem", mock_redis)
    return mock_redis
```

---

## pytest.ini e conftest.py

**templates obrigatórios:**
- `core/templates/django/pytest.ini`
- `core/templates/django/conftest.py`

**usar sempre os templates como base.**

---

## testes de integração vs unitários

**testes unitários:**
- testam uma função/método isoladamente
- todos os dependências mockadas
- rápidos e determinísticos

**testes de integração:**
- testam múltiplos componentes juntos
- podem usar banco de teste (isolado)
- mais lentos, mas validam integração

**priorizar testes unitários (maioria).**

---

## referências

- templates: `core/templates/django/pytest.ini`, `core/templates/django/conftest.py`
- regras gerais: `core/agents/programming.mdc`

---

**estas regras são obrigatórias para todos os projetos.**


