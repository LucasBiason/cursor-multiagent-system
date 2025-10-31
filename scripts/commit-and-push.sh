#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_DIR}"

echo "================================================"
echo "   Cursor Multiagent System - Commit & Push"
echo "================================================"
echo ""

if [ -z "$1" ]; then
    echo "Erro: Mensagem de commit não fornecida"
    echo "Uso: ./scripts/commit-and-push.sh \"mensagem do commit\""
    exit 1
fi

COMMIT_MESSAGE="$1"

echo "1. Verificando alterações..."
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "   ✓ Alterações detectadas"
else
    echo "   ✗ Nenhuma alteração para commitar"
    exit 0
fi

echo ""
echo "2. Adicionando arquivos ao staging..."
git add -A
echo "   ✓ Arquivos adicionados"

echo ""
echo "3. Verificando por tokens sensíveis..."
# Procura por tokens Notion reais (excluindo placeholders conhecidos)
if git diff --cached | grep -E "ntn_[0-9]{10,}[a-zA-Z0-9]{20,}" > /dev/null 2>&1; then
    echo "   ✗ AVISO: Token Notion real detectado! Remova antes de commitar."
    exit 1
fi
echo "   ✓ Nenhum token sensível detectado"

echo ""
echo "4. Criando commit..."
git commit -m "${COMMIT_MESSAGE}"
echo "   ✓ Commit criado"

echo ""
echo "5. Enviando para GitHub..."
git push origin main
echo "   ✓ Push concluído"

echo ""
echo "================================================"
echo "   ✓ Commit e push realizados com sucesso!"
echo "================================================"
echo ""
echo "Ver no GitHub: https://github.com/LucasBiason/cursor-multiagent-system"

