"""
Probability Distribution Data Analyzer

Generates structured data for probability distributions including histograms,
PDF/CDF curves, confidence intervals, and statistical summaries. Pure backend
data generation for frontend visualization.

Author: REGIQ AI/ML Team
Phase: 4.4 - Visualization & Reporting
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import numpy as np
from scipy import stats
from datetime import datetime


class DistributionType(Enum):
    """Probability distribution types"""
    NORMAL = "normal"
    LOGNORMAL = "lognormal"
    BETA = "beta"
    GAMMA = "gamma"
    EXPONENTIAL = "exponential"
    UNIFORM = "uniform"
    EMPIRICAL = "empirical"


@dataclass
class HistogramData:
    """Histogram data structure"""
    bin_edges: List[float]
    bin_counts: List[int]
    bin_centers: List[float]
    bin_widths: List[float]
    total_count: int
    density: List[float]  # Normalized to sum=1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PDFCDFData:
    """Probability Density Function and Cumulative Distribution Function data"""
    x_values: List[float]
    pdf_values: List[float]
    cdf_values: List[float]
    distribution_type: str
    parameters: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfidenceInterval:
    """Confidence interval data"""
    confidence_level: float  # e.g., 0.95 for 95%
    lower_bound: float
    upper_bound: float
    mean: float
    median: float
    mode: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DistributionAnalysis:
    """Complete distribution analysis data"""
    distribution_type: str
    histogram: HistogramData
    pdf_cdf: PDFCDFData
    confidence_intervals: List[ConfidenceInterval]
    statistics: Dict[str, Any]
    percentiles: Dict[str, float]
    generated_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class DistributionAnalyzer:
    """Analyze and generate probability distribution data"""
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize distribution analyzer"""
        self.random_state = random_state
        self.np_random = np.random.RandomState(random_state)
    
    def analyze_risk_distribution(
        self,
        risk_scores: List[float],
        distribution_type: DistributionType = DistributionType.EMPIRICAL,
        num_bins: int = 30,
        confidence_levels: Optional[List[float]] = None
    ) -> DistributionAnalysis:
        """
        Analyze risk score distribution
        
        Args:
            risk_scores: List of risk scores to analyze
            distribution_type: Type of distribution to fit
            num_bins: Number of histogram bins
            confidence_levels: List of confidence levels (e.g., [0.90, 0.95, 0.99])
            
        Returns:
            Complete distribution analysis
        """
        if confidence_levels is None:
            confidence_levels = [0.90, 0.95, 0.99]
        
        risk_array = np.array(risk_scores)
        
        # Generate histogram
        histogram = self._generate_histogram(risk_array, num_bins)
        
        # Fit distribution and generate PDF/CDF
        pdf_cdf = self._fit_distribution(risk_array, distribution_type)
        
        # Calculate confidence intervals
        confidence_intervals = [
            self._calculate_confidence_interval(risk_array, level)
            for level in confidence_levels
        ]
        
        # Calculate statistics
        statistics = self._calculate_statistics(risk_array)
        
        # Calculate percentiles
        percentiles = self._calculate_percentiles(risk_array)
        
        return DistributionAnalysis(
            distribution_type=distribution_type.value,
            histogram=histogram,
            pdf_cdf=pdf_cdf,
            confidence_intervals=confidence_intervals,
            statistics=statistics,
            percentiles=percentiles,
            generated_at=datetime.utcnow().isoformat(),
            metadata={
                'sample_size': len(risk_scores),
                'description': f'{distribution_type.value} distribution analysis of risk scores'
            }
        )
    
    def analyze_monte_carlo_results(
        self,
        simulation_results: List[float],
        num_bins: int = 50
    ) -> DistributionAnalysis:
        """
        Analyze Monte Carlo simulation results
        
        Args:
            simulation_results: List of simulation outcomes
            num_bins: Number of histogram bins
            
        Returns:
            Distribution analysis optimized for Monte Carlo results
        """
        return self.analyze_risk_distribution(
            risk_scores=simulation_results,
            distribution_type=DistributionType.EMPIRICAL,
            num_bins=num_bins,
            confidence_levels=[0.90, 0.95, 0.99]
        )
    
    def compare_distributions(
        self,
        baseline_scores: List[float],
        scenario_scores: List[float],
        num_bins: int = 30
    ) -> Dict[str, Any]:
        """
        Compare two distributions (e.g., baseline vs scenario)
        
        Args:
            baseline_scores: Baseline risk scores
            scenario_scores: Scenario risk scores
            num_bins: Number of histogram bins
            
        Returns:
            Comparison data structure
        """
        baseline_analysis = self.analyze_risk_distribution(
            baseline_scores,
            num_bins=num_bins
        )
        scenario_analysis = self.analyze_risk_distribution(
            scenario_scores,
            num_bins=num_bins
        )
        
        # Statistical tests
        ks_statistic, ks_pvalue = stats.ks_2samp(baseline_scores, scenario_scores)
        t_statistic, t_pvalue = stats.ttest_ind(baseline_scores, scenario_scores)
        
        # Effect size (Cohen's d)
        cohens_d = self._calculate_cohens_d(
            np.array(baseline_scores),
            np.array(scenario_scores)
        )
        
        return {
            'baseline': baseline_analysis,
            'scenario': scenario_analysis,
            'statistical_tests': {
                'kolmogorov_smirnov': {
                    'statistic': float(ks_statistic),
                    'p_value': float(ks_pvalue),
                    'significant': ks_pvalue < 0.05
                },
                't_test': {
                    'statistic': float(t_statistic),
                    'p_value': float(t_pvalue),
                    'significant': t_pvalue < 0.05
                },
                'cohens_d': {
                    'value': float(cohens_d),
                    'interpretation': self._interpret_cohens_d(cohens_d)
                }
            },
            'comparison_metrics': {
                'mean_difference': scenario_analysis.statistics['mean'] - baseline_analysis.statistics['mean'],
                'median_difference': scenario_analysis.statistics['median'] - baseline_analysis.statistics['median'],
                'std_difference': scenario_analysis.statistics['std'] - baseline_analysis.statistics['std'],
                'percentile_95_difference': (
                    scenario_analysis.percentiles['p95'] - baseline_analysis.percentiles['p95']
                )
            },
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def generate_risk_bands(
        self,
        risk_scores: List[float],
        num_bands: int = 5
    ) -> Dict[str, Any]:
        """
        Generate risk bands (quintiles/quartiles) data
        
        Args:
            risk_scores: List of risk scores
            num_bands: Number of bands to create
            
        Returns:
            Risk bands data structure
        """
        risk_array = np.array(risk_scores)
        
        # Calculate band boundaries
        percentiles = np.linspace(0, 100, num_bands + 1)
        boundaries = np.percentile(risk_array, percentiles)
        
        # Categorize scores into bands
        bands = []
        for i in range(num_bands):
            lower = boundaries[i]
            upper = boundaries[i + 1]
            
            # Find scores in this band
            if i == num_bands - 1:  # Last band includes upper boundary
                mask = (risk_array >= lower) & (risk_array <= upper)
            else:
                mask = (risk_array >= lower) & (risk_array < upper)
            
            band_scores = risk_array[mask]
            
            bands.append({
                'band_index': i,
                'band_name': self._get_band_name(i, num_bands),
                'lower_bound': float(lower),
                'upper_bound': float(upper),
                'count': int(np.sum(mask)),
                'percentage': float(np.sum(mask) / len(risk_array) * 100),
                'mean': float(np.mean(band_scores)) if len(band_scores) > 0 else 0.0,
                'median': float(np.median(band_scores)) if len(band_scores) > 0 else 0.0
            })
        
        return {
            'num_bands': num_bands,
            'total_count': len(risk_scores),
            'bands': bands,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def to_json(self, analysis: DistributionAnalysis) -> Dict[str, Any]:
        """
        Convert distribution analysis to JSON-serializable format
        
        Args:
            analysis: DistributionAnalysis object
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            'distribution_type': analysis.distribution_type,
            'histogram': {
                'bin_edges': analysis.histogram.bin_edges,
                'bin_counts': analysis.histogram.bin_counts,
                'bin_centers': analysis.histogram.bin_centers,
                'bin_widths': analysis.histogram.bin_widths,
                'total_count': analysis.histogram.total_count,
                'density': analysis.histogram.density,
                'metadata': analysis.histogram.metadata
            },
            'pdf_cdf': {
                'x_values': analysis.pdf_cdf.x_values,
                'pdf_values': analysis.pdf_cdf.pdf_values,
                'cdf_values': analysis.pdf_cdf.cdf_values,
                'distribution_type': analysis.pdf_cdf.distribution_type,
                'parameters': analysis.pdf_cdf.parameters,
                'metadata': analysis.pdf_cdf.metadata
            },
            'confidence_intervals': [
                {
                    'confidence_level': ci.confidence_level,
                    'lower_bound': ci.lower_bound,
                    'upper_bound': ci.upper_bound,
                    'mean': ci.mean,
                    'median': ci.median,
                    'mode': ci.mode,
                    'metadata': ci.metadata
                }
                for ci in analysis.confidence_intervals
            ],
            'statistics': analysis.statistics,
            'percentiles': analysis.percentiles,
            'generated_at': analysis.generated_at,
            'metadata': analysis.metadata
        }
    
    # Helper methods
    
    def _generate_histogram(self, data: np.ndarray, num_bins: int) -> HistogramData:
        """Generate histogram data"""
        counts, edges = np.histogram(data, bins=num_bins)
        centers = (edges[:-1] + edges[1:]) / 2
        widths = np.diff(edges)
        
        # Calculate density (normalized)
        total = np.sum(counts)
        density = counts / total if total > 0 else counts
        
        return HistogramData(
            bin_edges=edges.tolist(),
            bin_counts=counts.tolist(),
            bin_centers=centers.tolist(),
            bin_widths=widths.tolist(),
            total_count=int(total),
            density=density.tolist(),
            metadata={'num_bins': num_bins}
        )
    
    def _fit_distribution(
        self,
        data: np.ndarray,
        dist_type: DistributionType
    ) -> PDFCDFData:
        """Fit distribution and generate PDF/CDF data"""
        # Generate x values for smooth curves
        x_min, x_max = np.min(data), np.max(data)
        margin = (x_max - x_min) * 0.1
        x_values = np.linspace(x_min - margin, x_max + margin, 200)
        
        if dist_type == DistributionType.NORMAL:
            mean, std = np.mean(data), np.std(data)
            pdf_values = stats.norm.pdf(x_values, mean, std)
            cdf_values = stats.norm.cdf(x_values, mean, std)
            parameters = {'mean': float(mean), 'std': float(std)}
            
        elif dist_type == DistributionType.LOGNORMAL:
            # Fit lognormal (data must be positive)
            data_positive = data[data > 0]
            if len(data_positive) > 0:
                shape, loc, scale = stats.lognorm.fit(data_positive)
                pdf_values = stats.lognorm.pdf(x_values, shape, loc, scale)
                cdf_values = stats.lognorm.cdf(x_values, shape, loc, scale)
                parameters = {'shape': float(shape), 'loc': float(loc), 'scale': float(scale)}
            else:
                pdf_values = np.zeros_like(x_values)
                cdf_values = np.zeros_like(x_values)
                parameters = {'shape': 0.0, 'loc': 0.0, 'scale': 0.0}
        
        elif dist_type == DistributionType.BETA:
            # Fit beta distribution (data in [0,1])
            data_normalized = (data - x_min) / (x_max - x_min) if x_max > x_min else data
            a, b, loc, scale = stats.beta.fit(data_normalized)
            x_norm = (x_values - x_min) / (x_max - x_min) if x_max > x_min else x_values
            pdf_values = stats.beta.pdf(x_norm, a, b, loc, scale)
            cdf_values = stats.beta.cdf(x_norm, a, b, loc, scale)
            parameters = {'a': float(a), 'b': float(b), 'loc': float(loc), 'scale': float(scale)}
            
        elif dist_type == DistributionType.EMPIRICAL:
            # Use kernel density estimation
            kde = stats.gaussian_kde(data)
            pdf_values = kde(x_values)
            
            # Empirical CDF
            cdf_values = np.array([np.sum(data <= x) / len(data) for x in x_values])
            parameters = {'bandwidth': float(kde.factor)}
            
        else:  # Default to normal
            mean, std = np.mean(data), np.std(data)
            pdf_values = stats.norm.pdf(x_values, mean, std)
            cdf_values = stats.norm.cdf(x_values, mean, std)
            parameters = {'mean': float(mean), 'std': float(std)}
        
        return PDFCDFData(
            x_values=x_values.tolist(),
            pdf_values=pdf_values.tolist(),
            cdf_values=cdf_values.tolist(),
            distribution_type=dist_type.value,
            parameters=parameters,
            metadata={'num_points': len(x_values)}
        )
    
    def _calculate_confidence_interval(
        self,
        data: np.ndarray,
        confidence_level: float
    ) -> ConfidenceInterval:
        """Calculate confidence interval"""
        mean = np.mean(data)
        median = np.median(data)
        
        # Calculate confidence interval
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        lower_bound = np.percentile(data, lower_percentile)
        upper_bound = np.percentile(data, upper_percentile)
        
        # Try to calculate mode (most frequent value or peak of KDE)
        try:
            kde = stats.gaussian_kde(data)
            x_range = np.linspace(np.min(data), np.max(data), 1000)
            mode = float(x_range[np.argmax(kde(x_range))])
        except:
            mode = None
        
        return ConfidenceInterval(
            confidence_level=confidence_level,
            lower_bound=float(lower_bound),
            upper_bound=float(upper_bound),
            mean=float(mean),
            median=float(median),
            mode=mode,
            metadata={
                'interval_width': float(upper_bound - lower_bound),
                'margin_of_error': float((upper_bound - lower_bound) / 2)
            }
        )
    
    def _calculate_statistics(self, data: np.ndarray) -> Dict[str, Any]:
        """Calculate comprehensive statistics"""
        return {
            'count': int(len(data)),
            'mean': float(np.mean(data)),
            'median': float(np.median(data)),
            'std': float(np.std(data)),
            'variance': float(np.var(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'range': float(np.max(data) - np.min(data)),
            'skewness': float(stats.skew(data)),
            'kurtosis': float(stats.kurtosis(data)),
            'coefficient_of_variation': float(np.std(data) / np.mean(data)) if np.mean(data) != 0 else 0.0
        }
    
    def _calculate_percentiles(self, data: np.ndarray) -> Dict[str, float]:
        """Calculate key percentiles"""
        percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
        return {
            f'p{p}': float(np.percentile(data, p))
            for p in percentiles
        }
    
    def _calculate_cohens_d(self, group1: np.ndarray, group2: np.ndarray) -> float:
        """Calculate Cohen's d effect size"""
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        return (np.mean(group2) - np.mean(group1)) / pooled_std
    
    def _interpret_cohens_d(self, d: float) -> str:
        """Interpret Cohen's d effect size"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return 'negligible'
        elif abs_d < 0.5:
            return 'small'
        elif abs_d < 0.8:
            return 'medium'
        else:
            return 'large'
    
    def _get_band_name(self, index: int, num_bands: int) -> str:
        """Get descriptive name for risk band"""
        if num_bands == 5:
            names = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
            return names[index]
        elif num_bands == 4:
            names = ['Low', 'Medium', 'High', 'Critical']
            return names[index]
        else:
            return f'Band {index + 1}'
