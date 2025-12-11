# devops - padrões e boas práticas

**última atualização:** 2025-12-08  
**aplicável a:** todos os projetos com deploy

---

## docker e docker-compose

### estrutura básica

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
    volumes:
      - ./backend:/app
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### secrets em .env

```bash
# docker-compose.yml
environment:
  - API_KEY=${API_KEY}

# .env (gitignored)
API_KEY=sk-1234567890abcdef
```

### nunca hardcodar secrets

```yaml
# ❌ errado
environment:
  - API_KEY=sk-1234567890abcdef

# ✅ correto
environment:
  - API_KEY=${API_KEY}
```

---

## dockerfile - a base de tudo

### estrutura otimizada

um dockerfile bem feito é rápido de build, pequeno em tamanho, e seguro:

```dockerfile
# Use imagem base oficial e específica (não latest)
FROM python:3.11-slim

# Metadados (opcional mas útil)
LABEL maintainer="seu-email@example.com"
LABEL description="API FastAPI para processamento de dados"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Criar usuário não-root (segurança)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Diretório de trabalho
WORKDIR /app

# Copiar apenas requirements primeiro (cache layer)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Mudar ownership para usuário não-root
RUN chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 8000

# Healthcheck (importante para orquestração)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Entrypoint (ver seção específica)
ENTRYPOINT ["./entrypoint.sh"]

# Comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### por que não root?

executar containers como root é perigoso. se alguém conseguir explorar uma vulnerabilidade, terá acesso root no container:

```dockerfile
# ❌ perigoso
USER root
CMD ["python", "app.py"]

# ✅ seguro
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
CMD ["python", "app.py"]
```

### multi-stage builds

para aplicações que precisam compilar código, use multi-stage builds:

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
RUN npm ci --production
CMD ["node", "dist/index.js"]
```

isso resulta em imagens muito menores, porque você não inclui ferramentas de build na imagem final.

---

## docker compose - orquestração de serviços

### estrutura completa

docker compose é onde a mágica acontece. você define todos os serviços, redes, volumes e dependências em um arquivo:

```yaml
version: '3.8'

services:
  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      args:
        - BUILD_ENV=production
    container_name: myapp-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env
      - .env.local  # Sobrescreve .env se existir
    volumes:
      - ./backend:/app
      - backend_static:/app/staticfiles
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Database
  db:
    image: postgres:15-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Nginx (reverse proxy)
  nginx:
    image: nginx:alpine
    container_name: myapp-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - backend_static:/static:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
    networks:
      - app-network

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  backend_static:
    driver: local

networks:
  app-network:
    driver: bridge
```

### por que healthchecks?

healthchecks permitem que o docker saiba quando um serviço está realmente pronto:

```yaml
# Sem healthcheck - depende_on só espera container iniciar
depends_on:
  - db  # Pode iniciar antes do banco estar pronto!

# Com healthcheck - espera até estar saudável
depends_on:
  db:
    condition: service_healthy  # Espera healthcheck passar
```

### variáveis de ambiente

nunca hardcode secrets. use variáveis de ambiente:

```yaml
# ❌ nunca fazer
environment:
  - DATABASE_PASSWORD=senha123

# ✅ sempre fazer
environment:
  - DATABASE_PASSWORD=${DB_PASSWORD}

# Ou melhor ainda, usar env_file
env_file:
  - .env
```

### .env file

crie um `.env.example` para documentar variáveis necessárias:

```bash
# .env.example
DATABASE_URL=postgresql://user:password@db:5432/mydb
REDIS_URL=redis://redis:6379/0
SECRET_KEY=change-me-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# .env (gitignored)
# Copie .env.example e preencha com valores reais
```

---

## entrypoint - inicialização inteligente

### por que entrypoint?

entrypoint é o script que roda quando o container inicia. ele é perfeito para:
- aguardar dependências ficarem prontas
- rodar migrations
- criar diretórios necessários
- validar configurações

### entrypoint básico

```bash
#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting application..."

# Aguardar banco de dados ficar pronto
echo "⏳ Waiting for database..."
until pg_isready -h db -U ${DB_USER} -d ${DB_NAME}; do
  echo "Database is unavailable - sleeping"
  sleep 2
done
echo "✅ Database is ready!"

# Rodar migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Criar superuser se não existir (apenas em dev)
if [ "$CREATE_SUPERUSER" = "true" ]; then
  echo "👤 Creating superuser..."
  python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
EOF
fi

# Executar comando passado (CMD do Dockerfile)
echo "✅ Starting application..."
exec "$@"
```

