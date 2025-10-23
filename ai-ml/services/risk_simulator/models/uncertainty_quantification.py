"""
Uncertainty Quantification Models

This module implements advanced uncertainty quantification methods for regulatory
risk assessment, including sensitivity analysis, scenario analysis, and confidence
estimation across multiple risk dimensions.

Models:
- SensitivityAnalyzer: Global and local sensitivity analysis
- ScenarioAnalyzer: Best/worst/expected case scenario modeling
- ConfidenceBandEstimator: Time-varying confidence estimation
- UncertaintyPropagator: Propagate uncertainty through risk models
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
import numpy as np
from scipy import stats
from scipy.stats import qmc


class SensitivityMethod(Enum):
    """Sensitivity analysis methods"""
    SOBOL = "sobol"
    MORRIS = "morris"
    CORRELATION = "correlation"
    VARIANCE_BASED = "variance_based"


class ScenarioType(Enum):
    """Scenario types"""
    BEST_CASE = "best_case"
    EXPECTED = "expected"
    WORST_CASE = "worst_case"
    CUSTOM = "custom"


@dataclass
class SensitivityResult:
    """Result container for sensitivity analysis"""
    parameter_name: str
    sensitivity_index: float
    total_sensitivity_index: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    rank: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'parameter_name': self.parameter_name,
            'sensitivity_index': float(self.sensitivity_index),
            'total_sensitivity_index': float(self.total_sensitivity_index) if self.total_sensitivity_index else None,
            'confidence_interval': tuple(float(x) for x in self.confidence_interval) if self.confidence_interval else None,
            'rank': self.rank
        }


@dataclass
class ScenarioResult:
    """Result container for scenario analysis"""
    scenario_type: str
    risk_value: float
    probability: float
    parameter_values: Dict[str, float]
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'scenario_type': self.scenario_type,
            'risk_value': float(self.risk_value),
            'probability': float(self.probability),
            'parameter_values': {k: float(v) for k, v in self.parameter_values.items()},
            'description': self.description
        }


@dataclass
class UncertaintyResult:
    """Result container for uncertainty quantification"""
    mean: float
    median: float
    std: float
    variance: float
    skewness: float
    kurtosis: float
    percentiles: Dict[str, float]
    confidence_bands: Dict[str, Tuple[float, float]]
    coefficient_of_variation: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'mean': float(self.mean),
            'median': float(self.median),
            'std': float(self.std),
            'variance': float(self.variance),
            'skewness': float(self.skewness),
            'kurtosis': float(self.kurtosis),
            'percentiles': {k: float(v) for k, v in self.percentiles.items()},
            'confidence_bands': {
                k: tuple(float(x) for x in v) 
                for k, v in self.confidence_bands.items()
            },
            'coefficient_of_variation': float(self.coefficient_of_variation)
        }


class SensitivityAnalyzer:
    """
    Global and local sensitivity analysis for risk models.
    
    Implements Sobol indices and Morris screening methods.
    """
    
    def __init__(self,
                 method: SensitivityMethod = SensitivityMethod.SOBOL,
                 random_state: Optional[int] = None):
        """
        Initialize sensitivity analyzer.
        
        Args:
            method: Sensitivity analysis method
            random_state: Random seed for reproducibility
        """
        self.method = method
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def analyze(self,
                model_func: Callable,
                parameters: Dict[str, Tuple[float, float]],
                n_samples: int = 10000) -> List[SensitivityResult]:
        """
        Perform sensitivity analysis.
        
        Args:
            model_func: Model function to analyze (takes dict of parameters, returns float)
            parameters: Dictionary of parameter names to (min, max) ranges
            n_samples: Number of samples for analysis
            
        Returns:
            List of SensitivityResult ordered by importance
        """
        if self.method == SensitivityMethod.SOBOL:
            return self._sobol_sensitivity(model_func, parameters, n_samples)
        elif self.method == SensitivityMethod.MORRIS:
            return self._morris_sensitivity(model_func, parameters, n_samples)
        elif self.method == SensitivityMethod.CORRELATION:
            return self._correlation_sensitivity(model_func, parameters, n_samples)
        else:
            return self._variance_based_sensitivity(model_func, parameters, n_samples)
    
    def _sobol_sensitivity(self,
                          model_func: Callable,
                          parameters: Dict[str, Tuple[float, float]],
                          n_samples: int) -> List[SensitivityResult]:
        """Sobol sensitivity analysis"""
        param_names = list(parameters.keys())
        n_params = len(param_names)
        
        # Generate Sobol samples
        sampler = qmc.Sobol(d=n_params, scramble=True)
        samples_unit = sampler.random(n=n_samples)
        
        # Scale to parameter ranges
        samples = np.zeros_like(samples_unit)
        for i, param_name in enumerate(param_names):
            min_val, max_val = parameters[param_name]
            samples[:, i] = min_val + samples_unit[:, i] * (max_val - min_val)
        
        # Evaluate model
        outputs = np.array([
            model_func({param_names[i]: samples[j, i] for i in range(n_params)})
            for j in range(n_samples)
        ])
        
        # Calculate first-order Sobol indices (simplified)
        total_variance = np.var(outputs)
        results = []
        
        for i, param_name in enumerate(param_names):
            # Compute conditional variance
            # Group by parameter value bins
            n_bins = 10
            bins = np.linspace(samples[:, i].min(), samples[:, i].max(), n_bins + 1)
            bin_indices = np.digitize(samples[:, i], bins) - 1
            
            conditional_means = np.array([
                outputs[bin_indices == b].mean() if np.sum(bin_indices == b) > 0 else 0
                for b in range(n_bins)
            ])
            
            # Variance of conditional means
            var_cond_means = np.var(conditional_means)
            
            # First-order sensitivity index
            S_i = var_cond_means / total_variance if total_variance > 0 else 0
            
            results.append(SensitivityResult(
                parameter_name=param_name,
                sensitivity_index=float(S_i),
                total_sensitivity_index=None,  # Could compute with more sampling
                confidence_interval=None
            ))
        
        # Rank by sensitivity
        results.sort(key=lambda x: x.sensitivity_index, reverse=True)
        for rank, result in enumerate(results, 1):
            result.rank = rank
        
        return results
    
    def _morris_sensitivity(self,
                           model_func: Callable,
                           parameters: Dict[str, Tuple[float, float]],
                           n_samples: int) -> List[SensitivityResult]:
        """Morris screening method (Elementary Effects)"""
        param_names = list(parameters.keys())
        n_params = len(param_names)
        n_trajectories = max(10, n_samples // (n_params + 1))
        
        # Morris sampling parameters
        levels = 10
        delta = levels / (2 * (levels - 1))
        
        elementary_effects = {name: [] for name in param_names}
        
        for _ in range(n_trajectories):
            # Generate base point
            base = self.rng.randint(0, levels, size=n_params)
            
            # Evaluate at base
            base_params = {
                param_names[i]: parameters[param_names[i]][0] + 
                               base[i] * (parameters[param_names[i]][1] - parameters[param_names[i]][0]) / (levels - 1)
                for i in range(n_params)
            }
            base_output = model_func(base_params)
            
            # Compute elementary effects
            for i in range(n_params):
                # Perturb parameter i
                perturbed = base.copy()
                perturbed[i] = min(levels - 1, perturbed[i] + int(delta * (levels - 1)))
                
                perturbed_params = {
                    param_names[j]: parameters[param_names[j]][0] + 
                                   perturbed[j] * (parameters[param_names[j]][1] - parameters[param_names[j]][0]) / (levels - 1)
                    for j in range(n_params)
                }
                perturbed_output = model_func(perturbed_params)
                
                # Elementary effect
                ee = (perturbed_output - base_output) / delta
                elementary_effects[param_names[i]].append(ee)
        
        # Calculate sensitivity indices (mean absolute elementary effects)
        results = []
        for param_name in param_names:
            ee_array = np.array(elementary_effects[param_name])
            mu_star = np.mean(np.abs(ee_array))  # Mean absolute effect
            sigma = np.std(ee_array)  # Standard deviation
            
            results.append(SensitivityResult(
                parameter_name=param_name,
                sensitivity_index=float(mu_star),
                total_sensitivity_index=float(sigma),  # Use sigma as measure of interactions
                confidence_interval=None
            ))
        
        # Rank by sensitivity
        results.sort(key=lambda x: x.sensitivity_index, reverse=True)
        for rank, result in enumerate(results, 1):
            result.rank = rank
        
        return results
    
    def _correlation_sensitivity(self,
                                 model_func: Callable,
                                 parameters: Dict[str, Tuple[float, float]],
                                 n_samples: int) -> List[SensitivityResult]:
        """Correlation-based sensitivity (Pearson correlation)"""
        param_names = list(parameters.keys())
        n_params = len(param_names)
        
        # Latin Hypercube Sampling
        sampler = qmc.LatinHypercube(d=n_params)
        samples_unit = sampler.random(n=n_samples)
        
        # Scale to parameter ranges
        samples = np.zeros_like(samples_unit)
        for i, param_name in enumerate(param_names):
            min_val, max_val = parameters[param_name]
            samples[:, i] = min_val + samples_unit[:, i] * (max_val - min_val)
        
        # Evaluate model
        outputs = np.array([
            model_func({param_names[i]: samples[j, i] for i in range(n_params)})
            for j in range(n_samples)
        ])
        
        # Calculate correlations
        results = []
        for i, param_name in enumerate(param_names):
            correlation = np.corrcoef(samples[:, i], outputs)[0, 1]
            
            results.append(SensitivityResult(
                parameter_name=param_name,
                sensitivity_index=float(abs(correlation)),  # Use absolute correlation
                confidence_interval=None
            ))
        
        # Rank by sensitivity
        results.sort(key=lambda x: x.sensitivity_index, reverse=True)
        for rank, result in enumerate(results, 1):
            result.rank = rank
        
        return results
    
    def _variance_based_sensitivity(self,
                                    model_func: Callable,
                                    parameters: Dict[str, Tuple[float, float]],
                                    n_samples: int) -> List[SensitivityResult]:
        """Simple variance-based sensitivity"""
        param_names = list(parameters.keys())
        n_params = len(param_names)
        
        # Sample parameters
        samples = {
            name: self.rng.uniform(min_val, max_val, size=n_samples)
            for name, (min_val, max_val) in parameters.items()
        }
        
        # Evaluate model
        outputs = np.array([
            model_func({name: samples[name][i] for name in param_names})
            for i in range(n_samples)
        ])
        
        total_variance = np.var(outputs)
        
        # Calculate variance contribution of each parameter
        results = []
        for param_name in param_names:
            # Fix this parameter at median, vary others
            median_val = float(np.median(samples[param_name]))
            
            conditional_outputs = []
            for _ in range(100):  # Smaller sample for conditional
                params = {
                    name: self.rng.uniform(*parameters[name])
                    for name in param_names if name != param_name
                }
                params[param_name] = median_val
                conditional_outputs.append(model_func(params))
            
            conditional_variance = np.var(conditional_outputs)
            variance_reduction = (total_variance - conditional_variance) / total_variance if total_variance > 0 else 0
            
            results.append(SensitivityResult(
                parameter_name=param_name,
                sensitivity_index=float(max(0, variance_reduction)),
                confidence_interval=None
            ))
        
        # Rank by sensitivity
        results.sort(key=lambda x: x.sensitivity_index, reverse=True)
        for rank, result in enumerate(results, 1):
            result.rank = rank
        
        return results


class ScenarioAnalyzer:
    """
    Scenario analysis for regulatory risk assessment.
    
    Generates and analyzes best/worst/expected case scenarios.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize scenario analyzer"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def analyze_scenarios(self,
                         model_func: Callable,
                         parameters: Dict[str, Tuple[float, float]],
                         custom_scenarios: Optional[List[Dict[str, float]]] = None) -> List[ScenarioResult]:
        """
        Analyze multiple scenarios.
        
        Args:
            model_func: Model function (takes dict of parameters, returns float)
            parameters: Dictionary of parameter names to (min, max) ranges
            custom_scenarios: Optional list of custom parameter sets
            
        Returns:
            List of ScenarioResult
        """
        results = []
        
        # Best case (optimistic parameters)
        best_case_params = {name: min_val for name, (min_val, max_val) in parameters.items()}
        best_case_value = model_func(best_case_params)
        results.append(ScenarioResult(
            scenario_type=ScenarioType.BEST_CASE.value,
            risk_value=float(best_case_value),
            probability=0.10,  # Estimated probability
            parameter_values=best_case_params,
            description="Best case scenario with optimistic assumptions"
        ))
        
        # Expected case (median parameters)
        expected_params = {
            name: (min_val + max_val) / 2 
            for name, (min_val, max_val) in parameters.items()
        }
        expected_value = model_func(expected_params)
        results.append(ScenarioResult(
            scenario_type=ScenarioType.EXPECTED.value,
            risk_value=float(expected_value),
            probability=0.60,  # Estimated probability
            parameter_values=expected_params,
            description="Expected case scenario with median assumptions"
        ))
        
        # Worst case (pessimistic parameters)
        worst_case_params = {name: max_val for name, (min_val, max_val) in parameters.items()}
        worst_case_value = model_func(worst_case_params)
        results.append(ScenarioResult(
            scenario_type=ScenarioType.WORST_CASE.value,
            risk_value=float(worst_case_value),
            probability=0.10,  # Estimated probability
            parameter_values=worst_case_params,
            description="Worst case scenario with pessimistic assumptions"
        ))
        
        # Custom scenarios
        if custom_scenarios:
            for i, custom_params in enumerate(custom_scenarios):
                custom_value = model_func(custom_params)
                results.append(ScenarioResult(
                    scenario_type=ScenarioType.CUSTOM.value,
                    risk_value=float(custom_value),
                    probability=0.20 / len(custom_scenarios),  # Distribute remaining probability
                    parameter_values=custom_params,
                    description=f"Custom scenario {i+1}"
                ))
        
        return results


