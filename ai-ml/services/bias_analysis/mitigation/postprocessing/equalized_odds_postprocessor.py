"""
Equalized Odds Post-processing for Bias Mitigation.

This module implements post-processing techniques to achieve equalized odds,
primarily using Fairlearn's ThresholdOptimizer and custom implementations.
"""

import numpy as np
from typing import Dict, Optional, List, Tuple, Any
from dataclasses import dataclass, field
from fairlearn.postprocessing import ThresholdOptimizer as FairlearnThresholdOptimizer
from sklearn.base import BaseEstimator, ClassifierMixin
import logging

logger = logging.getLogger(__name__)


@dataclass
class EOPostprocessingResult:
    """Result of equalized odds post-processing"""
    method: str
    postprocessor: Any
    original_metrics: Dict[str, float]
    postprocessed_metrics: Dict[str, float]
    fairness_improvement: Dict[str, float]
    group_specific_metrics: Dict[str, Dict[str, float]]
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'method': self.method,
            'original_metrics': {k: float(v) for k, v in self.original_metrics.items()},
            'postprocessed_metrics': {k: float(v) for k, v in self.postprocessed_metrics.items()},
            'fairness_improvement': {k: float(v) for k, v in self.fairness_improvement.items()},
            'group_specific_metrics': {
                str(g): {k: float(v) for k, v in metrics.items()}
                for g, metrics in self.group_specific_metrics.items()
            },
            'metadata': self.metadata
        }


