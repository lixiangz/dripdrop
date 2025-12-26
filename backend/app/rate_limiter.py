"""
Rate limiting configuration for API endpoints.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

from core.config import get_env

# Initialize rate limiter
# Default: 10 requests per minute per IP address
# Can be overridden with RATE_LIMIT_PER_MINUTE environment variable
rate_limit_per_minute = int(get_env("RATE_LIMIT_PER_MINUTE", "10"))
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{rate_limit_per_minute}/minute"],
    storage_uri="memory://",  # In-memory storage (use Redis for distributed systems)
)

