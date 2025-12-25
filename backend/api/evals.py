"""
Evaluation endpoint for running test cases.
"""
import logging

from fastapi import APIRouter, Depends

from db.client import DatabaseClient
from models.schemas import EvalRequest, EvalResponse
from services.eval_service import EvalService
from services.sql_generator import SQLGenerator
from app.dependencies import get_database, get_generator

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/evals/run", response_model=EvalResponse)
def run_evals(
    body: EvalRequest,
    db: DatabaseClient = Depends(get_database),
    generator: SQLGenerator = Depends(get_generator),
):
    """
    Run evaluation test cases.
    
    Args:
        body: Evaluation request with test cases
        db: Database client dependency
        generator: SQL generator dependency
        
    Returns:
        Evaluation response with results
    """
    eval_service = EvalService(db, generator)
    result = eval_service.run_evals(body.test_cases)
    return EvalResponse(**result)

