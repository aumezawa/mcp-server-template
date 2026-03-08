"""
logger.py

version : 1.2.0
author  : aumezawa
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

if TYPE_CHECKING:
    from fastapi import Request, Response


class LoggingHttpMiddleware(BaseHTTPMiddleware):
    """HTTP Middleware for Logging."""

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Handle before and after a HTTP request."""
        body = await request.body()
        logger.debug(f"method: {request.method}, headers: {request.headers}, body: {body.decode()}")
        return await call_next(request)
