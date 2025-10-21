#!/usr/bin/env python3
"""
Simple Gemini API Test - Direct HTTP Requests
Tests the Gemini API using direct HTTP requests without any SDK.
"""

import os
import sys
import requests
import json
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from config.env_config import get_env_config

def test_direct_api():
    """Test Gemini API with direct HTTP requests."""
    print("🧪 Testing Gemini API with Direct HTTP Requests")
    print("="*60)
    
    # Get configuration
    env_config = get_env_config()
    api_key = env_config.gemini_api_key
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file or environment variables")
        print("   1. Check your .env file contains: GEMINI_API_KEY=your-actual-api-key")
        print("   2. Or set environment variable: set GEMINI_API_KEY=your-actual-api-key")
        return False
    
    # API endpoint
    model = "gemini-1.5-flash"  # Using flash for faster testing
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    # Headers
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Test payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Say 'Hello from REGIQ AI/ML!' in exactly those words."
                    }
                ]
            }
        ]
    }
    
    print(f"🌐 Making request to: {url}")
    print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        # Make the request
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            # Parse response
            data = response.json()
            
            # Extract text
            if 'candidates' in data and data['candidates']:
                candidate = data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if parts and 'text' in parts[0]:
                        generated_text = parts[0]['text']
                        
                        print("✅ API Request Successful!")
                        print(f"📝 Response: {generated_text.strip()}")
                        return True
            
            print("❌ Unexpected response format")
            print(f"📄 Raw response: {json.dumps(data, indent=2)}")
            return False
            
        else:
            print(f"❌ API Request Failed: {response.status_code}")
            print(f"📄 Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_multiple_models():
    """Test multiple Gemini models."""
    print("\n🤖 Testing Multiple Models")
    print("-" * 40)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ API key not available")
        return False
    
    models = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-flash"
    ]
    
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "What is AI? Answer in one sentence."
                    }
                ]
            }
        ]
    }
    
    success_count = 0
    
    for model in models:
        print(f"\n   Testing {model}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and data['candidates']:
                    candidate = data['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        parts = candidate['content']['parts']
                        if parts and 'text' in parts[0]:
                            text = parts[0]['text'].strip()
                            print(f"   ✅ {model}: {text[:80]}...")
                            success_count += 1
                            continue
            
            print(f"   ❌ {model}: Failed ({response.status_code})")
            
        except Exception as e:
            print(f"   ❌ {model}: Error - {e}")
    
    print(f"\n📊 Models tested: {success_count}/{len(models)} successful")
    return success_count > 0

def main():
    """Main test function."""
    print("🚀 REGIQ AI/ML - Simple Gemini API Test")
    print("="*60)
    
    # Test basic API
    basic_success = test_direct_api()
    
    if basic_success:
        # Test multiple models
        models_success = test_multiple_models()
        
        if models_success:
            print("\n🎉 All tests passed! Gemini API is working perfectly.")
            print("\n✨ You can now use Gemini API in your REGIQ AI/ML project!")
            print("\n📋 Next steps:")
            print("   1. Run: python scripts/setup_gemini_api.py")
            print("   2. Use the GeminiAPIManager class in your code")
            print("   3. Start building AI/ML features!")
        else:
            print("\n⚠️  Basic API works, but some models may have issues.")
    else:
        print("\n❌ Basic API test failed. Please check:")
        print("   1. API key is correct")
        print("   2. Internet connection is working")
        print("   3. Gemini API service is available")
    
    return basic_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
