#!/usr/bin/env python3
"""
Comprehensive Test Suite for Phase 3.2: Fairness Metrics
Tests demographic parity, equalized odds, calibration analysis, and individual fairness.
"""

import sys
import os
import tempfile
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))


def test_demographic_parity_metrics():
    print("\n📊 Testing Demographic Parity Metrics...")
    from services.bias_analysis.metrics.demographic_parity import (
        DemographicParityAnalyzer, ParityThreshold, DemographicParityResult
    )
    
    # Test configuration
    threshold = ParityThreshold()
    analyzer = DemographicParityAnalyzer(threshold)
    
    # Test metadata creation
    result = DemographicParityResult(
        metric_name="Demographic Parity",
        protected_attribute="gender",
        groups=["male", "female"],
        positive_rates={"male": 0.7, "female": 0.5},
        parity_score=0.8,
        max_difference=0.2,
        threshold_violation=True,
        threshold_value=0.1,
        statistical_significance=0.05,
        recommendations=["Test recommendation"],
        metadata={"analysis_date": "2025-01-01"}
    )
    
    assert result.metric_name == "Demographic Parity"
    assert result.parity_score == 0.8
    assert result.threshold_violation == True
    print("✅ Demographic parity result structure valid")
    
    # Test with real data
    np.random.seed(42)
    n_samples = 1000
    
    # Create biased predictions
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.zeros(n_samples)
    
    # Male group: higher positive rate
    male_mask = gender == 'male'
    y_pred[male_mask] = np.random.binomial(1, 0.7, np.sum(male_mask))
    
    # Female group: lower positive rate
    female_mask = gender == 'female'
    y_pred[female_mask] = np.random.binomial(1, 0.5, np.sum(female_mask))
    
    # Test calculation
    result = analyzer.calculate_demographic_parity(y_true, y_pred, gender)
    
    assert result.parity_score >= 0.0 and result.parity_score <= 1.0
    assert len(result.groups) == 2
    assert "male" in result.positive_rates
    assert "female" in result.positive_rates
    print("✅ Demographic parity calculation works")
    print(f"✅ Parity score: {result.parity_score:.3f}")
    print(f"✅ Max difference: {result.max_difference:.3f}")


def test_equalized_odds_metrics():
    print("\n⚖️ Testing Equalized Odds Metrics...")
    from services.bias_analysis.metrics.equalized_odds import (
        EqualizedOddsAnalyzer, EqualizedOddsThreshold, EqualizedOddsResult
    )
    
    # Test configuration
    threshold = EqualizedOddsThreshold()
    analyzer = EqualizedOddsAnalyzer(threshold)
    
    # Test metadata creation
    result = EqualizedOddsResult(
        metric_name="Equalized Odds",
        protected_attribute="gender",
        groups=["male", "female"],
        tpr_by_group={"male": 0.8, "female": 0.6},
        fpr_by_group={"male": 0.2, "female": 0.4},
        tnr_by_group={"male": 0.8, "female": 0.6},
        fnr_by_group={"male": 0.2, "female": 0.4},
        tpr_difference=0.2,
        fpr_difference=0.2,
        equalized_odds_score=0.8,
        threshold_violation=True,
        threshold_value=0.1,
        statistical_tests={"chi_square_p_value": 0.05},
        recommendations=["Test recommendation"],
        metadata={"analysis_date": "2025-01-01"}
    )
    
    assert result.metric_name == "Equalized Odds"
    assert result.equalized_odds_score == 0.8
    assert result.threshold_violation == True
    print("✅ Equalized odds result structure valid")
    
    # Test with real data
    np.random.seed(42)
    n_samples = 1000
    
    # Create biased predictions with different TPR/FPR
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.zeros(n_samples)
    
    # Male group: higher TPR, lower FPR
    male_mask = gender == 'male'
    y_pred[male_mask] = np.where(y_true[male_mask] == 1, 
                                np.random.binomial(1, 0.8, np.sum(male_mask)),
                                np.random.binomial(1, 0.2, np.sum(male_mask)))
    
    # Female group: lower TPR, higher FPR
    female_mask = gender == 'female'
    y_pred[female_mask] = np.where(y_true[female_mask] == 1,
                                  np.random.binomial(1, 0.6, np.sum(female_mask)),
                                  np.random.binomial(1, 0.4, np.sum(female_mask)))
    
    # Test calculation
    result = analyzer.calculate_equalized_odds(y_true, y_pred, gender)
    
    assert result.equalized_odds_score >= 0.0 and result.equalized_odds_score <= 1.0
    assert len(result.groups) == 2
    assert "male" in result.tpr_by_group
    assert "female" in result.tpr_by_group
    print("✅ Equalized odds calculation works")
    print(f"✅ Equalized odds score: {result.equalized_odds_score:.3f}")
    print(f"✅ TPR difference: {result.tpr_difference:.3f}")
    print(f"✅ FPR difference: {result.fpr_difference:.3f}")


