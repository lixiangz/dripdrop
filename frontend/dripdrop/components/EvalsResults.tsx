"use client";

import { EvalResponse, EvalResult, EvalStatus } from "@/types/api";

interface EvalsResultsProps {
  result: EvalResponse;
  onClose: () => void;
}

export default function EvalsResults({ result, onClose }: EvalsResultsProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Evaluation Results
        </h2>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          aria-label="Close evaluation results"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
      <div className="space-y-6">
        {/* Summary */}
        <SummaryStats
          total={result.total}
          passed={result.passed}
          failed={result.failed}
        />

        {/* Per-case Results */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Test Cases
          </h3>
          <div className="space-y-3">
            {result.results.map((evalResult, idx) => (
              <EvalResultCard key={idx} result={evalResult} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function SummaryStats({
  total,
  passed,
  failed,
}: {
  total: number;
  passed: number;
  failed: number;
}) {
  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
        <div className="text-sm text-gray-600 dark:text-gray-400">Total</div>
        <div className="text-2xl font-bold text-gray-900 dark:text-white">
          {total}
        </div>
      </div>
      <div className="bg-green-100 dark:bg-green-900/20 rounded-lg p-4">
        <div className="text-sm text-green-600 dark:text-green-400">
          Passed
        </div>
        <div className="text-2xl font-bold text-green-700 dark:text-green-300">
          {passed}
        </div>
      </div>
      <div className="bg-red-100 dark:bg-red-900/20 rounded-lg p-4">
        <div className="text-sm text-red-600 dark:text-red-400">Failed</div>
        <div className="text-2xl font-bold text-red-700 dark:text-red-300">
          {failed}
        </div>
      </div>
    </div>
  );
}

function EvalResultCard({ result }: { result: EvalResult }) {
  const isPassed = result.status === "pass";

  return (
    <div
      className={`border rounded-lg p-4 ${
        isPassed
          ? "bg-green-50 dark:bg-green-900/10 border-green-200 dark:border-green-800"
          : "bg-red-50 dark:bg-red-900/10 border-red-200 dark:border-red-800"
      }`}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <StatusBadge status={result.status} />
            {result.name && (
              <span className="font-medium text-gray-900 dark:text-white">
                {result.name}
              </span>
            )}
          </div>
          <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
            <strong>Question:</strong> {result.question}
          </p>
        </div>
      </div>

      {result.actual_sql && (
        <div className="mt-3">
          <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
            Generated SQL:
          </p>
          <pre className="bg-gray-100 dark:bg-gray-900 p-2 rounded text-xs font-mono text-gray-900 dark:text-gray-100 overflow-x-auto">
            {result.actual_sql}
          </pre>
        </div>
      )}

      {result.error && (
        <ErrorDisplay error={result.error} isPassed={isPassed} />
      )}

      {result.actual_result && (
        <div className="mt-3">
          <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
            Result:
          </p>
          <pre className="bg-gray-100 dark:bg-gray-900 p-2 rounded text-xs font-mono text-gray-900 dark:text-gray-100 overflow-x-auto max-h-32 overflow-y-auto">
            {JSON.stringify(result.actual_result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: EvalStatus }) {
  const isPassed = status === "pass";
  return (
    <span
      className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
        isPassed
          ? "bg-green-200 text-green-800 dark:bg-green-800 dark:text-green-200"
          : "bg-red-200 text-red-800 dark:bg-red-800 dark:text-red-200"
      }`}
    >
      {isPassed ? "✓ PASS" : `✗ ${status.toUpperCase()}`}
    </span>
  );
}

function ErrorDisplay({
  error,
  isPassed,
}: {
  error: string;
  isPassed: boolean;
}) {
  if (isPassed) {
    // For passing security tests, the error is actually the rejection message (success)
    return (
      <div className="mt-3">
        <p className="text-xs font-medium text-green-600 dark:text-green-400 mb-1">
          Security Check:
        </p>
        <p className="text-xs text-green-700 dark:text-green-300">{error}</p>
      </div>
    );
  }

  // For failed tests, show as error
  return (
    <div className="mt-3">
      <p className="text-xs font-medium text-red-600 dark:text-red-400 mb-1">
        Error:
      </p>
      <p className="text-xs text-red-700 dark:text-red-300">{error}</p>
    </div>
  );
}

