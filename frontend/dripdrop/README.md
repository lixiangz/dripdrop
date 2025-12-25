# DripDrop Frontend

Natural language to SQL query interface with CFG validation. Built with Next.js and deployed on Vercel.

## Features

- **Natural Language Queries**: Type queries in plain English and get SQL results
- **SQL Generation**: View the generated SQL for each query
- **Results Display**: See query results in a formatted table
- **Evaluation Testing**: Run comprehensive test suites to verify SQL generation and security
- **Error Handling**: Clear error messages for failed queries
- **Loading States**: Visual feedback during API calls

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see backend README)

### Environment Variables

Create a `.env.local` file in the root directory:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, set this to your deployed backend URL.

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Build

```bash
npm run build
npm start
```

## Usage

1. **Run Query**: Enter a natural language query in the textarea (e.g., "sum the total of all orders placed in the last 30 hours") and click "Run Query"
2. **View Results**: See the generated SQL, any warnings, and the query results in formatted tables
3. **Run Evals**: Click "Run Evals" to execute all evaluation test cases and see pass/fail results

