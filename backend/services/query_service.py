"""
Business logic for query execution.
"""
import logging
from typing import Optional

from core.constants import DATA_MIN_DATE, DATA_MAX_DATE, LARGE_RESULT_SET_THRESHOLD
from core.exceptions import DateRangeError, QueryExecutionError
from db.client import DatabaseClient
from services.sql_generator import SQLGenerator, SQLGenerationError
from utils.data_helpers import sanitize_data_for_json
from utils.date_helpers import validate_date_range

logger = logging.getLogger(__name__)


class QueryService:
    """
    Service for handling natural language queries.
    """
    
    def __init__(self, db_client: DatabaseClient, sql_generator: SQLGenerator):
        """
        Initialize the query service.
        
        Args:
            db_client: Database client instance
            sql_generator: SQL generator instance
        """
        self.db_client = db_client
        self.sql_generator = sql_generator
    
    def _handle_database_error(self, error: Exception) -> None:
        """
        Convert database errors to user-friendly exceptions.
        
        Args:
            error: Database exception
            
        Raises:
            QueryExecutionError: With user-friendly message
        """
        error_msg = str(error).lower()
        
        if "timeout" in error_msg or "timed out" in error_msg:
            raise QueryExecutionError(
                "Query timed out. Try using a smaller date range or simpler query."
            )
        elif "syntax" in error_msg or "parse" in error_msg:
            logger.error(f"Database syntax error: {error}")
            raise QueryExecutionError(
                "Query syntax error. Please try rephrasing your question."
            )
        elif "memory" in error_msg or "out of memory" in error_msg:
            raise QueryExecutionError(
                "Query requires too much memory. Try using a smaller date range."
            )
        else:
            raise QueryExecutionError(f"Database error: {str(error)}")
    
    def _check_result_quality(self, data: dict) -> Optional[str]:
        """
        Check result quality and return warning message if needed.
        
        Args:
            data: Query result data
            
        Returns:
            Warning message or None
        """
        rows = data.get("rows", [])
        
        if not rows or len(rows) == 0:
            return (
                "Query returned no rows. This may be because the date range has no matching records. "
                f"Data is available from {DATA_MIN_DATE} to {DATA_MAX_DATE}."
            )
        
        first_row = rows[0]
        if first_row and all(v is None for v in first_row):
            return (
                "Query returned no data. This may be because the date range has no matching records, "
                f"or all values in the result are NULL. Data is available from {DATA_MIN_DATE} to {DATA_MAX_DATE}."
            )
        
        if len(rows) > LARGE_RESULT_SET_THRESHOLD:
            logger.warning(f"Large result set returned: {len(rows)} rows")
            # Could add a warning here if needed
        
        return None
    
    def execute_query(self, question: str) -> dict:
        """
        Execute a natural language query.
        
        Args:
            question: Natural language query string
            
        Returns:
            Dictionary with 'sql', 'data', and optional 'warning' keys
            
        Raises:
            ValueError: If question is invalid
            SQLGenerationError: If SQL generation fails
            DateRangeError: If date range is invalid
            QueryExecutionError: If query execution fails
        """
        # Generate SQL from natural language
        logger.info(f"Generating SQL for question: {question[:100]}")
        sql = self.sql_generator.generate(question)
        
        # Validate date range before executing
        try:
            validate_date_range(sql)
        except DateRangeError as e:
            logger.warning(f"Date range validation failed: {str(e)}")
            raise
        
        # Execute the query
        logger.info(f"Executing SQL: {sql[:100]}")
        try:
            data = self.db_client.query(sql)
        except Exception as db_error:
            self._handle_database_error(db_error)
        
        # Sanitize and check result quality
        sanitized_data = sanitize_data_for_json(data)
        warning = self._check_result_quality(sanitized_data)
        
        result = {
            "sql": sql.strip(),
            "data": sanitized_data,
        }
        
        if warning:
            result["warning"] = warning
        
        return result

