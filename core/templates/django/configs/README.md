# Estrutura de Configurações

**Última Atualização:** 2025-12-08

---

## estrutura obrigatória

```
configs/
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── nginx.conf
├── .env.development
├── .env.production
└── .env.database
```

---

## docker-compose

**desenvolvimento (`docker-compose.dev.yml`):**
- usar `Dockerfile.dev`
- volumes para hot-reload
- banco de dados local
- redis local (se necessário)

**produção (`docker-compose.prod.yml`):**
- usar `Dockerfile.prod`
- sem volumes (imagens finais)
- configurações de produção
- health checks

**banco de dados:**
- se usar container de banco, criar `.env.database`
- separar configurações de banco das da aplicação

---

## nginx

**configuração:**
- proxy para serviços backend
- servir arquivos estáticos (produção)
- health check endpoint
- CORS headers

**template:** usar como base o nginx do ExpenseIQ

---

## arquivos .env

**desenvolvimento (`.env.development`):**
- DEBUG=True
- banco local
- redis local
- configurações de dev

**produção (`.env.production`):**
- DEBUG=False
- banco de produção
- redis de produção
- secrets reais

**banco (`.env.database`):**
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- PGPORT

**outros serviços:**
- `.env.redis` (se necessário)
- `.env.kafka` (se necessário)
- `.env.mongodb` (se necessário)

---

## referências

- templates: `core/templates/django/configs/`
- regras gerais: `core/agents/programming.mdc`

---

**esta estrutura é obrigatória para todos os projetos.**


