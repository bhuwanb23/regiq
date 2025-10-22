#!/usr/bin/env python3
"""
Quick test runner for Phase 3.4 modules.
Tests all components individually before running full integration test.
"""

import sys
from pathlib import Path

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent))

def test_all_modules():
    """Test all Phase 3.4 modules."""
    print("=" * 70)
    print("🧪 REGIQ Phase 3.4 - Bias Scoring System Test Suite")
    print("=" * 70)
    
    modules_to_test = [
        ("Scoring Algorithm", "services.bias_analysis.scoring.scoring_algorithm"),
        ("Weight Profiles", "services.bias_analysis.scoring.weight_profiles"),
        ("Composite Calculator", "services.bias_analysis.scoring.composite_calculator"),
        ("Score Interpreter", "services.bias_analysis.scoring.score_interpreter"),
        ("Risk Classifier", "services.bias_analysis.scoring.classification_engine"),
        ("Alert System", "services.bias_analysis.scoring.alert_system"),
        ("Report Generator", "services.bias_analysis.scoring.report_generator"),
    ]
    
    passed = 0
    failed = 0
    
    for name, module_path in modules_to_test:
        print(f"\n📦 Testing: {name}")
        print("-" * 70)
        
        try:
            # Import and run module
            import importlib
            module = importlib.import_module(module_path)
            
            # Run main if exists
            if hasattr(module, 'main'):
                module.main()
                print(f"✅ {name} - PASSED")
                passed += 1
            else:
                print(f"⚠️  {name} - No main() function, skipping")
        
        except Exception as e:
            print(f"❌ {name} - FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 Test Summary: {passed} passed, {failed} failed out of {len(modules_to_test)} modules")
    print("=" * 70)
    
    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = test_all_modules()
    sys.exit(exit_code)
