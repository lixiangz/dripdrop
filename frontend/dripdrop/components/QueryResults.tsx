"use client";

import { QueryResponse } from "@/types/api";
import ResultsTable from "./ResultsTable";

interface QueryResultsProps {
  result: QueryResponse;
}

export default function QueryResults({ result }: QueryResultsProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Query Results
      </h2>
      <div className="space-y-6">
        {/* Generated SQL */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Generated SQL
          </h3>
          <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm font-mono text-gray-900 dark:text-gray-100">
            {result.sql}
          </pre>
        </div>

        {/* Warning */}
        {result.warning && (
          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
            <p className="text-sm text-yellow-800 dark:text-yellow-200">
              <strong>Warning:</strong> {result.warning}
            </p>
          </div>
        )}

        {/* Results Table */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Results
          </h3>
          <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 overflow-x-auto">
            <ResultsTable data={result.data} />
          </div>
        </div>
      </div>
    </div>
  );
}

