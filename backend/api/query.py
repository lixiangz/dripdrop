"""
Query endpoint for natural language to SQL conversion.
"""
import logging

from fastapi import APIRouter, HTTPException, Depends, Request

from core.constants import MAX_QUESTION_LENGTH
from core.exceptions import DateRangeError, QueryExecutionError, SQLGenerationError
from db.client import DatabaseClient
from models.schemas import QueryRequest, QueryResponse
from services.query_service import QueryService
from services.sql_generator import SQLGenerator
from app.dependencies import get_database, get_generator
from app.rate_limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
@limiter.limit("10/minute")
def query(
    request: Request,
    body: QueryRequest,
    db: DatabaseClient = Depends(get_database),
    generator: SQLGenerator = Depends(get_generator),
):
    """
    Generate SQL from natural language query and execute it.
    
    Args:
        body: Query request with natural language question
        db: Database client dependency
        generator: SQL generator dependency
        
    Returns:
        Query response with SQL and results
    """
    # Validate question length
    if len(body.question) > MAX_QUESTION_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Question is too long. Please keep it under {MAX_QUESTION_LENGTH} characters."
        )
    
    try:
        query_service = QueryService(db, generator)
        result = query_service.execute_query(body.question)
        return QueryResponse(**result)
    except SQLGenerationError as e:
        logger.error(f"SQL generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate SQL: {str(e)}"
        )
    except DateRangeError as e:
        logger.warning(f"Date range validation failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except QueryExecutionError as e:
        logger.error(f"Query execution failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except ValueError as e:
        logger.error(f"SQL validation failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid SQL generated: {str(e)}"
        )
    except Exception as e:
        logger.exception("Unexpected error in query endpoint")
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {str(e)}"
        )

