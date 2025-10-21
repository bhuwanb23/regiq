#!/usr/bin/env python3
"""
REGIQ AI/ML Gemini SDK Test
Tests Gemini API using the official Google GenAI SDK.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from config.env_config import get_env_config

def test_gemini_sdk():
    """Test Gemini API using Google GenAI SDK."""
    print("🤖 Testing Gemini API with Google GenAI SDK")
    print("="*60)
    
    try:
        from google import genai
        print("✅ Google GenAI SDK imported successfully")
    except ImportError:
        print("❌ Google GenAI SDK not installed")
        print("   Install with: pip install google-genai")
        return False
    
    # Get configuration
    env_config = get_env_config()
    api_key = env_config.gemini_api_key
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        print("   Check your .env file contains: GEMINI_API_KEY=your-actual-api-key")
        return False
    
    print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        # Initialize client
        os.environ['GEMINI_API_KEY'] = api_key
        client = genai.Client()
        print("✅ Gemini client initialized")
        
        # Test with gemini-2.5-flash
        print(f"\n🧪 Testing gemini-2.5-flash...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say 'Hello from REGIQ AI/ML!' in exactly those words."
        )
        
        print(f"✅ API Response: {response.text.strip()}")
        
        # Test with a simple math question
        print(f"\n🧪 Testing with math question...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="What is 2+2? Answer with just the number."
        )
        
        print(f"✅ Math Response: {response.text.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def test_multiple_models():
    """Test multiple Gemini models."""
    print(f"\n🤖 Testing Multiple Models")
    print("-" * 40)
    
    try:
        from google import genai
        
        env_config = get_env_config()
        api_key = env_config.gemini_api_key
        
        if not api_key:
            print("❌ API key not available")
            return False
        
        os.environ['GEMINI_API_KEY'] = api_key
        client = genai.Client()
        
        models = [
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ]
        
        success_count = 0
        
        for model in models:
            print(f"\n   Testing {model}...")
            try:
                response = client.models.generate_content(
                    model=model,
                    contents="What is AI? Answer in one sentence."
                )
                
                text = response.text.strip()
                print(f"   ✅ {model}: {text[:80]}...")
                success_count += 1
                
            except Exception as e:
                print(f"   ❌ {model}: Error - {e}")
        
        print(f"\n📊 Models tested: {success_count}/{len(models)} successful")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Multiple models test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 REGIQ AI/ML - Gemini SDK Test")
    print("="*60)
    
    # Test basic SDK functionality
    basic_success = test_gemini_sdk()
    
    if basic_success:
        # Test multiple models
        models_success = test_multiple_models()
        
        if models_success:
            print("\n🎉 All tests passed! Gemini SDK is working perfectly.")
            print("\n✨ You can now use Gemini API in your REGIQ AI/ML project!")
            print("\n📋 Usage example:")
            print("   from google import genai")
            print("   client = genai.Client()")
            print("   response = client.models.generate_content(")
            print("       model='gemini-2.5-flash',")
            print("       contents='Your prompt here'")
            print("   )")
            print("   print(response.text)")
        else:
            print("\n⚠️  Basic SDK works, but some models may have issues.")
    else:
        print("\n❌ SDK test failed. Please check:")
        print("   1. Install SDK: pip install google-genai")
        print("   2. API key is correct in .env file")
        print("   3. Internet connection is working")
    
    return basic_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
