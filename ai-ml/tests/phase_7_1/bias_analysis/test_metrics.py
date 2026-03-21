#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Metrics Tests
Test suite for fairness metrics analyzers.

Tests:
    - Demographic Parity Analyzer
    - Equalized Odds Analyzer
    - Calibration Analyzer
    - Individual Fairness Analyzer

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import numpy as np
from typing import Dict, Any
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.bias_analysis.metrics import (
    DemographicParityAnalyzer,
    DemographicParityResult,
    ParityThreshold,
    EqualizedOddsAnalyzer,
    EqualizedOddsResult,
    EqualizedOddsThreshold,
    CalibrationAnalyzer,
    CalibrationResult,
    CalibrationThreshold,
    IndividualFairnessAnalyzer,
    IndividualFairnessResult,
    IndividualFairnessThreshold,
)


class TestDemographicParityAnalyzer(unittest.TestCase):
    """Test demographic parity metric calculation."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = DemographicParityAnalyzer()
        
        # Create sample dataset
        np.random.seed(42)
        n_samples = 1000
        
        # Protected attribute (0 = privileged, 1 = unprivileged)
        self.protected = np.random.binomial(1, 0.5, n_samples)
        
        # Predictions with slight bias
        self.y_pred = np.where(
            self.protected == 0,
            np.random.binomial(1, 0.7, n_samples),  # 70% approval for privileged
            np.random.binomial(1, 0.6, n_samples)   # 60% approval for unprivileged
        )
        
        # Ground truth
        self.y_true = np.random.binomial(1, 0.65, n_samples)

    def test_analyze_basic(self):
        """Test basic demographic parity analysis."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        self.assertIsInstance(result, DemographicParityResult)
        self.assertGreaterEqual(result.demographic_parity_ratio, 0.0)
        self.assertLessEqual(result.demographic_parity_ratio, 2.0)
        self.assertIn('statistical_parity_diff', result.metrics)

    def test_perfect_parity(self):
        """Test with perfectly balanced predictions."""
        # Create perfectly balanced predictions
        y_pred_balanced = np.concatenate([
            np.ones(500),  # 500 positive for privileged
            np.ones(500)   # 500 positive for unprivileged
        ])
        protected_balanced = np.concatenate([
            np.zeros(500),  # Privileged group
            np.ones(500)    # Unprivileged group
        ])
        
        result = self.analyzer.analyze(
            y_true=y_pred_balanced,
            y_pred=y_pred_balanced,
            protected_attribute=protected_balanced
        )
        
        # Should have perfect or near-perfect parity
        self.assertAlmostEqual(result.demographic_parity_ratio, 1.0, places=1)

    def test_threshold_check(self):
        """Test threshold compliance checking."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        # Check against 80% rule
        threshold = ParityThreshold.THRESHOLD_80_PERCENT
        is_compliant = result.is_compliant(threshold)
        
        self.assertIsInstance(is_compliant, bool)

    def test_invalid_input_length_mismatch(self):
        """Test error handling for mismatched input lengths."""
        with self.assertRaises(ValueError):
            self.analyzer.analyze(
                y_true=np.array([1, 0, 1]),
                y_pred=np.array([1, 0]),  # Wrong length
                protected_attribute=np.array([0, 1, 0])
            )

    def test_group_rates_calculation(self):
        """Test group-specific rate calculation."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        self.assertIn('privileged_rate', result.group_rates)
        self.assertIn('unprivileged_rate', result.group_rates)
        self.assertGreaterEqual(result.group_rates['privileged_rate'], 0.0)
        self.assertLessEqual(result.group_rates['unprivileged_rate'], 1.0)


