"""
Data sanitization and transformation utilities.
"""
import math
from typing import Any


def sanitize_data_for_json(data: dict) -> dict:
    """
    Convert NaN, Infinity values to None for JSON serialization.
    ClickHouse may return NaN/Infinity which aren't JSON compliant.
    
    Args:
        data: Dictionary with 'columns' and 'rows' keys
        
    Returns:
        Sanitized dictionary with NaN/Infinity converted to None
    """
    def sanitize_value(value: Any) -> Any:
        if isinstance(value, float):
            if math.isnan(value):
                return None
            if math.isinf(value):
                return None
        elif isinstance(value, (list, tuple)):
            return [sanitize_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: sanitize_value(v) for k, v in value.items()}
        return value

    return {
        "columns": data.get("columns", []),
        "rows": [sanitize_value(row) for row in data.get("rows", [])]
    }

