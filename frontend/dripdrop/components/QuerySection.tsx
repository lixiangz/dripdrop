"use client";

import { QueryResponse } from "@/types/api";

interface QuerySectionProps {
  query: string;
  setQuery: (query: string) => void;
  queryLoading: boolean;
  onRunQuery: () => void;
}

export default function QuerySection({
  query,
  setQuery,
  queryLoading,
  onRunQuery,
}: QuerySectionProps) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Run query on Enter (but allow Shift+Enter for new lines)
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!queryLoading && query.trim()) {
        onRunQuery();
      }
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Run Query
      </h2>
      <div className="space-y-4">
        <div>
          <label
            htmlFor="query-input"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Natural Language Query
          </label>
          <textarea
            id="query-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="e.g., What is the average closing price of Bitcoin in 2020?"
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white resize-none"
            rows={4}
            disabled={queryLoading}
          />
        </div>
        <button
          onClick={onRunQuery}
          disabled={queryLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {queryLoading ? (
            <>
              <LoadingSpinner />
              Running...
            </>
          ) : (
            "Run Query"
          )}
        </button>
      </div>
    </div>
  );
}

function LoadingSpinner() {
  return (
    <svg
      className="animate-spin h-5 w-5"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      ></circle>
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  );
}

