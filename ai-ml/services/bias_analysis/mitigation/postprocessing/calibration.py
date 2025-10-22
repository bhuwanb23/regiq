"""
Fair Calibration Techniques for Bias Mitigation.

This module provides group-aware probability calibration methods to ensure
well-calibrated predictions across protected groups.
"""

import numpy as np
from typing import Dict, Optional, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from sklearn.calibration import CalibratedClassifierCV
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
import logging

logger = logging.getLogger(__name__)


class CalibrationMethod(Enum):
    """Calibration method to use"""
    PLATT = "platt"  # Platt scaling (logistic regression)
    ISOTONIC = "isotonic"  # Isotonic regression
    TEMPERATURE = "temperature"  # Temperature scaling
    BETA = "beta"  # Beta calibration


@dataclass
class CalibrationResult:
    """Result of fair calibration"""
    method: str
    group_calibrators: Dict[int, Any]
    original_calibration_error: float
    calibrated_calibration_error: float
    group_calibration_errors: Dict[str, float]
    fairness_improvement: Dict[str, float]
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'method': self.method,
            'original_calibration_error': float(self.original_calibration_error),
            'calibrated_calibration_error': float(self.calibrated_calibration_error),
            'group_calibration_errors': {
                str(k): float(v) for k, v in self.group_calibration_errors.items()
            },
            'fairness_improvement': {
                k: float(v) for k, v in self.fairness_improvement.items()
            },
            'metadata': self.metadata
        }


