#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 6.1 Authentication Tests
Unit tests for authentication endpoints.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def test_auth_router_imports():
    """Test that auth router can be imported."""
    try:
        from services.api.routers.auth import router
        assert router is not None
    except ImportError as e:
        pytest.fail(f"Failed to import auth router: {e}")

def test_health_router_imports():
    """Test that health router can be imported."""
    try:
        from services.api.routers.health import router
        assert router is not None
    except ImportError as e:
        pytest.fail(f"Failed to import health router: {e}")

def test_jwt_functions():
    """Test JWT functions."""
    try:
        from services.api.auth.jwt_handler import create_access_token, verify_token, hash_password, verify_password
        
        # Test password hashing
        password = "test_password"
        hashed = hash_password(password)
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)
        
        # Test token creation and verification
        data = {"sub": "test_user", "role": "user"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
        
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "test_user"
        assert payload["role"] == "user"
        
    except Exception as e:
        pytest.fail(f"JWT functions test failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])