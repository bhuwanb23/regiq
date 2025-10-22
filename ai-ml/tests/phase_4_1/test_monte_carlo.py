"""
Tests for Monte Carlo Simulation Engine.

This test suite covers:
- Initialization and configuration
- Parameter space setup
- Sampling execution
- Parallel processing
- Result aggregation
- Convergence monitoring
- Distribution support
- JSON serialization
"""

import pytest
import numpy as np
import json
from typing import Dict

from services.risk_simulator.simulation.monte_carlo import (
    MonteCarloSimulator,
    SamplingMethod,
    DistributionType,
    SimulationResult
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def simple_parameters():
    """Simple parameter configuration for testing"""
    return {
        'param1': {
            'distribution': 'normal',
            'mean': 10,
            'std': 2
        },
        'param2': {
            'distribution': 'uniform',
            'low': 0,
            'high': 1
        }
    }


@pytest.fixture
def complex_parameters():
    """Complex parameter configuration with multiple distributions"""
    return {
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
        },
        'remediation_cost': {
            'distribution': 'gamma',
            'shape': 2,
            'scale': 5
        }
    }


@pytest.fixture
def simple_model():
    """Simple model function for testing"""
    def model(params: Dict) -> float:
        return params['param1'] + params['param2']
    return model


@pytest.fixture
def risk_model():
    """Compliance risk model for testing"""
    def model(params: Dict) -> float:
        return (params['violation_rate'] * 
                params['penalty_amount'] * 
                params['enforcement_prob'] + 
                params['remediation_cost'])
    return model


# ============================================================================
# Test Monte Carlo Simulator
# ============================================================================

