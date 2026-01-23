#!/usr/bin/env python3
"""
Initialize Database

Script to initialize the database (create tables, seed data, etc.).
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.database import Base, engine
from src.core.config import settings


def init_db():
    """Initialize database tables."""
    print(f"Initializing database: {settings.DATABASE_URL}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database initialized successfully!")
    print("⚠️  Note: In production, use Alembic migrations instead of this script.")


if __name__ == "__main__":
    init_db()

