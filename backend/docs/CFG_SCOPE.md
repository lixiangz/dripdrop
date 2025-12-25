# CFG Scope Contract

This document describes the Context-Free Grammar (CFG) constraints for SQL query generation in the DripDrop API. The grammar is enforced both in GPT-5 generation and server-side validation.

## Table Schema

**Table Name:** `coin_Bitcoin` (case-sensitive)

**Available Columns (all lowercase):**

- `date` (DateTime) - Timestamp of the data point
- `close` (Float) - Closing price
- `high` (Float) - Highest price
- `low` (Float) - Lowest price
- `open` (Float) - Opening price
- `volume` (Float) - Trading volume
- `marketcap` (Float) - Market capitalization

**Important:** All column names must be lowercase in generated SQL queries.

## Data Range

**Available Data:** 2013-04-29 to 2021-07-06

**Note:** Since data ends in 2021, queries using `now() - INTERVAL` will return empty results. Use explicit date ranges instead.

## Allowed Operations

### SELECT Aggregations

The following aggregation functions are supported:

- `SUM(column)` - Sum of values
- `COUNT(*)` - Count of all rows
- `COUNT(column)` - Count of non-null values in a column
- `AVG(column)` - Average of values
- `MIN(column)` - Minimum value
- `MAX(column)` - Maximum value

**Allowed columns for aggregation:**

- `close`, `high`, `low`, `open`, `volume`, `marketcap` (numeric columns only)
- `date` can be used in `COUNT(date)` but not in other aggregations

**Examples:**

- `SUM(volume)` - Total volume
- `AVG(close)` - Average closing price
- `COUNT(*)` - Number of records
- `MAX(high)` - Maximum high price
- `MIN(low)` - Minimum low price

**Multiple Aggregations:**

Multiple aggregations are supported in a single query:

```sql
SELECT AVG(close), MAX(high), MIN(low)
FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'
```

### Column Selection

You can also select individual columns (with optional aliases):

```sql
SELECT date, close AS closing_price
FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'
```

### Required Filters

**Time Window Filter (REQUIRED):**

All queries MUST include a time window filter on the `date` column to keep queries bounded.

**Supported formats:**

1. **Date Range (RECOMMENDED):**
   - `date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` - Date range
   - `date >= 'YYYY-MM-DD'` - Greater than or equal to date
   - `date <= 'YYYY-MM-DD'` - Less than or equal to date
   - Can combine: `date >= 'YYYY-MM-DD' AND date <= 'YYYY-MM-DD'`

2. **Interval-based (Note: Data ends in 2021, so this may return empty results):**
   - `date >= now() - INTERVAL N HOUR` - Last N hours
   - `date >= now() - INTERVAL N DAY` - Last N days

**Examples:**

- "average close between august and november 2022" → `date BETWEEN '2022-08-01' AND '2022-11-30'`
- "sum volume from 2020 to 2021" → `date >= '2020-01-01' AND date <= '2021-12-31'`
- "last 30 hours" → `date >= now() - INTERVAL 30 HOUR` (will return empty - data ends in 2021)
- "last 7 days" → `date >= now() - INTERVAL 7 DAY` (will return empty - data ends in 2021)

**Date Range Validation:**

- Dates must be within the data range: 2013-04-29 to 2021-07-06
- Date ranges are limited to 9 years (3285 days) to prevent performance issues
- Start date must be before or equal to end date

### Optional: GROUP BY

**Supported grouping dimensions:**

- `toStartOfDay(date)` - Group by day
- `toStartOfHour(date)` - Group by hour

**Examples:**

```sql
SELECT AVG(close), toStartOfDay(date) AS day
FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'
GROUP BY toStartOfDay(date)
```

**Note:** When using GROUP BY, you can select the grouped dimension in the SELECT clause.

### Optional: ORDER BY

**Supported ordering:**

- `ORDER BY column ASC` - Ascending order
- `ORDER BY column DESC` - Descending order
- `ORDER BY IDENTIFIER ASC/DESC` - Order by alias or aggregated column

**Examples:**

```sql
SELECT AVG(close), toStartOfDay(date) AS day
FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'
GROUP BY toStartOfDay(date)
ORDER BY day ASC
```

### Optional: LIMIT

**Supported:**

- `LIMIT N` - Limit results to N rows

**Examples:**

```sql
SELECT date, close
FROM coin_Bitcoin
WHERE date BETWEEN '2020-01-01' AND '2021-01-01'
ORDER BY close DESC
LIMIT 10
```

### Aliases

Aliases are supported using `AS`:

- `SELECT AVG(close) AS avg_price`
- `SELECT date AS timestamp`
- `SELECT toStartOfDay(date) AS day`

## Query Structure

**Basic pattern:**

```sql
SELECT <aggregation>
FROM coin_Bitcoin
WHERE date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

**With multiple aggregations:**

```sql
SELECT <aggregation1>, <aggregation2>, <aggregation3>
FROM coin_Bitcoin
WHERE date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

**With GROUP BY:**

```sql
SELECT <aggregation>, <group_dimension>
FROM coin_Bitcoin
WHERE date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
GROUP BY <group_dimension>
```

**With ORDER BY and LIMIT:**

```sql
SELECT <aggregation>
FROM coin_Bitcoin
WHERE date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
ORDER BY <column> ASC|DESC
LIMIT N
```

## Natural Language Examples

The CFG should support queries like:

- "sum the total volume in the last 30 hours" → `SUM(volume)` with interval filter
- "count all records from the last 7 days" → `COUNT(*)` with interval filter
- "average closing price over the last 24 hours" → `AVG(close)` with interval filter
- "maximum high price in the last 2 days" → `MAX(high)` with interval filter
- "minimum low price from the last 12 hours" → `MIN(low)` with interval filter
- "average close between august and november 2022" → `AVG(close)` with date range
- "sum volume from 2020 to 2021" → `SUM(volume)` with date range
- "show me the top 10 highest closing prices in 2020" → `SELECT close, date ORDER BY close DESC LIMIT 10`

## Security Constraints

- All queries must be read-only (SELECT only)
- Only the `coin_Bitcoin` table is accessible
- Time window filter is enforced by SQL guard
- Column allowlist is enforced
- Forbidden keywords are blocked: INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, REVOKE, ATTACH, DETACH, OPTIMIZE, SYSTEM, KILL

## Validation

All generated SQL is validated against the CFG grammar using Lark parser. The grammar is defined in `security/sql_guard.py` and must match exactly what GPT-5 generates.

## Out of Scope (v1)

- JOINs with other tables
- Subqueries or CTEs
- Filtering by non-date columns in WHERE clause (only date filters are allowed)
- Complex WHERE conditions (only time window filters)
- Window functions
- UNION queries
- Multiple tables

