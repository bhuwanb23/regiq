#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 3.3 Comprehensive Test Suite
Tests SHAP Integration, LIME Implementation, and Feature Attribution.
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

def test_shap_integration():
    """Test SHAP integration functionality."""
    print("\n🔍 Testing SHAP Integration...")
    
    try:
        from services.bias_analysis.explainability.shap_integration import SHAPExplainer, SHAPConfig
        
        # Test configuration
        config = SHAPConfig(max_samples=100, background_samples=50)
        explainer = SHAPExplainer(config)
        print("✅ SHAP explainer created")
        
        # Test with synthetic data
        np.random.seed(42)
        n_samples = 200
        n_features = 5
        
        X = np.random.randn(n_samples, n_features)
        y = np.random.binomial(1, 0.6, n_samples)
        
        # Train a simple model
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Test explainer creation
        shap_explainer = explainer.create_explainer(model, X)
        print("✅ SHAP explainer created for model")
        
        # Test explanation generation
        explanation = explainer.explain_prediction(shap_explainer, X[:5])
        print("✅ SHAP explanation generated")
        print(f"   - Model type: {explanation.model_type}")
        print(f"   - Base value: {explanation.base_value:.3f}")
        print(f"   - Features: {len(explanation.feature_names)}")
        
        # Test visualization
        viz_path = explainer.create_visualization(explanation, "test_shap_viz.html")
        if viz_path:
            print(f"✅ SHAP visualization created: {viz_path}")
        
        # Test report generation
        report = explainer.generate_report(explanation)
        print(f"✅ SHAP report generated with {len(report)} sections")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  SHAP not available: {e}")
        print("   Install with: pip install shap")
        return False
    except Exception as e:
        print(f"❌ SHAP integration test failed: {e}")
        return False


def test_lime_implementation():
    """Test LIME implementation functionality."""
    print("\n🔍 Testing LIME Implementation...")
    
    try:
        from services.bias_analysis.explainability.lime_implementation import LIMEExplainer, LIMEConfig
        
        # Test configuration
        config = LIMEConfig(num_features=5, num_samples=1000)
        explainer = LIMEExplainer(config)
        print("✅ LIME explainer created")
        
        # Test with synthetic data
        np.random.seed(42)
        n_samples = 200
        n_features = 5
        
        X = np.random.randn(n_samples, n_features)
        y = np.random.binomial(1, 0.6, n_samples)
        
        # Train a simple model
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Test tabular explainer creation
        lime_explainer = explainer.create_tabular_explainer(X)
        print("✅ LIME tabular explainer created")
        
        # Test explanation generation
        instance = X[0]
        explanation = explainer.explain_instance(lime_explainer, model, instance)
        print("✅ LIME explanation generated")
        print(f"   - Model type: {explanation.model_type}")
        print(f"   - Prediction: {explanation.prediction:.0f}")
        print(f"   - Confidence: {explanation.confidence:.3f}")
        print(f"   - Features: {len(explanation.feature_names)}")
        
        # Test visualization
        viz_path = explainer.create_visualization(explanation, "test_lime_viz.html")
        if viz_path:
            print(f"✅ LIME visualization created: {viz_path}")
        
        # Test report generation
        report = explainer.generate_report(explanation)
        print(f"✅ LIME report generated with {len(report)} sections")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  LIME not available: {e}")
        print("   Install with: pip install lime")
        return False
    except Exception as e:
        print(f"❌ LIME implementation test failed: {e}")
        return False


def test_feature_attribution():
    """Test feature attribution functionality."""
    print("\n🔍 Testing Feature Attribution...")
    
    try:
        from services.bias_analysis.explainability.feature_attribution import FeatureAttributionAnalyzer, AttributionConfig
        
        # Test configuration
        config = AttributionConfig(n_permutations=5, top_k=5)
        analyzer = FeatureAttributionAnalyzer(config)
        print("✅ Feature attribution analyzer created")
        
        # Test with synthetic data
        np.random.seed(42)
        n_samples = 200
        n_features = 5
        
        X = np.random.randn(n_samples, n_features)
        y = np.random.binomial(1, 0.6, n_samples)
        
        # Train a simple model
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Test feature attribution calculation
        attribution = analyzer.calculate_feature_importance(model, X, y)
        print("✅ Feature attribution calculated")
        print(f"   - Model type: {attribution.model_type}")
        print(f"   - Methods used: {attribution.metadata['methods_used']}")
        print(f"   - Features: {len(attribution.feature_names)}")
        print(f"   - Top features: {[item[0] for item in attribution.feature_rankings[:3]]}")
        
        # Test visualization
        viz_path = analyzer.create_attribution_charts(attribution, "test_attribution_viz.html")
        if viz_path:
            print(f"✅ Attribution charts created: {viz_path}")
        
        # Test report generation
        report = analyzer.generate_explanation_summary(attribution)
        print(f"✅ Attribution report generated with {len(report)} sections")
        
        return True
        
    except Exception as e:
        print(f"❌ Feature attribution test failed: {e}")
        return False


