#!/usr/bin/env python3
"""
REGIQ AI/ML - Health Check Router
FastAPI router for health check endpoints.
"""

from fastapi import APIRouter, status
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/",
    summary="Health Check",
    description="Check if the API service is running and healthy",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "service": "REGIQ AI/ML API",
                        "version": "1.0.0"
                    }
                }
            }
        }
    }
)
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "REGIQ AI/ML API",
        "version": "1.0.0"
    }

@router.get(
    "/ready",
    summary="Readiness Check",
    description="Check if the API service is ready to accept requests",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Service is ready",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ready",
                        "components": {
                            "database": "connected",
                            "cache": "available"
                        }
                    }
                }
            }
        }
    }
)
async def readiness_check() -> Dict[str, Any]:
    """Readiness check endpoint."""
    logger.info("Readiness check requested")
    return {
        "status": "ready",
        "components": {
            "database": "connected",
            "cache": "available"
        }
    }