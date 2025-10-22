#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Scoring Utilities
Helper functions for normalization, validation, and statistical operations.
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple, Any


logger = logging.getLogger("bias_scoring_utils")


def normalize_metric(value: float, min_val: float = 0.0, max_val: float = 1.0,
                     invert: bool = False) -> float:
    """
    Normalize a metric to [0, 1] range.
    
    Args:
        value: Raw metric value
        min_val: Minimum expected value
        max_val: Maximum expected value
        invert: If True, inverts the normalization (1 = worse)
        
    Returns:
        Normalized value in [0, 1] range
    """
    try:
        # Clip value to expected range
        clipped_value = np.clip(value, min_val, max_val)
        
        # Normalize to [0, 1]
        if max_val - min_val == 0:
            normalized = 0.0
        else:
            normalized = (clipped_value - min_val) / (max_val - min_val)
        
        # Invert if needed (for metrics where higher is worse)
        if invert:
            normalized = 1.0 - normalized
            
        return float(normalized)
        
    except Exception as e:
        logger.error(f"Metric normalization failed: {e}")
        return 0.0


def validate_weights(weights: Dict[str, float], tolerance: float = 1e-6) -> bool:
    """
    Validate that weights sum to 1.0.
    
    Args:
        weights: Dictionary of metric weights
        tolerance: Acceptable deviation from 1.0
        
    Returns:
        True if weights are valid, False otherwise
    """
    try:
        total = sum(weights.values())
        return abs(total - 1.0) < tolerance
    except Exception as e:
        logger.error(f"Weight validation failed: {e}")
        return False


def calculate_confidence_interval(values: np.ndarray, confidence: float = 0.95,
                                 n_bootstrap: int = 1000) -> Tuple[float, float]:
    """
    Calculate bootstrap confidence interval for a metric.
    
    Args:
        values: Array of values
        confidence: Confidence level (default 95%)
        n_bootstrap: Number of bootstrap samples
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    try:
        if len(values) == 0:
            return (0.0, 0.0)
        
        # Bootstrap resampling
        bootstrap_means = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(values, size=len(values), replace=True)
            bootstrap_means.append(np.mean(sample))
        
        # Calculate percentiles
        alpha = 1 - confidence
        lower = np.percentile(bootstrap_means, 100 * alpha / 2)
        upper = np.percentile(bootstrap_means, 100 * (1 - alpha / 2))
        
        return (float(lower), float(upper))
        
    except Exception as e:
        logger.error(f"Confidence interval calculation failed: {e}")
        return (0.0, 0.0)


def check_data_quality(data: Dict[str, Any], required_keys: List[str]) -> Tuple[bool, List[str]]:
    """
    Check if data contains all required keys.
    
    Args:
        data: Data dictionary to validate
        required_keys: List of required keys
        
    Returns:
        Tuple of (is_valid, missing_keys)
    """
    try:
        missing_keys = [key for key in required_keys if key not in data]
        return (len(missing_keys) == 0, missing_keys)
    except Exception as e:
        logger.error(f"Data quality check failed: {e}")
        return (False, required_keys)


def aggregate_metrics(metrics: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Aggregate multiple metrics using weighted sum.
    
    Args:
        metrics: Dictionary of metric values
        weights: Dictionary of metric weights
        
    Returns:
        Aggregated score
    """
    try:
        if not validate_weights(weights):
            logger.warning("Weights do not sum to 1.0, normalizing...")
            total_weight = sum(weights.values())
            weights = {k: v / total_weight for k, v in weights.items()}
        
        score = 0.0
        for metric_name, metric_value in metrics.items():
            if metric_name in weights:
                score += metric_value * weights[metric_name]
        
        return float(score)
        
    except Exception as e:
        logger.error(f"Metric aggregation failed: {e}")
        return 0.0


def calculate_statistical_significance(group1: np.ndarray, group2: np.ndarray,
                                      test: str = "ttest") -> float:
    """
    Calculate statistical significance between two groups.
    
    Args:
        group1: First group of values
        group2: Second group of values
        test: Statistical test to use ("ttest", "mannwhitney", "ks")
        
    Returns:
        P-value of the test
    """
    try:
        from scipy import stats
        
        if test == "ttest":
            _, p_value = stats.ttest_ind(group1, group2)
        elif test == "mannwhitney":
            _, p_value = stats.mannwhitneyu(group1, group2)
        elif test == "ks":
            _, p_value = stats.ks_2samp(group1, group2)
        else:
            logger.warning(f"Unknown test: {test}, using t-test")
            _, p_value = stats.ttest_ind(group1, group2)
        
        return float(p_value)
        
    except Exception as e:
        logger.warning(f"Statistical significance test failed: {e}")
        return 1.0  # Return non-significant p-value


def format_score(score: float, decimals: int = 3) -> str:
    """
    Format score for display.
    
    Args:
        score: Score value
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    try:
        return f"{score:.{decimals}f}"
    except Exception as e:
        logger.error(f"Score formatting failed: {e}")
        return "0.000"
