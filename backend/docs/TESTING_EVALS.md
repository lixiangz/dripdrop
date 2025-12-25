# Testing Evals

Guide for testing SQL generation via the `/evals/run` endpoint.

## Quick Start

Run all CFG evals (functional + security tests):

```bash
cd backend
python -m tests.run_cfg_evals
```

## Endpoint

**POST** `/evals/run`

## Request Format

```json
{
    "test_cases": [
        {
            "name": "Test name (optional)",
            "question": "natural language query",
            "expected_sql": "optional expected SQL",
            "should_pass": true,
            "expected_error_contains": ["error", "keywords"]
        }
    ]
}
```

**Fields:**

-   `question` (required) - Natural language query
-   `should_pass` (default: `true`) - `false` for security tests
-   `expected_sql` (optional) - Validate generated SQL matches
-   `expected_error_contains` (optional) - Error keywords for security tests

## Response Format

```json
{
    "total": 1,
    "passed": 1,
    "failed": 0,
    "results": [
        {
            "name": "Test name",
            "status": "pass",
            "actual_sql": "generated SQL",
            "sql_match": true,
            "error": null
        }
    ]
}
```

**Status values:**

-   `"pass"` - Test passed
-   `"sql_mismatch"` - SQL doesn't match expected
-   `"error"` - Error during generation/execution
-   `"security_fail"` - Security test failed (should have been rejected)

## Example Test Cases

### Functional Test

```json
{
    "test_cases": [
        {
            "name": "SUM aggregation",
            "question": "sum volume from 2020 to 2021",
            "should_pass": true
        }
    ]
}
```

### Security Test

```json
{
    "test_cases": [
        {
            "name": "SQL injection attempt",
            "question": "sum volume; DROP TABLE coin_Bitcoin; --",
            "should_pass": false,
            "expected_error_contains": ["DROP", "Security violation"]
        }
    ]
}
```

## Testing Methods

### cURL

```bash
curl -X POST http://localhost:8000/evals/run \
  -H "Content-Type: application/json" \
  -d '{"test_cases": [{"question": "average close in 2020"}]}'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/evals/run",
    json={"test_cases": [{"question": "average close in 2020"}]}
)
print(response.json())
```

## Tips

1. **Date ranges**: Data is from 2013-04-29 to 2021-07-06
2. **SQL comparison**: Case-insensitive, whitespace-normalized, aliases/LIMIT ignored
3. **Security tests**: Set `should_pass: false`, use `expected_error_contains` to verify rejection
4. **Column names**: Must be lowercase (`date`, `close`, etc.)

## Common Issues

-   **"SQL does not match grammar"**: Check column names are lowercase, date filters included
-   **"Date range validation failed"**: Ensure dates within 2013-04-29 to 2021-07-06, max 9 years
-   **Security test failing**: Query wasn't rejected - check suspicious patterns are detected
