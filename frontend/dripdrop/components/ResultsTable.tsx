/**
 * Component for rendering query results in table format
 */

import { QueryData, RowsColumnsData, ArrayOfObjectsData } from "@/types/api";

interface ResultsTableProps {
  data: QueryData;
}

export default function ResultsTable({ data }: ResultsTableProps) {
  if (!data || typeof data !== "object") {
    return (
      <pre className="text-sm">{JSON.stringify(data, null, 2)}</pre>
    );
  }

  // Check if data has rows/columns structure
  if (isRowsColumnsData(data)) {
    return <RowsColumnsTable data={data} />;
  }

  // Check if data is an array of objects
  if (Array.isArray(data)) {
    return <ArrayOfObjectsTable data={data} />;
  }

  // Fallback: render as JSON
  return <pre className="text-sm">{JSON.stringify(data, null, 2)}</pre>;
}

function isRowsColumnsData(
  data: QueryData
): data is RowsColumnsData {
  return (
    data !== null &&
    typeof data === "object" &&
    "rows" in data &&
    "columns" in data &&
    Array.isArray(data.rows) &&
    Array.isArray(data.columns)
  );
}

function RowsColumnsTable({ data }: { data: RowsColumnsData }) {
  const { columns, rows } = data;

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-800">
          <tr>
            {columns.map((col: string, idx: number) => (
              <th
                key={idx}
                className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-300"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
          {rows.map((row: unknown[], rowIdx: number) => (
            <tr
              key={rowIdx}
              className="hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              {row.map((cell: unknown, cellIdx: number) => (
                <td
                  key={cellIdx}
                  className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100"
                >
                  {cell !== null && cell !== undefined
                    ? String(cell)
                    : "null"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ArrayOfObjectsTable({ data }: { data: ArrayOfObjectsData }) {
  if (data.length === 0) {
    return (
      <p className="text-gray-500 dark:text-gray-400">No results</p>
    );
  }

  const keys = Object.keys(data[0] as Record<string, unknown>);

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-800">
          <tr>
            {keys.map((key) => (
              <th
                key={key}
                className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-300"
              >
                {key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
          {data.map((row: Record<string, unknown>, rowIdx: number) => (
            <tr
              key={rowIdx}
              className="hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              {keys.map((key) => (
                <td
                  key={key}
                  className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100"
                >
                  {row[key] !== null && row[key] !== undefined
                    ? String(row[key])
                    : "null"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

