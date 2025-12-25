"""
Quick test script to verify the CFG-based SQL guard works.
Run from backend directory: python -m tests.test_cfg_guard
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import from backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from security.sql_guard import validate_sql, sql_grammar

# Test cases
test_queries = [
    # Valid queries
    "SELECT AVG(Close) AS avg_close FROM coin_Bitcoin WHERE Date >= now() - INTERVAL 24 HOUR",
    "SELECT SUM(Volume) FROM coin_Bitcoin WHERE date >= now() - INTERVAL 30 HOUR",
    "SELECT COUNT(*) FROM coin_Bitcoin WHERE Date >= now() - INTERVAL 7 DAY",
    "SELECT High AS min_close FROM coin_Bitcoin WHERE date >= now() - INTERVAL 24 HOUR",
    
    # Invalid queries (should fail)
    # "SELECT * FROM coin_Bitcoin",  # No WHERE clause
    # "SELECT INSERT INTO ...",  # Forbidden keyword
]

print("Testing CFG-based SQL guard...")
print("=" * 60)

for i, sql in enumerate(test_queries, 1):
    print(f"\nTest {i}: {sql[:60]}...")
    try:
        validate_sql(sql)
        print("✓ PASSED")
    except ValueError as e:
        print(f"✗ FAILED: {e}")

print("\n" + "=" * 60)
print("\nGrammar (first 500 chars):")
print(sql_grammar()[:500] + "...")


