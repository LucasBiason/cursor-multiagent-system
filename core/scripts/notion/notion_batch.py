#!/usr/bin/env python3
"""
Notion Batch Operations Script

Realiza operações em lote no Notion usando a API diretamente ou via MCP.
Útil para:
- Atualizar status de múltiplos cards
- Arquivar cards antigos
- Reorganizar hierarquias
- Mover cards entre databases

Uso:
    python core/scripts/notion/notion_batch.py --action list --database studies
    python core/scripts/notion/notion_batch.py --action update-status --database studies --status "Concluído" --filter "tag:hackathon"
    python core/scripts/notion/notion_batch.py --action archive --database personal --older-than 90
    python core/scripts/notion/notion_batch.py --action stats --database all
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    print("requests não encontrado. Instale com: pip install requests")
    sys.exit(1)

# Carregar variáveis de ambiente
try:
    from dotenv import load_dotenv

    PROJECT_ROOT = Path(__file__).parent.parent
    env_paths = [
        PROJECT_ROOT / "config" / "system" / "infrastructure" / ".env",
        PROJECT_ROOT / "config" / ".env",
        PROJECT_ROOT / ".env",
    ]

    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path, override=True)
            break
except ImportError:
    pass


class NotionBatch:
    """Cliente para operações batch no Notion."""

    BASE_URL = "https://api.notion.com/v1"
    NOTION_VERSION = "2022-06-28"

    def __init__(self, token: Optional[str] = None):
        """
        Inicializa o cliente Notion.

        Args:
            token: Notion API token. Se não fornecido, usa NOTION_API_KEY do ambiente.
        """
        self.token = token or os.getenv("NOTION_API_KEY") or os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError(
                "Notion API token não encontrado. "
                "Configure NOTION_API_KEY ou NOTION_TOKEN no ambiente."
            )

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": self.NOTION_VERSION,
        }

        # Carregar IDs das databases
        self.database_ids = self._load_database_ids()

    def _load_database_ids(self) -> Dict[str, str]:
        """Carrega IDs das databases do arquivo de configuração."""
        # Database IDs are now in the MCP project, not here
        # This script should use the MCP instead of direct IDs
        config_paths = [
            # Legacy paths (deprecated - use MCP instead)
            Path(__file__).parent.parent / "config" / "notion-ids.json",
        ]

        for path in config_paths:
            if path.exists():
                with open(path) as f:
                    data = json.load(f)
                    return data.get("databases", {})

        return {}

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Faz uma requisição à API do Notion."""
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            elif method == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data, timeout=30)
            else:
                raise ValueError(f"Método não suportado: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Resposta: {e.response.text}")
            return {}

    def get_database_id(self, name: str) -> Optional[str]:
        """Obtém o ID de uma database pelo nome."""
        return self.database_ids.get(name.lower())

    def query_database(
        self,
        database_id: str,
        filter_obj: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        page_size: int = 100,
    ) -> List[Dict]:
        """
        Consulta uma database do Notion.

        Args:
            database_id: ID da database
            filter_obj: Filtro Notion
            sorts: Ordenação
            page_size: Tamanho da página

        Returns:
            Lista de páginas/cards
        """
        data = {"page_size": page_size}
        if filter_obj:
            data["filter"] = filter_obj
        if sorts:
            data["sorts"] = sorts

        all_results = []
        has_more = True
        start_cursor = None

        while has_more:
            if start_cursor:
                data["start_cursor"] = start_cursor

            response = self._request("POST", f"databases/{database_id}/query", data)

            if not response:
                break

            all_results.extend(response.get("results", []))
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")

        return all_results

    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """
        Atualiza propriedades de uma página.

        Args:
            page_id: ID da página
            properties: Propriedades a atualizar

        Returns:
            Página atualizada
        """
        return self._request("PATCH", f"pages/{page_id}", {"properties": properties})

    def archive_page(self, page_id: str) -> Dict:
        """
        Arquiva uma página.

        Args:
            page_id: ID da página

        Returns:
            Página arquivada
        """
        return self._request("PATCH", f"pages/{page_id}", {"archived": True})

    def get_page_title(self, page: Dict) -> str:
        """Extrai o título de uma página."""
        properties = page.get("properties", {})

        # Procurar propriedade de título
        for prop in properties.values():
            if prop.get("type") == "title":
                title_content = prop.get("title", [])
                if title_content:
                    return title_content[0].get("plain_text", "Sem título")

        return "Sem título"

    def get_page_status(self, page: Dict) -> Optional[str]:
        """Extrai o status de uma página."""
        properties = page.get("properties", {})

        for prop in properties.values():
            if prop.get("type") == "status":
                status = prop.get("status")
                if status:
                    return status.get("name")
            elif prop.get("type") == "select":
                select = prop.get("select")
                if select:
                    return select.get("name")

        return None

    def get_page_date(self, page: Dict, date_prop: str = "created_time") -> Optional[datetime]:
        """Extrai uma data de uma página."""
        if date_prop == "created_time":
            date_str = page.get("created_time")
        elif date_prop == "last_edited_time":
            date_str = page.get("last_edited_time")
        else:
            properties = page.get("properties", {})
            date_obj = properties.get(date_prop, {})
            if date_obj.get("type") == "date" and date_obj.get("date"):
                date_str = date_obj["date"].get("start")
            else:
                return None

        if date_str:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return None


