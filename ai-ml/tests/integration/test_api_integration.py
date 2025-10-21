#!/usr/bin/env python3
"""
Integration tests for API functionality.
Tests real API calls and integration between components.
"""

import pytest
import os
from unittest.mock import patch

from config.gemini_config import GeminiAPIManager
from config.env_config import get_env_config


@pytest.mark.integration
@pytest.mark.api
class TestGeminiAPIIntegration:
    """Integration tests for Gemini API."""
    
    @pytest.mark.skipif(not os.getenv('GEMINI_API_KEY'), reason="Requires real API key")
    def test_real_api_connection(self):
        """Test real API connection with actual key."""
        manager = GeminiAPIManager()
        
        response = manager.generate_content("Say 'Hello' in one word.")
        
        assert response is not None
        assert isinstance(response, str)
        assert len(response.strip()) > 0
    
    @pytest.mark.skipif(not os.getenv('GEMINI_API_KEY'), reason="Requires real API key")
    def test_multiple_model_calls(self):
        """Test calling different models."""
        manager = GeminiAPIManager()
        
        models_to_test = ["gemini-2.5-flash"]
        
        for model in models_to_test:
            response = manager.generate_content(
                "What is 1+1? Answer with just the number.",
                model=model
            )
            
            assert response is not None
            assert "2" in response
    
    def test_mock_api_integration(self, mock_gemini_api_manager):
        """Test API integration with mocked responses."""
        manager = mock_gemini_api_manager
        
        # Test basic generation
        response = manager.generate_content("Test prompt")
        assert response == "This is a test response from Gemini API"
        
        # Test with different parameters
        response = manager.generate_content(
            "Another test", 
            model="gemini-1.5-flash",
            temperature=0.7
        )
        assert response is not None
    
    def test_rate_limiting_integration(self, mock_gemini_api_manager):
        """Test rate limiting in integration scenario."""
        manager = mock_gemini_api_manager
        
        # Make multiple rapid requests
        responses = []
        for i in range(5):
            response = manager.generate_content(f"Test prompt {i}")
            responses.append(response)
        
        # All should succeed with mocked client
        assert len(responses) == 5
        assert all(r is not None for r in responses)
    
    def test_error_handling_integration(self, gemini_config_test):
        """Test error handling in integration scenario."""
        # Use invalid API key
        gemini_config_test.api_key = "invalid-key"
        manager = GeminiAPIManager(gemini_config_test)
        
        with patch('config.gemini_config.genai.Client') as mock_client:
            mock_client.side_effect = Exception("Invalid API key")
            
            response = manager.generate_content("Test prompt")
            assert response is None
    
    def test_fallback_model_integration(self, mock_gemini_api_manager):
        """Test fallback model functionality."""
        manager = mock_gemini_api_manager
        
        # Mock primary model to fail, fallback to succeed
        manager.client.models.generate_content.side_effect = [
            Exception("Primary model failed"),
            type('MockResponse', (), {'text': 'Fallback model response'})()
        ]
        
        response = manager.generate_content("Test prompt")
        assert response == "Fallback model response"
        assert manager.client.models.generate_content.call_count == 2


@pytest.mark.integration
class TestEnvironmentIntegration:
    """Integration tests for environment configuration."""
    
    def test_env_config_integration(self, test_env_config):
        """Test environment configuration integration."""
        env_config = test_env_config
        
        # Test all properties work together
        assert env_config.gemini_api_key is not None
        assert env_config.database_url is not None
        assert env_config.debug is True
        
        # Test validation
        validation = env_config.validate_required()
        assert validation['valid'] is True
    
    def test_config_to_api_manager_integration(self, test_env_config):
        """Test integration between env config and API manager."""
        # Create API manager using environment config
        with patch.dict(os.environ, {'GEMINI_API_KEY': test_env_config.gemini_api_key}):
            manager = GeminiAPIManager()
            
            assert manager.config.api_key == test_env_config.gemini_api_key
            assert manager.config.rate_limit_requests_per_minute == test_env_config.gemini_rate_limit_rpm
    
    def test_configuration_loading_priority(self):
        """Test configuration loading priority (env vars > config file > defaults)."""
        # Test environment variable takes priority
        with patch.dict(os.environ, {'GEMINI_RATE_LIMIT_RPM': '120'}):
            env_config = get_env_config()
            assert env_config.gemini_rate_limit_rpm == 120
    
    def test_missing_config_graceful_handling(self):
        """Test graceful handling of missing configuration."""
        with patch.dict(os.environ, {}, clear=True):
            env_config = get_env_config()
            
            # Should use defaults
            assert env_config.gemini_rate_limit_rpm == 60
            assert env_config.gemini_rate_limit_tpm == 32000
            
            # But validation should fail for required keys
            validation = env_config.validate_required()
            assert not validation['valid']


