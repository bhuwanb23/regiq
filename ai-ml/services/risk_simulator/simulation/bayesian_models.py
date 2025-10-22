"""
Bayesian Probabilistic Models for Compliance Risk Assessment.

This module provides PyMC5-based Bayesian modeling for:
- Prior specification
- Likelihood modeling  
- Posterior inference
- Predictive distributions
- Model comparison

Uses PyMC5 for improved performance over PyMC3.
"""

import numpy as np
import pymc as pm
import arviz as az
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class BayesianModelResult:
    """Results from Bayesian model inference"""
    model_name: str
    posterior_samples: Dict[str, np.ndarray]
    posterior_stats: Dict[str, Dict[str, float]]
    convergence_metrics: Dict[str, float]
    predictive_samples: Optional[np.ndarray] = None
    model_comparison: Optional[Dict[str, float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'model_name': self.model_name,
            'posterior_stats': {
                param: {k: float(v) for k, v in stats.items()}
                for param, stats in self.posterior_stats.items()
            },
            'convergence_metrics': {k: float(v) for k, v in self.convergence_metrics.items()},
            'model_comparison': self.model_comparison if self.model_comparison else {},
            'metadata': self.metadata
        }
    
    def summary(self) -> str:
        """Generate text summary"""
        lines = [
            f"Bayesian Model: {self.model_name}",
            "=" * 60,
            "",
            "Posterior Statistics:",
            "-" * 60
        ]
        
        for param, stats in self.posterior_stats.items():
            lines.append(f"{param}:")
            for stat, value in stats.items():
                lines.append(f"  {stat}: {value:.4f}")
        
        lines.extend([
            "",
            "Convergence Metrics:",
            "-" * 60
        ])
        
        for metric, value in self.convergence_metrics.items():
            lines.append(f"  {metric}: {value:.4f}")
        
        return '\n'.join(lines)


class BayesianRiskModel:
    """
    Base class for Bayesian risk models.
    
    Provides framework for:
    - Prior specification
    - Likelihood definition
    - MCMC sampling
    - Posterior analysis
    """
    
    def __init__(self, name: str = "bayesian_model"):
        """Initialize Bayesian model"""
        self.name = name
        self.model = None
        self.trace = None
        self.idata = None  # InferenceData object
        
    def build_model(self, data: Dict[str, np.ndarray]) -> pm.Model:
        """
        Build PyMC model (to be overridden by subclasses).
        
        Args:
            data: Dictionary of observed data
            
        Returns:
            PyMC model
        """
        raise NotImplementedError("Subclasses must implement build_model()")
    
    def fit(self,
            data: Dict[str, np.ndarray],
            draws: int = 2000,
            tune: int = 1000,
            chains: int = 4,
            target_accept: float = 0.95,
            random_seed: Optional[int] = None) -> BayesianModelResult:
        """
        Fit Bayesian model using MCMC sampling.
        
        Args:
            data: Observed data
            draws: Number of posterior samples per chain
            tune: Number of tuning/warmup samples
            chains: Number of MCMC chains
            target_accept: Target acceptance rate for NUTS
            random_seed: Random seed for reproducibility
            
        Returns:
            BayesianModelResult with posterior samples and diagnostics
        """
        logger.info(f"Fitting Bayesian model '{self.name}' with {chains} chains")
        
        # Build model
        self.model = self.build_model(data)
        
        # Sample from posterior
        with self.model:
            self.idata = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                target_accept=target_accept,
                random_seed=random_seed,
                return_inferencedata=True,
                progressbar=False
            )
            
            # Sample from posterior predictive
            self.idata.extend(pm.sample_posterior_predictive(
                self.idata,
                progressbar=False
            ))
        
        # Extract results
        return self._extract_results()
    
    def _extract_results(self) -> BayesianModelResult:
        """Extract results from InferenceData"""
        # Get posterior samples
        posterior_samples = {}
        posterior_stats = {}
        
        for var_name in self.idata.posterior.data_vars:
            samples = self.idata.posterior[var_name].values
            # Flatten chains
            samples_flat = samples.reshape(-1, *samples.shape[2:])
            posterior_samples[var_name] = samples_flat
            
            # Calculate statistics
            posterior_stats[var_name] = {
                'mean': float(np.mean(samples_flat)),
                'std': float(np.std(samples_flat)),
                'median': float(np.median(samples_flat)),
                'hdi_2.5%': float(np.percentile(samples_flat, 2.5)),
                'hdi_97.5%': float(np.percentile(samples_flat, 97.5))
            }
        
        # Get convergence metrics
        convergence_metrics = self._compute_convergence_metrics()
        
        # Get predictive samples if available
        predictive_samples = None
        if hasattr(self.idata, 'posterior_predictive'):
            pred_vars = list(self.idata.posterior_predictive.data_vars)
            if pred_vars:
                predictive_samples = self.idata.posterior_predictive[pred_vars[0]].values
        
        return BayesianModelResult(
            model_name=self.name,
            posterior_samples=posterior_samples,
            posterior_stats=posterior_stats,
            convergence_metrics=convergence_metrics,
            predictive_samples=predictive_samples,
            metadata={
                'n_chains': len(self.idata.posterior.chain),
                'n_draws': len(self.idata.posterior.draw)
            }
        )
    
    def _compute_convergence_metrics(self) -> Dict[str, float]:
        """Compute convergence diagnostics"""
        metrics = {}
        
        # R-hat (Gelman-Rubin statistic)
        rhat = az.rhat(self.idata)
        metrics['rhat_max'] = float(max([rhat[var].values.max() for var in rhat.data_vars]))
        metrics['rhat_mean'] = float(np.mean([rhat[var].values.mean() for var in rhat.data_vars]))
        
        # Effective sample size
        ess = az.ess(self.idata)
        metrics['ess_min'] = float(min([ess[var].values.min() for var in ess.data_vars]))
        metrics['ess_mean'] = float(np.mean([ess[var].values.mean() for var in ess.data_vars]))
        
        return metrics
    
    def predict(self, new_data: Optional[Dict[str, np.ndarray]] = None) -> np.ndarray:
        """
        Generate predictions from posterior.
        
        Args:
            new_data: New data for prediction (if None, uses posterior predictive)
            
        Returns:
            Array of predictions
        """
        if new_data is not None:
            # Posterior predictive with new data
            with self.model:
                post_pred = pm.sample_posterior_predictive(
                    self.idata,
                    predictions=True,
                    progressbar=False
                )
            pred_vars = list(post_pred.predictions.data_vars)
            return post_pred.predictions[pred_vars[0]].values
        else:
            # Use existing posterior predictive
            if hasattr(self.idata, 'posterior_predictive'):
                pred_vars = list(self.idata.posterior_predictive.data_vars)
                return self.idata.posterior_predictive[pred_vars[0]].values
            else:
                raise ValueError("No posterior predictive samples available")


