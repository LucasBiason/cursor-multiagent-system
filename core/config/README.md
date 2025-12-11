# Configuration Files

This directory contains environment variable templates, configuration examples, and helper scripts.

## Files

### `.env.example`
Complete template with ALL environment variables needed by agents and scripts.

**Contains:**
- Notion API tokens
- Hostinger server credentials (all 3 projects: ExpenseIQ, KPI, Portfolio)
- Render.com API keys and service IDs
- GitHub tokens and repository URLs
- FIAP portal credentials
- Database connections (commented templates)
- SMTP settings
- JWT secrets
- Application URLs
- Timezone settings

**Location:** `core/config/.env.example`  
**Usage:** Copy to `.env.passwords` and fill with actual values

### `load_env_example.py`
Example script demonstrating how to load environment variables in Python scripts.

**Features:**
- Checks multiple locations for `.env.passwords`
- Helper functions for common credentials (Hostinger, Render, Notion, GitHub, FIAP)
- Proper error handling and path resolution

**Usage:**
```python
from core.config.load_env_example import load_env_passwords, get_hostinger_credentials

load_env_passwords()
creds = get_hostinger_credentials("expenseiq")
```

### `config.template.json`
Template JSON configuration file for the multiagent system.

**Contains:**
- System version and settings
- Agent definitions and capabilities
- Notion configuration
- Environment variable references
- Logging configuration
- Validation rules

**Note:** This is a template. Actual configuration should be stored in private config.

## Usage

### 1. Setup Environment Variables

```bash
# Copy the example file
cp .env.example .env.passwords

# Edit with actual values
nano .env.passwords  # or use your preferred editor
```

### 2. Load in Python Scripts

**Method 1: Using python-dotenv directly**
```python
from dotenv import load_dotenv
import os
from pathlib import Path

# Load from core/config/.env.passwords
project_root = Path(__file__).parent.parent.parent
env_path = project_root / "core" / "config" / ".env.passwords"

if env_path.exists():
    load_dotenv(env_path, override=True)
else:
    # Fallback to project root
    load_dotenv(project_root / ".env.passwords")

# Use variables
password = os.getenv('HOSTINGER_EXPENSEIQ_PASSWORD')
```

**Method 2: Using the helper script**
```python
from core.config.load_env_example import (
    load_env_passwords,
    get_hostinger_credentials,
    get_render_credentials,
    get_notion_credentials
)

# Load environment
load_env_passwords()

# Get credentials
expenseiq = get_hostinger_credentials("expenseiq")
render = get_render_credentials()
notion = get_notion_credentials()
```

### 3. Reference Variable Names

Always check `core/config/.env.example` for the correct variable names:
- Don't hardcode variable names
- Use the exact names from `.env.example`
- Follow the naming conventions

## Variable Naming Convention

### Hostinger
Format: `HOSTINGER_{PROJECT}_{TYPE}`

Examples:
- `HOSTINGER_EXPENSEIQ_PASSWORD`
- `HOSTINGER_KPI_IP`
- `HOSTINGER_PORTFOLIO_SSH_HOST`

Projects: `EXPENSEIQ`, `KPI`, `PORTFOLIO`

### Render
Format: `RENDER_{SERVICE}_{TYPE}`

Examples:
- `RENDER_API_KEY`
- `RENDER_PGHERO_SERVICE_ID`
- `RENDER_PGHERO_USERNAME`

### GitHub
Format: `GITHUB_{TYPE}`

Examples:
- `GITHUB_TOKEN`
- `GITHUB_USERNAME`
- `GITHUB_EXPENSEIQ_REPO`

### Database
Format: `{PROJECT}_DB_{TYPE}`

Examples:
- `EXPENSEIQ_DB_PASSWORD`
- `KPI_DB_HOST`
- `PORTFOLIO_DB_NAME`

### Notion
- `NOTION_TOKEN` (not `NOTION_API_KEY`)
- `NOTION_API_VERSION`

## Security

### ✅ Best Practices
- `.env.passwords` is gitignored (never commit!)
- Always use environment variables in scripts
- Never hardcode passwords or tokens
- Reference `.env.example` for variable names
- Use `load_dotenv()` with proper path resolution
- Check file existence before loading

### ❌ Never Do
- Commit `.env.passwords` to git
- Hardcode credentials in scripts
- Share `.env.passwords` in public repositories
- Use different variable names than in `.env.example`
- Store credentials in code comments

## File Locations

### Primary Location
- **Example:** `core/config/.env.example`
- **Actual:** `core/config/.env.passwords` (gitignored)

### Fallback Locations
Scripts should check these locations in order:
1. `core/config/.env.passwords` (preferred)
2. Project root `.env.passwords`
3. Current directory `.env.passwords`

## Agent Integration

All agents should:
1. Reference `core/config/.env.example` for variable names
2. Use `python-dotenv` to load from `.env.passwords`
3. Check multiple locations (core/config, project root, current dir)
4. Never hardcode credentials
5. Use helper functions from `load_env_example.py` when possible

**See agent files for specific integration:**
- `core/agents/cicd-agent.mdc` - Deployment credentials
- `core/agents/work-assistant.mdc` - Work project credentials
- `core/agents/personal-assistant.mdc` - Notion and general credentials
- `core/agents/studies-assistant.mdc` - FIAP and study credentials

## Troubleshooting

### Variable Not Found
1. Check if `.env.passwords` exists in expected location
2. Verify variable name matches `.env.example` exactly
3. Ensure `load_dotenv()` was called before using `os.getenv()`
4. Check if file has correct permissions

### Wrong Values
1. Verify `.env.passwords` has actual values (not `YOUR_*_HERE`)
2. Check for typos in variable names
3. Ensure no extra spaces around `=` sign
4. Verify file encoding (should be UTF-8)

### Script Can't Find File
1. Use absolute paths or proper relative path resolution
2. Check current working directory
3. Use `Path(__file__).parent` for relative paths
4. See `load_env_example.py` for proper path resolution

---

**Last Updated:** 2025-12-08  
**Version:** 1.2.0
