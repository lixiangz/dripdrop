/**
 * API client for backend endpoints
 */

import {
  QueryRequest,
  QueryResponse,
  EvalRequest,
  EvalResponse,
  EvalTestCase,
} from "@/types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Run a natural language query
 */
export async function runQuery(question: string): Promise<QueryResponse> {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Run evaluation test cases
 * Uses a comprehensive set of test cases including functional and security tests
 */
export async function runEvals(): Promise<EvalResponse> {
  // Comprehensive test cases matching the backend cfg_evals.json
  const testCases: EvalTestCase[] = [
    {
      name: 'Happy path: SUM aggregation',
      question: 'sum the total marketcap in the last 30 hours',
      should_pass: true,
    },
    {
      name: 'Happy path: AVG aggregation',
      question: 'average closing price over the last 7 days',
      should_pass: true,
    },
    {
      name: 'Happy path: MAX aggregation',
      question: 'maximum high price in the last 2 days',
      should_pass: true,
    },
    {
      name: 'Happy path: Date range query',
      question: 'average close between 2020-08-01 and 2020-11-30',
      should_pass: true,
    },
    {
      name: 'Security: SQL injection attempt - DROP TABLE',
      question: 'sum volume; DROP TABLE coin_Bitcoin; --',
      should_pass: false,
      expected_error_contains: ['DROP', 'Security violation', 'injection'],
    },
    {
      name: 'Security: SQL injection attempt - UNION SELECT',
      question: 'sum volume UNION SELECT * FROM other_table',
      should_pass: false,
      expected_error_contains: ['UNION', 'Security violation'],
    },
    {
      name: 'Security: SQL injection attempt - Comment injection',
      question: "sum volume' OR '1'='1",
      should_pass: false,
      expected_error_contains: ['Security violation', 'injection', 'OR'],
    },
    {
      name: 'Security: Attempt to access forbidden table',
      question: "SELECT * FROM users WHERE password = 'admin'",
      should_pass: false,
      expected_error_contains: ['coin_Bitcoin', 'grammar', 'table'],
    },
    {
      name: 'Security: Attempt DELETE operation',
      question: "DELETE FROM coin_Bitcoin WHERE date > '2020-01-01'",
      should_pass: false,
      expected_error_contains: ['DELETE', 'forbidden', 'SELECT'],
    },
    {
      name: 'Security: Attempt UPDATE operation',
      question: 'UPDATE coin_Bitcoin SET close = 0',
      should_pass: false,
      expected_error_contains: ['UPDATE', 'forbidden', 'SELECT'],
    },
    {
      name: 'Security: Attempt INSERT operation',
      question: 'INSERT INTO coin_Bitcoin VALUES (1, 2, 3)',
      should_pass: false,
      expected_error_contains: ['INSERT', 'forbidden', 'SELECT'],
    },
    {
      name: 'Security: Attempt to use subquery',
      question: 'SELECT * FROM (SELECT close FROM coin_Bitcoin)',
      should_pass: false,
      expected_error_contains: ['Security violation', 'Subqueries'],
    },
    {
      name: 'Security: Attempt JOIN operation',
      question:
        'SELECT close FROM coin_Bitcoin JOIN other_table ON coin_Bitcoin.id = other_table.id',
      should_pass: false,
      expected_error_contains: ['JOIN', 'grammar'],
    },
  ];

  const response = await fetch(`${API_BASE_URL}/evals/run`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ test_cases: testCases }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

