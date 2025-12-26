"""
Health check endpoint.
"""
from fastapi import APIRouter, Request

from app.rate_limiter import limiter

router = APIRouter()


@router.get("/health")
@limiter.limit("30/minute")
def health(request: Request):
    return {"ok": True}

