"""
Evaluation endpoint for running test cases.
"""
import json
import logging
from pathlib import Path

from fastapi import APIRouter, Depends

from db.client import DatabaseClient
from models.schemas import EvalResponse, EvalTestCase
from services.eval_service import EvalService
from services.sql_generator import SQLGenerator
from app.dependencies import get_database, get_generator

logger = logging.getLogger(__name__)

router = APIRouter()


def _load_default_test_cases() -> list[EvalTestCase]:
    """Load default test cases from cfg_evals.json."""
    try:
        evals_file = Path(__file__).parent.parent / "tests" / "cfg_evals.json"
        with open(evals_file) as f:
            data = json.load(f)
            return [EvalTestCase(**tc) for tc in data.get("test_cases", [])]
    except Exception as e:
        logger.warning(f"Failed to load test cases from file: {e}")
        # Return a minimal set if file loading fails
        return [
            EvalTestCase(
                name="Happy path: SUM aggregation",
                question="sum the total marketcap in the last 30 hours",
                should_pass=True,
            )
        ]


@router.get("/evals/run", response_model=EvalResponse)
def run_evals(
    db: DatabaseClient = Depends(get_database),
    generator: SQLGenerator = Depends(get_generator),
):
    """
    Run evaluation test cases.

    Uses default test cases defined in cfg_evals.json.

    Args:
        db: Database client dependency
        generator: SQL generator dependency

    Returns:
        Evaluation response with results
    """
    test_cases = _load_default_test_cases()
    eval_service = EvalService(db, generator)
    result = eval_service.run_evals(test_cases)
    return EvalResponse(**result)
