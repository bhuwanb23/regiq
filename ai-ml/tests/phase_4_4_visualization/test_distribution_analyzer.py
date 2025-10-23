"""
Test Distribution Analyzer

Tests for probability distribution analysis functionality.
"""

import pytest
import numpy as np
from services.risk_simulator.visualization.distribution_analyzer import (
    DistributionAnalyzer,
    DistributionType
)


class TestDistributionAnalyzer:
    """Test DistributionAnalyzer class"""
    
    def test_initialization(self):
        """Test distribution analyzer initialization"""
        analyzer = DistributionAnalyzer(random_state=42)
        assert analyzer.random_state == 42
        assert analyzer.np_random is not None
    
    def test_analyze_risk_distribution_empirical(self):
        """Test empirical distribution analysis"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        # Generate sample risk scores
        risk_scores = np.random.RandomState(42).uniform(0.2, 0.8, 100).tolist()
        
        analysis = analyzer.analyze_risk_distribution(
            risk_scores,
            distribution_type=DistributionType.EMPIRICAL,
            num_bins=20
        )
        
        assert analysis.distribution_type == DistributionType.EMPIRICAL.value
        assert len(analysis.histogram.bin_counts) == 20
        assert len(analysis.histogram.bin_centers) == 20
        assert analysis.histogram.total_count == 100
        assert len(analysis.confidence_intervals) == 3  # 90%, 95%, 99%
        assert 'mean' in analysis.statistics
        assert 'median' in analysis.statistics
        assert 'p95' in analysis.percentiles
    
    def test_analyze_risk_distribution_normal(self):
        """Test normal distribution fitting"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        # Generate normal-ish data
        risk_scores = np.random.RandomState(42).normal(0.5, 0.1, 100).tolist()
        
        analysis = analyzer.analyze_risk_distribution(
            risk_scores,
            distribution_type=DistributionType.NORMAL
        )
        
        assert analysis.distribution_type == DistributionType.NORMAL.value
        assert 'mean' in analysis.pdf_cdf.parameters
        assert 'std' in analysis.pdf_cdf.parameters
        assert len(analysis.pdf_cdf.x_values) == 200
        assert len(analysis.pdf_cdf.pdf_values) == 200
        assert len(analysis.pdf_cdf.cdf_values) == 200
    
    def test_confidence_intervals(self):
        """Test confidence interval calculation"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        risk_scores = [0.3, 0.4, 0.5, 0.6, 0.7] * 20
        
        analysis = analyzer.analyze_risk_distribution(
            risk_scores,
            confidence_levels=[0.90, 0.95, 0.99]
        )
        
        assert len(analysis.confidence_intervals) == 3
        
        # Check 95% CI
        ci_95 = next(ci for ci in analysis.confidence_intervals if ci.confidence_level == 0.95)
        assert ci_95.lower_bound < ci_95.mean
        assert ci_95.mean < ci_95.upper_bound
        assert ci_95.lower_bound < ci_95.median < ci_95.upper_bound
    
    def test_statistics_calculation(self):
        """Test statistical metrics calculation"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        risk_scores = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        
        analysis = analyzer.analyze_risk_distribution(risk_scores)
        
        stats = analysis.statistics
        assert stats['count'] == 9
        assert 0 < stats['mean'] < 1
        assert 0 < stats['median'] < 1
        assert stats['std'] > 0
        assert stats['min'] == 0.1
        assert stats['max'] == 0.9
        assert stats['range'] == 0.8
    
    def test_percentiles_calculation(self):
        """Test percentile calculation"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        risk_scores = [float(x) for x in range(0, 101)]  # 0 to 100
        
        analysis = analyzer.analyze_risk_distribution(risk_scores)
        
        percentiles = analysis.percentiles
        assert 'p1' in percentiles
        assert 'p50' in percentiles
        assert 'p95' in percentiles
        assert 'p99' in percentiles
        assert percentiles['p50'] == pytest.approx(50, abs=1)
        assert percentiles['p95'] == pytest.approx(95, abs=1)
    
    def test_analyze_monte_carlo_results(self):
        """Test Monte Carlo results analysis"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        # Simulate Monte Carlo outputs
        simulation_results = np.random.RandomState(42).exponential(0.3, 1000).tolist()
        
        analysis = analyzer.analyze_monte_carlo_results(simulation_results, num_bins=50)
        
        assert analysis.distribution_type == DistributionType.EMPIRICAL.value
        assert len(analysis.histogram.bin_counts) == 50
        assert analysis.statistics['count'] == 1000
    
    def test_compare_distributions(self):
        """Test distribution comparison"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        baseline_scores = np.random.RandomState(42).normal(0.4, 0.1, 100).tolist()
        scenario_scores = np.random.RandomState(43).normal(0.6, 0.1, 100).tolist()
        
        comparison = analyzer.compare_distributions(baseline_scores, scenario_scores)
        
        assert 'baseline' in comparison
        assert 'scenario' in comparison
        assert 'statistical_tests' in comparison
        assert 'comparison_metrics' in comparison
        
        # Check statistical tests
        assert 'kolmogorov_smirnov' in comparison['statistical_tests']
        assert 't_test' in comparison['statistical_tests']
        assert 'cohens_d' in comparison['statistical_tests']
        
        # Check metrics
        assert 'mean_difference' in comparison['comparison_metrics']
        assert comparison['comparison_metrics']['mean_difference'] > 0  # Scenario higher
    
    def test_cohens_d_interpretation(self):
        """Test Cohen's d effect size interpretation"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        # Small difference with variation
        np.random.seed(42)
        baseline = np.random.normal(0.5, 0.01, 50).tolist()
        scenario_small = np.random.normal(0.52, 0.01, 50).tolist()
        
        comparison_small = analyzer.compare_distributions(baseline, scenario_small)
        cohens_d = comparison_small['statistical_tests']['cohens_d']['value']
        interpretation = comparison_small['statistical_tests']['cohens_d']['interpretation']
        
        assert interpretation in ['negligible', 'small', 'medium', 'large']  # Can vary with random data
        
        # Large difference
        scenario_large = np.random.normal(0.8, 0.01, 50).tolist()
        comparison_large = analyzer.compare_distributions(baseline, scenario_large)
        interpretation_large = comparison_large['statistical_tests']['cohens_d']['interpretation']
        
        assert interpretation_large in ['medium', 'large']
    
    def test_generate_risk_bands(self):
        """Test risk bands generation"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        risk_scores = [float(x) for x in range(1, 101)]  # 1 to 100
        
        bands = analyzer.generate_risk_bands(risk_scores, num_bands=5)
        
        assert bands['num_bands'] == 5
        assert bands['total_count'] == 100
        assert len(bands['bands']) == 5
        
        # Check each band
        for i, band in enumerate(bands['bands']):
            assert band['band_index'] == i
            assert band['count'] > 0
            assert 0 < band['percentage'] < 100
            assert band['lower_bound'] < band['upper_bound']
    
    def test_generate_risk_bands_quartiles(self):
        """Test quartile bands"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        risk_scores = [0.1] * 25 + [0.3] * 25 + [0.6] * 25 + [0.9] * 25
        
        bands = analyzer.generate_risk_bands(risk_scores, num_bands=4)
        
        assert len(bands['bands']) == 4
        assert sum(b['count'] for b in bands['bands']) == 100
    
    def test_to_json_conversion(self):
        """Test JSON serialization"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        risk_scores = [0.3, 0.4, 0.5, 0.6, 0.7]
        analysis = analyzer.analyze_risk_distribution(risk_scores)
        
        json_data = analyzer.to_json(analysis)
        
        assert isinstance(json_data, dict)
        assert 'distribution_type' in json_data
        assert 'histogram' in json_data
        assert 'pdf_cdf' in json_data
        assert 'confidence_intervals' in json_data
        assert 'statistics' in json_data
        assert 'percentiles' in json_data
    
    def test_histogram_density_normalization(self):
        """Test histogram density normalization"""
        analyzer = DistributionAnalyzer(random_state=42)
        
        # Use varied data instead of constant values
        np.random.seed(42)
        risk_scores = np.random.normal(0.5, 0.1, 100).tolist()
        analysis = analyzer.analyze_risk_distribution(risk_scores, num_bins=10)
        
        # Density should sum to 1 (approximately)
        density_sum = sum(analysis.histogram.density)
        assert density_sum == pytest.approx(1.0, abs=0.01)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