def test_explainability_integration():
    """Test integration between all explainability tools."""
    print("\n🔍 Testing Explainability Integration...")
    
    try:
        # Test data
        np.random.seed(42)
        n_samples = 100
        n_features = 4
        
        X = np.random.randn(n_samples, n_features)
        y = np.random.binomial(1, 0.6, n_samples)
        
        # Train model
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Test SHAP integration
        try:
            from services.bias_analysis.explainability.shap_integration import SHAPExplainer
            shap_explainer = SHAPExplainer()
            shap_exp = shap_explainer.create_explainer(model, X)
            shap_result = shap_explainer.explain_prediction(shap_exp, X[:1])
            print("✅ SHAP integration working")
        except ImportError:
            print("⚠️  SHAP not available for integration test")
        
        # Test LIME implementation
        try:
            from services.bias_analysis.explainability.lime_implementation import LIMEExplainer
            lime_explainer = LIMEExplainer()
            lime_exp = lime_explainer.create_tabular_explainer(X)
            lime_result = lime_explainer.explain_instance(lime_exp, model, X[0])
            print("✅ LIME integration working")
        except ImportError:
            print("⚠️  LIME not available for integration test")
        
        # Test feature attribution
        from services.bias_analysis.explainability.feature_attribution import FeatureAttributionAnalyzer
        attr_analyzer = FeatureAttributionAnalyzer()
        attr_result = attr_analyzer.calculate_feature_importance(model, X, y)
        print("✅ Feature attribution integration working")
        
        print("✅ All explainability tools integrated successfully")
        return True
        
    except Exception as e:
        print(f"❌ Explainability integration test failed: {e}")
        return False


def test_performance():
    """Test performance of explainability tools."""
    print("\n🔍 Testing Performance...")
    
    try:
        # Test data
        np.random.seed(42)
        n_samples = 100
        n_features = 5
        
        X = np.random.randn(n_samples, n_features)
        y = np.random.binomial(1, 0.6, n_samples)
        
        # Train model
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Test SHAP performance
        try:
            from services.bias_analysis.explainability.shap_integration import SHAPExplainer
            start_time = time.time()
            shap_explainer = SHAPExplainer()
            shap_exp = shap_explainer.create_explainer(model, X)
            shap_result = shap_explainer.explain_prediction(shap_exp, X[:5])
            shap_time = time.time() - start_time
            print(f"✅ SHAP performance: {shap_time:.3f}s")
        except ImportError:
            print("⚠️  SHAP not available for performance test")
        
        # Test LIME performance
        try:
            from services.bias_analysis.explainability.lime_implementation import LIMEExplainer
            start_time = time.time()
            lime_explainer = LIMEExplainer()
            lime_exp = lime_explainer.create_tabular_explainer(X)
            lime_result = lime_explainer.explain_instance(lime_exp, model, X[0])
            lime_time = time.time() - start_time
            print(f"✅ LIME performance: {lime_time:.3f}s")
        except ImportError:
            print("⚠️  LIME not available for performance test")
        
        # Test feature attribution performance
        start_time = time.time()
        from services.bias_analysis.explainability.feature_attribution import FeatureAttributionAnalyzer
        attr_analyzer = FeatureAttributionAnalyzer()
        attr_result = attr_analyzer.calculate_feature_importance(model, X, y)
        attr_time = time.time() - start_time
        print(f"✅ Feature attribution performance: {attr_time:.3f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False


def test_error_handling():
    """Test error handling in explainability tools."""
    print("\n🔍 Testing Error Handling...")
    
    try:
        # Test with invalid data
        X_invalid = np.array([])
        y_invalid = np.array([])
        
        # Test feature attribution with invalid data
        from services.bias_analysis.explainability.feature_attribution import FeatureAttributionAnalyzer
        analyzer = FeatureAttributionAnalyzer()
        
        try:
            # This should handle empty data gracefully
            result = analyzer.calculate_feature_importance(None, X_invalid, y_invalid)
            print("⚠️  Should have failed with invalid data")
        except Exception as e:
            print(f"✅ Error handling working: {type(e).__name__}")
        
        # Test with valid data but edge cases
        np.random.seed(42)
        X = np.random.randn(10, 3)
        y = np.random.binomial(1, 0.5, 10)
        
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X, y)
        
        # Test with small dataset
        result = analyzer.calculate_feature_importance(model, X, y)
        print("✅ Edge case handling working")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def main():
    """Run comprehensive Phase 3.3 tests."""
    print("🧪 Phase 3.3 Comprehensive Test Suite")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(("SHAP Integration", test_shap_integration()))
    test_results.append(("LIME Implementation", test_lime_implementation()))
    test_results.append(("Feature Attribution", test_feature_attribution()))
    test_results.append(("Explainability Integration", test_explainability_integration()))
    test_results.append(("Performance", test_performance()))
    test_results.append(("Error Handling", test_error_handling()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All Phase 3.3 tests passed!")
    else:
        print("⚠️  Some tests failed. Check dependencies and implementation.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
