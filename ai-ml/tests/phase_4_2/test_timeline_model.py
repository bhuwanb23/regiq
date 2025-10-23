"""
Tests for Timeline Models

Test coverage:
- TimeToDetectionModel (5 tests)
- TimeToRemediationModel (5 tests)
- ViolationForecastModel (5 tests)
- RegulatoryResponseTimeModel (4 tests)

Total: 19 tests
"""

import pytest
import numpy as np
from services.risk_simulator.models.timeline_model import (
    TimeToDetectionModel,
    TimeToRemediationModel,
    ViolationForecastModel,
    RegulatoryResponseTimeModel,
    TimelineResult,
    ForecastResult,
    TimelinePhase
)


class TestTimeToDetectionModel:
    """Test suite for TimeToDetectionModel"""
    
    def test_initialization_exponential(self):
        """Test initialization with exponential distribution"""
        model = TimeToDetectionModel(distribution='exponential', random_state=42)
        assert model.distribution == 'exponential'
        assert model.random_state == 42
    
    def test_initialization_weibull(self):
        """Test initialization with Weibull distribution"""
        model = TimeToDetectionModel(distribution='weibull', random_state=42)
        assert model.distribution == 'weibull'
    
    def test_invalid_distribution(self):
        """Test that invalid distribution raises error"""
        with pytest.raises(ValueError):
            TimeToDetectionModel(distribution='invalid')
    
    def test_fit_exponential(self):
        """Test fitting exponential model"""
        model = TimeToDetectionModel(distribution='exponential', random_state=42)
        detection_times = [10.0, 15.0, 20.0, 25.0, 30.0, 12.0, 18.0]
        
        model.fit(detection_times, mcmc_draws=500, mcmc_tune=500)
        
        assert model.fitted_params is not None
        assert 'lambda' in model.fitted_params
        assert model.trace is not None
    
    def test_predict_detection_time(self):
        """Test detection time prediction"""
        model = TimeToDetectionModel(distribution='exponential', random_state=42)
        detection_times = [10.0, 15.0, 20.0, 25.0, 30.0]
        model.fit(detection_times, mcmc_draws=500, mcmc_tune=500)
        
        result = model.predict()
        
        assert isinstance(result, TimelineResult)
        assert result.mean_days > 0
        assert result.median_days > 0
        assert result.confidence_interval[0] < result.confidence_interval[1]
        assert result.distribution_type == 'exponential'
    
    def test_sample_detection_times(self):
        """Test sampling from fitted distribution"""
        model = TimeToDetectionModel(distribution='exponential', random_state=42)
        detection_times = [10.0, 15.0, 20.0, 25.0, 30.0]
        model.fit(detection_times, mcmc_draws=500, mcmc_tune=500)
        
        samples = model.sample_detection_times(n_samples=1000)
        
        assert len(samples) == 1000
        assert np.all(samples > 0)


class TestTimeToRemediationModel:
    """Test suite for TimeToRemediationModel"""
    
    def test_initialization(self):
        """Test initialization"""
        model = TimeToRemediationModel(distribution='lognormal', random_state=42)
        assert model.distribution == 'lognormal'
    
    def test_fit_lognormal(self):
        """Test fitting log-normal model"""
        model = TimeToRemediationModel(distribution='lognormal', random_state=42)
        remediation_times = [30.0, 45.0, 60.0, 50.0, 40.0, 55.0]
        
        model.fit(remediation_times)
        
        assert 'mu' in model.fitted_params
        assert 'sigma' in model.fitted_params
    
    def test_fit_with_complexity(self):
        """Test fitting with complexity scores"""
        model = TimeToRemediationModel(distribution='lognormal', random_state=42)
        remediation_times = [30.0, 45.0, 60.0, 50.0, 40.0, 55.0]
        complexity_scores = [0.3, 0.5, 0.8, 0.6, 0.4, 0.7]
        
        model.fit(remediation_times, complexity_scores)
        
        assert 'complexity_slope' in model.fitted_params
        assert 'complexity_intercept' in model.fitted_params
    
    def test_predict_remediation_time(self):
        """Test remediation time prediction"""
        model = TimeToRemediationModel(distribution='lognormal', random_state=42)
        remediation_times = [30.0, 45.0, 60.0, 50.0, 40.0]
        model.fit(remediation_times)
        
        result = model.predict()
        
        assert isinstance(result, TimelineResult)
        assert result.mean_days > 0
        assert result.phase == TimelinePhase.REMEDIATION.value
    
    def test_predict_with_complexity(self):
        """Test prediction with complexity adjustment"""
        model = TimeToRemediationModel(distribution='lognormal', random_state=42)
        remediation_times = [30.0, 45.0, 60.0, 50.0, 40.0]
        complexity_scores = [0.3, 0.5, 0.8, 0.6, 0.4]
        model.fit(remediation_times, complexity_scores)
        
        result_low = model.predict(complexity_score=0.2)
        result_high = model.predict(complexity_score=0.9)
        
        # Higher complexity should generally mean longer time
        assert result_high.mean_days >= result_low.mean_days


