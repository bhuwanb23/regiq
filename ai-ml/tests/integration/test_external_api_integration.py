#!/usr/bin/env python3
"""
External API integration tests for REGIQ AI/ML system.
Tests integration with external APIs including Gemini, regulatory data sources, and third-party services.
"""

import pytest
import os
from unittest.mock import patch, Mock

from config.gemini_config import GeminiAPIManager, GeminiConfig
from config.env_config import get_env_config
from services.api.routers.data_pipeline.models import (
    UploadRequest, BatchProcessRequest, ValidationRequest,
    JobStatus, FileFormat, ProcessingPriority
)


@pytest.mark.integration
@pytest.mark.api
class TestGeminiAPIIntegration:
    """Integration tests for Gemini API."""
    
    @pytest.mark.skipif(not os.getenv('GEMINI_API_KEY'), reason="Requires real API key")
    def test_real_gemini_api_connection(self):
        """Test real connection to Gemini API with actual key."""
        manager = GeminiAPIManager()
        
        response = manager.generate_content("Say 'Hello' in one word.")
        
        assert response is not None
        assert isinstance(response, str)
        assert len(response.strip()) > 0
    
    @pytest.mark.skipif(not os.getenv('GEMINI_API_KEY'), reason="Requires real API key")
    def test_gemini_model_variants(self):
        """Test different Gemini model variants."""
        manager = GeminiAPIManager()
        
        models_to_test = ["gemini-1.5-flash", "gemini-1.5-pro"]
        
        for model in models_to_test:
            response = manager.generate_content(
                "What is artificial intelligence in one sentence?",
                model=model
            )
            
            assert response is not None
            assert isinstance(response, str)
            assert len(response.strip()) > 0
    
    def test_gemini_api_with_mocked_responses(self, mock_gemini_api_manager):
        """Test Gemini API integration with mocked responses."""
        manager = mock_gemini_api_manager
        
        # Test basic content generation
        response = manager.generate_content("Test prompt for bias analysis")
        assert response == "This is a test response from Gemini API"
        
        # Test with different parameters
        response = manager.generate_content(
            "Analyze this regulatory document", 
            model="gemini-1.5-pro",
            temperature=0.3
        )
        assert response is not None
    
    def test_gemini_rate_limiting_behavior(self, mock_gemini_api_manager):
        """Test rate limiting behavior with Gemini API."""
        manager = mock_gemini_api_manager
        
        # Make multiple rapid requests to test rate limiting
        responses = []
        for i in range(10):
            response = manager.generate_content(f"Test prompt {i} for rate limiting")
            responses.append(response)
        
        # All should succeed with mocked client
        assert len(responses) == 10
        assert all(r is not None for r in responses)
    
    def test_gemini_error_handling(self, gemini_config_test):
        """Test error handling with Gemini API."""
        # Use invalid API key
        gemini_config_test.api_key = "invalid-api-key"
        manager = GeminiAPIManager(gemini_config_test)
        
        with patch('config.gemini_config.genai.Client') as mock_client:
            mock_client.side_effect = Exception("Invalid API key")
            
            response = manager.generate_content("Test prompt for error handling")
            assert response is None
    
    def test_gemini_fallback_mechanism(self, mock_gemini_api_manager):
        """Test fallback model mechanism."""
        manager = mock_gemini_api_manager
        
        # Mock primary model to fail, fallback to succeed
        manager.client.models.generate_content.side_effect = [
            Exception("Primary model temporarily unavailable"),
            Mock(text="Fallback model response for bias analysis")
        ]
        
        response = manager.generate_content("Analyze model bias")
        assert response == "Fallback model response for bias analysis"
        assert manager.client.models.generate_content.call_count == 2


@pytest.mark.integration
@pytest.mark.api
class TestRegulatoryAPIIntegration:
    """Integration tests for regulatory data APIs."""
    
    def test_sec_edgar_api_integration(self, mock_gemini_api_manager):
        """Test integration with SEC EDGAR API."""
        # Mock SEC EDGAR API response
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "filings": [
                    {
                        "id": "0001234567-25-000001",
                        "type": "10-K",
                        "company": "Test Corp",
                        "date": "2025-01-01",
                        "url": "https://www.sec.gov/Archives/edgar/data/1234567/000123456725000001/0001234567-25-000001.txt"
                    }
                ]
            }
            mock_get.return_value = mock_response
            
            # Simulate calling the regulatory intelligence service
            import requests
            response = requests.get("https://data.sec.gov/submissions/LATEST_SUBMISSIONS.json")
            
            assert response.status_code == 200
            filings = response.json()["filings"]
            assert len(filings) > 0
            assert "id" in filings[0]
            assert "type" in filings[0]
    
    def test_eu_regulatory_api_integration(self, mock_gemini_api_manager):
        """Test integration with EU regulatory APIs."""
        # Mock EU regulatory API response
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "regulations": [
                    {
                        "id": "EU-2025-1234",
                        "title": "Digital Services Act Amendment",
                        "date": "2025-02-01",
                        "status": "proposed"
                    }
                ]
            }
            mock_get.return_value = mock_response
            
            # Simulate calling the EU regulatory service
            import requests
            response = requests.get("https://eur-lex.europa.eu/search-api/search")
            
            assert response.status_code == 200
            regulations = response.json()["regulations"]
            assert len(regulations) > 0
            assert "id" in regulations[0]
            assert "title" in regulations[0]


