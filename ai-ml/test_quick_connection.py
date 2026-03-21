#!/usr/bin/env python3
"""
Quick test to verify AI/ML service is running and accessible
"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "regiq-internal-api-key"

# Headers with API key
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test a single endpoint."""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTesting {method} {endpoint}...")
        
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=HEADERS, timeout=10)
        
        status = "✅ PASS" if response.status_code == expected_status else "❌ FAIL"
        print(f"{status} - Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Response keys: {list(result.keys())[:5]}")
            return True
        else:
            print(f"   Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("="*60)
    print("REGIQ AI/ML SERVICE - QUICK CONNECTION TEST")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"API Key: {API_KEY}")
    
    tests = [
        # Health check (no auth required)
        ("GET", "/health", None, 200),
        
        # Root endpoint (no auth required)
        ("GET", "/", None, 200),
        
        # Bias Analysis endpoints
        ("POST", "/api/v1/bias-analysis/score", {"modelId": "test"}, 200),
        ("POST", "/api/v1/bias-analysis/explain", {"analysis_id": "123", "explainer_type": "shap"}, 200),
        
        # Risk Simulator endpoints
        ("GET", "/api/v1/risk-simulator/frameworks", None, 200),
        ("POST", "/api/v1/risk-simulator/monte-carlo", {"simulation_id": "test", "n_simulations": 10}, 200),
        ("POST", "/api/v1/risk-simulator/bayesian", {"prior": {"mean": 0.5, "std": 0.1}}, 200),
        
        # Regulatory Intelligence
        ("POST", "/api/v1/regulatory-intelligence/documents/analyze", {"document_text": "GDPR test", "document_type": "policy"}, 200),
        
        # Report Generator
        ("POST", "/api/v1/report-generator/generate", {"report_type": "fairness", "data": {}}, 200),
    ]
    
    results = []
    for method, endpoint, data, expected in tests:
        result = test_endpoint(method, endpoint, data, expected)
        results.append((f"{method} {endpoint}", result))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 ALL ENDPOINTS WORKING!")
    else:
        print(f"\n⚠️  {total - passed} endpoints failed")
        print("\nTroubleshooting:")
        print("1. Make sure AI/ML service is running: uvicorn services.api.main:app --reload")
        print("2. Check that .env has SERVICE_API_KEY=regiq-internal-api-key")
        print("3. Verify virtual environment is activated")

if __name__ == "__main__":
    main()