class TestMonteCarloSimulator:
    """Tests for MonteCarloSimulator class"""
    
    def test_initialization(self):
        """Test simulator initialization"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.LATIN_HYPERCUBE,
            random_state=42
        )
        
        assert simulator.n_simulations == 1000
        assert simulator.sampling_method == SamplingMethod.LATIN_HYPERCUBE
        assert simulator.random_state == 42
        assert simulator.convergence_threshold == 0.01
        assert simulator.convergence_window == 1000
    
    def test_default_initialization(self):
        """Test simulator with default parameters"""
        simulator = MonteCarloSimulator()
        
        assert simulator.n_simulations == 10000
        assert simulator.sampling_method == SamplingMethod.LATIN_HYPERCUBE
        assert simulator.random_state is None
    
    def test_simple_random_sampling(self, simple_parameters, simple_model):
        """Test simple random sampling method"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.SIMPLE_RANDOM,
            random_state=42
        )
        
        result = simulator.run(simple_model, simple_parameters)
        
        assert isinstance(result, SimulationResult)
        assert len(result.samples) == 1000
        assert result.n_simulations == 1000
        # param1 ~ N(10, 2), param2 ~ U(0, 1), so sum should be around 10.5
        assert 9 < result.mean < 12
        assert result.std > 0
    
    def test_latin_hypercube_sampling(self, simple_parameters, simple_model):
        """Test Latin Hypercube Sampling method"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.LATIN_HYPERCUBE,
            random_state=42
        )
        
        result = simulator.run(simple_model, simple_parameters)
        
        assert isinstance(result, SimulationResult)
        assert len(result.samples) == 1000
        # LHS should provide good coverage
        assert 9 < result.mean < 12
    
    def test_stratified_sampling(self, simple_parameters, simple_model):
        """Test stratified sampling method"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.STRATIFIED,
            random_state=42
        )
        
        result = simulator.run(simple_model, simple_parameters)
        
        assert isinstance(result, SimulationResult)
        assert len(result.samples) == 1000
    
    def test_sobol_sampling(self, simple_parameters, simple_model):
        """Test Sobol quasi-random sampling"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.SOBOL,
            random_state=42
        )
        
        result = simulator.run(simple_model, simple_parameters)
        
        assert isinstance(result, SimulationResult)
        assert len(result.samples) == 1000
    
    def test_result_statistics(self, simple_parameters, simple_model):
        """Test statistical calculations in results"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.SIMPLE_RANDOM,
            random_state=42
        )
        
        result = simulator.run(simple_model, simple_parameters)
        
        # Check all statistics are present
        assert result.mean is not None
        assert result.median is not None
        assert result.std is not None
        assert result.variance is not None
        
        # Check percentiles
        assert 'p5' in result.percentiles
        assert 'p25' in result.percentiles
        assert 'p50' in result.percentiles
        assert 'p75' in result.percentiles
        assert 'p95' in result.percentiles
        
        # Check confidence intervals
        assert 'ci_90' in result.confidence_intervals
        assert 'ci_95' in result.confidence_intervals
        assert 'ci_99' in result.confidence_intervals
        
        # Median should equal p50
        assert abs(result.median - result.percentiles['p50']) < 0.01
        
        # Variance should equal std^2
        assert abs(result.variance - result.std**2) < 0.01
    
    def test_complex_distributions(self, complex_parameters, risk_model):
        """Test with multiple distribution types"""
        simulator = MonteCarloSimulator(
            n_simulations=2000,
            sampling_method=SamplingMethod.LATIN_HYPERCUBE,
            random_state=42
        )
        
        result = simulator.run(risk_model, complex_parameters)
        
        assert isinstance(result, SimulationResult)
        assert len(result.samples) == 2000
        assert result.mean > 0  # All parameters are positive
        assert result.std > 0
    
    def test_convergence_monitoring(self, simple_parameters, simple_model):
        """Test convergence detection"""
        # Large number of simulations should converge
        simulator = MonteCarloSimulator(
            n_simulations=5000,
            sampling_method=SamplingMethod.SIMPLE_RANDOM,
            random_state=42,
            convergence_threshold=0.05,
            convergence_window=1000
        )
        
        result = simulator.run(simple_model, simple_parameters)
        
        # With 5000 simulations, should likely converge
        assert isinstance(result.convergence_achieved, bool)
    
    def test_custom_percentiles(self, simple_parameters, simple_model):
        """Test custom percentile specification"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            random_state=42
        )
        
        custom_percentiles = [1.0, 10.0, 50.0, 90.0, 99.0]
        result = simulator.run(
            simple_model, 
            simple_parameters,
            percentiles=custom_percentiles
        )
        
        assert 'p1' in result.percentiles
        assert 'p10' in result.percentiles
        assert 'p50' in result.percentiles
        assert 'p90' in result.percentiles
        assert 'p99' in result.percentiles
    
    def test_result_serialization(self, simple_parameters, simple_model):
        """Test JSON serialization of results"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            random_state=42
        )
        
        result = simulator.run(simple_model, simple_parameters)
        result_dict = result.to_dict()
        
        # Check JSON serializability
        json_str = json.dumps(result_dict)
        assert isinstance(json_str, str)
        
        # Check all required fields
        assert 'mean' in result_dict
        assert 'median' in result_dict
        assert 'std' in result_dict
        assert 'percentiles' in result_dict
        assert 'confidence_intervals' in result_dict
        assert 'convergence_achieved' in result_dict
        assert 'n_simulations' in result_dict
        assert 'metadata' in result_dict
    
    def test_result_summary(self, simple_parameters, simple_model):
        """Test text summary generation"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            random_state=42
        )
        
        result = simulator.run(simple_model, simple_parameters)
        summary = result.summary()
        
        assert isinstance(summary, str)
        assert 'Monte Carlo Simulation Results' in summary
        assert 'Mean:' in summary
        assert 'Median:' in summary
        assert 'Percentiles:' in summary
        assert 'Confidence Intervals:' in summary
    
    def test_metadata_tracking(self, simple_parameters, simple_model):
        """Test metadata in results"""
        simulator = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.LATIN_HYPERCUBE,
            random_state=42
        )
        
        result = simulator.run(simple_model, simple_parameters)
        
        assert 'sampling_method' in result.metadata
        assert result.metadata['sampling_method'] == 'latin_hypercube'
        assert 'parameters' in result.metadata
        assert 'param1' in result.metadata['parameters']
        assert 'param2' in result.metadata['parameters']
        assert 'timestamp' in result.metadata


# ============================================================================
# Test Distribution Support
# ============================================================================

class TestDistributions:
    """Tests for distribution support"""
    
    def test_uniform_distribution(self):
        """Test uniform distribution sampling"""
        params = {
            'x': {
                'distribution': 'uniform',
                'low': 0,
                'high': 10
            }
        }
        
        simulator = MonteCarloSimulator(n_simulations=1000, random_state=42)
        result = simulator.run(lambda p: p['x'], params)
        
        # Mean of uniform(0, 10) should be around 5
        assert 4 < result.mean < 6
        # All samples should be in [0, 10]
        assert np.all(result.samples >= 0)
        assert np.all(result.samples <= 10)
    
    def test_normal_distribution(self):
        """Test normal distribution sampling"""
        params = {
            'x': {
                'distribution': 'normal',
                'mean': 100,
                'std': 10
            }
        }
        
        simulator = MonteCarloSimulator(n_simulations=1000, random_state=42)
        result = simulator.run(lambda p: p['x'], params)
        
        # Mean should be close to 100
        assert 95 < result.mean < 105
        # Std should be close to 10
        assert 8 < result.std < 12
    
    def test_beta_distribution(self):
        """Test beta distribution sampling"""
        params = {
            'x': {
                'distribution': 'beta',
                'alpha': 2,
                'beta': 5
            }
        }
        
        simulator = MonteCarloSimulator(n_simulations=1000, random_state=42)
        result = simulator.run(lambda p: p['x'], params)
        
        # Beta(2, 5) has mean = 2/(2+5) ≈ 0.286
        assert 0.2 < result.mean < 0.4
        # All samples should be in [0, 1]
        assert np.all(result.samples >= 0)
        assert np.all(result.samples <= 1)
    
    def test_lognormal_distribution(self):
        """Test lognormal distribution sampling"""
        params = {
            'x': {
                'distribution': 'lognormal',
                'mean': 0,
                'std': 0.5
            }
        }
        
        simulator = MonteCarloSimulator(n_simulations=1000, random_state=42)
        result = simulator.run(lambda p: p['x'], params)
        
        # Lognormal should have all positive samples
        assert np.all(result.samples > 0)
        assert result.mean > 0
    
    def test_gamma_distribution(self):
        """Test gamma distribution sampling"""
        params = {
            'x': {
                'distribution': 'gamma',
                'shape': 2,
                'scale': 3
            }
        }
        
        simulator = MonteCarloSimulator(n_simulations=1000, random_state=42)
        result = simulator.run(lambda p: p['x'], params)
        
        # Gamma(2, 3) has mean = 2*3 = 6
        assert 4 < result.mean < 8
        # All samples should be positive
        assert np.all(result.samples > 0)
    
    def test_exponential_distribution(self):
        """Test exponential distribution sampling"""
        params = {
            'x': {
                'distribution': 'exponential',
                'rate': 0.5
            }
        }
        
        simulator = MonteCarloSimulator(n_simulations=1000, random_state=42)
        result = simulator.run(lambda p: p['x'], params)
        
        # Exponential(0.5) has mean = 1/0.5 = 2
        assert 1.5 < result.mean < 2.5
        # All samples should be positive
        assert np.all(result.samples > 0)
    
    def test_triangular_distribution(self):
        """Test triangular distribution sampling"""
        params = {
            'x': {
                'distribution': 'triangular',
                'low': 0,
                'mode': 5,
                'high': 10
            }
        }
        
        simulator = MonteCarloSimulator(n_simulations=1000, random_state=42)
        result = simulator.run(lambda p: p['x'], params)
        
        # Triangular(0, 5, 10) has mean = (0+5+10)/3 ≈ 5
        assert 4 < result.mean < 6
        # All samples should be in [0, 10]
        assert np.all(result.samples >= 0)
        assert np.all(result.samples <= 10)


# ============================================================================
# Test Edge Cases
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_single_simulation(self):
        """Test with n_simulations=1"""
        params = {'x': {'distribution': 'normal', 'mean': 0, 'std': 1}}
        simulator = MonteCarloSimulator(n_simulations=1, random_state=42)
        
        result = simulator.run(lambda p: p['x'], params)
        
        assert len(result.samples) == 1
        assert result.mean == result.median
    
    def test_large_simulation(self):
        """Test with large number of simulations"""
        params = {'x': {'distribution': 'normal', 'mean': 0, 'std': 1}}
        simulator = MonteCarloSimulator(n_simulations=10000, random_state=42)
        
        result = simulator.run(lambda p: p['x'], params)
        
        assert len(result.samples) == 10000
        # With 10000 samples, mean should be very close to 0
        assert abs(result.mean) < 0.1
    
    def test_deterministic_model(self):
        """Test with deterministic (constant) model"""
        params = {'x': {'distribution': 'normal', 'mean': 0, 'std': 1}}
        
        # Model that ignores parameters
        def constant_model(p):
            return 42.0
        
        simulator = MonteCarloSimulator(n_simulations=100, random_state=42)
        result = simulator.run(constant_model, params)
        
        assert result.mean == 42.0
        assert result.median == 42.0
        assert result.std == 0.0
    
    def test_reproducibility(self, simple_parameters, simple_model):
        """Test that same random_state gives same results"""
        simulator1 = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.SIMPLE_RANDOM,
            random_state=42
        )
        result1 = simulator1.run(simple_model, simple_parameters)
        
        simulator2 = MonteCarloSimulator(
            n_simulations=1000,
            sampling_method=SamplingMethod.SIMPLE_RANDOM,
            random_state=42
        )
        result2 = simulator2.run(simple_model, simple_parameters)
        
        # Results should be identical
        assert result1.mean == result2.mean
        assert result1.std == result2.std
        np.testing.assert_array_equal(result1.samples, result2.samples)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
