"""
mcp_logger.py

version : 1.2.0
author  : aumezawa
"""

from __future__ import annotations

from typing import Any, override

from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from loguru import logger


class LoggingMcpMiddleware(Middleware):
    """MCP Middleware for Logging."""

    @override
    async def on_message(
        self,
        context: MiddlewareContext[Any],
        call_next: CallNext[Any, Any],
    ) -> Any:
        """Handle before and after an MCP request."""
        logger.debug(f"http headers: {get_http_headers()}, context: {context}")
        return await call_next(context)
