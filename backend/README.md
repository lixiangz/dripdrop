# DripDrop Backend

FastAPI backend that converts natural language queries to SQL using GPT models with CFG grammar constraints. Provides secure, validated SQL generation for Bitcoin cryptocurrency data.

## Features

-   **Natural Language to SQL**: Converts plain English queries to ClickHouse SQL
-   **CFG Grammar Validation**: Ensures generated SQL matches strict grammar rules
-   **Security**: Multi-layer validation prevents SQL injection and unauthorized operations
-   **Query Execution**: Executes validated SQL against Tinybird/ClickHouse database
-   **Evaluation Testing**: Comprehensive test suite for SQL generation and security

## Quick Start

### Prerequisites

-   Python 3.11+
-   OpenAI API key
-   Database credentials (Tinybird token or ClickHouse connection)

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Running

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`

## API Endpoints

-   `GET /health` - Health check
-   `POST /query` - Generate and execute SQL from natural language
-   `POST /evals/run` - Run evaluation test cases
-   `GET /test/hardcoded` - Test endpoint with hardcoded query

## Documentation

-   [Structure](docs/STRUCTURE.md) - Backend architecture overview
-   [CFG Scope](docs/CFG_SCOPE.md) - SQL grammar constraints and allowed operations
-   [Testing Evals](docs/TESTING_EVALS.md) - How to test SQL generation
-   [Deployment](docs/DEPLOYMENT.md) - Deployment guide for various platforms

## Architecture

-   **FastAPI** - Web framework
-   **OpenAI GPT** - SQL generation with CFG constraints
-   **Lark Parser** - Grammar validation
-   **Tinybird/ClickHouse** - Database backend

See [STRUCTURE.md](docs/STRUCTURE.md) for detailed architecture.
