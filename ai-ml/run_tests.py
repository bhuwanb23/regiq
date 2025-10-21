#!/usr/bin/env python3
"""
REGIQ AI/ML Test Runner
Comprehensive test runner with different test suites and reporting.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        print(f"✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED (exit code: {e.returncode})")
        return False


def run_unit_tests():
    """Run unit tests."""
    cmd = "pytest tests/unit/ -v --tb=short"
    return run_command(cmd, "Unit Tests")


def run_integration_tests():
    """Run integration tests."""
    cmd = "pytest tests/integration/ -v --tb=short -m integration"
    return run_command(cmd, "Integration Tests")


def run_e2e_tests():
    """Run end-to-end tests."""
    cmd = "pytest tests/e2e/ -v --tb=short -m e2e"
    return run_command(cmd, "End-to-End Tests")


def run_performance_tests():
    """Run performance tests."""
    cmd = "pytest tests/performance/ -v --tb=short -m performance"
    return run_command(cmd, "Performance Tests")


def run_api_tests():
    """Run API-specific tests."""
    cmd = "pytest -v --tb=short -m api"
    return run_command(cmd, "API Tests")


def run_database_tests():
    """Run database-specific tests."""
    cmd = "pytest -v --tb=short -m database"
    return run_command(cmd, "Database Tests")


def run_smoke_tests():
    """Run smoke tests."""
    cmd = "pytest -v --tb=short -m smoke"
    return run_command(cmd, "Smoke Tests")


def run_all_tests():
    """Run all tests."""
    cmd = "pytest tests/ -v --tb=short --cov=config --cov=services --cov-report=html --cov-report=term"
    return run_command(cmd, "All Tests with Coverage")


def run_quick_tests():
    """Run quick tests (unit + smoke)."""
    cmd = "pytest tests/unit/ -v --tb=short -m 'not slow'"
    return run_command(cmd, "Quick Tests (Unit + Fast)")


def run_load_tests():
    """Run load tests."""
    cmd = "pytest tests/performance/ -v --tb=short --run-load-tests"
    return run_command(cmd, "Load Tests")


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="REGIQ AI/ML Test Runner")
    parser.add_argument("--suite", choices=[
        "unit", "integration", "e2e", "performance", "api", "database", 
        "smoke", "all", "quick", "load"
    ], default="quick", help="Test suite to run")
    
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Generate coverage report")
    parser.add_argument("--parallel", "-p", action="store_true", help="Run tests in parallel")
    
    args = parser.parse_args()
    
    print("🚀 REGIQ AI/ML Test Runner")
    print("="*60)
    print(f"Test Suite: {args.suite}")
    print(f"Verbose: {args.verbose}")
    print(f"Coverage: {args.coverage}")
    print(f"Parallel: {args.parallel}")
    
    # Test suite mapping
    test_functions = {
        "unit": run_unit_tests,
        "integration": run_integration_tests,
        "e2e": run_e2e_tests,
        "performance": run_performance_tests,
        "api": run_api_tests,
        "database": run_database_tests,
        "smoke": run_smoke_tests,
        "all": run_all_tests,
        "quick": run_quick_tests,
        "load": run_load_tests
    }
    
    # Run selected test suite
    test_func = test_functions.get(args.suite)
    if test_func:
        success = test_func()
        
        if success:
            print(f"\n🎉 {args.suite.upper()} TESTS PASSED!")
            sys.exit(0)
        else:
            print(f"\n❌ {args.suite.upper()} TESTS FAILED!")
            sys.exit(1)
    else:
        print(f"❌ Unknown test suite: {args.suite}")
        sys.exit(1)


if __name__ == "__main__":
    main()
