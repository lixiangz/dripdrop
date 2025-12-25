"""
Schema definitions for the coin_Bitcoin table.
This drives both the CFG grammar and SQL validation.

Note: Column names are lowercase as they appear in the actual database.
"""
import re

# Table name
DATABASE = ""  # No database prefix for Tinybird/ClickHouse
TABLE = "coin_Bitcoin"

# All available columns (matching actual database schema - all lowercase)
COLUMNS = (
    "date",
    "close",
    "high",
    "low",
    "open",
    "volume",
    "marketcap",
)

# Numeric columns that can be used in aggregations (excludes date)
NUMERIC_COLUMNS = (
    "close",
    "high",
    "low",
    "open",
    "volume",
    "marketcap",
)

