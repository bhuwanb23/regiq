#!/usr/bin/env python3
"""
REGIQ AI/ML - FastAPI Main Application
Main entry point for the FastAPI application.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Import routers
from services.api.routers import health, auth
from services.api.routers.regulatory_intelligence import main as regulatory_intelligence_router
from services.api.routers.bias_analysis import main as bias_analysis_router
from services.api.routers.risk_simulator import main as risk_simulator_router
from services.api.routers.report_generator import main as report_generator_router
from services.api.routers.data_pipeline import main as data_pipeline_router

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

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(regulatory_intelligence_router.router)
app.include_router(bias_analysis_router.router)
app.include_router(risk_simulator_router.router)
app.include_router(report_generator_router.router)
app.include_router(data_pipeline_router.router)

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
        "services.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )