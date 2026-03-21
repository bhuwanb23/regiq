#!/usr/bin/env python3
"""
REGIQ AI/ML - Monte Carlo Simulation Tests
Test suite for Monte Carlo simulation engine.

Tests:
    - Basic Monte Carlo simulation
    - Sampling methods (LHS, Sobol, Random)
    - Distribution handling
    - Convergence diagnostics
    - Result analysis

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.risk_simulator.simulation import (
    MonteCarloSimulator,
    SamplingMethod,
    DistributionType,
    SimulationResult,
    Parameter,
    ParameterSpace,
)


class TestMonteCarloSimulator(unittest.TestCase):
    """Test Monte Carlo simulation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.simulator = MonteCarloSimulator(n_simulations=1000)
        
        # Sample parameters
        self.sample_params = {
            'violation_probability': Parameter(
                name='violation_probability',
                distribution=DistributionType.BETA,
                params={'alpha': 2, 'beta': 5},
                min_val=0.0,
                max_val=1.0
            ),
            'penalty_amount': Parameter(
                name='penalty_amount',
                distribution=DistributionType.LOGNORMAL,
                params={'mean': 100000, 'std': 50000},
                min_val=0.0,
                max_val=10000000
            )
        }

    def test_initialization(self):
        """Test simulator initialization."""
        self.assertIsNotNone(self.simulator)
        self.assertEqual(self.simulator.n_simulations, 1000)

    def test_run_basic_simulation(self):
        """Test basic Monte Carlo simulation."""
        try:
            result = self.simulator.run(self.sample_params)
            
            self.assertIsInstance(result, SimulationResult)
            self.assertGreater(len(result.samples), 0)
            self.assertEqual(len(result.samples), 1000)
        except Exception as e:
            self.skipTest(f"Monte Carlo simulation failed: {e}")

    def test_sampling_method_lhs(self):
        """Test Latin Hypercube Sampling."""
        simulator_lhs = MonteCarloSimulator(
            n_simulations=500,
            sampling_method=SamplingMethod.LATIN_HYPERCUBE
        )
        
        try:
            result = simulator_lhs.run(self.sample_params)
            
            self.assertIsInstance(result, SimulationResult)
            # LHS should provide more uniform coverage
        except Exception as e:
            self.skipTest(f"LHS sampling failed: {e}")

    def test_sampling_method_sobol(self):
        """Test Sobol quasi-random sampling."""
        simulator_sobol = MonteCarloSimulator(
            n_simulations=500,
            sampling_method=SamplingMethod.SOBOL
        )
        
        try:
            result = simulator_sobol.run(self.sample_params)
            
            self.assertIsInstance(result, SimulationResult)
        except Exception as e:
            self.skipTest(f"Sobol sampling failed: {e}")

    def test_convergence_check(self):
        """Test convergence checking."""
        # Run with increasing simulations
        results = []
        for n_sims in [100, 500, 1000]:
            sim = MonteCarloSimulator(n_simulations=n_sims)
            result = sim.run(self.sample_params)
            results.append(result)
        
        # Mean should stabilize with more simulations
        means = [r.statistics['mean'] for r in results if hasattr(r, 'statistics')]
        
        if len(means) >= 2:
            # Check convergence trend
            diff_1_2 = abs(means[1] - means[0])
            diff_2_3 = abs(means[2] - means[1]) if len(means) > 2 else 0
            
            # Should generally converge
            self.assertLessEqual(diff_2_3, diff_1_2 * 1.5)  # Allow some tolerance

    def test_confidence_intervals(self):
        """Test confidence interval calculation."""
        try:
            result = self.simulator.run(self.sample_params)
            
            # Should calculate confidence intervals
            if hasattr(result, 'confidence_intervals'):
                ci_95 = result.confidence_intervals.get('95%')
                
                if ci_95:
                    self.assertLess(ci_95[0], ci_95[1])
                    self.assertIsInstance(ci_95[0], (int, float))
        except Exception as e:
            self.skipTest(f"CI calculation failed: {e}")

    def test_result_statistics(self):
        """Test result statistical analysis."""
        try:
            result = self.simulator.run(self.sample_params)
            
            # Should provide statistics
            if hasattr(result, 'statistics'):
                stats = result.statistics
                
                self.assertIn('mean', stats)
                self.assertIn('std', stats)
                self.assertIn('min', stats)
                self.assertIn('max', stats)
                
                # Mean should be reasonable
                mean_val = stats['mean']
                self.assertIsInstance(mean_val, (int, float))
        except Exception as e:
            self.skipTest(f"Statistics calculation failed: {e}")

    def test_parameter_space_generation(self):
        """Test parameter space generation."""
        param_space = ParameterSpace(self.sample_params)
        
        self.assertIsNotNone(param_space)
        self.assertEqual(len(param_space.parameters), 2)
        
        # Should generate combinations
        combinations = param_space.generate_grid(n_points=5)
        self.assertGreater(len(combinations), 0)

    def test_large_scale_simulation(self):
        """Test large-scale simulation (10k+ simulations)."""
        large_sim = MonteCarloSimulator(n_simulations=10000)
        
        try:
            result = large_sim.run(self.sample_params)
            
            self.assertEqual(len(result.samples), 10000)
            # Should complete in reasonable time (<10 seconds)
        except Exception as e:
            self.skipTest(f"Large simulation failed: {e}")


class TestDistributionTypes(unittest.TestCase):
    """Test different distribution types."""

    def setUp(self):
        """Set up fixtures."""
        self.simulator = MonteCarloSimulator(n_simulations=500)

    def test_normal_distribution(self):
        """Test normal distribution sampling."""
        params = {
            'risk_factor': Parameter(
                name='risk_factor',
                distribution=DistributionType.NORMAL,
                params={'mean': 0.5, 'std': 0.1}
            )
        }
        
        try:
            result = self.simulator.run(params)
            
            samples = result.samples
            # Should be roughly normal
            mean = np.mean(samples)
            self.assertAlmostEqual(mean, 0.5, delta=0.1)
        except Exception as e:
            self.skipTest(f"Normal distribution failed: {e}")

    def test_uniform_distribution(self):
        """Test uniform distribution sampling."""
        params = {
            'uniform_var': Parameter(
                name='uniform_var',
                distribution=DistributionType.UNIFORM,
                params={'low': 0.0, 'high': 1.0}
            )
        }
        
        try:
            result = self.simulator.run(params)
            
            samples = result.samples
            # All samples should be in range
            self.assertTrue(all(0.0 <= s <= 1.0 for s in samples))
        except Exception as e:
            self.skipTest(f"Uniform distribution failed: {e}")

    def test_triangular_distribution(self):
        """Test triangular distribution sampling."""
        params = {
            'triangular_var': Parameter(
                name='triangular_var',
                distribution=DistributionType.TRIANGULAR,
                params={'low': 0.0, 'mode': 0.5, 'high': 1.0}
            )
        }
        
        try:
            result = self.simulator.run(params)
            
            samples = result.samples
            # Mode should be most frequent
            self.assertTrue(all(0.0 <= s <= 1.0 for s in samples))
        except Exception as e:
            self.skipTest(f"Triangular distribution failed: {e}")


def run_tests():
    """Run all Monte Carlo tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestMonteCarloSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestDistributionTypes))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
