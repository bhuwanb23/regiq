#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 6.1 API Demo Test
Demo test showing API functionality.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def test_api_demo():
    """Demo test showing API functionality."""
    try:
        # Import the FastAPI app
        from services.api.main import app
        
        # Test that the app was created successfully
        assert app is not None
        assert app.title == "REGIQ AI/ML API"
        
        # Test that routes are registered
        route_paths = [getattr(route, 'path', '') for route in app.routes]
        
        # Check for key routes
        assert "/" in route_paths  # Root endpoint
        assert "/health/" in route_paths  # Health check
        assert "/health/ready" in route_paths  # Readiness check
        assert "/auth/token" in route_paths  # Login endpoint
        assert "/auth/register" in route_paths  # Registration endpoint
        
        # Test authentication functionality
        from services.api.auth.jwt_handler import create_access_token, verify_token, hash_password, verify_password
        
        # Test password hashing
        password = "demo_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)
        
        # Test JWT token creation and verification
        user_data = {"sub": "demouser", "role": "user"}
        token = create_access_token(user_data)
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "demouser"
        assert payload["role"] == "user"
        
        print("✅ API Demo Test Passed!")
        print(f"   - API Title: {app.title}")
        print(f"   - API Version: {app.version}")
        print(f"   - Registered Routes: {len(route_paths)}")
        print(f"   - JWT Token Generated: {len(token)} characters")
        print("   - Authentication System: Working")
        
    except Exception as e:
        pytest.fail(f"API Demo Test failed: {e}")

if __name__ == "__main__":
    test_api_demo()
    print("🎉 All API functionality demonstrated successfully!")