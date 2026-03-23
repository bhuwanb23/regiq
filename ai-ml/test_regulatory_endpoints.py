#!/usr/bin/env python3
"""Test script to verify regulatory intelligence endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "regiq-internal-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_analyze_document():
    """Test document analysis endpoint"""
    print("\n=== Testing /api/v1/regulatory-intelligence/documents/analyze ===")
    
    payload = {
        "document_text": "GDPR requires organizations to protect personal data and privacy.",
        "document_type": "regulation",
        "analysis_depth": "standard"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/regulatory-intelligence/documents/analyze",
            headers=headers,
            json=payload
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
        else:
            print(f"❌ FAILED: {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def test_summarize():
    """Test summarization endpoint"""
    print("\n=== Testing /api/v1/regulatory-intelligence/summarize ===")
    
    payload = {
        "text": "The GDPR requires organizations to implement appropriate technical and organizational measures.",
        "summary_type": "executive",
        "max_length": 300
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/regulatory-intelligence/summarize",
            headers=headers,
            json=payload
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
        else:
            print(f"❌ FAILED: {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def test_qa():
    """Test Q&A endpoint"""
    print("\n=== Testing /api/v1/regulatory-intelligence/qa ===")
    
    payload = {
        "question": "What are GDPR penalties?",
        "context": "GDPR compliance",
        "model_preference": "gemini"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/regulatory-intelligence/qa",
            headers=headers,
            json=payload
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
        else:
            print(f"❌ FAILED: {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    print("=" * 70)
    print("TESTING REGULATORY INTELLIGENCE ENDPOINTS")
    print("=" * 70)
    
    test_analyze_document()
    test_summarize()
    test_qa()
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
