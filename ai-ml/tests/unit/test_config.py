#!/usr/bin/env python3
"""
Unit tests for configuration modules.
Tests environment configuration and Gemini API configuration.
"""

import pytest
import os
from unittest.mock import patch, Mock

from config.env_config import EnvironmentConfig, get_env_config
from config.gemini_config import GeminiConfig, GeminiAPIManager


class TestEnvironmentConfig:
    """Test cases for EnvironmentConfig class."""
    
    def test_environment_config_initialization(self, mock_env_vars):
        """Test environment configuration initialization."""
        env_config = EnvironmentConfig()
        
        assert env_config.gemini_api_key == "test-api-key"
        assert env_config.debug is True
        assert env_config.log_level == "DEBUG"
    
    def test_gemini_api_key_property(self, mock_env_vars):
        """Test Gemini API key property."""
        env_config = EnvironmentConfig()
        assert env_config.gemini_api_key == "test-api-key"
    
    def test_database_url_property(self, mock_env_vars):
        """Test database URL property."""
        env_config = EnvironmentConfig()
        assert "sqlite" in env_config.database_url
    
    def test_rate_limiting_properties(self, mock_env_vars):
        """Test rate limiting properties."""
        env_config = EnvironmentConfig()
        assert env_config.gemini_rate_limit_rpm == 60
        assert env_config.gemini_rate_limit_tpm == 32000
    
    def test_validation_with_missing_key(self):
        """Test validation when required keys are missing."""
        with patch.dict(os.environ, {}, clear=True):
            env_config = EnvironmentConfig()
            validation = env_config.validate_required()
            
            assert not validation['valid']
            assert 'GEMINI_API_KEY' in validation['missing']
    
    def test_validation_with_all_keys(self, mock_env_vars):
        """Test validation when all required keys are present."""
        env_config = EnvironmentConfig()
        validation = env_config.validate_required()
        
        assert validation['valid']
        assert len(validation['missing']) == 0
    
    def test_get_methods(self, mock_env_vars):
        """Test utility get methods."""
        env_config = EnvironmentConfig()
        
        assert env_config.get('TESTING') == 'true'
        assert env_config.get('NONEXISTENT', 'default') == 'default'
        assert env_config.get_bool('DEBUG') is True
        assert env_config.get_int('GEMINI_RATE_LIMIT_RPM') == 60


class TestGeminiConfig:
    """Test cases for GeminiConfig class."""
    
    def test_gemini_config_creation(self):
        """Test GeminiConfig creation with default values."""
        config = GeminiConfig(api_key="test-key")
        
        assert config.api_key == "test-key"
        assert config.model_name == "gemini-2.5-flash"
        assert config.fallback_model == "gemini-1.5-flash"
        assert config.max_tokens == 8192
        assert config.temperature == 0.3
    
    def test_gemini_config_custom_values(self):
        """Test GeminiConfig with custom values."""
        config = GeminiConfig(
            api_key="custom-key",
            model_name="custom-model",
            max_tokens=4096,
            temperature=0.7
        )
        
        assert config.api_key == "custom-key"
        assert config.model_name == "custom-model"
        assert config.max_tokens == 4096
        assert config.temperature == 0.7


class TestGeminiAPIManager:
    """Test cases for GeminiAPIManager class."""
    
    def test_api_manager_initialization(self, gemini_config_test):
        """Test API manager initialization."""
        manager = GeminiAPIManager(gemini_config_test)
        
        assert manager.config.api_key == "test-api-key"
        assert manager.config.model_name == "gemini-2.5-flash"
    
    def test_rate_limiting_check(self, mock_gemini_api_manager):
        """Test rate limiting functionality."""
        manager = mock_gemini_api_manager
        
        # Should not raise any exceptions
        manager._check_rate_limit()
        
        # Verify request times are tracked
        assert hasattr(manager, 'request_times')
        assert isinstance(manager.request_times, list)
    
    @patch('config.gemini_config.SDK_AVAILABLE', True)
    def test_generate_content_success(self, mock_gemini_api_manager):
        """Test successful content generation."""
        manager = mock_gemini_api_manager
        
        response = manager.generate_content("Test prompt")
        
        assert response == "This is a test response from Gemini API"
        manager.client.models.generate_content.assert_called_once()
    
    @patch('config.gemini_config.SDK_AVAILABLE', False)
    def test_generate_content_no_sdk(self, gemini_config_test):
        """Test content generation when SDK is not available."""
        manager = GeminiAPIManager(gemini_config_test)
        
        response = manager.generate_content("Test prompt")
        
        assert response is None
    
    def test_get_available_models(self, mock_gemini_api_manager):
        """Test getting available models."""
        manager = mock_gemini_api_manager
        
        models = manager.get_available_models()
        
        assert isinstance(models, list)
        assert "gemini-2.5-flash" in models
        assert "gemini-1.5-pro" in models
        assert "gemini-1.5-flash" in models
    
    def test_api_key_loading_from_env(self, mock_env_vars):
        """Test API key loading from environment variables."""
        manager = GeminiAPIManager()
        
        assert manager.config.api_key == "test-api-key"
    
    def test_fallback_model_on_error(self, mock_gemini_api_manager):
        """Test fallback to different model on error."""
        manager = mock_gemini_api_manager
        
        # Mock first call to fail, second to succeed
        manager.client.models.generate_content.side_effect = [
            Exception("Model not found"),
            Mock(text="Fallback response")
        ]
        
        response = manager.generate_content("Test prompt")
        
        assert response == "Fallback response"
        assert manager.client.models.generate_content.call_count == 2
