# git - workflow e boas práticas

**última atualização:** 2025-12-08  
**aplicável a:** todos os projetos versionados

---

## workflow de branches

### feature branches obrigatório

```bash
# sempre usar feature branches
git checkout -b feature/nome-da-feature
git checkout -b fix/nome-do-bug
git checkout -b refactor/nome-do-refactor
```

### estrutura de branches

```
main                    # produção (protegida)
├── develop            # desenvolvimento (opcional)
├── feature/xxx        # novas features
├── fix/xxx            # correções de bugs
├── refactor/xxx       # refatorações
└── hotfix/xxx         # correções urgentes em produção
```

### git flow simplificado

**princípios:**
- `main` sempre estável e deployável
- features desenvolvidas em branches separadas
- merge apenas via pull request
- code review obrigatório antes de merge
- **hotfixes**: podem ser commitados direto em `main` (correções urgentes em produção)

**fluxo:**
1. criar branch a partir de `main`
2. desenvolver feature
3. commitar frequentemente com mensagens descritivas
4. criar pull request
5. code review
6. merge após aprovação
7. deletar branch após merge

**hotfixes (exceção):**
- correções urgentes em produção
- podem ser commitados direto em `main`
- usar tipo `fix:` ou `hotfix:` no commit
- exemplo: `fix: corrigir erro crítico em produção`

---

## mensagens de commit

### formato obrigatório

```
<tipo>: <descrição curta>

<descrição detalhada (opcional)>

<referências (opcional)>
```

### tipos de commit

- `feat`: nova feature
- `fix`: correção de bug
- `refactor`: refatoração de código
- `docs`: documentação
- `test`: testes
- `chore`: tarefas de manutenção
- `style`: formatação (sem mudança de código)
- `perf`: melhorias de performance

### exemplos

```bash
# ✅ correto
git commit -m "feat: adicionar autenticação via jwt"

git commit -m "fix: corrigir validação de email no formulário

A validação estava permitindo emails inválidos.
Agora valida formato e domínio."

git commit -m "refactor: mover lógica de negócio para controller

Separa lógica de negócio da view seguindo padrão controller."
```

### erros comuns

```bash
# ❌ errado - mensagem vaga
git commit -m "update"

# ❌ errado - sem tipo
git commit -m "adicionar feature"

# ❌ errado - muito longo na primeira linha
git commit -m "adicionar sistema completo de autenticação com jwt tokens e refresh tokens e middleware de validação"
```

---

## pull requests

### antes de criar pr

- [ ] código testado localmente
- [ ] todos os testes passando
- [ ] sem conflitos com main
- [ ] código revisado (self-review)
- [ ] documentação atualizada se necessário

### descrição do pr

```markdown
## Descrição
Breve descrição do que foi feito.

## Tipo de mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Refatoração
- [ ] Documentação

## Checklist
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Código segue padrões do projeto
- [ ] Sem breaking changes (ou documentados)
```

---

## code review

### antes de aprovar

- [ ] código segue padrões do projeto
- [ ] testes adequados
- [ ] sem código comentado desnecessário
- [ ] sem secrets hardcoded
- [ ] performance considerada
- [ ] segurança considerada

### feedback

- ser construtivo e educacional
- explicar o porquê das sugestões
- sugerir alternativas quando possível
- reconhecer boas práticas

---

## tags e releases

### semantic versioning

```
v<major>.<minor>.<patch>
```

- **major**: breaking changes
- **minor**: novas features (backward compatible)
- **patch**: bug fixes

### criar tag

```bash
git tag -a v1.2.0 -m "Release 1.2.0: Adicionar autenticação JWT"
git push origin v1.2.0
```

---

## regras gerais

### nunca fazer

- ❌ force push para main
- ❌ commits diretos em main (sempre via pr)
- ❌ commits sem mensagem descritiva
- ❌ commits com código quebrado
- ❌ commits com secrets

### sempre fazer

- ✅ usar feature branches
- ✅ commits frequentes e descritivos
- ✅ revisar código antes de commit
- ✅ rodar testes antes de commit
- ✅ atualizar documentação quando necessário

---

## boas práticas adicionais

### commits frequentes

**fazer commits pequenos e frequentes:**
- cada commit deve representar uma mudança lógica
- commits frequentes facilitam rollback
- commits pequenos facilitam code review

### antes de commit

- [ ] código testado localmente
- [ ] todos os testes passando
- [ ] código formatado (black, prettier, etc.)
- [ ] sem código comentado desnecessário
- [ ] sem console.log/debugger
- [ ] sem secrets hardcoded

### organização de commits

**um commit = uma responsabilidade:**
```bash
# ✅ correto - commits separados
git commit -m "feat: adicionar validação de email"
git commit -m "refactor: mover lógica para controller"
git commit -m "test: adicionar testes para validação"

# ❌ errado - tudo em um commit
git commit -m "feat: adicionar validação e refatorar controller e testes"
```

---

## referências

- semantic versioning: https://semver.org/
- conventional commits: https://www.conventionalcommits.org/
- git flow: https://nvie.com/posts/a-successful-git-branching-model/

---

**estas regras são obrigatórias em todos os projetos.**