def cmd_list(notion: NotionBatch, args: argparse.Namespace) -> None:
    """Lista cards de uma database."""
    db_id = notion.get_database_id(args.database)
    if not db_id:
        print(f"Database '{args.database}' não encontrada.")
        print(f"Databases disponíveis: {list(notion.database_ids.keys())}")
        return

    pages = notion.query_database(db_id)

    print(f"\n{'='*60}")
    print(f"Database: {args.database.upper()}")
    print(f"Total: {len(pages)} cards")
    print(f"{'='*60}\n")

    for page in pages[:args.limit]:
        title = notion.get_page_title(page)
        status = notion.get_page_status(page) or "N/A"
        created = notion.get_page_date(page, "created_time")
        created_str = created.strftime("%Y-%m-%d") if created else "N/A"

        print(f"- [{status}] {title} (criado: {created_str})")


def cmd_stats(notion: NotionBatch, args: argparse.Namespace) -> None:
    """Mostra estatísticas das databases."""
    databases = [args.database] if args.database != "all" else list(notion.database_ids.keys())

    print(f"\n{'='*60}")
    print("ESTATÍSTICAS DO NOTION")
    print(f"{'='*60}\n")

    total_cards = 0

    for db_name in databases:
        db_id = notion.get_database_id(db_name)
        if not db_id:
            continue

        pages = notion.query_database(db_id)
        total_cards += len(pages)

        # Contar por status
        status_count: Dict[str, int] = {}
        for page in pages:
            status = notion.get_page_status(page) or "Sem status"
            status_count[status] = status_count.get(status, 0) + 1

        print(f"📊 {db_name.upper()}: {len(pages)} cards")
        for status, count in sorted(status_count.items(), key=lambda x: -x[1]):
            print(f"   - {status}: {count}")
        print()

    print(f"{'='*60}")
    print(f"TOTAL GERAL: {total_cards} cards")
    print(f"{'='*60}")


