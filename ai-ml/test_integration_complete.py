#!/usr/bin/env python3
"""
REGIQ AI/ML Service Integration Test Script

This script tests all AI/ML service endpoints to ensure they're working correctly.
Run this AFTER starting the FastAPI server.

Usage:
    python test_integration_complete.py
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health_endpoint():
    """Test the health check endpoint."""
    print_section("1. Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Status: {data.get('status', 'unknown')}")
            print(f"   Service: {data.get('service', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to AI/ML service - Is it running?")
        print("   Start with: uvicorn services.api.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print_section("2. Root Endpoint")
    
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Welcome Message: {data.get('message', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Docs: {data.get('docs', 'N/A')}")
            return True
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_bias_analysis_endpoints():
    """Test bias analysis endpoints."""
    print_section("3. Bias Analysis Endpoints")
    
    # Test analyze endpoint
    try:
        print("Testing POST /api/v1/bias-analysis/analyze...")
        test_data = {
            "model_id": "test_model",
            "dataset": {
                "features": ["age", "income"],
                "sensitive_attributes": ["gender"],
                "predictions": [1, 0, 1, 0],
                "actuals": [1, 0, 0, 1]
            }
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/bias-analysis/analyze",
            json=test_data,
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            print("✅ Analyze endpoint working")
        else:
            print(f"⚠️  Analyze endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Analyze endpoint error: {e}")
    
    # Test score endpoint
    try:
        print("\nTesting POST /api/v1/bias-analysis/score...")
        response = requests.post(
            f"{BASE_URL}/api/v1/bias-analysis/score",
            json={"modelId": "test"},
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Score endpoint working")
            if "demographic_parity" in data or "fairness_metrics" in data:
                print("   Returns fairness metrics ✓")
        else:
            print(f"⚠️  Score endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Score endpoint error: {e}")
    
    # Test explain endpoint
    try:
        print("\nTesting POST /api/v1/bias-analysis/explain...")
        response = requests.post(
            f"{BASE_URL}/api/v1/bias-analysis/explain",
            json={"analysis_id": "test", "explainer_type": "shap"},
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            print("✅ Explain endpoint working")
        else:
            print(f"⚠️  Explain endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Explain endpoint error: {e}")

def test_risk_simulator_endpoints():
    """Test risk simulator endpoints."""
    print_section("4. Risk Simulator Endpoints")
    
    # Test frameworks endpoint
    try:
        print("Testing GET /api/v1/risk-simulator/frameworks...")
        response = requests.get(
            f"{BASE_URL}/api/v1/risk-simulator/frameworks",
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            frameworks = data.get("frameworks", [])
            print(f"✅ Frameworks endpoint working")
            print(f"   Available frameworks: {len(frameworks)}")
            for fw in frameworks[:3]:  # Show first 3
                print(f"   - {fw.get('name', 'Unknown')}")
        else:
            print(f"⚠️  Frameworks endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Frameworks endpoint error: {e}")
    
    # Test simulate endpoint
    try:
        print("\nTesting POST /api/v1/risk-simulator/simulate...")
        response = requests.post(
            f"{BASE_URL}/api/v1/risk-simulator/simulate",
            json={
                "simulation_type": "monte_carlo",
                "framework_id": "eu_ai_act"
            },
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            print("✅ Simulate endpoint working")
        else:
            print(f"⚠️  Simulate endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Simulate endpoint error: {e}")
    
    # Test monte-carlo endpoint
    try:
        print("\nTesting POST /api/v1/risk-simulator/monte-carlo...")
        response = requests.post(
            f"{BASE_URL}/api/v1/risk-simulator/monte-carlo",
            json={
                "simulation_id": "test",
                "n_simulations": 100,
                "sampling_method": "lhs"
            },
            timeout=TIMEOUT * 2  # Give it more time
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Monte Carlo endpoint working")
            if "mean" in data or "statistics" in data:
                print("   Returns statistical results ✓")
        else:
            print(f"⚠️  Monte Carlo endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Monte Carlo endpoint error: {e}")
    
    # Test bayesian endpoint
    try:
        print("\nTesting POST /api/v1/risk-simulator/bayesian...")
        response = requests.post(
            f"{BASE_URL}/api/v1/risk-simulator/bayesian",
            json={
                "prior": {"mean": 0.5, "std": 0.1},
                "data": [0.4, 0.6, 0.5, 0.7]
            },
            timeout=TIMEOUT * 2
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Bayesian endpoint working")
            if "posterior_mean" in data or "posterior" in data:
                print("   Returns posterior distribution ✓")
        else:
            print(f"⚠️  Bayesian endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Bayesian endpoint error: {e}")

def test_regulatory_intelligence_endpoints():
    """Test regulatory intelligence endpoints."""
    print_section("5. Regulatory Intelligence Endpoints")
    
    # Test compliance analysis
    try:
        print("Testing POST /api/v1/regulatory-intelligence/documents/analyze...")
        response = requests.post(
            f"{BASE_URL}/api/v1/regulatory-intelligence/documents/analyze",
            json={
                "document_text": "GDPR requires data protection and privacy.",
                "document_type": "policy"
            },
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            print("✅ Compliance analysis endpoint working")
        else:
            print(f"⚠️  Compliance analysis returned {response.status_code}")
    except Exception as e:
        print(f"❌ Compliance analysis error: {e}")
    
    # Test summarize
    try:
        print("\nTesting POST /api/v1/regulatory-intelligence/documents/summarize...")
        response = requests.post(
            f"{BASE_URL}/api/v1/regulatory-intelligence/documents/summarize",
            json={
                "document_text": "Long regulatory text about GDPR compliance...",
                "summary_type": "executive"
            },
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            print("✅ Summarize endpoint working")
        else:
            print(f"⚠️  Summarize endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Summarize endpoint error: {e}")
    
    # Test Q&A
    try:
        print("\nTesting POST /api/v1/regulatory-intelligence/qa...")
        response = requests.post(
            f"{BASE_URL}/api/v1/regulatory-intelligence/qa",
            json={
                "question": "What are the penalties for GDPR violation?",
                "context": "GDPR compliance framework"
            },
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            print("✅ Q&A endpoint working")
        else:
            print(f"⚠️  Q&A endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Q&A endpoint error: {e}")

def test_report_generator_endpoints():
    """Test report generator endpoints."""
    print_section("6. Report Generator Endpoints")
    
    # Test generate endpoint
    try:
        print("Testing POST /api/v1/report-generator/generate...")
        response = requests.post(
            f"{BASE_URL}/api/v1/report-generator/generate",
            json={
                "report_type": "fairness",
                "data": {"test": "data"}
            },
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            print("✅ Report generation endpoint working")
        else:
            print(f"⚠️  Report generation returned {response.status_code}")
    except Exception as e:
        print(f"❌ Report generation error: {e}")
    
    # Test export endpoint
    try:
        print("\nTesting POST /api/v1/report-generator/export...")
        response = requests.post(
            f"{BASE_URL}/api/v1/report-generator/export",
            json={
                "report_id": "test",
                "format": "html"
            },
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            print("✅ Report export endpoint working")
        else:
            print(f"⚠️  Report export returned {response.status_code}")
    except Exception as e:
        print(f"❌ Report export error: {e}")

def main():
    """Run all integration tests."""
    print("="*60)
    print("  REGIQ AI/ML SERVICE INTEGRATION TESTS")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Timeout: {TIMEOUT}s")
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health_endpoint()))
    results.append(("Root Endpoint", test_root_endpoint()))
    results.append(("Bias Analysis", test_bias_analysis_endpoints()))
    results.append(("Risk Simulator", test_risk_simulator_endpoints()))
    results.append(("Regulatory Intelligence", test_regulatory_intelligence_endpoints()))
    results.append(("Report Generator", test_report_generator_endpoints()))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nAI/ML service is ready for backend integration.")
        print("\nNext steps:")
        print("1. Keep AI/ML service running")
        print("2. Start backend: cd backend && npm run dev")
        print("3. Test backend → AI/ML integration")
    else:
        print("\n⚠️  Some tests failed.")
        print("\nTroubleshooting:")
        print("1. Make sure AI/ML service is running: uvicorn services.api.main:app --reload")
        print("2. Check virtual environment is activated")
        print("3. Verify all dependencies are installed: pip install -r requirements.txt")
        print("4. Check logs for detailed error messages")

if __name__ == "__main__":
    main()
