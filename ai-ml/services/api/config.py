#!/usr/bin/env python3
"""
REGIQ AI/ML - API Configuration
Configuration settings for the FastAPI application.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"

# Security Settings
SECRET_KEY = os.getenv("SECRET_KEY", "regiq-ai-ml-secret-key-for-development-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# CORS Settings
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# Database Settings (if needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../data/regiq.db")

# Logging Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class Settings:
    """API settings class."""
    
    # API Settings
    host: str = API_HOST
    port: int = API_PORT
    debug: bool = API_DEBUG
    
    # Security Settings
    secret_key: str = SECRET_KEY
    algorithm: str = ALGORITHM
    access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire_days: int = REFRESH_TOKEN_EXPIRE_DAYS
    
    # CORS Settings
    allowed_origins: list = ALLOWED_ORIGINS
    
    # Database Settings
    database_url: str = DATABASE_URL
    
    # Logging Settings
    log_level: str = LOG_LEVEL

settings = Settings()