### entrypoint avançado

para aplicações mais complexas:

```bash
#!/bin/bash
set -e

# Função para log
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Função para aguardar serviço
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    
    log "⏳ Waiting for $service at $host:$port..."
    until nc -z $host $port; do
        log "$service is unavailable - sleeping"
        sleep 2
    done
    log "✅ $service is ready!"
}

# Aguardar dependências
wait_for_service db 5432 "PostgreSQL"
wait_for_service redis 6379 "Redis"

# Validar variáveis de ambiente críticas
if [ -z "$SECRET_KEY" ]; then
    log "❌ ERROR: SECRET_KEY not set"
    exit 1
fi

# Rodar migrations apenas se necessário
if [ "$RUN_MIGRATIONS" = "true" ]; then
    log "📦 Running migrations..."
    python manage.py migrate --noinput
fi

# Coletar estáticos apenas em produção
if [ "$ENVIRONMENT" = "production" ]; then
    log "📁 Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Healthcheck script
if [ "$1" = "healthcheck" ]; then
    python -c "import requests; requests.get('http://localhost:8000/health')"
    exit $?
fi

# Executar comando
log "✅ Starting application..."
exec "$@"
```

### tornar entrypoint executável

no dockerfile:

```dockerfile
# Copiar entrypoint
COPY entrypoint.sh /app/entrypoint.sh

# Tornar executável
RUN chmod +x /app/entrypoint.sh

# Usar como entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
```

---

## makefile - automação de tarefas

### por que makefile?

makefile é a forma mais simples de documentar e automatizar tarefas comuns. em vez de lembrar comandos longos, você só precisa rodar `make up` ou `make test`.

### makefile completo

```makefile
.PHONY: help build up down restart logs shell test clean

# Variáveis
COMPOSE_FILE = docker-compose.yml
COMPOSE = docker-compose -f $(COMPOSE_FILE)
DOCKER = docker

# Cores para output
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

help: ## Mostra esta mensagem de ajuda
	@echo "$(GREEN)Comandos disponíveis:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'

build: ## Constrói as imagens Docker
	$(COMPOSE) build

build-no-cache: ## Constrói sem usar cache
	$(COMPOSE) build --no-cache

up: ## Inicia todos os serviços
	$(COMPOSE) up -d

up-build: ## Constrói e inicia serviços
	$(COMPOSE) up -d --build

down: ## Para todos os serviços
	$(COMPOSE) down

down-volumes: ## Para serviços e remove volumes
	$(COMPOSE) down -v

restart: ## Reinicia todos os serviços
	$(COMPOSE) restart

logs: ## Mostra logs de todos os serviços
	$(COMPOSE) logs -f

logs-backend: ## Mostra logs apenas do backend
	$(COMPOSE) logs -f backend

shell: ## Abre shell no container backend
	$(COMPOSE) exec backend bash

shell-db: ## Abre shell no banco de dados
	$(COMPOSE) exec db psql -U $(DB_USER) -d $(DB_NAME)

test: ## Roda testes
	$(COMPOSE) exec backend pytest

test-watch: ## Roda testes em modo watch
	$(COMPOSE) exec backend pytest-watch

migrate: ## Roda migrations
	$(COMPOSE) exec backend python manage.py migrate

makemigrations: ## Cria novas migrations
	$(COMPOSE) exec backend python manage.py makemigrations

collectstatic: ## Coleta arquivos estáticos
	$(COMPOSE) exec backend python manage.py collectstatic --noinput

createsuperuser: ## Cria superuser Django
	$(COMPOSE) exec backend python manage.py createsuperuser

clean: ## Remove containers, volumes e imagens não utilizados
	$(DOCKER) system prune -a --volumes -f

clean-all: ## Remove tudo (containers, volumes, imagens, networks)
	$(COMPOSE) down -v --rmi all
	$(DOCKER) system prune -a --volumes -f

ps: ## Lista containers em execução
	$(COMPOSE) ps

status: ## Mostra status dos serviços
	$(COMPOSE) ps
	@echo "\n$(GREEN)Health checks:$(RESET)"
	@$(COMPOSE) ps --format json | jq -r '.[] | "\(.Name): \(.Health)"'

# Desenvolvimento
dev: ## Inicia ambiente de desenvolvimento
	$(COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml up

dev-build: ## Constrói e inicia ambiente de desenvolvimento
	$(COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml up --build

# Produção
prod: ## Inicia ambiente de produção
	$(COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-build: ## Constrói e inicia ambiente de produção
	$(COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Backup e restore
backup-db: ## Faz backup do banco de dados
	$(COMPOSE) exec db pg_dump -U $(DB_USER) $(DB_NAME) > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Restaura banco de dados (use: make restore-db FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then \
		echo "$(YELLOW)Erro: Especifique o arquivo com FILE=backup.sql$(RESET)"; \
		exit 1; \
	fi
	$(COMPOSE) exec -T db psql -U $(DB_USER) -d $(DB_NAME) < $(FILE)
```

