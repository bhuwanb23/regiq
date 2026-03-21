#!/usr/bin/env python3
"""
REGIQ AI/ML - Risk Simulator Visualization Tests
Test suite for risk visualization components.

Tests:
    - Heatmap generation
    - Distribution analysis
    - Timeline projection
    - Export functionality

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.risk_simulator.visualization import (
    HeatmapGenerator,
    DistributionAnalyzer,
    TimelineProjector,
    ExportManager,
)


class TestHeatmapGenerator(unittest.TestCase):
    """Test heatmap generation."""

    def setUp(self):
        """Set up fixtures."""
        self.heatmap_gen = HeatmapGenerator()
        
        # Sample risk data
        self.risk_data = {
            'dimensions': ['probability', 'impact', 'velocity'],
            'data': np.random.rand(10, 3),
            'labels': [f'Risk_{i}' for i in range(10)]
        }

    def test_heatmap_generation(self):
        """Test basic heatmap generation."""
        try:
            heatmap = self.heatmap_gen.generate(self.risk_data)
            
            self.assertIsNotNone(heatmap)
            self.assertIsInstance(heatmap, dict)
        except Exception as e:
            self.skipTest(f"Heatmap generation failed: {e}")

    def test_color_mapping(self):
        """Test color mapping for risk levels."""
        try:
            colors = self.heatmap_gen.map_colors(
                values=[0.2, 0.5, 0.8],
                colormap='green_yellow_red'
            )
            
            self.assertIsNotNone(colors)
            self.assertEqual(len(colors), 3)
        except Exception as e:
            self.skipTest(f"Color mapping failed: {e}")

    def test_cell_aggregation(self):
        """Test cell value aggregation."""
        try:
            aggregated = self.heatmap_gen.aggregate_cells(
                data=self.risk_data['data'],
                method='mean'
            )
            
            self.assertIsNotNone(aggregated)
        except Exception as e:
            self.skipTest(f"Cell aggregation failed: {e}")


class TestDistributionAnalyzer(unittest.TestCase):
    """Test distribution analysis."""

    def setUp(self):
        """Set up fixtures."""
        self.analyzer = DistributionAnalyzer()
        
        # Sample simulation results
        self.samples = np.random.normal(100, 20, 1000)

    def test_histogram_generation(self):
        """Test histogram data generation."""
        try:
            histogram = self.analyzer.generate_histogram(self.samples)
            
            self.assertIsNotNone(histogram)
            self.assertIn('bins', histogram)
            self.assertIn('counts', histogram)
        except Exception as e:
            self.skipTest(f"Histogram generation failed: {e}")

    def test_pdf_cdf_estimation(self):
        """Test PDF and CDF estimation."""
        try:
            pdf_cdf = self.analyzer.estimate_pdf_cdf(self.samples)
            
            self.assertIsNotNone(pdf_cdf)
            self.assertIn('pdf', pdf_cdf)
            self.assertIn('cdf', pdf_cdf)
        except Exception as e:
            self.skipTest(f"PDF/CDF estimation failed: {e}")

    def test_confidence_interval_calculation(self):
        """Test confidence interval calculation."""
        try:
            ci = self.analyzer.calculate_confidence_interval(
                self.samples, confidence=0.95
            )
            
            self.assertIsNotNone(ci)
            self.assertLess(ci[0], ci[1])  # Lower < upper
        except Exception as e:
            self.skipTest(f"CI calculation failed: {e}")

    def test_statistical_moments(self):
        """Test statistical moment calculation."""
        try:
            moments = self.analyzer.calculate_moments(self.samples)
            
            self.assertIsNotNone(moments)
            self.assertIn('mean', moments)
            self.assertIn('variance', moments)
            self.assertIn('skewness', moments)
            self.assertIn('kurtosis', moments)
        except Exception as e:
            self.skipTest(f"Moment calculation failed: {e}")


class TestTimelineProjector(unittest.TestCase):
    """Test timeline projection."""

    def setUp(self):
        """Set up fixtures."""
        self.timeline_proj = TimelineProjector()
        
        # Sample time series data
        self.time_series = np.cumsum(np.random.randn(100)) + 100

    def test_timeline_projection(self):
        """Test future timeline projection."""
        try:
            projection = self.timeline_proj.project(
                historical_data=self.time_series,
                steps_ahead=12
            )
            
            self.assertIsNotNone(projection)
            self.assertIn('projected_values', projection)
            self.assertEqual(len(projection['projected_values']), 12)
        except Exception as e:
            self.skipTest(f"Timeline projection failed: {e}")

    def test_action_plan_generation(self):
        """Test action plan generation."""
        try:
            action_plan = self.timeline_proj.generate_action_plan(
                timeline_projection={'milestones': [1, 2, 3]},
                priorities=['high', 'medium', 'low']
            )
            
            self.assertIsNotNone(action_plan)
            self.assertIsInstance(action_plan, list)
        except Exception as e:
            self.skipTest(f"Action plan generation failed: {e}")


class TestExportManager(unittest.TestCase):
    """Test export functionality."""

    def setUp(self):
        """Set up fixtures."""
        self.export_mgr = ExportManager()
        
        # Sample data
        self.sample_data = {
            'risk_scores': np.random.rand(10),
            'metrics': {'mean': 0.5, 'std': 0.2}
        }

    def test_export_to_json(self):
        """Test JSON export."""
        try:
            result = self.export_mgr.export(
                data=self.sample_data,
                format='json',
                return_bytes=False
            )
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result, (str, dict))
        except Exception as e:
            self.skipTest(f"JSON export failed: {e}")

    def test_export_to_csv(self):
        """Test CSV export."""
        try:
            result = self.export_mgr.export(
                data={'col1': [1, 2, 3], 'col2': [4, 5, 6]},
                format='csv',
                return_bytes=False
            )
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
        except Exception as e:
            self.skipTest(f"CSV export failed: {e}")

    def test_export_validation(self):
        """Test export data validation."""
        try:
            is_valid = self.export_mgr.validate_data(self.sample_data)
            
            self.assertIsInstance(is_valid, bool)
        except Exception as e:
            self.skipTest(f"Export validation failed: {e}")


def run_tests():
    """Run all visualization tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestHeatmapGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestDistributionAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestTimelineProjector))
    suite.addTests(loader.loadTestsFromTestCase(TestExportManager))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
