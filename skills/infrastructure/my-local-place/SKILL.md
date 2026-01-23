# My Local Place - Local Infrastructure Platform

## Objetivo

Esta skill define padrões para uso do **My Local Place** como plataforma de infraestrutura local para desenvolvimento. Quando um projeto não possui ferramentas embutidas no `docker-compose.yml` (Redis, PostgreSQL, Kafka, Ollama, etc.), os agentes **DEVEM** sugerir ou usar o My Local Place.

---

## Quando Usar

**SEMPRE** considerar My Local Place quando:

1. ✅ Projeto não tem Redis no docker-compose
2. ✅ Projeto não tem PostgreSQL no docker-compose
3. ✅ Projeto não tem Kafka/RabbitMQ no docker-compose
4. ✅ Projeto não tem Ollama/Qwen no docker-compose
5. ✅ Projeto não tem MongoDB/MySQL no docker-compose
6. ✅ Projeto precisa de ferramentas de desenvolvimento local
7. ✅ Projeto precisa de observabilidade (Prometheus/Grafana)
8. ✅ Projeto precisa de ferramentas de automação (n8n)

**NÃO** usar My Local Place quando:

- ❌ Projeto já tem todas as ferramentas necessárias no docker-compose
- ❌ Projeto está em produção (usar serviços gerenciados)
- ❌ Projeto requer configurações muito específicas que não podem ser compartilhadas

---

## Localização

**Repositório:** `/home/lucas-biason/Projetos/Infraestrutura/my-local-place`

**Estrutura:**
```
my-local-place/
├── docker-compose.yml          # Orquestração principal
├── services/                    # Serviços individuais
│   ├── postgres/
│   ├── redis/
│   ├── kafka/
│   ├── ollama/
│   ├── evolution/              # Evolution API (WhatsApp)
│   └── ...
├── configs/                     # Configurações por serviço
└── README.md                    # Documentação completa
```

---

## Serviços Disponíveis

### Bancos de Dados

- **PostgreSQL** (`local-postgres`) - Porta 5432
- **MongoDB** (`local-mongodb`) - Porta 27017
- **MySQL** (`local-mysql`) - Porta 3306

### Cache e Mensageria

- **Redis** (`local-redis`) - Porta 6379
- **RabbitMQ** (`local-rabbitmq`) - Porta 5672
- **Kafka** (`local-kafka`) - Porta 9092

### IA e ML

- **Ollama** (`local-ollama`) - Porta 11434
- **OpenWebUI** (`local-openwebui`) - Porta 3001
- **LangFlow** (`local-langflow`) - Porta 7860
- **Jupyter** (`local-jupyter`) - Porta 8888

### Automação e Processamento

- **n8n** (`local-n8n`) - Porta 5678
- **BentoPDF** (`local-bentopdf`) - Porta 8080
- **Evolution API** (`local-evolution`) - Porta 8080

### Observabilidade

- **Prometheus** (`mylocalplace-prometheus`) - Porta 9090
- **Grafana** (`mylocalplace-grafana`) - Porta 3030

### Administração

- **PgAdmin** (`local-dbadmin`) - Porta 8080

---

## Como Usar

### 1. Iniciar Serviços

```bash
cd /home/lucas-biason/Projetos/Infraestrutura/my-local-place

# Iniciar todos os serviços
docker-compose --profile services up -d

# Iniciar serviço específico
docker-compose up -d local-postgres
docker-compose up -d local-redis
docker-compose up -d local-ollama
```

### 2. Verificar Status

```bash
# Ver status de todos os serviços
docker-compose ps

# Ver logs de um serviço
docker-compose logs -f local-postgres
```

### 3. Parar Serviços

```bash
# Parar todos os serviços
docker-compose --profile services down

# Parar serviço específico
docker-compose stop local-postgres
```

---

## Configuração de Conexão

### PostgreSQL

```python
# .env do projeto
DATABASE_URL=postgresql://postgres:senha@localhost:5432/nome_db
# ou
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=senha
DB_NAME=nome_db
```

### Redis

```python
# .env do projeto
REDIS_URL=redis://localhost:6379
# ou
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=senha
```

### Kafka

```python
# .env do projeto
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

### Ollama

```python
# .env do projeto
OLLAMA_BASE_URL=http://localhost:11434
```

### Evolution API

```python
# .env do projeto
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_chave_aqui
EVOLUTION_INSTANCE_NAME=nome_instancia
```

---

## Padrões de Uso

### Padrão 1: Projeto Precisa de Redis

**Situação:** Projeto precisa de cache Redis mas não tem no docker-compose.

**Solução:**
1. Verificar se My Local Place tem Redis disponível ✅
2. Iniciar Redis no My Local Place: `docker-compose up -d local-redis`
3. Configurar variáveis de ambiente no projeto:
   ```bash
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_PASSWORD=senha_do_my_local_place
   ```
4. Documentar no README do projeto que usa My Local Place

### Padrão 2: Projeto Precisa de PostgreSQL

**Situação:** Projeto precisa de banco PostgreSQL mas não tem no docker-compose.

**Solução:**
1. Verificar se My Local Place tem PostgreSQL disponível ✅
2. Iniciar PostgreSQL no My Local Place: `docker-compose up -d local-postgres`
3. Criar banco de dados:
   ```bash
   docker exec -it local-postgres psql -U postgres -c "CREATE DATABASE nome_db;"
   ```
4. Configurar variáveis de ambiente no projeto:
   ```bash
   DATABASE_URL=postgresql://postgres:senha@localhost:5432/nome_db
   ```
5. Documentar no README do projeto

### Padrão 3: Projeto Precisa de Ollama

**Situação:** Projeto precisa de LLM local mas não tem no docker-compose.

**Solução:**
1. Verificar se My Local Place tem Ollama disponível ✅
2. Iniciar Ollama no My Local Place: `docker-compose up -d local-ollama`
3. Baixar modelo necessário:
   ```bash
   docker exec -it local-ollama ollama pull llama2
   ```
4. Configurar variáveis de ambiente no projeto:
   ```bash
   OLLAMA_BASE_URL=http://localhost:11434
   ```
5. Documentar no README do projeto

---

## Adicionar Novo Serviço

Quando um novo serviço precisa ser adicionado ao My Local Place:

### 1. Criar Estrutura

```bash
cd /home/lucas-biason/Projetos/Infraestrutura/my-local-place
mkdir -p services/novo-servico
```

### 2. Criar docker-compose.yml do Serviço

```yaml
# services/novo-servico/docker-compose.yml
version: '3'

