#!/usr/bin/env python3
"""
Script Python para salvar contexto automaticamente após cada interação.
Deve ser chamado pelos agentes após cada interação significativa.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import json

# Configurações
# Get the project root directory (parent of scripts/)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SESSIONS_DIR = CONFIG_DIR / "sessions"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S GMT-3")
HOSTNAME = os.uname().nodename if hasattr(os, 'uname') else os.environ.get('HOSTNAME', 'unknown')

def save_session_context(interaction_summary: str = "", changes: dict = None):
    """
    Salva o contexto da sessão atual.
    
    Args:
        interaction_summary: Resumo da interação
        changes: Dicionário com mudanças realizadas
    """
    SESSIONS_DIR.mkdir(exist_ok=True)
    
    session_file = SESSIONS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_context.md"
    
    content = f"""# Contexto da Sessão
**Data:** {TIMESTAMP}
**Máquina:** {HOSTNAME}
**Usuário:** {os.environ.get('USER', 'unknown')}

## Resumo da Interação
{interaction_summary if interaction_summary else "Interação automática"}

## Mudanças Realizadas
"""
    
    if changes:
        for key, value in changes.items():
            content += f"- **{key}:** {value}\n"
    else:
        content += "- Nenhuma mudança específica registrada\n"
    
    content += f"""
## Status do Sistema
- **Última Atualização:** {TIMESTAMP}
- **Projetos Ativos:** Ver CONTEXTO_COMPLETO_ATUAL.md
- **Próximas Ações:** Ver PROJETOS_DETALHADOS.md

## Arquivos de Referência
- `CONTEXTO_COMPLETO_ATUAL.md` - Contexto geral do sistema
- `PROJETOS_DETALHADOS.md` - Detalhes dos projetos
- `user-context.md` - Contexto do usuário
- `system-context.md` - Contexto do sistema
"""
    
    session_file.write_text(content, encoding='utf-8')
    print(f"✅ Contexto salvo: {session_file}")
    
    # Atualizar timestamp no contexto principal
    update_main_context_timestamp()
    
    # Commit automático
    commit_context_changes(interaction_summary)
    
    return session_file

def update_main_context_timestamp():
    """Atualiza o timestamp no arquivo de contexto principal"""
    context_file = CONFIG_DIR / "CONTEXTO_COMPLETO_ATUAL.md"
    if context_file.exists():
        content = context_file.read_text(encoding='utf-8')
        # Substituir última atualização
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('**Última Atualização:**'):
                lines[i] = f"**Última Atualização:** {TIMESTAMP}"
                break
        context_file.write_text('\n'.join(lines), encoding='utf-8')

def commit_context_changes(message: str = None):
    """Faz commit automático das mudanças no repositório privado"""
    if not (CONFIG_DIR / ".git").exists():
        return
    
    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=CONFIG_DIR,
            check=True,
            capture_output=True
        )
        
        commit_msg = message or f"Auto-save: {TIMESTAMP}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=CONFIG_DIR,
            check=False,  # Não falhar se não houver mudanças
            capture_output=True
        )
        
        # Tentar push (pode falhar se não houver conexão)
        subprocess.run(
            ["git", "push", "origin", "master"],
            cwd=CONFIG_DIR,
            check=False,
            capture_output=True
        )
    except Exception as e:
        print(f"⚠️  Erro ao commitar: {e}")

def save_project_update(project_name: str, status: str, details: str = ""):
    """Salva atualização específica de um projeto"""
    changes = {
        "Projeto": project_name,
        "Status": status,
        "Detalhes": details
    }
    return save_session_context(
        interaction_summary=f"Atualização do projeto: {project_name}",
        changes=changes
    )

if __name__ == "__main__":
    # Exemplo de uso
    if len(sys.argv) > 1:
        summary = sys.argv[1]
        save_session_context(interaction_summary=summary)
    else:
        save_session_context()