class ComplianceViolationModel(BayesianRiskModel):
    """
    Bayesian model for compliance violation probability.
    
    Models violation rate as Beta-distributed with prior knowledge.
    """
    
    def __init__(self):
        super().__init__(name="compliance_violation")
    
    def build_model(self, data: Dict[str, np.ndarray]) -> pm.Model:
        """
        Build violation model.
        
        Expected data:
            - 'n_audits': Number of audits
            - 'n_violations': Number of violations observed
        """
        n_audits = data['n_audits']
        n_violations = data['n_violations']
        
        with pm.Model() as model:
            # Prior: Beta distribution for violation rate
            # Beta(2, 8) implies prior belief of ~20% violation rate
            violation_rate = pm.Beta('violation_rate', alpha=2, beta=8)
            
            # Likelihood: Binomial
            observations = pm.Binomial(
                'violations',
                n=n_audits,
                p=violation_rate,
                observed=n_violations
            )
        
        return model


class PenaltyAmountModel(BayesianRiskModel):
    """
    Bayesian model for penalty amounts.
    
    Models penalty as log-normal with hierarchical structure.
    """
    
    def __init__(self):
        super().__init__(name="penalty_amount")
    
    def build_model(self, data: Dict[str, np.ndarray]) -> pm.Model:
        """
        Build penalty model.
        
        Expected data:
            - 'observed_penalties': Array of observed penalty amounts
        """
        penalties = data['observed_penalties']
        
        with pm.Model() as model:
            # Priors
            mu = pm.Normal('mu', mu=10, sigma=2)  # Log-scale mean
            sigma = pm.HalfNormal('sigma', sigma=1)  # Log-scale std
            
            # Likelihood: Log-normal
            penalty = pm.Lognormal(
                'penalty',
                mu=mu,
                sigma=sigma,
                observed=penalties
            )
        
        return model


class TimeToViolationModel(BayesianRiskModel):
    """
    Bayesian model for time until compliance violation.
    
    Uses exponential/Weibull distribution for time-to-event.
    """
    
    def __init__(self):
        super().__init__(name="time_to_violation")
    
    def build_model(self, data: Dict[str, np.ndarray]) -> pm.Model:
        """
        Build time-to-violation model.
        
        Expected data:
            - 'observed_times': Array of time-to-violation observations
        """
        times = data['observed_times']
        
        with pm.Model() as model:
            # Prior for rate parameter
            rate = pm.Gamma('rate', alpha=2, beta=1)
            
            # Likelihood: Exponential distribution
            time_to_violation = pm.Exponential(
                'time',
                lam=rate,
                observed=times
            )
        
        return model


