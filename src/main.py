"""
main.py

version : 1.1.0
author  : aumezawa
"""

from __future__ import annotations

from typing import Any, override

from fastapi import FastAPI, Request, Response
from fastmcp import FastMCP
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.libs.logger import setup_logger
from src.tools.currency_rate import get_exchange_rate

setup_logger(["uvicorn", "uvicorn.access"])


class CustomMcpMiddleware(Middleware):
    """Custom MCP Middleware Class."""

    @override
    async def on_message(
        self,
        context: MiddlewareContext[Any],
        call_next: CallNext[Any, Any],
    ) -> Any:
        """Handle before and after an MCP request."""
        logger.debug(f"context: {context}")
        return await call_next(context)


class CustomHttpMiddleware(BaseHTTPMiddleware):
    """Custom HTTP Middleware Class."""

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Handle before and after a HTTP request."""
        body = await request.body()
        logger.debug(f"method: {request.method}, headers: {request.headers}, body: {body.decode()}")
        return await call_next(request)


mcp = FastMCP(
    name="currency_rate",
    instructions="This MCP server provides the capability to exchange a currency rate to another currency.",
    version="1.0.0",
    auth=None,
    lifespan=None,
    tools=[get_exchange_rate],
    strict_input_validation=True,
)

mcp.add_middleware(CustomMcpMiddleware())

mcp_app = mcp.http_app(
    path="/",
    transport="streamable-http",
)

app = FastAPI(lifespan=mcp_app.lifespan)
app.add_middleware(CustomHttpMiddleware)
app.mount("/mcp", mcp_app)


@app.get("/")
async def root() -> dict[str, str]:
    """Return hello."""
    return {"message": "Hello."}


@app.get("/health")
async def health() -> dict[str, str]:
    """Return health status."""
    return {"status": "healthy"}


@app.get("/status")
async def status() -> dict[str, str]:
    """Return server status."""
    return {"status": "running"}
