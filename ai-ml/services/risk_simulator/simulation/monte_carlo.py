"""
Monte Carlo Simulation Engine for Compliance Risk Assessment.

This module provides a comprehensive Monte Carlo simulation framework for
assessing regulatory compliance risks, including:
- Parameter space definition
- Multiple sampling strategies
- Parallel execution
- Convergence monitoring
- Statistical analysis

Example:
    >>> from services.risk_simulator.simulation import MonteCarloSimulator
    >>> simulator = MonteCarloSimulator(n_simulations=10000)
    >>> result = simulator.run(risk_function, parameters)
    >>> print(result.mean, result.confidence_interval)
"""

import numpy as np
from typing import Dict, List, Optional, Callable, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class SamplingMethod(Enum):
    """Supported sampling methods for Monte Carlo simulation"""
    SIMPLE_RANDOM = "simple_random"  # Simple Random Sampling
    LATIN_HYPERCUBE = "latin_hypercube"  # Latin Hypercube Sampling (default)
    STRATIFIED = "stratified"  # Stratified Sampling
    SOBOL = "sobol"  # Sobol Quasi-Random Sequences
    ADAPTIVE = "adaptive"  # Adaptive Importance Sampling


class DistributionType(Enum):
    """Supported probability distributions"""
    UNIFORM = "uniform"
    NORMAL = "normal"
    LOGNORMAL = "lognormal"
    BETA = "beta"
    GAMMA = "gamma"
    EXPONENTIAL = "exponential"
    TRIANGULAR = "triangular"
    WEIBULL = "weibull"


