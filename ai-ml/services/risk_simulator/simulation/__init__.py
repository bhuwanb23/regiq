"""Simulation Framework for Compliance Risk Assessment.

This module provides comprehensive simulation tools including:
- Monte Carlo simulation
- Bayesian inference
- Parameter space definition
- Advanced sampling methods
- MCMC sampling
- Convergence diagnostics
"""

# Monte Carlo imports
from .monte_carlo import (
    MonteCarloSimulator,
    SamplingMethod,
    DistributionType,
    SimulationResult
)

# Parameter Space imports
from .parameter_space import (
    Parameter,
    ParameterSpace,
    DistributionType as ParamDistributionType
)

# Bayesian Model imports
from .bayesian_models import (
    BayesianRiskModel,
    BayesianModelResult,
    ComplianceViolationModel,
    PenaltyAmountModel,
    TimeToViolationModel,
    HierarchicalRiskModel,
    compare_models
)

# MCMC Sampler imports
from .mcmc_sampler import (
    MCMCSampler,
    MCMCConfig,
    MCMCSamplingResult
)

# Diagnostics imports
from .diagnostics import (
    ConvergenceDiagnostics,
    check_convergence,
    geweke_test,
    compute_autocorrelation,
    effective_sample_size_simple,
    diagnose_divergences
)

__all__ = [
    # Monte Carlo
    'MonteCarloSimulator',
    'SamplingMethod',
    'DistributionType',
    'SimulationResult',
    # Parameter Space
    'Parameter',
    'ParameterSpace',
    # Bayesian Models
    'BayesianRiskModel',
    'BayesianModelResult',
    'ComplianceViolationModel',
    'PenaltyAmountModel',
    'TimeToViolationModel',
    'HierarchicalRiskModel',
    'compare_models',
    # MCMC Sampling
    'MCMCSampler',
    'MCMCConfig',
    'MCMCSamplingResult',
    # Diagnostics
    'ConvergenceDiagnostics',
    'check_convergence',
    'geweke_test',
    'compute_autocorrelation',
    'effective_sample_size_simple',
    'diagnose_divergences',
]