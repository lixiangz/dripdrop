import { useState } from "react";
import { runQuery } from "@/lib/api";
import { QueryResponse } from "@/types/api";

interface UseQueryReturn {
  query: string;
  setQuery: (query: string) => void;
  queryLoading: boolean;
  queryResult: QueryResponse | null;
  queryError: string | null;
  handleRunQuery: () => Promise<void>;
  clearResults: () => void;
}

export function useQuery(): UseQueryReturn {
  const [query, setQuery] = useState("");
  const [queryLoading, setQueryLoading] = useState(false);
  const [queryResult, setQueryResult] = useState<QueryResponse | null>(null);
  const [queryError, setQueryError] = useState<string | null>(null);

  const handleRunQuery = async () => {
    if (!query.trim()) {
      setQueryError("Please enter a query");
      return;
    }

    setQueryLoading(true);
    setQueryError(null);
    setQueryResult(null);

    try {
      const result = await runQuery(query);
      setQueryResult(result);
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Failed to run query";
      setQueryError(errorMessage);
    } finally {
      setQueryLoading(false);
    }
  };

  const clearResults = () => {
    setQueryResult(null);
    setQueryError(null);
  };

  return {
    query,
    setQuery,
    queryLoading,
    queryResult,
    queryError,
    handleRunQuery,
    clearResults,
  };
}

