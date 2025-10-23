"""
Regulatory Risk Models

This module implements probabilistic models for assessing regulatory compliance
risks using Bayesian inference and Monte Carlo simulation.

Models:
- ViolationProbabilityModel: Beta-Binomial model for violation likelihood
- ViolationFrequencyModel: Poisson/Negative Binomial for violation counts
- ViolationSeverityClassifier: Severity classification and scoring
- RegulatoryRiskAssessor: Integrated regulatory risk assessment
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats
import pymc as pm
import arviz as az


class ViolationSeverity(Enum):
    """Violation severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class JurisdictionType(Enum):
    """Regulatory jurisdiction types"""
    FEDERAL = "federal"
    STATE = "state"
    LOCAL = "local"
    INTERNATIONAL = "international"


@dataclass
class RegulatoryRiskResult:
    """Result container for regulatory risk assessment"""
    violation_probability: float
    expected_violations_per_year: float
    severity_distribution: Dict[str, float]
    risk_score: float
    confidence_interval_95: Tuple[float, float]
    jurisdiction_risks: Dict[str, float]
    posterior_samples: Optional[np.ndarray] = None
    convergence_diagnostics: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'violation_probability': float(self.violation_probability),
            'expected_violations_per_year': float(self.expected_violations_per_year),
            'severity_distribution': {k: float(v) for k, v in self.severity_distribution.items()},
            'risk_score': float(self.risk_score),
            'confidence_interval_95': tuple(float(x) for x in self.confidence_interval_95),
            'jurisdiction_risks': {k: float(v) for k, v in self.jurisdiction_risks.items()},
            'convergence_diagnostics': self.convergence_diagnostics or {}
        }


class ViolationProbabilityModel:
    """
    Bayesian Beta-Binomial model for violation probability estimation.
    
    Uses historical compliance data to estimate the probability of
    regulatory violations using conjugate prior-posterior updating.
    """
    
    def __init__(self,
                 prior_alpha: float = 2.0,
                 prior_beta: float = 10.0,
                 random_state: Optional[int] = None):
        """
        Initialize violation probability model.
        
        Args:
            prior_alpha: Beta prior alpha parameter (prior successes)
            prior_beta: Beta prior beta parameter (prior failures)
            random_state: Random seed for reproducibility
        """
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        self.random_state = random_state
        self.posterior_alpha: Optional[float] = None
        self.posterior_beta: Optional[float] = None
        self.trace = None
        
    def fit(self,
            n_violations: int,
            n_opportunities: int,
            mcmc_draws: int = 2000,
            mcmc_tune: int = 1000) -> 'ViolationProbabilityModel':
        """
        Fit the model using observed violation data.
        
        Args:
            n_violations: Number of observed violations
            n_opportunities: Total number of opportunities for violations
            mcmc_draws: Number of MCMC samples to draw
            mcmc_tune: Number of tuning steps
            
        Returns:
            Self for method chaining
        """
        # Conjugate update (analytical)
        self.posterior_alpha = self.prior_alpha + n_violations
        self.posterior_beta = self.prior_beta + (n_opportunities - n_violations)
        
        # MCMC sampling for uncertainty quantification
        with pm.Model() as model:
            # Prior
            p = pm.Beta('p', alpha=self.prior_alpha, beta=self.prior_beta)
            
            # Likelihood
            violations = pm.Binomial('violations',
                                    n=n_opportunities,
                                    p=p,
                                    observed=n_violations)
            
            # Sample
            self.trace = pm.sample(
                draws=mcmc_draws,
                tune=mcmc_tune,
                random_seed=self.random_state,
                return_inferencedata=True,
                progressbar=False
            )
        
        return self
    
    def predict_probability(self, credible_interval: float = 0.95) -> Tuple[float, Tuple[float, float]]:
        """
        Predict violation probability with credible interval.
        
        Args:
            credible_interval: Credible interval level (default 95%)
            
        Returns:
            Tuple of (mean probability, (lower bound, upper bound))
        """
        if self.posterior_alpha is None or self.posterior_beta is None:
            raise ValueError("Model must be fitted before prediction")
        
        # Mean of posterior Beta distribution
        mean_prob = self.posterior_alpha / (self.posterior_alpha + self.posterior_beta)
        
        # Credible interval
        alpha_level = (1 - credible_interval) / 2
        lower = stats.beta.ppf(alpha_level, self.posterior_alpha, self.posterior_beta)
        upper = stats.beta.ppf(1 - alpha_level, self.posterior_alpha, self.posterior_beta)
        
        return mean_prob, (float(lower), float(upper))
    
    def sample_posterior(self, n_samples: int = 10000) -> np.ndarray:
        """
        Sample from posterior distribution.
        
        Args:
            n_samples: Number of samples to draw
            
        Returns:
            Array of posterior samples
        """
        if self.posterior_alpha is None or self.posterior_beta is None:
            raise ValueError("Model must be fitted before sampling")
        
        rng = np.random.RandomState(self.random_state)
        return rng.beta(self.posterior_alpha, self.posterior_beta, size=n_samples)
    
    def get_convergence_diagnostics(self) -> Dict[str, Any]:
        """Get MCMC convergence diagnostics"""
        if self.trace is None:
            return {}
        
        rhat = az.rhat(self.trace)
        ess = az.ess(self.trace)
        
        return {
            'rhat': float(rhat['p'].values),
            'ess_bulk': float(ess['p'].values),
            'converged': bool(rhat['p'].values < 1.01)
        }


