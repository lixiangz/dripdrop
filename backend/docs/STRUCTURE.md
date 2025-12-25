# Backend Structure

This document describes the refactored backend structure following proper coding standards and separation of concerns.

## Directory Structure

```
backend/
├── app/                    # FastAPI application setup
│   ├── __init__.py        # Minimal (no side effects on import)
│   ├── main.py            # App factory and route registration
│   ├── instances.py       # Global instance management (lazy init)
│   └── dependencies.py    # Dependency injection for FastAPI
│
├── api/                   # API routes (flattened structure)
│   ├── health.py          # GET /health
│   ├── query.py           # POST /query
│   ├── evals.py           # POST /evals/run
│   └── test.py            # GET /test/hardcoded
│
├── core/                  # Core configuration and constants
│   ├── config.py          # Environment variable management
│   ├── constants.py       # Application constants
│   └── exceptions.py      # Custom exceptions
│
├── services/              # Business logic services
│   ├── sql_generator.py   # SQL generation with GPT-5
│   ├── query_service.py   # Query execution logic
│   └── eval_service.py    # Evaluation logic
│
├── models/                # Pydantic models and schemas
│   └── schemas.py         # Request/response models
│
├── db/                    # Database layer
│   └── client.py          # DatabaseClient (Tinybird/ClickHouse)
│
├── security/              # Security and validation
│   ├── schema.py          # Table schema definitions
│   └── sql_guard.py       # SQL validation with CFG grammar
│
├── utils/                 # Utility functions
│   ├── data_helpers.py    # Data sanitization (NaN/Infinity handling)
│   └── date_helpers.py    # Date extraction and validation
│
├── docs/                  # Documentation
│   ├── STRUCTURE.md       # This file
│   └── CFG_SCOPE.md       # CFG grammar scope documentation
│
├── tests/                 # Test files
│   ├── test_backend.py
│   └── test_cfg_guard.py
│
└── requirements.txt       # Python dependencies
```

## Architecture Principles

### Separation of Concerns

-   **Routes** (`api/`): Handle HTTP requests/responses only
-   **Services** (`services/`): Contain business logic
-   **Models** (`models/`): Define data structures
-   **Utils** (`utils/`): Reusable helper functions
-   **Core** (`core/`): Configuration and shared constants

### Dependency Injection

-   FastAPI's `Depends()` is used for dependency injection
-   Services are injected into route handlers via `app/dependencies.py`
-   Database client and SQL generator are lazy-initialized in `app/instances.py`

### Error Handling

-   Custom exceptions in `core/exceptions.py`
-   User-friendly error messages
-   Proper HTTP status codes

### Import Safety

-   `app/__init__.py` is kept minimal to avoid side effects on import
-   `app/main.py` contains app factory (only executes when server starts)
-   Logging configuration happens in `app/main.py`, not on package import

## Key Files

### Entry Point

-   `app/main.py`: Creates FastAPI app, configures middleware, registers routes
-   `app/instances.py`: Manages global instances with lazy initialization
-   `app/dependencies.py`: Provides FastAPI dependency functions

### Services

-   `services/query_service.py`: Orchestrates query generation and execution
-   `services/eval_service.py`: Handles evaluation test cases
-   `services/sql_generator.py`: Generates SQL using GPT-5 with CFG constraints

### Routes

Each route file is self-contained with its own router:

-   `api/health.py`: GET /health
-   `api/query.py`: POST /query
-   `api/evals.py`: POST /evals/run
-   `api/test.py`: GET /test/hardcoded

### Database

-   `db/client.py`: DatabaseClient class for Tinybird/ClickHouse queries

### Security

-   `security/schema.py`: Table schema definitions (drives CFG grammar)
-   `security/sql_guard.py`: CFG-based SQL validation using Lark parser

### Utilities

-   `utils/data_helpers.py`: Sanitizes database results (handles NaN/Infinity)
-   `utils/date_helpers.py`: Extracts and validates date ranges from SQL

## Adding New Features

To add a new feature:

1. **New endpoint**: Create a new file in `api/` (e.g., `api/new_endpoint.py`)
2. **New business logic**: Create a service in `services/`
3. **New data model**: Add to `models/schemas.py`
4. **New utility**: Add to `utils/`
5. **Register route**: Add to `app/main.py`:
    ```python
    from api import new_endpoint
    app.include_router(new_endpoint.router, tags=["new_tag"])
    ```

## Running the Application

```bash
cd backend
uvicorn app.main:app --reload
```

The app will be available at `http://localhost:8000`

## Design Decisions

### Why routes are in `api/` not `api/routes/`?

-   Simpler structure when there aren't many routes
-   Easier to find and maintain
-   Can add subdirectories later if needed (e.g., `api/v1/`, `api/v2/`)

### Why `app/__init__.py` is minimal?

-   Prevents side effects when importing the package
-   Better for testing, type checking, and tooling
-   Follows Python best practices

### Why separate `app/instances.py`?

-   Separates instance management from app creation
-   Makes it clear where global state lives
-   Easier to test and mock

### Why `app/main.py` instead of root `main.py`?

-   Keeps app setup code separate from entry point
-   Allows for multiple entry points if needed
-   Cleaner structure without unnecessary wrapper files

## Benefits of This Structure

1. **Maintainability**: Clear separation makes code easy to understand
2. **Testability**: Services can be tested independently, no side effects on import
3. **Scalability**: Easy to add new features without cluttering
4. **Reusability**: Utils and services can be reused across routes
5. **Type Safety**: Pydantic models provide validation and type hints
6. **Import Safety**: No side effects when importing packages (better for tooling)