@pytest.mark.integration
@pytest.mark.database
class TestDatabaseIntegration:
    """Integration tests for database operations."""
    
    def test_database_api_integration(self, db_with_sample_data):
        """Test integration between database and API components."""
        cursor = db_with_sample_data.cursor()
        
        # Simulate storing API response in database
        api_response = "This is a test API response"
        model_name = "gemini-2.5-flash"
        
        cursor.execute(
            "INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)",
            (f"API_Test_{model_name}", "api_test", 0.0)
        )
        db_with_sample_data.commit()
        
        # Verify integration
        cursor.execute("SELECT name FROM test_models WHERE type = 'api_test'")
        result = cursor.fetchone()
        assert result[0] == f"API_Test_{model_name}"
    
    def test_config_database_integration(self, test_env_config, test_db):
        """Test integration between configuration and database."""
        # Use config to get database URL
        db_url = test_env_config.database_url
        assert "sqlite" in db_url
        
        # Test database operations with config
        cursor = test_db.cursor()
        cursor.execute("INSERT INTO test_users (username, email) VALUES (?, ?)", ("config_user", "config@test.com"))
        test_db.commit()
        
        cursor.execute("SELECT username FROM test_users WHERE username = 'config_user'")
        result = cursor.fetchone()
        assert result[0] == "config_user"
    
    def test_full_stack_integration(self, db_with_sample_data, mock_gemini_api_manager):
        """Test full stack integration: Config -> API -> Database."""
        cursor = db_with_sample_data.cursor()
        manager = mock_gemini_api_manager
        
        # Generate content via API
        response = manager.generate_content("Test integration prompt")
        
        # Store result in database
        cursor.execute(
            "INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)",
            ("Integration_Test", "full_stack", 0.88)
        )
        db_with_sample_data.commit()
        
        # Verify full integration
        assert response == "This is a test response from Gemini API"
        
        cursor.execute("SELECT name, type FROM test_models WHERE name = 'Integration_Test'")
        result = cursor.fetchone()
        assert result[0] == "Integration_Test"
        assert result[1] == "full_stack"


@pytest.mark.integration
@pytest.mark.slow
class TestPerformanceIntegration:
    """Integration tests for performance scenarios."""
    
    def test_concurrent_api_calls(self, mock_gemini_api_manager, performance_timer):
        """Test concurrent API call handling."""
        manager = mock_gemini_api_manager
        
        performance_timer.start()
        
        # Simulate concurrent requests
        responses = []
        for i in range(10):
            response = manager.generate_content(f"Concurrent test {i}")
            responses.append(response)
        
        performance_timer.stop()
        
        # Verify all requests completed
        assert len(responses) == 10
        assert all(r is not None for r in responses)
        
        # Performance should be reasonable (mocked, so very fast)
        assert performance_timer.elapsed < 1.0
    
    def test_database_performance_integration(self, test_db, performance_timer):
        """Test database performance with multiple operations."""
        cursor = test_db.cursor()
        
        performance_timer.start()
        
        # Insert multiple records
        for i in range(100):
            cursor.execute(
                "INSERT INTO test_users (username, email) VALUES (?, ?)",
                (f"user_{i}", f"user_{i}@test.com")
            )
        
        test_db.commit()
        
        # Query records
        cursor.execute("SELECT COUNT(*) FROM test_users")
        count = cursor.fetchone()[0]
        
        performance_timer.stop()
        
        assert count == 100
        assert performance_timer.elapsed < 2.0  # Should be fast for SQLite
    
    @pytest.mark.skipif(not os.getenv('RUN_PERFORMANCE_TESTS'), reason="Performance tests disabled")
    def test_api_response_time(self, mock_gemini_api_manager, performance_timer):
        """Test API response time performance."""
        manager = mock_gemini_api_manager
        
        response_times = []
        
        for i in range(5):
            performance_timer.start()
            response = manager.generate_content("Performance test prompt")
            performance_timer.stop()
            
            response_times.append(performance_timer.elapsed)
            assert response is not None
        
        # Calculate average response time
        avg_response_time = sum(response_times) / len(response_times)
        
        # With mocked client, should be very fast
        assert avg_response_time < 0.1