@dataclass
class SimulationResult:
    """Results from Monte Carlo simulation"""
    samples: np.ndarray
    mean: float
    median: float
    std: float
    variance: float
    percentiles: Dict[str, float]
    confidence_intervals: Dict[str, Tuple[float, float]]
    convergence_achieved: bool
    n_simulations: int
    execution_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to JSON-serializable dictionary"""
        return {
            'mean': float(self.mean),
            'median': float(self.median),
            'std': float(self.std),
            'variance': float(self.variance),
            'percentiles': {k: float(v) for k, v in self.percentiles.items()},
            'confidence_intervals': {
                k: (float(v[0]), float(v[1])) 
                for k, v in self.confidence_intervals.items()
            },
            'convergence_achieved': self.convergence_achieved,
            'n_simulations': self.n_simulations,
            'execution_time': self.execution_time,
            'metadata': self.metadata
        }
    
    def summary(self) -> str:
        """Generate text summary of results"""
        summary_lines = [
            f"Monte Carlo Simulation Results",
            f"{'='*50}",
            f"Simulations: {self.n_simulations:,}",
            f"Execution Time: {self.execution_time:.2f}s",
            f"Convergence: {'Yes' if self.convergence_achieved else 'No'}",
            f"",
            f"Statistics:",
            f"  Mean: {self.mean:.4f}",
            f"  Median: {self.median:.4f}",
            f"  Std Dev: {self.std:.4f}",
            f"",
            f"Percentiles:",
        ]
        
        for pct, val in sorted(self.percentiles.items()):
            summary_lines.append(f"  {pct}: {val:.4f}")
        
        summary_lines.append(f"")
        summary_lines.append(f"Confidence Intervals:")
        for ci, (lower, upper) in sorted(self.confidence_intervals.items()):
            summary_lines.append(f"  {ci}: [{lower:.4f}, {upper:.4f}]")
        
        return '\n'.join(summary_lines)


class MonteCarloSimulator:
    """
    Monte Carlo simulation engine for risk assessment.
    
    Supports multiple sampling strategies, parallel execution, and
    comprehensive statistical analysis.
    
    Args:
        n_simulations: Number of Monte Carlo simulations to run
        sampling_method: Sampling strategy to use
        n_workers: Number of parallel workers (None = serial execution)
        random_state: Random seed for reproducibility
        convergence_threshold: Threshold for convergence check (relative std change)
        convergence_window: Number of iterations to check for convergence
    
    Example:
        >>> simulator = MonteCarloSimulator(
        ...     n_simulations=10000,
        ...     sampling_method=SamplingMethod.LATIN_HYPERCUBE,
        ...     n_workers=4
        ... )
        >>> result = simulator.run(compliance_risk_function, params)
    """
    
    def __init__(self,
                 n_simulations: int = 10000,
                 sampling_method: SamplingMethod = SamplingMethod.LATIN_HYPERCUBE,
                 n_workers: Optional[int] = None,
                 random_state: Optional[int] = None,
                 convergence_threshold: float = 0.01,
                 convergence_window: int = 1000):
        """Initialize Monte Carlo simulator"""
        self.n_simulations = n_simulations
        self.sampling_method = sampling_method
        self.n_workers = n_workers
        self.random_state = random_state
        self.convergence_threshold = convergence_threshold
        self.convergence_window = convergence_window
        
        # Set random seed
        if random_state is not None:
            np.random.seed(random_state)
        
        logger.info(f"Initialized MonteCarloSimulator with {n_simulations} simulations")
    
    def run(self,
            model_function: Callable,
            parameters: Dict[str, Dict[str, Any]],
            percentiles: Optional[List[float]] = None,
            confidence_levels: Optional[List[float]] = None) -> SimulationResult:
        """
        Run Monte Carlo simulation.
        
        Args:
            model_function: Function to evaluate (takes dict of parameters)
            parameters: Dictionary of parameter definitions
                {
                    'param_name': {
                        'distribution': 'normal',
                        'mean': 0,
                        'std': 1
                    }
                }
            percentiles: Percentiles to calculate (default: [5, 25, 50, 75, 95])
            confidence_levels: Confidence levels (default: [0.90, 0.95, 0.99])
        
        Returns:
            SimulationResult with comprehensive statistics
        """
        import time
        start_time = time.time()
        
        # Default values
        if percentiles is None:
            percentiles = [5, 25, 50, 75, 95]
        if confidence_levels is None:
            confidence_levels = [0.90, 0.95, 0.99]
        
        logger.info(f"Starting Monte Carlo simulation with {self.n_simulations} iterations")
        
        # Generate samples
        parameter_samples = self._generate_samples(parameters)
        
        # Run simulations
        if self.n_workers is not None and self.n_workers > 1:
            results = self._run_parallel(model_function, parameter_samples)
        else:
            results = self._run_serial(model_function, parameter_samples)
        
        # Check convergence
        convergence_achieved = self._check_convergence(results)
        
        # Calculate statistics
        mean_val = float(np.mean(results))
        median_val = float(np.median(results))
        std_val = float(np.std(results))
        var_val = float(np.var(results))
        
        # Calculate percentiles
        pct_dict = {
            f"p{int(p)}": float(np.percentile(results, p))
            for p in percentiles
        }
        
        # Calculate confidence intervals
        ci_dict = {}
        for cl in confidence_levels:
            alpha = 1 - cl
            lower = float(np.percentile(results, 100 * alpha / 2))
            upper = float(np.percentile(results, 100 * (1 - alpha / 2)))
            ci_dict[f"ci_{int(cl*100)}"] = (lower, upper)
        
        execution_time = time.time() - start_time
        
        logger.info(f"Simulation completed in {execution_time:.2f}s")
        
        return SimulationResult(
            samples=results,
            mean=mean_val,
            median=median_val,
            std=std_val,
            variance=var_val,
            percentiles=pct_dict,
            confidence_intervals=ci_dict,
            convergence_achieved=convergence_achieved,
            n_simulations=self.n_simulations,
            execution_time=execution_time,
            metadata={
                'sampling_method': self.sampling_method.value,
                'n_workers': self.n_workers,
                'parameters': list(parameters.keys()),
                'timestamp': datetime.now().isoformat()
            }
        )
    
    def _generate_samples(self, parameters: Dict[str, Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """Generate parameter samples based on sampling method"""
        n_params = len(parameters)
        param_names = list(parameters.keys())
        
        if self.sampling_method == SamplingMethod.SIMPLE_RANDOM:
            samples = self._simple_random_sampling(parameters)
        elif self.sampling_method == SamplingMethod.LATIN_HYPERCUBE:
            samples = self._latin_hypercube_sampling(parameters)
        elif self.sampling_method == SamplingMethod.STRATIFIED:
            samples = self._stratified_sampling(parameters)
        elif self.sampling_method == SamplingMethod.SOBOL:
            samples = self._sobol_sampling(parameters)
        elif self.sampling_method == SamplingMethod.ADAPTIVE:
            samples = self._adaptive_sampling(parameters)
        else:
            raise ValueError(f"Unknown sampling method: {self.sampling_method}")
        
        return samples
    
    def _simple_random_sampling(self, parameters: Dict[str, Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """Simple random sampling from distributions"""
        samples = {}
        for param_name, param_config in parameters.items():
            dist_type = param_config.get('distribution', 'normal')
            samples[param_name] = self._sample_distribution(
                dist_type, param_config, self.n_simulations
            )
        return samples
    
    def _latin_hypercube_sampling(self, parameters: Dict[str, Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """Latin Hypercube Sampling for better coverage"""
        from scipy.stats import qmc
        
        n_params = len(parameters)
        param_names = list(parameters.keys())
        
        # Generate LHS samples in [0, 1]
        sampler = qmc.LatinHypercube(d=n_params)
        lhs_samples = sampler.random(n=self.n_simulations)
        
        # Transform to parameter distributions
        samples = {}
        for i, param_name in enumerate(param_names):
            param_config = parameters[param_name]
            uniform_samples = lhs_samples[:, i]
            
            # Transform uniform samples to target distribution
            samples[param_name] = self._inverse_transform_sampling(
                uniform_samples, param_config
            )
        
        return samples
    
    def _stratified_sampling(self, parameters: Dict[str, Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """Stratified sampling with equal-sized strata"""
        n_strata = int(np.sqrt(self.n_simulations))
        samples_per_stratum = self.n_simulations // n_strata
        remainder = self.n_simulations % n_strata
        
        samples = {}
        for param_name, param_config in parameters.items():
            param_samples = []
            
            for i in range(n_strata):
                # Sample within stratum
                stratum_lower = i / n_strata
                stratum_upper = (i + 1) / n_strata
                
                # Add remainder to last stratum
                n_samples = samples_per_stratum + (remainder if i == n_strata - 1 else 0)
                
                uniform_samples = np.random.uniform(
                    stratum_lower, stratum_upper, n_samples
                )
                
                stratum_samples = self._inverse_transform_sampling(
                    uniform_samples, param_config
                )
                param_samples.extend(stratum_samples)
            
            samples[param_name] = np.array(param_samples)
        
        return samples
    
    def _sobol_sampling(self, parameters: Dict[str, Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """Sobol quasi-random sequence sampling"""
        from scipy.stats import qmc
        
        n_params = len(parameters)
        param_names = list(parameters.keys())
        
        # Generate Sobol samples
        sampler = qmc.Sobol(d=n_params, scramble=True)
        sobol_samples = sampler.random(n=self.n_simulations)
        
        # Transform to parameter distributions
        samples = {}
        for i, param_name in enumerate(param_names):
            param_config = parameters[param_name]
            uniform_samples = sobol_samples[:, i]
            
            samples[param_name] = self._inverse_transform_sampling(
                uniform_samples, param_config
            )
        
        return samples
    
    def _adaptive_sampling(self, parameters: Dict[str, Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """Adaptive importance sampling (simplified version)"""
        # Start with simple random sampling
        return self._simple_random_sampling(parameters)
    
    def _inverse_transform_sampling(self,
                                     uniform_samples: np.ndarray,
                                     param_config: Dict[str, Any]) -> np.ndarray:
        """Transform uniform [0,1] samples to target distribution"""
        from scipy import stats
        
        dist_type = param_config.get('distribution', 'normal')
        
        if dist_type == 'uniform' or dist_type == DistributionType.UNIFORM.value:
            low = param_config.get('low', 0)
            high = param_config.get('high', 1)
            return stats.uniform(loc=low, scale=high-low).ppf(uniform_samples)
        
        elif dist_type == 'normal' or dist_type == DistributionType.NORMAL.value:
            mean = param_config.get('mean', 0)
            std = param_config.get('std', 1)
            return stats.norm(loc=mean, scale=std).ppf(uniform_samples)
        
        elif dist_type == 'lognormal' or dist_type == DistributionType.LOGNORMAL.value:
            mean = param_config.get('mean', 0)
            std = param_config.get('std', 1)
            return stats.lognorm(s=std, scale=np.exp(mean)).ppf(uniform_samples)
        
        elif dist_type == 'beta' or dist_type == DistributionType.BETA.value:
            alpha = param_config.get('alpha', 2)
            beta = param_config.get('beta', 2)
            return stats.beta(a=alpha, b=beta).ppf(uniform_samples)
        
        elif dist_type == 'gamma' or dist_type == DistributionType.GAMMA.value:
            shape = param_config.get('shape', 2)
            scale = param_config.get('scale', 1)
            return stats.gamma(a=shape, scale=scale).ppf(uniform_samples)
        
        elif dist_type == 'exponential' or dist_type == DistributionType.EXPONENTIAL.value:
            rate = param_config.get('rate', 1)
            return stats.expon(scale=1/rate).ppf(uniform_samples)
        
        elif dist_type == 'triangular' or dist_type == DistributionType.TRIANGULAR.value:
            low = param_config.get('low', 0)
            mode = param_config.get('mode', 0.5)
            high = param_config.get('high', 1)
            c = (mode - low) / (high - low)
            return stats.triang(c=c, loc=low, scale=high-low).ppf(uniform_samples)
        
        else:
            # Default to normal distribution
            logger.warning(f"Unknown distribution type: {dist_type}, using normal")
            mean = param_config.get('mean', 0)
            std = param_config.get('std', 1)
            return stats.norm(loc=mean, scale=std).ppf(uniform_samples)
    
    def _sample_distribution(self,
                            dist_type: str,
                            param_config: Dict[str, Any],
                            n_samples: int) -> np.ndarray:
        """Sample from a probability distribution"""
        if dist_type == 'uniform' or dist_type == DistributionType.UNIFORM.value:
            low = param_config.get('low', 0)
            high = param_config.get('high', 1)
            return np.random.uniform(low, high, n_samples)
        
        elif dist_type == 'normal' or dist_type == DistributionType.NORMAL.value:
            mean = param_config.get('mean', 0)
            std = param_config.get('std', 1)
            return np.random.normal(mean, std, n_samples)
        
        elif dist_type == 'lognormal' or dist_type == DistributionType.LOGNORMAL.value:
            mean = param_config.get('mean', 0)
            std = param_config.get('std', 1)
            return np.random.lognormal(mean, std, n_samples)
        
        elif dist_type == 'beta' or dist_type == DistributionType.BETA.value:
            alpha = param_config.get('alpha', 2)
            beta = param_config.get('beta', 2)
            return np.random.beta(alpha, beta, n_samples)
        
        elif dist_type == 'gamma' or dist_type == DistributionType.GAMMA.value:
            shape = param_config.get('shape', 2)
            scale = param_config.get('scale', 1)
            return np.random.gamma(shape, scale, n_samples)
        
        elif dist_type == 'exponential' or dist_type == DistributionType.EXPONENTIAL.value:
            rate = param_config.get('rate', 1)
            return np.random.exponential(1/rate, n_samples)
        
        elif dist_type == 'triangular' or dist_type == DistributionType.TRIANGULAR.value:
            low = param_config.get('low', 0)
            mode = param_config.get('mode', 0.5)
            high = param_config.get('high', 1)
            return np.random.triangular(low, mode, high, n_samples)
        
        else:
            # Default to normal
            logger.warning(f"Unknown distribution: {dist_type}, using normal")
            mean = param_config.get('mean', 0)
            std = param_config.get('std', 1)
            return np.random.normal(mean, std, n_samples)
    
    def _run_serial(self,
                   model_function: Callable,
                   parameter_samples: Dict[str, np.ndarray]) -> np.ndarray:
        """Run simulations serially"""
        results = []
        
        for i in range(self.n_simulations):
            params = {k: v[i] for k, v in parameter_samples.items()}
            result = model_function(params)
            results.append(result)
            
            if (i + 1) % 1000 == 0:
                logger.debug(f"Completed {i+1}/{self.n_simulations} simulations")
        
        return np.array(results)
    
    def _run_parallel(self,
                     model_function: Callable,
                     parameter_samples: Dict[str, np.ndarray]) -> np.ndarray:
        """Run simulations in parallel"""
        results = []
        
        with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
            futures = []
            
            for i in range(self.n_simulations):
                params = {k: v[i] for k, v in parameter_samples.items()}
                future = executor.submit(model_function, params)
                futures.append(future)
            
            for i, future in enumerate(as_completed(futures)):
                results.append(future.result())
                
                if (i + 1) % 1000 == 0:
                    logger.debug(f"Completed {i+1}/{self.n_simulations} simulations")
        
        return np.array(results)
    
    def _check_convergence(self, results: np.ndarray) -> bool:
        """Check if simulation has converged"""
        if len(results) < self.convergence_window * 2:
            return False
        
        # Calculate running mean
        window = self.convergence_window
        early_mean = np.mean(results[:window])
        late_mean = np.mean(results[-window:])
        
        # Check relative change
        if early_mean == 0:
            return bool(abs(late_mean) < self.convergence_threshold)
        
        relative_change = abs((late_mean - early_mean) / early_mean)
        
        return bool(relative_change < self.convergence_threshold)


if __name__ == "__main__":
    # Example usage
    print("="*60)
    print("Monte Carlo Simulator - Example Usage")
    print("="*60)
    
    # Define a simple compliance risk function
    def compliance_risk(params):
        """
        Simple compliance risk model:
        Risk = violation_rate * penalty_amount * enforcement_probability
        """
        return (params['violation_rate'] * 
                params['penalty_amount'] * 
                params['enforcement_prob'])
    
    # Define parameters
    parameters = {
        'violation_rate': {
            'distribution': 'beta',
            'alpha': 2,
            'beta': 5
        },
        'penalty_amount': {
            'distribution': 'lognormal',
            'mean': 10,
            'std': 0.5
        },
        'enforcement_prob': {
            'distribution': 'uniform',
            'low': 0.5,
            'high': 0.9
        }
    }
    
    # Run simulation with different sampling methods
    for method in [SamplingMethod.SIMPLE_RANDOM, SamplingMethod.LATIN_HYPERCUBE]:
        print(f"\n{'-'*60}")
        print(f"Sampling Method: {method.value.upper()}")
        print('-'*60)
        
        simulator = MonteCarloSimulator(
            n_simulations=5000,
            sampling_method=method,
            random_state=42
        )
        
        result = simulator.run(compliance_risk, parameters)
        
        print(result.summary())
        print(f"\nJSON Output (sample):")
        result_dict = result.to_dict()
        print(json.dumps({k: v for k, v in list(result_dict.items())[:5]}, indent=2))
    
    print(f"\n{'='*60}")
    print("Monte Carlo simulation examples completed!")
    print('='*60)
