"""
main.py

version : 1.0.0
author  : aumezawa
"""

from fastapi import FastAPI
from fastmcp import FastMCP

from src.libs.logger import setup_logger
from src.tools.currency_rate import get_exchange_rate

setup_logger(["uvicorn", "uvicorn.access"])


mcp = FastMCP(
    name="currency_rate",
    instructions="This MCP server provides the capability to exchange a currency rate to another currency.",
    version="1.0.0",
    auth=None,
    lifespan=None,
    tools=[get_exchange_rate],
    strict_input_validation=True,
)

mcp_app = mcp.http_app(
    path="/",
    transport="streamable-http",
)

app = FastAPI(lifespan=mcp_app.lifespan)
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
