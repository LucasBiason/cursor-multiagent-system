#!/usr/bin/env bash
# Executa testes de uma collection Postman usando Newman
# 
# IMPORTANTE: Este script NÃO converte OpenAPI/Swagger em Postman.
# Ele apenas EXECUTA uma collection Postman já existente.
# 
# Para converter OpenAPI → Postman, use: ./generate-from-openapi.sh
#
# Usage: ./run_newman.sh [collection.json] [environment.json]

COLLECTION=${1:-postman/collection.json}
ENV=${2:-postman/environment.json}
REPORT_DIR=${REPORT_DIR:-reports/postman}

mkdir -p "$REPORT_DIR"

npx newman run "$COLLECTION" -e "$ENV" \
  --reporters cli,junit,html \
  --reporter-junit-export "$REPORT_DIR/junit-results.xml" \
  --reporter-html-export "$REPORT_DIR/report.html"

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "Newman tests failed (exit $EXIT_CODE)"
  exit $EXIT_CODE
fi

echo "Newman finished."

