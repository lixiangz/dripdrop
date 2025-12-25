"""
Dependency injection for FastAPI routes.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.client import DatabaseClient
    from services.sql_generator import SQLGenerator

from app.instances import get_db_client, get_sql_generator


def get_database():
    """Dependency for database client."""
    return get_db_client()


def get_generator():
    """Dependency for SQL generator."""
    return get_sql_generator()

