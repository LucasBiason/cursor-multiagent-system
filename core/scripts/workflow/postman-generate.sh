#!/usr/bin/env bash
# Gera collection Postman a partir de OpenAPI/Swagger
# Usage: ./postman-generate.sh [openapi.json] [output-dir]

OPENAPI_FILE=${1:-openapi.json}
OUTPUT_DIR=${2:-postman}

echo "🔄 Convertendo OpenAPI para Postman Collection..."

# Procurar arquivo OpenAPI se não encontrado
if [ ! -f "$OPENAPI_FILE" ]; then
    echo "❌ Arquivo OpenAPI não encontrado: $OPENAPI_FILE"
    echo "   Procurando em locais comuns..."
    for file in openapi.json swagger.json docs/openapi.yaml docs/swagger.yaml; do
        if [ -f "$file" ]; then
            echo "   ✅ Encontrado: $file"
            OPENAPI_FILE=$file
            break
        fi
    done
    if [ ! -f "$OPENAPI_FILE" ]; then
        echo "   ❌ Nenhum arquivo OpenAPI encontrado"
        exit 1
    fi
fi

# Criar diretório de saída
mkdir -p "$OUTPUT_DIR"

# Verificar se openapi-to-postmanv2 está instalado
if ! command -v openapi-to-postmanv2 &> /dev/null; then
    echo "📦 Instalando openapi-to-postmanv2..."
    npm install -g openapi-to-postmanv2 || {
        echo "❌ Erro ao instalar. Execute: npm install -g openapi-to-postmanv2"
        exit 1
    }
fi

# Converter OpenAPI para Postman
echo "📝 Convertendo $OPENAPI_FILE para $OUTPUT_DIR/collection.json..."
openapi-to-postmanv2 -s "$OPENAPI_FILE" -o "$OUTPUT_DIR/collection.json" || {
    echo "❌ Erro ao converter OpenAPI para Postman"
    exit 1
}

echo "✅ Collection gerada em $OUTPUT_DIR/collection.json"
echo ""
echo "⚠️  PRÓXIMOS PASSOS:"
echo "1. Adicionar scripts de autenticação (pre-request e test scripts)"
echo "2. Configurar variáveis de ambiente ($OUTPUT_DIR/environment.json)"
echo "3. Adicionar exemplos de resposta manualmente"
echo "4. Executar testes: make postman-test"

