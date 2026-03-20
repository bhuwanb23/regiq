"""
Quick Test: Bias Mitigation Models

Tests saving and loading of fairness models.
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "services"))

from bias_analysis.utils.fairness_model_persistence import FairnessModelPersistence


def test_fairness_persistence():
    """Test fairness model persistence."""
    print("\n" + "="*60)
    print("BIAS & FAIRNESS MODEL PERSISTENCE TEST")
    print("="*60)
    
    fp = FairnessModelPersistence()
    
    # List available models
    print("\n📂 Available Models:")
    available = fp.list_available_models()
    
    for category, models in available.items():
        if models:
            print(f"\n{category}:")
            for model in models:
                print(f"  - {model}")
    
    if not any(available.values()):
        print("\n⚠️ No models found yet. Run train_mitigation_models.py first!")
        return
    
    # Test loading each type
    print("\n🧪 Testing Model Loading:")
    
    # Preprocessing
    try:
        reweight, meta = fp.load_mitigation_model('sample_reweighting', 'preprocessing')
        print(f"✅ Sample Reweighting loaded (improvement: {meta.get('improvement', 0):.2%})")
    except Exception as e:
        print(f"❌ Sample Reweighting failed: {e}")
    
    # Post-processing
    try:
        threshold, meta = fp.load_mitigation_model('threshold_adjustment', 'post_processing')
        print(f"✅ Threshold Adjustment loaded (improvement: {meta.get('improvement', 0):.2%})")
    except Exception as e:
        print(f"❌ Threshold Adjustment failed: {e}")

    # Test metrics loading
    print("\n📊 Testing Metrics Loading:")
    try:
        # Try to load any available metrics
        metrics_list = available.get('metrics', [])
        if metrics_list:
            for model_name in metrics_list:
                metrics = fp.load_fairness_metrics(model_name)
                print(f"✅ Loaded metrics for {model_name}")
        else:
            print("⚠️ No precomputed metrics found")
    except Exception as e:
        print(f"❌ Metrics loading failed: {e}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)


if __name__ == "__main__":
    test_fairness_persistence()
