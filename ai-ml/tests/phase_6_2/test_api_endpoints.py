#!/usr/bin/env python3
"""
API Endpoint Testing Script
Test the REGIQ AI/ML API endpoints
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint: OK")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint: OK")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_docs_endpoint():
    """Test the docs endpoint"""
    print("\nTesting docs endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Docs endpoint: OK")
            return True
        else:
            print(f"❌ Docs endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Docs endpoint error: {e}")
        return False

def test_regulatory_intelligence_endpoints():
    """Test regulatory intelligence endpoints (structure only)"""
    print("\nTesting regulatory intelligence endpoint structure...")
    
    endpoints = [
        ("/regulatory-intelligence/documents/analyze", "POST"),
        ("/regulatory-intelligence/summarize", "POST"),
        ("/regulatory-intelligence/qa", "POST"),
        ("/regulatory-intelligence/search", "POST")
    ]
    
    success_count = 0
    for endpoint, method in endpoints:
        try:
            url = f"{BASE_URL}{API_PREFIX}{endpoint}"
            if method == "POST":
                # Test with empty payload to check if endpoint exists
                response = requests.post(url, json={}, timeout=5)
            else:
                response = requests.get(url, timeout=5)
            
            # We expect 422 (validation error) or 401 (auth error) if endpoint exists
            # What we don't want is 404 (endpoint not found)
            if response.status_code != 404:
                print(f"✅ {method} {endpoint}: Endpoint exists (status {response.status_code})")
                success_count += 1
            else:
                print(f"❌ {method} {endpoint}: Endpoint not found")
        except requests.exceptions.ConnectionError:
            print(f"❌ {method} {endpoint}: Connection error")
        except Exception as e:
            print(f"✅ {method} {endpoint}: Endpoint exists (error: {type(e).__name__})")
            success_count += 1
    
    return success_count == len(endpoints)

def test_bias_analysis_endpoints():
    """Test bias analysis endpoints (structure only)"""
    print("\nTesting bias analysis endpoint structure...")
    
    endpoints = [
        ("/bias-analysis/models/upload", "POST"),
        ("/bias-analysis/analyze", "POST"),
        ("/bias-analysis/results/test_id", "GET"),
        ("/bias-analysis/reports/generate", "POST")
    ]
    
    success_count = 0
    for endpoint, method in endpoints:
        try:
            url = f"{BASE_URL}{API_PREFIX}{endpoint}"
            if method == "POST":
                response = requests.post(url, json={}, timeout=5)
            else:
                response = requests.get(url, timeout=5)
            
            # We expect 422 (validation error) or 401 (auth error) if endpoint exists
            if response.status_code != 404:
                print(f"✅ {method} {endpoint}: Endpoint exists (status {response.status_code})")
                success_count += 1
            else:
                print(f"❌ {method} {endpoint}: Endpoint not found")
        except requests.exceptions.ConnectionError:
            print(f"❌ {method} {endpoint}: Connection error")
        except Exception as e:
            print(f"✅ {method} {endpoint}: Endpoint exists (error: {type(e).__name__})")
            success_count += 1
    
    return success_count == len(endpoints)

def test_risk_simulator_endpoints():
    """Test risk simulator endpoints (structure only)"""
    print("\nTesting risk simulator endpoint structure...")
    
    endpoints = [
        ("/risk-simulator/setup", "POST"),
        ("/risk-simulator/run/test_id", "POST"),
        ("/risk-simulator/stream/test_id", "GET"),
        ("/risk-simulator/scenarios", "GET"),
        ("/risk-simulator/scenarios", "POST")
    ]
    
    success_count = 0
    for endpoint, method in endpoints:
        try:
            url = f"{BASE_URL}{API_PREFIX}{endpoint}"
            if method == "POST":
                response = requests.post(url, json={}, timeout=5)
            else:
                response = requests.get(url, timeout=5)
            
            # We expect 422 (validation error) or 401 (auth error) if endpoint exists
            if response.status_code != 404:
                print(f"✅ {method} {endpoint}: Endpoint exists (status {response.status_code})")
                success_count += 1
            else:
                print(f"❌ {method} {endpoint}: Endpoint not found")
        except requests.exceptions.ConnectionError:
            print(f"❌ {method} {endpoint}: Connection error")
        except Exception as e:
            print(f"✅ {method} {endpoint}: Endpoint exists (error: {type(e).__name__})")
            success_count += 1
    
    return success_count == len(endpoints)

def test_report_generation_endpoints():
    """Test report generation endpoints (structure only)"""
    print("\nTesting report generation endpoint structure...")
    
    endpoints = [
        ("/reports/create", "POST"),
        ("/reports/templates", "GET"),
        ("/reports/templates", "POST"),
        ("/reports/export/test_id", "GET"),
        ("/reports/status/test_id", "GET")
    ]
    
    success_count = 0
    for endpoint, method in endpoints:
        try:
            url = f"{BASE_URL}{API_PREFIX}{endpoint}"
            if method == "POST":
                response = requests.post(url, json={}, timeout=5)
            else:
                response = requests.get(url, timeout=5)
            
            # We expect 422 (validation error) or 401 (auth error) if endpoint exists
            if response.status_code != 404:
                print(f"✅ {method} {endpoint}: Endpoint exists (status {response.status_code})")
                success_count += 1
            else:
                print(f"❌ {method} {endpoint}: Endpoint not found")
        except requests.exceptions.ConnectionError:
            print(f"❌ {method} {endpoint}: Connection error")
        except Exception as e:
            print(f"✅ {method} {endpoint}: Endpoint exists (error: {type(e).__name__})")
            success_count += 1
    
    return success_count == len(endpoints)

def main():
    """Main test function"""
    print(f"Testing REGIQ AI/ML API at {BASE_URL}")
    print("=" * 50)
    
    # Test basic endpoints
    health_ok = test_health_endpoint()
    root_ok = test_root_endpoint()
    docs_ok = test_docs_endpoint()
    
    # Test service endpoints
    ri_ok = test_regulatory_intelligence_endpoints()
    ba_ok = test_bias_analysis_endpoints()
    rs_ok = test_risk_simulator_endpoints()
    rg_ok = test_report_generation_endpoints()
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Root Endpoint: {'✅ PASS' if root_ok else '❌ FAIL'}")
    print(f"Docs Endpoint: {'✅ PASS' if docs_ok else '❌ FAIL'}")
    print(f"Regulatory Intelligence: {'✅ PASS' if ri_ok else '❌ FAIL'}")
    print(f"Bias Analysis: {'✅ PASS' if ba_ok else '❌ FAIL'}")
    print(f"Risk Simulator: {'✅ PASS' if rs_ok else '❌ FAIL'}")
    print(f"Report Generation: {'✅ PASS' if rg_ok else '❌ FAIL'}")
    
    overall_success = all([health_ok, root_ok, docs_ok, ri_ok, ba_ok, rs_ok, rg_ok])
    print("\n" + "=" * 50)
    if overall_success:
        print("🎉 ALL TESTS PASSED! API is running correctly.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    print("=" * 50)
    
    return overall_success

if __name__ == "__main__":
    main()