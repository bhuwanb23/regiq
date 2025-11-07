#!/usr/bin/env python3
"""
REGIQ AI/ML - FastAPI Main Application
Main entry point for the FastAPI application.
"""

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting REGIQ AI/ML API Server")
    
    # Initialize services here if needed
    # For example: database connections, cache initialization, etc.
    
    yield
    
    # Shutdown
    logger.info("Shutting down REGIQ AI/ML API Server")
    
    # Cleanup resources here if needed
    # For example: close database connections, cleanup cache, etc.

# Create FastAPI app with lifespan
app = FastAPI(
    title="REGIQ AI/ML API",
    description="API for REGIQ AI Compliance Copilot - Fintech Regulatory Intelligence, Bias Analysis, and Risk Simulation",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "REGIQ AI/ML API"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to REGIQ AI/ML API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )