#!/usr/bin/env python3
"""
Cleanup Script for Cursor Multiagent System

Limpa arquivos temporários antigos seguindo política de retenção:
- Logs > 30 dias: deletar
- @temp/* concluídos: deletar
- Arquivos RESUMO_*, RELATORIO_*, ANALISE_*: mover para logs/ ou deletar

Uso:
    python core/scripts/workflow/cleanup_temp.py           # Dry run (mostra o que seria feito)
    python core/scripts/workflow/cleanup_temp.py --execute # Executa limpeza
    python core/scripts/workflow/cleanup_temp.py --help    # Ajuda
"""

import argparse
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

# Configuração
PROJECT_ROOT = Path(__file__).parent.parent
TEMP_DIR = PROJECT_ROOT / "@temp"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"

# Política de retenção (dias)
RETENTION_DAYS = {
    "logs": 30,
    "temp": 7,
    "analysis": 30,
}

# Padrões de arquivos temporários
TEMP_PATTERNS = [
    "RESUMO_*.md",
    "RELATORIO_*.md",
    "ANALISE_*.md",
    "STATUS_*.md",
    "PLANO_*.md",
    "CONTEXTO_RESPOSTA*.md",
]


def get_file_age_days(file_path: Path) -> int:
    """Retorna idade do arquivo em dias."""
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    return (datetime.now() - mtime).days


def find_old_logs(max_age_days: int = 30) -> List[Path]:
    """Encontra logs mais velhos que max_age_days."""
    old_files = []
    if LOGS_DIR.exists():
        for file in LOGS_DIR.rglob("*.md"):
            if get_file_age_days(file) > max_age_days:
                old_files.append(file)
    return old_files


def find_old_temp_files(max_age_days: int = 7) -> List[Path]:
    """Encontra arquivos em @temp mais velhos que max_age_days."""
    old_files = []
    if TEMP_DIR.exists():
        for file in TEMP_DIR.rglob("*"):
            if file.is_file() and get_file_age_days(file) > max_age_days:
                old_files.append(file)
    return old_files


def find_misplaced_temp_files() -> List[Tuple[Path, str]]:
    """
    Encontra arquivos temporários em locais errados.
    Retorna lista de (arquivo, local_sugerido).
    """
    misplaced = []

    # Procurar em todo o projeto
    for pattern in TEMP_PATTERNS:
        for file in PROJECT_ROOT.rglob(pattern):
            # Ignorar se já está em @temp ou logs
            if "@temp" in str(file) or "logs" in str(file):
                continue

            # Sugerir local correto
            if "RESUMO" in file.name or "RELATORIO" in file.name:
                suggested = LOGS_DIR / "system" / file.name
            elif "ANALISE" in file.name:
                suggested = LOGS_DIR / "analysis" / file.name
            else:
                suggested = TEMP_DIR / "misc" / file.name

            misplaced.append((file, str(suggested)))

    return misplaced


def find_empty_dirs() -> List[Path]:
    """Encontra diretórios vazios em @temp e logs."""
    empty_dirs = []

    for base_dir in [TEMP_DIR, LOGS_DIR]:
        if base_dir.exists():
            for dir_path in sorted(base_dir.rglob("*"), reverse=True):
                if dir_path.is_dir() and not any(dir_path.iterdir()):
                    empty_dirs.append(dir_path)

    return empty_dirs


def calculate_size(files: List[Path]) -> str:
    """Calcula tamanho total dos arquivos."""
    total_bytes = sum(f.stat().st_size for f in files if f.exists())

    if total_bytes < 1024:
        return f"{total_bytes} B"
    elif total_bytes < 1024 * 1024:
        return f"{total_bytes / 1024:.1f} KB"
    else:
        return f"{total_bytes / (1024 * 1024):.1f} MB"


