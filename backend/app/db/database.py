"""Database helper functions"""

import os

def get_database_path() -> str:
    """Get database path from environment or default"""
    return os.getenv("DATABASE_PATH", "data/sample.db")
