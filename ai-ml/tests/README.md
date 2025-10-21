# 🧪 REGIQ AI/ML Testing Framework

Comprehensive testing framework for the REGIQ AI/ML system with unit tests, integration tests, end-to-end tests, and performance benchmarks.

## 📁 **Test Structure**

```
tests/
├── unit/                    # Unit tests (fast, isolated)
│   ├── test_config.py      # Configuration module tests
│   └── test_database.py    # Database operation tests
├── integration/             # Integration tests (external dependencies)
│   └── test_api_integration.py  # API integration tests
├── e2e/                    # End-to-end tests (full workflows)
│   └── test_end_to_end.py  # Complete system workflows
├── performance/            # Performance and load tests
│   └── test_benchmarks.py  # Performance benchmarks
├── conftest.py            # Global test configuration and fixtures
└── README.md              # This file
```

## 🚀 **Quick Start**

### **Install Test Dependencies**
```bash
pip install pytest pytest-cov pytest-asyncio pytest-mock
```

### **Run Tests**
```bash
# Quick tests (recommended for development)
python run_tests.py --suite quick

# All tests with coverage
python run_tests.py --suite all

# Specific test suites
python run_tests.py --suite unit
python run_tests.py --suite integration
python run_tests.py --suite e2e
```

## 🎯 **Test Categories**

### **📋 Unit Tests (`tests/unit/`)**
- **Fast and isolated** tests for individual components
- **No external dependencies** (database, API calls)
- **Mock all external services**
- **Run frequently** during development

**Examples:**
- Configuration loading and validation
- Database schema and operations
- Utility functions and helpers

### **🔗 Integration Tests (`tests/integration/`)**
- **Test component interactions**
- **May use external services** (with mocking when needed)
- **Test API integrations** and data flow
- **Slower than unit tests**

**Examples:**
- Gemini API integration
- Database integration with configuration
- Environment configuration integration

### **🌐 End-to-End Tests (`tests/e2e/`)**
- **Complete user workflows**
- **Full system integration**
- **Real-world scenarios**
- **Slowest but most comprehensive**

**Examples:**
- Complete setup workflow
- User registration and model analysis
- Report generation workflow

### **⚡ Performance Tests (`tests/performance/`)**
- **Performance benchmarks**
- **Load testing**
- **Memory usage testing**
- **Stress testing**

**Examples:**
- API call performance
- Database operation benchmarks
- Concurrent request handling

## 🏷️ **Test Markers**

Tests are automatically marked based on location and content:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests  
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.api` - API-related tests
- `@pytest.mark.database` - Database tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.smoke` - Basic functionality tests

### **Run Tests by Marker**
```bash
# Run only API tests
pytest -m api

# Run only fast tests
pytest -m "not slow"

# Run database tests
pytest -m database
```

## 🔧 **Test Configuration**

### **pytest.ini**
Main pytest configuration with:
- Test discovery settings
- Coverage configuration
- Marker definitions
- Output formatting

### **conftest.py**
Global test fixtures and configuration:
- Environment setup
- Database fixtures
- API mocking
- Performance utilities

## 📊 **Fixtures Available**

### **Environment Fixtures**
- `test_env_config` - Test environment configuration
- `mock_env_vars` - Mock environment variables

### **Database Fixtures**
- `test_db` - Clean test database
- `db_with_sample_data` - Database with sample data
- `test_db_path` - Test database file path

### **API Fixtures**
- `mock_gemini_client` - Mocked Gemini API client
- `gemini_config_test` - Test Gemini configuration
- `mock_gemini_api_manager` - Complete mocked API manager

### **Utility Fixtures**
- `temp_file` - Temporary file for testing
- `temp_dir` - Temporary directory
- `sample_test_data` - Sample data for tests
- `performance_timer` - Performance timing utility

## 🎮 **Running Tests**

### **Using Test Runner**
```bash
# Quick development tests
python run_tests.py --suite quick

# All tests with coverage
python run_tests.py --suite all --coverage

# Specific suites
python run_tests.py --suite unit
python run_tests.py --suite integration
python run_tests.py --suite e2e
python run_tests.py --suite performance
```

### **Using pytest Directly**
```bash
# Basic test run
pytest

# With coverage
pytest --cov=config --cov=services --cov-report=html

# Specific directory
pytest tests/unit/

# Specific test file
pytest tests/unit/test_config.py

# Specific test function
pytest tests/unit/test_config.py::TestEnvironmentConfig::test_gemini_api_key_property

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run in parallel (requires pytest-xdist)
pytest -n auto
```

## 📈 **Coverage Reports**

### **Generate Coverage Report**
```bash
pytest --cov=config --cov=services --cov-report=html --cov-report=term
```

### **View HTML Coverage Report**
```bash
# Coverage report will be in htmlcov/index.html
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

## 🔍 **Test Development Guidelines**

### **Writing Unit Tests**
```python
import pytest
from unittest.mock import Mock, patch

class TestMyComponent:
    def test_basic_functionality(self):
        # Arrange
        component = MyComponent()
        
        # Act
        result = component.do_something()
        
        # Assert
        assert result is not None
    
    def test_with_mock(self, mock_external_service):
        # Use fixtures for mocking
        component = MyComponent(mock_external_service)
        result = component.call_external()
        assert result == "mocked_response"
```

### **Writing Integration Tests**
```python
@pytest.mark.integration
class TestAPIIntegration:
    def test_real_api_call(self, mock_gemini_api_manager):
        # Test with mocked external services
        response = mock_gemini_api_manager.generate_content("test")
        assert response is not None
    
    @pytest.mark.skipif(not os.getenv('GEMINI_API_KEY'), reason="Requires API key")
    def test_with_real_api(self):
        # Test with real API (when available)
        manager = GeminiAPIManager()
        response = manager.generate_content("test")
        assert response is not None
```

### **Writing Performance Tests**
```python
@pytest.mark.performance
class TestPerformance:
    def test_response_time(self, performance_timer):
        performance_timer.start()
        # ... perform operation
        performance_timer.stop()
        
        assert performance_timer.elapsed < 1.0  # Should complete in under 1 second
```

## 🚨 **Test Environment Variables**

Set these environment variables for testing:

```bash
# Required for API tests
GEMINI_API_KEY=your-test-api-key

# Optional test configuration
TESTING=true
RUN_PERFORMANCE_TESTS=1  # Enable performance tests
LOG_LEVEL=DEBUG
```

## 📋 **Test Checklist**

Before committing code, ensure:

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Code coverage is above 80%
- [ ] No test warnings or errors
- [ ] Performance tests don't show regressions
- [ ] New features have corresponding tests

## 🐛 **Debugging Tests**

### **Run Single Test with Debug**
```bash
pytest tests/unit/test_config.py::TestEnvironmentConfig::test_gemini_api_key_property -v -s
```

### **Use pytest debugger**
```python
def test_something():
    import pytest
    pytest.set_trace()  # Debugger breakpoint
    # ... test code
```

### **Print debugging**
```bash
pytest -s  # Don't capture stdout
```

## 📚 **Additional Resources**

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## 🎯 **Next Steps**

1. **Run the test suite**: `python run_tests.py --suite quick`
2. **Check coverage**: `python run_tests.py --suite all --coverage`
3. **Add tests for new features** as you develop them
4. **Run tests before committing** code changes

**Happy Testing! 🧪✨**
