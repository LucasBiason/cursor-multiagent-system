# /handoff - Transição Entre Ferramentas

## Cursor → Claude Code

### Quando Usar
Após implementar código no Cursor, para passar para revisão.

### Comando
```bash
claude "review as alterações, rode os testes e reporte"
```

### O Que o Cursor Deve Ter Feito
- [ ] Código implementado
- [ ] Funcionalidade testada manualmente
- [ ] Sem erros de sintaxe
- [ ] Arquivos salvos

### O Que Claude Code Faz
1. `git diff` para ver alterações
2. Code review (qualidade, segurança, padrões)
3. Executa testes automatizados
4. Reporta issues encontrados
5. Sugere correções se necessário

---

## Claude Code → Cursor

### Quando Usar
Quando Claude Code encontra issues que precisam de correção.

### Formato do Report
```markdown
## Issues para Correção (Cursor)

### Críticos (bloqueia commit)
1. **[src/auth.py:45]** SQL injection vulnerability
   - Problema: Query concatenada diretamente
   - Solução: Usar parameterized query

### Médios (deveria corrigir)
2. **[src/utils.py:23]** Função muito longa (150 linhas)
   - Solução: Extrair em funções menores

### Baixos (nice to have)
3. **[src/models.py:67]** Docstring ausente
   - Solução: Adicionar documentação

---

**Cursor:** Corrija os issues críticos e médios, depois chame Claude Code novamente.
```

---

## Workflow Completo

```
┌─────────────────────────────────────────────────────────┐
│                    CICLO DE DESENVOLVIMENTO              │
└─────────────────────────────────────────────────────────┘

     CURSOR                CLAUDE CODE              VOCÊ
        │                      │                      │
        ▼                      │                      │
   Implementa                  │                      │
   código novo                 │                      │
        │                      │                      │
        └──────────────────────▶                      │
                               │                      │
                          Review +                    │
                          Testes                      │
                               │                      │
                               ├── Se OK ────────────▶│
                               │                      │
                               │               Aprova commit?
                               │                      │
                               │◀── Se SIM ──────────┤
                               │                      │
                          Faz commit                  │
                          (com permissão)             │
                               │                      │
                               ├── Se issues ────────▶│
                               │                      │
        ◀──────────────────────┤              Lista issues
                               │                      │
   Corrige issues              │                      │
        │                      │                      │
        └──────────────────────▶                      │
                               │                      │
                          Re-review                   │
                               │                      │
                              ...                    ...
```

---

## Comandos de Handoff

### Do Cursor para Claude Code
```bash
# Review básico
claude "review as alterações"

# Review + testes
claude "review as alterações e rode os testes"

# Preparar commit
claude "prepare o commit das alterações"

# Fluxo completo
claude "review, teste e prepare commit se tudo OK"
```

### Respostas do Claude Code para Cursor
```
# Se tudo OK
"Review aprovado. Pronto para commit."

# Se tem issues
"Issues encontrados: [lista]
Cursor: corrija X no arquivo Y, depois chame review novamente."

# Se testes falharam
"2 testes falhando: [lista]
Cursor: investigue e corrija antes de continuar."
```
