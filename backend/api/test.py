"""
Test endpoint for database connection verification.
This is for testing and debugging purposes, not used in production.
"""
import logging

from fastapi import APIRouter, Depends, Request

from db.client import DatabaseClient
from utils.data_helpers import sanitize_data_for_json
from app.dependencies import get_database
from app.rate_limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/test/hardcoded")
@limiter.limit("10/minute")
def test_hardcoded(
    request: Request,
    db: DatabaseClient = Depends(get_database),
):
    """
    Test endpoint to verify database connection with a hardcoded SQL query.
    This bypasses SQL generation and validation to test the Tinybird connection directly.
    """
    # First, check what columns exist and get a sample of data
    inspect_sql = "SELECT * FROM coin_Bitcoin LIMIT 5"

    # Then try the aggregation query
    # Note: Data is from 2013-2021, so use a date range that has data
    test_sql = """
        SELECT AVG(close) AS avg_close
        FROM coin_Bitcoin
        WHERE date >= '2020-01-01' AND date <= '2021-07-06'
    """

    results = {}

    try:
        # Step 1: Inspect table structure and sample data
        logger.info("Inspecting table structure...")
        inspect_data = db.query(inspect_sql)
        results["table_inspection"] = {
            "sql": inspect_sql,
            "columns": inspect_data.get("columns", []),
            "row_count": len(inspect_data.get("rows", [])),
            "sample_rows": sanitize_data_for_json(inspect_data)["rows"][:3]
        }

        # Step 2: Check date range in table
        date_range_sql = """
            SELECT 
                MIN(date) AS min_date,
                MAX(date) AS max_date,
                COUNT(*) AS total_rows
            FROM coin_Bitcoin
        """
        logger.info("Checking date range...")
        date_range_data = db.query(date_range_sql)
        results["date_range"] = sanitize_data_for_json(date_range_data)

        # Step 3: Try the aggregation query
        logger.info(f"Testing aggregation query: {test_sql.strip()}")
        test_data = db.query(test_sql)
        results["aggregation_test"] = {
            "sql": test_sql.strip(),
            "data": sanitize_data_for_json(test_data),
            "message": "Query executed successfully"
        }

        logger.info("All database tests passed")
        return {
            "status": "success",
            "message": "Database connection successful",
            "results": results
        }

    except Exception as e:
        logger.exception("Database connection test failed")
        return {
            "status": "error",
            "message": f"Database test failed: {str(e)}",
            "results": results if results else {}
        }