class FairCalibrator:
    """
    Group-aware probability calibration for fair predictions.
    
    Calibrates prediction probabilities separately for each protected group
    to ensure well-calibrated predictions across all groups.
    
    Supports multiple calibration methods:
    - Platt Scaling: Logistic regression on prediction scores
    - Isotonic Regression: Non-parametric monotonic calibration
    - Temperature Scaling: Simple temperature parameter for neural networks
    - Beta Calibration: Three-parameter calibration
    """
    
    def __init__(self,
                 method: CalibrationMethod = CalibrationMethod.PLATT,
                 n_bins: int = 10):
        """
        Initialize fair calibrator.
        
        Args:
            method: Calibration method to use
            n_bins: Number of bins for calibration error estimation
        """
        self.method = method
        self.n_bins = n_bins
        self.group_calibrators_: Optional[Dict[int, Any]] = None
        self.groups_: Optional[np.ndarray] = None
        
    def fit(self,
            y_true: np.ndarray,
            y_proba: np.ndarray,
            sensitive_features: np.ndarray) -> 'FairCalibrator':
        """
        Fit calibrators for each protected group.
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities (before calibration)
            sensitive_features: Protected group memberships
            
        Returns:
            self
        """
        y_true = np.asarray(y_true)
        y_proba = np.asarray(y_proba)
        sensitive_features = np.asarray(sensitive_features)
        
        # Get unique groups
        self.groups_ = np.unique(sensitive_features)
        self.group_calibrators_ = {}
        
        # Fit calibrator for each group
        for group in self.groups_:
            group_mask = sensitive_features == group
            y_group = y_true[group_mask]
            proba_group = y_proba[group_mask]
            
            if len(np.unique(y_group)) < 2:
                logger.warning(f"Group {group} has only one class, skipping calibration")
                self.group_calibrators_[group] = None
                continue
            
            # Fit calibrator based on method
            if self.method == CalibrationMethod.PLATT:
                calibrator = self._fit_platt(y_group, proba_group)
            elif self.method == CalibrationMethod.ISOTONIC:
                calibrator = self._fit_isotonic(y_group, proba_group)
            elif self.method == CalibrationMethod.TEMPERATURE:
                calibrator = self._fit_temperature(y_group, proba_group)
            elif self.method == CalibrationMethod.BETA:
                calibrator = self._fit_beta(y_group, proba_group)
            else:
                raise ValueError(f"Unknown calibration method: {self.method}")
            
            self.group_calibrators_[group] = calibrator
        
        return self
    
    def _fit_platt(self, y_true: np.ndarray, y_proba: np.ndarray) -> LogisticRegression:
        """Fit Platt scaling (logistic regression on scores)"""
        # Convert probabilities to logits
        epsilon = 1e-7
        y_proba_clipped = np.clip(y_proba, epsilon, 1 - epsilon)
        logits = np.log(y_proba_clipped / (1 - y_proba_clipped))
        
        # Fit logistic regression
        calibrator = LogisticRegression()
        calibrator.fit(logits.reshape(-1, 1), y_true)
        
        return calibrator
    
    def _fit_isotonic(self, y_true: np.ndarray, y_proba: np.ndarray) -> IsotonicRegression:
        """Fit isotonic regression calibration"""
        calibrator = IsotonicRegression(out_of_bounds='clip')
        calibrator.fit(y_proba, y_true)
        return calibrator
    
    def _fit_temperature(self, y_true: np.ndarray, y_proba: np.ndarray) -> Dict:
        """Fit temperature scaling"""
        # Find optimal temperature via cross-entropy minimization
        epsilon = 1e-7
        y_proba_clipped = np.clip(y_proba, epsilon, 1 - epsilon)
        logits = np.log(y_proba_clipped / (1 - y_proba_clipped))
        
        # Grid search for best temperature
        temperatures = np.linspace(0.1, 5.0, 50)
        best_temp = 1.0
        best_nll = float('inf')
        
        for temp in temperatures:
            # Apply temperature scaling
            scaled_proba = 1 / (1 + np.exp(-logits / temp))
            scaled_proba = np.clip(scaled_proba, epsilon, 1 - epsilon)
            
            # Compute negative log-likelihood
            nll = -np.mean(y_true * np.log(scaled_proba) + 
                          (1 - y_true) * np.log(1 - scaled_proba))
            
            if nll < best_nll:
                best_nll = nll
                best_temp = temp
        
        return {'temperature': best_temp}
    
    def _fit_beta(self, y_true: np.ndarray, y_proba: np.ndarray) -> Dict:
        """Fit beta calibration (simplified version)"""
        # Simplified beta calibration using logistic regression with features
        epsilon = 1e-7
        y_proba_clipped = np.clip(y_proba, epsilon, 1 - epsilon)
        
        # Create features: log-odds, log-odds squared, log-odds cubed
        logits = np.log(y_proba_clipped / (1 - y_proba_clipped))
        features = np.column_stack([
            logits,
            logits ** 2,
            logits ** 3
        ])
        
        # Fit logistic regression
        calibrator = LogisticRegression()
        calibrator.fit(features, y_true)
        
        return {'model': calibrator}
    
    def predict_proba(self,
                      y_proba: np.ndarray,
                      sensitive_features: np.ndarray) -> np.ndarray:
        """
        Apply calibration to prediction probabilities.
        
        Args:
            y_proba: Uncalibrated probabilities
            sensitive_features: Protected group memberships
            
        Returns:
            Calibrated probabilities
        """
        if self.group_calibrators_ is None:
            raise ValueError("Calibrator not fitted. Call fit() first.")
        
        y_proba = np.asarray(y_proba)
        sensitive_features = np.asarray(sensitive_features)
        calibrated_proba = np.zeros_like(y_proba)
        
        # Apply group-specific calibration
        for group in self.groups_:
            group_mask = sensitive_features == group
            proba_group = y_proba[group_mask]
            
            if self.group_calibrators_[group] is None:
                # No calibration for this group
                calibrated_proba[group_mask] = proba_group
                continue
            
            # Apply calibration based on method
            if self.method == CalibrationMethod.PLATT:
                calibrated = self._apply_platt(proba_group, self.group_calibrators_[group])
            elif self.method == CalibrationMethod.ISOTONIC:
                calibrated = self.group_calibrators_[group].predict(proba_group)
            elif self.method == CalibrationMethod.TEMPERATURE:
                calibrated = self._apply_temperature(proba_group, self.group_calibrators_[group])
            elif self.method == CalibrationMethod.BETA:
                calibrated = self._apply_beta(proba_group, self.group_calibrators_[group])
            else:
                calibrated = proba_group
            
            calibrated_proba[group_mask] = calibrated
        
        return calibrated_proba
    
    def _apply_platt(self, y_proba: np.ndarray, calibrator: LogisticRegression) -> np.ndarray:
        """Apply Platt scaling"""
        epsilon = 1e-7
        y_proba_clipped = np.clip(y_proba, epsilon, 1 - epsilon)
        logits = np.log(y_proba_clipped / (1 - y_proba_clipped))
        return calibrator.predict_proba(logits.reshape(-1, 1))[:, 1]
    
    def _apply_temperature(self, y_proba: np.ndarray, calibrator: Dict) -> np.ndarray:
        """Apply temperature scaling"""
        epsilon = 1e-7
        y_proba_clipped = np.clip(y_proba, epsilon, 1 - epsilon)
        logits = np.log(y_proba_clipped / (1 - y_proba_clipped))
        temp = calibrator['temperature']
        calibrated = 1 / (1 + np.exp(-logits / temp))
        return np.clip(calibrated, epsilon, 1 - epsilon)
    
    def _apply_beta(self, y_proba: np.ndarray, calibrator: Dict) -> np.ndarray:
        """Apply beta calibration"""
        epsilon = 1e-7
        y_proba_clipped = np.clip(y_proba, epsilon, 1 - epsilon)
        logits = np.log(y_proba_clipped / (1 - y_proba_clipped))
        features = np.column_stack([
            logits,
            logits ** 2,
            logits ** 3
        ])
        return calibrator['model'].predict_proba(features)[:, 1]
    
    def evaluate(self,
                 y_true: np.ndarray,
                 y_proba_original: np.ndarray,
                 y_proba_calibrated: np.ndarray,
                 sensitive_features: np.ndarray) -> CalibrationResult:
        """
        Evaluate calibration quality and fairness.
        
        Args:
            y_true: True labels
            y_proba_original: Original (uncalibrated) probabilities
            y_proba_calibrated: Calibrated probabilities
            sensitive_features: Protected group memberships
            
        Returns:
            CalibrationResult with evaluation metrics
        """
        # Compute overall calibration errors
        original_error = self._calibration_error(y_true, y_proba_original)
        calibrated_error = self._calibration_error(y_true, y_proba_calibrated)
        
        # Compute per-group calibration errors
        group_errors = {}
        for group in self.groups_:
            group_mask = sensitive_features == group
            if np.sum(group_mask) == 0:
                continue
            
            group_error = self._calibration_error(
                y_true[group_mask],
                y_proba_calibrated[group_mask]
            )
            group_errors[f"group_{group}"] = group_error
        
        # Compute fairness improvement
        max_group_error = max(group_errors.values()) if group_errors else 0.0
        min_group_error = min(group_errors.values()) if group_errors else 0.0
        calibration_disparity = max_group_error - min_group_error
        
        fairness_improvement = {
            'calibration_error_reduction': original_error - calibrated_error,
            'calibration_disparity': calibration_disparity,
            'relative_improvement': (original_error - calibrated_error) / (original_error + 1e-7)
        }
        
        return CalibrationResult(
            method=self.method.value,
            group_calibrators=self.group_calibrators_,
            original_calibration_error=original_error,
            calibrated_calibration_error=calibrated_error,
            group_calibration_errors=group_errors,
            fairness_improvement=fairness_improvement,
            metadata={
                'n_bins': self.n_bins,
                'n_groups': len(self.groups_)
            }
        )
    
    def _calibration_error(self, y_true: np.ndarray, y_proba: np.ndarray) -> float:
        """
        Compute Expected Calibration Error (ECE).
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            
        Returns:
            Expected calibration error
        """
        if len(y_true) == 0:
            return 0.0
        
        # Create bins
        bin_boundaries = np.linspace(0, 1, self.n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        
        ece = 0.0
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            # Find samples in this bin
            in_bin = (y_proba > bin_lower) & (y_proba <= bin_upper)
            prop_in_bin = np.mean(in_bin)
            
            if prop_in_bin > 0:
                # Average confidence and accuracy in this bin
                avg_confidence = np.mean(y_proba[in_bin])
                avg_accuracy = np.mean(y_true[in_bin])
                
                # Add weighted difference to ECE
                ece += prop_in_bin * abs(avg_confidence - avg_accuracy)
        
        return ece


if __name__ == "__main__":
    # Test fair calibration
    from sklearn.datasets import make_classification
    
    # Generate test data
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    sensitive = np.random.choice([0, 1], size=1000)
    
    # Generate some uncalibrated probabilities (shifted for each group)
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
        X, y, sensitive, test_size=0.3, random_state=42
    )
    
    # Train model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Get uncalibrated probabilities
    y_proba_train = model.predict_proba(X_train)[:, 1]
    y_proba_test = model.predict_proba(X_test)[:, 1]
    
    # Test each calibration method
    for method in CalibrationMethod:
        print(f"\n{'='*60}")
        print(f"Testing {method.value} calibration")
        print('='*60)
        
        try:
            calibrator = FairCalibrator(method=method, n_bins=10)
            calibrator.fit(y_train, y_proba_train, s_train)
            
            # Apply calibration
            y_proba_calibrated = calibrator.predict_proba(y_proba_test, s_test)
            
            # Evaluate
            result = calibrator.evaluate(y_test, y_proba_test, y_proba_calibrated, s_test)
            
            print(f"\nCalibration Results:")
            print(f"  Original ECE: {result.original_calibration_error:.4f}")
            print(f"  Calibrated ECE: {result.calibrated_calibration_error:.4f}")
            print(f"  Improvement: {result.fairness_improvement['calibration_error_reduction']:.4f}")
            print(f"  Relative Improvement: {result.fairness_improvement['relative_improvement']:.2%}")
            
            print(f"\nPer-Group Calibration Errors:")
            for group, error in result.group_calibration_errors.items():
                print(f"  {group}: {error:.4f}")
            
            print(f"\nCalibration Disparity: {result.fairness_improvement['calibration_disparity']:.4f}")
            
        except Exception as e:
            print(f"Error testing {method.value}: {str(e)}")
    
    print(f"\n{'='*60}")
    print("Fair calibration tests completed!")
    print('='*60)