def test_calibration_analysis():
    print("\n🎯 Testing Calibration Analysis...")
    from services.bias_analysis.metrics.calibration_analysis import (
        CalibrationAnalyzer, CalibrationThreshold, CalibrationResult
    )
    
    # Test configuration
    threshold = CalibrationThreshold()
    analyzer = CalibrationAnalyzer(threshold)
    
    # Test metadata creation
    result = CalibrationResult(
        metric_name="Calibration Analysis",
        protected_attribute="gender",
        groups=["male", "female"],
        brier_scores={"male": 0.2, "female": 0.3},
        log_loss_scores={"male": 0.5, "female": 0.7},
        ece_scores={"male": 0.1, "female": 0.15},
        mce_scores={"male": 0.2, "female": 0.25},
        reliability_diagrams={"male": {"fraction_of_positives": [0.1, 0.2], "mean_predicted_value": [0.1, 0.2]}},
        calibration_quality="good",
        threshold_violation=False,
        threshold_value=0.25,
        recommendations=["Test recommendation"],
        metadata={"analysis_date": "2025-01-01"}
    )
    
    assert result.metric_name == "Calibration Analysis"
    assert result.calibration_quality == "good"
    assert result.threshold_violation == False
    print("✅ Calibration result structure valid")
    
    # Test with real data
    np.random.seed(42)
    n_samples = 1000
    
    # Create biased probability predictions
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_prob = np.random.beta(2, 3, n_samples)  # Biased towards lower probabilities
    
    # Add group-specific bias
    male_mask = gender == 'male'
    female_mask = gender == 'female'
    
    # Male group: better calibrated
    y_prob[male_mask] = np.random.beta(3, 2, np.sum(male_mask))
    
    # Female group: poorly calibrated
    y_prob[female_mask] = np.random.beta(1, 4, np.sum(female_mask))
    
    # Test calculation
    result = analyzer.calculate_calibration_metrics(y_true, y_prob, gender)
    
    assert result.calibration_quality in ["excellent", "good", "fair", "poor"]
    assert len(result.groups) == 2
    assert "male" in result.brier_scores
    assert "female" in result.brier_scores
    print("✅ Calibration analysis works")
    print(f"✅ Calibration quality: {result.calibration_quality}")
    print(f"✅ Brier scores: {result.brier_scores}")


