"""API Key Authentication Middleware for service-to-service communication"""
import logging
from fastapi import Request, HTTPException, status
import os

logger = logging.getLogger(__name__)

# Get the expected API key from environment variables
EXPECTED_API_KEY = os.getenv("SERVICE_API_KEY", "regiq_service_api_key_here_change_in_production")

async def api_key_auth_middleware(request: Request, call_next):
    """
    Middleware to validate API key for service-to-service communication.
    Allows JWT authentication to proceed if API key is not present.
    Skips authentication for health check and documentation endpoints.
    """
    # Skip authentication for certain endpoints
    skip_paths = ["/health", "/docs", "/redoc", "/openapi.json"]
    if any(request.url.path.startswith(path) for path in skip_paths):
        response = await call_next(request)
        return response
    
    # Get the authorization header
    auth_header = request.headers.get("Authorization")
    
    # If no auth header, let JWT authentication handle it
    if not auth_header:
        response = await call_next(request)
        return response
    
    # If it's a Bearer token, check if it's an API key
    if auth_header.startswith("Bearer "):
        # Extract the token
        token = auth_header[7:]  # Remove "Bearer " prefix
        
        # If it matches our expected API key, allow the request
        if token == EXPECTED_API_KEY:
            logger.info(f"API key validated for {request.url.path}")
            response = await call_next(request)
            return response
        
        # If it doesn't match our API key, let JWT authentication handle it
        response = await call_next(request)
        return response
    
    # For other auth types, let JWT authentication handle it
    response = await call_next(request)
    return response