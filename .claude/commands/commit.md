# /commit - Preparar Commit

## Quando Usar
Após review aprovado, para preparar o commit.

## O Que Faz
1. Mostra `git status` e `git diff`
2. Sugere mensagem de commit (conventional commits)
3. **AGUARDA APROVAÇÃO** antes de commitar
4. Pergunta sobre push

## Regras OBRIGATÓRIAS

### NUNCA fazer sem permissão:
- `git commit`
- `git push`
- `git reset --hard`
- `git rebase`
- Qualquer comando destrutivo

### SEMPRE mostrar antes:
- Preview completo das alterações
- Mensagem de commit sugerida
- Confirmação explícita do usuário

## Conventional Commits

### Formato
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta código)
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

### Exemplos
```
feat(auth): add JWT token refresh endpoint
fix(api): handle null response in user service
docs(readme): update installation instructions
refactor(utils): extract date formatting to helper
test(auth): add unit tests for login flow
```

## Workflow

```
1. Mostrar: git status
2. Mostrar: git diff --stat
3. Sugerir: mensagem de commit
4. PERGUNTAR: "Posso fazer o commit?"
5. Se SIM: git commit -m "mensagem"
6. PERGUNTAR: "Quer fazer push?"
7. Se SIM: git push
```

## Output Esperado

```markdown
## Preparação de Commit

### Alterações
- 3 arquivos modificados
- 45 inserções, 12 deleções

### Arquivos
- `src/auth/service.py` (modificado)
- `src/auth/models.py` (modificado)
- `tests/test_auth.py` (novo)

### Commit Sugerido
```
feat(auth): implement password reset flow

- Add password reset endpoint
- Add email notification service
- Add unit tests for reset flow
```

**Posso fazer o commit com essa mensagem?** [Aguardando confirmação]
```