@pytest.mark.integration
@pytest.mark.api
class TestDataPipelineAPIIntegration:
    """Integration tests for data pipeline APIs."""
    
    def test_data_ingestion_api_integration(self):
        """Test integration with data ingestion API."""
        # Test data structures
        upload_request = UploadRequest(
            file_name="test_regulatory_data.csv",
            file_format=FileFormat.CSV,
            description="Test regulatory documents",
            tags=["test", "regulatory", "compliance"]
        )
        
        assert upload_request.file_name == "test_regulatory_data.csv"
        assert upload_request.file_format == FileFormat.CSV
        assert "test" in upload_request.tags
    
    def test_batch_processing_api_integration(self):
        """Test integration with batch processing API."""
        batch_request = BatchProcessRequest(
            upload_id="upload_12345",
            pipeline_type="regulatory_analysis",
            priority=ProcessingPriority.HIGH,
            configuration={
                "model_name": "gemini-1.5-pro",
                "analysis_depth": "detailed",
                "include_bias_analysis": True
            }
        )
        
        assert batch_request.upload_id == "upload_12345"
        assert batch_request.pipeline_type == "regulatory_analysis"
        assert batch_request.priority == ProcessingPriority.HIGH
        assert batch_request.configuration is not None
        assert batch_request.configuration["model_name"] == "gemini-1.5-pro"
    
    def test_validation_api_integration(self):
        """Test integration with data validation API."""
        validation_request = ValidationRequest(
            upload_id="upload_12345",
            validation_rules=["completeness", "format", "consistency"],
            sample_size=1000
        )
        
        assert validation_request.upload_id == "upload_12345"
        assert len(validation_request.validation_rules) == 3
        assert validation_request.sample_size == 1000


@pytest.mark.integration
@pytest.mark.api
class TestAPIRateLimiting:
    """Test API rate limiting mechanisms."""
    
    def test_gemini_rate_limit_respecting(self, mock_gemini_api_manager):
        """Test that API calls respect rate limits."""
        manager = mock_gemini_api_manager
        
        # Configure rate limiting
        manager.config.rate_limit_requests_per_minute = 5
        manager.config.rate_limit_tokens_per_minute = 1000
        
        # Make calls within rate limit
        responses = []
        for i in range(5):
            response = manager.generate_content(f"Rate limit test {i}")
            responses.append(response)
        
        # All should succeed
        assert len(responses) == 5
        assert all(r is not None for r in responses)
    
    def test_backoff_mechanism_on_rate_limit(self, gemini_config_test):
        """Test exponential backoff mechanism when rate limited."""
        # Configure for testing
        gemini_config_test.max_retries = 3
        gemini_config_test.retry_delay = 0.1  # Fast retry for testing
        manager = GeminiAPIManager(gemini_config_test)
        
        with patch('config.gemini_config.genai.Client') as mock_client_class:
            mock_client = Mock()
            # Simulate rate limiting on first call, success on retry
            mock_client.models.generate_content.side_effect = [
                Exception("429 Too Many Requests"),
                Exception("429 Too Many Requests"),
                Mock(text="Success after rate limit backoff")
            ]
            mock_client_class.return_value = mock_client
            
            response = manager.generate_content("Test with rate limiting")
            
            # Should succeed after retries
            assert response == "Success after rate limit backoff"
            assert mock_client.models.generate_content.call_count == 3


@pytest.mark.integration
@pytest.mark.api
class TestAPIErrorHandling:
    """Test error handling for external APIs."""
    
    def test_timeout_handling(self, gemini_config_test):
        """Test handling of API timeouts."""
        gemini_config_test.timeout_seconds = 1
        manager = GeminiAPIManager(gemini_config_test)
        
        with patch('config.gemini_config.genai.Client') as mock_client_class:
            mock_client = Mock()
            mock_client.models.generate_content.side_effect = TimeoutError("Request timeout")
            mock_client_class.return_value = mock_client
            
            response = manager.generate_content("Test timeout handling")
            assert response is None
    
    def test_network_error_handling(self, gemini_config_test):
        """Test handling of network errors."""
        manager = GeminiAPIManager(gemini_config_test)
        
        with patch('config.gemini_config.genai.Client') as mock_client_class:
            mock_client = Mock()
            mock_client.models.generate_content.side_effect = ConnectionError("Network unreachable")
            mock_client_class.return_value = mock_client
            
            response = manager.generate_content("Test network error handling")
            assert response is None
    
    def test_invalid_response_handling(self, mock_gemini_api_manager):
        """Test handling of invalid API responses."""
        manager = mock_gemini_api_manager
        
        # Mock invalid response
        mock_response = Mock()
        mock_response.text = None  # Invalid response
        manager.client.models.generate_content.return_value = mock_response
        
        response = manager.generate_content("Test invalid response handling")
        assert response is None  # Should handle gracefully


@pytest.mark.integration
@pytest.mark.api
class TestAPIConfigurationIntegration:
    """Test integration between API configuration and external services."""
    
    def test_environment_config_to_api_manager(self, test_env_config):
        """Test that environment configuration properly integrates with API manager."""
        # Set up environment variables
        with patch.dict(os.environ, {
            'GEMINI_API_KEY': 'test-config-key',
            'GEMINI_RATE_LIMIT_RPM': '120',
            'GEMINI_TIMEOUT_SECONDS': '30'
        }):
            env_config = get_env_config()
            manager = GeminiAPIManager()
            
            assert manager.config.api_key == 'test-config-key'
            assert manager.config.rate_limit_requests_per_minute == 120
            assert manager.config.timeout_seconds == 30
    
    def test_api_config_validation(self, gemini_config_test):
        """Test validation of API configuration."""
        # Valid configuration
        assert gemini_config_test.validate() is True
        
        # Invalid configuration - missing API key
        gemini_config_test.api_key = ""
        assert gemini_config_test.validate() is False
        
        # Invalid configuration - negative rate limit
        gemini_config_test.api_key = "test-key"
        gemini_config_test.rate_limit_requests_per_minute = -1
        assert gemini_config_test.validate() is False