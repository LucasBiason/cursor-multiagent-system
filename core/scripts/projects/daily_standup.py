#!/usr/bin/env python3
"""
Daily Standup - Preparação de Standup/Planning

Gera resumo para standup diário ou planning semanal,
consolidando informações de projetos, tarefas e compromissos.

Uso:
    python core/scripts/projects/daily_standup.py           # Standup de hoje
    python core/scripts/projects/daily_standup.py --week    # Planning semanal
    python core/scripts/projects/daily_standup.py --focus   # Modo focado (apenas prioridades)
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent
PROJECTS_BASE = Path.home() / "Projetos" / "Projetos" / "Ativos"

# Projetos são carregados do arquivo de configuração
# config/system/tracked-projects.json (privado, não versionado no repo público)
def load_tracked_projects() -> Dict[str, Dict]:
    """Carrega projetos do arquivo de configuração."""
    config_paths = [
        PROJECT_ROOT / "config" / "system" / "tracked-projects.json",
        PROJECT_ROOT / "config" / "tracked-projects.json",
    ]

    for config_path in config_paths:
        if config_path.exists():
            import json
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
            "priority": 3,
            "tags": ["infraestrutura", "workflow"],
        },
    }

TRACKED_PROJECTS = load_tracked_projects()

# Focos possíveis por dia da semana
WEEKLY_FOCUS = {
    0: "Planejamento semanal, revisão de backlog",  # Segunda
    1: "Desenvolvimento - foco em hackathon",  # Terça
    2: "Desenvolvimento - foco em trabalho",  # Quarta
    3: "Code review, testes, documentação",  # Quinta
    4: "Finalização de tasks, preparar próxima semana",  # Sexta
    5: "Descanso / estudos livres",  # Sábado
    6: "Descanso / estudos livres",  # Domingo
}


def get_greeting() -> str:
    """Retorna saudação baseada no horário."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Bom dia"
    elif 12 <= hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"


