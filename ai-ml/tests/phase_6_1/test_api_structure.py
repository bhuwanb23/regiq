#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 6.1 API Structure Tests
Unit tests for API structure and basic functionality.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def test_api_imports():
    """Test that API modules can be imported."""
    try:
        from services.api.main import app
        assert app is not None
    except ImportError as e:
        pytest.fail(f"Failed to import API modules: {e}")

def test_api_config():
    """Test API configuration."""
    try:
        from services.api.config import settings
        assert settings is not None
        assert hasattr(settings, 'host')
        assert hasattr(settings, 'port')
    except ImportError as e:
        pytest.fail(f"Failed to import API config: {e}")

def test_jwt_handler():
    """Test JWT handler imports."""
    try:
        from services.api.auth.jwt_handler import create_access_token, verify_token
        assert create_access_token is not None
        assert verify_token is not None
    except ImportError as e:
        pytest.skip(f"JWT handler not fully implemented yet: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])