#!/usr/bin/env python3
"""
Fast Test Suite for Phase 3.2: Fairness Metrics
Optimized for speed with smaller datasets and essential tests only.
"""

import sys
import os
import tempfile
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))


def test_demographic_parity_fast():
    print("\n📊 Testing Demographic Parity (Fast)...")
    from services.bias_analysis.metrics.demographic_parity import (
        DemographicParityAnalyzer, ParityThreshold, DemographicParityResult
    )
    
    # Test with small dataset
    np.random.seed(42)
    n_samples = 200
    
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.zeros(n_samples)
    
    # Create bias
    male_mask = gender == 'male'
    y_pred[male_mask] = np.random.binomial(1, 0.7, np.sum(male_mask))
    female_mask = gender == 'female'
    y_pred[female_mask] = np.random.binomial(1, 0.5, np.sum(female_mask))
    
    # Test calculation
    analyzer = DemographicParityAnalyzer()
    result = analyzer.calculate_demographic_parity(y_true, y_pred, gender)
    
    assert result.parity_score >= 0.0 and result.parity_score <= 1.0
    assert len(result.groups) == 2
    print(f"✅ Demographic parity: {result.parity_score:.3f}")


def test_equalized_odds_fast():
    print("\n⚖️ Testing Equalized Odds (Fast)...")
    from services.bias_analysis.metrics.equalized_odds import (
        EqualizedOddsAnalyzer, EqualizedOddsThreshold, EqualizedOddsResult
    )
    
    # Test with small dataset
    np.random.seed(42)
    n_samples = 200
    
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.zeros(n_samples)
    
    # Create bias
    male_mask = gender == 'male'
    y_pred[male_mask] = np.where(y_true[male_mask] == 1, 
                                np.random.binomial(1, 0.8, np.sum(male_mask)),
                                np.random.binomial(1, 0.2, np.sum(male_mask)))
    
    female_mask = gender == 'female'
    y_pred[female_mask] = np.where(y_true[female_mask] == 1,
                                  np.random.binomial(1, 0.6, np.sum(female_mask)),
                                  np.random.binomial(1, 0.4, np.sum(female_mask)))
    
    # Test calculation
    analyzer = EqualizedOddsAnalyzer()
    result = analyzer.calculate_equalized_odds(y_true, y_pred, gender)
    
    assert result.equalized_odds_score >= 0.0 and result.equalized_odds_score <= 1.0
    assert len(result.groups) == 2
    print(f"✅ Equalized odds: {result.equalized_odds_score:.3f}")


def test_calibration_fast():
    print("\n🎯 Testing Calibration (Fast)...")
    from services.bias_analysis.metrics.calibration_analysis import (
        CalibrationAnalyzer, CalibrationThreshold, CalibrationResult
    )
    
    # Test with small dataset
    np.random.seed(42)
    n_samples = 200
    
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_prob = np.random.beta(3, 2, n_samples)
    
    # Add group bias
    male_mask = gender == 'male'
    y_prob[male_mask] = np.random.beta(3, 2, np.sum(male_mask))
    female_mask = gender == 'female'
    y_prob[female_mask] = np.random.beta(1, 4, np.sum(female_mask))
    
    # Test calculation
    analyzer = CalibrationAnalyzer()
    result = analyzer.calculate_calibration_metrics(y_true, y_prob, gender)
    
    assert result.calibration_quality in ["excellent", "good", "fair", "poor"]
    assert len(result.groups) == 2
    print(f"✅ Calibration quality: {result.calibration_quality}")


def test_individual_fairness_fast():
    print("\n👤 Testing Individual Fairness (Fast)...")
    from services.bias_analysis.metrics.individual_fairness import (
        IndividualFairnessAnalyzer, IndividualFairnessThreshold, IndividualFairnessResult
    )
    
    # Test with small dataset (but large enough for groups)
    np.random.seed(42)
    n_samples = 100  # Small but sufficient for groups
    
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    X = np.random.randn(n_samples, 2)  # Only 2 features
    y_pred = np.zeros(n_samples)
    
    # Create bias
    male_mask = gender == 'male'
    y_pred[male_mask] = np.random.binomial(1, 0.7, np.sum(male_mask))
    female_mask = gender == 'female'
    y_pred[female_mask] = np.random.binomial(1, 0.5, np.sum(female_mask))
    
    # Test calculation
    analyzer = IndividualFairnessAnalyzer()
    result = analyzer.calculate_individual_fairness(X, y_pred, gender)
    
    assert result.overall_consistency >= 0.0 and result.overall_consistency <= 1.0
    assert len(result.groups) == 2
    print(f"✅ Individual fairness: {result.overall_consistency:.3f}")


def test_integration_fast():
    print("\n🔄 Testing Integration (Fast)...")
    from services.bias_analysis.metrics.demographic_parity import DemographicParityAnalyzer
    from services.bias_analysis.metrics.equalized_odds import EqualizedOddsAnalyzer
    from services.bias_analysis.metrics.calibration_analysis import CalibrationAnalyzer
    from services.bias_analysis.metrics.individual_fairness import IndividualFairnessAnalyzer
    
    # Test all analyzers with small dataset
    np.random.seed(42)
    n_samples = 100
    
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.random.binomial(1, 0.7, n_samples)
    y_prob = np.random.beta(3, 2, n_samples)
    X = np.random.randn(n_samples, 2)
    
    # Test all analyzers
    dp_analyzer = DemographicParityAnalyzer()
    eo_analyzer = EqualizedOddsAnalyzer()
    cal_analyzer = CalibrationAnalyzer()
    if_analyzer = IndividualFairnessAnalyzer()
    
    # Quick tests
    dp_result = dp_analyzer.calculate_demographic_parity(y_true, y_pred, gender)
    eo_result = eo_analyzer.calculate_equalized_odds(y_true, y_pred, gender)
    cal_result = cal_analyzer.calculate_calibration_metrics(y_true, y_prob, gender)
    if_result = if_analyzer.calculate_individual_fairness(X, y_pred, gender)
    
    assert dp_result.parity_score >= 0.0
    assert eo_result.equalized_odds_score >= 0.0
    assert cal_result.calibration_quality in ["excellent", "good", "fair", "poor"]
    assert if_result.overall_consistency >= 0.0
    
    print("✅ All fairness metrics integration works")


def main():
    print("🚀 Phase 3.2 Fast Test Suite")
    print("=" * 40)
    
    test_demographic_parity_fast()
    test_equalized_odds_fast()
    test_calibration_fast()
    test_individual_fairness_fast()
    test_integration_fast()
    
    print("\n🎉 Phase 3.2 fast tests completed!")
    print("=" * 40)


if __name__ == "__main__":
    main()