class ViolationFrequencyModel:
    """
    Poisson/Negative Binomial model for violation frequency estimation.
    
    Models the number of violations expected over time periods,
    with overdispersion handling via Negative Binomial.
    """
    
    def __init__(self,
                 model_type: str = 'negative_binomial',
                 random_state: Optional[int] = None):
        """
        Initialize violation frequency model.
        
        Args:
            model_type: 'poisson' or 'negative_binomial'
            random_state: Random seed for reproducibility
        """
        if model_type not in ['poisson', 'negative_binomial']:
            raise ValueError("model_type must be 'poisson' or 'negative_binomial'")
        
        self.model_type = model_type
        self.random_state = random_state
        self.fitted_lambda: Optional[float] = None
        self.fitted_alpha: Optional[float] = None
        self.trace = None
        
    def fit(self,
            violation_counts: List[int],
            mcmc_draws: int = 2000,
            mcmc_tune: int = 1000) -> 'ViolationFrequencyModel':
        """
        Fit the model using observed violation counts.
        
        Args:
            violation_counts: List of violation counts per period
            mcmc_draws: Number of MCMC samples
            mcmc_tune: Number of tuning steps
            
        Returns:
            Self for method chaining
        """
        violation_array = np.array(violation_counts)
        
        with pm.Model() as model:
            if self.model_type == 'poisson':
                # Poisson model
                lambda_param = pm.Exponential('lambda', lam=1.0)
                violations = pm.Poisson('violations',
                                       mu=lambda_param,
                                       observed=violation_array)
            else:
                # Negative Binomial (handles overdispersion)
                mu = pm.Exponential('mu', lam=1.0)
                alpha = pm.Exponential('alpha', lam=1.0)
                violations = pm.NegativeBinomial('violations',
                                                mu=mu,
                                                alpha=alpha,
                                                observed=violation_array)
            
            # Sample
            self.trace = pm.sample(
                draws=mcmc_draws,
                tune=mcmc_tune,
                random_seed=self.random_state,
                return_inferencedata=True,
                progressbar=False
            )
        
        # Extract fitted parameters
        if self.model_type == 'poisson':
            self.fitted_lambda = float(self.trace.posterior['lambda'].mean())
        else:
            self.fitted_lambda = float(self.trace.posterior['mu'].mean())
            self.fitted_alpha = float(self.trace.posterior['alpha'].mean())
        
        return self
    
    def predict_frequency(self,
                         time_horizon: float = 1.0,
                         credible_interval: float = 0.95) -> Tuple[float, Tuple[float, float]]:
        """
        Predict violation frequency over time horizon.
        
        Args:
            time_horizon: Time period in years
            credible_interval: Credible interval level
            
        Returns:
            Tuple of (expected frequency, (lower bound, upper bound))
        """
        if self.fitted_lambda is None:
            raise ValueError("Model must be fitted before prediction")
        
        # Scale lambda by time horizon
        scaled_lambda = self.fitted_lambda * time_horizon
        
        if self.model_type == 'poisson':
            mean_freq = scaled_lambda
            # Use Poisson quantiles
            alpha_level = (1 - credible_interval) / 2
            lower = stats.poisson.ppf(alpha_level, scaled_lambda)
            upper = stats.poisson.ppf(1 - alpha_level, scaled_lambda)
        else:
            if self.fitted_alpha is None:
                raise ValueError("Alpha parameter not fitted for Negative Binomial model")
            mean_freq = scaled_lambda
            # Use Negative Binomial quantiles
            alpha_level = (1 - credible_interval) / 2
            p = self.fitted_alpha / (self.fitted_alpha + scaled_lambda)
            n = self.fitted_alpha
            lower = stats.nbinom.ppf(alpha_level, n, p)
            upper = stats.nbinom.ppf(1 - alpha_level, n, p)
        
        return mean_freq, (float(lower), float(upper))
    
    def sample_violations(self, time_horizon: float = 1.0, n_samples: int = 10000) -> np.ndarray:
        """
        Sample violation counts from fitted distribution.
        
        Args:
            time_horizon: Time period in years
            n_samples: Number of samples
            
        Returns:
            Array of sampled violation counts
        """
        if self.fitted_lambda is None:
            raise ValueError("Model must be fitted before sampling")
        
        rng = np.random.RandomState(self.random_state)
        scaled_lambda = self.fitted_lambda * time_horizon
        
        if self.model_type == 'poisson':
            return rng.poisson(scaled_lambda, size=n_samples)
        else:
            if self.fitted_alpha is None:
                raise ValueError("Alpha parameter not fitted for Negative Binomial model")
            p = self.fitted_alpha / (self.fitted_alpha + scaled_lambda)
            n = max(1, int(self.fitted_alpha))  # Ensure n >= 1
            return rng.negative_binomial(n, p, size=n_samples)