### uso do makefile

```bash
# Ver todos os comandos disponíveis
make help

# Iniciar ambiente
make up

# Ver logs
make logs

# Rodar testes
make test

# Abrir shell no container
make shell

# Fazer backup do banco
make backup-db
```

---

## .dockerignore - otimizar builds

criar `.dockerignore` é essencial para builds rápidos:

```
# Git
.git
.gitignore
.gitattributes

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.eggs

# Virtual environments
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Environment
.env
.env.local
.env.*.local

# Tests
.pytest_cache/
.coverage
htmlcov/

# Documentation
docs/
*.md
!README.md

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore
```

---

## nginx configuration

### estrutura básica

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

---

## environment variables

### desenvolvimento

```bash
# .env (gitignored)
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=dev-secret-key
```

### produção

```bash
# .env.prod (no servidor, não versionado)
DEBUG=False
DATABASE_URL=postgresql://user:realpass@db:5432/prod_db
SECRET_KEY=production-secret-key-from-secrets-manager
```

### carregamento

```python
# sempre usar python-dotenv
from dotenv import load_dotenv
import os

# tentar carregar .env.prod primeiro, depois .env
if os.path.exists('.env.prod'):
    load_dotenv('.env.prod')
else:
    load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
```

---

## deployment process

### staging first

- sempre testar em staging antes de produção
- validar migrations antes de deploy
- ter rollback plan pronto
- monitorar após deploy

### checklist de deploy

- [ ] código testado em staging
- [ ] migrations validadas
- [ ] environment variables configuradas
- [ ] secrets atualizados
- [ ] backup do banco (se necessário)
- [ ] rollback plan documentado
- [ ] monitoramento ativo

---

## ci/cd pipelines

### estrutura básica

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: |
          # deployment commands
```

---

## boas práticas gerais

### 1. sempre use tags específicas

```dockerfile
# ❌ ruim - latest pode mudar
FROM python:latest

# ✅ bom - versão específica
FROM python:3.11-slim
```

### 2. ordene comandos por frequência de mudança

```dockerfile
# Comandos que mudam pouco primeiro (cache melhor)
FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc

# Comandos que mudam frequentemente por último
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 3. use .dockerignore

sem `.dockerignore`, você copia arquivos desnecessários, aumentando tempo de build e tamanho da imagem.

### 4. healthchecks em todos os serviços

healthchecks permitem que docker saiba quando serviços estão realmente prontos:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 5. restart policies

```yaml
# Sempre reiniciar se falhar
restart: always

# Reiniciar a menos que parado manualmente
restart: unless-stopped

# Nunca reiniciar automaticamente
restart: no
```

### 6. limites de recursos

em produção, sempre defina limites:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

---

## troubleshooting

### container não inicia

```bash
# Ver logs
docker-compose logs service-name

# Ver logs em tempo real
docker-compose logs -f service-name

# Entrar no container
docker-compose exec service-name bash
```

### build lento

```bash
# Verificar cache
docker system df

# Limpar cache
docker builder prune

# Build sem cache (para testar)
docker-compose build --no-cache
```

### volumes não funcionam

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect volume-name

# Remover volume
docker volume rm volume-name
```

---

## referências

- cicd agent → `../../../agents/cicd-agent.mdc`
- cicd context → `../../../../config/cicd/README.md`
- docker best practices → seção "dockerfile - a base de tudo" acima

---

**estas regras são obrigatórias para todos os deploys.**


