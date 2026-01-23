# ============================================
# Makefile para Projeto Django
# ============================================
# 
# Este Makefile segue os padrões do cursor-multiagent-system.
# Para detalhes completos sobre Makefiles, consulte:
# - Makefile Skill: skills/infrastructure/makefile/SKILL.md
#
# Comandos principais DEVEM estar no Makefile.
# Use 'make help' para ver todos os comandos disponíveis.
#
# ============================================

.PHONY: help build build-test build-prod run run-dev test lint format export-reqs push scan clean

# Variáveis
IMAGE_NAME ?= django-app
PYTHON_VERSION ?= 3.11
REGISTRY ?= 
TAG ?= latest

help: ## Mostra esta mensagem de ajuda
	@echo "═══════════════════════════════════════════════"
	@echo "       DJANGO PROJECT - MAKEFILE"
	@echo "═══════════════════════════════════════════════"
	@echo ""
	@echo "Available Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build da imagem final (runtime)
	docker build -t $(IMAGE_NAME):$(TAG) --target runtime -f Dockerfile .

build-test: ## Build até o stage de testes
	docker build -t $(IMAGE_NAME):test --target test -f Dockerfile .

build-prod: ## Build da imagem de produção (runtime)
	docker build -t $(IMAGE_NAME):$(TAG) --target runtime -f Dockerfile .

build-builder: ## Build apenas o stage builder
	docker build -t $(IMAGE_NAME):builder --target builder -f Dockerfile .

run: ## Executar container em modo produção
	docker run --rm -p 8000:8000 \
		-e DATABASE_URL=$(DATABASE_URL) \
		-e SECRET_KEY=$(SECRET_KEY) \
		$(IMAGE_NAME):$(TAG)

run-dev: ## Executar container em modo desenvolvimento
	docker run --rm -p 8000:8000 \
		-e DATABASE_URL=$(DATABASE_URL) \
		-e SECRET_KEY=$(SECRET_KEY) \
		-e DEBUG=True \
		$(IMAGE_NAME):$(TAG) dev

test: ## Executar testes no container
	docker build -t $(IMAGE_NAME):test --target test -f Dockerfile . && \
	docker run --rm $(IMAGE_NAME):test

test-local: ## Executar testes localmente (fora do Docker)
	pytest --cov=app --cov-report=term-missing --cov-report=html -v

lint: ## Lint do código
	ruff check app/ tests/
	black --check app/ tests/

format: ## Formatar código
	black app/ tests/
	ruff check --fix app/ tests/

export-reqs: ## Exportar requirements.txt do Poetry (se usar Poetry)
	poetry export -f requirements.txt --output requirements.txt --without-hashes

export-reqs-dev: ## Exportar requirements.txt com dev dependencies
	poetry export -f requirements.txt --output requirements-dev.txt --without-hashes --with dev

push: ## Push da imagem para registry
	@if [ -z "$(REGISTRY)" ]; then \
		echo "❌ ERROR: REGISTRY não definido. Use: make push REGISTRY=myregistry.io"; \
		exit 1; \
	fi
	docker tag $(IMAGE_NAME):$(TAG) $(REGISTRY)/$(IMAGE_NAME):$(TAG)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(TAG)

scan: ## Escanear imagem para vulnerabilidades (requer Trivy)
	@if ! command -v trivy &> /dev/null; then \
		echo "⚠️  Trivy não encontrado. Instale: https://github.com/aquasecurity/trivy"; \
		exit 1; \
	fi
	trivy image $(IMAGE_NAME):$(TAG)

clean: ## Limpar imagens Docker locais
	docker rmi $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):test $(IMAGE_NAME):builder 2>/dev/null || true
	docker system prune -f

.DEFAULT_GOAL := help