def cleanup_report(
    old_logs: List[Path],
    old_temp: List[Path],
    misplaced: List[Tuple[Path, str]],
    empty_dirs: List[Path],
) -> str:
    """Gera relatório de limpeza."""
    report = []
    report.append("=" * 60)
    report.append("CLEANUP REPORT - Cursor Multiagent System")
    report.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    report.append("")

    # Logs antigos
    report.append(f"## Logs antigos (> {RETENTION_DAYS['logs']} dias)")
    report.append(f"   Arquivos: {len(old_logs)}")
    report.append(f"   Tamanho: {calculate_size(old_logs)}")
    if old_logs:
        for f in old_logs[:5]:
            report.append(f"   - {f.relative_to(PROJECT_ROOT)}")
        if len(old_logs) > 5:
            report.append(f"   ... e mais {len(old_logs) - 5} arquivos")
    report.append("")

    # Temp antigos
    report.append(f"## Arquivos temp antigos (> {RETENTION_DAYS['temp']} dias)")
    report.append(f"   Arquivos: {len(old_temp)}")
    report.append(f"   Tamanho: {calculate_size(old_temp)}")
    if old_temp:
        for f in old_temp[:5]:
            report.append(f"   - {f.relative_to(PROJECT_ROOT)}")
        if len(old_temp) > 5:
            report.append(f"   ... e mais {len(old_temp) - 5} arquivos")
    report.append("")

    # Arquivos mal posicionados
    report.append("## Arquivos temporários em locais errados")
    report.append(f"   Arquivos: {len(misplaced)}")
    if misplaced:
        for f, suggested in misplaced[:5]:
            report.append(f"   - {f.relative_to(PROJECT_ROOT)}")
            report.append(f"     → Sugerido: {suggested}")
        if len(misplaced) > 5:
            report.append(f"   ... e mais {len(misplaced) - 5} arquivos")
    report.append("")

    # Diretórios vazios
    report.append("## Diretórios vazios")
    report.append(f"   Diretórios: {len(empty_dirs)}")
    if empty_dirs:
        for d in empty_dirs[:5]:
            report.append(f"   - {d.relative_to(PROJECT_ROOT)}")
        if len(empty_dirs) > 5:
            report.append(f"   ... e mais {len(empty_dirs) - 5} diretórios")
    report.append("")

    # Sumário
    total_files = len(old_logs) + len(old_temp) + len(misplaced)
    report.append("=" * 60)
    report.append(f"TOTAL: {total_files} arquivos, {len(empty_dirs)} diretórios")
    report.append("=" * 60)

    return "\n".join(report)


def execute_cleanup(
    old_logs: List[Path],
    old_temp: List[Path],
    misplaced: List[Tuple[Path, str]],
    empty_dirs: List[Path],
    dry_run: bool = True,
) -> None:
    """Executa a limpeza."""
    if dry_run:
        print("\n[DRY RUN] Nenhuma alteração será feita.\n")
        print("Use --execute para executar a limpeza.\n")
        return

    print("\n[EXECUTANDO LIMPEZA]\n")

    # Deletar logs antigos
    for f in old_logs:
        try:
            f.unlink()
            print(f"✓ Deletado: {f.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            print(f"✗ Erro ao deletar {f}: {e}")

    # Deletar temp antigos
    for f in old_temp:
        try:
            f.unlink()
            print(f"✓ Deletado: {f.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            print(f"✗ Erro ao deletar {f}: {e}")

    # Mover arquivos mal posicionados
    for f, suggested in misplaced:
        try:
            suggested_path = Path(suggested)
            suggested_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(suggested_path))
            print(f"✓ Movido: {f.name} → {suggested_path.parent.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            print(f"✗ Erro ao mover {f}: {e}")

    # Deletar diretórios vazios
    for d in empty_dirs:
        try:
            d.rmdir()
            print(f"✓ Removido dir vazio: {d.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            print(f"✗ Erro ao remover {d}: {e}")

    print("\n[LIMPEZA CONCLUÍDA]")


def main():
    parser = argparse.ArgumentParser(
        description="Limpa arquivos temporários do Cursor Multiagent System"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Executa a limpeza (default: dry run)",
    )
    parser.add_argument(
        "--logs-days",
        type=int,
        default=RETENTION_DAYS["logs"],
        help=f"Dias de retenção para logs (default: {RETENTION_DAYS['logs']})",
    )
    parser.add_argument(
        "--temp-days",
        type=int,
        default=RETENTION_DAYS["temp"],
        help=f"Dias de retenção para temp (default: {RETENTION_DAYS['temp']})",
    )

    args = parser.parse_args()

    # Encontrar arquivos
    old_logs = find_old_logs(args.logs_days)
    old_temp = find_old_temp_files(args.temp_days)
    misplaced = find_misplaced_temp_files()
    empty_dirs = find_empty_dirs()

    # Gerar e mostrar relatório
    report = cleanup_report(old_logs, old_temp, misplaced, empty_dirs)
    print(report)

    # Executar limpeza
    execute_cleanup(
        old_logs,
        old_temp,
        misplaced,
        empty_dirs,
        dry_run=not args.execute,
    )


if __name__ == "__main__":
    main()
