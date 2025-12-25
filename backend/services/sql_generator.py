"""
SQL generation using OpenAI GPT-5 with Context-Free Grammar (CFG) constraints.
Generates SQL queries that match the exact grammar defined in sql_guard.py.
"""
import logging
from typing import Optional

from openai import OpenAI

from core.config import ConfigurationError, get_env, require_env
from core.exceptions import SQLGenerationError
from security.schema import COLUMNS, NUMERIC_COLUMNS, TABLE
from security.sql_guard import sql_grammar, validate_sql

logger = logging.getLogger(__name__)

# Environment variable names
API_KEY_ENV = "OPENAI_API_KEY"
MODEL_ENV = "OPENAI_MODEL"
DEFAULT_MODEL = "gpt-5.2"

# Tool configuration
TOOL_NAME = "sql_query"

# Build column descriptions for system instructions
COLUMN_LIST = ", ".join(COLUMNS)
NUMERIC_COLUMN_LIST = ", ".join(NUMERIC_COLUMNS)

SYSTEM_INSTRUCTIONS = (
    f"You generate ClickHouse SQL queries for the Bitcoin cryptocurrency dataset. "
    f"The table is '{TABLE}' with columns: {COLUMN_LIST}. "
    f"\n\n"
    f"Column details (all lowercase):\n"
    f"- date: DateTime timestamp of the data point (data range: 2013-04-29 to 2021-07-06)\n"
    f"- close, high, low, open: Price values (Float)\n"
    f"- volume: Trading volume (Float)\n"
    f"- marketcap: Market capitalization (Float)\n"
    f"\n"
    f"IMPORTANT: Data is from 2013-2021, so 'now() - INTERVAL' queries will return empty results.\n"
    f"Use date ranges like 'date BETWEEN \\'YYYY-MM-DD\\' AND \\'YYYY-MM-DD\\'' instead.\n"
    f"\n"
    f"Rules:\n"
    f"1. Use a single SELECT statement that matches the provided grammar exactly.\n"
    f"2. Numeric columns ({NUMERIC_COLUMN_LIST}) can be aggregated with SUM, AVG, MIN, MAX.\n"
    f"3. Use COUNT(*) to count all rows, or COUNT(column) to count non-null values.\n"
    f"4. ALL queries MUST include a time window filter on the date column using:\n"
    f"   - date >= now() - INTERVAL N HOUR (for last N hours - note: data ends in 2021)\n"
    f"   - date >= now() - INTERVAL N DAY (for last N days - note: data ends in 2021)\n"
    f"   - date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD' (for date ranges - RECOMMENDED)\n"
    f"5. Optional: Use GROUP BY with toStartOfDay(date) or toStartOfHour(date) for time-based grouping.\n"
    f"6. Use exact column names as shown - ALL COLUMN NAMES MUST BE LOWERCASE: date, close, high, low, open, volume, marketcap.\n"
    f"   Do NOT use uppercase like Date, Close, etc. - use lowercase only.\n"
    f"7. Return only the SQL query, no explanations or markdown formatting.\n"
)


class SQLGenerator:
    """
    Generates SQL queries using OpenAI GPT-5 with CFG constraints.
    
    The generated SQL is guaranteed to match the grammar defined in sql_guard.py,
    ensuring security and correctness.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the SQL generator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model name (defaults to OPENAI_MODEL env var or DEFAULT_MODEL)
        """
        self.api_key = api_key or require_env(
            API_KEY_ENV,
            f"{API_KEY_ENV} is required. Set it in backend/.env",
            ConfigurationError,
        )
        self.model = model or get_env(MODEL_ENV, DEFAULT_MODEL)
        self._client: Optional[OpenAI] = None
    
    @property
    def client(self) -> OpenAI:
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key)
        return self._client
    
    def _create_tool_definition(self) -> dict:
        """
        Create the CFG-constrained tool definition for GPT-5.
        
        Returns:
            Tool definition dictionary with grammar constraint
        """
        return {
            "type": "custom",
            "name": TOOL_NAME,
            "description": (
                f"Generate a single ClickHouse SELECT statement for the {TABLE} table. "
                "The query must include a time window filter on the Date column."
            ),
            "format": {
                "type": "grammar",
                "syntax": "lark",
                "definition": sql_grammar(),
            },
        }
    
    def _extract_sql_from_response(self, response) -> str:
        """
        Extract SQL from GPT-5 response.
        
        Args:
            response: OpenAI response object
            
        Returns:
            Generated SQL query string
            
        Raises:
            SQLGenerationError: If no valid SQL is found in the response
        """
        # Look for custom tool call in the response output
        if not hasattr(response, "output"):
            raise SQLGenerationError("Response missing 'output' attribute")
        
        for item in response.output:
            if (
                getattr(item, "type", None) == "custom_tool_call"
                and getattr(item, "name", "") == TOOL_NAME
            ):
                sql = getattr(item, "input", None)
                if sql:
                    return sql.strip()
        
        raise SQLGenerationError(
            f"No valid SQL found in response. Expected custom_tool_call with name '{TOOL_NAME}'"
        )
    
    def generate(self, prompt: str) -> str:
        """
        Generate SQL query from natural language prompt.
        
        Args:
            prompt: Natural language query (e.g., "sum the total volume in the last 30 hours")
            
        Returns:
            Validated SQL query string
            
        Raises:
            ValueError: If prompt is empty
            SQLGenerationError: If generation fails
            ValueError: If generated SQL doesn't match grammar
        """
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        logger.info(
            "Generating SQL from prompt",
            extra={"model": self.model, "prompt_length": len(prompt)}
        )
        
        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                instructions=SYSTEM_INSTRUCTIONS,
                tools=[self._create_tool_definition()],
                # Force the tool call to ensure CFG-constrained output
                tool_choice={"type": "custom", "name": TOOL_NAME},
                temperature=0,  # Deterministic output
                max_output_tokens=512,  # SQL queries should be concise
            )
        except Exception as e:
            logger.exception("OpenAI API call failed", extra={"model": self.model})
            raise SQLGenerationError(f"Failed to generate SQL: {str(e)}") from e
        
        try:
            sql = self._extract_sql_from_response(response)
        except SQLGenerationError:
            logger.error("Failed to extract SQL from response", extra={"model": self.model})
            raise
        
        # Validate the generated SQL against the grammar
        try:
            validate_sql(sql)
        except ValueError as e:
            logger.error(
                "Generated SQL failed validation",
                extra={"model": self.model, "sql": sql, "error": str(e)}
            )
            raise ValueError(f"Generated SQL does not match grammar: {e}") from e
        
        logger.info(
            "Successfully generated and validated SQL",
            extra={"model": self.model, "sql_length": len(sql)}
        )
        
        return sql


# Convenience function for simple usage
def generate_sql(prompt: str, api_key: Optional[str] = None, model: Optional[str] = None) -> str:
    """
    Generate SQL from a natural language prompt.
    
    Convenience function that creates a SQLGenerator instance and generates SQL.
    
    Args:
        prompt: Natural language query
        api_key: Optional OpenAI API key (defaults to env var)
        model: Optional model name (defaults to env var or DEFAULT_MODEL)
        
    Returns:
        Validated SQL query string
    """
    generator = SQLGenerator(api_key=api_key, model=model)
    return generator.generate(prompt)

