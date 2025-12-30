# ruff: noqa: B008, D417
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from src.api.schemas import (
    HealthCheckResponse
)

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> Any:
    """Health check endpoint.

    Returns:
        HealthCheckResponse: The status of the health check.
    """
    return {"status": "ok"}

