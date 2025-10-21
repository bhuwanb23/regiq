#!/usr/bin/env python3
"""
REGIQ AI/ML Gemini API Configuration
Handles Gemini API setup, authentication, and rate limiting.
"""

import os
import time
import yaml
import requests
import json
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class GeminiConfig:
    """Gemini API configuration settings."""
    api_key: str
    model_name: str = "gemini-1.5-pro"
    fallback_model: str = "gemini-1.5-flash"
    max_tokens: int = 8192
    temperature: float = 0.3
    rate_limit_requests_per_minute: int = 60
    rate_limit_tokens_per_minute: int = 32000
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

class GeminiAPIManager:
    """Manages Gemini API connections, rate limiting, and error handling."""
    
    def __init__(self, config: Optional[GeminiConfig] = None):
        """Initialize the Gemini API manager."""
        self.config = config or self._load_config()
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.last_request_time = 0
        self.request_count = 0
        self.request_times = []
        
    def _load_config(self) -> GeminiConfig:
        """Load configuration from environment variables and config files."""
        
        # Try to load API key from multiple sources
        api_key = self._get_api_key()
        
        if not api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable "
                "or add it to config/api_keys.yaml"
            )
        
        # Load additional config from YAML if available
        config_path = Path("config/api_keys.yaml")
        yaml_config = {}
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                    yaml_config = yaml_data.get('llm_providers', {}).get('google', {})
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}")
        
        return GeminiConfig(
            api_key=api_key,
            model_name=yaml_config.get('model_name', 'gemini-1.5-pro'),
            fallback_model=yaml_config.get('fallback_model', 'gemini-1.5-flash'),
            max_tokens=int(os.getenv('GEMINI_MAX_TOKENS', yaml_config.get('max_tokens', 8192))),
            temperature=float(os.getenv('GEMINI_TEMPERATURE', yaml_config.get('temperature', 0.3))),
            rate_limit_requests_per_minute=int(os.getenv('GEMINI_RATE_LIMIT_RPM', yaml_config.get('rate_limit_rpm', 60))),
            rate_limit_tokens_per_minute=int(os.getenv('GEMINI_RATE_LIMIT_TPM', yaml_config.get('rate_limit_tpm', 32000))),
        )
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from multiple sources."""
        
        # 1. Environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            return api_key
        
        # 2. Config file
        config_path = Path("config/api_keys.yaml")
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                    return yaml_data.get('llm_providers', {}).get('google', {}).get('api_key')
            except Exception:
                pass
        
        return None
    
    def _make_request(self, model: str, prompt: str) -> Optional[Dict]:
        """Make direct HTTP request to Gemini API."""
        url = f"{self.base_url}/{model}:generateContent"
        
        headers = {
            "x-goog-api-key": self.config.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(
                url, 
                headers=headers, 
                json=payload, 
                timeout=self.config.timeout_seconds
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API request failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Request error: {e}")
            return None
    
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        current_time = time.time()
        
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        # Check if we're hitting rate limits
        if len(self.request_times) >= self.config.rate_limit_requests_per_minute:
            sleep_time = 60 - (current_time - self.request_times[0])
            if sleep_time > 0:
                print(f"⏳ Rate limit reached. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
        
        # Add current request time
        self.request_times.append(current_time)
    
    def generate_content(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """Generate content using Gemini API with error handling and retries."""
        
        # Use provided parameters or defaults
        model_name = model or self.config.model_name
        temp = temperature if temperature is not None else self.config.temperature
        max_tok = max_tokens or self.config.max_tokens
        
        for attempt in range(self.config.max_retries):
            try:
                # Check rate limiting
                self._check_rate_limit()
                
                # Make API request
                response_data = self._make_request(model_name, prompt)
                
                if response_data and 'candidates' in response_data:
                    # Extract text from response
                    candidates = response_data['candidates']
                    if candidates and 'content' in candidates[0]:
                        parts = candidates[0]['content']['parts']
                        if parts and 'text' in parts[0]:
                            return parts[0]['text']
                
                return None
                
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.config.max_retries - 1:
                    # Try fallback model on error
                    if model_name != self.config.fallback_model:
                        print(f"🔄 Trying fallback model: {self.config.fallback_model}")
                        model_name = self.config.fallback_model
                    
                    # Wait before retry
                    time.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    print(f"❌ All attempts failed for prompt: {prompt[:50]}...")
        
        return None
    
    def test_connection(self) -> bool:
        """Test the API connection with a simple request."""
        print("🧪 Testing Gemini API connection...")
        
        test_prompt = "Say 'Hello, REGIQ AI/ML!' in exactly those words."
        response = self.generate_content(test_prompt)
        
        if response:
            print(f"✅ API test successful!")
            print(f"   Response: {response.strip()}")
            return True
        else:
            print("❌ API test failed")
            return False
    
    def get_available_models(self) -> list:
        """Get list of available Gemini models."""
        try:
            # Available Gemini models via API
            available_models = [
                "gemini-1.5-pro",
                "gemini-1.5-flash", 
                "gemini-2.5-flash"
            ]
            return available_models
        except Exception as e:
            print(f"❌ Could not fetch available models: {e}")
            return []

def create_api_keys_file():
    """Create api_keys.yaml from template if it doesn't exist."""
    
    source_path = Path("config/api_keys.yaml.example")
    target_path = Path("config/api_keys.yaml")
    
    if target_path.exists():
        print(f"📁 {target_path} already exists")
        return True
    
    if not source_path.exists():
        print(f"❌ Template file {source_path} not found")
        return False
    
    try:
        # Copy template to actual config file
        with open(source_path, 'r') as src, open(target_path, 'w') as dst:
            content = src.read()
            dst.write(content)
        
        print(f"✅ Created {target_path} from template")
        print(f"   Please edit this file and add your actual API key")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def main():
    """Main function for testing the configuration."""
    print("🔑 REGIQ AI/ML Gemini API Configuration")
    print("="*50)
    
    # Create config file if needed
    create_api_keys_file()
    
    try:
        # Initialize API manager
        api_manager = GeminiAPIManager()
        
        # Test connection
        success = api_manager.test_connection()
        
        if success:
            print("\n🎉 Gemini API setup complete!")
            print("   Available models:", api_manager.get_available_models())
        else:
            print("\n❌ Setup incomplete. Please check your API key.")
            
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
        print("\n📋 Setup steps:")
        print("   1. Get API key: https://aistudio.google.com/app/apikey")
        print("   2. Set environment variable: set GEMINI_API_KEY=your-key")
        print("   3. Or edit config/api_keys.yaml with your key")

if __name__ == "__main__":
    main()
