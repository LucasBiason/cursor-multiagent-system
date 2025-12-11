# model context protocol (mcp) - padrões e boas práticas

**última atualização:** 2025-12-08  
**aplicável a:** todos os mcp servers

---

## estrutura de mcp server

### organização

```
mcp-server/
├── src/
│   ├── server.py              # ponto de entrada
│   ├── tools/                 # definições de tools
│   │   ├── __init__.py
│   │   └── notion_tools.py
│   ├── services/              # serviços (notion, etc.)
│   │   └── notion_service.py
│   ├── custom/                # implementações customizadas
│   │   └── personal_notion.py
│   ├── utils/                 # utilitários
│   │   ├── validators.py
│   │   └── formatters.py
│   └── exceptions/            # exceções customizadas
│       └── notion_service.py
├── tests/                     # testes
└── README.md
```

---

## definição de tools

### estrutura de tool

```python
from mcp.types import Tool

TOOLS = [
    Tool(
        name="create_notion_page",
        description="Create a new page in Notion database",
        inputSchema={
            "type": "object",
            "properties": {
                "database_id": {
                    "type": "string",
                    "description": "Notion database ID"
                },
                "properties": {
                    "type": "object",
                    "description": "Page properties"
                }
            },
            "required": ["database_id", "properties"]
        }
    )
]
```

### implementação de tool handler

```python
async def handle_create_notion_page(
    database_id: str,
    properties: dict
) -> dict:
    """Handle create_notion_page tool call.
    
    Args:
        database_id: Notion database ID
        properties: Page properties
        
    Returns:
        Created page information
        
    Raises:
        NotionAPIError: If API call fails
    """
    try:
        service = NotionService()
        page = service.create_page(
            database_id=database_id,
            properties=properties
        )
        return {
            "success": True,
            "page_id": page["id"],
            "url": page["url"]
        }
    except Exception as e:
        raise NotionAPIError(f"Failed to create page: {e}")
```

---

## error handling

### exceções customizadas

```python
class NotionAPIError(Exception):
    """Raised when Notion API call fails."""
    pass

class ValidationError(Exception):
    """Raised when validation fails."""
    pass
```

### tratamento de erros

```python
async def handle_tool_call(tool_name: str, arguments: dict) -> dict:
    """Handle tool call with error handling."""
    try:
        if tool_name == "create_notion_page":
            return await handle_create_notion_page(**arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    except ValidationError as e:
        return {
            "success": False,
            "error": f"Validation error: {e}"
        }
    except NotionAPIError as e:
        return {
            "success": False,
            "error": f"Notion API error: {e}"
        }
    except Exception as e:
        logger.error(f"Unexpected error in {tool_name}: {e}")
        return {
            "success": False,
            "error": "Internal server error"
        }
```

---

## best practices

### validação de entrada

```python
def validate_database_id(database_id: str) -> bool:
    """Validate Notion database ID format."""
    import re
    pattern = r'^[a-f0-9]{32}$'
    return bool(re.match(pattern, database_id.replace('-', '')))
```

### formatação de dados

```python
def format_date_gmt3(dt: datetime) -> str:
    """Format datetime to GMT-3 ISO format.
    
    Args:
        dt: Datetime object
        
    Returns:
        ISO format string with GMT-3 timezone
    """
    tz = timezone(timedelta(hours=-3))
    dt_aware = dt.replace(tzinfo=tz) if dt.tzinfo is None else dt.astimezone(tz)
    return dt_aware.isoformat()
```

### logging

```python
import logging

logger = logging.getLogger(__name__)

async def handle_tool_call(tool_name: str, arguments: dict) -> dict:
    logger.info(f"Tool call: {tool_name} with args: {arguments}")
    # ... implementation
    logger.info(f"Tool call successful: {tool_name}")
```

---

## referências

- notion mcp → `my-local-place/services/external/notion-automation-suite`
- mcp documentation → https://modelcontextprotocol.io

---

**estas regras são obrigatórias para todos os mcp servers.**

