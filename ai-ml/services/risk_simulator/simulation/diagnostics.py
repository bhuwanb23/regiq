"""
Convergence Diagnostics for MCMC Sampling.

Provides comprehensive convergence checking including:
- Gelman-Rubin R-hat statistic
- Effective Sample Size (ESS)
- Geweke diagnostic
- Autocorrelation analysis
- Automated warnings
"""

import numpy as np
import arviz as az
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConvergenceDiagnostics:
    """
    Comprehensive convergence diagnostics for MCMC.
    
    Attributes:
        rhat: R-hat statistics per parameter
        ess_bulk: Bulk effective sample size
        ess_tail: Tail effective sample size
        geweke_z: Geweke Z-scores
        converged: Overall convergence status
        warnings: List of warning messages
    """
    rhat: Dict[str, float]
    ess_bulk: Dict[str, float]
    ess_tail: Dict[str, float]
    geweke_z: Dict[str, float]
    converged: bool
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'rhat': {k: float(v) for k, v in self.rhat.items()},
            'ess_bulk': {k: float(v) for k, v in self.ess_bulk.items()},
            'ess_tail': {k: float(v) for k, v in self.ess_tail.items()},
            'geweke_z': {k: float(v) for k, v in self.geweke_z.items()},
            'converged': self.converged,
            'warnings': self.warnings,
            'metadata': self.metadata
        }
    
    def summary(self) -> str:
        """Generate text summary of diagnostics"""
        lines = [
            "MCMC Convergence Diagnostics",
            "=" * 60,
            f"Overall Status: {'✅ CONVERGED' if self.converged else '❌ NOT CONVERGED'}",
            "",
            "R-hat Statistics (should be < 1.01):",
            "-" * 60
        ]
        
        for param, value in self.rhat.items():
            status = "✅" if value < 1.01 else "⚠️"
            lines.append(f"  {param}: {value:.4f} {status}")
        
        lines.extend([
            "",
            "Effective Sample Size (ESS):",
            "-" * 60
        ])
        
        for param in self.ess_bulk:
            bulk = self.ess_bulk[param]
            tail = self.ess_tail[param]
            status = "✅" if bulk > 400 and tail > 400 else "⚠️"
            lines.append(f"  {param}:")
            lines.append(f"    Bulk ESS: {bulk:.0f} {status}")
            lines.append(f"    Tail ESS: {tail:.0f} {status}")
        
        if self.geweke_z:
            lines.extend([
                "",
                "Geweke Z-scores (should be < 2):",
                "-" * 60
            ])
            for param, z in self.geweke_z.items():
                status = "✅" if abs(z) < 2 else "⚠️"
                lines.append(f"  {param}: {z:.3f} {status}")
        
        if self.warnings:
            lines.extend([
                "",
                "Warnings:",
                "-" * 60
            ])
            for warning in self.warnings:
                lines.append(f"  ⚠️  {warning}")
        
        return '\n'.join(lines)


def check_convergence(idata: Any,
                      rhat_threshold: float = 1.01,
                      ess_threshold: int = 400) -> ConvergenceDiagnostics:
    """
    Comprehensive convergence check for MCMC samples.
    
    Args:
        idata: ArviZ InferenceData object
        rhat_threshold: Maximum acceptable R-hat value
        ess_threshold: Minimum acceptable ESS
        
    Returns:
        ConvergenceDiagnostics object
    """
    logger.info("Checking MCMC convergence...")
    
    warnings = []
    
    # 1. R-hat (Gelman-Rubin)
    rhat_dict = {}
    rhat_data = az.rhat(idata)
    for var in rhat_data.data_vars:
        rhat_val = float(rhat_data[var].values.max())
        rhat_dict[var] = rhat_val
        if rhat_val > rhat_threshold:
            warnings.append(f"R-hat for '{var}' = {rhat_val:.4f} > {rhat_threshold}")
    
    # 2. Effective Sample Size
    ess_bulk_dict = {}
    ess_tail_dict = {}
    
    ess_bulk = az.ess(idata, method='bulk')
    ess_tail = az.ess(idata, method='tail')
    
    for var in ess_bulk.data_vars:
        bulk_val = float(ess_bulk[var].values.min())
        tail_val = float(ess_tail[var].values.min())
        
        ess_bulk_dict[var] = bulk_val
        ess_tail_dict[var] = tail_val
        
        if bulk_val < ess_threshold:
            warnings.append(f"Bulk ESS for '{var}' = {bulk_val:.0f} < {ess_threshold}")
        if tail_val < ess_threshold:
            warnings.append(f"Tail ESS for '{var}' = {tail_val:.0f} < {ess_threshold}")
    
    # 3. Geweke diagnostic
    geweke_dict = {}
    try:
        for var in idata.posterior.data_vars:
            samples = idata.posterior[var].values
            # Flatten chains
            samples_flat = samples.reshape(-1, *samples.shape[2:])
            if samples_flat.ndim == 1:
                z_score = geweke_test(samples_flat)
                geweke_dict[var] = z_score
                if abs(z_score) > 2:
                    warnings.append(f"Geweke Z-score for '{var}' = {z_score:.3f} (|Z| > 2)")
    except Exception as e:
        logger.warning(f"Geweke test failed: {e}")
    
    # Overall convergence
    converged = (
        all(r < rhat_threshold for r in rhat_dict.values()) and
        all(e > ess_threshold for e in ess_bulk_dict.values()) and
        all(e > ess_threshold for e in ess_tail_dict.values())
    )
    
    if converged:
        logger.info("✅ MCMC converged successfully")
    else:
        logger.warning(f"⚠️  MCMC convergence issues detected ({len(warnings)} warnings)")
    
    return ConvergenceDiagnostics(
        rhat=rhat_dict,
        ess_bulk=ess_bulk_dict,
        ess_tail=ess_tail_dict,
        geweke_z=geweke_dict,
        converged=converged,
        warnings=warnings,
        metadata={
            'rhat_threshold': rhat_threshold,
            'ess_threshold': ess_threshold
        }
    )


