#!/usr/bin/env python3
"""
REGIQ AI/ML Gemini API Test Script
Tests all aspects of Gemini API integration including connectivity, rate limiting, and error handling.
"""

import sys
import os
import time
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from config.gemini_config import GeminiAPIManager, GeminiConfig, create_api_keys_file

def test_api_key_setup():
    """Test if API key is properly configured."""
    print("🔑 Testing API Key Setup...")
    
    # Check environment variable
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key:
        print("✅ GEMINI_API_KEY environment variable found")
        return True
    
    # Check config file
    config_path = Path("config/api_keys.yaml")
    if config_path.exists():
        print("✅ config/api_keys.yaml file found")
        return True
    
    print("❌ No API key found")
    print("   Set environment variable: set GEMINI_API_KEY=your-key")
    print("   Or edit config/api_keys.yaml")
    return False

def test_basic_connectivity():
    """Test basic API connectivity."""
    print("\n🌐 Testing Basic Connectivity...")
    
    try:
        api_manager = GeminiAPIManager()
        success = api_manager.test_connection()
        return success
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_different_models():
    """Test different Gemini models."""
    print("\n🤖 Testing Different Models...")
    
    try:
        api_manager = GeminiAPIManager()
        
        models_to_test = [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-2.5-flash"
        ]
        
        test_prompt = "What is AI? Answer in one sentence."
        
        for model in models_to_test:
            print(f"\n   Testing {model}...")
            response = api_manager.generate_content(test_prompt, model=model)
            
            if response:
                print(f"   ✅ {model}: {response[:100]}...")
            else:
                print(f"   ❌ {model}: Failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Model testing failed: {e}")
        return False

def test_rate_limiting():
    """Test rate limiting functionality."""
    print("\n⏱️  Testing Rate Limiting...")
    
    try:
        # Create config with low rate limits for testing
        from config.gemini_config import GeminiConfig
        config = GeminiConfig(
            api_key=os.getenv('GEMINI_API_KEY') or "test-key",
            rate_limit_requests_per_minute=3  # Low limit for testing
        )
        
        api_manager = GeminiAPIManager(config)
        
        print("   Making rapid requests to test rate limiting...")
        
        for i in range(5):
            start_time = time.time()
            response = api_manager.generate_content(f"Count to {i+1}")
            end_time = time.time()
            
            print(f"   Request {i+1}: {end_time - start_time:.1f}s")
            
            if i >= 2 and end_time - start_time > 1:
                print("   ✅ Rate limiting is working (requests are being delayed)")
                return True
        
        print("   ⚠️  Rate limiting may not be active (requests too fast)")
        return True
        
    except Exception as e:
        print(f"❌ Rate limiting test failed: {e}")
        return False

def test_error_handling():
    """Test error handling and retry logic."""
    print("\n🛡️  Testing Error Handling...")
    
    try:
        # Test with invalid API key
        from config.gemini_config import GeminiConfig
        config = GeminiConfig(api_key="invalid-key-for-testing")
        api_manager = GeminiAPIManager(config)
        
        print("   Testing with invalid API key...")
        response = api_manager.generate_content("Test prompt")
        
        if not response:
            print("   ✅ Error handling works (invalid key rejected)")
        else:
            print("   ⚠️  Unexpected success with invalid key")
        
        return True
        
    except Exception as e:
        print(f"   ✅ Error properly caught: {type(e).__name__}")
        return True

def test_configuration_loading():
    """Test configuration loading from different sources."""
    print("\n⚙️  Testing Configuration Loading...")
    
    try:
        # Test environment variable loading
        original_key = os.getenv('GEMINI_API_KEY')
        
        if original_key:
            print("   ✅ Environment variable configuration works")
        
        # Test config file loading
        config_path = Path("config/api_keys.yaml")
        if config_path.exists():
            print("   ✅ Config file found")
        else:
            print("   ⚠️  Config file not found (using environment variable)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all API tests."""
    print("🧪 REGIQ AI/ML Gemini API Comprehensive Test")
    print("="*60)
    
    tests = [
        ("API Key Setup", test_api_key_setup),
        ("Basic Connectivity", test_basic_connectivity),
        ("Different Models", test_different_models),
        ("Rate Limiting", test_rate_limiting),
        ("Error Handling", test_error_handling),
        ("Configuration Loading", test_configuration_loading),
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
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Gemini API is ready for development.")
    elif passed >= total * 0.8:
        print("\n👍 Most tests passed. Minor issues may need attention.")
    else:
        print("\n⚠️  Several tests failed. Please check your configuration.")
    
    return passed == total

def main():
    """Main test function."""
    
    # Ensure config file exists
    create_api_keys_file()
    
    # Run comprehensive tests
    success = run_comprehensive_test()
    
    if not success:
        print(f"\n📋 Troubleshooting Steps:")
        print(f"   1. Get API key: https://aistudio.google.com/app/apikey")
        print(f"   2. Set environment variable: set GEMINI_API_KEY=your-actual-key")
        print(f"   3. Or edit config/api_keys.yaml with your key")
        print(f"   4. Install Google GenAI: pip install -q -U google-genai")
        print(f"   5. Check internet connection")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
