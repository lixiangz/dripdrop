"""
Application factory and route registration.
This module contains the FastAPI app creation logic.
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import health, query, evals, test

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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with your Vercel domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes with tags
    app.include_router(health.router, tags=["health"])
    app.include_router(query.router, tags=["queries"])
    app.include_router(evals.router, tags=["evaluations"])
    app.include_router(test.router, tags=["testing"])

    return app


# Create app instance (only when this module is imported for running the server)
app = create_app()
