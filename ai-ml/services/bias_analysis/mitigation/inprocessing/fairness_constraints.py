"""
Fairness-constrained classification using Fairlearn.

Implements fairness constraints during model training to ensure
demographic parity, equalized odds, or other fairness criteria.

Author: REGIQ AI/ML Team
Phase: 3.5.2 - In-processing Mitigation
"""

import numpy as np
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass
from enum import Enum
import logging

from fairlearn.reductions import (
    ExponentiatedGradient,
    GridSearch,
    DemographicParity,
    EqualizedOdds,
    ErrorRateParity,
    TruePositiveRateParity,
    FalsePositiveRateParity
)
from sklearn.base import BaseEstimator, ClassifierMixin

logger = logging.getLogger(__name__)


class ConstraintType(Enum):
    """Types of fairness constraints"""
    DEMOGRAPHIC_PARITY = "demographic_parity"
    EQUALIZED_ODDS = "equalized_odds"
    ERROR_RATE_PARITY = "error_rate_parity"
    TRUE_POSITIVE_RATE_PARITY = "true_positive_rate_parity"
    FALSE_POSITIVE_RATE_PARITY = "false_positive_rate_parity"


class OptimizationAlgorithm(Enum):
    """Optimization algorithms for fairness constraints"""
    EXPONENTIATED_GRADIENT = "exponentiated_gradient"
    GRID_SEARCH = "grid_search"


@dataclass
class ConstrainedTrainingResult:
    """Result of fairness-constrained training"""
    fitted_model: Any
    constraint_type: str
    algorithm: str
    n_iterations: int
    best_gap: float
    weights: Optional[np.ndarray]
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'constraint_type': self.constraint_type,
            'algorithm': self.algorithm,
            'n_iterations': self.n_iterations,
            'best_gap': float(self.best_gap),
            'has_weights': self.weights is not None,
            'metadata': self.metadata
        }


class FairnessConstrainedClassifier(BaseEstimator, ClassifierMixin):
    """
    Train classifier with fairness constraints using Fairlearn.
    
    Supports multiple fairness constraints and optimization algorithms:
    - Demographic Parity: Equal selection rates across groups
    - Equalized Odds: Equal TPR and FPR across groups
    - Error Rate Parity: Equal error rates across groups
    
    Algorithms:
    - Exponentiated Gradient: Fast iterative optimization
    - Grid Search: Exhaustive search over constraint space
    """
    
    def __init__(self,
                 base_estimator: BaseEstimator,
                 constraint: ConstraintType = ConstraintType.DEMOGRAPHIC_PARITY,
                 algorithm: OptimizationAlgorithm = OptimizationAlgorithm.EXPONENTIATED_GRADIENT,
                 eps: float = 0.01,
                 max_iter: int = 50,
                 nu: Optional[float] = None,
                 eta0: float = 2.0,
                 grid_size: int = 10):
        """
        Initialize fairness-constrained classifier.
        
        Args:
            base_estimator: Base ML estimator (e.g., LogisticRegression)
            constraint: Fairness constraint type
            algorithm: Optimization algorithm to use
            eps: Tolerance for constraint violation (lower = stricter)
            max_iter: Maximum iterations for exponentiated gradient
            nu: Learning rate for exponentiated gradient (None = auto)
            eta0: Initial step size for exponentiated gradient
            grid_size: Number of points in grid for grid search
        """
        self.base_estimator = base_estimator
        self.constraint = constraint
        self.algorithm = algorithm
        self.eps = eps
        self.max_iter = max_iter
        self.nu = nu
        self.eta0 = eta0
        self.grid_size = grid_size
        
        self.mitigator_ = None
        self.is_fitted_ = False
        self.training_result_: Optional[ConstrainedTrainingResult] = None
    
    def fit(self, X: np.ndarray, y: np.ndarray, 
            sensitive_features: np.ndarray,
            sample_weight: Optional[np.ndarray] = None) -> 'FairnessConstrainedClassifier':
        """
        Train model with fairness constraints.
        
        Args:
            X: Training features
            y: Training labels
            sensitive_features: Protected attributes
            sample_weight: Optional sample weights
            
        Returns:
            self
        """
        logger.info(
            f"Training with {self.constraint.value} constraint "
            f"using {self.algorithm.value} algorithm"
        )
        
        # Create constraint object
        constraint_obj = self._create_constraint()
        
        # Create and configure mitigator
        if self.algorithm == OptimizationAlgorithm.EXPONENTIATED_GRADIENT:
            self.mitigator_ = ExponentiatedGradient(
                estimator=self.base_estimator,
                constraints=constraint_obj,
                eps=self.eps,
                max_iter=self.max_iter,
                nu=self.nu,
                eta0=self.eta0
            )
        else:  # GRID_SEARCH
            self.mitigator_ = GridSearch(
                estimator=self.base_estimator,
                constraints=constraint_obj,
                grid_size=self.grid_size
            )
        
        # Fit mitigator
        if sample_weight is not None:
            self.mitigator_.fit(
                X, y, 
                sensitive_features=sensitive_features,
                sample_weight=sample_weight
            )
        else:
            self.mitigator_.fit(
                X, y,
                sensitive_features=sensitive_features
            )
        
        # Extract training results
        n_iterations = getattr(self.mitigator_, 'n_oracle_calls_', 0)
        best_gap = getattr(self.mitigator_, 'best_gap_', 0.0)
        
        self.training_result_ = ConstrainedTrainingResult(
            fitted_model=self.mitigator_,
            constraint_type=self.constraint.value,
            algorithm=self.algorithm.value,
            n_iterations=n_iterations,
            best_gap=best_gap,
            weights=sample_weight,
            metadata={
                'eps': self.eps,
                'max_iter': self.max_iter,
                'grid_size': self.grid_size if self.algorithm == OptimizationAlgorithm.GRID_SEARCH else None
            }
        )
        
        self.is_fitted_ = True
        logger.info(
            f"Training complete. Iterations: {n_iterations}, "
            f"Constraint gap: {best_gap:.6f}"
        )
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions with fair model"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted before prediction")
        
        return self.mitigator_.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict probabilities (if supported by base estimator)"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted before prediction")
        
        # Check if mitigator supports predict_proba
        if hasattr(self.mitigator_, 'predict_proba'):
            return self.mitigator_.predict_proba(X)
        else:
            raise ValueError("Base estimator does not support probability predictions")
    
    def _create_constraint(self):
        """Create Fairlearn constraint object"""
        if self.constraint == ConstraintType.DEMOGRAPHIC_PARITY:
            return DemographicParity()
        elif self.constraint == ConstraintType.EQUALIZED_ODDS:
            return EqualizedOdds()
        elif self.constraint == ConstraintType.ERROR_RATE_PARITY:
            return ErrorRateParity()
        elif self.constraint == ConstraintType.TRUE_POSITIVE_RATE_PARITY:
            return TruePositiveRateParity()
        elif self.constraint == ConstraintType.FALSE_POSITIVE_RATE_PARITY:
            return FalsePositiveRateParity()
        else:
            raise ValueError(f"Unknown constraint type: {self.constraint}")
    
    def get_training_summary(self) -> Dict:
        """Get summary of constrained training"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted first")
        
        summary = self.training_result_.to_dict()
        
        # Add model-specific info
        if hasattr(self.mitigator_, 'best_classifier_'):
            summary['has_best_classifier'] = True
        
        if hasattr(self.mitigator_, 'predictors_'):
            summary['n_predictors'] = len(self.mitigator_.predictors_)
        
        return summary
    
    def score(self, X: np.ndarray, y: np.ndarray, 
              sample_weight: Optional[np.ndarray] = None) -> float:
        """Calculate accuracy score"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted before scoring")
        
        predictions = self.predict(X)
        
        if sample_weight is not None:
            accuracy = np.average(predictions == y, weights=sample_weight)
        else:
            accuracy = np.mean(predictions == y)
        
        return float(accuracy)


