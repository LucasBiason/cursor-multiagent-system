#!/usr/bin/env bash
# Gera collection Postman a partir de OpenAPI/Swagger
# Usage: ./generate-from-openapi.sh [openapi.json] [output-dir]

OPENAPI_FILE=${1:-openapi.json}
OUTPUT_DIR=${2:-postman}

echo "🔄 Convertendo OpenAPI para Postman Collection..."

# Verificar se openapi-to-postmanv2 está instalado
if ! command -v openapi-to-postmanv2 &> /dev/null; then
    echo "❌ openapi-to-postmanv2 não encontrado"
    echo "📦 Instalando..."
    npm install -g openapi-to-postmanv2
fi

# Criar diretório de saída
mkdir -p "$OUTPUT_DIR"

# Converter OpenAPI para Postman
echo "📝 Convertendo $OPENAPI_FILE para $OUTPUT_DIR/collection.json..."
openapi-to-postmanv2 -s "$OPENAPI_FILE" -o "$OUTPUT_DIR/collection.json"

if [ $? -eq 0 ]; then
    echo "✅ Collection gerada em $OUTPUT_DIR/collection.json"
    echo ""
    echo "⚠️  PRÓXIMOS PASSOS:"
    echo "1. Adicionar scripts de autenticação (pre-request e test scripts)"
    echo "2. Configurar variáveis de ambiente (environment.json)"
    echo "3. Adicionar exemplos de resposta manualmente"
    echo "4. Executar testes: ./run_newman.sh $OUTPUT_DIR/collection.json $OUTPUT_DIR/environment.json"
else
    echo "❌ Erro ao converter OpenAPI para Postman"
    exit 1
fi

