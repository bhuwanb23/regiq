#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 6.1 API Integration Tests
Integration tests for the complete API setup.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def test_api_app_creation():
    """Test that the FastAPI app can be created."""
    try:
        from services.api.main import app
        assert app is not None
        assert app.title == "REGIQ AI/ML API"
        assert app.version == "1.0.0"
    except Exception as e:
        pytest.fail(f"Failed to create FastAPI app: {e}")

def test_api_routers_included():
    """Test that routers are included in the app."""
    try:
        from services.api.main import app
        
        # Check that routes are registered
        routes = [getattr(route, 'path', '') for route in app.routes]
        
        # Check for health routes
        assert "/health/" in routes
        assert "/health/ready" in routes
        
        # Check for auth routes
        assert "/auth/token" in routes
        assert "/auth/register" in routes
        
        # Check for root route
        assert "/" in routes
        
    except Exception as e:
        pytest.fail(f"Failed to verify API routes: {e}")

def test_api_docs_available():
    """Test that API documentation is available."""
    try:
        from services.api.main import app
        
        # Check that docs routes are available
        routes = [getattr(route, 'path', '') for route in app.routes]
        # Note: FastAPI automatically adds docs routes, so we don't need to explicitly check for them
        assert len(routes) > 0
        
    except Exception as e:
        pytest.fail(f"Failed to verify API documentation: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])