class TestViolationForecastModel:
    """Test suite for ViolationForecastModel"""
    
    def test_initialization(self):
        """Test initialization"""
        model = ViolationForecastModel(random_state=42)
        assert model.random_state == 42
        assert model.fitted is False
    
    def test_fit(self):
        """Test fitting the model"""
        model = ViolationForecastModel(random_state=42)
        historical_counts = [2, 3, 2, 4, 3, 5, 4, 6, 5, 7]
        
        model.fit(historical_counts)
        
        assert model.fitted is True
        assert model.base_rate > 0
    
    def test_forecast(self):
        """Test forecasting violations"""
        model = ViolationForecastModel(random_state=42)
        historical_counts = [2, 3, 2, 4, 3, 5, 4, 6]
        model.fit(historical_counts)
        
        forecast = model.forecast(forecast_days=365, n_simulations=1000)
        
        assert isinstance(forecast, ForecastResult)
        assert forecast.expected_violations >= 0
        assert 0 <= forecast.violation_probability <= 1
        assert forecast.trend in ['increasing', 'decreasing', 'stable']
    
    def test_forecast_trend_detection(self):
        """Test trend detection"""
        model_increasing = ViolationForecastModel(random_state=42)
        increasing_counts = [1, 2, 3, 4, 5, 6, 7, 8]
        model_increasing.fit(increasing_counts)
        forecast_inc = model_increasing.forecast(forecast_days=365)
        
        assert forecast_inc.trend == 'increasing'
    
    def test_confidence_bands(self):
        """Test confidence bands in forecast"""
        model = ViolationForecastModel(random_state=42)
        historical_counts = [2, 3, 2, 4, 3, 5]
        model.fit(historical_counts)
        
        forecast = model.forecast(forecast_days=365, n_simulations=1000)
        
        assert '50%' in forecast.confidence_bands
        assert '90%' in forecast.confidence_bands
        assert '95%' in forecast.confidence_bands


class TestRegulatoryResponseTimeModel:
    """Test suite for RegulatoryResponseTimeModel"""
    
    def test_initialization(self):
        """Test initialization"""
        model = RegulatoryResponseTimeModel(random_state=42)
        assert model.random_state == 42
    
    def test_fit(self):
        """Test fitting the model"""
        model = RegulatoryResponseTimeModel(random_state=42)
        response_times = [30.0, 45.0, 60.0, 40.0, 50.0, 35.0, 55.0, 65.0]
        severities = ['low', 'medium', 'high', 'low', 'medium', 'low', 'high', 'critical']
        
        model.fit(response_times, severities)
        
        assert len(model.fitted_distributions) > 0
        assert 'low' in model.fitted_distributions
    
    def test_predict(self):
        """Test prediction"""
        model = RegulatoryResponseTimeModel(random_state=42)
        response_times = [30.0, 45.0, 60.0, 40.0, 50.0, 35.0, 55.0, 65.0]
        severities = ['low', 'medium', 'high', 'low', 'medium', 'low', 'high', 'critical']
        model.fit(response_times, severities)
        
        result = model.predict('low')
        
        assert isinstance(result, TimelineResult)
        assert result.mean_days > 0
        assert result.phase == TimelinePhase.REGULATORY_RESPONSE.value
    
    def test_predict_unknown_severity(self):
        """Test prediction with unknown severity raises error"""
        model = RegulatoryResponseTimeModel(random_state=42)
        response_times = [30.0, 45.0, 60.0]
        severities = ['low', 'medium', 'high']
        model.fit(response_times, severities)
        
        with pytest.raises(ValueError):
            model.predict('unknown')


class TestTimelineIntegration:
    """Integration tests for timeline models"""
    
    def test_end_to_end_timeline(self):
        """Test complete timeline estimation"""
        # Detection
        detection_model = TimeToDetectionModel(distribution='exponential', random_state=42)
        detection_times = [10.0, 15.0, 20.0, 25.0]
        detection_model.fit(detection_times, mcmc_draws=500, mcmc_tune=500)
        detection_result = detection_model.predict()
        
        # Remediation
        remediation_model = TimeToRemediationModel(distribution='lognormal', random_state=42)
        remediation_times = [30.0, 45.0, 60.0]
        remediation_model.fit(remediation_times)
        remediation_result = remediation_model.predict()
        
        # Total timeline
        total_expected = detection_result.mean_days + remediation_result.mean_days
        
        assert total_expected > 0
        assert detection_result.to_dict() is not None
        assert remediation_result.to_dict() is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
