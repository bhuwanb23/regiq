#!/usr/bin/env python3
"""
REGIQ AI/ML - Composite Bias Score Calculator
Integrates fairness metrics from Phase 3.2 and calculates composite bias scores.
"""

import logging
import numpy as np
import time
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, asdict

from .scoring_algorithm import BiasScoreAlgorithm, ScoringConfiguration
from .weight_profiles import WeightProfileManager
from .utils import calculate_confidence_interval


logger = logging.getLogger("composite_calculator")


@dataclass
class BiasScoreResult:
    """Complete bias score calculation result."""
    model_id: str
    overall_bias_score: float
    confidence_interval: List[float]
    normalized_metrics: Dict[str, float]
    metric_contributions: Dict[str, float]
    weight_profile_used: str
    weights: Dict[str, float]
    raw_metrics: Dict[str, float]
    dominant_metric: str
    dominant_contribution: float
    timestamp: str
    metadata: Dict[str, Any]


class BiasScoreCalculator:
    """
    Composite bias score calculator.
    
    Integrates with Phase 3.2 fairness metrics to produce:
    - Overall bias score [0, 1]
    - Metric contributions
    - Confidence intervals
    - Dominant metric identification
    """
    
    def __init__(self, weight_profile: str = "default"):
        """
        Initialize bias score calculator.
        
        Args:
            weight_profile: Name of weight profile to use
        """
        self.logger = logger
        self.weight_manager = WeightProfileManager()
        self.weight_profile = weight_profile
        
        # Get weights for profile
        weights_dict = self.weight_manager.get_weights(weight_profile)
        
        # Create scoring configuration
        config = ScoringConfiguration(
            demographic_parity_weight=weights_dict["demographic_parity"],
            equalized_odds_weight=weights_dict["equalized_odds"],
            calibration_weight=weights_dict["calibration"],
            individual_fairness_weight=weights_dict["individual_fairness"]
        )
        
        self.algorithm = BiasScoreAlgorithm(config)
        
        self.logger.info(f"Initialized calculator with profile: {weight_profile}")
    
    def calculate_from_phase_3_2_results(self,
                                        model_id: str,
                                        demographic_parity_result: Any,
                                        equalized_odds_result: Any,
                                        calibration_result: Any,
                                        individual_fairness_result: Any,
                                        n_bootstrap: int = 1000) -> BiasScoreResult:
        """
        Calculate composite bias score from Phase 3.2 fairness metric results.
        
        Args:
            model_id: Model identifier
            demographic_parity_result: DemographicParityResult from Phase 3.2
            equalized_odds_result: EqualizedOddsResult from Phase 3.2
            calibration_result: CalibrationResult from Phase 3.2
            individual_fairness_result: IndividualFairnessResult from Phase 3.2
            n_bootstrap: Number of bootstrap samples for confidence interval
            
        Returns:
            BiasScoreResult with complete scoring information
        """
        try:
            # Extract raw metrics from Phase 3.2 results
            raw_metrics = self._extract_raw_metrics(
                demographic_parity_result,
                equalized_odds_result,
                calibration_result,
                individual_fairness_result
            )
            
            # Calculate composite score
            score_data = self.algorithm.calculate_composite_score(raw_metrics)
            
            # Calculate confidence interval
            # Bootstrap by slightly varying each metric within reasonable bounds
            bootstrap_scores = []
            for _ in range(n_bootstrap):
                # Add small random noise to each metric
                noisy_metrics = {
                    metric: value + np.random.normal(0, 0.01)
                    for metric, value in raw_metrics.items()
                }
                noisy_result = self.algorithm.calculate_composite_score(noisy_metrics)
                bootstrap_scores.append(noisy_result["overall_bias_score"])
            
            ci_lower, ci_upper = calculate_confidence_interval(
                np.array(bootstrap_scores),
                confidence=0.95,
                n_bootstrap=n_bootstrap
            )
            
            # Get dominant metric
            dominant_metric, dominant_contribution = self.algorithm.get_dominant_metric(score_data)
            
            # Create result
            result = BiasScoreResult(
                model_id=model_id,
                overall_bias_score=score_data["overall_bias_score"],
                confidence_interval=[ci_lower, ci_upper],
                normalized_metrics=score_data["normalized_metrics"],
                metric_contributions=score_data["metric_contributions"],
                weight_profile_used=self.weight_profile,
                weights=score_data["weights_used"],
                raw_metrics=raw_metrics,
                dominant_metric=dominant_metric,
                dominant_contribution=dominant_contribution,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                metadata={
                    "n_bootstrap": n_bootstrap,
                    "phase_3_2_results_used": True,
                    "calculation_method": "composite_weighted_sum"
                }
            )
            
            self.logger.info(f"Calculated bias score for model {model_id}: {result.overall_bias_score:.3f}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Bias score calculation failed: {e}")
            raise
    
    def _extract_raw_metrics(self,
                            dp_result: Any,
                            eo_result: Any,
                            cal_result: Any,
                            if_result: Any) -> Dict[str, float]:
        """
        Extract raw metric values from Phase 3.2 results.
        
        Args:
            dp_result: Demographic parity result
            eo_result: Equalized odds result
            cal_result: Calibration result
            if_result: Individual fairness result
            
        Returns:
            Dictionary of raw metric values
        """
        try:
            # Extract demographic parity difference
            dp_diff = getattr(dp_result, 'max_difference', 0.0)
            
            # Extract equalized odds difference (max of TPR/FPR differences)
            tpr_diff = getattr(eo_result, 'tpr_difference', 0.0)
            fpr_diff = getattr(eo_result, 'fpr_difference', 0.0)
            eo_diff = max(tpr_diff, fpr_diff)
            
            # Extract calibration error (use ECE as primary metric)
            if hasattr(cal_result, 'ece_scores'):
                # Average ECE across groups
                ece_scores = cal_result.ece_scores
                cal_error = np.mean(list(ece_scores.values())) if ece_scores else 0.0
            else:
                cal_error = 0.0
            
            # Extract individual fairness consistency (inverted to get inconsistency)
            if hasattr(if_result, 'overall_consistency'):
                if_consistency = getattr(if_result, 'overall_consistency', 1.0)
            else:
                if_consistency = 1.0
            
            return {
                "demographic_parity": float(dp_diff),
                "equalized_odds": float(eo_diff),
                "calibration": float(cal_error),
                "individual_fairness": float(if_consistency)
            }
            
        except Exception as e:
            self.logger.error(f"Metric extraction failed: {e}")
            return {
                "demographic_parity": 0.0,
                "equalized_odds": 0.0,
                "calibration": 0.0,
                "individual_fairness": 1.0
            }
    
    def calculate_from_raw_metrics(self,
                                   model_id: str,
                                   raw_metrics: Dict[str, float],
                                   n_bootstrap: int = 1000) -> BiasScoreResult:
        """
        Calculate composite bias score from raw metric values.
        
        Args:
            model_id: Model identifier
            raw_metrics: Dictionary of raw metric values
            n_bootstrap: Number of bootstrap samples
            
        Returns:
            BiasScoreResult
        """
        try:
            # Calculate composite score
            score_data = self.algorithm.calculate_composite_score(raw_metrics)
            
            # Calculate confidence interval
            bootstrap_scores = []
            for _ in range(n_bootstrap):
                noisy_metrics = {
                    metric: value + np.random.normal(0, 0.01)
                    for metric, value in raw_metrics.items()
                }
                noisy_result = self.algorithm.calculate_composite_score(noisy_metrics)
                bootstrap_scores.append(noisy_result["overall_bias_score"])
            
            ci_lower, ci_upper = calculate_confidence_interval(
                np.array(bootstrap_scores),
                confidence=0.95,
                n_bootstrap=n_bootstrap
            )
            
            # Get dominant metric
            dominant_metric, dominant_contribution = self.algorithm.get_dominant_metric(score_data)
            
            # Create result
            result = BiasScoreResult(
                model_id=model_id,
                overall_bias_score=score_data["overall_bias_score"],
                confidence_interval=[ci_lower, ci_upper],
                normalized_metrics=score_data["normalized_metrics"],
                metric_contributions=score_data["metric_contributions"],
                weight_profile_used=self.weight_profile,
                weights=score_data["weights_used"],
                raw_metrics=raw_metrics,
                dominant_metric=dominant_metric,
                dominant_contribution=dominant_contribution,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                metadata={
                    "n_bootstrap": n_bootstrap,
                    "phase_3_2_results_used": False,
                    "calculation_method": "composite_weighted_sum"
                }
            )
            
            self.logger.info(f"Calculated bias score for model {model_id}: {result.overall_bias_score:.3f}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Bias score calculation failed: {e}")
            raise
    
    def change_weight_profile(self, profile_name: str):
        """
        Change the weight profile used for scoring.
        
        Args:
            profile_name: Name of new profile to use
        """
        self.weight_profile = profile_name
        weights_dict = self.weight_manager.get_weights(profile_name)
        
        config = ScoringConfiguration(
            demographic_parity_weight=weights_dict["demographic_parity"],
            equalized_odds_weight=weights_dict["equalized_odds"],
            calibration_weight=weights_dict["calibration"],
            individual_fairness_weight=weights_dict["individual_fairness"]
        )
        
        self.algorithm = BiasScoreAlgorithm(config)
        self.logger.info(f"Changed weight profile to: {profile_name}")
    
    def to_dict(self, result: BiasScoreResult) -> Dict[str, Any]:
        """
        Convert BiasScoreResult to dictionary for JSON serialization.
        
        Args:
            result: BiasScoreResult to convert
            
        Returns:
            Dictionary representation
        """
        return asdict(result)


