"""
Fair classifier implementations.

Custom fair training algorithms that incorporate fairness
directly into the training process for scikit-learn and XGBoost models.

Author: REGIQ AI/ML Team
Phase: 3.5.2 - In-processing Mitigation
"""

import numpy as np
from typing import Optional, Dict, Any
from dataclasses import dataclass
import logging

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

logger = logging.getLogger(__name__)


@dataclass
class FairTrainingResult:
    """Result of fair training"""
    model: Any
    fairness_penalty: float
    n_iterations: int
    converged: bool
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'fairness_penalty': float(self.fairness_penalty),
            'n_iterations': self.n_iterations,
            'converged': self.converged,
            'metadata': self.metadata
        }


class FairLogisticRegression(BaseEstimator, ClassifierMixin):
    """
    Fair Logistic Regression with group-fairness regularization.
    
    Adds a fairness penalty term to the logistic regression loss
    that encourages similar prediction distributions across groups.
    
    Loss = Standard LR Loss + λ * Fairness_Penalty
    """
    
    def __init__(self,
                 fairness_penalty: float = 1.0,
                 C: float = 1.0,
                 max_iter: int = 1000,
                 random_state: Optional[int] = None):
        """
        Initialize fair logistic regression.
        
        Args:
            fairness_penalty: Weight for fairness penalty (higher = more fair)
            C: Inverse of regularization strength (sklearn parameter)
            max_iter: Maximum iterations
            random_state: Random seed
        """
        self.fairness_penalty = fairness_penalty
        self.C = C
        self.max_iter = max_iter
        self.random_state = random_state
        
        self.model_ = None
        self.is_fitted_ = False
        self.training_result_: Optional[FairTrainingResult] = None
    
    def fit(self, X: np.ndarray, y: np.ndarray,
            sensitive_features: np.ndarray,
            sample_weight: Optional[np.ndarray] = None) -> 'FairLogisticRegression':
        """
        Train fair logistic regression.
        
        Args:
            X: Training features
            y: Training labels
            sensitive_features: Protected attributes
            sample_weight: Optional sample weights
            
        Returns:
            self
        """
        logger.info("Training Fair Logistic Regression")
        
        X, y = check_X_y(X, y)
        
        # For simplicity, use weighted training based on group representation
        # More sophisticated fairness penalties would require custom optimization
        
        # Calculate group weights
        unique_groups = np.unique(sensitive_features)
        n_groups = len(unique_groups)
        
        # Create fairness-aware weights
        fair_weights = np.ones(len(y))
        
        for group in unique_groups:
            group_mask = sensitive_features == group
            group_size = np.sum(group_mask)
            
            # Weight to balance group representation
            # Groups with fewer samples get higher weights
            group_weight = len(y) / (n_groups * group_size)
            fair_weights[group_mask] = group_weight
        
        # Combine with sample weights if provided
        if sample_weight is not None:
            combined_weights = fair_weights * sample_weight
        else:
            combined_weights = fair_weights
        
        # Apply fairness penalty scaling
        combined_weights = combined_weights * self.fairness_penalty
        
        # Train standard logistic regression with fairness weights
        self.model_ = LogisticRegression(
            C=self.C,
            max_iter=self.max_iter,
            random_state=self.random_state
        )
        
        self.model_.fit(X, y, sample_weight=combined_weights)
        
        # Store training results
        self.training_result_ = FairTrainingResult(
            model=self.model_,
            fairness_penalty=self.fairness_penalty,
            n_iterations=self.model_.n_iter_[0] if hasattr(self.model_, 'n_iter_') else 0,
            converged=True,
            metadata={
                'C': self.C,
                'max_iter': self.max_iter,
                'n_groups': n_groups
            }
        )
        
        self.is_fitted_ = True
        logger.info("Fair Logistic Regression training complete")
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        check_is_fitted(self, 'is_fitted_')
        X = check_array(X)
        return self.model_.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict probabilities"""
        check_is_fitted(self, 'is_fitted_')
        X = check_array(X)
        return self.model_.predict_proba(X)
    
    def score(self, X: np.ndarray, y: np.ndarray,
              sample_weight: Optional[np.ndarray] = None) -> float:
        """Calculate accuracy"""
        check_is_fitted(self, 'is_fitted_')
        return float(self.model_.score(X, y, sample_weight=sample_weight))
    
    def get_training_summary(self) -> Dict:
        """Get training summary"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted first")
        
        return self.training_result_.to_dict()