class EqualizedOddsPostprocessor:
    """
    Post-processing to achieve equalized odds fairness.
    
    Wraps Fairlearn's ThresholdOptimizer and provides additional
    equalized odds post-processing techniques:
    - Equalized Odds: Equal TPR and FPR across groups
    - Equal Opportunity: Equal TPR across groups
    - Demographic Parity: Equal positive prediction rates
    
    The postprocessor adjusts predictions to satisfy fairness constraints
    while maintaining reasonable accuracy.
    """
    
    def __init__(self,
                 constraint: str = "equalized_odds",
                 objective: str = "accuracy_score",
                 grid_size: int = 100,
                 flip: bool = True,
                 predict_method: str = "auto"):
        """
        Initialize equalized odds postprocessor.
        
        Args:
            constraint: Fairness constraint ("equalized_odds", "equal_opportunity", 
                       "demographic_parity")
            objective: Optimization objective (e.g., "accuracy_score")
            grid_size: Number of grid points for threshold search
            flip: Whether to allow prediction flipping
            predict_method: Prediction method ("auto", "randomized", "threshold")
        """
        self.constraint = constraint
        self.objective = objective
        self.grid_size = grid_size
        self.flip = flip
        self.predict_method = predict_method
        self.postprocessor_: Optional[FairlearnThresholdOptimizer] = None
        self.groups_: Optional[np.ndarray] = None
        
    def fit(self,
            estimator: BaseEstimator,
            X: np.ndarray,
            y_true: np.ndarray,
            sensitive_features: np.ndarray) -> 'EqualizedOddsPostprocessor':
        """
        Fit the post-processor to achieve equalized odds.
        
        Args:
            estimator: Pre-trained classifier
            X: Training features
            y_true: True labels
            sensitive_features: Protected group memberships
            
        Returns:
            self
        """
        y_true = np.asarray(y_true)
        sensitive_features = np.asarray(sensitive_features)
        self.groups_ = np.unique(sensitive_features)
        
        # Create Fairlearn ThresholdOptimizer
        self.postprocessor_ = FairlearnThresholdOptimizer(
            estimator=estimator,
            constraints=self.constraint,
            objective=self.objective,
            grid_size=self.grid_size,
            flip=self.flip,
            predict_method=self.predict_method
        )
        
        # Fit the postprocessor
        self.postprocessor_.fit(X, y_true, sensitive_features=sensitive_features)
        
        return self
    
    def predict(self,
                X: np.ndarray,
                sensitive_features: np.ndarray,
                random_state: Optional[int] = None) -> np.ndarray:
        """
        Make predictions using the post-processor.
        
        Args:
            X: Features to predict on
            sensitive_features: Protected group memberships
            random_state: Random state for randomized predictions
            
        Returns:
            Post-processed predictions
        """
        if self.postprocessor_ is None:
            raise ValueError("Postprocessor not fitted. Call fit() first.")
        
        sensitive_features = np.asarray(sensitive_features)
        
        # Make predictions using the postprocessor
        if random_state is not None:
            np.random.seed(random_state)
        
        predictions = self.postprocessor_.predict(
            X,
            sensitive_features=sensitive_features,
            random_state=random_state
        )
        
        return predictions
    
    def predict_proba(self,
                      estimator: BaseEstimator,
                      X: np.ndarray,
                      sensitive_features: np.ndarray) -> np.ndarray:
        """
        Get probability estimates (from base estimator).
        
        Args:
            estimator: Base estimator
            X: Features
            sensitive_features: Protected group memberships
            
        Returns:
            Probability estimates
        """
        if hasattr(estimator, 'predict_proba'):
            return estimator.predict_proba(X)
        else:
            # Convert binary predictions to probabilities
            predictions = estimator.predict(X)
            proba = np.zeros((len(predictions), 2))
            proba[predictions == 0, 0] = 1.0
            proba[predictions == 1, 1] = 1.0
            return proba
    
    def evaluate(self,
                 X: np.ndarray,
                 y_true: np.ndarray,
                 sensitive_features: np.ndarray,
                 estimator: BaseEstimator,
                 random_state: Optional[int] = None) -> EOPostprocessingResult:
        """
        Evaluate post-processing results.
        
        Args:
            X: Features
            y_true: True labels
            sensitive_features: Protected group memberships
            estimator: Original estimator (for baseline comparison)
            random_state: Random state for predictions
            
        Returns:
            EOPostprocessingResult with evaluation metrics
        """
        y_true = np.asarray(y_true)
        sensitive_features = np.asarray(sensitive_features)
        
        # Get original predictions
        y_pred_original = estimator.predict(X)
        
        # Get post-processed predictions
        y_pred_postprocessed = self.predict(X, sensitive_features, random_state)
        
        # Compute metrics
        original_metrics = self._compute_metrics(y_true, y_pred_original, sensitive_features)
        postprocessed_metrics = self._compute_metrics(y_true, y_pred_postprocessed, sensitive_features)
        
        # Compute group-specific metrics
        group_specific_metrics = {}
        for group in self.groups_:
            group_mask = sensitive_features == group
            if np.sum(group_mask) == 0:
                continue
            
            group_metrics = self._compute_group_metrics(
                y_true[group_mask],
                y_pred_postprocessed[group_mask]
            )
            group_specific_metrics[f"group_{group}"] = group_metrics
        
        # Compute fairness improvement
        fairness_improvement = self._compute_fairness_improvement(
            original_metrics,
            postprocessed_metrics
        )
        
        return EOPostprocessingResult(
            method=f"equalized_odds_{self.constraint}",
            postprocessor=self.postprocessor_,
            original_metrics=original_metrics,
            postprocessed_metrics=postprocessed_metrics,
            fairness_improvement=fairness_improvement,
            group_specific_metrics=group_specific_metrics,
            metadata={
                'constraint': self.constraint,
                'objective': self.objective,
                'grid_size': self.grid_size,
                'n_groups': len(self.groups_)
            }
        )
    
    def _compute_metrics(self,
                         y_true: np.ndarray,
                         y_pred: np.ndarray,
                         sensitive_features: np.ndarray) -> Dict[str, float]:
        """Compute overall and fairness metrics"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0)
        }
        
        # Compute per-group TPR and FPR
        tprs = []
        fprs = []
        positive_rates = []
        
        for group in self.groups_:
            group_mask = sensitive_features == group
            if np.sum(group_mask) == 0:
                continue
            
            y_true_group = y_true[group_mask]
            y_pred_group = y_pred[group_mask]
            
            # TPR (True Positive Rate)
            positives = np.sum(y_true_group == 1)
            if positives > 0:
                tpr = np.sum((y_pred_group == 1) & (y_true_group == 1)) / positives
                tprs.append(tpr)
            
            # FPR (False Positive Rate)
            negatives = np.sum(y_true_group == 0)
            if negatives > 0:
                fpr = np.sum((y_pred_group == 1) & (y_true_group == 0)) / negatives
                fprs.append(fpr)
            
            # Positive prediction rate
            positive_rate = np.mean(y_pred_group == 1)
            positive_rates.append(positive_rate)
        
        # Fairness metrics
        if tprs:
            metrics['tpr_disparity'] = max(tprs) - min(tprs)
            metrics['tpr_ratio'] = min(tprs) / (max(tprs) + 1e-7)
        
        if fprs:
            metrics['fpr_disparity'] = max(fprs) - min(fprs)
            metrics['fpr_ratio'] = min(fprs) / (max(fprs) + 1e-7)
        
        if positive_rates:
            metrics['positive_rate_disparity'] = max(positive_rates) - min(positive_rates)
            metrics['positive_rate_ratio'] = min(positive_rates) / (max(positive_rates) + 1e-7)
        
        return metrics
    
    def _compute_group_metrics(self,
                               y_true: np.ndarray,
                               y_pred: np.ndarray) -> Dict[str, float]:
        """Compute metrics for a single group"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        
        # Compute confusion matrix components
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        tn = np.sum((y_pred == 0) & (y_true == 0))
        fn = np.sum((y_pred == 0) & (y_true == 1))
        
        # TPR and FPR
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'tpr': tpr,
            'fpr': fpr,
            'positive_rate': np.mean(y_pred == 1)
        }
    
    def _compute_fairness_improvement(self,
                                      original_metrics: Dict[str, float],
                                      postprocessed_metrics: Dict[str, float]) -> Dict[str, float]:
        """Compute improvement in fairness metrics"""
        improvement = {}
        
        # TPR disparity improvement
        if 'tpr_disparity' in original_metrics and 'tpr_disparity' in postprocessed_metrics:
            improvement['tpr_disparity_reduction'] = (
                original_metrics['tpr_disparity'] - postprocessed_metrics['tpr_disparity']
            )
        
        # FPR disparity improvement
        if 'fpr_disparity' in original_metrics and 'fpr_disparity' in postprocessed_metrics:
            improvement['fpr_disparity_reduction'] = (
                original_metrics['fpr_disparity'] - postprocessed_metrics['fpr_disparity']
            )
        
        # Positive rate disparity improvement
        if 'positive_rate_disparity' in original_metrics and 'positive_rate_disparity' in postprocessed_metrics:
            improvement['positive_rate_disparity_reduction'] = (
                original_metrics['positive_rate_disparity'] - 
                postprocessed_metrics['positive_rate_disparity']
            )
        
        # Accuracy change
        if 'accuracy' in original_metrics and 'accuracy' in postprocessed_metrics:
            improvement['accuracy_change'] = (
                postprocessed_metrics['accuracy'] - original_metrics['accuracy']
            )
        
        return improvement