services:
  novo-servico:
    hostname: novo-servico
    image: imagem:tag
    ports:
      - "PORTA:PORTA"
    environment:
      - VAR1=${VAR1}
      - VAR2=${VAR2}
    volumes:
      - novo_servico_data:/data
    restart: on-failure:5
    healthcheck:
      test: ["CMD", "healthcheck-command"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  novo_servico_data:
```

### 3. Adicionar ao docker-compose.yml Principal

```yaml
# docker-compose.yml
local-novo-servico:
  container_name: local-novo-servico
  extends:
    file: services/novo-servico/docker-compose.yml
    service: novo-servico
  env_file:
    - .env
  networks:
    - local-services-network
  healthcheck:
    test: ["CMD", "healthcheck-command"]
    interval: 10s
    timeout: 5s
    retries: 5
  profiles: ["services"]
```

### 4. Adicionar Volume

```yaml
# docker-compose.yml (seção volumes)
volumes:
  # ... outros volumes
  novo_servico_data:
```

### 5. Documentar

- Adicionar ao README.md do My Local Place
- Adicionar exemplo de configuração
- Adicionar variáveis de ambiente necessárias

---

## Checklist de Integração

Ao sugerir ou usar My Local Place:

- [ ] Verificar se serviço está disponível no My Local Place
- [ ] Iniciar serviço: `docker-compose up -d local-[servico]`
- [ ] Verificar saúde: `docker-compose ps`
- [ ] Configurar variáveis de ambiente no projeto
- [ ] Testar conexão do projeto com o serviço
- [ ] Documentar no README do projeto que usa My Local Place
- [ ] Adicionar instruções de setup no README

---

## Exemplos de Uso

### Exemplo 1: Projeto FastAPI Precisa de Redis

```bash
# 1. Iniciar Redis no My Local Place
cd /home/lucas-biason/Projetos/Infraestrutura/my-local-place
docker-compose up -d local-redis

# 2. Configurar no projeto
# .env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=senha_do_my_local_place

# 3. Testar conexão
python -c "import redis; r = redis.Redis(host='localhost', port=6379, password='senha'); print(r.ping())"
```

### Exemplo 2: Projeto Precisa de PostgreSQL

```bash
# 1. Iniciar PostgreSQL no My Local Place
cd /home/lucas-biason/Projetos/Infraestrutura/my-local-place
docker-compose up -d local-postgres

# 2. Criar banco
docker exec -it local-postgres psql -U postgres -c "CREATE DATABASE meu_projeto;"

# 3. Configurar no projeto
# .env
DATABASE_URL=postgresql://postgres:senha@localhost:5432/meu_projeto

# 4. Rodar migrations
python manage.py migrate  # Django
# ou
alembic upgrade head  # FastAPI
```

### Exemplo 3: Projeto Precisa de Evolution API

```bash
# 1. Iniciar Evolution no My Local Place
cd /home/lucas-biason/Projetos/Infraestrutura/my-local-place
docker-compose up -d local-evolution

# 2. Configurar no projeto
# .env
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_chave_aqui
EVOLUTION_INSTANCE_NAME=meu_projeto

# 3. Verificar saúde
curl http://localhost:8080/health
```

---

## Referências

- **Repositório:** `/home/lucas-biason/Projetos/Infraestrutura/my-local-place`
- **README:** Ver `my-local-place/README.md` para documentação completa
- **Docker Compose:** Ver `my-local-place/docker-compose.yml` para todos os serviços

---

## Notas Importantes

1. **Sempre verificar se serviço já está rodando:** `docker-compose ps`
2. **Usar profiles:** Serviços usam profile `services` para não iniciar automaticamente
3. **Variáveis de ambiente:** Sempre usar `.env` do My Local Place para configurações
4. **Rede compartilhada:** Todos os serviços usam `local-services-network`
5. **Health checks:** Todos os serviços têm health checks configurados
6. **Volumes persistentes:** Dados são persistidos em volumes Docker

---

## Integração com Agentes

Agentes de programação **DEVEM**:

1. **Reconhecer** quando projeto precisa de ferramenta não disponível no docker-compose
2. **Sugerir** uso do My Local Place
3. **Iniciar** serviço necessário no My Local Place
4. **Configurar** variáveis de ambiente no projeto
5. **Testar** conexão
6. **Documentar** uso no README do projeto

**Exemplo de resposta do agente:**

```
✅ Redis configurado via My Local Place!

📊 Configuração:
- Serviço: local-redis (porta 6379)
- Status: ✅ Rodando
- Variáveis configuradas no .env

🔗 Conexão testada com sucesso!

📝 Documentação atualizada no README.md
```

