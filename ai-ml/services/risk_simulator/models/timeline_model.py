"""
Timeline Models for Regulatory Violations

This module implements models for forecasting and analyzing violation timelines,
detection times, remediation periods, and regulatory response patterns.

Models:
- TimeToDetectionModel: Model time from violation to detection
- TimeToRemediationModel: Model remediation timeline
- ViolationForecastModel: Forecast future violations
- RegulatoryResponseTimeModel: Model regulator response timing
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats
from scipy.special import gamma as scipy_gamma
import pymc as pm
import arviz as az


class TimelinePhase(Enum):
    """Phases in violation timeline"""
    VIOLATION_OCCURS = "violation_occurs"
    DETECTION = "detection"
    INVESTIGATION = "investigation"
    REMEDIATION = "remediation"
    REGULATORY_RESPONSE = "regulatory_response"
    CLOSURE = "closure"


@dataclass
class TimelineResult:
    """Result container for timeline predictions"""
    mean_days: float
    median_days: float
    percentile_90: float
    percentile_95: float
    confidence_interval: Tuple[float, float]
    distribution_type: str
    phase: str
    uncertainty_high: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'mean_days': float(self.mean_days),
            'median_days': float(self.median_days),
            'percentile_90': float(self.percentile_90),
            'percentile_95': float(self.percentile_95),
            'confidence_interval': tuple(float(x) for x in self.confidence_interval),
            'distribution_type': self.distribution_type,
            'phase': self.phase,
            'uncertainty_high': bool(self.uncertainty_high)
        }


@dataclass
class ForecastResult:
    """Result container for violation forecasts"""
    forecast_period_days: int
    expected_violations: float
    violation_probability: float
    forecast_distribution: np.ndarray
    confidence_bands: Dict[str, Tuple[float, float]]
    trend: str  # 'increasing', 'decreasing', 'stable'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'forecast_period_days': int(self.forecast_period_days),
            'expected_violations': float(self.expected_violations),
            'violation_probability': float(self.violation_probability),
            'forecast_summary': {
                'mean': float(np.mean(self.forecast_distribution)),
                'std': float(np.std(self.forecast_distribution)),
                'min': float(np.min(self.forecast_distribution)),
                'max': float(np.max(self.forecast_distribution))
            },
            'confidence_bands': {
                k: tuple(float(x) for x in v) 
                for k, v in self.confidence_bands.items()
            },
            'trend': self.trend
        }


class TimeToDetectionModel:
    """
    Model for time from violation occurrence to detection.
    
    Uses exponential/Weibull distributions for detection time modeling.
    """
    
    def __init__(self,
                 distribution: str = 'exponential',
                 random_state: Optional[int] = None):
        """
        Initialize detection time model.
        
        Args:
            distribution: 'exponential' or 'weibull'
            random_state: Random seed for reproducibility
        """
        if distribution not in ['exponential', 'weibull']:
            raise ValueError("distribution must be 'exponential' or 'weibull'")
        
        self.distribution = distribution
        self.random_state = random_state
        self.fitted_params: Dict[str, float] = {}
        self.trace = None
    
    def fit(self,
            detection_times_days: List[float],
            mcmc_draws: int = 2000,
            mcmc_tune: int = 1000) -> 'TimeToDetectionModel':
        """
        Fit model using observed detection times.
        
        Args:
            detection_times_days: List of detection times in days
            mcmc_draws: Number of MCMC samples
            mcmc_tune: Number of tuning steps
            
        Returns:
            Self for method chaining
        """
        times_array = np.array(detection_times_days)
        
        with pm.Model() as model:
            if self.distribution == 'exponential':
                # Exponential model (constant hazard rate)
                lam = pm.Exponential('lambda', lam=1.0)
                detection_times = pm.Exponential('detection_times',
                                                 lam=lam,
                                                 observed=times_array)
            else:
                # Weibull model (time-varying hazard rate)
                alpha = pm.Exponential('alpha', lam=1.0)  # shape
                beta = pm.Exponential('beta', lam=1.0)    # scale
                detection_times = pm.Weibull('detection_times',
                                             alpha=alpha,
                                             beta=beta,
                                             observed=times_array)
            
            # Sample
            self.trace = pm.sample(
                draws=mcmc_draws,
                tune=mcmc_tune,
                random_seed=self.random_state,
                return_inferencedata=True,
                progressbar=False
            )
        
        # Extract fitted parameters
        if self.distribution == 'exponential':
            self.fitted_params = {
                'lambda': float(self.trace.posterior['lambda'].mean())
            }
        else:
            self.fitted_params = {
                'alpha': float(self.trace.posterior['alpha'].mean()),
                'beta': float(self.trace.posterior['beta'].mean())
            }
        
        return self
    
    def predict(self,
                confidence_level: float = 0.95) -> TimelineResult:
        """
        Predict detection time.
        
        Args:
            confidence_level: Confidence interval level
            
        Returns:
            TimelineResult with predictions
        """
        if not self.fitted_params:
            raise ValueError("Model must be fitted before prediction")
        
        if self.distribution == 'exponential':
            lam = self.fitted_params['lambda']
            mean_days = 1.0 / lam
            median_days = np.log(2) / lam
            percentile_90 = float(stats.expon.ppf(0.90, scale=1/lam))
            percentile_95 = float(stats.expon.ppf(0.95, scale=1/lam))
            
            alpha_level = (1 - confidence_level) / 2
            ci_lower = float(stats.expon.ppf(alpha_level, scale=1/lam))
            ci_upper = float(stats.expon.ppf(1 - alpha_level, scale=1/lam))
        else:
            alpha = self.fitted_params['alpha']
            beta = self.fitted_params['beta']
            mean_days = beta * np.exp(np.log(scipy_gamma(1 + 1/alpha)))
            median_days = beta * (np.log(2) ** (1/alpha))
            percentile_90 = float(stats.weibull_min.ppf(0.90, alpha, scale=beta))
            percentile_95 = float(stats.weibull_min.ppf(0.95, alpha, scale=beta))
            
            alpha_level = (1 - confidence_level) / 2
            ci_lower = float(stats.weibull_min.ppf(alpha_level, alpha, scale=beta))
            ci_upper = float(stats.weibull_min.ppf(1 - alpha_level, alpha, scale=beta))
        
        # High uncertainty if CI is very wide
        uncertainty_high = bool((ci_upper / ci_lower) > 5.0)
        
        return TimelineResult(
            mean_days=mean_days,
            median_days=median_days,
            percentile_90=percentile_90,
            percentile_95=percentile_95,
            confidence_interval=(ci_lower, ci_upper),
            distribution_type=self.distribution,
            phase=TimelinePhase.DETECTION.value,
            uncertainty_high=uncertainty_high
        )
    
    def sample_detection_times(self, n_samples: int = 10000) -> np.ndarray:
        """
        Sample detection times from fitted distribution.
        
        Args:
            n_samples: Number of samples
            
        Returns:
            Array of sampled detection times
        """
        if not self.fitted_params:
            raise ValueError("Model must be fitted before sampling")
        
        rng = np.random.RandomState(self.random_state)
        
        if self.distribution == 'exponential':
            lam = self.fitted_params['lambda']
            return rng.exponential(scale=1/lam, size=n_samples)
        else:
            alpha = self.fitted_params['alpha']
            beta = self.fitted_params['beta']
            return rng.weibull(alpha, size=n_samples) * beta


class TimeToRemediationModel:
    """
    Model for remediation timeline estimation.
    
    Uses log-normal or gamma distributions for remediation duration.
    """
    
    def __init__(self,
                 distribution: str = 'lognormal',
                 random_state: Optional[int] = None):
        """
        Initialize remediation time model.
        
        Args:
            distribution: 'lognormal' or 'gamma'
            random_state: Random seed
        """
        if distribution not in ['lognormal', 'gamma']:
            raise ValueError("distribution must be 'lognormal' or 'gamma'")
        
        self.distribution = distribution
        self.random_state = random_state
        self.fitted_params: Dict[str, float] = {}
    
    def fit(self,
            remediation_times_days: List[float],
            complexity_scores: Optional[List[float]] = None) -> 'TimeToRemediationModel':
        """
        Fit remediation time model.
        
        Args:
            remediation_times_days: List of remediation times in days
            complexity_scores: Optional complexity scores (0-1)
            
        Returns:
            Self for method chaining
        """
        times_array = np.array(remediation_times_days)
        
        if self.distribution == 'lognormal':
            # Fit log-normal distribution
            log_times = np.log(times_array)
            mu = np.mean(log_times)
            sigma = np.std(log_times)
            
            self.fitted_params = {
                'mu': float(mu),
                'sigma': float(sigma)
            }
        else:
            # Fit gamma distribution
            alpha, loc, beta = stats.gamma.fit(times_array, floc=0)
            
            self.fitted_params = {
                'alpha': float(alpha),
                'beta': float(beta)
            }
        
        # If complexity scores provided, model relationship
        if complexity_scores is not None:
            complexity_array = np.array(complexity_scores)
            # Linear regression: log(time) ~ complexity
            slope, intercept = np.polyfit(complexity_array, np.log(times_array), 1)
            self.fitted_params['complexity_slope'] = float(slope)
            self.fitted_params['complexity_intercept'] = float(intercept)
        
        return self
    
    def predict(self,
                complexity_score: Optional[float] = None,
                confidence_level: float = 0.95) -> TimelineResult:
        """
        Predict remediation time.
        
        Args:
            complexity_score: Complexity score (0-1) if available
            confidence_level: Confidence interval level
            
        Returns:
            TimelineResult with predictions
        """
        if not self.fitted_params:
            raise ValueError("Model must be fitted before prediction")
        
        # Adjust parameters based on complexity if available
        mu: float
        sigma: float
        alpha: float
        beta: float
        
        if complexity_score is not None and 'complexity_slope' in self.fitted_params:
            slope = self.fitted_params['complexity_slope']
            intercept = self.fitted_params['complexity_intercept']
            adjusted_log_time = slope * complexity_score + intercept
            
            if self.distribution == 'lognormal':
                # Adjust mu based on complexity
                mu = adjusted_log_time
                sigma = self.fitted_params['sigma']
                alpha = 0.0  # Not used
                beta = 0.0   # Not used
            else:
                # For gamma, adjust scale
                alpha = self.fitted_params['alpha']
                beta = np.exp(adjusted_log_time) / alpha
                mu = 0.0    # Not used
                sigma = 0.0  # Not used
        else:
            if self.distribution == 'lognormal':
                mu = self.fitted_params['mu']
                sigma = self.fitted_params['sigma']
                alpha = 0.0  # Not used
                beta = 0.0   # Not used
            else:
                alpha = self.fitted_params['alpha']
                beta = self.fitted_params['beta']
                mu = 0.0    # Not used
                sigma = 0.0  # Not used
        
        # Calculate statistics
        if self.distribution == 'lognormal':
            mean_days = np.exp(mu + sigma**2 / 2)
            median_days = np.exp(mu)
            percentile_90 = float(stats.lognorm.ppf(0.90, sigma, scale=np.exp(mu)))
            percentile_95 = float(stats.lognorm.ppf(0.95, sigma, scale=np.exp(mu)))
            
            alpha_level = (1 - confidence_level) / 2
            ci_lower = float(stats.lognorm.ppf(alpha_level, sigma, scale=np.exp(mu)))
            ci_upper = float(stats.lognorm.ppf(1 - alpha_level, sigma, scale=np.exp(mu)))
        else:
            mean_days = alpha * beta
            median_days = float(stats.gamma.ppf(0.5, alpha, scale=beta))
            percentile_90 = float(stats.gamma.ppf(0.90, alpha, scale=beta))
            percentile_95 = float(stats.gamma.ppf(0.95, alpha, scale=beta))
            
            alpha_level = (1 - confidence_level) / 2
            ci_lower = float(stats.gamma.ppf(alpha_level, alpha, scale=beta))
            ci_upper = float(stats.gamma.ppf(1 - alpha_level, alpha, scale=beta))
        
        uncertainty_high = bool((ci_upper / ci_lower) > 3.0)
        
        return TimelineResult(
            mean_days=mean_days,
            median_days=median_days,
            percentile_90=percentile_90,
            percentile_95=percentile_95,
            confidence_interval=(ci_lower, ci_upper),
            distribution_type=self.distribution,
            phase=TimelinePhase.REMEDIATION.value,
            uncertainty_high=uncertainty_high
        )


class ViolationForecastModel:
    """
    Model for forecasting future violations using time series approaches.
    
    Implements simple exponential smoothing and trend analysis.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize forecast model"""
        self.random_state = random_state
        self.fitted = False
        self.trend_coefficient: float = 0.0
        self.base_rate: float = 0.0
        self.volatility: float = 0.0
    
    def fit(self,
            historical_counts: List[int],
            time_periods_days: Optional[List[int]] = None) -> 'ViolationForecastModel':
        """
        Fit forecast model.
        
        Args:
            historical_counts: Historical violation counts per period
            time_periods_days: Time periods (if None, assumes sequential)
            
        Returns:
            Self for method chaining
        """
        counts_array = np.array(historical_counts, dtype=float)
        n = len(counts_array)
        
        if time_periods_days is None:
            time_periods_days = list(range(n))
        
        periods_array = np.array(time_periods_days, dtype=float)
        
        # Fit linear trend
        self.trend_coefficient, intercept = np.polyfit(periods_array, counts_array, 1)
        self.base_rate = float(np.mean(counts_array))
        
        # Calculate volatility (standard deviation of residuals)
        fitted_values = self.trend_coefficient * periods_array + intercept
        residuals = counts_array - fitted_values
        self.volatility = float(np.std(residuals))
        
        self.fitted = True
        return self
    
    def forecast(self,
                forecast_days: int,
                n_simulations: int = 10000) -> ForecastResult:
        """
        Forecast violations for future period.
        
        Args:
            forecast_days: Number of days to forecast
            n_simulations: Number of Monte Carlo simulations
            
        Returns:
            ForecastResult with forecast
        """
        if not self.fitted:
            raise ValueError("Model must be fitted before forecasting")
        
        rng = np.random.RandomState(self.random_state)
        
        # Monte Carlo simulation
        forecast_samples = []
        for _ in range(n_simulations):
            # Base forecast with trend
            trend_component = self.trend_coefficient * (forecast_days / 30)  # Monthly trend
            base_forecast = self.base_rate + trend_component
            
            # Add noise
            noise = rng.normal(0, self.volatility)
            forecasted_count = max(0, base_forecast + noise)  # Non-negative
            forecast_samples.append(forecasted_count)
        
        forecast_distribution = np.array(forecast_samples)
        expected_violations = float(np.mean(forecast_distribution))
        
        # Probability of at least one violation
        violation_probability = float(np.mean(forecast_distribution > 0))
        
        # Confidence bands
        confidence_bands = {
            '50%': (float(np.percentile(forecast_distribution, 25)),
                   float(np.percentile(forecast_distribution, 75))),
            '90%': (float(np.percentile(forecast_distribution, 5)),
                   float(np.percentile(forecast_distribution, 95))),
            '95%': (float(np.percentile(forecast_distribution, 2.5)),
                   float(np.percentile(forecast_distribution, 97.5)))
        }
        
        # Determine trend
        if self.trend_coefficient > 0.1:
            trend = 'increasing'
        elif self.trend_coefficient < -0.1:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return ForecastResult(
            forecast_period_days=forecast_days,
            expected_violations=expected_violations,
            violation_probability=violation_probability,
            forecast_distribution=forecast_distribution,
            confidence_bands=confidence_bands,
            trend=trend
        )


class RegulatoryResponseTimeModel:
    """
    Model for regulatory authority response times.
    
    Models time from notification to regulatory action.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize regulatory response time model"""
        self.random_state = random_state
        self.response_times_by_severity: Dict[str, List[float]] = {}
        self.fitted_distributions: Dict[str, Dict[str, float]] = {}
    
    def fit(self,
            response_times_days: List[float],
            severity_levels: List[str]) -> 'RegulatoryResponseTimeModel':
        """
        Fit response time model by severity.
        
        Args:
            response_times_days: List of response times in days
            severity_levels: Corresponding severity levels
            
        Returns:
            Self for method chaining
        """
        # Group by severity
        for time, severity in zip(response_times_days, severity_levels):
            if severity not in self.response_times_by_severity:
                self.response_times_by_severity[severity] = []
            self.response_times_by_severity[severity].append(time)
        
        # Fit distributions for each severity
        for severity, times in self.response_times_by_severity.items():
            times_array = np.array(times)
            
            # Fit gamma distribution
            alpha, loc, beta = stats.gamma.fit(times_array, floc=0)
            
            self.fitted_distributions[severity] = {
                'alpha': float(alpha),
                'beta': float(beta),
                'mean': float(np.mean(times_array)),
                'std': float(np.std(times_array))
            }
        
        return self
    
    def predict(self,
                severity: str,
                confidence_level: float = 0.95) -> TimelineResult:
        """
        Predict regulatory response time.
        
        Args:
            severity: Severity level
            confidence_level: Confidence interval level
            
        Returns:
            TimelineResult with predictions
        """
        if severity not in self.fitted_distributions:
            raise ValueError(f"Severity '{severity}' not found in fitted data")
        
        params = self.fitted_distributions[severity]
        alpha = params['alpha']
        beta = params['beta']
        
        mean_days = params['mean']
        median_days = float(stats.gamma.ppf(0.5, alpha, scale=beta))
        percentile_90 = float(stats.gamma.ppf(0.90, alpha, scale=beta))
        percentile_95 = float(stats.gamma.ppf(0.95, alpha, scale=beta))
        
        alpha_level = (1 - confidence_level) / 2
        ci_lower = float(stats.gamma.ppf(alpha_level, alpha, scale=beta))
        ci_upper = float(stats.gamma.ppf(1 - alpha_level, alpha, scale=beta))
        
        uncertainty_high = bool((ci_upper / ci_lower) > 4.0)
        
        return TimelineResult(
            mean_days=mean_days,
            median_days=median_days,
            percentile_90=percentile_90,
            percentile_95=percentile_95,
            confidence_interval=(ci_lower, ci_upper),
            distribution_type='gamma',
            phase=TimelinePhase.REGULATORY_RESPONSE.value,
            uncertainty_high=uncertainty_high
        )
