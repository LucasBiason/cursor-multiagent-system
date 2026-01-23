#!/usr/bin/env bash
# Atualiza collection Postman a partir de OpenAPI
# Usage: ./postman-update.sh [openapi.json]

OPENAPI_FILE=${1:-openapi.json}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "🔄 Atualizando collection Postman a partir de OpenAPI..."

# Verificar se OpenAPI existe
if [ ! -f "$OPENAPI_FILE" ]; then
    echo "❌ Arquivo OpenAPI não encontrado: $OPENAPI_FILE"
    exit 1
fi

# Verificar se collection existe
if [ ! -f "postman/collection.json" ]; then
    echo "⚠️  Collection não existe. Gerando nova collection..."
    "$SCRIPT_DIR/postman-generate.sh" "$OPENAPI_FILE" postman
else
    echo "📝 Atualizando collection existente..."
    "$SCRIPT_DIR/postman-generate.sh" "$OPENAPI_FILE" postman
    echo "⚠️  Verifique se scripts customizados foram preservados"
fi

