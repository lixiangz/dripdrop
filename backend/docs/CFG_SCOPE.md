# CFG Scope Contract

SQL query constraints enforced by CFG grammar in GPT model generation and server-side validation.

## Table Schema

**Table:** `coin_Bitcoin` (case-sensitive)

**Columns (all lowercase):**

-   `date` (DateTime) - Data range: 2013-04-29 to 2021-07-06
-   `close`, `high`, `low`, `open`, `volume`, `marketcap` (Float)

## Allowed Operations

### SELECT Aggregations

-   `SUM()`, `AVG()`, `MIN()`, `MAX()` - On numeric columns only
-   `COUNT(*)` or `COUNT(column)` - Count rows or non-null values
-   Multiple aggregations supported

### Column Selection

-   Select individual columns with optional aliases (`AS alias_name`)

### Required: Time Window Filter

All queries MUST include a date filter:

-   `date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` (recommended)
-   `date >= now() - INTERVAL N HOUR/DAY` (note: data ends in 2021, may return empty)

### Optional: GROUP BY

-   `toStartOfDay(date)` - Group by day
-   `toStartOfHour(date)` - Group by hour

### Optional: ORDER BY

-   `ORDER BY column ASC/DESC` - Single or multiple columns
-   Can order by aliases

### Optional: LIMIT

-   `LIMIT N` - Limit result rows

## Example Queries

```sql
-- Aggregation with date range
SELECT AVG(close) FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'

-- Multiple aggregations
SELECT AVG(close), MAX(high), MIN(low)
FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'

-- Group by day
SELECT AVG(close), toStartOfDay(date) AS day
FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'
GROUP BY toStartOfDay(date)

-- Order and limit
SELECT date, close
FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'
ORDER BY close DESC LIMIT 10
```

## Security

**Validation layers:**

1. Pre-validation: Natural language input checked for SQL injection (`utils/query_validation.py`)
2. Grammar validation: SQL parsed against CFG grammar (`security/sql_guard.py`)
3. Date validation: Date ranges validated (`utils/date_helpers.py`)

**Constraints:**

-   Read-only (SELECT only)
-   Only `coin_Bitcoin` table accessible
-   Forbidden keywords blocked: INSERT, UPDATE, DELETE, DROP, ALTER, etc.
-   Time window filter required
-   Column allowlist enforced

## Out of Scope (v1)

-   JOINs, subqueries, CTEs
-   Filtering by non-date columns
-   Window functions, UNION
-   Multiple tables
-   Standalone `date >= 'YYYY-MM-DD'` (use BETWEEN or INTERVAL)

## Implementation

-   **Model**: `gpt-5.2` (configurable via `OPENAI_MODEL`)
-   **Grammar**: Programmatically generated from `security/schema.py`
-   **Validation**: Lark parser (LALR) in `security/sql_guard.py`
