"""
Tests for Regulatory Risk Models

Test coverage:
- ViolationProbabilityModel (7 tests)
- ViolationFrequencyModel (5 tests)
- ViolationSeverityClassifier (5 tests)
- RegulatoryRiskAssessor (3 tests)

Total: 20 tests
"""

import pytest
import numpy as np
from scipy import stats
from services.risk_simulator.models.regulatory_risk import (
    ViolationProbabilityModel,
    ViolationFrequencyModel,
    ViolationSeverityClassifier,
    RegulatoryRiskAssessor,
    ViolationSeverity,
    JurisdictionType,
    RegulatoryRiskResult
)


# ============================================================================
# ViolationProbabilityModel Tests
# ============================================================================

class TestViolationProbabilityModel:
    """Test suite for ViolationProbabilityModel"""
    
    def test_initialization(self):
        """Test model initialization with custom priors"""
        model = ViolationProbabilityModel(
            prior_alpha=5.0,
            prior_beta=15.0,
            random_state=42
        )
        
        assert model.prior_alpha == 5.0
        assert model.prior_beta == 15.0
        assert model.random_state == 42
        assert model.posterior_alpha is None
        assert model.posterior_beta is None
    
    def test_fit_conjugate_update(self):
        """Test Bayesian conjugate update"""
        model = ViolationProbabilityModel(
            prior_alpha=2.0,
            prior_beta=10.0,
            random_state=42
        )
        
        # Fit with observed data
        n_violations = 5
        n_opportunities = 50
        model.fit(n_violations, n_opportunities, mcmc_draws=500, mcmc_tune=500)
        
        # Check conjugate update
        expected_alpha = 2.0 + 5  # prior + successes
        expected_beta = 10.0 + 45  # prior + failures
        
        assert model.posterior_alpha == expected_alpha
        assert model.posterior_beta == expected_beta
        assert model.trace is not None
    
    def test_predict_probability(self):
        """Test probability prediction"""
        model = ViolationProbabilityModel(random_state=42)
        model.fit(10, 100, mcmc_draws=500, mcmc_tune=500)
        
        mean_prob, (lower, upper) = model.predict_probability()
        
        # Check bounds
        assert 0 <= mean_prob <= 1
        assert 0 <= lower <= mean_prob
        assert mean_prob <= upper <= 1
        
        # Check reasonable estimate (10/100 = 0.1)
        assert 0.05 < mean_prob < 0.20
    
    def test_predict_without_fit_raises_error(self):
        """Test that prediction without fitting raises error"""
        model = ViolationProbabilityModel()
        
        with pytest.raises(ValueError, match="Model must be fitted"):
            model.predict_probability()
    
    def test_sample_posterior(self):
        """Test posterior sampling"""
        model = ViolationProbabilityModel(random_state=42)
        model.fit(10, 100, mcmc_draws=500, mcmc_tune=500)
        
        samples = model.sample_posterior(n_samples=5000)
        
        assert len(samples) == 5000
        assert np.all(samples >= 0) and np.all(samples <= 1)
        
        # Sample mean should be close to posterior mean
        mean_prob, _ = model.predict_probability()
        assert abs(np.mean(samples) - mean_prob) < 0.02
    
    def test_convergence_diagnostics(self):
        """Test MCMC convergence diagnostics"""
        model = ViolationProbabilityModel(random_state=42)
        model.fit(10, 100, mcmc_draws=1000, mcmc_tune=1000)
        
        diagnostics = model.get_convergence_diagnostics()
        
        assert 'rhat' in diagnostics
        assert 'ess_bulk' in diagnostics
        assert 'converged' in diagnostics
        
        # Should converge with sufficient samples
        assert diagnostics['converged'] is True
        assert diagnostics['rhat'] < 1.05
    
    def test_different_credible_intervals(self):
        """Test different credible interval levels"""
        model = ViolationProbabilityModel(random_state=42)
        model.fit(10, 100, mcmc_draws=500, mcmc_tune=500)
        
        mean_90, (lower_90, upper_90) = model.predict_probability(credible_interval=0.90)
        mean_95, (lower_95, upper_95) = model.predict_probability(credible_interval=0.95)
        
        # Same mean, wider interval for higher credibility
        assert abs(mean_90 - mean_95) < 0.001
        assert lower_90 > lower_95
        assert upper_90 < upper_95


# ============================================================================
# ViolationFrequencyModel Tests
# ============================================================================

