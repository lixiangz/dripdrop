"""
Custom exceptions for the application.
"""


class SQLGenerationError(Exception):
    """Raised when SQL generation fails."""
    pass


class DateRangeError(Exception):
    """Raised when date range validation fails."""
    pass


class QueryExecutionError(Exception):
    """Raised when query execution fails."""
    pass

