"""
Global Dependencies

Shared dependencies for routes (DB, auth, etc.).
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_db

# Re-export get_db for convenience
__all__ = ["get_db"]

