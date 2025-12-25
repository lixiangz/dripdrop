"""
Simple test script to verify the backend endpoints work.
Run this after starting the FastAPI server with: uvicorn app.main:app --reload
Run from backend directory: python -m tests.test_backend
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test GET /health"""
    print("Testing GET /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    print("✓ Health check passed\n")


def test_query():
    """Test POST /query with hardcoded SQL"""
    print("Testing POST /query...")
    payload = {"question": "test question"}
    response = requests.post(
        f"{BASE_URL}/query",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"SQL: {result.get('sql', 'N/A')}")
    print(f"Data columns: {result.get('data', {}).get('columns', [])}")
    print(f"Data rows: {result.get('data', {}).get('rows', [])}")
    assert response.status_code == 200
    assert "sql" in result
    assert "data" in result
    print("✓ Query endpoint passed\n")


def test_evals():
    """Test POST /evals/run"""
    print("Testing POST /evals/run...")
    payload = {
        "test_cases": [
            {
                "question": "sum the total volume in the last 30 hours",
                "expected_sql": "SELECT SUM(Volume) FROM coin_Bitcoin WHERE Date >= now() - INTERVAL 30 HOUR"
            }
        ]
    }
    response = requests.post(
        f"{BASE_URL}/evals/run",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total test cases: {result.get('total', 0)}")
    print(f"Results: {json.dumps(result.get('results', []), indent=2)}")
    assert response.status_code == 200
    assert "total" in result
    assert "results" in result
    print("✓ Evals endpoint passed\n")


if __name__ == "__main__":
    print("=" * 50)
    print("Backend API Test Suite")
    print("=" * 50)
    print()

    try:
        test_health()
        test_query()
        test_evals()
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

