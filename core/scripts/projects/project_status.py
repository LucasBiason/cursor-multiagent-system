#!/usr/bin/env python3
"""
Project Status - Status Consolidado dos Projetos

Gera um status consolidado de todos os projetos ativos,
evitando a criação de arquivos RESUMO_*.md espalhados.

Uso:
    python core/scripts/projects/project_status.py                     # Print para stdout
    python core/scripts/projects/project_status.py --output status.md  # Salvar em arquivo
    python core/scripts/projects/project_status.py --json              # Output JSON
    python core/scripts/projects/project_status.py --project hackathon # Projeto específico
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
PROJECTS_BASE = Path.home() / "Projetos" / "Projetos" / "Ativos"

# Projetos são carregados do arquivo de configuração
# config/system/tracked-projects.json (privado, não versionado no repo público)
def load_known_projects() -> Dict[str, Dict]:
    """Carrega projetos do arquivo de configuração."""
    config_paths = [
        PROJECT_ROOT / "config" / "system" / "tracked-projects.json",
        PROJECT_ROOT / "config" / "tracked-projects.json",
    ]

    for config_path in config_paths:
        if config_path.exists():
            with open(config_path) as f:
                data = json.load(f)
                # Converter paths de string para Path
                for project in data.values():
                    if "path" in project:
                        project["path"] = Path(project["path"]).expanduser()
                return data

    # Fallback: apenas o projeto atual (público)
    return {
        "cursor-multiagent": {
            "name": "Cursor Multiagent System",
            "path": PROJECT_ROOT,
            "type": "infrastructure",
            "priority": "ALTA",
        },
    }

KNOWN_PROJECTS = load_known_projects()


def get_git_info(project_path: Path) -> Dict[str, Any]:
    """Obtém informações do git de um projeto."""
    if not (project_path / ".git").exists():
        return {"has_git": False}

    info = {"has_git": True}

    try:
        # Branch atual
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        info["branch"] = result.stdout.strip() if result.returncode == 0 else "unknown"

        # Status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            changes = result.stdout.strip().split("\n") if result.stdout.strip() else []
            info["uncommitted_changes"] = len(changes)
            info["is_clean"] = len(changes) == 0

        # Último commit
        result = subprocess.run(
            ["git", "log", "-1", "--format=%h %s (%ar)"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        info["last_commit"] = result.stdout.strip() if result.returncode == 0 else "N/A"

    except (subprocess.TimeoutExpired, FileNotFoundError):
        info["error"] = "Erro ao obter info git"

    return info


def count_files(project_path: Path, pattern: str = "*.py") -> int:
    """Conta arquivos com determinado padrão."""
    if not project_path.exists():
        return 0
    return len(list(project_path.rglob(pattern)))


def check_tests(project_path: Path) -> Dict[str, Any]:
    """Verifica status dos testes."""
    tests_dir = project_path / "tests"
    test_files = list(project_path.rglob("test_*.py")) + list(project_path.rglob("*_test.py"))

    return {
        "has_tests_dir": tests_dir.exists(),
        "test_files_count": len(test_files),
    }


def get_project_status(project_id: str, project_info: Dict) -> Dict[str, Any]:
    """Obtém status completo de um projeto."""
    path = project_info.get("path")

    status = {
        "id": project_id,
        "name": project_info.get("name", project_id),
        "type": project_info.get("type", "unknown"),
        "priority": project_info.get("priority", "N/A"),
        "exists": path.exists() if path else False,
    }

    if project_info.get("deadline"):
        deadline = datetime.strptime(project_info["deadline"], "%Y-%m-%d")
        days_left = (deadline - datetime.now()).days
        status["deadline"] = project_info["deadline"]
        status["days_left"] = days_left

    if not status["exists"]:
        status["error"] = f"Projeto não encontrado em {path}"
        return status

    # Git info
    status["git"] = get_git_info(path)

    # Contagem de arquivos
    status["python_files"] = count_files(path, "*.py")
    status["md_files"] = count_files(path, "*.md")

    # Testes
    status["tests"] = check_tests(path)

    # README
    status["has_readme"] = (path / "README.md").exists()

    return status


def format_project_status(status: Dict) -> str:
    """Formata status de um projeto para exibição."""
    lines = []

    # Cabeçalho
    priority_emoji = {"CRÍTICA": "🔴", "ALTA": "🟠", "MÉDIA": "🟡", "BAIXA": "🟢"}.get(
        status.get("priority", ""), "⚪"
    )
    lines.append(f"\n## {priority_emoji} {status['name']}")
    lines.append(f"**Tipo:** {status['type']} | **Prioridade:** {status['priority']}")

    if not status.get("exists"):
        lines.append(f"❌ **ERRO:** {status.get('error', 'Projeto não encontrado')}")
        return "\n".join(lines)

    # Deadline
    if "deadline" in status:
        days_left = status.get("days_left", 0)
        if days_left < 0:
            lines.append(f"⚠️ **ATRASADO** por {abs(days_left)} dias (deadline: {status['deadline']})")
        elif days_left <= 7:
            lines.append(f"🔥 **{days_left} dias** para deadline ({status['deadline']})")
        else:
            lines.append(f"📅 Deadline: {status['deadline']} ({days_left} dias)")

    # Git
    git = status.get("git", {})
    if git.get("has_git"):
        branch = git.get("branch", "?")
        changes = git.get("uncommitted_changes", 0)
        clean_status = "✅ limpo" if git.get("is_clean") else f"⚠️ {changes} alterações"
        lines.append(f"**Git:** branch `{branch}` - {clean_status}")
        lines.append(f"**Último commit:** {git.get('last_commit', 'N/A')}")

    # Métricas
    lines.append(
        f"**Arquivos:** {status.get('python_files', 0)} .py | {status.get('md_files', 0)} .md"
    )

    # Testes
    tests = status.get("tests", {})
    if tests.get("has_tests_dir"):
        lines.append(f"**Testes:** {tests.get('test_files_count', 0)} arquivos de teste")
    else:
        lines.append("**Testes:** ⚠️ Sem diretório tests/")

    # README
    if not status.get("has_readme"):
        lines.append("⚠️ **README.md ausente**")

    return "\n".join(lines)


def generate_report(projects: Optional[List[str]] = None, format_type: str = "markdown") -> str:
    """Gera relatório de status."""
    if projects:
        project_list = {k: v for k, v in KNOWN_PROJECTS.items() if k in projects}
    else:
        project_list = KNOWN_PROJECTS

    statuses = []
    for project_id, project_info in project_list.items():
        statuses.append(get_project_status(project_id, project_info))

    # Ordenar por prioridade
    priority_order = {"CRÍTICA": 0, "ALTA": 1, "MÉDIA": 2, "BAIXA": 3}
    statuses.sort(key=lambda x: priority_order.get(x.get("priority", ""), 99))

    if format_type == "json":
        return json.dumps(statuses, indent=2, default=str, ensure_ascii=False)

    # Markdown
    lines = []
    lines.append("# Status dos Projetos")
    lines.append(f"\n**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (GMT-3)")
    lines.append(f"**Total:** {len(statuses)} projetos\n")

    # Sumário
    lines.append("## Sumário")
    for status in statuses:
        emoji = "✅" if status.get("git", {}).get("is_clean") else "🔄"
        deadline_info = ""
        if "days_left" in status:
            days = status["days_left"]
            if days <= 7:
                deadline_info = f" - ⏰ {days}d"
        lines.append(f"- {emoji} **{status['name']}** ({status['priority']}){deadline_info}")

    lines.append("\n---")

    # Detalhes
    for status in statuses:
        lines.append(format_project_status(status))

    lines.append("\n---")
    lines.append("*Gerado por `core/scripts/projects/project_status.py`*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Status consolidado dos projetos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s                          # Todos os projetos
  %(prog)s --project hackathon      # Projeto específico
  %(prog)s --output status.md       # Salvar em arquivo
  %(prog)s --json                   # Output JSON
        """,
    )

    parser.add_argument(
        "--project",
        "-p",
        action="append",
        help="Projeto específico (pode repetir)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Arquivo de saída (default: stdout)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output em formato JSON",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista projetos conhecidos",
    )

    args = parser.parse_args()

    if args.list:
        print("Projetos conhecidos:")
        for pid, pinfo in KNOWN_PROJECTS.items():
            print(f"  - {pid}: {pinfo['name']} ({pinfo['type']})")
        return

    format_type = "json" if args.json else "markdown"
    report = generate_report(args.project, format_type)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"✅ Relatório salvo em: {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
