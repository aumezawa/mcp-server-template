"""
root.py

version : 1.2.0
author  : aumezawa
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Return root message."""
    return {"message": "Hello."}


@router.get("/health")
async def health() -> dict[str, str]:
    """Return health status."""
    return {"status": "green"}
