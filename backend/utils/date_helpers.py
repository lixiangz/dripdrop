"""
Date extraction and validation utilities.
"""
import re
from datetime import datetime
from typing import Optional, Tuple

from core.constants import DATA_MIN_DATE, DATA_MAX_DATE, MAX_DATE_RANGE_DAYS
from core.exceptions import DateRangeError


def extract_dates_from_sql(sql: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract date values from SQL query.
    
    Args:
        sql: SQL query string
        
    Returns:
        Tuple of (min_date, max_date) or (None, None) if not found
    """
    # Pattern for date = 'YYYY-MM-DD' (equality)
    equals_pattern = r"date\s*=\s+['\"](\d{4}-\d{2}-\d{2})['\"]"
    equals_match = re.search(equals_pattern, sql, re.IGNORECASE)
    if equals_match:
        date_value = equals_match.group(1)
        return date_value, date_value

    # Pattern for BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD' or BETWEEN 'YYYY-MM-DD HH:MM:SS' AND 'YYYY-MM-DD HH:MM:SS'
    # Extract just the date part (YYYY-MM-DD) from DateTime strings
    between_pattern = r"date\s+BETWEEN\s+['\"](\d{4}-\d{2}-\d{2})(?:\s+\d{2}:\d{2}:\d{2})?['\"]\s+AND\s+['\"](\d{4}-\d{2}-\d{2})(?:\s+\d{2}:\d{2}:\d{2})?['\"]"
    match = re.search(between_pattern, sql, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)

    # Pattern for date >= 'YYYY-MM-DD' or date <= 'YYYY-MM-DD'
    gte_pattern = r"date\s*>=\s+['\"](\d{4}-\d{2}-\d{2})['\"]"
    lte_pattern = r"date\s*<=\s+['\"](\d{4}-\d{2}-\d{2})['\"]"

    min_date = None
    max_date = None

    gte_match = re.search(gte_pattern, sql, re.IGNORECASE)
    if gte_match:
        min_date = gte_match.group(1)

    lte_match = re.search(lte_pattern, sql, re.IGNORECASE)
    if lte_match:
        max_date = lte_match.group(1)

    return min_date, max_date


def validate_date_range(sql: str) -> None:
    """
    Validate that dates in SQL query are within the data range.
    
    Args:
        sql: SQL query string
        
    Raises:
        DateRangeError: If dates are out of range or invalid
    """
    min_date, max_date = extract_dates_from_sql(sql)

    if min_date is None and max_date is None:
        # No explicit dates found, might be using now() - INTERVAL
        # We'll let it pass but note that data ends in 2021
        return

    if min_date and min_date < DATA_MIN_DATE:
        raise DateRangeError(
            f"Query date '{min_date}' is before the earliest data available. "
            f"Data is available from {DATA_MIN_DATE} to {DATA_MAX_DATE}."
        )

    if max_date and max_date > DATA_MAX_DATE:
        raise DateRangeError(
            f"Query date '{max_date}' is after the latest data available. "
            f"Data is available from {DATA_MIN_DATE} to {DATA_MAX_DATE}."
        )

    if min_date and max_date and min_date > max_date:
        raise DateRangeError(
            f"Invalid date range: start date '{min_date}' is after end date '{max_date}'."
        )

    # Check for very large date ranges that might cause performance issues
    if min_date and max_date:
        try:
            start = datetime.strptime(min_date, "%Y-%m-%d")
            end = datetime.strptime(max_date, "%Y-%m-%d")
            days_diff = (end - start).days
            if days_diff > MAX_DATE_RANGE_DAYS:
                raise DateRangeError(
                    f"Date range is too large ({days_diff} days). "
                    f"Please use a smaller date range (recommended: less than 1 year)."
                )
        except ValueError:
            # Date parsing failed, let the database handle it
            pass

