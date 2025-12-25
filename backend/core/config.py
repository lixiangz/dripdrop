"""
Configuration and environment variable management.
"""
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class ConfigurationError(Exception):
    """Raised when a required configuration is missing or invalid."""
    pass


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get an environment variable with optional default.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.environ.get(key, default)


def require_env(key: str, error_message: Optional[str] = None, exception_class=ConfigurationError) -> str:
    """
    Get a required environment variable, raising an exception if not found.
    
    Args:
        key: Environment variable name
        error_message: Custom error message (defaults to key-based message)
        exception_class: Exception class to raise (defaults to ConfigurationError)
        
    Returns:
        Environment variable value
        
    Raises:
        exception_class: If the environment variable is not set
    """
    value = os.environ.get(key)
    if value is None:
        msg = error_message or f"Required environment variable '{key}' is not set"
        raise exception_class(msg)
    return value

