# /review - Code Review Workflow

## Quando Usar
Após implementar código no Cursor, chame este comando para revisar.

## O Que Faz
1. Identifica arquivos alterados (`git diff`)
2. Analisa qualidade do código
3. Verifica padrões e convenções
4. Identifica problemas de segurança
5. Executa testes relacionados
6. Reporta issues encontrados

## Checklist de Review

### Qualidade
- [ ] Código legível e bem organizado
- [ ] Nomes descritivos (variáveis, funções, classes)
- [ ] Funções pequenas e focadas
- [ ] Sem código duplicado
- [ ] Tratamento de erros adequado

### Segurança
- [ ] Sem credenciais hardcoded
- [ ] Input validation presente
- [ ] Sem SQL injection vulnerabilities
- [ ] Sem XSS vulnerabilities
- [ ] Dados sensíveis protegidos

### Padrões
- [ ] Segue convenções do projeto
- [ ] Imports organizados
- [ ] Formatação consistente
- [ ] Documentação onde necessário

### Testes
- [ ] Testes existem para novas funcionalidades
- [ ] Testes passando
- [ ] Cobertura adequada

## Output Esperado

```markdown
## Code Review Report

### Arquivos Analisados
- `path/to/file1.py`
- `path/to/file2.py`

### Issues Encontrados
1. **[CRÍTICO]** Descrição em `file:linha`
2. **[MÉDIO]** Descrição em `file:linha`
3. **[BAIXO]** Descrição em `file:linha`

### Testes
- ✅ X testes passaram
- ❌ Y testes falharam

### Recomendações
1. Correção necessária
2. Melhoria sugerida

### Próximos Passos
- Cursor: corrija issues críticos
- Depois: `/commit` para preparar commit
```
