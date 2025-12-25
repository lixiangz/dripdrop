"use client";

import { useQuery } from "@/hooks/useQuery";
import { useEvals } from "@/hooks/useEvals";
import DataInfoSection from "@/components/DataInfoSection";
import QuerySection from "@/components/QuerySection";
import EvalsSection from "@/components/EvalsSection";
import QueryResults from "@/components/QueryResults";
import EvalsResults from "@/components/EvalsResults";
import ErrorDisplay from "@/components/ErrorDisplay";

export default function Home() {
    const {
        query,
        setQuery,
        queryLoading,
        queryResult,
        queryError,
        handleRunQuery,
    } = useQuery();

    const {
        evalsLoading,
        evalsResult,
        evalsError,
        handleRunEvals,
        clearResults: clearEvalsResults,
    } = useEvals();

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <div className="container mx-auto px-4 py-8 max-w-7xl">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                        Bitcoin Price Data Query Interface
                    </h1>
                    <p className="text-gray-600 dark:text-gray-400">
                        Natural language to SQL queries with CFG validation
                    </p>
                </header>

                <DataInfoSection />

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    <QuerySection
                        query={query}
                        setQuery={setQuery}
                        queryLoading={queryLoading}
                        onRunQuery={handleRunQuery}
                    />

                    <EvalsSection
                        evalsLoading={evalsLoading}
                        onRunEvals={handleRunEvals}
                    />
                </div>

                {queryResult && <QueryResults result={queryResult} />}

                {queryError && <ErrorDisplay message={queryError} />}

                {evalsResult && (
                    <EvalsResults
                        result={evalsResult}
                        onClose={clearEvalsResults}
                    />
                )}

                {evalsError && <ErrorDisplay message={evalsError} />}
            </div>
        </div>
    );
}
