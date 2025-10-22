"""
Mitigation validation using fairness metrics.

Validates bias mitigation effectiveness by comparing fairness metrics
before and after mitigation, and checking model performance impact.

Author: REGIQ AI/ML Team  
Phase: 3.5 - Mitigation Validation
"""

import numpy as np
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import logging

# Import Phase 3.2 fairness metrics
from services.bias_analysis.metrics.demographic_parity import DemographicParityAnalyzer
from services.bias_analysis.metrics.equalized_odds import EqualizedOddsAnalyzer
from services.bias_analysis.metrics.calibration_analysis import CalibrationAnalyzer

# Import Phase 3.4 bias scoring
from services.bias_analysis.scoring.composite_calculator import BiasScoreCalculator

# Import model wrapper
from services.bias_analysis.mitigation.utils.model_wrapper import ModelWrapper

logger = logging.getLogger(__name__)


@dataclass
class MetricsComparison:
    """Comparison of metrics before and after mitigation"""
    metric_name: str
    before_value: float
    after_value: float
    improvement: float
    improvement_pct: float
    meets_threshold: bool


@dataclass
class ValidationReport:
    """Comprehensive validation report for mitigation"""
    mitigation_technique: str
    
    # Fairness metrics comparison
    demographic_parity_comparison: MetricsComparison
    equalized_odds_comparison: MetricsComparison
    calibration_comparison: Optional[MetricsComparison]
    
    # Bias score comparison
    bias_score_before: float
    bias_score_after: float
    bias_score_improvement: float
    bias_score_improvement_pct: float
    
    # Model performance comparison
    accuracy_before: float
    accuracy_after: float
    accuracy_change: float
    accuracy_change_pct: float
    
    # Overall assessment
    fairness_improved: bool
    accuracy_acceptable: bool
    mitigation_effective: bool
    
    # Metadata
    protected_attribute: str
    n_samples_before: int
    n_samples_after: int
    timestamp: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        return result
    
    def to_json(self, filepath: Optional[str] = None) -> str:
        """Convert to JSON string or save to file"""
        json_str = json.dumps(self.to_dict(), indent=2)
        
        if filepath:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(json_str)
            logger.info(f"Validation report saved to {filepath}")
        
        return json_str


