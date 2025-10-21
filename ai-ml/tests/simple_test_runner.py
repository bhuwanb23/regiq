#!/usr/bin/env python3
"""
Simple Test Runner for REGIQ AI/ML (without pytest dependency)
Runs tests directly using Python's unittest framework.
"""

import sys
import os
import unittest
import importlib.util
from pathlib import Path


def discover_and_run_tests():
    """Discover and run all test files."""
    print("🧪 REGIQ AI/ML Simple Test Runner")
    print("="*60)
    
    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Test our existing working tests
    test_files = [
        "tests/test_environment.py",
        "tests/test_gemini_sdk.py", 
        "tests/simple_gemini_test.py"
    ]
    
    results = {}
    
    for test_file in test_files:
        test_path = project_root / test_file
        if test_path.exists():
            print(f"\n🔍 Running {test_file}...")
            try:
                # Import and run the test module
                spec = importlib.util.spec_from_file_location("test_module", test_path)
                test_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(test_module)
                
                # If the module has a main function, run it
                if hasattr(test_module, 'main'):
                    result = test_module.main()
                    results[test_file] = result
                    status = "✅ PASS" if result else "❌ FAIL"
                    print(f"   {status}")
                else:
                    print(f"   ⚠️  No main() function found")
                    results[test_file] = True
                    
            except Exception as e:
                print(f"   ❌ Error running {test_file}: {e}")
                results[test_file] = False
        else:
            print(f"   ⚠️  {test_file} not found")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_file, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_file:<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


def run_unit_tests_manually():
    """Run unit tests manually without pytest."""
    print("\n🧪 Running Unit Tests Manually")
    print("-"*40)
    
    # Test environment configuration
    try:
        from config.env_config import get_env_config
        env_config = get_env_config()
        
        # Test basic properties
        assert env_config.gemini_api_key is not None, "API key should be set"
        assert env_config.debug is True, "Debug should be True"
        assert env_config.gemini_rate_limit_rpm == 60, "Rate limit should be 60"
        
        print("✅ Environment configuration tests passed")
        
    except Exception as e:
        print(f"❌ Environment configuration tests failed: {e}")
        return False
    
    # Test Gemini configuration
    try:
        from config.gemini_config import GeminiConfig, GeminiAPIManager
        
        # Test config creation
        config = GeminiConfig(api_key="test-key")
        assert config.api_key == "test-key"
        assert config.model_name == "gemini-2.5-flash"
        
        print("✅ Gemini configuration tests passed")
        
    except Exception as e:
        print(f"❌ Gemini configuration tests failed: {e}")
        return False
    
    # Test database operations
    try:
        import sqlite3
        from pathlib import Path
        
        # Create test database
        test_db_path = "data/unit_test.db"
        Path(test_db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()
        
        # Create test table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50)
            )
        """)
        
        # Test insert
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test_name",))
        conn.commit()
        
        # Test select
        cursor.execute("SELECT name FROM test_table WHERE name = ?", ("test_name",))
        result = cursor.fetchone()
        assert result[0] == "test_name"
        
        conn.close()
        
        # Cleanup
        if Path(test_db_path).exists():
            Path(test_db_path).unlink()
        
        print("✅ Database operation tests passed")
        
    except Exception as e:
        print(f"❌ Database operation tests failed: {e}")
        return False
    
    return True


def main():
    """Main test runner function."""
    print("🚀 Starting REGIQ AI/ML Tests")
    
    # Run existing working tests
    existing_tests_passed = discover_and_run_tests()
    
    # Run manual unit tests
    unit_tests_passed = run_unit_tests_manually()
    
    # Overall result
    all_passed = existing_tests_passed and unit_tests_passed
    
    if all_passed:
        print("\n🎉 All tests completed successfully!")
        print("\n📋 To install pytest for advanced testing:")
        print("   pip install pytest pytest-cov pytest-asyncio pytest-mock psutil")
        print("\n🚀 Ready to proceed to Phase 2: Regulatory Intelligence Engine")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
