#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 3.3 Fast Test Suite
Quick tests for SHAP, LIME, and Feature Attribution.
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
import time
import warnings

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

def test_shap_basic():
    """Test basic SHAP functionality."""
    print("\n🔍 Testing SHAP Basic...")
    
    try:
        from services.bias_analysis.explainability.shap_integration import SHAPExplainer, SHAPConfig
        
        # Quick test with minimal data
        config = SHAPConfig(max_samples=50, background_samples=20)
        explainer = SHAPExplainer(config)
        print("✅ SHAP explainer created")
        
        # Minimal test data
        np.random.seed(42)
        X = np.random.randn(50, 3)
        y = np.random.binomial(1, 0.6, 50)
        
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X, y)
        
        # Test explainer creation
        shap_explainer = explainer.create_explainer(model, X)
        print("✅ SHAP explainer created for model")
        
        # Test explanation generation
        explanation = explainer.explain_prediction(shap_explainer, X[:2])
        print("✅ SHAP explanation generated")
        print(f"   - Model type: {explanation.model_type}")
        print(f"   - Features: {len(explanation.feature_names)}")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  SHAP not available: {e}")
        return False
    except Exception as e:
        print(f"❌ SHAP basic test failed: {e}")
        return False


def test_lime_basic():
    """Test basic LIME functionality."""
    print("\n🔍 Testing LIME Basic...")
    
    try:
        from services.bias_analysis.explainability.lime_implementation import LIMEExplainer, LIMEConfig
        
        # Quick test with minimal data
        config = LIMEConfig(num_features=3, num_samples=500)
        explainer = LIMEExplainer(config)
        print("✅ LIME explainer created")
        
        # Minimal test data
        np.random.seed(42)
        X = np.random.randn(50, 3)
        y = np.random.binomial(1, 0.6, 50)
        
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X, y)
        
        # Test explainer creation
        lime_explainer = explainer.create_tabular_explainer(X)
        print("✅ LIME tabular explainer created")
        
        # Test explanation generation
        instance = X[0]
        explanation = explainer.explain_instance(lime_explainer, model, instance)
        print("✅ LIME explanation generated")
        print(f"   - Model type: {explanation.model_type}")
        print(f"   - Features: {len(explanation.feature_names)}")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  LIME not available: {e}")
        return False
    except Exception as e:
        print(f"❌ LIME basic test failed: {e}")
        return False


def test_feature_attribution_basic():
    """Test basic feature attribution functionality."""
    print("\n🔍 Testing Feature Attribution Basic...")
    
    try:
        from services.bias_analysis.explainability.feature_attribution import FeatureAttributionAnalyzer, AttributionConfig
        
        # Quick test with minimal data
        config = AttributionConfig(n_permutations=3, top_k=3)
        analyzer = FeatureAttributionAnalyzer(config)
        print("✅ Feature attribution analyzer created")
        
        # Minimal test data
        np.random.seed(42)
        X = np.random.randn(50, 3)
        y = np.random.binomial(1, 0.6, 50)
        
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X, y)
        
        # Test feature attribution calculation
        attribution = analyzer.calculate_feature_importance(model, X, y)
        print("✅ Feature attribution calculated")
        print(f"   - Model type: {attribution.model_type}")
        print(f"   - Features: {len(attribution.feature_names)}")
        print(f"   - Top features: {[item[0] for item in attribution.feature_rankings[:2]]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Feature attribution basic test failed: {e}")
        return False


def test_explainability_imports():
    """Test that all explainability modules can be imported."""
    print("\n🔍 Testing Explainability Imports...")
    
    try:
        # Test SHAP import
        try:
            from services.bias_analysis.explainability.shap_integration import SHAPExplainer
            print("✅ SHAP module imported")
        except ImportError as e:
            print(f"⚠️  SHAP import failed: {e}")
        
        # Test LIME import
        try:
            from services.bias_analysis.explainability.lime_implementation import LIMEExplainer
            print("✅ LIME module imported")
        except ImportError as e:
            print(f"⚠️  LIME import failed: {e}")
        
        # Test Feature Attribution import
        from services.bias_analysis.explainability.feature_attribution import FeatureAttributionAnalyzer
        print("✅ Feature Attribution module imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def test_configuration():
    """Test configuration objects."""
    print("\n🔍 Testing Configuration...")
    
    try:
        # Test SHAP config
        from services.bias_analysis.explainability.shap_integration import SHAPConfig
        shap_config = SHAPConfig(max_samples=100, background_samples=50)
        print("✅ SHAP configuration created")
        
        # Test LIME config
        from services.bias_analysis.explainability.lime_implementation import LIMEConfig
        lime_config = LIMEConfig(num_features=5, num_samples=1000)
        print("✅ LIME configuration created")
        
        # Test Attribution config
        from services.bias_analysis.explainability.feature_attribution import AttributionConfig
        attr_config = AttributionConfig(n_permutations=5, top_k=5)
        print("✅ Attribution configuration created")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def main():
    """Run fast Phase 3.3 tests."""
    print("🧪 Phase 3.3 Fast Test Suite")
    print("=" * 40)
    
    test_results = []
    
    # Run fast tests
    test_results.append(("SHAP Basic", test_shap_basic()))
    test_results.append(("LIME Basic", test_lime_basic()))
    test_results.append(("Feature Attribution Basic", test_feature_attribution_basic()))
    test_results.append(("Explainability Imports", test_explainability_imports()))
    test_results.append(("Configuration", test_configuration()))
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 Fast Test Results:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All Phase 3.3 fast tests passed!")
    else:
        print("⚠️  Some tests failed. Check dependencies and implementation.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
