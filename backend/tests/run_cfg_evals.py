"""
Run CFG evals to test SQL generation against the Context-Free Grammar.

This script runs the required 3+ evals for CFG generation validation.
Run from backend directory: python -m tests.run_cfg_evals
"""
import requests
import json
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"


def load_evals():
    """Load evals from JSON file."""
    evals_file = Path(__file__).parent / "cfg_evals.json"
    with open(evals_file) as f:
        return json.load(f)


def run_cfg_evals():
    """Run CFG evals and display results."""
    print("=" * 70)
    print("CFG Generation Evals")
    print("Testing SQL generation against Context-Free Grammar")
    print("=" * 70)
    print()
    
    # Load test cases
    evals_data = load_evals()
    test_cases = evals_data["test_cases"]
    
    print(f"Running {len(test_cases)} CFG evals...\n")
    
    # Run evals
    response = requests.post(
        f"{BASE_URL}/evals/run",
        json={"test_cases": test_cases},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 200:
        print(f"ERROR: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    result = response.json()
    
    # Display summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total evals: {result['total']}")
    print(f"Passed: {result['passed']}")
    print(f"Failed: {result['failed']}")
    
    # Security test breakdown
    security_tests = [r for r in result['results'] if r.get('name', '').startswith('Security:')]
    functional_tests = [r for r in result['results'] if not r.get('name', '').startswith('Security:')]
    
    if security_tests:
        security_passed = sum(1 for r in security_tests if r['status'] == 'pass')
        security_failed = len(security_tests) - security_passed
        print(f"\nSecurity Tests: {len(security_tests)} total, {security_passed} passed, {security_failed} failed")
    
    if functional_tests:
        functional_passed = sum(1 for r in functional_tests if r['status'] == 'pass')
        functional_failed = len(functional_tests) - functional_passed
        print(f"Functional Tests: {len(functional_tests)} total, {functional_passed} passed, {functional_failed} failed")
    
    print()
    
    # Display detailed results
    print("=" * 70)
    print("DETAILED RESULTS")
    print("=" * 70)
    
    for i, eval_result in enumerate(result['results'], 1):
        # Determine status prefix
        if eval_result['status'] == 'pass':
            status_prefix = "[PASS]"
        elif eval_result['status'] == 'security_fail':
            status_prefix = "[SECURITY FAIL]"
        elif eval_result['status'] == 'security_partial':
            status_prefix = "[SECURITY PARTIAL]"
        else:
            status_prefix = "[FAIL]"
        
        # Get test case name if available (for security tests)
        test_name = eval_result.get('name') or eval_result.get('question', 'Unknown test')
        if len(test_name) > 60:
            test_name = test_name[:57] + "..."
        
        print(f"\n{i}. {status_prefix} {test_name}")
        print(f"   Status: {eval_result['status']}")
        
        if eval_result.get('expected_sql'):
            print(f"   Expected SQL: {eval_result['expected_sql']}")
        
        if eval_result.get('actual_sql'):
            print(f"   Actual SQL:   {eval_result['actual_sql']}")
        
        if eval_result.get('sql_match') is not None:
            match_status = "MATCH" if eval_result['sql_match'] else "NO MATCH"
            print(f"   SQL Match: {match_status}")
        
        if eval_result.get('error'):
            error_msg = eval_result['error']
            # Truncate long error messages
            if len(error_msg) > 200:
                error_msg = error_msg[:197] + "..."
            print(f"   Error: {error_msg}")
        
        if eval_result.get('actual_result'):
            data = eval_result['actual_result']
            print(f"   Result: {len(data.get('rows', []))} rows returned")
    
    print("\n" + "=" * 70)
    
    # Exit with error code if any failed
    if result['failed'] > 0:
        print(f"FAILED: {result['failed']} eval(s) failed")
        sys.exit(1)
    else:
        print("SUCCESS: All CFG evals passed!")
        sys.exit(0)


if __name__ == "__main__":
    try:
        run_cfg_evals()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server.")
        print("Make sure the server is running: cd backend && uvicorn app.main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

