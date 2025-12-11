#!/usr/bin/env python3
"""
Example script showing how to load environment variables from .env.passwords

This demonstrates the pattern all agents should use when creating scripts
that need credentials, IPs, passwords, or tokens.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_env_passwords():
    """
    Load environment variables from .env.passwords
    
    Checks multiple locations:
    1. core/config/.env.passwords (preferred)
    2. Project root .env.passwords
    3. Current directory .env.passwords
    
    Returns:
        bool: True if file was loaded, False otherwise
    """
    # Get project root (assuming script is in core/config/)
    project_root = Path(__file__).parent.parent.parent
    
    # Try core/config/.env.passwords first
    env_paths = [
        project_root / "core" / "config" / ".env.passwords",
        project_root / ".env.passwords",
        Path.cwd() / ".env.passwords",
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path, override=True)
            print(f"✅ Loaded environment from: {env_path}")
            return True
    
    print("⚠️  No .env.passwords file found. Using system environment variables.")
    return False


def get_hostinger_credentials(project: str) -> dict:
    """
    Get Hostinger credentials for a specific project.
    
    Args:
        project: Project name (expenseiq, kpi, portfolio)
    
    Returns:
        dict: Credentials with keys: server, ip, ssh_user, ssh_host, password
    """
    project_upper = project.upper()
    
    return {
        "server": os.getenv(f"HOSTINGER_{project_upper}_SERVER"),
        "ip": os.getenv(f"HOSTINGER_{project_upper}_IP"),
        "ssh_user": os.getenv(f"HOSTINGER_{project_upper}_SSH_USER", "root"),
        "ssh_host": os.getenv(f"HOSTINGER_{project_upper}_SSH_HOST"),
        "password": os.getenv(f"HOSTINGER_{project_upper}_PASSWORD"),
        "github_repo": os.getenv(f"HOSTINGER_{project_upper}_GITHUB_REPO"),
        "branch": os.getenv(f"HOSTINGER_{project_upper}_BRANCH", "main"),
    }


def get_render_credentials() -> dict:
    """Get Render.com API credentials."""
    return {
        "api_key": os.getenv("RENDER_API_KEY"),
        "api_url": os.getenv("RENDER_API_URL", "https://api.render.com"),
        "dashboard_url": os.getenv("RENDER_DASHBOARD_URL", "https://dashboard.render.com"),
    }


def get_notion_credentials() -> dict:
    """Get Notion API credentials."""
    return {
        "token": os.getenv("NOTION_TOKEN"),
        "api_version": os.getenv("NOTION_API_VERSION", "v1"),
    }


def get_github_credentials() -> dict:
    """Get GitHub API credentials."""
    return {
        "token": os.getenv("GITHUB_TOKEN"),
        "username": os.getenv("GITHUB_USERNAME"),
        "api_url": os.getenv("GITHUB_API_URL", "https://api.github.com"),
    }


def get_fiap_credentials() -> dict:
    """Get FIAP portal credentials."""
    return {
        "url": os.getenv("FIAP_PORTAL_URL", "https://on.fiap.com.br"),
        "username": os.getenv("FIAP_USERNAME"),
        "password": os.getenv("FIAP_PASSWORD"),
    }


# Example usage
if __name__ == "__main__":
    # Load environment
    load_env_passwords()
    
    # Get credentials
    expenseiq_creds = get_hostinger_credentials("expenseiq")
    render_creds = get_render_credentials()
    notion_creds = get_notion_credentials()
    
    print("\n📋 Loaded Credentials:")
    print(f"ExpenseIQ IP: {expenseiq_creds.get('ip', 'NOT SET')}")
    print(f"Render API Key: {'SET' if render_creds.get('api_key') else 'NOT SET'}")
    print(f"Notion Token: {'SET' if notion_creds.get('token') else 'NOT SET'}")