def geweke_test(chain: np.ndarray,
                first: float = 0.1,
                last: float = 0.5) -> float:
    """
    Geweke convergence diagnostic.
    
    Compares means of first and last portions of chain.
    
    Args:
        chain: MCMC chain (1D array)
        first: Fraction of chain for first segment
        last: Fraction of chain for last segment
        
    Returns:
        Z-score (should be < 2 for convergence)
    """
    n = len(chain)
    
    # First segment
    n_first = int(n * first)
    first_segment = chain[:n_first]
    first_mean = np.mean(first_segment)
    first_var = np.var(first_segment) / n_first
    
    # Last segment
    n_last = int(n * last)
    last_segment = chain[-n_last:]
    last_mean = np.mean(last_segment)
    last_var = np.var(last_segment) / n_last
    
    # Z-score
    z = (first_mean - last_mean) / np.sqrt(first_var + last_var)
    
    return float(z)


def compute_autocorrelation(chain: np.ndarray, max_lag: int = 40) -> np.ndarray:
    """
    Compute autocorrelation function.
    
    Args:
        chain: MCMC chain
        max_lag: Maximum lag to compute
        
    Returns:
        Autocorrelation values for lags 0 to max_lag
    """
    n = len(chain)
    chain_centered = chain - np.mean(chain)
    
    autocorr = np.zeros(max_lag + 1)
    var = np.var(chain)
    
    for lag in range(max_lag + 1):
        if lag == 0:
            autocorr[lag] = 1.0
        else:
            autocorr[lag] = np.mean(chain_centered[:n-lag] * chain_centered[lag:]) / var
    
    return autocorr


def effective_sample_size_simple(chain: np.ndarray) -> float:
    """
    Simple ESS calculation using autocorrelation.
    
    Args:
        chain: MCMC chain
        
    Returns:
        Effective sample size
    """
    n = len(chain)
    autocorr = compute_autocorrelation(chain, max_lag=min(n-1, 100))
    
    # Sum autocorrelations until they become negative
    tau = 1.0
    for i in range(1, len(autocorr)):
        if autocorr[i] < 0:
            break
        tau += 2 * autocorr[i]
    
    ess = n / tau
    return float(max(1.0, ess))


def diagnose_divergences(idata: Any) -> Dict[str, Any]:
    """
    Analyze divergent transitions in NUTS sampling.
    
    Args:
        idata: InferenceData object
        
    Returns:
        Dictionary with divergence analysis
    """
    if not hasattr(idata, 'sample_stats'):
        return {'divergences': 0, 'divergence_rate': 0.0}
    
    diverging = idata.sample_stats.get('diverging', None)
    
    if diverging is None:
        return {'divergences': 0, 'divergence_rate': 0.0}
    
    n_divergences = int(diverging.values.sum())
    total_samples = diverging.values.size
    divergence_rate = n_divergences / total_samples
    
    result = {
        'divergences': n_divergences,
        'total_samples': total_samples,
        'divergence_rate': float(divergence_rate)
    }
    
    if n_divergences > 0:
        logger.warning(f"⚠️  {n_divergences} divergent transitions detected "
                      f"({divergence_rate:.1%} of samples)")
        result['warning'] = "Divergences detected - consider increasing target_accept"
    
    return result


if __name__ == "__main__":
    import pymc as pm
    
    print("="*60)
    print("Convergence Diagnostics - Example Usage")
    print("="*60)
    
    # Create and sample a simple model
    np.random.seed(42)
    observed_data = np.random.normal(5, 2, size=100)
    
    with pm.Model() as model:
        mu = pm.Normal('mu', mu=0, sigma=10)
        sigma = pm.HalfNormal('sigma', sigma=5)
        likelihood = pm.Normal('y', mu=mu, sigma=sigma, observed=observed_data)
        
        idata = pm.sample(
            draws=1000,
            tune=500,
            chains=4,
            random_seed=42,
            return_inferencedata=True,
            progressbar=False
        )
    
    # Check convergence
    print("\nRunning convergence diagnostics...")
    diagnostics = check_convergence(idata)
    
    print("\n" + diagnostics.summary())
    
    # Check divergences
    print("\nDivergence Analysis:")
    print("-"*60)
    div_analysis = diagnose_divergences(idata)
    for key, value in div_analysis.items():
        print(f"  {key}: {value}")
    
    print(f"\n{'='*60}")
    print("Convergence diagnostics example completed!")
    print('='*60)
