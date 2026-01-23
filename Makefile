.PHONY: help validate test clean install setup pre-commit-install postman-generate postman-test postman-validate postman-update

help:
	@echo "═══════════════════════════════════════════════"
	@echo "       CURSOR MULTIAGENT SYSTEM - MAKEFILE"
	@echo "═══════════════════════════════════════════════"
	@echo ""
	@echo "Available Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'

validate: ## Validar configuração e segurança
	@./core/scripts/infrastructure/validate.sh

test: ## Executar testes (se existirem)
	@echo "No tests configured yet"

install: ## Instalar dependências
	@pip install -r requirements.txt

setup: ## Setup inicial do projeto
	@./core/scripts/infrastructure/setup.sh

pre-commit-install: ## Instalar pre-commit hooks
	@pip install pre-commit
	@pre-commit install
	@echo "Pre-commit hooks instalados"

clean: ## Limpar arquivos temporários
	@python core/scripts/workflow/cleanup_temp.py --execute

# Postman Commands
postman-generate: ## Converter OpenAPI/Swagger em collection Postman (OPENAPI=openapi.json OUTPUT=postman)
	@./core/scripts/workflow/postman-generate.sh $(OPENAPI) $(OUTPUT)

postman-test: ## Executar testes Postman com Newman (COLLECTION=postman/collection.json ENV=postman/environment.json)
	@./core/scripts/workflow/postman-test.sh $(COLLECTION) $(ENV)

postman-validate: ## Validar estrutura da collection Postman (COLLECTION=postman/collection.json)
	@./core/scripts/workflow/postman-validate.sh $(COLLECTION)

postman-update: ## Atualizar collection Postman a partir de OpenAPI (OPENAPI=openapi.json)
	@./core/scripts/workflow/postman-update.sh $(OPENAPI)

.DEFAULT_GOAL := help