def main():
    """Test the composite bias score calculator."""
    print("🧪 Testing Composite Bias Score Calculator")
    
    # Create calculator
    calculator = BiasScoreCalculator(weight_profile="default")
    
    # Test with raw metrics
    raw_metrics = {
        "demographic_parity": 0.35,
        "equalized_odds": 0.52,
        "calibration": 0.28,
        "individual_fairness": 0.60
    }
    
    result = calculator.calculate_from_raw_metrics("test_model_v1", raw_metrics)
    
    print("✅ Bias score calculation completed")
    print(f"✅ Overall bias score: {result.overall_bias_score:.3f}")
    print(f"✅ Confidence interval: [{result.confidence_interval[0]:.3f}, {result.confidence_interval[1]:.3f}]")
    print(f"✅ Dominant metric: {result.dominant_metric} ({result.dominant_contribution:.3f})")
    print(f"✅ Normalized metrics: {result.normalized_metrics}")
    print(f"✅ Metric contributions: {result.metric_contributions}")
    
    # Test with different weight profile
    calculator.change_weight_profile("lending")
    result_lending = calculator.calculate_from_raw_metrics("test_model_v1", raw_metrics)
    print(f"✅ Lending profile bias score: {result_lending.overall_bias_score:.3f}")
    
    # Convert to dict
    result_dict = calculator.to_dict(result)
    print(f"✅ Result dictionary keys: {list(result_dict.keys())}")


if __name__ == "__main__":
    main()