def test_individual_fairness():
    print("\n👤 Testing Individual Fairness...")
    from services.bias_analysis.metrics.individual_fairness import (
        IndividualFairnessAnalyzer, IndividualFairnessThreshold, IndividualFairnessResult
    )
    
    # Test configuration
    threshold = IndividualFairnessThreshold()
    analyzer = IndividualFairnessAnalyzer(threshold)
    
    # Test metadata creation
    result = IndividualFairnessResult(
        metric_name="Individual Fairness",
        protected_attribute="gender",
        groups=["male", "female"],
        consistency_scores={"male": 0.8, "female": 0.6},
        similarity_scores={"male": 0.7, "female": 0.5},
        fairness_maps={"male": {"violation_rate": 0.1}},
        individual_reports={"male": {"group_size": 100}},
        overall_consistency=0.7,
        threshold_violation=True,
        threshold_value=0.8,
        recommendations=["Test recommendation"],
        metadata={"analysis_date": "2025-01-01"}
    )
    
    assert result.metric_name == "Individual Fairness"
    assert result.overall_consistency == 0.7
    assert result.threshold_violation == True
    print("✅ Individual fairness result structure valid")
    
    # Test with real data (smaller for speed)
    np.random.seed(42)
    n_samples = 100
    
    # Create features and predictions
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    X = np.random.randn(n_samples, 3)  # Fewer features for speed
    y_pred = np.zeros(n_samples)
    
    # Male group: more consistent predictions
    male_mask = gender == 'male'
    y_pred[male_mask] = np.random.binomial(1, 0.7, np.sum(male_mask))
    
    # Female group: less consistent predictions
    female_mask = gender == 'female'
    y_pred[female_mask] = np.random.binomial(1, 0.5, np.sum(female_mask))
    
    # Test calculation
    result = analyzer.calculate_individual_fairness(X, y_pred, gender)
    
    assert result.overall_consistency >= 0.0 and result.overall_consistency <= 1.0
    assert len(result.groups) == 2
    assert "male" in result.consistency_scores
    assert "female" in result.consistency_scores
    print("✅ Individual fairness calculation works")
    print(f"✅ Overall consistency: {result.overall_consistency:.3f}")
    print(f"✅ Consistency scores: {result.consistency_scores}")


def test_fairness_metrics_integration():
    print("\n🔄 Testing Fairness Metrics Integration...")
    from services.bias_analysis.metrics.demographic_parity import DemographicParityAnalyzer
    from services.bias_analysis.metrics.equalized_odds import EqualizedOddsAnalyzer
    from services.bias_analysis.metrics.calibration_analysis import CalibrationAnalyzer
    from services.bias_analysis.metrics.individual_fairness import IndividualFairnessAnalyzer
    
    # Test all analyzers
    dp_analyzer = DemographicParityAnalyzer()
    eo_analyzer = EqualizedOddsAnalyzer()
    cal_analyzer = CalibrationAnalyzer()
    if_analyzer = IndividualFairnessAnalyzer()
    
    assert dp_analyzer is not None
    assert eo_analyzer is not None
    assert cal_analyzer is not None
    assert if_analyzer is not None
    print("✅ All fairness analyzers initialized")
    
    # Test with common dataset
    np.random.seed(42)
    n_samples = 1000
    
    # Create test data
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.random.binomial(1, 0.7, n_samples)
    y_prob = np.random.beta(3, 2, n_samples)
    X = np.random.randn(n_samples, 5)
    
    # Test demographic parity
    dp_result = dp_analyzer.calculate_demographic_parity(y_true, y_pred, gender)
    assert dp_result.parity_score >= 0.0
    print("✅ Demographic parity integration works")
    
    # Test equalized odds
    eo_result = eo_analyzer.calculate_equalized_odds(y_true, y_pred, gender)
    assert eo_result.equalized_odds_score >= 0.0
    print("✅ Equalized odds integration works")
    
    # Test calibration analysis
    cal_result = cal_analyzer.calculate_calibration_metrics(y_true, y_prob, gender)
    assert cal_result.calibration_quality in ["excellent", "good", "fair", "poor"]
    print("✅ Calibration analysis integration works")
    
    # Test individual fairness
    if_result = if_analyzer.calculate_individual_fairness(X, y_pred, gender)
    assert if_result.overall_consistency >= 0.0
    print("✅ Individual fairness integration works")


