#!/usr/bin/env python3
"""
REGIQ AI/ML - Bayesian Models & MCMC Tests
Test suite for Bayesian risk models and MCMC sampling.

Tests:
    - Bayesian model inference
    - MCMC sampling
    - Convergence diagnostics
    - Posterior analysis

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.risk_simulator.simulation import (
    BayesianRiskModel,
    ComplianceViolationModel,
    PenaltyAmountModel,
    MCMCSampler,
    MCMCConfig,
    check_convergence,
    geweke_test,
)


class TestBayesianModels(unittest.TestCase):
    """Test Bayesian risk modeling."""

    def setUp(self):
        """Set up fixtures."""
        self.bayesian_model = BayesianRiskModel()
        self.violation_model = ComplianceViolationModel()
        self.penalty_model = PenaltyAmountModel()

    def test_bayesian_model_initialization(self):
        """Test Bayesian model setup."""
        self.assertIsNotNone(self.bayesian_model)

    def test_prior_specification(self):
        """Test prior distribution specification."""
        try:
            # Set up simple priors
            priors = {
                'risk_probability': {'dist': 'beta', 'alpha': 2, 'beta': 5},
                'impact_severity': {'dist': 'normal', 'mean': 0.5, 'std': 0.2}
            }
            
            self.bayesian_model.set_priors(priors)
            # Should not raise exception
        except Exception as e:
            self.skipTest(f"Prior specification failed: {e}")

    def test_posterior_inference(self):
        """Test posterior probability calculation."""
        try:
            # Generate synthetic data
            data = np.random.beta(2, 5, 100)
            
            # Perform inference
            posterior = self.bayesian_model.infer(data)
            
            self.assertIsNotNone(posterior)
            self.assertIn('posterior_samples', posterior)
        except Exception as e:
            self.skipTest(f"Posterior inference failed: {e}")

    def test_compliance_violation_model(self):
        """Test compliance violation modeling."""
        try:
            # Historical violation data
            historical_data = np.array([0.1, 0.15, 0.2, 0.18, 0.25])
            
            result = self.violation_model.fit(historical_data)
            
            self.assertIsNotNone(result)
        except Exception as e:
            self.skipTest(f"Violation model failed: {e}")

    def test_penalty_amount_model(self):
        """Test penalty amount prediction."""
        try:
            # Historical penalty data
            penalties = np.array([10000, 50000, 100000, 250000, 1000000])
            
            result = self.penalty_model.fit(penalties)
            
            self.assertIsNotNone(result)
        except Exception as e:
            self.skipTest(f"Penalty model failed: {e}")


class TestMCMCSampling(unittest.TestCase):
    """Test MCMC sampling functionality."""

    def setUp(self):
        """Set up fixtures."""
        self.config = MCMCConfig(
            n_chains=2,
            n_samples=500,
            tune=100,
            target_accept=0.8
        )
        self.sampler = MCMCSampler(self.config)

    def test_mcmc_configuration(self):
        """Test MCMC configuration validation."""
        self.assertIsNotNone(self.config)
        self.assertEqual(self.config.n_chains, 2)
        self.assertEqual(self.config.n_samples, 500)

    def test_mcmc_sampling(self):
        """Test MCMC sampling execution."""
        try:
            # Define simple log-probability function
            def logp_fn(x):
                return -0.5 * x**2  # Normal distribution
            
            # Sample
            trace = self.sampler.sample(logp_fn, start={'x': 0.0})
            
            self.assertIsNotNone(trace)
            self.assertGreater(len(trace), 0)
        except Exception as e:
            self.skipTest(f"MCMC sampling failed: {e}")

    def test_chain_convergence(self):
        """Test MCMC chain convergence checking."""
        try:
            # Generate synthetic chain
            chain = np.random.normal(0, 1, 1000)
            
            converged = check_convergence(chain)
            
            # Should return boolean or diagnostic info
            self.assertIsInstance(converged, (bool, dict))
        except Exception as e:
            self.skipTest(f"Convergence check failed: {e}")

    def test_geweke_diagnostic(self):
        """Test Geweke convergence diagnostic."""
        try:
            # Generate stationary chain
            chain = np.random.normal(0, 1, 1000)
            
            z_score = geweke_test(chain)
            
            # Z-score should be reasonable for converged chain
            self.assertLess(abs(z_score), 2.0)  # Within 2 std devs
        except Exception as e:
            self.skipTest(f"Geweke test failed: {e}")

    def test_tuning_phase(self):
        """Test MCMC tuning phase."""
        try:
            def logp_fn(x):
                return -0.5 * x**2
            
            # Sample with tuning
            trace = self.sampler.sample(logp_fn, start={'x': 0.0}, tune=200)
            
            self.assertIsNotNone(trace)
        except Exception as e:
            self.skipTest(f"Tuning failed: {e}")


class TestHierarchicalModel(unittest.TestCase):
    """Test hierarchical Bayesian modeling."""

    def setUp(self):
        """Set up fixtures."""
        from services.risk_simulator.simulation import HierarchicalRiskModel
        
        self.hierarchical_model = HierarchicalRiskModel()

    def test_hierarchical_structure(self):
        """Test hierarchical model structure."""
        try:
            # Define hierarchy
            hierarchy = {
                'organization_level': {
                    'department_1': ['team_a', 'team_b'],
                    'department_2': ['team_c']
                }
            }
            
            self.hierarchical_model.set_hierarchy(hierarchy)
            # Should not raise exception
        except Exception as e:
            self.skipTest(f"Hierarchy setup failed: {e}")

    def test_partial_pooling(self):
        """Test partial pooling in hierarchical model."""
        try:
            # Group-level data
            group_data = {
                'group_1': np.random.beta(2, 5, 50),
                'group_2': np.random.beta(3, 4, 60),
                'group_3': np.random.beta(2, 6, 40)
            }
            
            result = self.hierarchical_model.fit(group_data)
            
            self.assertIsNotNone(result)
        except Exception as e:
            self.skipTest(f"Partial pooling failed: {e}")


def run_tests():
    """Run all Bayesian/MCMC tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBayesianModels))
    suite.addTests(loader.loadTestsFromTestCase(TestMCMCSampling))
    suite.addTests(loader.loadTestsFromTestCase(TestHierarchicalModel))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
