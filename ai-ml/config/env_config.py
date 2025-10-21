#!/usr/bin/env python3
"""
REGIQ AI/ML Environment Configuration
Centralized environment variable management for all services.
"""

import os
from pathlib import Path
from typing import Optional, Union
from dotenv import load_dotenv

class EnvironmentConfig:
    """Centralized environment configuration manager."""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize environment configuration."""
        # Load .env file
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to find .env file in current directory or parent directories
            current_dir = Path.cwd()
            for path in [current_dir] + list(current_dir.parents):
                env_path = path / '.env'
                if env_path.exists():
                    load_dotenv(env_path)
                    print(f"✅ Loaded environment from: {env_path}")
                    break
            else:
                print("⚠️  No .env file found, using system environment variables only")
    
    # =============================================================================
    # GEMINI API CONFIGURATION
    # =============================================================================
    @property
    def gemini_api_key(self) -> Optional[str]:
        """Get Gemini API key."""
        return os.getenv('GEMINI_API_KEY')
    
    @property
    def gemini_rate_limit_rpm(self) -> int:
        """Get Gemini rate limit requests per minute."""
        return int(os.getenv('GEMINI_RATE_LIMIT_RPM', '60'))
    
    @property
    def gemini_rate_limit_tpm(self) -> int:
        """Get Gemini rate limit tokens per minute."""
        return int(os.getenv('GEMINI_RATE_LIMIT_TPM', '32000'))
    
    @property
    def gemini_max_tokens(self) -> int:
        """Get Gemini max tokens."""
        return int(os.getenv('GEMINI_MAX_TOKENS', '8192'))
    
    @property
    def gemini_temperature(self) -> float:
        """Get Gemini temperature."""
        return float(os.getenv('GEMINI_TEMPERATURE', '0.3'))
    
    # =============================================================================
    # DATABASE CONFIGURATION
    # =============================================================================
    @property
    def database_url(self) -> str:
        """Get database URL."""
        return os.getenv('DATABASE_URL', 'sqlite:///data/regiq_local.db')
    
    @property
    def postgres_host(self) -> str:
        """Get PostgreSQL host."""
        return os.getenv('POSTGRES_HOST', 'localhost')
    
    @property
    def postgres_port(self) -> int:
        """Get PostgreSQL port."""
        return int(os.getenv('POSTGRES_PORT', '5432'))
    
    @property
    def postgres_db(self) -> str:
        """Get PostgreSQL database name."""
        return os.getenv('POSTGRES_DB', 'regiq_ai_ml')
    
    @property
    def postgres_user(self) -> str:
        """Get PostgreSQL username."""
        return os.getenv('POSTGRES_USER', 'regiq_user')
    
    @property
    def postgres_password(self) -> Optional[str]:
        """Get PostgreSQL password."""
        return os.getenv('POSTGRES_PASSWORD')
    
    # =============================================================================
    # REDIS CONFIGURATION
    # =============================================================================
    @property
    def redis_host(self) -> str:
        """Get Redis host."""
        return os.getenv('REDIS_HOST', 'localhost')
    
    @property
    def redis_port(self) -> int:
        """Get Redis port."""
        return int(os.getenv('REDIS_PORT', '6379'))
    
    @property
    def redis_password(self) -> Optional[str]:
        """Get Redis password."""
        return os.getenv('REDIS_PASSWORD')
    
    # =============================================================================
    # APPLICATION SETTINGS
    # =============================================================================
    @property
    def debug(self) -> bool:
        """Get debug mode."""
        return os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes', 'on')
    
    @property
    def log_level(self) -> str:
        """Get log level."""
        return os.getenv('LOG_LEVEL', 'INFO').upper()
    
    @property
    def max_file_upload_size(self) -> int:
        """Get max file upload size in MB."""
        return int(os.getenv('MAX_FILE_UPLOAD_SIZE', '100'))
    
    @property
    def default_bias_threshold(self) -> float:
        """Get default bias threshold."""
        return float(os.getenv('DEFAULT_BIAS_THRESHOLD', '0.8'))
    
    @property
    def simulation_iterations(self) -> int:
        """Get simulation iterations."""
        return int(os.getenv('SIMULATION_ITERATIONS', '10000'))
    
    # =============================================================================
    # SECURITY SETTINGS
    # =============================================================================
    @property
    def secret_key(self) -> Optional[str]:
        """Get secret key for JWT."""
        return os.getenv('SECRET_KEY')
    
    @property
    def cors_origins(self) -> list:
        """Get CORS origins."""
        origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000')
        return [origin.strip() for origin in origins.split(',')]
    
    # =============================================================================
    # UTILITY METHODS
    # =============================================================================
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable with optional default."""
        return os.getenv(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get environment variable as integer."""
        try:
            return int(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get environment variable as float."""
        try:
            return float(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get environment variable as boolean."""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def validate_required(self) -> dict:
        """Validate that required environment variables are set."""
        required_vars = {
            'GEMINI_API_KEY': self.gemini_api_key,
        }
        
        missing = []
        for var_name, var_value in required_vars.items():
            if not var_value:
                missing.append(var_name)
        
        return {
            'valid': len(missing) == 0,
            'missing': missing,
            'message': f"Missing required environment variables: {', '.join(missing)}" if missing else "All required variables are set"
        }
    
    def print_config_summary(self):
        """Print configuration summary (without sensitive data)."""
        print("🔧 REGIQ AI/ML Environment Configuration")
        print("="*50)
        
        print(f"📊 Application Settings:")
        print(f"   Debug Mode: {self.debug}")
        print(f"   Log Level: {self.log_level}")
        print(f"   Max Upload Size: {self.max_file_upload_size}MB")
        
        print(f"\n🤖 Gemini API:")
        print(f"   API Key: {'✅ Set' if self.gemini_api_key else '❌ Missing'}")
        print(f"   Rate Limit: {self.gemini_rate_limit_rpm} RPM, {self.gemini_rate_limit_tpm} TPM")
        print(f"   Max Tokens: {self.gemini_max_tokens}")
        print(f"   Temperature: {self.gemini_temperature}")
        
        print(f"\n🗄️  Database:")
        print(f"   URL: {self.database_url}")
        print(f"   PostgreSQL: {self.postgres_host}:{self.postgres_port}/{self.postgres_db}")
        
        print(f"\n🔒 Security:")
        print(f"   Secret Key: {'✅ Set' if self.secret_key else '❌ Missing'}")
        print(f"   CORS Origins: {len(self.cors_origins)} configured")
        
        # Validation
        validation = self.validate_required()
        print(f"\n✅ Validation: {validation['message']}")

# Global instance
env_config = EnvironmentConfig()

def get_env_config() -> EnvironmentConfig:
    """Get the global environment configuration instance."""
    return env_config