def create_fair_classifier(
    base_estimator: BaseEstimator,
    constraint_type: Literal['demographic_parity', 'equalized_odds', 'error_rate_parity'] = 'demographic_parity',
    algorithm: Literal['exponentiated_gradient', 'grid_search'] = 'exponentiated_gradient',
    **kwargs
) -> FairnessConstrainedClassifier:
    """
    Factory function to create fairness-constrained classifier.
    
    Args:
        base_estimator: Base ML estimator
        constraint_type: Type of fairness constraint
        algorithm: Optimization algorithm
        **kwargs: Additional parameters for FairnessConstrainedClassifier
        
    Returns:
        Configured FairnessConstrainedClassifier
        
    Example:
        >>> from sklearn.linear_model import LogisticRegression
        >>> base = LogisticRegression()
        >>> fair_clf = create_fair_classifier(
        ...     base, 
        ...     constraint_type='demographic_parity',
        ...     eps=0.01
        ... )
        >>> fair_clf.fit(X_train, y_train, sensitive_features=protected_attr)
    """
    # Convert string to enum
    constraint_enum = ConstraintType(constraint_type)
    algorithm_enum = OptimizationAlgorithm(algorithm)
    
    return FairnessConstrainedClassifier(
        base_estimator=base_estimator,
        constraint=constraint_enum,
        algorithm=algorithm_enum,
        **kwargs
    )


def main():
    """Test fairness-constrained classifier"""
    print("🧪 Testing Fairness-Constrained Classifier")
    
    from sklearn.linear_model import LogisticRegression
    from sklearn.datasets import make_classification
    
    # Create test data
    X, y = make_classification(
        n_samples=1000, n_features=20, n_classes=2, random_state=42
    )
    
    # Create biased protected attribute
    protected_attr = np.random.choice([0, 1], size=1000, p=[0.7, 0.3])
    
    # Create fair classifier
    base_estimator = LogisticRegression(max_iter=1000)
    fair_clf = FairnessConstrainedClassifier(
        base_estimator=base_estimator,
        constraint=ConstraintType.DEMOGRAPHIC_PARITY,
        algorithm=OptimizationAlgorithm.EXPONENTIATED_GRADIENT,
        eps=0.01,
        max_iter=50
    )
    
    # Train
    print("\n✅ Training with demographic parity constraint...")
    fair_clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
    
    # Evaluate
    accuracy = fair_clf.score(X[800:], y[800:])
    print(f"✅ Test accuracy: {accuracy:.3f}")
    
    # Get summary
    summary = fair_clf.get_training_summary()
    print(f"✅ Training summary: {summary}")
    
    print("\n✅ Fairness-constrained classifier test complete!")


if __name__ == '__main__':
    main()
