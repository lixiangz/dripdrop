"""
Pre-validation for natural language queries to detect suspicious patterns.
"""
import re
from typing import Optional

from core.exceptions import SQLGenerationError


# Suspicious patterns that should be rejected
SUSPICIOUS_PATTERNS = [
    # SQL injection attempts
    (r';\s*(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE|CREATE)', 'SQL injection attempt detected'),
    (r'DROP\s+TABLE', 'DROP TABLE operation not allowed'),
    (r'DELETE\s+FROM', 'DELETE operation not allowed'),
    (r'UPDATE\s+', 'UPDATE operation not allowed'),
    (r'INSERT\s+INTO', 'INSERT operation not allowed'),
    (r'UNION\s+SELECT', 'UNION operation not allowed'),
    (r'--', 'SQL comment injection attempt'),
    (r'/\*', 'SQL comment injection attempt'),
    (r"'\s*OR\s*'1'\s*=\s*'1", 'SQL injection attempt (OR 1=1)'),
    (r"'\s*;\s*--", 'SQL injection attempt (comment)'),
    
    # Forbidden operations (be more specific to avoid false positives)
    (r'\bJOIN\s+', 'JOIN operations not allowed'),
    (r'\bSUBQUERY\b', 'Subqueries not allowed'),
    (r'\(SELECT\s+', 'Subqueries not allowed'),
    
    # Access control violations (only match SQL keywords, not natural language)
    (r'\bFROM\s+(?!coin_Bitcoin\b)\w+', 'Only coin_Bitcoin table is accessible'),
    (r'\bFROM\s+users\b', 'Access to users table not allowed'),
    (r'\bFROM\s+\w+.*password', 'Access to password-related queries not allowed'),
    
    # Suspicious keywords
    (r'\bGRANT\b', 'GRANT operation not allowed'),
    (r'\bREVOKE\b', 'REVOKE operation not allowed'),
    (r'\bEXEC\b', 'EXEC operation not allowed'),
    (r'\bEXECUTE\b', 'EXECUTE operation not allowed'),
]


def validate_query_input(question: str) -> None:
    """
    Validate natural language query for suspicious patterns.
    
    Args:
        question: Natural language query string
        
    Raises:
        SQLGenerationError: If suspicious patterns are detected
    """
    if not question or not question.strip():
        raise SQLGenerationError("Query cannot be empty")
    
    question_lower = question.lower()
    
    # Check for suspicious patterns
    for pattern, error_msg in SUSPICIOUS_PATTERNS:
        if re.search(pattern, question_lower, re.IGNORECASE):
            raise SQLGenerationError(
                f"Security violation: {error_msg}. "
                "Only SELECT queries on the coin_Bitcoin table are allowed."
            )
    
    # Check for attempts to bypass validation with encoding
    if '%' in question or '\\x' in question or '\\u' in question:
        raise SQLGenerationError(
            "Security violation: Encoded characters detected. "
            "Please use plain text queries only."
        )