class MitigationValidator:
    """
    Validate bias mitigation effectiveness.
    
    Compares fairness metrics and model performance before/after mitigation
    to assess effectiveness and identify trade-offs.
    """
    
    def __init__(self,
                 fairness_threshold: float = 0.1,
                 max_accuracy_drop: float = 0.03):
        """
        Initialize mitigation validator.
        
        Args:
            fairness_threshold: Max acceptable fairness metric value (e.g., 0.1 for 10%)
            max_accuracy_drop: Max acceptable accuracy drop (e.g., 0.03 for 3%)
        """
        self.fairness_threshold = fairness_threshold
        self.max_accuracy_drop = max_accuracy_drop
        
        # Initialize analyzers
        self.dp_analyzer = DemographicParityAnalyzer()
        self.eo_analyzer = EqualizedOddsAnalyzer()
        self.calib_analyzer = CalibrationAnalyzer()
        self.bias_calculator = BiasScoreCalculator()
    
    def validate_mitigation(self,
                           model: Any,
                           X_before: np.ndarray,
                           y_before: np.ndarray,
                           protected_attr_before: np.ndarray,
                           X_after: np.ndarray,
                           y_after: np.ndarray,
                           protected_attr_after: np.ndarray,
                           sample_weights: Optional[np.ndarray] = None,
                           mitigation_technique: str = 'unknown',
                           protected_attr_name: str = 'protected_attribute') -> ValidationReport:
        """
        Validate mitigation by comparing before/after metrics.
        
        Args:
            model: ML model to train and evaluate
            X_before: Features before mitigation
            y_before: Labels before mitigation
            protected_attr_before: Protected attributes before mitigation
            X_after: Features after mitigation
            y_after: Labels after mitigation
            protected_attr_after: Protected attributes after mitigation
            sample_weights: Optional sample weights (for reweighting)
            mitigation_technique: Name of mitigation technique used
            protected_attr_name: Name of protected attribute
            
        Returns:
            ValidationReport with comprehensive comparison
        """
        logger.info(f"Validating mitigation: {mitigation_technique}")
        
        # Wrap model
        model_wrapper = ModelWrapper(model)
        
        # Train on before data
        logger.info("Training model on pre-mitigation data...")
        model_before = model_wrapper.clone()
        model_before.fit(X_before, y_before)
        y_pred_before = model_before.predict(X_before)
        y_proba_before = model_before.predict_proba(X_before) if model_before.metadata.has_predict_proba else None
        
        # Train on after data
        logger.info("Training model on post-mitigation data...")
        model_after = model_wrapper.clone()
        model_after.fit(X_after, y_after, sample_weight=sample_weights)
        y_pred_after = model_after.predict(X_after)
        y_proba_after = model_after.predict_proba(X_after) if model_after.metadata.has_predict_proba else None
        
        # Calculate fairness metrics - BEFORE
        logger.info("Calculating pre-mitigation fairness metrics...")
        dp_before = self._calculate_demographic_parity(
            y_before, y_pred_before, protected_attr_before
        )
        eo_before = self._calculate_equalized_odds(
            y_before, y_pred_before, protected_attr_before
        )
        calib_before = self._calculate_calibration(
            y_before, y_proba_before, protected_attr_before
        ) if y_proba_before is not None else None
        
        # Calculate fairness metrics - AFTER
        logger.info("Calculating post-mitigation fairness metrics...")
        dp_after = self._calculate_demographic_parity(
            y_after, y_pred_after, protected_attr_after
        )
        eo_after = self._calculate_equalized_odds(
            y_after, y_pred_after, protected_attr_after
        )
        calib_after = self._calculate_calibration(
            y_after, y_proba_after, protected_attr_after
        ) if y_proba_after is not None else None
        
        # Calculate bias scores
        logger.info("Calculating bias scores...")
        bias_score_before = self._calculate_bias_score(
            y_before, y_pred_before, protected_attr_before, y_proba_before
        )
        bias_score_after = self._calculate_bias_score(
            y_after, y_pred_after, protected_attr_after, y_proba_after
        )
        
        # Calculate accuracy
        accuracy_before = float(np.mean(y_pred_before == y_before))
        accuracy_after = float(np.mean(y_pred_after == y_after))
        
        # Create comparisons
        dp_comparison = self._create_comparison(
            'demographic_parity_difference',
            dp_before,
            dp_after,
            self.fairness_threshold
        )
        
        eo_comparison = self._create_comparison(
            'equalized_odds_difference',
            eo_before,
            eo_after,
            self.fairness_threshold
        )
        
        calib_comparison = self._create_comparison(
            'calibration_difference',
            calib_before if calib_before is not None else 0.0,
            calib_after if calib_after is not None else 0.0,
            self.fairness_threshold
        ) if calib_before is not None and calib_after is not None else None
        
        # Overall assessment
        fairness_improved = (dp_comparison.improvement > 0 and eo_comparison.improvement > 0)
        accuracy_change = accuracy_after - accuracy_before
        accuracy_acceptable = accuracy_change >= -self.max_accuracy_drop
        mitigation_effective = fairness_improved and accuracy_acceptable
        
        # Create report
        from datetime import datetime
        report = ValidationReport(
            mitigation_technique=mitigation_technique,
            demographic_parity_comparison=dp_comparison,
            equalized_odds_comparison=eo_comparison,
            calibration_comparison=calib_comparison,
            bias_score_before=bias_score_before,
            bias_score_after=bias_score_after,
            bias_score_improvement=bias_score_before - bias_score_after,
            bias_score_improvement_pct=((bias_score_before - bias_score_after) / bias_score_before * 100) if bias_score_before > 0 else 0.0,
            accuracy_before=accuracy_before,
            accuracy_after=accuracy_after,
            accuracy_change=accuracy_change,
            accuracy_change_pct=(accuracy_change / accuracy_before * 100) if accuracy_before > 0 else 0.0,
            fairness_improved=fairness_improved,
            accuracy_acceptable=accuracy_acceptable,
            mitigation_effective=mitigation_effective,
            protected_attribute=protected_attr_name,
            n_samples_before=len(X_before),
            n_samples_after=len(X_after),
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(
            f"Validation complete. Effective: {mitigation_effective}, "
            f"Fairness improved: {fairness_improved}, "
            f"Accuracy acceptable: {accuracy_acceptable}"
        )
        
        return report
    
    def _calculate_demographic_parity(self,
                                     y_true: np.ndarray,
                                     y_pred: np.ndarray,
                                     protected_attr: np.ndarray) -> float:
        """Calculate demographic parity difference"""
        try:
            result = self.dp_analyzer.analyze(y_true, y_pred, protected_attr)
            return abs(result.demographic_parity_difference)
        except Exception as e:
            logger.warning(f"DP calculation failed: {e}")
            return 0.0
    
    def _calculate_equalized_odds(self,
                                 y_true: np.ndarray,
                                 y_pred: np.ndarray,
                                 protected_attr: np.ndarray) -> float:
        """Calculate equalized odds difference"""
        try:
            result = self.eo_analyzer.analyze(y_true, y_pred, protected_attr)
            # Use average of TPR and FPR differences
            return (abs(result.true_positive_rate_difference) + 
                   abs(result.false_positive_rate_difference)) / 2.0
        except Exception as e:
            logger.warning(f"EO calculation failed: {e}")
            return 0.0
    
    def _calculate_calibration(self,
                              y_true: np.ndarray,
                              y_proba: Optional[np.ndarray],
                              protected_attr: np.ndarray) -> Optional[float]:
        """Calculate calibration difference"""
        if y_proba is None:
            return None
        
        try:
            result = self.calib_analyzer.analyze(y_true, y_proba, protected_attr)
            return abs(result.calibration_difference)
        except Exception as e:
            logger.warning(f"Calibration calculation failed: {e}")
            return None
    
    def _calculate_bias_score(self,
                             y_true: np.ndarray,
                             y_pred: np.ndarray,
                             protected_attr: np.ndarray,
                             y_proba: Optional[np.ndarray]) -> float:
        """Calculate composite bias score using Phase 3.4 calculator"""
        try:
            result = self.bias_calculator.calculate_bias_score(
                y_true=y_true,
                y_pred=y_pred,
                protected_attr=protected_attr,
                y_proba=y_proba,
                industry='technology'  # Default industry
            )
            return result.composite_score
        except Exception as e:
            logger.warning(f"Bias score calculation failed: {e}")
            return 0.0
    
    def _create_comparison(self,
                          metric_name: str,
                          before_value: float,
                          after_value: float,
                          threshold: float) -> MetricsComparison:
        """Create metrics comparison object"""
        improvement = before_value - after_value  # Positive = better (lower is better)
        improvement_pct = (improvement / before_value * 100) if before_value > 0 else 0.0
        meets_threshold = after_value <= threshold
        
        return MetricsComparison(
            metric_name=metric_name,
            before_value=before_value,
            after_value=after_value,
            improvement=improvement,
            improvement_pct=improvement_pct,
            meets_threshold=meets_threshold
        )
    
    def generate_summary(self, report: ValidationReport) -> str:
        """Generate human-readable summary of validation results"""
        lines = [
            f"Mitigation Validation Report - {report.mitigation_technique}",
            "=" * 60,
            "",
            "Fairness Metrics:",
            f"  Demographic Parity: {report.demographic_parity_comparison.before_value:.4f} → {report.demographic_parity_comparison.after_value:.4f} ({report.demographic_parity_comparison.improvement_pct:+.1f}%)",
            f"  Equalized Odds: {report.equalized_odds_comparison.before_value:.4f} → {report.equalized_odds_comparison.after_value:.4f} ({report.equalized_odds_comparison.improvement_pct:+.1f}%)",
        ]
        
        if report.calibration_comparison:
            lines.append(
                f"  Calibration: {report.calibration_comparison.before_value:.4f} → {report.calibration_comparison.after_value:.4f} ({report.calibration_comparison.improvement_pct:+.1f}%)"
            )
        
        lines.extend([
            "",
            "Bias Score:",
            f"  Before: {report.bias_score_before:.4f}",
            f"  After: {report.bias_score_after:.4f}",
            f"  Improvement: {report.bias_score_improvement_pct:+.1f}%",
            "",
            "Model Performance:",
            f"  Accuracy Before: {report.accuracy_before:.4f}",
            f"  Accuracy After: {report.accuracy_after:.4f}",
            f"  Change: {report.accuracy_change_pct:+.1f}%",
            "",
            "Overall Assessment:",
            f"  Fairness Improved: {'✓' if report.fairness_improved else '✗'}",
            f"  Accuracy Acceptable: {'✓' if report.accuracy_acceptable else '✗'}",
            f"  Mitigation Effective: {'✓' if report.mitigation_effective else '✗'}",
            ""
        ])
        
        return "\n".join(lines)