class TestEqualizedOddsAnalyzer(unittest.TestCase):
    """Test equalized odds metric calculation."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EqualizedOddsAnalyzer()
        
        # Create sample dataset
        np.random.seed(42)
        n_samples = 1000
        
        self.protected = np.random.binomial(1, 0.5, n_samples)
        self.y_true = np.random.binomial(1, 0.6, n_samples)
        
        # Predictions with some correlation to ground truth
        self.y_pred = np.where(
            np.random.random(n_samples) < 0.7,
            self.y_true,
            1 - self.y_true
        )

    def test_analyze_basic(self):
        """Test basic equalized odds analysis."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        self.assertIsInstance(result, EqualizedOddsResult)
        self.assertIn('true_positive_rate_privileged', result.tpr_by_group)
        self.assertIn('true_positive_rate_unprivileged', result.tpr_by_group)
        self.assertIn('false_positive_rate_privileged', result.fpr_by_group)
        self.assertIn('false_positive_rate_unprivileged', result.fpr_by_group)

    def test_tpr_difference(self):
        """Test true positive rate difference calculation."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        tpr_diff = abs(
            result.tpr_by_group['true_positive_rate_privileged'] -
            result.tpr_by_group['true_positive_rate_unprivileged']
        )
        
        self.assertGreaterEqual(tpr_diff, 0.0)
        self.assertLessEqual(tpr_diff, 1.0)

    def test_fpr_difference(self):
        """Test false positive rate difference calculation."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        fpr_diff = abs(
            result.fpr_by_group['false_positive_rate_privileged'] -
            result.fpr_by_group['false_positive_rate_unprivileged']
        )
        
        self.assertGreaterEqual(fpr_diff, 0.0)
        self.assertLessEqual(fpr_diff, 1.0)

    def test_threshold_check(self):
        """Test threshold compliance checking."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        threshold = EqualizedOddsThreshold.THRESHOLD_80_PERCENT
        is_compliant = result.is_compliant(threshold)
        
        self.assertIsInstance(is_compliant, bool)


class TestCalibrationAnalyzer(unittest.TestCase):
    """Test calibration metric calculation."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CalibrationAnalyzer()
        
        # Create sample dataset
        np.random.seed(42)
        n_samples = 1000
        
        # Probabilistic predictions
        self.y_prob = np.random.beta(2, 2, n_samples)  # Values between 0 and 1
        self.y_true = np.random.binomial(1, self.y_prob)
        self.protected = np.random.binomial(1, 0.5, n_samples)

    def test_calibration_basic(self):
        """Test basic calibration analysis."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_prob=self.y_prob,
            protected_attribute=self.protected
        )
        
        self.assertIsInstance(result, CalibrationResult)
        self.assertIn('calibration_error', result.metrics)
        self.assertIn('calibration_slope', result.metrics)

    def test_perfect_calibration(self):
        """Test with perfectly calibrated predictions."""
        # Create perfectly calibrated predictions
        np.random.seed(42)
        n_samples = 1000
        y_prob = np.random.uniform(0, 1, n_samples)
        y_true = np.random.binomial(1, y_prob)
        
        result = self.analyzer.analyze(
            y_true=y_true,
            y_prob=y_prob,
            protected_attribute=np.random.binomial(1, 0.5, n_samples)
        )
        
        # Calibration error should be low
        self.assertLess(result.metrics['calibration_error'], 0.1)

    def test_calibration_by_group(self):
        """Test calibration breakdown by protected group."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_prob=self.y_prob,
            protected_attribute=self.protected
        )
        
        self.assertIn('calibration_by_group', result.calibration_breakdown)
        self.assertIn('privileged', result.calibration_breakdown['calibration_by_group'])
        self.assertIn('unprivileged', result.calibration_breakdown['calibration_by_group'])

    def test_reliability_diagram_data(self):
        """Test reliability diagram data generation."""
        result = self.analyzer.analyze(
            y_true=self.y_true,
            y_prob=self.y_prob,
            protected_attribute=self.protected
        )
        
        self.assertIn('fraction_of_positives', result.reliability_diagram)
        self.assertIn('mean_predicted_values', result.reliability_diagram)
        self.assertEqual(
            len(result.reliability_diagram['fraction_of_positives']),
            len(result.reliability_diagram['mean_predicted_values'])
        )


class TestIndividualFairnessAnalyzer(unittest.TestCase):
    """Test individual fairness metric calculation."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = IndividualFairnessAnalyzer()
        
        # Create sample dataset
        np.random.seed(42)
        n_samples = 100
        
        # Features for similarity calculation
        self.X = np.random.randn(n_samples, 5)
        self.y_pred = np.random.binomial(1, 0.6, n_samples)
        self.protected = np.random.binomial(1, 0.5, n_samples)

    def test_individual_fairness_basic(self):
        """Test basic individual fairness analysis."""
        result = self.analyzer.analyze(
            X=self.X,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        self.assertIsInstance(result, IndividualFairnessResult)
        self.assertIn('individual_fairness_score', result.metrics)
        self.assertIn('average_treatment_effect', result.metrics)

    def test_similarity_matrix(self):
        """Test similarity matrix calculation."""
        result = self.analyzer.analyze(
            X=self.X,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        # Should compute pairwise similarities
        self.assertIn('similarity_matrix', result.details)
        sim_matrix = result.details['similarity_matrix']
        self.assertEqual(sim_matrix.shape, (len(self.X), len(self.X)))

    def test_concordance_discordance(self):
        """Test concordance/discordance pair analysis."""
        result = self.analyzer.analyze(
            X=self.X,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        self.assertIn('concordant_pairs', result.pairwise_analysis)
        self.assertIn('discordant_pairs', result.pairwise_analysis)
        
        concordant = result.pairwise_analysis['concordant_pairs']
        discordant = result.pairwise_analysis['discordant_pairs']
        
        self.assertGreaterEqual(concordant, 0)
        self.assertGreaterEqual(discordant, 0)

    def test_threshold_check(self):
        """Test threshold compliance checking."""
        result = self.analyzer.analyze(
            X=self.X,
            y_pred=self.y_pred,
            protected_attribute=self.protected
        )
        
        threshold = IndividualFairnessThreshold.THRESHOLD_DEFAULT
        is_compliant = result.is_compliant(threshold)
        
        self.assertIsInstance(is_compliant, bool)


def run_tests():
    """Run all metric tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDemographicParityAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestEqualizedOddsAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestCalibrationAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIndividualFairnessAnalyzer))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