def get_git_changes(project_path: Path) -> Dict[str, Any]:
    """Obtém mudanças pendentes no git."""
    if not (project_path / ".git").exists():
        return {"has_git": False}

    try:
        # Status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        changes = result.stdout.strip().split("\n") if result.stdout.strip() else []

        # Commits não pushados
        result = subprocess.run(
            ["git", "log", "--oneline", "@{u}..HEAD"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        unpushed = result.stdout.strip().split("\n") if result.stdout.strip() else []

        return {
            "has_git": True,
            "uncommitted": len(changes),
            "unpushed": len([c for c in unpushed if c]),
            "is_clean": len(changes) == 0 and len([c for c in unpushed if c]) == 0,
        }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {"has_git": True, "error": True}


def calculate_deadline_urgency(deadline_str: str) -> Dict[str, Any]:
    """Calcula urgência baseada no deadline."""
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
    days_left = (deadline - datetime.now()).days

    if days_left < 0:
        return {"status": "ATRASADO", "days": abs(days_left), "emoji": "🔴", "urgent": True}
    elif days_left <= 3:
        return {"status": "CRÍTICO", "days": days_left, "emoji": "🔴", "urgent": True}
    elif days_left <= 7:
        return {"status": "URGENTE", "days": days_left, "emoji": "🟠", "urgent": True}
    elif days_left <= 14:
        return {"status": "PRÓXIMO", "days": days_left, "emoji": "🟡", "urgent": False}
    else:
        return {"status": "OK", "days": days_left, "emoji": "🟢", "urgent": False}


def get_today_tasks() -> List[str]:
    """
    Retorna tarefas sugeridas para hoje.
    Pode ser integrado com Notion futuramente.
    """
    weekday = datetime.now().weekday()

    tasks = []

    # Adicionar tarefas baseadas no dia
    if weekday == 0:  # Segunda
        tasks.extend([
            "Revisar plano da semana",
            "Verificar emails/mensagens pendentes",
            "Definir prioridades da semana",
        ])
    elif weekday in [1, 2, 3]:  # Terça a Quinta
        tasks.extend([
            "Continuar desenvolvimento",
            "Revisar PRs pendentes",
        ])
    elif weekday == 4:  # Sexta
        tasks.extend([
            "Finalizar tasks em andamento",
            "Documentar progresso",
            "Preparar planejamento próxima semana",
        ])

    return tasks


def format_project_summary(project_id: str, project_info: Dict) -> List[str]:
    """Formata resumo de um projeto."""
    lines = []
    path = project_info.get("path")

    # Nome e status
    git_info = get_git_changes(path) if path and path.exists() else {"has_git": False}

    status_emoji = "✅" if git_info.get("is_clean") else "🔄"
    lines.append(f"### {status_emoji} {project_info['name']}")

    # Deadline
    if "deadline" in project_info:
        urgency = calculate_deadline_urgency(project_info["deadline"])
        if urgency["status"] == "ATRASADO":
            lines.append(f"   {urgency['emoji']} **ATRASADO** por {urgency['days']} dias!")
        else:
            lines.append(
                f"   {urgency['emoji']} {urgency['status']}: {urgency['days']} dias restantes"
            )

    # Git status
    if git_info.get("has_git") and not git_info.get("error"):
        if not git_info.get("is_clean"):
            if git_info.get("uncommitted", 0) > 0:
                lines.append(f"   ⚠️ {git_info['uncommitted']} alterações não commitadas")
            if git_info.get("unpushed", 0) > 0:
                lines.append(f"   ⚠️ {git_info['unpushed']} commits não pushados")

    return lines


def generate_daily_standup() -> str:
    """Gera standup diário."""
    lines = []
    now = datetime.now()

    # Header
    lines.append(f"# {get_greeting()}! Standup de {now.strftime('%d/%m/%Y')}")
    lines.append(f"**{now.strftime('%A')}** - {WEEKLY_FOCUS.get(now.weekday(), 'Dia produtivo!')}")
    lines.append("")

    # Projetos urgentes primeiro
    lines.append("## 🎯 Projetos Prioritários")

    urgent_projects = []
    other_projects = []

    for pid, pinfo in sorted(TRACKED_PROJECTS.items(), key=lambda x: x[1].get("priority", 99)):
        if "deadline" in pinfo:
            urgency = calculate_deadline_urgency(pinfo["deadline"])
            if urgency["urgent"]:
                urgent_projects.append((pid, pinfo))
            else:
                other_projects.append((pid, pinfo))
        else:
            other_projects.append((pid, pinfo))

    # Projetos urgentes
    if urgent_projects:
        lines.append("\n### 🔴 ATENÇÃO URGENTE")
        for pid, pinfo in urgent_projects:
            lines.extend(format_project_summary(pid, pinfo))
            lines.append("")

    # Outros projetos
    if other_projects:
        lines.append("\n### 📋 Outros Projetos")
        for pid, pinfo in other_projects[:3]:  # Top 3
            lines.extend(format_project_summary(pid, pinfo))
            lines.append("")

    # Tarefas sugeridas
    lines.append("## ✅ Tarefas Sugeridas para Hoje")
    for task in get_today_tasks():
        lines.append(f"- [ ] {task}")

    # Lembretes
    lines.append("\n## 💡 Lembretes")
    lines.append("- Fazer pausas a cada 45-60 minutos")
    lines.append("- Atualizar status no Notion ao finalizar tarefas")
    lines.append("- Commitar e pushar mudanças frequentemente")

    lines.append("\n---")
    lines.append(f"*Gerado às {now.strftime('%H:%M')} por `scripts/daily_standup.py`*")

    return "\n".join(lines)


def generate_weekly_planning() -> str:
    """Gera planejamento semanal."""
    lines = []
    now = datetime.now()

    # Calcular início e fim da semana
    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    lines.append(f"# Planning Semanal")
    lines.append(
        f"**Semana:** {start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m/%Y')}"
    )
    lines.append("")

    # Deadlines na semana
    lines.append("## 📅 Deadlines Esta Semana")
    has_deadlines = False
    for pid, pinfo in TRACKED_PROJECTS.items():
        if "deadline" in pinfo:
            deadline = datetime.strptime(pinfo["deadline"], "%Y-%m-%d")
            if start_of_week <= deadline <= end_of_week:
                has_deadlines = True
                lines.append(f"- **{pinfo['name']}**: {pinfo['deadline']}")

    if not has_deadlines:
        lines.append("- Nenhum deadline esta semana ✅")

    # Foco por dia
    lines.append("\n## 📆 Foco por Dia")
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        day_name = day.strftime("%A")
        focus = WEEKLY_FOCUS.get(i, "")
        emoji = "📌" if i == now.weekday() else ""
        lines.append(f"- **{day_name}** {emoji}: {focus}")

    # Status dos projetos
    lines.append("\n## 📊 Status dos Projetos")
    for pid, pinfo in sorted(TRACKED_PROJECTS.items(), key=lambda x: x[1].get("priority", 99)):
        lines.extend(format_project_summary(pid, pinfo))
        lines.append("")

    # Metas da semana
    lines.append("## 🎯 Metas da Semana")
    lines.append("_Adicione suas metas aqui:_")
    lines.append("- [ ] Meta 1")
    lines.append("- [ ] Meta 2")
    lines.append("- [ ] Meta 3")

    lines.append("\n---")
    lines.append(f"*Gerado em {now.strftime('%d/%m/%Y %H:%M')} por `scripts/daily_standup.py`*")

    return "\n".join(lines)


def generate_focus_mode() -> str:
    """Gera resumo focado apenas em prioridades."""
    lines = []
    now = datetime.now()

    lines.append(f"# 🎯 FOCO - {now.strftime('%d/%m %H:%M')}")
    lines.append("")

    # Apenas projetos urgentes
    for pid, pinfo in sorted(TRACKED_PROJECTS.items(), key=lambda x: x[1].get("priority", 99)):
        if "deadline" in pinfo:
            urgency = calculate_deadline_urgency(pinfo["deadline"])
            if urgency["urgent"]:
                lines.append(f"## {urgency['emoji']} {pinfo['name']}")
                lines.append(f"**{urgency['status']}**: {urgency['days']} dias")
                lines.append("")

    if len(lines) <= 3:
        lines.append("✅ Nenhum projeto urgente no momento.")

    lines.append("\n**Foco de hoje:** " + WEEKLY_FOCUS.get(now.weekday(), "Dia produtivo!"))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Standup diário e planejamento semanal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s              # Standup de hoje
  %(prog)s --week       # Planning semanal
  %(prog)s --focus      # Modo focado
  %(prog)s -o standup.md  # Salvar em arquivo
        """,
    )

    parser.add_argument(
        "--week",
        "-w",
        action="store_true",
        help="Gerar planning semanal",
    )
    parser.add_argument(
        "--focus",
        "-f",
        action="store_true",
        help="Modo focado (apenas urgentes)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Arquivo de saída (default: stdout)",
    )

    args = parser.parse_args()

    if args.week:
        content = generate_weekly_planning()
    elif args.focus:
        content = generate_focus_mode()
    else:
        content = generate_daily_standup()

    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"✅ Salvo em: {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
