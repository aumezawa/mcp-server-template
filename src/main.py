"""
main.py

version : 1.2.0
author  : aumezawa
"""

from __future__ import annotations

from fastapi import FastAPI

from src.libs.logger import setup_logger
from src.mcp.mcp_server import mcp_app
from src.middlewares.logger import LoggingHttpMiddleware
from src.routes import root

setup_logger(["uvicorn", "uvicorn.access"])


app = FastAPI(lifespan=mcp_app.lifespan)
app.add_middleware(LoggingHttpMiddleware)

app.mount("/mcp", mcp_app)
app.include_router(root.router)
