import { useState } from "react";
import { runEvals } from "@/lib/api";
import { EvalResponse } from "@/types/api";

interface UseEvalsReturn {
  evalsLoading: boolean;
  evalsResult: EvalResponse | null;
  evalsError: string | null;
  handleRunEvals: () => Promise<void>;
  clearResults: () => void;
}

export function useEvals(): UseEvalsReturn {
  const [evalsLoading, setEvalsLoading] = useState(false);
  const [evalsResult, setEvalsResult] = useState<EvalResponse | null>(null);
  const [evalsError, setEvalsError] = useState<string | null>(null);

  const handleRunEvals = async () => {
    setEvalsLoading(true);
    setEvalsError(null);
    setEvalsResult(null);

    try {
      const result = await runEvals();
      setEvalsResult(result);
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Failed to run evals";
      setEvalsError(errorMessage);
    } finally {
      setEvalsLoading(false);
    }
  };

  const clearResults = () => {
    setEvalsResult(null);
    setEvalsError(null);
  };

  return {
    evalsLoading,
    evalsResult,
    evalsError,
    handleRunEvals,
    clearResults,
  };
}

