#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Scoring Algorithm
Core algorithm for calculating composite bias scores from fairness metrics.
"""

import logging
import numpy as np
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict

from .utils import normalize_metric, validate_weights, aggregate_metrics


logger = logging.getLogger("bias_scoring_algorithm")


@dataclass
class ScoringConfiguration:
    """Configuration for bias scoring algorithm."""
    demographic_parity_weight: float = 0.30
    equalized_odds_weight: float = 0.35
    calibration_weight: float = 0.20
    individual_fairness_weight: float = 0.15
    
    # Normalization parameters
    dp_max_difference: float = 1.0  # Max expected demographic parity difference
    eo_max_difference: float = 1.0  # Max expected equalized odds difference
    calibration_max_error: float = 0.5  # Max expected calibration error
    if_min_consistency: float = 0.0  # Min expected individual fairness consistency
    
    def to_weights_dict(self) -> Dict[str, float]:
        """Convert configuration to weights dictionary."""
        return {
            "demographic_parity": self.demographic_parity_weight,
            "equalized_odds": self.equalized_odds_weight,
            "calibration": self.calibration_weight,
            "individual_fairness": self.individual_fairness_weight
        }


class BiasScoreAlgorithm:
    """
    Core algorithm for calculating composite bias scores.
    
    The algorithm:
    1. Normalizes each fairness metric to [0, 1] scale (0 = perfectly fair, 1 = severely biased)
    2. Applies configurable weights to each metric
    3. Calculates weighted sum to produce composite bias score
    4. Provides metric contributions for explainability
    """
    
    def __init__(self, config: Optional[ScoringConfiguration] = None):
        """
        Initialize bias scoring algorithm.
        
        Args:
            config: Scoring configuration (uses defaults if None)
        """
        self.config = config or ScoringConfiguration()
        self.logger = logger
        
        # Validate weights
        weights = self.config.to_weights_dict()
        if not validate_weights(weights):
            self.logger.warning("Weights do not sum to 1.0, using normalized weights")
            total = sum(weights.values())
            self.config.demographic_parity_weight /= total
            self.config.equalized_odds_weight /= total
            self.config.calibration_weight /= total
            self.config.individual_fairness_weight /= total
    
    def normalize_demographic_parity(self, dp_difference: float) -> float:
        """
        Normalize demographic parity difference to [0, 1] scale.
        
        Args:
            dp_difference: Max difference in positive rates across groups
            
        Returns:
            Normalized score (0 = fair, 1 = biased)
        """
        return normalize_metric(
            dp_difference,
            min_val=0.0,
            max_val=self.config.dp_max_difference,
            invert=False  # Higher difference = worse = higher score
        )
    
    def normalize_equalized_odds(self, eo_difference: float) -> float:
        """
        Normalize equalized odds difference to [0, 1] scale.
        
        Args:
            eo_difference: Max of TPR/FPR differences across groups
            
        Returns:
            Normalized score (0 = fair, 1 = biased)
        """
        return normalize_metric(
            eo_difference,
            min_val=0.0,
            max_val=self.config.eo_max_difference,
            invert=False  # Higher difference = worse = higher score
        )
    
    def normalize_calibration(self, calibration_error: float) -> float:
        """
        Normalize calibration error to [0, 1] scale.
        
        Args:
            calibration_error: Calibration error metric (e.g., ECE, Brier)
            
        Returns:
            Normalized score (0 = well-calibrated, 1 = poorly calibrated)
        """
        return normalize_metric(
            calibration_error,
            min_val=0.0,
            max_val=self.config.calibration_max_error,
            invert=False  # Higher error = worse = higher score
        )
    
    def normalize_individual_fairness(self, if_consistency: float) -> float:
        """
        Normalize individual fairness consistency to [0, 1] scale.
        
        Args:
            if_consistency: Individual fairness consistency score
            
        Returns:
            Normalized score (0 = consistent, 1 = inconsistent)
        """
        return normalize_metric(
            if_consistency,
            min_val=self.config.if_min_consistency,
            max_val=1.0,
            invert=True  # Higher consistency = better = lower score
        )
    
    def calculate_composite_score(self, raw_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate composite bias score from raw fairness metrics.
        
        Args:
            raw_metrics: Dictionary containing:
                - demographic_parity: Max difference in positive rates
                - equalized_odds: Max of TPR/FPR differences
                - calibration: Calibration error (ECE, Brier, etc.)
                - individual_fairness: Consistency score
        
        Returns:
            Dictionary containing:
                - overall_bias_score: Composite score [0, 1]
                - normalized_metrics: Each metric normalized to [0, 1]
                - metric_contributions: Weighted contribution of each metric
                - weights_used: Weights applied to each metric
        """
        try:
            # Extract raw metrics with defaults
            dp_raw = raw_metrics.get("demographic_parity", 0.0)
            eo_raw = raw_metrics.get("equalized_odds", 0.0)
            cal_raw = raw_metrics.get("calibration", 0.0)
            if_raw = raw_metrics.get("individual_fairness", 1.0)  # Default 1.0 = perfect consistency
            
            # Normalize each metric
            dp_normalized = self.normalize_demographic_parity(dp_raw)
            eo_normalized = self.normalize_equalized_odds(eo_raw)
            cal_normalized = self.normalize_calibration(cal_raw)
            if_normalized = self.normalize_individual_fairness(if_raw)
            
            normalized_metrics = {
                "demographic_parity": dp_normalized,
                "equalized_odds": eo_normalized,
                "calibration": cal_normalized,
                "individual_fairness": if_normalized
            }
            
            # Calculate weighted contributions
            weights = self.config.to_weights_dict()
            contributions = {
                metric: normalized_metrics[metric] * weights[metric]
                for metric in weights.keys()
            }
            
            # Calculate composite score
            composite_score = sum(contributions.values())
            
            # Ensure score is in [0, 1] range
            composite_score = np.clip(composite_score, 0.0, 1.0)
            
            return {
                "overall_bias_score": float(composite_score),
                "normalized_metrics": normalized_metrics,
                "metric_contributions": contributions,
                "weights_used": weights,
                "raw_metrics": raw_metrics
            }
            
        except Exception as e:
            self.logger.error(f"Composite score calculation failed: {e}")
            return {
                "overall_bias_score": 0.0,
                "normalized_metrics": {},
                "metric_contributions": {},
                "weights_used": {},
                "raw_metrics": raw_metrics,
                "error": str(e)
            }
    
    def calculate_metric_importance(self, score_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate the importance (contribution percentage) of each metric.
        
        Args:
            score_data: Output from calculate_composite_score
            
        Returns:
            Dictionary of metric importance percentages
        """
        try:
            contributions = score_data.get("metric_contributions", {})
            total_contribution = sum(contributions.values())
            
            if total_contribution == 0:
                return {metric: 0.0 for metric in contributions.keys()}
            
            importance = {
                metric: (contrib / total_contribution) * 100
                for metric, contrib in contributions.items()
            }
            
            return importance
            
        except Exception as e:
            self.logger.error(f"Metric importance calculation failed: {e}")
            return {}
    
    def get_dominant_metric(self, score_data: Dict[str, Any]) -> Tuple[str, float]:
        """
        Identify the metric contributing most to the bias score.
        
        Args:
            score_data: Output from calculate_composite_score
            
        Returns:
            Tuple of (metric_name, contribution_value)
        """
        try:
            contributions = score_data.get("metric_contributions", {})
            if not contributions:
                return ("unknown", 0.0)
            
            dominant_metric = max(contributions.items(), key=lambda x: x[1])
            return dominant_metric
            
        except Exception as e:
            self.logger.error(f"Dominant metric identification failed: {e}")
            return ("unknown", 0.0)


def main():
    """Test the bias scoring algorithm."""
    print("🧪 Testing Bias Scoring Algorithm")
    
    # Create algorithm instance
    algorithm = BiasScoreAlgorithm()
    
    # Test with sample metrics
    raw_metrics = {
        "demographic_parity": 0.35,  # 35% difference in positive rates
        "equalized_odds": 0.52,      # Max 52% difference in TPR/FPR
        "calibration": 0.28,         # 28% calibration error
        "individual_fairness": 0.60  # 60% consistency
    }
    
    # Calculate composite score
    result = algorithm.calculate_composite_score(raw_metrics)
    
    print("✅ Bias scoring algorithm test completed")
    print(f"✅ Overall bias score: {result['overall_bias_score']:.3f}")
    print(f"✅ Normalized metrics: {result['normalized_metrics']}")
    print(f"✅ Metric contributions: {result['metric_contributions']}")
    
    # Calculate importance
    importance = algorithm.calculate_metric_importance(result)
    print(f"✅ Metric importance: {importance}")
    
    # Get dominant metric
    dominant_metric, contribution = algorithm.get_dominant_metric(result)
    print(f"✅ Dominant metric: {dominant_metric} ({contribution:.3f})")


if __name__ == "__main__":
    main()
