"""
test_mcp.py

version : 1.2.0
author  : aumezawa
"""

import argparse

import httpx
from loguru import logger

from src.libs.logger import setup_logger

setup_logger()


def mcp_client(*, protocol: str = "http", address: str = "localhost", port: str = "3000") -> None:
    """Test MCP Server."""
    res = httpx.post(
        url=f"{protocol}://{address}:{port}/mcp/",
        headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "capabilities": {"tools": {}, "prompts": {}},
                "clientInfo": {"name": "ExampleClient", "version": "1.0"},
            },
        },
    )
    if not res.is_success:
        logger.error(f"Error: {res.status_code} - {res.text}")
        return
    logger.info(f"Response: {res.text}")

    res = httpx.post(
        url=f"{protocol}://{address}:{port}/mcp/",
        headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "mcp-session-id": res.headers.get("mcp-session-id"),
        },
        json={
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        },
    )
    if not res.is_success:
        logger.error(f"Error: {res.status_code} - {res.text}")
        return

    res = httpx.post(
        url=f"{protocol}://{address}:{port}/mcp/",
        headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "mcp-session-id": res.headers.get("mcp-session-id"),
        },
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
        },
    )
    if not res.is_success:
        logger.error(f"Error: {res.status_code} - {res.text}")
        return
    logger.info(f"Response: {res.text}")


if __name__ == "__main__":
    """Run MCP Client."""
    parser = argparse.ArgumentParser(description="Select to execute a test server.")
    parser.add_argument(
        "-s",
        "--server",
        default="localhost",
        help="Specify the IP address of the server.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default="3000",
        help="Specify the port of the server.",
    )
    args = parser.parse_args()

    mcp_client(
        address=args.server,
        port=args.port,
    )