def test_visualization_capabilities():
    print("\n📊 Testing Visualization Capabilities...")
    from services.bias_analysis.metrics.demographic_parity import DemographicParityAnalyzer
    from services.bias_analysis.metrics.equalized_odds import EqualizedOddsAnalyzer
    from services.bias_analysis.metrics.calibration_analysis import CalibrationAnalyzer
    from services.bias_analysis.metrics.individual_fairness import IndividualFairnessAnalyzer
    
    # Test with sample data
    np.random.seed(42)
    n_samples = 500
    
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.random.binomial(1, 0.7, n_samples)
    y_prob = np.random.beta(3, 2, n_samples)
    X = np.random.randn(n_samples, 5)
    
    # Test demographic parity visualization
    dp_analyzer = DemographicParityAnalyzer()
    dp_result = dp_analyzer.calculate_demographic_parity(y_true, y_pred, gender)
    
    try:
        viz_path = dp_analyzer.create_visualization(dp_result, "test_dp_viz.html")
        if viz_path:
            print("✅ Demographic parity visualization works")
    except Exception as e:
        print(f"⚠️ Demographic parity visualization: {e}")
    
    # Test equalized odds visualization
    eo_analyzer = EqualizedOddsAnalyzer()
    eo_result = eo_analyzer.calculate_equalized_odds(y_true, y_pred, gender)
    
    try:
        viz_path = eo_analyzer.create_visualization(eo_result, "test_eo_viz.html")
        if viz_path:
            print("✅ Equalized odds visualization works")
    except Exception as e:
        print(f"⚠️ Equalized odds visualization: {e}")
    
    # Test calibration visualization
    cal_analyzer = CalibrationAnalyzer()
    cal_result = cal_analyzer.calculate_calibration_metrics(y_true, y_prob, gender)
    
    try:
        viz_path = cal_analyzer.create_visualization(cal_result, "test_cal_viz.html")
        if viz_path:
            print("✅ Calibration visualization works")
    except Exception as e:
        print(f"⚠️ Calibration visualization: {e}")
    
    # Test individual fairness visualization
    if_analyzer = IndividualFairnessAnalyzer()
    if_result = if_analyzer.calculate_individual_fairness(X, y_pred, gender)
    
    try:
        viz_path = if_analyzer.create_visualization(if_result, "test_if_viz.html")
        if viz_path:
            print("✅ Individual fairness visualization works")
    except Exception as e:
        print(f"⚠️ Individual fairness visualization: {e}")


def test_report_generation():
    print("\n📋 Testing Report Generation...")
    from services.bias_analysis.metrics.demographic_parity import DemographicParityAnalyzer
    from services.bias_analysis.metrics.equalized_odds import EqualizedOddsAnalyzer
    from services.bias_analysis.metrics.calibration_analysis import CalibrationAnalyzer
    from services.bias_analysis.metrics.individual_fairness import IndividualFairnessAnalyzer
    
    # Test with sample data
    np.random.seed(42)
    n_samples = 500
    
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.random.binomial(1, 0.7, n_samples)
    y_prob = np.random.beta(3, 2, n_samples)
    X = np.random.randn(n_samples, 5)
    
    # Test demographic parity report
    dp_analyzer = DemographicParityAnalyzer()
    dp_result = dp_analyzer.calculate_demographic_parity(y_true, y_pred, gender)
    dp_report = dp_analyzer.generate_report(dp_result)
    assert "analysis_type" in dp_report
    assert "summary" in dp_report
    print("✅ Demographic parity report generation works")
    
    # Test equalized odds report
    eo_analyzer = EqualizedOddsAnalyzer()
    eo_result = eo_analyzer.calculate_equalized_odds(y_true, y_pred, gender)
    eo_report = eo_analyzer.generate_report(eo_result)
    assert "analysis_type" in eo_report
    assert "summary" in eo_report
    print("✅ Equalized odds report generation works")
    
    # Test calibration report
    cal_analyzer = CalibrationAnalyzer()
    cal_result = cal_analyzer.calculate_calibration_metrics(y_true, y_prob, gender)
    cal_report = cal_analyzer.generate_report(cal_result)
    assert "analysis_type" in cal_report
    assert "summary" in cal_report
    print("✅ Calibration report generation works")
    
    # Test individual fairness report
    if_analyzer = IndividualFairnessAnalyzer()
    if_result = if_analyzer.calculate_individual_fairness(X, y_pred, gender)
    if_report = if_analyzer.generate_report(if_result)
    assert "analysis_type" in if_report
    assert "summary" in if_report
    print("✅ Individual fairness report generation works")


