#!/usr/bin/env bash
# Script para gerar novo projeto FastAPI a partir do template
# Usage: ./GENERATE_PROJECT.sh [project-name] [template-type]

set -e

PROJECT_NAME=${1:-my-fastapi-project}
TEMPLATE_TYPE=${2:-basic}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/$TEMPLATE_TYPE"
TARGET_DIR="$(pwd)/$PROJECT_NAME"

# Validar template
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "❌ Template não encontrado: $TEMPLATE_TYPE"
    echo "   Templates disponíveis: basic, with-framework"
    exit 1
fi

# Validar se diretório já existe
if [ -d "$TARGET_DIR" ]; then
    echo "❌ Diretório já existe: $TARGET_DIR"
    exit 1
fi

echo "🚀 Gerando projeto FastAPI..."
echo "   Nome: $PROJECT_NAME"
echo "   Template: $TEMPLATE_TYPE"
echo "   Destino: $TARGET_DIR"
echo ""

# Copiar template
echo "📋 Copiando arquivos do template..."
cp -r "$TEMPLATE_DIR" "$TARGET_DIR"

# Remover arquivos desnecessários
cd "$TARGET_DIR"
rm -f README.md  # Será recriado

# Criar README personalizado
cat > README.md << EOF
# $PROJECT_NAME

**Projeto FastAPI gerado a partir do template \`$TEMPLATE_TYPE\`.**

---

## 🚀 Quick Start

\`\`\`bash
# Instalar dependências
make install

# Configurar ambiente
cp .env.example .env
# Editar .env com suas configurações

# Subir banco de dados
make db-up

# Executar migrations
make migrate

# Iniciar servidor
make up
\`\`\`

---

## 📚 Documentação

- **Template Base:** \`core/templates/fastapi-project/$TEMPLATE_TYPE/\`
- **FastAPI Skill:** \`skills/backend/fastapi/SKILL.md\`
- **Database Snippets:** \`core/templates/database/\`
- **Cache Snippets:** \`core/templates/cache/\`

---

**Gerado em:** $(date +"%Y-%m-%d %H:%M:%S")
**Template:** $TEMPLATE_TYPE
EOF

# Substituir placeholders no código (se necessário)
echo "🔧 Configurando projeto..."

# Criar .env se não existir
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   ✅ .env criado (edite com suas configurações)"
fi

echo ""
echo "✅ Projeto gerado com sucesso!"
echo ""
echo "📝 Próximos passos:"
echo "   1. cd $PROJECT_NAME"
echo "   2. Editar .env com suas configurações"
echo "   3. make install"
echo "   4. make db-up"
echo "   5. make migrate"
echo "   6. make up"
echo ""
echo "📚 Documentação:"
echo "   - README.md (neste diretório)"
echo "   - core/templates/fastapi-project/README.md (template geral)"
if [ "$TEMPLATE_TYPE" = "with-framework" ]; then
    echo "   - core/templates/fastapi-project/FRAMEWORK_LIBRARY.md (biblioteca padrão)"
    echo "   - Repositório: https://github.com/LucasBiason/fastapi-microservice-framework"
fi

