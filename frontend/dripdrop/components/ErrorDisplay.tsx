"use client";

interface ErrorDisplayProps {
  title?: string;
  message: string;
}

export default function ErrorDisplay({
  title = "Error",
  message,
}: ErrorDisplayProps) {
  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
      <h3 className="text-sm font-medium text-red-800 dark:text-red-200 mb-2">
        {title}
      </h3>
      <p className="text-sm text-red-700 dark:text-red-300">{message}</p>
    </div>
  );
}

