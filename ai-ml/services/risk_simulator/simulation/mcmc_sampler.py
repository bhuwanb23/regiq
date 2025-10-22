"""
MCMC Sampling Engine for Bayesian Inference.

Provides MCMC sampling functionality including:
- NUTS (No-U-Turn Sampler)
- Metropolis-Hastings
- Chain management
- Sampling configuration
"""

import numpy as np
import pymc as pm
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class MCMCConfig:
    """Configuration for MCMC sampling"""
    draws: int = 2000
    tune: int = 1000
    chains: int = 4
    target_accept: float = 0.95
    max_treedepth: int = 10
    random_seed: Optional[int] = None
    progressbar: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'draws': self.draws,
            'tune': self.tune,
            'chains': self.chains,
            'target_accept': self.target_accept,
            'max_treedepth': self.max_treedepth,
            'random_seed': self.random_seed
        }


@dataclass
class MCMCSamplingResult:
    """Results from MCMC sampling"""
    sampler_type: str
    posterior_samples: Dict[str, np.ndarray]
    n_chains: int
    n_draws: int
    n_tune: int
    acceptance_rate: float
    divergences: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'sampler_type': self.sampler_type,
            'n_chains': self.n_chains,
            'n_draws': self.n_draws,
            'n_tune': self.n_tune,
            'acceptance_rate': float(self.acceptance_rate),
            'divergences': self.divergences,
            'metadata': self.metadata
        }


class MCMCSampler:
    """
    MCMC sampling engine with support for multiple samplers.
    
    Supports:
    - NUTS (default, most efficient)
    - Metropolis-Hastings
    - Custom step methods
    
    Example:
        >>> sampler = MCMCSampler(sampler_type='nuts')
        >>> config = MCMCConfig(draws=2000, chains=4)
        >>> result = sampler.sample(model, config)
    """
    
    def __init__(self, sampler_type: str = 'nuts'):
        """
        Initialize MCMC sampler.
        
        Args:
            sampler_type: Type of sampler ('nuts', 'metropolis', 'slice')
        """
        self.sampler_type = sampler_type
        self.idata = None
        
    def sample(self,
               model: pm.Model,
               config: Optional[MCMCConfig] = None) -> MCMCSamplingResult:
        """
        Run MCMC sampling.
        
        Args:
            model: PyMC model to sample from
            config: MCMC configuration
            
        Returns:
            MCMCSamplingResult with posterior samples and diagnostics
        """
        if config is None:
            config = MCMCConfig()
        
        logger.info(f"Running {self.sampler_type.upper()} sampling "
                   f"({config.chains} chains, {config.draws} draws)")
        
        with model:
            # Select step method
            if self.sampler_type == 'nuts':
                # NUTS is default in PyMC5
                step = None
            elif self.sampler_type == 'metropolis':
                step = pm.Metropolis()
            elif self.sampler_type == 'slice':
                step = pm.Slice()
            else:
                step = None
            
            # Sample
            self.idata = pm.sample(
                draws=config.draws,
                tune=config.tune,
                chains=config.chains,
                step=step,
                target_accept=config.target_accept,
                max_treedepth=config.max_treedepth,
                random_seed=config.random_seed,
                return_inferencedata=True,
                progressbar=config.progressbar
            )
        
        # Extract results
        return self._extract_results(config)
    
    def _extract_results(self, config: MCMCConfig) -> MCMCSamplingResult:
        """Extract sampling results"""
        # Get posterior samples
        posterior_samples = {}
        for var_name in self.idata.posterior.data_vars:
            samples = self.idata.posterior[var_name].values
            # Flatten chains: (chains, draws, ...) -> (chains*draws, ...)
            samples_flat = samples.reshape(-1, *samples.shape[2:])
            posterior_samples[var_name] = samples_flat
        
        # Get sampling statistics
        if hasattr(self.idata, 'sample_stats'):
            acceptance = self.idata.sample_stats.get('acceptance_rate', None)
            if acceptance is not None:
                acceptance_rate = float(acceptance.values.mean())
            else:
                acceptance_rate = 0.0
            
            divergences_arr = self.idata.sample_stats.get('diverging', None)
            if divergences_arr is not None:
                divergences = int(divergences_arr.values.sum())
            else:
                divergences = 0
        else:
            acceptance_rate = 0.0
            divergences = 0
        
        return MCMCSamplingResult(
            sampler_type=self.sampler_type,
            posterior_samples=posterior_samples,
            n_chains=config.chains,
            n_draws=config.draws,
            n_tune=config.tune,
            acceptance_rate=acceptance_rate,
            divergences=divergences,
            metadata={
                'target_accept': config.target_accept,
                'max_treedepth': config.max_treedepth
            }
        )


if __name__ == "__main__":
    print("="*60)
    print("MCMC Sampler - Example Usage")
    print("="*60)
    
    # Create a simple model
    with pm.Model() as model:
        # Prior
        mu = pm.Normal('mu', mu=0, sigma=1)
        sigma = pm.HalfNormal('sigma', sigma=1)
        
        # Likelihood
        obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=np.random.randn(100))
    
    # Test NUTS sampler
    print("\n1. NUTS Sampler")
    print("-"*60)
    
    nuts_sampler = MCMCSampler(sampler_type='nuts')
    config = MCMCConfig(draws=1000, tune=500, chains=2, random_seed=42)
    
    result = nuts_sampler.sample(model, config)
    
    print(f"Sampler: {result.sampler_type.upper()}")
    print(f"Chains: {result.n_chains}")
    print(f"Draws per chain: {result.n_draws}")
    print(f"Acceptance rate: {result.acceptance_rate:.3f}")
    print(f"Divergences: {result.divergences}")
    
    print(f"\nPosterior samples:")
    for param, samples in result.posterior_samples.items():
        print(f"  {param}: shape {samples.shape}, mean {samples.mean():.3f}")
    
    print(f"\n{'='*60}")
    print("MCMC sampler example completed!")
    print('='*60)
