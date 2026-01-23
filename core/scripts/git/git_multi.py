#!/usr/bin/env python3
"""
Git Multi-Repo Manager

Gerencia múltiplos repositórios git simultaneamente.
Útil para verificar status, fazer pull/fetch em batch,
e identificar branches desatualizadas.

Uso:
    python core/scripts/git/git_multi.py --status          # Status de todos os repos
    python core/scripts/git/git_multi.py --fetch           # Fetch em todos
    python core/scripts/git/git_multi.py --pull            # Pull em todos
    python core/scripts/git/git_multi.py --stale-branches  # Branches antigas
    python core/scripts/git/git_multi.py --uncommitted     # Repos com mudanças
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent
PROJECTS_BASE = Path.home() / "Projetos"

# Diretórios a escanear por repos
SCAN_DIRS = [
    PROJECTS_BASE / "Projetos" / "Ativos",
    PROJECTS_BASE / "Infraestrutura",
    # Adicione mais diretórios conforme necessário
]

# Repos ignorados
IGNORED_REPOS = [
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
]


def run_git_command(repo_path: Path, *args: str, timeout: int = 30) -> Tuple[bool, str]:
    """
    Executa comando git em um repositório.

    Returns:
        Tuple de (sucesso, output)
    """
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except FileNotFoundError:
        return False, "GIT NOT FOUND"


def find_git_repos(base_dirs: List[Path], max_depth: int = 3) -> List[Path]:
    """Encontra repositórios git nos diretórios base."""
    repos = []

    for base_dir in base_dirs:
        if not base_dir.exists():
            continue

        for path in base_dir.rglob(".git"):
            # Verificar profundidade
            try:
                relative = path.relative_to(base_dir)
                if len(relative.parts) > max_depth:
                    continue
            except ValueError:
                continue

            # Verificar se é diretório .git (não arquivo)
            if not path.is_dir():
                continue

            # Ignorar certos padrões
            repo_path = path.parent
            if any(ignored in str(repo_path) for ignored in IGNORED_REPOS):
                continue

            repos.append(repo_path)

    return sorted(set(repos))


def get_repo_status(repo_path: Path) -> Dict[str, Any]:
    """Obtém status completo de um repositório."""
    status = {
        "path": repo_path,
        "name": repo_path.name,
    }

    # Branch atual
    success, branch = run_git_command(repo_path, "branch", "--show-current")
    status["branch"] = branch if success else "unknown"

    # Status (alterações)
    success, changes = run_git_command(repo_path, "status", "--porcelain")
    if success:
        change_list = [c for c in changes.split("\n") if c]
        status["uncommitted"] = len(change_list)
        status["is_clean"] = len(change_list) == 0
    else:
        status["uncommitted"] = -1
        status["is_clean"] = False

    # Commits não pushados
    success, unpushed = run_git_command(repo_path, "log", "--oneline", "@{u}..HEAD")
    if success:
        unpushed_list = [c for c in unpushed.split("\n") if c]
        status["unpushed"] = len(unpushed_list)
    else:
        status["unpushed"] = 0  # Pode não ter upstream

    # Último commit
    success, last_commit = run_git_command(repo_path, "log", "-1", "--format=%h %s (%ar)")
    status["last_commit"] = last_commit if success else "N/A"

    # Data do último commit
    success, commit_date = run_git_command(repo_path, "log", "-1", "--format=%ci")
    if success:
        try:
            status["last_commit_date"] = datetime.fromisoformat(commit_date.split()[0])
        except (ValueError, IndexError):
            status["last_commit_date"] = None
    else:
        status["last_commit_date"] = None

    return status


def get_branch_info(repo_path: Path) -> List[Dict[str, Any]]:
    """Obtém informações sobre branches."""
    branches = []

    # Listar branches locais
    success, output = run_git_command(repo_path, "branch", "-v", "--no-abbrev")
    if not success:
        return branches

    for line in output.split("\n"):
        if not line.strip():
            continue

        is_current = line.startswith("*")
        line = line.lstrip("* ")
        parts = line.split()

        if len(parts) >= 2:
            branch_name = parts[0]
            commit_hash = parts[1]

            # Data do último commit na branch
            success, commit_date = run_git_command(
                repo_path, "log", "-1", "--format=%ci", branch_name
            )
            if success:
                try:
                    date = datetime.fromisoformat(commit_date.split()[0])
                    days_old = (datetime.now() - date).days
                except (ValueError, IndexError):
                    date = None
                    days_old = -1
            else:
                date = None
                days_old = -1

            branches.append(
                {
                    "name": branch_name,
                    "commit": commit_hash[:8],
                    "is_current": is_current,
                    "last_commit_date": date,
                    "days_old": days_old,
                }
            )

    return branches


def cmd_status(repos: List[Path], args: argparse.Namespace) -> None:
    """Mostra status de todos os repositórios."""
    print(f"\n{'='*70}")
    print(f"STATUS DE {len(repos)} REPOSITÓRIOS")
    print(f"{'='*70}\n")

    clean_repos = []
    dirty_repos = []

    for repo_path in repos:
        status = get_repo_status(repo_path)

        if status["is_clean"] and status["unpushed"] == 0:
            clean_repos.append(status)
        else:
            dirty_repos.append(status)

    # Mostrar repos com mudanças primeiro
    if dirty_repos:
        print("## 🔄 Repositórios com alterações\n")
        for status in dirty_repos:
            emoji = "🔴" if status["uncommitted"] > 5 else "🟠"
            print(f"{emoji} **{status['name']}** ({status['branch']})")
            if status["uncommitted"] > 0:
                print(f"   ⚠️ {status['uncommitted']} alterações não commitadas")
            if status["unpushed"] > 0:
                print(f"   ⚠️ {status['unpushed']} commits não pushados")
            print(f"   📍 {status['path']}")
            print()

    # Repos limpos
    if clean_repos and not args.dirty_only:
        print("## ✅ Repositórios limpos\n")
        for status in clean_repos:
            print(f"✅ {status['name']} ({status['branch']}) - {status['last_commit']}")

    # Sumário
    print(f"\n{'='*70}")
    print(f"SUMÁRIO: {len(clean_repos)} limpos, {len(dirty_repos)} com alterações")
    print(f"{'='*70}")


def cmd_fetch(repos: List[Path], args: argparse.Namespace) -> None:
    """Executa fetch em todos os repositórios."""
    print(f"\n{'='*70}")
    print(f"FETCH EM {len(repos)} REPOSITÓRIOS")
    print(f"{'='*70}\n")

    for repo_path in repos:
        print(f"⏳ Fetching {repo_path.name}...", end=" ", flush=True)
        success, output = run_git_command(repo_path, "fetch", "--all", "--prune")
        if success:
            print("✅")
        else:
            print(f"❌ {output}")


def cmd_pull(repos: List[Path], args: argparse.Namespace) -> None:
    """Executa pull em todos os repositórios."""
    print(f"\n{'='*70}")
    print(f"PULL EM {len(repos)} REPOSITÓRIOS")
    print(f"{'='*70}\n")

    for repo_path in repos:
        status = get_repo_status(repo_path)

        # Só fazer pull em repos limpos
        if not status["is_clean"]:
            print(f"⏭️ Skipping {repo_path.name} (tem alterações não commitadas)")
            continue

        print(f"⏳ Pulling {repo_path.name}...", end=" ", flush=True)
        success, output = run_git_command(repo_path, "pull", "--ff-only")
        if success:
            if "Already up to date" in output:
                print("✅ Já atualizado")
            else:
                print("✅ Atualizado")
        else:
            print(f"❌ {output[:50]}...")


def cmd_stale_branches(repos: List[Path], args: argparse.Namespace) -> None:
    """Lista branches antigas/esquecidas."""
    stale_days = args.stale_days or 30

    print(f"\n{'='*70}")
    print(f"BRANCHES > {stale_days} DIAS SEM ATIVIDADE")
    print(f"{'='*70}\n")

    total_stale = 0

    for repo_path in repos:
        branches = get_branch_info(repo_path)
        stale = [b for b in branches if b["days_old"] > stale_days and not b["is_current"]]

        if stale:
            print(f"## {repo_path.name}")
            for branch in sorted(stale, key=lambda x: -x["days_old"]):
                age_emoji = "🔴" if branch["days_old"] > 90 else "🟠"
                print(f"  {age_emoji} {branch['name']}: {branch['days_old']} dias")
            print()
            total_stale += len(stale)

    if total_stale == 0:
        print("✅ Nenhuma branch antiga encontrada!")
    else:
        print(f"\n{'='*70}")
        print(f"TOTAL: {total_stale} branches antigas")
        print(f"{'='*70}")


def cmd_uncommitted(repos: List[Path], args: argparse.Namespace) -> None:
    """Lista apenas repos com mudanças não commitadas."""
    print(f"\n{'='*70}")
    print("REPOSITÓRIOS COM MUDANÇAS NÃO COMMITADAS")
    print(f"{'='*70}\n")

    dirty = []
    for repo_path in repos:
        status = get_repo_status(repo_path)
        if not status["is_clean"]:
            dirty.append(status)

    if not dirty:
        print("✅ Todos os repositórios estão limpos!")
        return

    for status in dirty:
        print(f"🔴 {status['name']}")
        print(f"   Branch: {status['branch']}")
        print(f"   Alterações: {status['uncommitted']}")
        print(f"   Path: {status['path']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Gerenciador de múltiplos repositórios git",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s --status           # Status de todos
  %(prog)s --status --dirty-only  # Apenas com mudanças
  %(prog)s --fetch            # Fetch em todos
  %(prog)s --pull             # Pull em repos limpos
  %(prog)s --stale-branches   # Branches antigas
  %(prog)s --uncommitted      # Repos com mudanças
        """,
    )

    # Ações
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--status", action="store_true", help="Mostrar status de todos os repos")
    action.add_argument("--fetch", action="store_true", help="Fetch em todos os repos")
    action.add_argument("--pull", action="store_true", help="Pull em repos limpos")
    action.add_argument(
        "--stale-branches", action="store_true", help="Listar branches antigas"
    )
    action.add_argument(
        "--uncommitted", action="store_true", help="Listar repos com mudanças"
    )

    # Opções
    parser.add_argument(
        "--dirty-only",
        action="store_true",
        help="Mostrar apenas repos com alterações (para --status)",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="Dias para considerar branch antiga (default: 30)",
    )
    parser.add_argument(
        "--add-dir",
        action="append",
        help="Adicionar diretório para escanear",
    )

    args = parser.parse_args()

    # Construir lista de diretórios
    scan_dirs = list(SCAN_DIRS)
    if args.add_dir:
        scan_dirs.extend(Path(d) for d in args.add_dir)

    # Encontrar repos
    repos = find_git_repos(scan_dirs)

    if not repos:
        print("Nenhum repositório git encontrado.")
        sys.exit(1)

    # Executar ação
    if args.status:
        cmd_status(repos, args)
    elif args.fetch:
        cmd_fetch(repos, args)
    elif args.pull:
        cmd_pull(repos, args)
    elif args.stale_branches:
        cmd_stale_branches(repos, args)
    elif args.uncommitted:
        cmd_uncommitted(repos, args)


if __name__ == "__main__":
    main()
