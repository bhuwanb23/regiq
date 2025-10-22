#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 3.4 Comprehensive Test Suite
Tests all bias scoring system components.
"""

import sys
import pytest
import numpy as np
from pathlib import Path
from typing import Dict, Any

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.bias_analysis.scoring import (
    BiasScoreAlgorithm,
    WeightProfileManager,
    BiasScoreCalculator,
    ScoreInterpreter,
    RiskLevel,
    RiskClassifier,
    BiasAlertManager,
    BiasRiskReportGenerator
)
from services.bias_analysis.scoring.scoring_algorithm import ScoringConfiguration


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_raw_metrics():
    """Sample raw fairness metrics."""
    return {
        "demographic_parity": 0.35,
        "equalized_odds": 0.52,
        "calibration": 0.28,
        "individual_fairness": 0.60
    }


@pytest.fixture
def sample_bias_score_data():
    """Sample bias score calculation results."""
    return {
        "overall_bias_score": 0.45,
        "confidence_interval": [0.42, 0.48],
        "normalized_metrics": {
            "demographic_parity": 0.35,
            "equalized_odds": 0.52,
            "calibration": 0.56,
            "individual_fairness": 0.40
        },
        "metric_contributions": {
            "demographic_parity": 0.105,
            "equalized_odds": 0.182,
            "calibration": 0.112,
            "individual_fairness": 0.060
        },
        "dominant_metric": "equalized_odds",
        "dominant_contribution": 0.182,
        "weight_profile_used": "default",
        "weights": {
            "demographic_parity": 0.30,
            "equalized_odds": 0.35,
            "calibration": 0.20,
            "individual_fairness": 0.15
        },
        "raw_metrics": {
            "demographic_parity": 0.35,
            "equalized_odds": 0.52,
            "calibration": 0.28,
            "individual_fairness": 0.60
        }
    }


@pytest.fixture
def sample_risk_classification():
    """Sample risk classification results."""
    return {
        "risk_level": "MEDIUM",
        "risk_score": 0.45,
        "urgency": "MEDIUM",
        "action_timeline": "30_days",
        "action_days": 30,
        "notification_channels": ["in_app", "email"],
        "escalation_required": False,
        "regulatory_flags": [],
        "deployment_recommendation": "Conditional - requires monitoring"
    }


@pytest.fixture
def sample_interpretation_data():
    """Sample score interpretation."""
    return {
        "severity_level": "MODERATE",
        "severity_description": "Requires attention - Moderate bias",
        "interpretation": "The model shows moderate bias requiring attention.",
        "key_concerns": [
            "Equalized odds violation (52%) exceeds threshold",
            "Calibration error (28%) is elevated"
        ]
    }


# ============================================================================
# Test 1: Scoring Algorithm
# ============================================================================

class TestBiasScoringAlgorithm:
    """Test the core bias scoring algorithm."""
    
    def test_algorithm_initialization(self):
        """Test algorithm initialization with default config."""
        algo = BiasScoreAlgorithm()
        assert algo.config is not None
        assert algo.config.demographic_parity_weight == 0.30
        assert algo.config.equalized_odds_weight == 0.35
    
    def test_normalize_demographic_parity(self):
        """Test demographic parity normalization."""
        algo = BiasScoreAlgorithm()
        
        # Test perfect fairness
        assert algo.normalize_demographic_parity(0.0) == 0.0
        
        # Test maximum difference
        assert algo.normalize_demographic_parity(1.0) == 1.0
        
        # Test mid-range
        normalized = algo.normalize_demographic_parity(0.5)
        assert 0.4 < normalized < 0.6
    
    def test_composite_score_calculation(self, sample_raw_metrics):
        """Test composite score calculation."""
        algo = BiasScoreAlgorithm()
        result = algo.calculate_composite_score(sample_raw_metrics)
        
        assert "overall_bias_score" in result
        assert 0.0 <= result["overall_bias_score"] <= 1.0
        assert "normalized_metrics" in result
        assert "metric_contributions" in result
        assert len(result["metric_contributions"]) == 4
    
    def test_metric_importance_calculation(self, sample_bias_score_data):
        """Test metric importance calculation."""
        algo = BiasScoreAlgorithm()
        importance = algo.calculate_metric_importance(sample_bias_score_data)
        
        assert len(importance) > 0
        # Percentages should sum to ~100
        assert 95 < sum(importance.values()) < 105
    
    def test_dominant_metric_identification(self, sample_bias_score_data):
        """Test dominant metric identification."""
        algo = BiasScoreAlgorithm()
        dominant_metric, contribution = algo.get_dominant_metric(sample_bias_score_data)
        
        assert dominant_metric in ["demographic_parity", "equalized_odds", "calibration", "individual_fairness"]
        assert contribution > 0


# ============================================================================
# Test 2: Weight Profile Manager
# ============================================================================

class TestWeightProfileManager:
    """Test weight profile management."""
    
    def test_profile_loading(self):
        """Test loading of weight profiles."""
        manager = WeightProfileManager()
        profiles = manager.list_profiles()
        
        assert len(profiles) > 0
        assert "default" in profiles
    
    def test_get_default_profile(self):
        """Test retrieving default profile."""
        manager = WeightProfileManager()
        weights = manager.get_weights("default")
        
        assert len(weights) == 4
        assert "demographic_parity" in weights
        assert sum(weights.values()) == pytest.approx(1.0, abs=1e-6)
    
    def test_get_lending_profile(self):
        """Test retrieving lending-specific profile."""
        manager = WeightProfileManager()
        weights = manager.get_weights("lending")
        
        assert weights["equalized_odds"] > weights["demographic_parity"]
    
    def test_custom_profile_creation(self):
        """Test creating custom weight profile."""
        manager = WeightProfileManager()
        custom_weights = {
            "demographic_parity": 0.25,
            "equalized_odds": 0.25,
            "calibration": 0.25,
            "individual_fairness": 0.25
        }
        
        profile = manager.create_custom_profile("test_custom", custom_weights)
        assert profile.name == "test_custom"
        assert profile.validate()


# ============================================================================
# Test 3: Composite Calculator
# ============================================================================

class TestCompositeCalculator:
    """Test composite bias score calculator."""
    
    def test_calculator_initialization(self):
        """Test calculator initialization."""
        calc = BiasScoreCalculator(weight_profile="default")
        assert calc.weight_profile == "default"
        assert calc.algorithm is not None
    
    def test_calculate_from_raw_metrics(self, sample_raw_metrics):
        """Test calculation from raw metrics."""
        calc = BiasScoreCalculator()
        result = calc.calculate_from_raw_metrics("test_model", sample_raw_metrics, n_bootstrap=100)
        
        assert result.model_id == "test_model"
        assert 0.0 <= result.overall_bias_score <= 1.0
        assert len(result.confidence_interval) == 2
        assert result.dominant_metric in sample_raw_metrics.keys()
    
    def test_weight_profile_change(self, sample_raw_metrics):
        """Test changing weight profiles."""
        calc = BiasScoreCalculator(weight_profile="default")
        result1 = calc.calculate_from_raw_metrics("test_model", sample_raw_metrics, n_bootstrap=50)
        
        calc.change_weight_profile("lending")
        result2 = calc.calculate_from_raw_metrics("test_model", sample_raw_metrics, n_bootstrap=50)
        
        # Scores should differ with different weight profiles
        assert result1.overall_bias_score != result2.overall_bias_score
    
    def test_result_to_dict(self, sample_raw_metrics):
        """Test converting result to dictionary."""
        calc = BiasScoreCalculator()
        result = calc.calculate_from_raw_metrics("test_model", sample_raw_metrics, n_bootstrap=50)
        result_dict = calc.to_dict(result)
        
        assert isinstance(result_dict, dict)
        assert "overall_bias_score" in result_dict
        assert "model_id" in result_dict


# ============================================================================
# Test 4: Score Interpreter
# ============================================================================

class TestScoreInterpreter:
    """Test score interpretation."""
    
    def test_interpreter_initialization(self):
        """Test interpreter initialization."""
        interp = ScoreInterpreter(use_llm=False)
        assert interp.use_llm == False
    
    def test_severity_classification(self):
        """Test severity level classification."""
        interp = ScoreInterpreter(use_llm=False)
        
        # Test LOW
        result_low = interp.interpret_score(0.20, {}, {}, "demographic_parity")
        assert result_low["severity_level"] == "EXCELLENT"
        
        # Test MODERATE
        result_mod = interp.interpret_score(0.45, {}, {}, "equalized_odds")
        assert result_mod["severity_level"] == "MODERATE"
        
        # Test CRITICAL
        result_crit = interp.interpret_score(0.85, {}, {}, "calibration")
        assert result_crit["severity_level"] == "CRITICAL"
    
    def test_template_interpretation(self, sample_bias_score_data):
        """Test template-based interpretation."""
        interp = ScoreInterpreter(use_llm=False)
        result = interp.interpret_score(
            sample_bias_score_data["overall_bias_score"],
            sample_bias_score_data["metric_contributions"],
            sample_bias_score_data["raw_metrics"],
            sample_bias_score_data["dominant_metric"]
        )
        
        assert "interpretation" in result
        assert len(result["interpretation"]) > 0
        assert "key_concerns" in result
    
    def test_benchmark_comparison(self):
        """Test benchmark comparison."""
        interp = ScoreInterpreter(use_llm=False)
        benchmark_comp = interp._compare_to_benchmark(0.35, "lending")
        
        assert "industry" in benchmark_comp
        assert "industry_average" in benchmark_comp
        assert "performance" in benchmark_comp


# ============================================================================
# Test 5: Risk Classifier
# ============================================================================

class TestRiskClassifier:
    """Test risk classification engine."""
    
    def test_classifier_initialization(self):
        """Test classifier initialization."""
        classifier = RiskClassifier()
        assert classifier.rules is not None
    
    def test_base_classification(self):
        """Test base risk classification."""
        classifier = RiskClassifier()
        
        # Test LOW
        result_low = classifier.classify_risk(0.20, {})
        assert result_low["risk_level"] == "LOW"
        
        # Test MEDIUM
        result_med = classifier.classify_risk(0.40, {})
        assert result_med["risk_level"] == "MEDIUM"
        
        # Test HIGH
        result_high = classifier.classify_risk(0.65, {})
        assert result_high["risk_level"] == "HIGH"
        
        # Test CRITICAL
        result_crit = classifier.classify_risk(0.85, {})
        assert result_crit["risk_level"] == "CRITICAL"
    
    def test_override_rules(self):
        """Test override rule application."""
        classifier = RiskClassifier()
        
        # Should trigger demographic parity override
        metrics = {
            "demographic_parity": 0.85,
            "equalized_odds": 0.30,
            "calibration": 0.20,
            "individual_fairness": 0.15
        }
        
        result = classifier.classify_risk(0.40, metrics)  # Base would be MEDIUM
        # Should be escalated due to high DP
        assert result["override_applied"] or result["risk_level"] in ["HIGH", "CRITICAL"]
    
    def test_regulatory_context(self):
        """Test regulatory context adjustments."""
        classifier = RiskClassifier()
        result = classifier.classify_risk(
            0.45,
            {},
            regulatory_context="eu_ai_act_high_risk"
        )
        
        assert result["regulatory_context"] == "eu_ai_act_high_risk"


# ============================================================================
# Test 6: Alert Manager
# ============================================================================

class TestAlertManager:
    """Test bias alert management."""
    
    def test_alert_creation(self, sample_bias_score_data, sample_risk_classification, sample_interpretation_data):
        """Test alert creation."""
        manager = BiasAlertManager()
        alert = manager.create_alert(
            "test_model",
            sample_risk_classification,
            sample_bias_score_data,
            sample_interpretation_data
        )
        
        assert alert.model_id == "test_model"
        assert alert.risk_level == "MEDIUM"
        assert alert.priority in ["low", "medium", "high", "urgent"]
        assert len(alert.recommended_actions) > 0
    
    def test_alert_deduplication(self, sample_bias_score_data, sample_risk_classification, sample_interpretation_data):
        """Test alert deduplication."""
        manager = BiasAlertManager(dedup_window_hours=24)
        
        alert1 = manager.create_alert(
            "test_model",
            sample_risk_classification,
            sample_bias_score_data,
            sample_interpretation_data
        )
        
        alert2 = manager.create_alert(
            "test_model",
            sample_risk_classification,
            sample_bias_score_data,
            sample_interpretation_data
        )
        
        # Should return same alert (deduplicated)
        assert alert1.alert_id == alert2.alert_id
    
    def test_alert_acknowledgment(self, sample_bias_score_data, sample_risk_classification, sample_interpretation_data):
        """Test alert acknowledgment."""
        manager = BiasAlertManager()
        alert = manager.create_alert(
            "test_model",
            sample_risk_classification,
            sample_bias_score_data,
            sample_interpretation_data
        )
        
        success = manager.acknowledge_alert(alert.alert_id, "test_user@example.com")
        assert success == True
        assert alert.acknowledged == True
    
    def test_get_active_alerts(self, sample_bias_score_data, sample_risk_classification, sample_interpretation_data):
        """Test getting active alerts."""
        manager = BiasAlertManager(dedup_window_hours=24)
        
        manager.create_alert("model_1", sample_risk_classification, sample_bias_score_data, sample_interpretation_data)
        manager.create_alert("model_2", sample_risk_classification, sample_bias_score_data, sample_interpretation_data)
        
        active = manager.get_active_alerts()
        assert len(active) == 2
        
        active_model1 = manager.get_active_alerts(model_id="model_1")
        assert len(active_model1) == 1


# ============================================================================
# Test 7: Report Generator
# ============================================================================

class TestReportGenerator:
    """Test bias risk report generation."""
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        gen = BiasRiskReportGenerator(use_llm=False)
        assert gen.use_llm == False
    
    def test_report_generation(self, sample_bias_score_data, sample_risk_classification, sample_interpretation_data):
        """Test complete report generation."""
        gen = BiasRiskReportGenerator(use_llm=False)
        report = gen.generate_report_data(
            "test_model",
            sample_bias_score_data,
            sample_risk_classification,
            sample_interpretation_data
        )
        
        assert "report_id" in report
        assert report["model_id"] == "test_model"
        assert "executive_summary" in report
        assert "detailed_analysis" in report
        assert "visualizations" in report
        assert "recommendations" in report
        assert "compliance_checklist" in report
    
    def test_executive_summary(self, sample_bias_score_data, sample_risk_classification, sample_interpretation_data):
        """Test executive summary generation."""
        gen = BiasRiskReportGenerator(use_llm=False)
        report = gen.generate_report_data(
            "test_model",
            sample_bias_score_data,
            sample_risk_classification,
            sample_interpretation_data
        )
        
        summary = report["executive_summary"]
        assert "overall_bias_score" in summary
        assert "risk_classification" in summary
        assert "key_findings" in summary
        assert len(summary["key_findings"]) > 0
    
    def test_visualization_data(self, sample_bias_score_data, sample_risk_classification, sample_interpretation_data):
        """Test visualization data generation."""
        gen = BiasRiskReportGenerator(use_llm=False)
        report = gen.generate_report_data(
            "test_model",
            sample_bias_score_data,
            sample_risk_classification,
            sample_interpretation_data
        )
        
        viz = report["visualizations"]
        assert "risk_heatmap_data" in viz
        assert "metric_contributions_chart" in viz
        assert "score_gauge" in viz
        assert viz["risk_heatmap_data"]["type"] == "heatmap"


# ============================================================================
# Test 8: End-to-End Integration
# ============================================================================

class TestEndToEndIntegration:
    """Test complete bias scoring pipeline."""
    
    def test_complete_pipeline(self, sample_raw_metrics):
        """Test complete pipeline from raw metrics to report."""
        # Step 1: Calculate composite score
        calculator = BiasScoreCalculator(weight_profile="default")
        bias_score_result = calculator.calculate_from_raw_metrics(
            "integration_test_model",
            sample_raw_metrics,
            n_bootstrap=100
        )
        
        assert bias_score_result.overall_bias_score > 0
        
        # Step 2: Interpret score
        interpreter = ScoreInterpreter(use_llm=False)
        interpretation = interpreter.interpret_score(
            bias_score_result.overall_bias_score,
            bias_score_result.metric_contributions,
            bias_score_result.raw_metrics,
            bias_score_result.dominant_metric
        )
        
        assert "severity_level" in interpretation
        
        # Step 3: Classify risk
        classifier = RiskClassifier()
        risk_classification = classifier.classify_risk(
            bias_score_result.overall_bias_score,
            bias_score_result.normalized_metrics
        )
        
        assert "risk_level" in risk_classification
        
        # Step 4: Create alert
        alert_manager = BiasAlertManager()
        alert = alert_manager.create_alert(
            "integration_test_model",
            risk_classification,
            calculator.to_dict(bias_score_result),
            interpretation
        )
        
        assert alert.model_id == "integration_test_model"
        
        # Step 5: Generate report
        report_generator = BiasRiskReportGenerator(use_llm=False)
        report = report_generator.generate_report_data(
            "integration_test_model",
            calculator.to_dict(bias_score_result),
            risk_classification,
            interpretation,
            alert_manager.to_dict(alert)
        )
        
        assert report["model_id"] == "integration_test_model"
        assert "executive_summary" in report
        
        print("\n✅ End-to-end pipeline test passed!")
        print(f"✅ Bias Score: {bias_score_result.overall_bias_score:.3f}")
        print(f"✅ Risk Level: {risk_classification['risk_level']}")
        print(f"✅ Alert Priority: {alert.priority}")
        print(f"✅ Report ID: {report['report_id']}")


# ============================================================================
# Test 9: Performance Tests
# ============================================================================

class TestPerformance:
    """Test performance requirements."""
    
    def test_scoring_performance(self, sample_raw_metrics):
        """Test that scoring completes within 500ms."""
        import time
        
        calculator = BiasScoreCalculator()
        
        start = time.time()
        result = calculator.calculate_from_raw_metrics(
            "perf_test_model",
            sample_raw_metrics,
            n_bootstrap=100
        )
        elapsed = time.time() - start
        
        assert elapsed < 0.5, f"Scoring took {elapsed:.3f}s, should be <0.5s"
    
    def test_report_generation_performance(self, sample_bias_score_data, sample_risk_classification, sample_interpretation_data):
        """Test that report generation completes within 2s."""
        import time
        
        generator = BiasRiskReportGenerator(use_llm=False)
        
        start = time.time()
        report = generator.generate_report_data(
            "perf_test_model",
            sample_bias_score_data,
            sample_risk_classification,
            sample_interpretation_data
        )
        elapsed = time.time() - start
        
        assert elapsed < 2.0, f"Report generation took {elapsed:.3f}s, should be <2s"


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