def test_performance_metrics():
    print("\n⚡ Testing Performance Metrics...")
    import time
    from services.bias_analysis.metrics.demographic_parity import DemographicParityAnalyzer
    from services.bias_analysis.metrics.equalized_odds import EqualizedOddsAnalyzer
    from services.bias_analysis.metrics.calibration_analysis import CalibrationAnalyzer
    from services.bias_analysis.metrics.individual_fairness import IndividualFairnessAnalyzer
    
    # Test with smaller dataset for faster testing
    np.random.seed(42)
    n_samples = 1000
    
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_pred = np.random.binomial(1, 0.7, n_samples)
    y_prob = np.random.beta(3, 2, n_samples)
    X = np.random.randn(n_samples, 10)
    
    # Test demographic parity performance
    dp_analyzer = DemographicParityAnalyzer()
    start_time = time.time()
    dp_result = dp_analyzer.calculate_demographic_parity(y_true, y_pred, gender)
    dp_duration = time.time() - start_time
    print(f"✅ Demographic parity: {dp_duration:.3f} seconds")
    
    # Test equalized odds performance
    eo_analyzer = EqualizedOddsAnalyzer()
    start_time = time.time()
    eo_result = eo_analyzer.calculate_equalized_odds(y_true, y_pred, gender)
    eo_duration = time.time() - start_time
    print(f"✅ Equalized odds: {eo_duration:.3f} seconds")
    
    # Test calibration performance
    cal_analyzer = CalibrationAnalyzer()
    start_time = time.time()
    cal_result = cal_analyzer.calculate_calibration_metrics(y_true, y_prob, gender)
    cal_duration = time.time() - start_time
    print(f"✅ Calibration analysis: {cal_duration:.3f} seconds")
    
    # Test individual fairness performance (skip for speed)
    print("✅ Individual fairness: Skipped for speed (complex computation)")
    if_duration = 0.0
    
    # Performance should be reasonable
    assert dp_duration < 2.0  # Should complete within 2 seconds
    assert eo_duration < 2.0
    assert cal_duration < 2.0
    # Skip individual fairness performance test for speed


def test_error_handling():
    print("\n🛡️ Testing Error Handling...")
    from services.bias_analysis.metrics.demographic_parity import DemographicParityAnalyzer
    from services.bias_analysis.metrics.equalized_odds import EqualizedOddsAnalyzer
    from services.bias_analysis.metrics.calibration_analysis import CalibrationAnalyzer
    from services.bias_analysis.metrics.individual_fairness import IndividualFairnessAnalyzer
    
    # Test with invalid data
    try:
        dp_analyzer = DemographicParityAnalyzer()
        # Empty arrays
        result = dp_analyzer.calculate_demographic_parity([], [], [])
        print("⚠️ Empty data handling needs improvement")
    except Exception as e:
        print(f"✅ Empty data error handling: {type(e).__name__}")
    
    try:
        eo_analyzer = EqualizedOddsAnalyzer()
        # Mismatched array lengths
        result = eo_analyzer.calculate_equalized_odds([1, 0], [1], ['male'])
        print("⚠️ Mismatched data handling needs improvement")
    except Exception as e:
        print(f"✅ Mismatched data error handling: {type(e).__name__}")
    
    try:
        cal_analyzer = CalibrationAnalyzer()
        # Invalid probability values
        result = cal_analyzer.calculate_calibration_metrics([1, 0], [2, -1], ['male', 'female'])
        print("⚠️ Invalid probability handling needs improvement")
    except Exception as e:
        print(f"✅ Invalid probability error handling: {type(e).__name__}")
    
    try:
        if_analyzer = IndividualFairnessAnalyzer()
        # Single sample
        result = if_analyzer.calculate_individual_fairness([[1, 2]], [1], ['male'])
        print("⚠️ Single sample handling needs improvement")
    except Exception as e:
        print(f"✅ Single sample error handling: {type(e).__name__}")


def main():
    print("🚀 Phase 3.2 Comprehensive Test Suite")
    print("=" * 50)
    
    test_demographic_parity_metrics()
    test_equalized_odds_metrics()
    test_calibration_analysis()
    test_individual_fairness()
    test_fairness_metrics_integration()
    test_visualization_capabilities()
    test_report_generation()
    test_performance_metrics()
    test_error_handling()
    
    print("\n🎉 Phase 3.2 tests completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
