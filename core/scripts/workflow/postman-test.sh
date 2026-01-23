#!/usr/bin/env bash
# Executa testes Postman com Newman
# Usage: ./postman-test.sh [collection.json] [environment.json]

COLLECTION=${1:-postman/collection.json}
ENV=${2:-postman/environment.json}
REPORT_DIR=${REPORT_DIR:-reports/postman}

echo "🧪 Executando testes Postman..."

# Verificar se collection existe
if [ ! -f "$COLLECTION" ]; then
    echo "❌ Collection não encontrada: $COLLECTION"
    echo "   Execute primeiro: make postman-generate"
    exit 1
fi

# Criar diretório de relatórios
mkdir -p "$REPORT_DIR"

# Executar testes
echo "📊 Executando: $COLLECTION com environment: $ENV"
npx newman run "$COLLECTION" -e "$ENV" \
    --reporters cli,junit,html \
    --reporter-junit-export "$REPORT_DIR/junit-results.xml" \
    --reporter-html-export "$REPORT_DIR/report.html"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Testes concluídos com sucesso!"
    echo "📄 Relatórios:"
    echo "   - $REPORT_DIR/junit-results.xml"
    echo "   - $REPORT_DIR/report.html"
else
    echo ""
    echo "❌ Testes falharam (exit code: $EXIT_CODE)"
    echo "📄 Ver relatório: $REPORT_DIR/report.html"
fi

exit $EXIT_CODE