class TestViolationFrequencyModel:
    """Test suite for ViolationFrequencyModel"""
    
    def test_initialization_poisson(self):
        """Test Poisson model initialization"""
        model = ViolationFrequencyModel(model_type='poisson', random_state=42)
        
        assert model.model_type == 'poisson'
        assert model.random_state == 42
        assert model.fitted_lambda is None
    
    def test_initialization_negative_binomial(self):
        """Test Negative Binomial model initialization"""
        model = ViolationFrequencyModel(
            model_type='negative_binomial',
            random_state=42
        )
        
        assert model.model_type == 'negative_binomial'
        assert model.fitted_lambda is None
        assert model.fitted_alpha is None
    
    def test_invalid_model_type(self):
        """Test that invalid model type raises error"""
        with pytest.raises(ValueError, match="model_type must be"):
            ViolationFrequencyModel(model_type='gaussian')
    
    def test_fit_poisson(self):
        """Test fitting Poisson model"""
        model = ViolationFrequencyModel(model_type='poisson', random_state=42)
        
        # Generate Poisson-like data
        violation_counts = [2, 1, 3, 2, 1, 2, 3, 1, 2, 2]
        model.fit(violation_counts, mcmc_draws=500, mcmc_tune=500)
        
        assert model.fitted_lambda is not None
        assert model.trace is not None
        
        # Lambda should be close to mean of observed data
        observed_mean = np.mean(violation_counts)
        assert abs(model.fitted_lambda - observed_mean) < 1.0
    
    def test_fit_negative_binomial(self):
        """Test fitting Negative Binomial model"""
        model = ViolationFrequencyModel(
            model_type='negative_binomial',
            random_state=42
        )
        
        # Overdispersed count data
        violation_counts = [0, 5, 1, 8, 2, 0, 10, 3, 1, 6]
        model.fit(violation_counts, mcmc_draws=500, mcmc_tune=500)
        
        assert model.fitted_lambda is not None
        assert model.fitted_alpha is not None
        assert model.trace is not None
    
    def test_predict_frequency_poisson(self):
        """Test frequency prediction for Poisson model"""
        model = ViolationFrequencyModel(model_type='poisson', random_state=42)
        violation_counts = [2, 2, 3, 2, 2]
        model.fit(violation_counts, mcmc_draws=500, mcmc_tune=500)
        
        expected_freq, (lower, upper) = model.predict_frequency(time_horizon=1.0)
        
        assert expected_freq > 0
        assert lower <= expected_freq
        assert expected_freq <= upper
        
        # 2-year horizon should double frequency
        expected_freq_2y, _ = model.predict_frequency(time_horizon=2.0)
        assert abs(expected_freq_2y - 2 * expected_freq) < 0.5
    
    def test_predict_frequency_negative_binomial(self):
        """Test frequency prediction for Negative Binomial model"""
        model = ViolationFrequencyModel(
            model_type='negative_binomial',
            random_state=42
        )
        violation_counts = [0, 5, 1, 8, 2, 0, 10, 3]
        model.fit(violation_counts, mcmc_draws=500, mcmc_tune=500)
        
        expected_freq, (lower, upper) = model.predict_frequency(time_horizon=1.0)
        
        assert expected_freq > 0
        assert lower <= expected_freq
        assert expected_freq <= upper
    
    def test_sample_violations_poisson(self):
        """Test sampling violations for Poisson model"""
        model = ViolationFrequencyModel(model_type='poisson', random_state=42)
        violation_counts = [2, 2, 3, 2, 2]
        model.fit(violation_counts, mcmc_draws=500, mcmc_tune=500)
        
        samples = model.sample_violations(time_horizon=1.0, n_samples=5000)
        
        assert len(samples) == 5000
        assert np.all(samples >= 0)
        
        # Sample mean should be close to expected frequency
        expected_freq, _ = model.predict_frequency(time_horizon=1.0)
        assert abs(np.mean(samples) - expected_freq) < 0.5
    
    def test_sample_violations_negative_binomial(self):
        """Test sampling violations for Negative Binomial model"""
        model = ViolationFrequencyModel(
            model_type='negative_binomial',
            random_state=42
        )
        violation_counts = [0, 5, 1, 8, 2, 0, 10, 3]
        model.fit(violation_counts, mcmc_draws=500, mcmc_tune=500)
        
        samples = model.sample_violations(time_horizon=1.0, n_samples=5000)
        
        assert len(samples) == 5000
        assert np.all(samples >= 0)


# ============================================================================
# ViolationSeverityClassifier Tests
# ============================================================================

