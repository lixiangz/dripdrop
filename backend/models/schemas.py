"""
Pydantic models for API requests and responses.
"""
from typing import Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for natural language query."""
    question: str = Field(..., min_length=1, max_length=1000, description="Natural language query")


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    sql: str
    data: dict
    warning: Optional[str] = None


class EvalTestCase(BaseModel):
    """Single evaluation test case."""
    question: str
    expected_sql: Optional[str] = None
    expected_result: Optional[dict] = None


class EvalRequest(BaseModel):
    """Request model for evaluation endpoint."""
    test_cases: list[EvalTestCase] = Field(..., min_items=1)


class EvalResult(BaseModel):
    """Result for a single evaluation test case."""
    question: str
    expected_sql: Optional[str] = None
    status: str
    actual_sql: Optional[str] = None
    actual_result: Optional[dict] = None
    sql_match: Optional[bool] = None
    result_match: Optional[bool] = None
    error: Optional[str] = None


class EvalResponse(BaseModel):
    """Response model for evaluation endpoint."""
    total: int
    passed: int
    failed: int
    results: list[EvalResult]