class ViolationSeverityClassifier:
    """
    Classifier for violation severity with risk scoring.
    
    Assigns severity levels and calculates risk scores based on
    violation characteristics and regulatory context.
    """
    
    # Severity weights for risk scoring
    SEVERITY_WEIGHTS = {
        ViolationSeverity.LOW: 1.0,
        ViolationSeverity.MEDIUM: 3.0,
        ViolationSeverity.HIGH: 7.0,
        ViolationSeverity.CRITICAL: 15.0
    }
    
    def __init__(self,
                 severity_thresholds: Optional[Dict[str, float]] = None):
        """
        Initialize severity classifier.
        
        Args:
            severity_thresholds: Custom thresholds for severity classification
        """
        self.severity_thresholds = severity_thresholds or {
            'critical': 0.9,
            'high': 0.7,
            'medium': 0.4,
            'low': 0.0
        }
    
    def classify(self,
                impact_score: float,
                probability: float,
                regulatory_priority: float = 0.5) -> ViolationSeverity:
        """
        Classify violation severity.
        
        Args:
            impact_score: Impact score (0-1)
            probability: Violation probability (0-1)
            regulatory_priority: Priority level from regulator (0-1)
            
        Returns:
            ViolationSeverity level
        """
        # Combined risk score
        risk_score = (impact_score * 0.5 + 
                     probability * 0.3 + 
                     regulatory_priority * 0.2)
        
        # Classify based on thresholds
        if risk_score >= self.severity_thresholds['critical']:
            return ViolationSeverity.CRITICAL
        elif risk_score >= self.severity_thresholds['high']:
            return ViolationSeverity.HIGH
        elif risk_score >= self.severity_thresholds['medium']:
            return ViolationSeverity.MEDIUM
        else:
            return ViolationSeverity.LOW
    
    def calculate_risk_score(self,
                           violation_probability: float,
                           severity_distribution: Dict[ViolationSeverity, float]) -> float:
        """
        Calculate overall risk score from severity distribution.
        
        Args:
            violation_probability: Overall violation probability
            severity_distribution: Distribution across severity levels
            
        Returns:
            Overall risk score
        """
        weighted_severity = sum(
            self.SEVERITY_WEIGHTS[severity] * prob
            for severity, prob in severity_distribution.items()
        )
        
        return violation_probability * weighted_severity
    
    def get_severity_distribution(self,
                                 n_simulations: int = 10000,
                                 impact_scores: Optional[np.ndarray] = None,
                                 probabilities: Optional[np.ndarray] = None,
                                 regulatory_priorities: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        Get severity distribution from Monte Carlo simulation.
        
        Args:
            n_simulations: Number of simulations
            impact_scores: Array of impact scores (or None for random)
            probabilities: Array of probabilities (or None for random)
            regulatory_priorities: Array of priorities (or None for random)
            
        Returns:
            Dictionary mapping severity levels to probabilities
        """
        rng = np.random.RandomState(42)
        
        # Generate random inputs if not provided
        if impact_scores is None:
            impact_scores = rng.uniform(0, 1, n_simulations)
        if probabilities is None:
            probabilities = rng.uniform(0, 1, n_simulations)
        if regulatory_priorities is None:
            regulatory_priorities = rng.uniform(0, 1, n_simulations)
        
        # Classify all simulations
        severities = [
            self.classify(imp, prob, reg_pri)
            for imp, prob, reg_pri in zip(impact_scores, probabilities, regulatory_priorities)
        ]
        
        # Calculate distribution
        total = len(severities)
        distribution = {
            severity.value: sum(1 for s in severities if s == severity) / total
            for severity in ViolationSeverity
        }
        
        return distribution


class RegulatoryRiskAssessor:
    """
    Integrated regulatory risk assessment combining all models.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize regulatory risk assessor"""
        self.random_state = random_state
        self.probability_model = ViolationProbabilityModel(random_state=random_state)
        self.frequency_model = ViolationFrequencyModel(random_state=random_state)
        self.severity_classifier = ViolationSeverityClassifier()
    
    def assess_risk(self,
                   historical_violations: int,
                   historical_opportunities: int,
                   violation_counts_per_period: List[int],
                   jurisdictions: Optional[Dict[str, Dict[str, Any]]] = None,
                   time_horizon: float = 1.0) -> RegulatoryRiskResult:
        """
        Perform comprehensive regulatory risk assessment.
        
        Args:
            historical_violations: Number of past violations
            historical_opportunities: Number of past opportunities
            violation_counts_per_period: List of violation counts
            jurisdictions: Dictionary of jurisdiction-specific data
            time_horizon: Forecast time horizon in years
            
        Returns:
            RegulatoryRiskResult with comprehensive assessment
        """
        # Fit probability model
        self.probability_model.fit(historical_violations, historical_opportunities)
        mean_prob, ci_95 = self.probability_model.predict_probability()
        
        # Fit frequency model
        self.frequency_model.fit(violation_counts_per_period)
        expected_freq, _ = self.frequency_model.predict_frequency(time_horizon)
        
        # Get severity distribution
        severity_dist = self.severity_classifier.get_severity_distribution()
        severity_enum_dist = {
            ViolationSeverity[k.upper()]: v 
            for k, v in severity_dist.items()
        }
        
        # Calculate risk score
        risk_score = self.severity_classifier.calculate_risk_score(
            mean_prob,
            severity_enum_dist
        )
        
        # Jurisdiction-specific risks
        jurisdiction_risks = {}
        if jurisdictions:
            for jurisdiction, data in jurisdictions.items():
                jur_violations = data.get('violations', 0)
                jur_opportunities = data.get('opportunities', 1)
                jur_prob = (jur_violations + 1) / (jur_opportunities + 2)  # Laplace smoothing
                jurisdiction_risks[jurisdiction] = float(jur_prob)
        
        # Get convergence diagnostics
        convergence = self.probability_model.get_convergence_diagnostics()
        
        # Sample posterior
        posterior_samples = self.probability_model.sample_posterior()
        
        return RegulatoryRiskResult(
            violation_probability=mean_prob,
            expected_violations_per_year=expected_freq,
            severity_distribution=severity_dist,
            risk_score=risk_score,
            confidence_interval_95=ci_95,
            jurisdiction_risks=jurisdiction_risks,
            posterior_samples=posterior_samples,
            convergence_diagnostics=convergence
        )