class TestViolationSeverityClassifier:
    """Test suite for ViolationSeverityClassifier"""
    
    def test_initialization_default(self):
        """Test classifier initialization with defaults"""
        classifier = ViolationSeverityClassifier()
        
        assert 'critical' in classifier.severity_thresholds
        assert 'high' in classifier.severity_thresholds
        assert 'medium' in classifier.severity_thresholds
        assert 'low' in classifier.severity_thresholds
    
    def test_initialization_custom_thresholds(self):
        """Test classifier with custom thresholds"""
        custom_thresholds = {
            'critical': 0.95,
            'high': 0.75,
            'medium': 0.5,
            'low': 0.0
        }
        classifier = ViolationSeverityClassifier(severity_thresholds=custom_thresholds)
        
        assert classifier.severity_thresholds == custom_thresholds
    
    def test_classify_critical(self):
        """Test classification of critical violations"""
        classifier = ViolationSeverityClassifier()
        
        severity = classifier.classify(
            impact_score=1.0,
            probability=1.0,
            regulatory_priority=1.0
        )
        
        assert severity == ViolationSeverity.CRITICAL
    
    def test_classify_high(self):
        """Test classification of high severity violations"""
        classifier = ViolationSeverityClassifier()
        
        severity = classifier.classify(
            impact_score=0.8,
            probability=0.7,
            regulatory_priority=0.7
        )
        
        assert severity == ViolationSeverity.HIGH
    
    def test_classify_medium(self):
        """Test classification of medium severity violations"""
        classifier = ViolationSeverityClassifier()
        
        severity = classifier.classify(
            impact_score=0.5,
            probability=0.5,
            regulatory_priority=0.5
        )
        
        assert severity == ViolationSeverity.MEDIUM
    
    def test_classify_low(self):
        """Test classification of low severity violations"""
        classifier = ViolationSeverityClassifier()
        
        severity = classifier.classify(
            impact_score=0.1,
            probability=0.1,
            regulatory_priority=0.1
        )
        
        assert severity == ViolationSeverity.LOW
    
    def test_calculate_risk_score(self):
        """Test risk score calculation"""
        classifier = ViolationSeverityClassifier()
        
        severity_dist = {
            ViolationSeverity.CRITICAL: 0.1,
            ViolationSeverity.HIGH: 0.2,
            ViolationSeverity.MEDIUM: 0.3,
            ViolationSeverity.LOW: 0.4
        }
        
        risk_score = classifier.calculate_risk_score(
            violation_probability=0.5,
            severity_distribution=severity_dist
        )
        
        assert risk_score > 0
        
        # Higher probability should increase risk score
        risk_score_high_prob = classifier.calculate_risk_score(
            violation_probability=0.9,
            severity_distribution=severity_dist
        )
        assert risk_score_high_prob > risk_score
    
    def test_get_severity_distribution(self):
        """Test severity distribution generation"""
        classifier = ViolationSeverityClassifier()
        
        distribution = classifier.get_severity_distribution(n_simulations=10000)
        
        # Check all severity levels present
        assert 'low' in distribution
        assert 'medium' in distribution
        assert 'high' in distribution
        assert 'critical' in distribution
        
        # Probabilities should sum to 1.0
        assert abs(sum(distribution.values()) - 1.0) < 0.001
        
        # All probabilities should be non-negative
        assert all(p >= 0 for p in distribution.values())
    
    def test_get_severity_distribution_with_custom_inputs(self):
        """Test severity distribution with custom input arrays"""
        classifier = ViolationSeverityClassifier()
        
        # High impact, high probability scenarios
        impact_scores = np.full(1000, 0.9)
        probabilities = np.full(1000, 0.9)
        priorities = np.full(1000, 0.9)
        
        distribution = classifier.get_severity_distribution(
            n_simulations=1000,
            impact_scores=impact_scores,
            probabilities=probabilities,
            regulatory_priorities=priorities
        )
        
        # Should be mostly critical/high
        assert distribution['critical'] + distribution['high'] > 0.8
    
    def test_severity_weights(self):
        """Test severity weight constants"""
        classifier = ViolationSeverityClassifier()
        
        # Weights should be monotonically increasing
        assert (classifier.SEVERITY_WEIGHTS[ViolationSeverity.LOW] <
                classifier.SEVERITY_WEIGHTS[ViolationSeverity.MEDIUM] <
                classifier.SEVERITY_WEIGHTS[ViolationSeverity.HIGH] <
                classifier.SEVERITY_WEIGHTS[ViolationSeverity.CRITICAL])


# ============================================================================
# RegulatoryRiskAssessor Tests
# ============================================================================