class HierarchicalRiskModel(BayesianRiskModel):
    """
    Hierarchical Bayesian model for multi-jurisdiction risk.
    
    Allows sharing of information across jurisdictions while
    accounting for jurisdiction-specific effects.
    """
    
    def __init__(self):
        super().__init__(name="hierarchical_risk")
    
    def build_model(self, data: Dict[str, np.ndarray]) -> pm.Model:
        """
        Build hierarchical model.
        
        Expected data:
            - 'jurisdictions': Array of jurisdiction indices
            - 'violations': Array of violation counts
            - 'n_audits': Array of audit counts per jurisdiction
        """
        jurisdictions = data['jurisdictions']
        violations = data['violations']
        n_audits = data['n_audits']
        
        n_jurisdictions = len(np.unique(jurisdictions))
        
        with pm.Model() as model:
            # Hyperpriors
            mu_alpha = pm.Normal('mu_alpha', mu=2, sigma=1)
            sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)
            
            # Jurisdiction-specific parameters
            alpha_j = pm.Normal('alpha_j', mu=mu_alpha, sigma=sigma_alpha, shape=n_jurisdictions)
            
            # Transform to probability
            p_j = pm.Deterministic('p_j', pm.math.invlogit(alpha_j))
            
            # Likelihood
            violations_obs = pm.Binomial(
                'violations_obs',
                n=n_audits,
                p=p_j[jurisdictions],
                observed=violations
            )
        
        return model


def compare_models(models: List[Tuple[str, BayesianRiskModel]], 
                   data: Dict[str, np.ndarray],
                   ic: str = 'waic') -> Dict[str, Any]:
    """
    Compare multiple Bayesian models using information criteria.
    
    Args:
        models: List of (name, model) tuples
        data: Data for model fitting
        ic: Information criterion ('waic' or 'loo')
        
    Returns:
        Dictionary with comparison results
    """
    logger.info(f"Comparing {len(models)} models using {ic.upper()}")
    
    idata_dict = {}
    
    # Fit all models
    for name, model_obj in models:
        result = model_obj.fit(data, draws=1000, tune=500, chains=2)
        idata_dict[name] = model_obj.idata
    
    # Compare using arviz
    if ic == 'waic':
        comparison = az.compare(idata_dict, ic='waic')
    else:
        comparison = az.compare(idata_dict, ic='loo')
    
    # Convert to dictionary
    comparison_dict = {
        'ranking': comparison.index.tolist(),
        'ic_values': {name: float(comparison.loc[name, ic]) for name in comparison.index},
        'weights': {name: float(comparison.loc[name, 'weight']) for name in comparison.index}
    }
    
    logger.info(f"Best model: {comparison_dict['ranking'][0]}")
    
    return comparison_dict


if __name__ == "__main__":
    print("="*60)
    print("Bayesian Risk Models - Example Usage")
    print("="*60)
    
    # Example 1: Compliance Violation Model
    print("\n1. Compliance Violation Model")
    print("-"*60)
    
    violation_model = ComplianceViolationModel()
    
    # Simulated data: 100 audits, 15 violations
    data = {
        'n_audits': 100,
        'n_violations': 15
    }
    
    result = violation_model.fit(data, draws=1000, tune=500, chains=2, random_seed=42)
    
    print(result.summary())
    print(f"\nJSON Output (sample):")
    print(json.dumps(result.to_dict(), indent=2)[:500] + "...")
    
    # Example 2: Penalty Amount Model
    print("\n\n2. Penalty Amount Model")
    print("-"*60)
    
    penalty_model = PenaltyAmountModel()
    
    # Simulated penalty data
    np.random.seed(42)
    observed_penalties = np.random.lognormal(mean=10, sigma=0.5, size=50)
    
    data = {'observed_penalties': observed_penalties}
    
    result = penalty_model.fit(data, draws=1000, tune=500, chains=2, random_seed=42)
    
    print(f"Penalty Statistics:")
    for param, stats in result.posterior_stats.items():
        print(f"\n{param}:")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  95% HDI: [{stats['hdi_2.5%']:.2f}, {stats['hdi_97.5%']:.2f}]")
    
    print(f"\n{'='*60}")
    print("Bayesian models example completed!")
    print('='*60)
