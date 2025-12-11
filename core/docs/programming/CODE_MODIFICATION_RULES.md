# Regras de Modificação de Código

**Última Atualização:** 2025-12-08

---

## regra fundamental: só alterar o que foi pedido

**os agentes de programação devem:**
- alterar apenas o que foi explicitamente solicitado pelo usuário
- não fazer alterações "melhorias" não solicitadas
- não remover código que não foi pedido para remover
- não adicionar funcionalidades que não foram solicitadas
- não refatorar código que não foi pedido para refatorar

---

## proibições absolutas

**nunca fazer sem solicitação explícita:**
1. remover código existente
2. adicionar novas funcionalidades
3. refatorar código
4. alterar estrutura de arquivos
5. modificar configurações existentes
6. alterar nomes de variáveis/funções/classes
7. mudar estilo de código
8. adicionar ou remover dependências
9. modificar migrations django
10. alterar arquivos de configuração (nginx, docker, etc.)

---

## quando o usuário pede uma alteração

**fazer apenas:**
1. a alteração específica solicitada
2. alterações mínimas necessárias para a alteração funcionar
3. manter tudo o resto exatamente como estava

---

## exemplos

### exemplo 1: adicionar endpoint

**solicitação:** "adicionar endpoint GET /users"

**correto:**
- criar apenas o endpoint solicitado
- seguir estrutura existente
- não alterar outros endpoints
- não refatorar código existente

**incorreto:**
- refatorar todos os endpoints
- alterar estrutura de pastas
- adicionar funcionalidades extras
- modificar outros arquivos não relacionados

---

### exemplo 2: corrigir bug

**solicitação:** "corrigir bug no cálculo de desconto"

**correto:**
- corrigir apenas o bug específico
- manter resto do código igual
- não "melhorar" outras partes

**incorreto:**
- refatorar toda a função
- alterar outras funções relacionadas
- adicionar validações extras não solicitadas

---

## quando há dúvida

**se não tiver certeza se deve alterar algo:**
1. fazer apenas o que foi explicitamente pedido
2. se necessário, perguntar ao usuário antes de alterar
3. nunca assumir que "melhorias" são desejadas

---

## exceções

**alterações permitidas sem solicitação explícita:**
1. correção de erros de sintaxe que impedem execução
2. correção de imports quebrados necessários para a alteração
3. ajustes mínimos de formatação para manter consistência (apenas se não alterar lógica)

---

## referências

- regras gerais: `core/agents/programming.mdc`
- templates: `core/templates/`

---

**esta regra é crítica e deve ser seguida rigorosamente por todos os agentes.**


