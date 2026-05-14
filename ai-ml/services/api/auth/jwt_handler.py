#!/usr/bin/env python3
"""
REGIQ AI/ML - JWT Handler
JWT token generation and validation utilities.
"""

import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt import PyJWTError
import bcrypt
import sys
from pathlib import Path
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.env_config import get_env_config

# Get configuration
config = get_env_config()
SECRET_KEY = config.get("JWT_SECRET_KEY", "regiq-ai-ml-secret-key-for-development-only") or "regiq-ai-ml-secret-key-for-development-only"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30") or "30")

# Service API key (matches services/api/middleware/api_key_auth.py).
# When the Node gateway calls FastAPI, it sends this key in the Authorization
# header. We accept it as a service-level principal so handlers protected by
# get_current_user still work for inter-service traffic.
SERVICE_API_KEY = os.getenv(
    "SERVICE_API_KEY",
    "regiq_service_api_key_here_change_in_production",
)

# OAuth2 scheme: auto_error=False so we can fall through to the service
# API key check when no JWT is supplied.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token", auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None

def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):
    """
    Resolve the current principal from the Bearer token.

    Accepts either:
      1. A valid user JWT (issued by `create_access_token`) — returns the JWT payload.
      2. The service API key (used by the Node API gateway for service-to-service
         calls) — returns a synthetic service principal so downstream handlers
         can rely on `current_user`.

    Raises 401 only if both checks fail.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    # 1) Service API key fast path (Node gateway → FastAPI).
    if token == SERVICE_API_KEY:
        return {
            "sub": "regiq-node-gateway",
            "role": "service",
            "is_service": True,
        }

    # 2) Otherwise, treat as a user JWT.
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    return payload

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))