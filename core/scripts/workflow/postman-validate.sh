#!/usr/bin/env bash
# Valida estrutura da collection Postman
# Usage: ./postman-validate.sh [collection.json]

COLLECTION=${1:-postman/collection.json}

echo "🔍 Validando collection Postman..."

# Verificar se collection existe
if [ ! -f "$COLLECTION" ]; then
    echo "❌ Collection não encontrada: $COLLECTION"
    exit 1
fi

# Validar com jq se disponível
if command -v jq &> /dev/null; then
    echo "✅ Validando JSON..."
    if ! jq empty "$COLLECTION" 2>/dev/null; then
        echo "   ❌ JSON inválido"
        exit 1
    fi
    echo "   ✅ JSON válido"
    
    echo "✅ Verificando estrutura..."
    if ! jq -e '.info' "$COLLECTION" > /dev/null 2>&1; then
        echo "   ❌ Campo 'info' ausente"
        exit 1
    fi
    echo "   ✅ Campo 'info' presente"
    
    if ! jq -e '.item' "$COLLECTION" > /dev/null 2>&1; then
        echo "   ❌ Campo 'item' ausente"
        exit 1
    fi
    echo "   ✅ Campo 'item' presente"
    
    ITEM_COUNT=$(jq '.item | length' "$COLLECTION")
    if [ "$ITEM_COUNT" -gt 0 ]; then
        echo "   ✅ Collection contém $ITEM_COUNT item(s)"
    else
        echo "   ⚠️  Collection vazia (sem requests)"
    fi
    
    echo ""
    echo "✅ Collection válida: $COLLECTION"
else
    echo "⚠️  jq não instalado. Validando apenas se arquivo existe..."
    echo "✅ Collection encontrada: $COLLECTION"
    echo "   Instale jq para validação completa: sudo apt-get install jq"
fi