if __name__ == "__main__":
    # Test equalized odds post-processing
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    
    print("="*60)
    print("Testing Equalized Odds Post-processing")
    print("="*60)
    
    # Generate test data with bias
    np.random.seed(42)
    X, y = make_classification(n_samples=2000, n_features=20, 
                               n_informative=15, n_redundant=5,
                               random_state=42)
    
    # Create biased sensitive features
    sensitive = np.random.choice([0, 1], size=2000, p=[0.7, 0.3])
    
    # Introduce bias: group 1 has lower positive labels
    y[sensitive == 1] = np.random.choice([0, 1], size=np.sum(sensitive == 1), p=[0.7, 0.3])
    
    # Split data
    X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
        X, y, sensitive, test_size=0.3, random_state=42
    )
    
    # Train baseline model
    print("\nTraining baseline model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Test each constraint
    constraints = ["equalized_odds", "equal_opportunity", "demographic_parity"]
    
    for constraint in constraints:
        print(f"\n{'-'*60}")
        print(f"Testing constraint: {constraint}")
        print('-'*60)
        
        try:
            # Create and fit postprocessor
            postprocessor = EqualizedOddsPostprocessor(
                constraint=constraint,
                objective="accuracy_score",
                grid_size=50,
                predict_method="auto"
            )
            
            postprocessor.fit(model, X_train, y_train, s_train)
            
            # Evaluate
            result = postprocessor.evaluate(X_test, y_test, s_test, model, random_state=42)
            
            print(f"\nOriginal Metrics:")
            print(f"  Accuracy: {result.original_metrics['accuracy']:.4f}")
            if 'tpr_disparity' in result.original_metrics:
                print(f"  TPR Disparity: {result.original_metrics['tpr_disparity']:.4f}")
            if 'fpr_disparity' in result.original_metrics:
                print(f"  FPR Disparity: {result.original_metrics['fpr_disparity']:.4f}")
            if 'positive_rate_disparity' in result.original_metrics:
                print(f"  Positive Rate Disparity: {result.original_metrics['positive_rate_disparity']:.4f}")
            
            print(f"\nPost-processed Metrics:")
            print(f"  Accuracy: {result.postprocessed_metrics['accuracy']:.4f}")
            if 'tpr_disparity' in result.postprocessed_metrics:
                print(f"  TPR Disparity: {result.postprocessed_metrics['tpr_disparity']:.4f}")
            if 'fpr_disparity' in result.postprocessed_metrics:
                print(f"  FPR Disparity: {result.postprocessed_metrics['fpr_disparity']:.4f}")
            if 'positive_rate_disparity' in result.postprocessed_metrics:
                print(f"  Positive Rate Disparity: {result.postprocessed_metrics['positive_rate_disparity']:.4f}")
            
            print(f"\nFairness Improvement:")
            for metric, value in result.fairness_improvement.items():
                print(f"  {metric}: {value:.4f}")
            
            print(f"\nGroup-Specific Metrics:")
            for group, metrics in result.group_specific_metrics.items():
                print(f"  {group}:")
                print(f"    Accuracy: {metrics['accuracy']:.4f}")
                print(f"    TPR: {metrics['tpr']:.4f}")
                print(f"    FPR: {metrics['fpr']:.4f}")
            
        except Exception as e:
            print(f"Error testing {constraint}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("Equalized odds post-processing tests completed!")
    print('='*60)
