"""
Application factory and route registration.
This module contains the FastAPI app creation logic.
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import health, query, evals, test
from core.config import get_env

# Configure logging (only when this module is imported, not on package import)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    This function should only be called when actually starting the server,
    not during package import.

    Returns:
        Configured FastAPI app instance
    """
    app = FastAPI(
        title="DripDrop API",
        description="Natural language to SQL query API with CFG constraints",
        version="1.0.0",
    )

    # Add CORS support for Vercel frontend
    cors_origins_env = get_env("CORS_ORIGINS", "http://localhost:3000")
    cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Register routes with tags
    app.include_router(health.router, tags=["health"])
    app.include_router(query.router, tags=["queries"])
    app.include_router(evals.router, tags=["evaluations"])
    app.include_router(test.router, tags=["testing"])

    return app


app = create_app()
