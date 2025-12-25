"use client";

interface EvalsSectionProps {
  evalsLoading: boolean;
  onRunEvals: () => void;
}

export default function EvalsSection({
  evalsLoading,
  onRunEvals,
}: EvalsSectionProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Run Evaluations
      </h2>
      <div className="space-y-4">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Run all evaluation test cases to verify SQL generation and security.
        </p>
        <button
          onClick={onRunEvals}
          disabled={evalsLoading}
          className="w-full bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {evalsLoading ? (
            <>
              <LoadingSpinner />
              Running...
            </>
          ) : (
            "Run Evals"
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

