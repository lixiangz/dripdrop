"""
Global instance management for database client and SQL generator.
Uses lazy initialization to avoid errors on import if environment variables are missing.
"""
import logging
from typing import Optional

from dotenv import load_dotenv

from db.client import DatabaseClient
from services.sql_generator import SQLGenerator

logger = logging.getLogger(__name__)

load_dotenv()

# Global instances (initialized on first use)
_db_client: Optional[DatabaseClient] = None
_sql_generator: Optional[SQLGenerator] = None


def get_db_client() -> DatabaseClient:
    """
    Get or create database client instance (lazy initialization).

    Returns:
        DatabaseClient instance
    """
    global _db_client
    if _db_client is None:
        _db_client = DatabaseClient()
    return _db_client


def get_sql_generator() -> SQLGenerator:
    """
    Get or create SQL generator instance (lazy initialization).

    Returns:
        SQLGenerator instance
    """
    global _sql_generator
    if _sql_generator is None:
        _sql_generator = SQLGenerator()
    return _sql_generator
