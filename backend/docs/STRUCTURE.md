# Backend Structure

High-level overview of the backend architecture.

## Directory Structure

```
backend/
├── app/           # FastAPI application (main.py, dependencies, instances)
├── api/           # API routes (health, query, evals, test)
├── core/          # Configuration, constants, exceptions
├── services/      # Business logic (SQL generation, query execution, evals)
├── models/        # Pydantic schemas
├── db/            # Database client (Tinybird/ClickHouse)
├── security/      # SQL validation (CFG grammar, schema)
├── utils/         # Helpers (data sanitization, date validation, query validation)
├── tests/         # Test files
└── docs/          # Documentation
```

## Architecture

**Separation of Concerns:**
- `api/` - HTTP request/response handling
- `services/` - Business logic
- `db/` - Database access
- `security/` - SQL validation and schema
- `utils/` - Reusable utilities

**Key Components:**
- `app/main.py` - FastAPI app factory, route registration
- `app/instances.py` - Lazy-initialized global instances
- `app/dependencies.py` - FastAPI dependency injection
- `services/sql_generator.py` - GPT-based SQL generation with CFG constraints
- `services/query_service.py` - Query orchestration
- `security/sql_guard.py` - CFG grammar validation

## Adding Features

1. **New endpoint**: Add file in `api/` (e.g., `api/new_endpoint.py`)
2. **Business logic**: Add service in `services/`
3. **Data models**: Add to `models/schemas.py`
4. **Register route**: Add to `app/main.py`:
   ```python
   from api import new_endpoint
   app.include_router(new_endpoint.router, tags=["tag"])
   ```

## Running

```bash
cd backend
uvicorn app.main:app --reload
```

Available at `http://localhost:8000`
