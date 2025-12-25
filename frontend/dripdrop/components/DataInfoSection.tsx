"use client";

import { useState } from "react";

export default function DataInfoSection() {
  const [showSchema, setShowSchema] = useState(false);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
      <div className="mb-4">
        <p className="text-gray-700 dark:text-gray-300">
          This application queries historical Bitcoin price data from 2013 to
          2021, including daily high, low, open, close prices, trading volume,
          and market capitalization. You can ask questions in natural language
          to analyze trends, calculate aggregations, and explore the dataset.{" "}
          <a
            href="https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory?resource=download&select=coin_Bitcoin.csv"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 underline"
          >
            View data source
          </a>
        </p>
      </div>
      <div>
        <button
          onClick={() => setShowSchema(!showSchema)}
          className="flex items-center justify-between w-full text-left text-sm font-medium text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
        >
          <span>View Database Schema</span>
          <svg
            className={`w-5 h-5 transition-transform ${
              showSchema ? "rotate-180" : ""
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>
        {showSchema && (
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-2 px-3 font-medium text-gray-700 dark:text-gray-300">
                      Column
                    </th>
                    <th className="text-left py-2 px-3 font-medium text-gray-700 dark:text-gray-300">
                      Type
                    </th>
                    <th className="text-left py-2 px-3 font-medium text-gray-700 dark:text-gray-300">
                      Description
                    </th>
                  </tr>
                </thead>
                <tbody className="text-gray-600 dark:text-gray-400">
                  {SCHEMA_ROWS.map((row, idx) => (
                    <tr
                      key={idx}
                      className="border-b border-gray-100 dark:border-gray-800"
                    >
                      <td className="py-2 px-3 font-mono">{row.column}</td>
                      <td className="py-2 px-3">{row.type}</td>
                      <td className="py-2 px-3">{row.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

interface SchemaRow {
  column: string;
  type: string;
  description: string;
}

const SCHEMA_ROWS: SchemaRow[] = [
  {
    column: "sno",
    type: "Integer",
    description: "Serial number",
  },
  {
    column: "name",
    type: "String",
    description: "Cryptocurrency name (Bitcoin)",
  },
  {
    column: "symbol",
    type: "String",
    description: "Ticker symbol (BTC)",
  },
  {
    column: "date",
    type: "DateTime",
    description: "Date and time of the record",
  },
  {
    column: "high",
    type: "Float",
    description: "Highest price during the day",
  },
  {
    column: "low",
    type: "Float",
    description: "Lowest price during the day",
  },
  {
    column: "open",
    type: "Float",
    description: "Opening price at the start of the day",
  },
  {
    column: "close",
    type: "Float",
    description: "Closing price at the end of the day",
  },
  {
    column: "volume",
    type: "Float",
    description: "Trading volume for the day",
  },
  {
    column: "marketcap",
    type: "Float",
    description: "Market capitalization",
  },
];

