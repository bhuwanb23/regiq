#!/usr/bin/env python3
"""
REGIQ AI/ML pytest configuration and fixtures
Global test configuration, fixtures, and utilities.
"""

import os
import sys
import pytest
import sqlite3
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock, patch

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config.env_config import EnvironmentConfig
from config.gemini_config import GeminiAPIManager, GeminiConfig

# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Set testing environment
    os.environ['TESTING'] = 'true'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    
    # Ensure test directories exist
    test_dirs = [
        'data/test',
        'logs/test',
        'tmp/test'
    ]
    
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath) or "end_to_end" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        
        # Add markers based on test name
        if "test_api" in item.name or "gemini" in item.name:
            item.add_marker(pytest.mark.api)
        if "test_db" in item.name or "database" in item.name:
            item.add_marker(pytest.mark.database)
        if "performance" in item.name or "benchmark" in item.name:
            item.add_marker(pytest.mark.performance)

# =============================================================================
# ENVIRONMENT FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def test_env_config():
    """Provide test environment configuration."""
    # Create temporary .env file for testing
    test_env_content = """
TESTING=true
GEMINI_API_KEY=test-api-key-for-testing
DATABASE_URL=sqlite:///data/test_regiq.db
DEBUG=true
LOG_LEVEL=DEBUG
SECRET_KEY=test-secret-key-for-testing
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(test_env_content)
        temp_env_file = f.name
    
    try:
        # Load test environment
        env_config = EnvironmentConfig(temp_env_file)
        yield env_config
    finally:
        # Cleanup
        os.unlink(temp_env_file)

@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    test_vars = {
        'TESTING': 'true',
        'GEMINI_API_KEY': 'test-api-key',
        'DATABASE_URL': 'sqlite:///data/test_regiq.db',
        'DEBUG': 'true',
        'LOG_LEVEL': 'DEBUG'
    }
    
    with patch.dict(os.environ, test_vars):
        yield test_vars

# =============================================================================
# DATABASE FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def test_db_path():
    """Provide test database path."""
    db_path = Path("data/test_regiq.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    yield str(db_path)
    
    # Cleanup after all tests
    if db_path.exists():
        db_path.unlink()

@pytest.fixture
def test_db(test_db_path):
    """Provide clean test database for each test."""
    # Remove existing test database
    if Path(test_db_path).exists():
        Path(test_db_path).unlink()
    
    # Create fresh database with schema
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    
    # Create basic test tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            type VARCHAR(50),
            bias_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    
    yield conn
    
    # Cleanup
    conn.close()
    if Path(test_db_path).exists():
        Path(test_db_path).unlink()

@pytest.fixture
def db_with_sample_data(test_db):
    """Provide database with sample test data."""
    cursor = test_db.cursor()
    
    # Insert sample users
    sample_users = [
        ('testuser1', 'test1@example.com'),
        ('testuser2', 'test2@example.com'),
        ('testuser3', 'test3@example.com')
    ]
    
    cursor.executemany(
        "INSERT INTO test_users (username, email) VALUES (?, ?)",
        sample_users
    )
    
    # Insert sample models
    sample_models = [
        ('TestModel1', 'classification', 0.85),
        ('TestModel2', 'regression', 0.72),
        ('TestModel3', 'clustering', 0.91)
    ]
    
    cursor.executemany(
        "INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)",
        sample_models
    )
    
    test_db.commit()
    yield test_db

# =============================================================================
# API FIXTURES
# =============================================================================

@pytest.fixture
def mock_gemini_client():
    """Mock Gemini API client for testing."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.text = "This is a test response from Gemini API"
    
    mock_client.models.generate_content.return_value = mock_response
    
    yield mock_client

@pytest.fixture
def gemini_config_test():
    """Provide test Gemini configuration."""
    config = GeminiConfig(
        api_key="test-api-key",
        model_name="gemini-2.5-flash",
        fallback_model="gemini-1.5-flash",
        max_tokens=1000,
        temperature=0.3,
        rate_limit_requests_per_minute=10,  # Lower for testing
        rate_limit_tokens_per_minute=1000,
        timeout_seconds=10,
        max_retries=2,
        retry_delay=0.1  # Faster retries for testing
    )
    yield config

@pytest.fixture
def mock_gemini_api_manager(gemini_config_test, mock_gemini_client):
    """Mock Gemini API manager for testing."""
    with patch('config.gemini_config.genai.Client', return_value=mock_gemini_client):
        manager = GeminiAPIManager(gemini_config_test)
        manager.client = mock_gemini_client
        yield manager

# =============================================================================
# UTILITY FIXTURES
# =============================================================================

@pytest.fixture
def temp_file():
    """Provide temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def temp_dir():
    """Provide temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_path:
        yield Path(temp_path)

@pytest.fixture
def sample_test_data():
    """Provide sample test data."""
    return {
        'users': [
            {'id': 1, 'username': 'testuser1', 'email': 'test1@example.com'},
            {'id': 2, 'username': 'testuser2', 'email': 'test2@example.com'},
        ],
        'models': [
            {'id': 1, 'name': 'TestModel1', 'type': 'classification', 'bias_score': 0.85},
            {'id': 2, 'name': 'TestModel2', 'type': 'regression', 'bias_score': 0.72},
        ],
        'prompts': [
            "What is AI?",
            "Explain machine learning",
            "Define bias in AI models"
        ]
    }

# =============================================================================
# PERFORMANCE FIXTURES
# =============================================================================

@pytest.fixture
def performance_timer():
    """Timer fixture for performance testing."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    yield Timer()

# =============================================================================
# CLEANUP HOOKS
# =============================================================================

@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Automatically cleanup test files after each test."""
    yield
    
    # Cleanup patterns
    cleanup_patterns = [
        'data/test_*.db',
        'logs/test_*.log',
        'tmp/test_*'
    ]
    
    for pattern in cleanup_patterns:
        for file_path in Path('.').glob(pattern):
            try:
                file_path.unlink()
            except (OSError, PermissionError):
                pass  # Ignore cleanup errors

# =============================================================================
# SKIP CONDITIONS
# =============================================================================

def pytest_runtest_setup(item):
    """Setup conditions for running tests."""
    # Skip API tests if no real API key is available
    if item.get_closest_marker("api") and not os.getenv('GEMINI_API_KEY'):
        if not os.getenv('TESTING'):
            pytest.skip("API tests require GEMINI_API_KEY environment variable")
    
    # Skip performance tests in CI unless explicitly requested
    if item.get_closest_marker("performance"):
        if os.getenv('CI') and not os.getenv('RUN_PERFORMANCE_TESTS'):
            pytest.skip("Performance tests skipped in CI (set RUN_PERFORMANCE_TESTS=1 to enable)")

# =============================================================================
# CUSTOM ASSERTIONS
# =============================================================================

def assert_valid_response(response_text: str):
    """Assert that API response is valid."""
    assert response_text is not None
    assert isinstance(response_text, str)
    assert len(response_text.strip()) > 0
    assert "error" not in response_text.lower()

def assert_database_record_exists(cursor, table: str, **conditions):
    """Assert that database record exists with given conditions."""
    where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
    query = f"SELECT COUNT(*) FROM {table} WHERE {where_clause}"
    cursor.execute(query, list(conditions.values()))
    count = cursor.fetchone()[0]
    assert count > 0, f"No record found in {table} with conditions {conditions}"

# Add custom assertions to pytest namespace
pytest.assert_valid_response = assert_valid_response
pytest.assert_database_record_exists = assert_database_record_exists