class UncertaintyPropagator:
    """
    Propagate uncertainty through complex risk models using Monte Carlo.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize uncertainty propagator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def propagate(self,
                 model_func: Callable,
                 parameter_distributions: Dict[str, Tuple[str, Dict[str, float]]],
                 n_simulations: int = 10000) -> UncertaintyResult:
        """
        Propagate uncertainty through model.
        
        Args:
            model_func: Model function (takes dict of parameters, returns float)
            parameter_distributions: Dict of parameter names to (distribution_type, params)
                                    e.g., {'param1': ('normal', {'mean': 0, 'std': 1})}
            n_simulations: Number of Monte Carlo simulations
            
        Returns:
            UncertaintyResult with comprehensive statistics
        """
        # Sample from parameter distributions
        samples = {}
        for param_name, (dist_type, dist_params) in parameter_distributions.items():
            samples[param_name] = self._sample_distribution(
                dist_type,
                dist_params,
                n_simulations
            )
        
        # Evaluate model for all simulations
        outputs = np.array([
            model_func({name: samples[name][i] for name in samples.keys()})
            for i in range(n_simulations)
        ])
        
        # Calculate statistics
        mean = float(np.mean(outputs))
        median = float(np.median(outputs))
        std = float(np.std(outputs))
        variance = float(np.var(outputs))
        skewness = float(stats.skew(outputs))
        kurtosis = float(stats.kurtosis(outputs))
        
        # Percentiles
        percentiles = {
            'p10': float(np.percentile(outputs, 10)),
            'p25': float(np.percentile(outputs, 25)),
            'p50': float(np.percentile(outputs, 50)),
            'p75': float(np.percentile(outputs, 75)),
            'p90': float(np.percentile(outputs, 90)),
            'p95': float(np.percentile(outputs, 95)),
            'p99': float(np.percentile(outputs, 99))
        }
        
        # Confidence bands
        confidence_bands = {
            '68%': (float(np.percentile(outputs, 16)), float(np.percentile(outputs, 84))),
            '90%': (float(np.percentile(outputs, 5)), float(np.percentile(outputs, 95))),
            '95%': (float(np.percentile(outputs, 2.5)), float(np.percentile(outputs, 97.5))),
            '99%': (float(np.percentile(outputs, 0.5)), float(np.percentile(outputs, 99.5)))
        }
        
        # Coefficient of variation
        cv = std / abs(mean) if mean != 0 else float('inf')
        
        return UncertaintyResult(
            mean=mean,
            median=median,
            std=std,
            variance=variance,
            skewness=skewness,
            kurtosis=kurtosis,
            percentiles=percentiles,
            confidence_bands=confidence_bands,
            coefficient_of_variation=float(cv)
        )
    
    def _sample_distribution(self,
                            dist_type: str,
                            dist_params: Dict[str, float],
                            n_samples: int) -> np.ndarray:
        """Sample from specified distribution"""
        if dist_type == 'normal':
            return self.rng.normal(
                dist_params['mean'],
                dist_params['std'],
                size=n_samples
            )
        elif dist_type == 'uniform':
            return self.rng.uniform(
                dist_params['min'],
                dist_params['max'],
                size=n_samples
            )
        elif dist_type == 'lognormal':
            return self.rng.lognormal(
                dist_params['mean'],
                dist_params['std'],
                size=n_samples
            )
        elif dist_type == 'triangular':
            return self.rng.triangular(
                dist_params['left'],
                dist_params['mode'],
                dist_params['right'],
                size=n_samples
            )
        elif dist_type == 'beta':
            return self.rng.beta(
                dist_params['alpha'],
                dist_params['beta'],
                size=n_samples
            )
        else:
            raise ValueError(f"Unsupported distribution type: {dist_type}")
