# REGRAS CRITICAS - TODOS OS AGENTES

**Prioridade:** MAXIMA  
**Validade:** PERMANENTE  
**Escopo:** TODOS os agentes

---

## REGRA 1: SEM RELATORIOS DE SESSAO NO GIT

**NUNCA commitar:**
- Resumos de sessoes
- Relatorios de interacoes
- Feedback de conversas
- Logs diarios de uso
- Analises de agenda
- Status de conversas

**Razao:**
- Poluem o repositorio
- Nao sao parte do framework
- Sao temporarios/pessoais
- Nao tem valor reutilizavel

**Se usuario pedir resumo:**
- Fornecer NO CHAT
- NAO criar arquivo
- NAO commitar

**Ver detalhes:** core/docs/rules/NO_SESSION_REPORTS_IN_GIT.md

---

## REGRA 2: TIMEZONE SEMPRE GMT-3

**SEMPRE usar GMT-3 (Sao Paulo, Brazil)**  
**NUNCA usar UTC**

**Formato:** `2025-11-01T19:00:00-03:00`

**Ver detalhes:** core/docs/RULES_SYSTEM.md

---

## REGRA 3: SEM EMOJIS EM CODIGO

**NUNCA usar emojis em:**
- Codigo Python
- Arquivos de configuracao (.json, .yml, .env)
- Scripts shell
- Arquivos de testes

**Pode usar emojis em:**
- Markdown de documentacao
- Notion (como icone de pagina)
- Comentarios de codigo (com moderacao)

**Razao:** Emojis podem causar problemas de encoding

---

## REGRA 4: PRIVACIDADE PRIMEIRO

**NUNCA commitar:**
- IDs do Notion
- API keys e tokens
- Dados pessoais
- Informacoes medicas
- Detalhes de trabalho/cliente
- Dados sensiveis

**Tudo isso vai em:** `config/private/` (gitignored)

---

## REGRA 5: COMMITS APENAS DE FRAMEWORK

**Commitar APENAS:**
- Codigo do framework
- Templates genericos
- Documentacao de arquitetura
- Exemplos reutilizaveis
- Utilitarios
- Testes

**NAO commitar:**
- Configuracoes pessoais
- Relatorios de sessoes
- Logs de uso
- Dados especificos do usuario

---

## VALIDACAO ANTES DE COMMIT

Antes de QUALQUER commit, verificar:

```bash
# 1. Nao tem relatorios de sessao?
git status | grep -i "RESUMO\|RELATORIO\|FEEDBACK\|ANALISE"

# 2. Nao tem dados privados?
git diff | grep -i "secret_\|notion.*[0-9a-f]\{32\}\|@.*gmail"

# 3. Apenas arquivos do framework?
git status | grep "core/\|config/agents/.*template\|docs/"
```

Se encontrar algo suspeito: NAO COMMITAR!

---

## ENFORCEMENT

### Todos os agentes devem:

1. Ler este arquivo SEMPRE
2. Seguir TODAS as regras
3. Validar antes de criar arquivos
4. Nunca poluir o repositorio
5. Sempre proteger privacidade

### Usuario pode:

- Reclamar se regra for quebrada
- Pedir remocao imediata
- Exigir cumprimento rigoroso

---

## VIOLACOES COMUNS (EVITAR)

### Violacao 1: Criar relatorio de sessao

Errado:
```bash
# Agent cria
RESUMO_SESSAO_01_NOV_2025.md
git add RESUMO_SESSAO_01_NOV_2025.md
git commit -m "docs: add session summary"
```

Correto:
```bash
# Agent fornece resumo no chat
# NAO cria arquivo
# NAO commita nada
```

---

### Violacao 2: Commitar dados privados

Errado:
```json
{
  "notion_database_id": "1f9962a7693c80d39295f90317129cbd"
}
```

Correto:
```json
{
  "notion_database_id": "SEE_config/private/notion-ids.json"
}
```

---

### Violacao 3: Emojis em codigo

Errado:
```python
def create_card():
    title = "Planejamento Semanal"
```

Correto:
```python
def create_card():
    title = "Planejamento Semanal"
```

---

## CHECKLIST PARA AGENTES

Antes de criar qualquer arquivo:

- [ ] Este arquivo e parte do framework? (nao e relatorio)
- [ ] Vai ser reutilizavel por outros? (nao e pessoal)
- [ ] Nao contem dados privados? (sem IDs, tokens)
- [ ] Esta no lugar certo? (core/ ou config/private/)
- [ ] Nao tem emojis em codigo? (apenas em docs)

Se TODOS sim: OK para criar e commitar (se publico)

Se ALGUM nao: Repensar onde salvar ou se criar

---

## RESUMO

**DO:**
- Criar framework reutilizavel
- Documentar arquitetura
- Proteger privacidade
- Commits limpos

**DON'T:**
- Relatorios de sessoes
- Dados privados em git
- Emojis em codigo
- Poluir repositorio

---

**ESTAS REGRAS SAO OBRIGATORIAS E NAO NEGOCIAVEIS**

---

Last Updated: 2024-11-01  
Version: 1.0  
Priority: CRITICAL  
Scope: ALL AGENTS

