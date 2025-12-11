# programming documentation - índice completo

**última atualização:** 2025-12-08  
**versão:** 2.0  
**aplicável a:** todos os agentes que trabalham com código

---

## 📚 estrutura de documentação

esta pasta contém toda a documentação sobre como o usuário programa, organizada por áreas de conhecimento.

### organização

```
programming/
├── README.md              # este arquivo (índice)
├── QUICK_START_API.md     # ⭐ guia passo a passo para criar api completa
├── python.md              # python, django, fastapi
├── typescript.md          # typescript, react, frontend
├── git.md                 # git workflow, commits, branches
├── api-rest.md            # api rest, endpoints, versionamento
├── architecture.md        # padrões arquiteturais, mvc, clean architecture
├── devops.md              # docker, deploy, ci/cd
├── ssl-https-letsencrypt.md # ssl/https com let's encrypt e certbot
├── testing.md            # testes, tdd, cobertura
├── security.md            # segurança, secrets, validação
├── mcp.md                 # model context protocol, mcp servers
└── code-quality.md        # clean code e qualidade de código
```

---

## 🎯 como usar esta documentação

### para agentes

1. **sempre consultar** `core/agents/programming.mdc` primeiro
2. **referenciar** documentos específicos quando necessário
3. **seguir** os padrões documentados sem exceção
4. **nunca** desobedecer as regras estabelecidas

### para desenvolvedores

1. **ler** o documento relevante antes de implementar
2. **seguir** os templates e exemplos fornecidos
3. **consultar** quando houver dúvidas sobre padrões
4. **atualizar** se encontrar inconsistências

---

## 📖 documentos por área

### quick start api
- **localização:** `QUICK_START_API.md`
- **conteúdo:**
  - estrutura completa passo a passo
  - exemplos django rest framework
  - exemplos fastapi
  - checklist de implementação
  - todas as camadas (model, repository, validator, controller, api)
- **quando usar:** sempre que o usuário pedir uma api nova

### python
- **localização:** `python.md`
- **conteúdo:** 
  - type hints obrigatórios
  - docstrings (padrão google)
  - classes vs funções
  - django patterns
  - fastapi patterns
  - estrutura de projetos
  - imports e organização
  - testing best practices

### typescript
- **localização:** `typescript.md`
- **conteúdo:**
  - types vs interfaces
  - react best practices
  - absolute imports
  - hooks customizados
  - performance (memo, usecallback)
  - tailwind css
  - acessibilidade
  - ecossistema frontend completo

### git
- **localização:** `git.md`
- **conteúdo:**
  - workflow de branches
  - mensagens de commit
  - pull requests
  - code review
  - tags e releases

### api-rest
- **localização:** `api-rest.md`
- **conteúdo:**
  - versionamento obrigatório
  - estrutura de urls
  - http methods
  - status codes
  - serialização
  - paginação
  - error handling

### architecture
- **localização:** `architecture.md`
- **conteúdo:**
  - repository pattern
  - controller pattern
  - validators
  - separação de views (template vs api)
  - clean architecture
  - mvc

### devops
- **localização:** `devops.md`
- **conteúdo:**
  - docker e docker-compose
  - dockerfile otimizado
  - entrypoint scripts
  - makefile
  - nginx configuration
  - environment variables
  - deployment process
  - ci/cd pipelines

### ssl/https
- **localização:** `ssl-https-letsencrypt.md`
- **conteúdo:**
  - configuração SSL com Let's Encrypt
  - integração Certbot com Docker
  - configuração Nginx para HTTPS
  - renovação automática de certificados
  - boas práticas de segurança SSL
  - troubleshooting comum
  - exemplo completo Django + Nginx + Certbot
- **quando usar:** sempre que configurar SSL/HTTPS em produção

### testing
- **localização:** `testing.md`
- **conteúdo:**
  - tdd approach
  - unit tests
  - integration tests
  - coverage requirements
  - test organization

### security
- **localização:** `security.md`
- **conteúdo:**
  - secrets management
  - input validation
  - sql injection prevention
  - authentication/authorization
  - environment variables

### mcp
- **localização:** `mcp.md`
- **conteúdo:**
  - model context protocol
  - mcp server structure
  - tool definitions
  - error handling
  - best practices

### code quality
- **localização:** `code-quality.md`
- **conteúdo:**
  - nomenclatura descritiva
  - funções pequenas e focadas
  - tratamento de erros explícito
  - princípio DRY
  - redução de complexidade
  - organização de código
  - princípios SOLID
  - checklist de code review

---

## 🔗 referências rápidas

### guia completo
- **criar api do zero** → `QUICK_START_API.md` - Guia passo a passo completo
- **best practices completo** → `BEST_PRACTICES.md` - Guia consolidado de todas as práticas

### padrões obrigatórios
- repository pattern → `architecture.md` e `python.md`
- controller pattern → `architecture.md` e `python.md`
- validators → `architecture.md` e `python.md`
- api versioning → `api-rest.md`
- sql puro apenas select → `python.md`

### regras críticas
- sem emojis no código → `python.md`
- type hints obrigatórios → `python.md`
- absolute imports → `typescript.md`
- secrets em .env → `security.md`

### documentação detalhada por tecnologia
- python completo → `python.md`
- typescript/react completo → `typescript.md`
- git workflow → `git.md`
- api rest → `api-rest.md`
- arquitetura → `architecture.md`
- devops completo → `devops.md`
- ssl/https → `ssl-https-letsencrypt.md`
- testing → `testing.md`
- segurança → `security.md`
- mcp → `mcp.md`
- code quality → `code-quality.md`

---

## 📝 atualização desta documentação

### quando atualizar
- novos padrões estabelecidos
- mudanças em preferências de código
- descoberta de inconsistências
- feedback de implementações

### como atualizar
1. editar documento específico
2. atualizar este índice se necessário
3. atualizar `core/agents/programming.mdc`
4. documentar mudança no changelog

---

**esta documentação é a fonte de verdade para todos os padrões de programação.**

