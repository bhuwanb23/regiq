#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 6.1 API Functionality Tests
Tests for API functionality without running the server.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def test_health_endpoint():
    """Test health endpoint functionality."""
    try:
        from services.api.routers.health import health_check, readiness_check
        
        # Test health check
        # These are async functions, so we just verify they exist
        assert health_check is not None
        assert readiness_check is not None
        
    except Exception as e:
        pytest.fail(f"Health endpoint test failed: {e}")

def test_auth_functionality():
    """Test authentication functionality."""
    try:
        from services.api.auth.jwt_handler import create_access_token, verify_token, hash_password, verify_password
        
        # Test password hashing
        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)
        
        # Test JWT token creation and verification
        user_data = {"sub": "testuser", "role": "admin"}
        token = create_access_token(user_data)
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"
        assert payload["role"] == "admin"
        
    except Exception as e:
        pytest.fail(f"Auth functionality test failed: {e}")

def test_user_registration():
    """Test user registration functionality."""
    try:
        # We'll test this by importing and checking the function exists
        from services.api.routers.auth import router
        # Just verify the router was created successfully
        assert router is not None
        
    except Exception as e:
        pytest.fail(f"User registration test failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])