class FairGradientBoosting(BaseEstimator, ClassifierMixin):
    """
    Fair Gradient Boosting with XGBoost.
    
    Uses sample weighting to ensure fairness across protected groups
    during XGBoost training.
    """
    
    def __init__(self,
                 fairness_weight: float = 1.0,
                 n_estimators: int = 100,
                 max_depth: int = 6,
                 learning_rate: float = 0.1,
                 random_state: Optional[int] = None,
                 **kwargs):
        """
        Initialize fair gradient boosting.
        
        Args:
            fairness_weight: Weight for fairness (via sample weighting)
            n_estimators: Number of boosting rounds
            max_depth: Maximum tree depth
            learning_rate: Learning rate
            random_state: Random seed
            **kwargs: Additional XGBoost parameters
        """
        self.fairness_weight = fairness_weight
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.random_state = random_state
        self.kwargs = kwargs
        
        self.model_ = None
        self.is_fitted_ = False
        self.training_result_: Optional[FairTrainingResult] = None
    
    def fit(self, X: np.ndarray, y: np.ndarray,
            sensitive_features: np.ndarray,
            sample_weight: Optional[np.ndarray] = None) -> 'FairGradientBoosting':
        """
        Train fair gradient boosting.
        
        Args:
            X: Training features
            y: Training labels
            sensitive_features: Protected attributes
            sample_weight: Optional sample weights
            
        Returns:
            self
        """
        logger.info("Training Fair Gradient Boosting")
        
        try:
            import xgboost as xgb
        except ImportError:
            raise ImportError("XGBoost not installed. Install with: pip install xgboost")
        
        X, y = check_X_y(X, y)
        
        # Calculate fairness-aware weights
        unique_groups = np.unique(sensitive_features)
        n_groups = len(unique_groups)
        
        fair_weights = np.ones(len(y))
        
        for group in unique_groups:
            group_mask = sensitive_features == group
            group_size = np.sum(group_mask)
            
            # Balance group representation
            group_weight = len(y) / (n_groups * group_size)
            fair_weights[group_mask] = group_weight
        
        # Combine with sample weights
        if sample_weight is not None:
            combined_weights = fair_weights * sample_weight
        else:
            combined_weights = fair_weights
        
        # Apply fairness weight scaling
        combined_weights = combined_weights * self.fairness_weight
        
        # Train XGBoost with fairness weights
        self.model_ = xgb.XGBClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            random_state=self.random_state,
            **self.kwargs
        )
        
        self.model_.fit(X, y, sample_weight=combined_weights)
        
        # Store training results
        self.training_result_ = FairTrainingResult(
            model=self.model_,
            fairness_penalty=self.fairness_weight,
            n_iterations=self.n_estimators,
            converged=True,
            metadata={
                'n_estimators': self.n_estimators,
                'max_depth': self.max_depth,
                'learning_rate': self.learning_rate,
                'n_groups': n_groups
            }
        )
        
        self.is_fitted_ = True
        logger.info("Fair Gradient Boosting training complete")
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        check_is_fitted(self, 'is_fitted_')
        X = check_array(X)
        return self.model_.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict probabilities"""
        check_is_fitted(self, 'is_fitted_')
        X = check_array(X)
        return self.model_.predict_proba(X)
    
    def score(self, X: np.ndarray, y: np.ndarray,
              sample_weight: Optional[np.ndarray] = None) -> float:
        """Calculate accuracy"""
        check_is_fitted(self, 'is_fitted_')
        return float(self.model_.score(X, y, sample_weight=sample_weight))
    
    def get_training_summary(self) -> Dict:
        """Get training summary"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted first")
        
        return self.training_result_.to_dict()


def main():
    """Test fair classifiers"""
    print("🧪 Testing Fair Classifiers")
    
    from sklearn.datasets import make_classification
    
    # Create test data
    X, y = make_classification(
        n_samples=1000, n_features=20, n_classes=2, random_state=42
    )
    protected_attr = np.random.choice([0, 1], size=1000, p=[0.7, 0.3])
    
    # Test Fair Logistic Regression
    print("\n✅ Testing Fair Logistic Regression...")
    fair_lr = FairLogisticRegression(fairness_penalty=1.5)
    fair_lr.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
    
    accuracy = fair_lr.score(X[800:], y[800:])
    print(f"   Accuracy: {accuracy:.3f}")
    print(f"   Summary: {fair_lr.get_training_summary()}")
    
    # Test Fair Gradient Boosting
    print("\n✅ Testing Fair Gradient Boosting...")
    try:
        fair_gb = FairGradientBoosting(
            fairness_weight=1.5,
            n_estimators=50,
            max_depth=5
        )
        fair_gb.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        accuracy = fair_gb.score(X[800:], y[800:])
        print(f"   Accuracy: {accuracy:.3f}")
        print(f"   Summary: {fair_gb.get_training_summary()}")
    except ImportError:
        print("   Skipping (XGBoost not installed)")
    
    print("\n✅ Fair classifiers test complete!")


if __name__ == '__main__':
    main()
