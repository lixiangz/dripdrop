/**
 * Type definitions for API requests and responses
 */

export interface QueryRequest {
  question: string;
}

export interface QueryResponse {
  sql: string;
  data: QueryData;
  warning?: string;
}

export type QueryData =
  | RowsColumnsData
  | ArrayOfObjectsData
  | Record<string, unknown>
  | null
  | undefined;

export interface RowsColumnsData {
  rows: unknown[][];
  columns: string[];
}

export interface ArrayOfObjectsData extends Array<Record<string, unknown>> {}

export interface EvalTestCase {
  name?: string;
  question: string;
  expected_sql?: string;
  expected_result?: QueryData;
  should_pass?: boolean;
  expected_error_contains?: string[];
}

export interface EvalRequest {
  test_cases: EvalTestCase[];
}

export interface EvalResult {
  question: string;
  name?: string;
  expected_sql?: string;
  status: EvalStatus;
  actual_sql?: string;
  actual_result?: QueryData;
  sql_match?: boolean;
  result_match?: boolean;
  error?: string;
}

export type EvalStatus =
  | "pass"
  | "error"
  | "sql_mismatch"
  | "result_mismatch"
  | "security_fail"
  | "security_partial";

export interface EvalResponse {
  total: number;
  passed: number;
  failed: number;
  results: EvalResult[];
}