class TestRegulatoryRiskAssessor:
    """Test suite for RegulatoryRiskAssessor"""
    
    def test_initialization(self):
        """Test assessor initialization"""
        assessor = RegulatoryRiskAssessor(random_state=42)
        
        assert assessor.random_state == 42
        assert assessor.probability_model is not None
        assert assessor.frequency_model is not None
        assert assessor.severity_classifier is not None
    
    def test_assess_risk_basic(self):
        """Test basic risk assessment"""
        assessor = RegulatoryRiskAssessor(random_state=42)
        
        result = assessor.assess_risk(
            historical_violations=10,
            historical_opportunities=100,
            violation_counts_per_period=[2, 1, 3, 2, 1, 2, 3, 2],
            time_horizon=1.0
        )
        
        assert isinstance(result, RegulatoryRiskResult)
        assert 0 <= result.violation_probability <= 1
        assert result.expected_violations_per_year > 0
        assert result.risk_score > 0
        assert len(result.confidence_interval_95) == 2
        assert result.posterior_samples is not None
        assert result.convergence_diagnostics is not None
    
    def test_assess_risk_with_jurisdictions(self):
        """Test risk assessment with jurisdiction data"""
        assessor = RegulatoryRiskAssessor(random_state=42)
        
        jurisdictions = {
            'federal': {'violations': 5, 'opportunities': 50},
            'state': {'violations': 3, 'opportunities': 30},
            'local': {'violations': 2, 'opportunities': 20}
        }
        
        result = assessor.assess_risk(
            historical_violations=10,
            historical_opportunities=100,
            violation_counts_per_period=[2, 1, 3, 2, 1, 2, 3, 2],
            jurisdictions=jurisdictions,
            time_horizon=1.0
        )
        
        assert 'federal' in result.jurisdiction_risks
        assert 'state' in result.jurisdiction_risks
        assert 'local' in result.jurisdiction_risks
        
        # All jurisdiction risks should be probabilities
        for risk in result.jurisdiction_risks.values():
            assert 0 <= risk <= 1
    
    def test_assess_risk_different_time_horizons(self):
        """Test risk assessment with different time horizons"""
        assessor = RegulatoryRiskAssessor(random_state=42)
        
        result_1y = assessor.assess_risk(
            historical_violations=10,
            historical_opportunities=100,
            violation_counts_per_period=[2, 1, 3, 2, 1, 2, 3, 2],
            time_horizon=1.0
        )
        
        # Create new assessor for 2-year horizon
        assessor_2y = RegulatoryRiskAssessor(random_state=42)
        result_2y = assessor_2y.assess_risk(
            historical_violations=10,
            historical_opportunities=100,
            violation_counts_per_period=[2, 1, 3, 2, 1, 2, 3, 2],
            time_horizon=2.0
        )
        
        # 2-year horizon should have higher expected violations
        assert result_2y.expected_violations_per_year > result_1y.expected_violations_per_year
    
    def test_result_to_dict(self):
        """Test RegulatoryRiskResult serialization"""
        assessor = RegulatoryRiskAssessor(random_state=42)
        
        result = assessor.assess_risk(
            historical_violations=10,
            historical_opportunities=100,
            violation_counts_per_period=[2, 1, 3, 2, 1, 2, 3, 2],
            time_horizon=1.0
        )
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'violation_probability' in result_dict
        assert 'expected_violations_per_year' in result_dict
        assert 'severity_distribution' in result_dict
        assert 'risk_score' in result_dict
        assert 'confidence_interval_95' in result_dict
        assert 'jurisdiction_risks' in result_dict
        
        # All values should be JSON-serializable (no numpy types)
        import json
        json_str = json.dumps(result_dict)
        assert json_str is not None


# ============================================================================
# Integration Tests
# ============================================================================

class TestRegulatoryRiskIntegration:
    """Integration tests for complete workflow"""
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end risk assessment workflow"""
        # Setup
        assessor = RegulatoryRiskAssessor(random_state=42)
        
        # Historical data
        historical_violations = 15
        historical_opportunities = 200
        violation_counts = [3, 2, 4, 1, 2, 3, 2, 1, 3, 2, 2, 1]
        
        jurisdictions = {
            'federal': {'violations': 8, 'opportunities': 100},
            'state': {'violations': 5, 'opportunities': 75},
            'local': {'violations': 2, 'opportunities': 25}
        }
        
        # Perform assessment
        result = assessor.assess_risk(
            historical_violations=historical_violations,
            historical_opportunities=historical_opportunities,
            violation_counts_per_period=violation_counts,
            jurisdictions=jurisdictions,
            time_horizon=1.0
        )
        
        # Verify comprehensive output
        assert result.violation_probability > 0
        assert result.expected_violations_per_year > 0
        assert result.risk_score > 0
        assert result.confidence_interval_95[0] < result.confidence_interval_95[1]
        assert len(result.severity_distribution) == 4
        assert len(result.jurisdiction_risks) == 3
        assert result.posterior_samples is not None
        assert len(result.posterior_samples) > 0
        
        # Export to dict
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        
        # Verify serializable
        import json
        json.dumps(result_dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
