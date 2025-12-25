"""
Business logic for evaluation test cases.
"""
import logging
from typing import List, Dict, Any

from db.client import DatabaseClient
from models.schemas import EvalTestCase, EvalResult
from services.sql_generator import SQLGenerator

logger = logging.getLogger(__name__)


class EvalService:
    """
    Service for running evaluation test cases.
    """
    
    def __init__(self, db_client: DatabaseClient, sql_generator: SQLGenerator):
        """
        Initialize the eval service.
        
        Args:
            db_client: Database client instance
            sql_generator: SQL generator instance
        """
        self.db_client = db_client
        self.sql_generator = sql_generator
    
    def _normalize_sql(self, sql: str) -> str:
        """
        Normalize SQL for comparison (case-insensitive, whitespace).
        
        Args:
            sql: SQL query string
            
        Returns:
            Normalized SQL string
        """
        return " ".join(sql.upper().split())
    
    def _compare_results(self, actual: Dict[str, Any], expected: Dict[str, Any]) -> bool:
        """
        Compare query results (simple equality check).
        
        Args:
            actual: Actual query result
            expected: Expected query result
            
        Returns:
            True if results match
        """
        return actual == expected
    
    def run_eval(self, test_case: EvalTestCase, index: int, total: int) -> EvalResult:
        """
        Run a single evaluation test case.
        
        Args:
            test_case: Test case to run
            index: Current test case index (1-based)
            total: Total number of test cases
            
        Returns:
            EvalResult with test results
        """
        result = EvalResult(
            question=test_case.question,
            expected_sql=test_case.expected_sql,
            status="pending",
            actual_sql=None,
            actual_result=None,
            sql_match=None,
            result_match=None,
            error=None,
        )
        
        try:
            # Step 1: Generate SQL from question
            logger.info(
                f"Eval {index}/{total}: Generating SQL for: {test_case.question[:50]}"
            )
            actual_sql = self.sql_generator.generate(test_case.question)
            result.actual_sql = actual_sql
            
            # Step 2: Compare with expected SQL (if provided)
            if test_case.expected_sql:
                expected_normalized = self._normalize_sql(test_case.expected_sql)
                actual_normalized = self._normalize_sql(actual_sql)
                result.sql_match = expected_normalized == actual_normalized
                logger.info(f"SQL match: {result.sql_match}")
            
            # Step 3: Execute the generated SQL
            logger.info(f"Executing SQL: {actual_sql[:100]}")
            query_result = self.db_client.query(actual_sql)
            result.actual_result = query_result
            
            # Step 4: Compare results with expected (if provided)
            if test_case.expected_result is not None:
                result.result_match = self._compare_results(
                    query_result,
                    test_case.expected_result
                )
            
            # Determine overall status
            if result.error:
                result.status = "error"
            elif test_case.expected_sql and not result.sql_match:
                result.status = "sql_mismatch"
            elif test_case.expected_result is not None and not result.result_match:
                result.status = "result_mismatch"
            else:
                result.status = "pass"
                
        except Exception as e:
            logger.exception(f"Eval {index} failed")
            result.status = "error"
            result.error = str(e)
        
        return result
    
    def run_evals(self, test_cases: List[EvalTestCase]) -> Dict[str, Any]:
        """
        Run multiple evaluation test cases.
        
        Args:
            test_cases: List of test cases to run
            
        Returns:
            Dictionary with summary statistics and results
        """
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            result = self.run_eval(test_case, i, len(test_cases))
            results.append(result)
        
        # Calculate summary statistics
        total = len(results)
        passed = sum(1 for r in results if r.status == "pass")
        failed = sum(1 for r in results if r.status in [
            "error", "sql_mismatch", "result_mismatch"
        ])
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "results": [r.dict() for r in results],
        }

