"""
Unified Post-processing Engine for Bias Mitigation.

This module provides a unified interface for applying post-processing
bias mitigation techniques with automatic method selection.
"""

import numpy as np
from typing import Dict, Optional, List, Any, Union, Tuple
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator
import logging

from .threshold_optimizer import (
    ThresholdOptimizer,
    OptimizationObjective,
    ThresholdOptimizationResult
)
from .calibration import (
    FairCalibrator,
    CalibrationMethod,
    CalibrationResult
)
from .equalized_odds_postprocessor import (
    EqualizedOddsPostprocessor,
    EOPostprocessingResult
)

logger = logging.getLogger(__name__)


@dataclass
class PostprocessingResult:
    """Result of post-processing mitigation"""
    method: str
    technique_results: Dict[str, Any]
    combined_metrics: Dict[str, float]
    fairness_improvement: Dict[str, float]
    predictions: np.ndarray
    probabilities: Optional[np.ndarray]
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        result = {
            'method': self.method,
            'technique_results': {},
            'combined_metrics': {k: float(v) for k, v in self.combined_metrics.items()},
            'fairness_improvement': {k: float(v) for k, v in self.fairness_improvement.items()},
            'metadata': self.metadata
        }
        
        # Convert technique results to dict
        for name, tech_result in self.technique_results.items():
            if hasattr(tech_result, 'to_dict'):
                result['technique_results'][name] = tech_result.to_dict()
            else:
                result['technique_results'][name] = str(tech_result)
        
        return result


