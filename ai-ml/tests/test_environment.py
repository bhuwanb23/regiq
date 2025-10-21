#!/usr/bin/env python3
"""
REGIQ AI/ML Environment Test Suite
Tests all environment configuration and API connectivity.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from config.env_config import get_env_config
from config.gemini_config import GeminiAPIManager

def test_environment_loading():
    """Test environment variable loading."""
    print("🔧 Testing Environment Configuration")
    print("="*50)
    
    try:
        env_config = get_env_config()
        env_config.print_config_summary()
        
        # Validate required variables
        validation = env_config.validate_required()
        
        if validation['valid']:
            print("\n✅ Environment configuration is valid")
            return True
        else:
            print(f"\n❌ Environment validation failed: {validation['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Environment loading failed: {e}")
        return False

def test_gemini_api_integration():
    """Test Gemini API with environment configuration."""
    print("\n🤖 Testing Gemini API Integration")
    print("="*50)
    
    try:
        # Initialize API manager (should use .env config)
        api_manager = GeminiAPIManager()
        
        # Test connection
        success = api_manager.test_connection()
        
        if success:
            print("✅ Gemini API integration successful")
            
            # Test different models
            models = ["gemini-1.5-flash", "gemini-1.5-pro"]
            for model in models:
                print(f"\n   Testing {model}...")
                response = api_manager.generate_content(
                    "What is 2+2? Answer with just the number.", 
                    model=model
                )
                if response:
                    print(f"   ✅ {model}: {response.strip()}")
                else:
                    print(f"   ❌ {model}: Failed")
            
            return True
        else:
            print("❌ Gemini API integration failed")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test error: {e}")
        return False

def test_database_config():
    """Test database configuration."""
    print("\n🗄️  Testing Database Configuration")
    print("="*50)
    
    try:
        env_config = get_env_config()
        
        print(f"Database URL: {env_config.database_url}")
        print(f"PostgreSQL: {env_config.postgres_host}:{env_config.postgres_port}")
        print(f"Database: {env_config.postgres_db}")
        print(f"User: {env_config.postgres_user}")
        print(f"Password: {'✅ Set' if env_config.postgres_password else '❌ Not set'}")
        
        # Test SQLite database path
        if 'sqlite' in env_config.database_url:
            db_path = env_config.database_url.replace('sqlite:///', '')
            db_file = Path(db_path)
            
            if db_file.exists():
                print(f"✅ SQLite database exists: {db_file}")
                return True
            else:
                print(f"⚠️  SQLite database not found: {db_file}")
                print("   Run: python scripts/setup_database.py")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database config test error: {e}")
        return False

def test_security_config():
    """Test security configuration."""
    print("\n🔒 Testing Security Configuration")
    print("="*50)
    
    try:
        env_config = get_env_config()
        
        # Check secret key
        if env_config.secret_key:
            print("✅ Secret key is configured")
        else:
            print("⚠️  Secret key not set (required for production)")
        
        # Check CORS origins
        origins = env_config.cors_origins
        print(f"✅ CORS origins configured: {len(origins)} origins")
        for origin in origins:
            print(f"   - {origin}")
        
        return True
        
    except Exception as e:
        print(f"❌ Security config test error: {e}")
        return False

def run_all_tests():
    """Run all environment tests."""
    print("🧪 REGIQ AI/ML Environment Test Suite")
    print("="*60)
    
    tests = [
        ("Environment Loading", test_environment_loading),
        ("Gemini API Integration", test_gemini_api_integration),
        ("Database Configuration", test_database_config),
        ("Security Configuration", test_security_config),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Environment is ready for development.")
        print("\n🚀 Next Steps:")
        print("   1. Start Phase 2: Regulatory Intelligence Engine")
        print("   2. Begin building AI/ML services")
        print("   3. Use env_config in your code for all settings")
        
    elif passed >= total * 0.8:
        print("\n👍 Most tests passed. Minor configuration needed.")
        
    else:
        print("\n⚠️  Several tests failed. Please check your configuration.")
        print("\n📋 Common fixes:")
        print("   1. Verify .env file exists and has correct values")
        print("   2. Check GEMINI_API_KEY is set correctly")
        print("   3. Run database setup if needed")
    
    return passed == total

def main():
    """Main test function."""
    success = run_all_tests()
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
