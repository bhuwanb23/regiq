#!/usr/bin/env python3
"""
REGIQ AI/ML - Authentication Router
FastAPI router for authentication endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any
from datetime import timedelta
import logging

from services.api.auth.jwt_handler import create_access_token, verify_password, hash_password
from ..config import settings

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

# Simple in-memory user storage for demonstration
# In production, this would be a database
users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": hash_password("admin123"),
        "role": "admin"
    },
    "user": {
        "username": "user",
        "hashed_password": hash_password("user123"),
        "role": "user"
    }
}

@router.post(
    "/token",
    summary="Login",
    description="Authenticate user and get access token",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Access token generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {"description": "Incorrect username or password"}
    }
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    """Login endpoint to get access token."""
    logger.info(f"Login attempt for user: {form_data.username}")
    
    # Check if user exists
    user = users_db.get(form_data.username)
    if not user:
        logger.warning(f"Login failed - user not found: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user["hashed_password"]):
        logger.warning(f"Login failed - invalid password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    logger.info(f"Login successful for user: {form_data.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post(
    "/register",
    summary="Register User",
    description="Register a new user account",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "username": "newuser",
                        "role": "user",
                        "message": "User created successfully"
                    }
                }
            }
        },
        400: {"description": "Username already exists"}
    }
)
async def register_user(username: str, password: str, role: str = "user") -> Dict[str, Any]:
    """Register a new user."""
    logger.info(f"Registration attempt for user: {username}")
    
    # Check if user already exists
    if username in users_db:
        logger.warning(f"Registration failed - username already exists: {username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    # Create new user
    hashed_password = hash_password(password)
    users_db[username] = {
        "username": username,
        "hashed_password": hashed_password,
        "role": role
    }
    
    logger.info(f"User registered successfully: {username}")
    return {
        "username": username,
        "role": role,
        "message": "User created successfully"
    }