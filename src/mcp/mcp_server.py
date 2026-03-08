"""
mcp_server.py

version : 1.2.0
author  : aumezawa
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from fastmcp import FastMCP
from loguru import logger

from src.mcp.mcp_logger import LoggingMcpMiddleware
from src.mcp.mcp_tools import get_exchange_rate

try:
    with Path("pyproject.toml").open(mode="rb") as fp:
        pyproject = tomllib.load(fp)
except Exception as e:
    pyproject = {}
    logger.error(f"Could not read `pyproject.toml` file. e: {e}")

mcp = FastMCP(
    name=pyproject.get("project", {}).get("name") or "UNKNOW",
    instructions=pyproject.get("project", {}).get("description") or "UNKNOW",
    version=pyproject.get("project", {}).get("version") or "UNKNOW",
    auth=None,
    lifespan=None,
    tools=[get_exchange_rate],
    strict_input_validation=True,
)

mcp.add_middleware(LoggingMcpMiddleware())

mcp_app = mcp.http_app(
    path="/",
    transport="streamable-http",
)
