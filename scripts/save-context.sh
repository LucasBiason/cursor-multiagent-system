#!/bin/bash
# Script para salvar contexto automaticamente após cada interação

CONFIG_DIR="/home/lucas-biason/Projetos/Infraestrutura/cursor-multiagent-system/config"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S GMT-3")

# Criar arquivo de contexto da sessão
SESSION_FILE="$CONFIG_DIR/sessions/$(date +%Y%m%d_%H%M%S)_context.md"

mkdir -p "$CONFIG_DIR/sessions"

cat > "$SESSION_FILE" << EOF
# Contexto da Sessão
**Data:** $TIMESTAMP
**Máquina:** $(hostname)
**Usuário:** $(whoami)

## Interação
\`\`\`
$(cat)
\`\`\`

## Status do Sistema
- **Última Atualização:** $TIMESTAMP
- **Projetos Ativos:** Ver CONTEXTO_COMPLETO_ATUAL.md
- **Próximas Ações:** Ver PROJETOS_DETALHADOS.md

EOF

# Atualizar timestamp no contexto principal
sed -i "s/^\\*\\*Última Atualização:\\*\\*.*/\\*\\*Última Atualização:\\*\\* $TIMESTAMP/" \
    "$CONFIG_DIR/CONTEXTO_COMPLETO_ATUAL.md" 2>/dev/null || true

# Commit automático no repositório privado
cd "$CONFIG_DIR"
if [ -d ".git" ]; then
    git add -A
    git commit -m "Auto-save: $TIMESTAMP" 2>/dev/null || true
    git push origin master 2>/dev/null || true
fi

echo "Contexto salvo: $SESSION_FILE"