class PostprocessingEngine:
    """
    Unified engine for post-processing bias mitigation.
    
    Automatically selects and applies appropriate post-processing techniques:
    - Threshold Optimization: For binary classification threshold adjustment
    - Fair Calibration: For probability calibration across groups
    - Equalized Odds Post-processing: For fairness constraint satisfaction
    
    Supports combined approaches (e.g., calibration + threshold optimization).
    """
    
    def __init__(self,
                 method: str = "auto",
                 calibration_method: Optional[str] = None,
                 threshold_objective: Optional[str] = None,
                 eo_constraint: Optional[str] = None,
                 combine_techniques: bool = False):
        """
        Initialize post-processing engine.
        
        Args:
            method: Post-processing method ("auto", "threshold", "calibration", 
                   "equalized_odds", "combined")
            calibration_method: Specific calibration method if using calibration
            threshold_objective: Threshold optimization objective
            eo_constraint: Equalized odds constraint type
            combine_techniques: Whether to combine multiple techniques
        """
        self.method = method
        self.calibration_method = calibration_method
        self.threshold_objective = threshold_objective
        self.eo_constraint = eo_constraint
        self.combine_techniques = combine_techniques
        
        # Will be populated during fit
        self.selected_method_: Optional[str] = None
        self.threshold_optimizer_: Optional[ThresholdOptimizer] = None
        self.calibrator_: Optional[FairCalibrator] = None
        self.eo_postprocessor_: Optional[EqualizedOddsPostprocessor] = None
        self.base_estimator_: Optional[BaseEstimator] = None
        
    def fit(self,
            estimator: BaseEstimator,
            X: np.ndarray,
            y_true: np.ndarray,
            y_proba: Optional[np.ndarray],
            sensitive_features: np.ndarray) -> 'PostprocessingEngine':
        """
        Fit post-processing technique(s).
        
        Args:
            estimator: Pre-trained classifier
            X: Training features
            y_true: True labels
            y_proba: Predicted probabilities (optional, will compute if needed)
            sensitive_features: Protected group memberships
            
        Returns:
            self
        """
        self.base_estimator_ = estimator
        
        # Get probabilities if not provided
        if y_proba is None:
            if hasattr(estimator, 'predict_proba'):
                y_proba = estimator.predict_proba(X)[:, 1]
            else:
                y_proba = estimator.predict(X).astype(float)
        
        # Select method if auto
        if self.method == "auto":
            self.selected_method_ = self._auto_select_method(
                estimator, y_true, y_proba, sensitive_features
            )
        else:
            self.selected_method_ = self.method
        
        # Fit selected techniques
        if self.selected_method_ in ["threshold", "combined"]:
            self._fit_threshold_optimizer(y_true, y_proba, sensitive_features)
        
        if self.selected_method_ in ["calibration", "combined"]:
            self._fit_calibrator(y_true, y_proba, sensitive_features)
        
        if self.selected_method_ in ["equalized_odds", "combined"]:
            self._fit_eo_postprocessor(estimator, X, y_true, sensitive_features)
        
        return self
    
    def _auto_select_method(self,
                            estimator: BaseEstimator,
                            y_true: np.ndarray,
                            y_proba: np.ndarray,
                            sensitive_features: np.ndarray) -> str:
        """
        Automatically select best post-processing method.
        
        Selection criteria:
        - Has predict_proba: Can use calibration
        - Binary classification: Can use threshold optimization
        - Complex bias patterns: Use equalized odds
        - Default: Threshold optimization
        """
        has_proba = hasattr(estimator, 'predict_proba')
        is_binary = len(np.unique(y_true)) == 2
        
        # Check calibration error
        if has_proba:
            calibration_error = self._estimate_calibration_error(y_true, y_proba)
            if calibration_error > 0.1:  # High calibration error
                logger.info("High calibration error detected, selecting calibration method")
                return "calibration"
        
        # Check if we should combine techniques
        if self.combine_techniques and has_proba and is_binary:
            logger.info("Combining calibration and threshold optimization")
            return "combined"
        
        # Default to threshold optimization for binary classification
        if is_binary:
            logger.info("Binary classification detected, selecting threshold optimization")
            return "threshold"
        
        # Fall back to equalized odds
        logger.info("Selecting equalized odds post-processing")
        return "equalized_odds"
    
    def _estimate_calibration_error(self, y_true: np.ndarray, y_proba: np.ndarray) -> float:
        """Estimate expected calibration error"""
        n_bins = 10
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        
        ece = 0.0
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            in_bin = (y_proba > bin_lower) & (y_proba <= bin_upper)
            prop_in_bin = np.mean(in_bin)
            
            if prop_in_bin > 0:
                avg_confidence = np.mean(y_proba[in_bin])
                avg_accuracy = np.mean(y_true[in_bin])
                ece += prop_in_bin * abs(avg_confidence - avg_accuracy)
        
        return ece
    
    def _fit_threshold_optimizer(self,
                                  y_true: np.ndarray,
                                  y_proba: np.ndarray,
                                  sensitive_features: np.ndarray):
        """Fit threshold optimizer"""
        objective = self.threshold_objective or "equal_opportunity"
        
        try:
            obj_enum = OptimizationObjective[objective.upper()]
        except KeyError:
            obj_enum = OptimizationObjective.EQUAL_OPPORTUNITY
        
        self.threshold_optimizer_ = ThresholdOptimizer(
            objective=obj_enum,
            constraint_slack=0.05,
            n_grid_points=100
        )
        
        self.threshold_optimizer_.fit(y_true, y_proba, sensitive_features)
        logger.info("Threshold optimizer fitted successfully")
    
    def _fit_calibrator(self,
                        y_true: np.ndarray,
                        y_proba: np.ndarray,
                        sensitive_features: np.ndarray):
        """Fit calibrator"""
        method = self.calibration_method or "platt"
        
        try:
            method_enum = CalibrationMethod[method.upper()]
        except KeyError:
            method_enum = CalibrationMethod.PLATT
        
        self.calibrator_ = FairCalibrator(
            method=method_enum,
            n_bins=10
        )
        
        self.calibrator_.fit(y_true, y_proba, sensitive_features)
        logger.info("Calibrator fitted successfully")
    
    def _fit_eo_postprocessor(self,
                               estimator: BaseEstimator,
                               X: np.ndarray,
                               y_true: np.ndarray,
                               sensitive_features: np.ndarray):
        """Fit equalized odds postprocessor"""
        constraint = self.eo_constraint or "equalized_odds"
        
        self.eo_postprocessor_ = EqualizedOddsPostprocessor(
            constraint=constraint,
            objective="accuracy_score",
            grid_size=100
        )
        
        self.eo_postprocessor_.fit(estimator, X, y_true, sensitive_features)
        logger.info("Equalized odds postprocessor fitted successfully")
    
    def predict(self,
                X: np.ndarray,
                sensitive_features: np.ndarray,
                return_proba: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Make predictions using post-processing.
        
        Args:
            X: Features to predict on
            sensitive_features: Protected group memberships
            return_proba: Whether to return probabilities
            
        Returns:
            Predictions (and probabilities if return_proba=True)
        """
        if self.selected_method_ is None:
            raise ValueError("Engine not fitted. Call fit() first.")
        
        # Get base predictions/probabilities
        if hasattr(self.base_estimator_, 'predict_proba'):
            y_proba = self.base_estimator_.predict_proba(X)[:, 1]
        else:
            y_proba = self.base_estimator_.predict(X).astype(float)
        
        # Apply techniques in sequence
        if self.selected_method_ in ["calibration", "combined"] and self.calibrator_ is not None:
            y_proba = self.calibrator_.predict_proba(y_proba, sensitive_features)
        
        if self.selected_method_ in ["threshold", "combined"] and self.threshold_optimizer_ is not None:
            predictions = self.threshold_optimizer_.predict(y_proba, sensitive_features)
        elif self.selected_method_ == "equalized_odds" and self.eo_postprocessor_ is not None:
            predictions = self.eo_postprocessor_.predict(X, sensitive_features)
        else:
            # Default: threshold at 0.5
            predictions = (y_proba >= 0.5).astype(int)
        
        if return_proba:
            return predictions, y_proba
        return predictions
    
    def evaluate(self,
                 X: np.ndarray,
                 y_true: np.ndarray,
                 sensitive_features: np.ndarray) -> PostprocessingResult:
        """
        Evaluate post-processing results.
        
        Args:
            X: Features
            y_true: True labels
            sensitive_features: Protected group memberships
            
        Returns:
            PostprocessingResult with comprehensive evaluation
        """
        # Get predictions
        predictions, probabilities = self.predict(X, sensitive_features, return_proba=True)
        
        # Collect results from each technique
        technique_results = {}
        
        if self.threshold_optimizer_ is not None:
            threshold_result = self.threshold_optimizer_.evaluate(
                y_true, probabilities, sensitive_features
            )
            technique_results['threshold_optimization'] = threshold_result
        
        if self.calibrator_ is not None:
            # Get original probabilities for comparison
            if hasattr(self.base_estimator_, 'predict_proba'):
                y_proba_orig = self.base_estimator_.predict_proba(X)[:, 1]
            else:
                y_proba_orig = self.base_estimator_.predict(X).astype(float)
            
            calibration_result = self.calibrator_.evaluate(
                y_true, y_proba_orig, probabilities, sensitive_features
            )
            technique_results['calibration'] = calibration_result
        
        if self.eo_postprocessor_ is not None:
            eo_result = self.eo_postprocessor_.evaluate(
                X, y_true, sensitive_features, self.base_estimator_
            )
            technique_results['equalized_odds'] = eo_result
        
        # Compute combined metrics
        combined_metrics = self._compute_combined_metrics(
            y_true, predictions, probabilities, sensitive_features
        )
        
        # Compute overall fairness improvement
        fairness_improvement = self._compute_overall_fairness_improvement(
            technique_results
        )
        
        return PostprocessingResult(
            method=self.selected_method_,
            technique_results=technique_results,
            combined_metrics=combined_metrics,
            fairness_improvement=fairness_improvement,
            predictions=predictions,
            probabilities=probabilities,
            metadata={
                'calibration_method': self.calibration_method,
                'threshold_objective': self.threshold_objective,
                'eo_constraint': self.eo_constraint,
                'combine_techniques': self.combine_techniques
            }
        )
    
    def _compute_combined_metrics(self,
                                   y_true: np.ndarray,
                                   predictions: np.ndarray,
                                   probabilities: np.ndarray,
                                   sensitive_features: np.ndarray) -> Dict[str, float]:
        """Compute combined performance and fairness metrics"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
        
        metrics = {
            'accuracy': accuracy_score(y_true, predictions),
            'precision': precision_score(y_true, predictions, zero_division=0),
            'recall': recall_score(y_true, predictions, zero_division=0)
        }
        
        # Add AUC if probabilities are valid
        if len(np.unique(y_true)) == 2 and np.min(probabilities) < np.max(probabilities):
            try:
                metrics['auc'] = roc_auc_score(y_true, probabilities)
            except:
                pass
        
        return metrics
    
    def _compute_overall_fairness_improvement(self,
                                              technique_results: Dict[str, Any]) -> Dict[str, float]:
        """Aggregate fairness improvements from all techniques"""
        improvement = {}
        
        for name, result in technique_results.items():
            if hasattr(result, 'fairness_improvement'):
                for metric, value in result.fairness_improvement.items():
                    key = f"{name}_{metric}"
                    improvement[key] = value
        
        return improvement


if __name__ == "__main__":
    # Test post-processing engine
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    
    print("="*60)
    print("Testing Post-processing Engine")
    print("="*60)
    
    # Generate test data
    np.random.seed(42)
    X, y = make_classification(n_samples=2000, n_features=20, 
                               n_informative=15, n_redundant=5,
                               random_state=42)
    
    # Create sensitive features with bias
    sensitive = np.random.choice([0, 1], size=2000, p=[0.6, 0.4])
    
    # Split data
    X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
        X, y, sensitive, test_size=0.3, random_state=42
    )
    
    # Train model
    print("\nTraining base model...")
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    # Get base probabilities
    y_proba_train = model.predict_proba(X_train)[:, 1]
    
    # Test different methods
    methods = ["auto", "threshold", "calibration", "equalized_odds", "combined"]
    
    for method in methods:
        print(f"\n{'-'*60}")
        print(f"Testing method: {method}")
        print('-'*60)
        
        try:
            # Create engine
            engine = PostprocessingEngine(
                method=method,
                calibration_method="platt",
                threshold_objective="equal_opportunity",
                eo_constraint="equalized_odds",
                combine_techniques=(method == "combined")
            )
            
            # Fit
            engine.fit(model, X_train, y_train, y_proba_train, s_train)
            
            print(f"  Selected method: {engine.selected_method_}")
            
            # Evaluate
            result = engine.evaluate(X_test, y_test, s_test)
            
            print(f"\nCombined Metrics:")
            for metric, value in result.combined_metrics.items():
                print(f"  {metric}: {value:.4f}")
            
            print(f"\nFairness Improvements:")
            for metric, value in result.fairness_improvement.items():
                print(f"  {metric}: {value:.4f}")
            
            print(f"\nTechniques Applied: {list(result.technique_results.keys())}")
            
        except Exception as e:
            print(f"Error testing {method}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("Post-processing engine tests completed!")
    print('='*60)
