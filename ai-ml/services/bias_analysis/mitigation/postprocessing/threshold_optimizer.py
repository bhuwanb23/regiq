"""
Threshold optimization for fairness.

Adjusts decision thresholds per protected group to achieve fairness
criteria such as demographic parity, equal opportunity, or equalized odds.

Author: REGIQ AI/ML Team
Phase: 3.5.3 - Post-processing Mitigation
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from sklearn.metrics import roc_curve
import logging

logger = logging.getLogger(__name__)


class OptimizationObjective(Enum):
    """Objective for threshold optimization"""
    DEMOGRAPHIC_PARITY = "demographic_parity"
    EQUAL_OPPORTUNITY = "equal_opportunity"
    EQUALIZED_ODDS = "equalized_odds"
    MAXIMIZE_ACCURACY = "maximize_accuracy"


@dataclass
class ThresholdOptimizationResult:
    """Result of threshold optimization"""
    group_thresholds: Dict[int, float]
    objective: str
    original_accuracy: float
    optimized_accuracy: float
    fairness_improvement: Dict[str, float]
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'group_thresholds': {str(k): float(v) for k, v in self.group_thresholds.items()},
            'objective': self.objective,
            'original_accuracy': float(self.original_accuracy),
            'optimized_accuracy': float(self.optimized_accuracy),
            'fairness_improvement': {k: float(v) for k, v in self.fairness_improvement.items()},
            'metadata': self.metadata
        }


class ThresholdOptimizer:
    """
    Optimize classification thresholds per protected group for fairness.
    
    Supports multiple objectives:
    - Demographic Parity: Equal positive prediction rates
    - Equal Opportunity: Equal true positive rates
    - Equalized Odds: Equal TPR and FPR
    - Maximize Accuracy: Best overall accuracy with fairness constraint
    """
    
    def __init__(self,
                 objective: OptimizationObjective = OptimizationObjective.EQUAL_OPPORTUNITY,
                 constraint_slack: float = 0.05,
                 n_grid_points: int = 100):
        """
        Initialize threshold optimizer.
        
        Args:
            objective: Optimization objective
            constraint_slack: Allowed fairness violation (e.g., 0.05 = 5%)
            n_grid_points: Number of threshold values to try
        """
        self.objective = objective
        self.constraint_slack = constraint_slack
        self.n_grid_points = n_grid_points
        
        self.group_thresholds_: Optional[Dict[int, float]] = None
        self.is_fitted_ = False
    
    def fit(self,
            y_true: np.ndarray,
            y_proba: np.ndarray,
            sensitive_features: np.ndarray) -> 'ThresholdOptimizer':
        """
        Find optimal thresholds for each group.
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            sensitive_features: Protected attribute values
            
        Returns:
            self
        """
        logger.info(f"Optimizing thresholds for {self.objective.value}")
        
        unique_groups = np.unique(sensitive_features)
        
        if self.objective == OptimizationObjective.DEMOGRAPHIC_PARITY:
            self.group_thresholds_ = self._optimize_demographic_parity(
                y_true, y_proba, sensitive_features, unique_groups
            )
        elif self.objective == OptimizationObjective.EQUAL_OPPORTUNITY:
            self.group_thresholds_ = self._optimize_equal_opportunity(
                y_true, y_proba, sensitive_features, unique_groups
            )
        elif self.objective == OptimizationObjective.EQUALIZED_ODDS:
            self.group_thresholds_ = self._optimize_equalized_odds(
                y_true, y_proba, sensitive_features, unique_groups
            )
        elif self.objective == OptimizationObjective.MAXIMIZE_ACCURACY:
            self.group_thresholds_ = self._optimize_accuracy(
                y_true, y_proba, sensitive_features, unique_groups
            )
        else:
            raise ValueError(f"Unknown objective: {self.objective}")
        
        self.is_fitted_ = True
        logger.info(f"Optimized thresholds: {self.group_thresholds_}")
        
        return self
    
    def predict(self,
                y_proba: np.ndarray,
                sensitive_features: np.ndarray) -> np.ndarray:
        """
        Make predictions using optimized thresholds.
        
        Args:
            y_proba: Predicted probabilities
            sensitive_features: Protected attribute values
            
        Returns:
            Binary predictions
        """
        if not self.is_fitted_:
            raise ValueError("Optimizer must be fitted before prediction")
        
        predictions = np.zeros(len(y_proba), dtype=int)
        
        for group, threshold in self.group_thresholds_.items():
            group_mask = sensitive_features == group
            predictions[group_mask] = (y_proba[group_mask] >= threshold).astype(int)
        
        return predictions
    
    def _optimize_demographic_parity(self,
                                     y_true: np.ndarray,
                                     y_proba: np.ndarray,
                                     sensitive_features: np.ndarray,
                                     unique_groups: np.ndarray) -> Dict[int, float]:
        """Optimize for demographic parity (equal positive rates)"""
        
        # Grid search over thresholds
        thresholds_grid = np.linspace(0.0, 1.0, self.n_grid_points)
        
        best_thresholds = {}
        best_score = -np.inf
        
        # Try all combinations
        for t1 in thresholds_grid:
            for t2 in thresholds_grid:
                thresholds = {unique_groups[0]: t1, unique_groups[1]: t2}
                
                # Calculate positive rates
                pos_rates = {}
                for group in unique_groups:
                    mask = sensitive_features == group
                    preds = (y_proba[mask] >= thresholds[group]).astype(int)
                    pos_rates[group] = np.mean(preds)
                
                # Check demographic parity constraint
                dp_diff = abs(pos_rates[unique_groups[0]] - pos_rates[unique_groups[1]])
                
                if dp_diff <= self.constraint_slack:
                    # Calculate accuracy
                    preds = np.zeros(len(y_true), dtype=int)
                    for group in unique_groups:
                        mask = sensitive_features == group
                        preds[mask] = (y_proba[mask] >= thresholds[group]).astype(int)
                    
                    accuracy = np.mean(preds == y_true)
                    
                    if accuracy > best_score:
                        best_score = accuracy
                        best_thresholds = thresholds.copy()
        
        # If no solution found, use default
        if not best_thresholds:
            logger.warning("No solution satisfying constraint found, using 0.5")
            best_thresholds = {g: 0.5 for g in unique_groups}
        
        return best_thresholds
    
    def _optimize_equal_opportunity(self,
                                    y_true: np.ndarray,
                                    y_proba: np.ndarray,
                                    sensitive_features: np.ndarray,
                                    unique_groups: np.ndarray) -> Dict[int, float]:
        """Optimize for equal opportunity (equal TPR)"""
        
        thresholds_grid = np.linspace(0.0, 1.0, self.n_grid_points)
        
        best_thresholds = {}
        best_score = -np.inf
        
        for t1 in thresholds_grid:
            for t2 in thresholds_grid:
                thresholds = {unique_groups[0]: t1, unique_groups[1]: t2}
                
                # Calculate TPR per group
                tprs = {}
                for group in unique_groups:
                    mask = sensitive_features == group
                    y_true_group = y_true[mask]
                    y_proba_group = y_proba[mask]
                    
                    preds = (y_proba_group >= thresholds[group]).astype(int)
                    
                    # TPR = TP / (TP + FN)
                    tp = np.sum((preds == 1) & (y_true_group == 1))
                    fn = np.sum((preds == 0) & (y_true_group == 1))
                    
                    tprs[group] = tp / (tp + fn) if (tp + fn) > 0 else 0
                
                # Check equal opportunity constraint
                tpr_diff = abs(tprs[unique_groups[0]] - tprs[unique_groups[1]])
                
                if tpr_diff <= self.constraint_slack:
                    # Calculate accuracy
                    preds = np.zeros(len(y_true), dtype=int)
                    for group in unique_groups:
                        mask = sensitive_features == group
                        preds[mask] = (y_proba[mask] >= thresholds[group]).astype(int)
                    
                    accuracy = np.mean(preds == y_true)
                    
                    if accuracy > best_score:
                        best_score = accuracy
                        best_thresholds = thresholds.copy()
        
        if not best_thresholds:
            logger.warning("No solution found, using 0.5")
            best_thresholds = {g: 0.5 for g in unique_groups}
        
        return best_thresholds
    
    def _optimize_equalized_odds(self,
                                 y_true: np.ndarray,
                                 y_proba: np.ndarray,
                                 sensitive_features: np.ndarray,
                                 unique_groups: np.ndarray) -> Dict[int, float]:
        """Optimize for equalized odds (equal TPR and FPR)"""
        
        thresholds_grid = np.linspace(0.0, 1.0, self.n_grid_points)
        
        best_thresholds = {}
        best_score = -np.inf
        
        for t1 in thresholds_grid:
            for t2 in thresholds_grid:
                thresholds = {unique_groups[0]: t1, unique_groups[1]: t2}
                
                # Calculate TPR and FPR per group
                tprs = {}
                fprs = {}
                
                for group in unique_groups:
                    mask = sensitive_features == group
                    y_true_group = y_true[mask]
                    y_proba_group = y_proba[mask]
                    
                    preds = (y_proba_group >= thresholds[group]).astype(int)
                    
                    # TPR
                    tp = np.sum((preds == 1) & (y_true_group == 1))
                    fn = np.sum((preds == 0) & (y_true_group == 1))
                    tprs[group] = tp / (tp + fn) if (tp + fn) > 0 else 0
                    
                    # FPR
                    fp = np.sum((preds == 1) & (y_true_group == 0))
                    tn = np.sum((preds == 0) & (y_true_group == 0))
                    fprs[group] = fp / (fp + tn) if (fp + tn) > 0 else 0
                
                # Check equalized odds constraints
                tpr_diff = abs(tprs[unique_groups[0]] - tprs[unique_groups[1]])
                fpr_diff = abs(fprs[unique_groups[0]] - fprs[unique_groups[1]])
                
                if tpr_diff <= self.constraint_slack and fpr_diff <= self.constraint_slack:
                    # Calculate accuracy
                    preds = np.zeros(len(y_true), dtype=int)
                    for group in unique_groups:
                        mask = sensitive_features == group
                        preds[mask] = (y_proba[mask] >= thresholds[group]).astype(int)
                    
                    accuracy = np.mean(preds == y_true)
                    
                    if accuracy > best_score:
                        best_score = accuracy
                        best_thresholds = thresholds.copy()
        
        if not best_thresholds:
            logger.warning("No solution found, using 0.5")
            best_thresholds = {g: 0.5 for g in unique_groups}
        
        return best_thresholds
    
    def _optimize_accuracy(self,
                          y_true: np.ndarray,
                          y_proba: np.ndarray,
                          sensitive_features: np.ndarray,
                          unique_groups: np.ndarray) -> Dict[int, float]:
        """Optimize for maximum accuracy with minimal fairness constraint"""
        
        # For each group, find threshold that maximizes group-specific accuracy
        best_thresholds = {}
        
        for group in unique_groups:
            mask = sensitive_features == group
            y_true_group = y_true[mask]
            y_proba_group = y_proba[mask]
            
            # Try different thresholds
            thresholds_grid = np.linspace(0.0, 1.0, self.n_grid_points)
            best_acc = -1
            best_t = 0.5
            
            for t in thresholds_grid:
                preds = (y_proba_group >= t).astype(int)
                acc = np.mean(preds == y_true_group)
                
                if acc > best_acc:
                    best_acc = acc
                    best_t = t
            
            best_thresholds[group] = best_t
        
        return best_thresholds
    
    def evaluate(self,
                 y_true: np.ndarray,
                 y_proba: np.ndarray,
                 sensitive_features: np.ndarray) -> ThresholdOptimizationResult:
        """
        Evaluate threshold optimization results.
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            sensitive_features: Protected attributes
            
        Returns:
            ThresholdOptimizationResult with metrics
        """
        if not self.is_fitted_:
            raise ValueError("Optimizer must be fitted before evaluation")
        
        # Original predictions (threshold = 0.5)
        y_pred_original = (y_proba >= 0.5).astype(int)
        original_acc = float(np.mean(y_pred_original == y_true))
        
        # Optimized predictions
        y_pred_optimized = self.predict(y_proba, sensitive_features)
        optimized_acc = float(np.mean(y_pred_optimized == y_true))
        
        # Calculate fairness improvement
        unique_groups = np.unique(sensitive_features)
        
        # Original metrics
        orig_pos_rates = {}
        for group in unique_groups:
            mask = sensitive_features == group
            orig_pos_rates[group] = np.mean(y_pred_original[mask])
        
        orig_dp_diff = abs(orig_pos_rates[unique_groups[0]] - orig_pos_rates[unique_groups[1]])
        
        # Optimized metrics
        opt_pos_rates = {}
        for group in unique_groups:
            mask = sensitive_features == group
            opt_pos_rates[group] = np.mean(y_pred_optimized[mask])
        
        opt_dp_diff = abs(opt_pos_rates[unique_groups[0]] - opt_pos_rates[unique_groups[1]])
        
        fairness_improvement = {
            'demographic_parity_before': float(orig_dp_diff),
            'demographic_parity_after': float(opt_dp_diff),
            'improvement': float(orig_dp_diff - opt_dp_diff)
        }
        
        return ThresholdOptimizationResult(
            group_thresholds=self.group_thresholds_,
            objective=self.objective.value,
            original_accuracy=original_acc,
            optimized_accuracy=optimized_acc,
            fairness_improvement=fairness_improvement,
            metadata={
                'constraint_slack': self.constraint_slack,
                'n_grid_points': self.n_grid_points,
                'n_groups': len(unique_groups)
            }
        )


def main():
    """Test threshold optimizer"""
    print("🧪 Testing Threshold Optimizer")
    
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    
    # Create test data
    X, y = make_classification(
        n_samples=1000, n_features=20, n_classes=2, random_state=42
    )
    protected_attr = np.random.choice([0, 1], size=1000, p=[0.7, 0.3])
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    protected_train = protected_attr[:len(X_train)]
    protected_test = protected_attr[len(X_train):]
    
    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Optimize thresholds
    print("\n✅ Optimizing for Equal Opportunity...")
    optimizer = ThresholdOptimizer(
        objective=OptimizationObjective.EQUAL_OPPORTUNITY,
        constraint_slack=0.05
    )
    
    optimizer.fit(y_test, y_proba, protected_test)
    result = optimizer.evaluate(y_test, y_proba, protected_test)
    
    print(f"   Thresholds: {result.group_thresholds}")
    print(f"   Original accuracy: {result.original_accuracy:.3f}")
    print(f"   Optimized accuracy: {result.optimized_accuracy:.3f}")
    print(f"   Fairness improvement: {result.fairness_improvement}")
    
    print("\n✅ Threshold optimizer test complete!")


if __name__ == '__main__':
    main()
