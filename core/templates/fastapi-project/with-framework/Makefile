.PHONY: help install up down test lint format clean migrate upgrade downgrade db-up db-down

help:
	@echo "═══════════════════════════════════════════════"
	@echo "       FASTAPI PROJECT - MAKEFILE"
	@echo "═══════════════════════════════════════════════"
	@echo ""
	@echo "Available Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependências
	@pip install -r requirements/dev.txt

up: ## Subir aplicação
	@uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

down: ## Parar aplicação
	@pkill -f "uvicorn src.main:app" || true

db-up: ## Subir banco de dados
	@docker compose up -d db

db-down: ## Parar banco de dados
	@docker compose down

migrate: ## Criar nova migration (MESSAGE="description")
	@alembic revision --autogenerate -m "$(MESSAGE)"

upgrade: ## Aplicar migrations
	@alembic upgrade head

downgrade: ## Reverter última migration
	@alembic downgrade -1

test: ## Executar testes
	@pytest tests/ -v

test-cov: ## Executar testes com cobertura
	@pytest tests/ --cov=src --cov-report=html --cov-report=term

lint: ## Lint com ruff
	@ruff check src/ tests/

format: ## Formatar código com black
	@black src/ tests/

clean: ## Limpar arquivos temporários
	@find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	@rm -rf .pytest_cache/ .coverage htmlcov/ .mypy_cache/

.DEFAULT_GOAL := help

