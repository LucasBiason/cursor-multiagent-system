# /test - Executar Testes

## Quando Usar
Para executar e reportar resultados de testes.

## O Que Faz
1. Detecta framework de testes do projeto
2. Executa testes
3. Reporta resultados e cobertura
4. Identifica testes falhando

## Detecção Automática

### Python
```bash
# Se pytest.ini ou pyproject.toml com pytest
pytest -v --tb=short

# Se unittest
python -m unittest discover
```

### JavaScript/TypeScript
```bash
# Se package.json com jest
npm test

# Se vitest
npx vitest run
```

### Go
```bash
go test ./... -v
```

## Output Esperado

```markdown
## Test Report

### Sumário
- **Total:** 42 testes
- **Passou:** 40 ✅
- **Falhou:** 2 ❌
- **Cobertura:** 78%

### Testes Falhando

#### test_user_creation (tests/test_user.py:45)
```
AssertionError: Expected status 201, got 400
Response: {"error": "email already exists"}
```

**Causa provável:** Teste não limpa database entre runs

#### test_api_timeout (tests/test_api.py:123)
```
TimeoutError: Request exceeded 5s limit
```

**Causa provável:** Mock de external API não configurado

### Arquivos Sem Cobertura
- `src/utils/legacy.py` (0%)
- `src/migrations/` (0%)

### Recomendações
1. Adicionar fixture para limpar database
2. Adicionar mock para external API
3. Considerar excluir migrations da cobertura
```

## Flags Úteis

### pytest
```bash
pytest -v                    # Verbose
pytest -x                    # Stop on first failure
pytest --lf                  # Run last failed
pytest -k "test_user"        # Filter by name
pytest --cov=src             # Coverage
```

### jest
```bash
npm test -- --verbose
npm test -- --coverage
npm test -- --watch
npm test -- -t "user"
```