def cmd_archive(notion: NotionBatch, args: argparse.Namespace) -> None:
    """Arquiva cards antigos."""
    db_id = notion.get_database_id(args.database)
    if not db_id:
        print(f"Database '{args.database}' não encontrada.")
        return

    cutoff_date = datetime.now() - timedelta(days=args.older_than)
    pages = notion.query_database(db_id)

    to_archive = []
    for page in pages:
        last_edited = notion.get_page_date(page, "last_edited_time")
        if last_edited and last_edited.replace(tzinfo=None) < cutoff_date:
            to_archive.append(page)

    print(f"\n{'='*60}")
    print(f"ARQUIVAR CARDS > {args.older_than} dias")
    print(f"Database: {args.database}")
    print(f"Cards a arquivar: {len(to_archive)}")
    print(f"{'='*60}\n")

    if not to_archive:
        print("Nenhum card para arquivar.")
        return

    for page in to_archive[:10]:  # Mostrar primeiros 10
        title = notion.get_page_title(page)
        last_edited = notion.get_page_date(page, "last_edited_time")
        last_edited_str = last_edited.strftime("%Y-%m-%d") if last_edited else "N/A"
        print(f"- {title} (última edição: {last_edited_str})")

    if len(to_archive) > 10:
        print(f"... e mais {len(to_archive) - 10} cards")

    if args.dry_run:
        print("\n[DRY RUN] Nenhuma alteração feita.")
        return

    print("\nArquivando...")
    archived = 0
    for page in to_archive:
        result = notion.archive_page(page["id"])
        if result:
            archived += 1
            print(f"✓ Arquivado: {notion.get_page_title(page)}")

    print(f"\n✅ {archived} cards arquivados.")


def cmd_update_status(notion: NotionBatch, args: argparse.Namespace) -> None:
    """Atualiza status de cards."""
    db_id = notion.get_database_id(args.database)
    if not db_id:
        print(f"Database '{args.database}' não encontrada.")
        return

    pages = notion.query_database(db_id)

    # Filtrar se especificado
    if args.filter:
        key, value = args.filter.split(":", 1) if ":" in args.filter else ("title", args.filter)
        filtered = []
        for page in pages:
            if key == "title":
                title = notion.get_page_title(page)
                if value.lower() in title.lower():
                    filtered.append(page)
            elif key == "status":
                status = notion.get_page_status(page)
                if status and value.lower() in status.lower():
                    filtered.append(page)
        pages = filtered

    print(f"\n{'='*60}")
    print(f"ATUALIZAR STATUS para: {args.status}")
    print(f"Database: {args.database}")
    print(f"Cards afetados: {len(pages)}")
    print(f"{'='*60}\n")

    if not pages:
        print("Nenhum card encontrado com o filtro especificado.")
        return

    for page in pages[:10]:
        title = notion.get_page_title(page)
        current_status = notion.get_page_status(page) or "N/A"
        print(f"- {title} ({current_status} → {args.status})")

    if len(pages) > 10:
        print(f"... e mais {len(pages) - 10} cards")

    if args.dry_run:
        print("\n[DRY RUN] Nenhuma alteração feita.")
        return

    # A atualização real dependeria de saber o nome da propriedade de status
    print("\n⚠️  Para atualizar status, configure a propriedade correta na database.")


def main():
    parser = argparse.ArgumentParser(
        description="Operações batch no Notion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s --action list --database studies
  %(prog)s --action stats --database all
  %(prog)s --action archive --database personal --older-than 90 --dry-run
  %(prog)s --action update-status --database work --status "Concluído" --filter "tag:hackathon"
        """,
    )

    parser.add_argument(
        "--action",
        required=True,
        choices=["list", "stats", "archive", "update-status"],
        help="Ação a executar",
    )
    parser.add_argument(
        "--database",
        default="all",
        help="Nome da database (studies, work, personal, all)",
    )
    parser.add_argument(
        "--status",
        help="Novo status (para update-status)",
    )
    parser.add_argument(
        "--filter",
        help="Filtro (key:value, ex: tag:hackathon, status:pendente)",
    )
    parser.add_argument(
        "--older-than",
        type=int,
        default=90,
        help="Dias para considerar antigo (para archive)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Limite de resultados a mostrar",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simular sem fazer alterações",
    )

    args = parser.parse_args()

    try:
        notion = NotionBatch()
    except ValueError as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

    actions = {
        "list": cmd_list,
        "stats": cmd_stats,
        "archive": cmd_archive,
        "update-status": cmd_update_status,
    }

    action_func = actions.get(args.action)
    if action_func:
        action_func(notion, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
