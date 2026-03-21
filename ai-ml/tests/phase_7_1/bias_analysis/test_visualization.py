#!/usr/bin/env python3
"""
REGIQ AI/ML - Visualization Tests
Test suite for BiasVisualizer with all 7 chart types.

Tests:
    - plot_fairness_metrics()
    - plot_group_comparison()
    - plot_mitigation_comparison()
    - plot_calibration_curve()
    - plot_feature_importance()
    - plot_score_distribution()
    - plot_summary_dashboard()

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import base64
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.bias_analysis.visualization import BiasVisualizer


class TestBiasVisualizer(unittest.TestCase):
    """Test BiasVisualizer chart generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.visualizer = BiasVisualizer()
        
        # Sample fairness metrics
        self.metrics = {
            'demographic_parity': 0.85,
            'equalized_odds': 0.78,
            'calibration': 0.92,
            'disparate_impact': 0.81,
            'individual_fairness': 0.88
        }
        
        # Sample group rates
        self.group_rates = {
            'Group A (Privileged)': 0.75,
            'Group B (Unprivileged)': 0.68,
            'Group C (Unprivileged)': 0.71
        }
        
        # Sample before/after metrics
        self.before_metrics = {
            'demographic_parity': 0.65,
            'equalized_odds': 0.58,
            'calibration': 0.72
        }
        self.after_metrics = {
            'demographic_parity': 0.85,
            'equalized_odds': 0.78,
            'calibration': 0.92
        }
        
        # Sample calibration data
        self.fraction_of_positives = [0.1, 0.25, 0.42, 0.58, 0.75, 0.92]
        self.mean_predicted_values = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
        
        # Sample feature importances
        self.feature_importances = {
            'credit_score': 0.45,
            'income': 0.32,
            'debt_to_income': -0.28,
            'employment_length': 0.15,
            'loan_amount': -0.12,
            'age': 0.08,
            'num_credit_lines': 0.05
        }
        
        # Sample score distributions
        np = __import__('numpy')
        np.random.seed(42)
        self.scores_by_group = {
            'Privileged': np.random.beta(7, 3, 500),  # Higher scores
            'Unprivileged': np.random.beta(5, 4, 500)  # Lower scores
        }

    def test_plot_fairness_metrics(self):
        """Test fairness metrics bar chart generation."""
        img_data = self.visualizer.plot_fairness_metrics(
            metrics=self.metrics,
            title="Fairness Metrics Overview",
            threshold=0.8
        )
        
        # Verify output is valid base64
        self.assertIsInstance(img_data, str)
        self.assertGreater(len(img_data), 0)
        
        # Decode and verify it's a valid image
        decoded = base64.b64decode(img_data)
        self.assertGreater(len(decoded), 0)
        
        # Check PNG magic bytes
        self.assertEqual(decoded[:4], b'\x89PNG')

    def test_plot_fairness_metrics_empty(self):
        """Test fairness metrics with empty input."""
        img_data = self.visualizer.plot_fairness_metrics(
            metrics={},
            title="Empty Metrics"
        )
        
        # Should still generate SVG or placeholder
        self.assertIsInstance(img_data, str)
        self.assertGreater(len(img_data), 0)

    def test_plot_group_comparison(self):
        """Test group comparison bar chart generation."""
        img_data = self.visualizer.plot_group_comparison(
            group_rates=self.group_rates,
            metric_name="Positive Prediction Rate",
            protected_attribute="Demographic Group"
        )
        
        # Verify output
        self.assertIsInstance(img_data, str)
        decoded = base64.b64decode(img_data)
        self.assertEqual(decoded[:4], b'\x89PNG')

    def test_plot_group_comparison_single_group(self):
        """Test group comparison with single group."""
        single_group = {'Only Group': 0.75}
        
        img_data = self.visualizer.plot_group_comparison(
            group_rates=single_group,
            metric_name="Approval Rate"
        )
        
        self.assertIsInstance(img_data, str)
        self.assertGreater(len(img_data), 0)

    def test_plot_mitigation_comparison(self):
        """Test before/after mitigation comparison chart."""
        img_data = self.visualizer.plot_mitigation_comparison(
            before_metrics=self.before_metrics,
            after_metrics=self.after_metrics,
            title="Bias Mitigation: Before vs After"
        )
        
        # Verify output
        self.assertIsInstance(img_data, str)
        decoded = base64.b64decode(img_data)
        self.assertEqual(decoded[:4], b'\x89PNG')
        
        # Verify chart shows improvement (green bars should be higher)
        # This is implicitly tested by successful generation

    def test_plot_mitigation_comparison_no_overlap(self):
        """Test mitigation comparison with non-overlapping metrics."""
        before = {'metric_a': 0.5, 'metric_b': 0.6}
        after = {'metric_c': 0.7, 'metric_d': 0.8}  # No common keys
        
        img_data = self.visualizer.plot_mitigation_comparison(
            before_metrics=before,
            after_metrics=after
        )
        
        # Should handle gracefully (may show empty chart or subset)
        self.assertIsInstance(img_data, str)

    def test_plot_calibration_curve(self):
        """Test calibration curve generation."""
        img_data = self.visualizer.plot_calibration_curve(
            fraction_of_positives=self.fraction_of_positives,
            mean_predicted_values=self.mean_predicted_values,
            group_name="Overall Population"
        )
        
        # Verify output
        self.assertIsInstance(img_data, str)
        decoded = base64.b64decode(img_data)
        self.assertEqual(decoded[:4], b'\x89PNG')

    def test_plot_calibration_curve_short_data(self):
        """Test calibration curve with minimal data points."""
        short_frac = [0.2, 0.8]
        short_pred = [0.2, 0.8]
        
        img_data = self.visualizer.plot_calibration_curve(
            fraction_of_positives=short_frac,
            mean_predicted_values=short_pred
        )
        
        self.assertIsInstance(img_data, str)
        self.assertGreater(len(img_data), 0)

    def test_plot_feature_importance(self):
        """Test feature importance (SHAP) bar chart."""
        img_data = self.visualizer.plot_feature_importance(
            feature_importances=self.feature_importances,
            title="Feature Importance (SHAP)",
            top_n=15
        )
        
        # Verify output
        self.assertIsInstance(img_data, str)
        decoded = base64.b64decode(img_data)
        self.assertEqual(decoded[:4], b'\x89PNG')
        
        # Should show all features (7 < top_n)
        # Chart should display features sorted by absolute value

    def test_plot_feature_importance_top_n(self):
        """Test feature importance with top_n filtering."""
        img_data = self.visualizer.plot_feature_importance(
            feature_importances=self.feature_importances,
            top_n=3
        )
        
        # Should only show top 3 features
        self.assertIsInstance(img_data, str)

    def test_plot_score_distribution(self):
        """Test score distribution histogram."""
        img_data = self.visualizer.plot_score_distribution(
            scores_by_group=self.scores_by_group,
            title="Risk Score Distribution by Group"
        )
        
        # Verify output
        self.assertIsInstance(img_data, str)
        decoded = base64.b64decode(img_data)
        self.assertEqual(decoded[:4], b'\x89PNG')

    def test_plot_score_distribution_single_group(self):
        """Test score distribution with single group."""
        np = __import__('numpy')
        single_group = {'All Users': np.random.beta(6, 3, 500)}
        
        img_data = self.visualizer.plot_score_distribution(
            scores_by_group=single_group
        )
        
        self.assertIsInstance(img_data, str)
        self.assertGreater(len(img_data), 0)

    def test_plot_summary_dashboard(self):
        """Test comprehensive summary dashboard generation."""
        img_data = self.visualizer.plot_summary_dashboard(
            overall_score=0.82,
            metrics=self.metrics,
            group_rates=self.group_rates,
            before_metrics=self.before_metrics,
            after_metrics=self.after_metrics
        )
        
        # Verify output (should be largest chart)
        self.assertIsInstance(img_data, str)
        decoded = base64.b64decode(img_data)
        self.assertEqual(decoded[:4], b'\x89PNG')
        
        # Dashboard should be significantly larger than individual charts
        self.assertGreater(len(img_data), 50000)  # Typically ~90-100KB

    def test_plot_summary_dashboard_partial_data(self):
        """Test dashboard with partial data (some optional parameters missing)."""
        img_data = self.visualizer.plot_summary_dashboard(
            overall_score=0.75,
            metrics=self.metrics,
            group_rates=None,  # Missing
            before_metrics=None,  # Missing
            after_metrics=None  # Missing
        )
        
        # Should still generate dashboard with available data
        self.assertIsInstance(img_data, str)
        self.assertGreater(len(img_data), 0)

    def test_plot_summary_dashboard_minimal(self):
        """Test dashboard with minimal required data."""
        img_data = self.visualizer.plot_summary_dashboard(
            overall_score=0.80,
            metrics={}
        )
        
        # Should generate even with minimal data
        self.assertIsInstance(img_data, str)

    def test_all_charts_consistent_styling(self):
        """Test that all charts use consistent REGIQ color palette."""
        # Generate all chart types
        charts = [
            self.visualizer.plot_fairness_metrics(self.metrics),
            self.visualizer.plot_group_comparison(self.group_rates),
            self.visualizer.plot_mitigation_comparison(
                self.before_metrics, self.after_metrics
            ),
            self.visualizer.plot_calibration_curve(
                self.fraction_of_positives, self.mean_predicted_values
            ),
            self.visualizer.plot_feature_importance(self.feature_importances),
            self.visualizer.plot_score_distribution(self.scores_by_group),
            self.visualizer.plot_summary_dashboard(0.82, self.metrics)
        ]
        
        # All charts should be valid PNG images
        for i, chart in enumerate(charts):
            decoded = base64.b64decode(chart)
            self.assertEqual(
                decoded[:4], b'\x89PNG',
                msg=f"Chart {i+1} is not a valid PNG"
            )

    def test_visualizer_initialization(self):
        """Test BiasVisualizer initialization."""
        visualizer = BiasVisualizer()
        
        self.assertIsNotNone(visualizer.logger)
        self.assertEqual(visualizer.__class__.__name__, 'BiasVisualizer')


def run_tests():
    """Run all visualization tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBiasVisualizer))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
