"""
Unified in-processing bias mitigation engine.

Provides high-level interface to all in-processing techniques with
automatic technique selection and comprehensive validation.

Author: REGIQ AI/ML Team
Phase: 3.5.2 - In-processing Mitigation
"""

import numpy as np
from typing import Optional, Dict, Literal, Any
from dataclasses import dataclass
import logging

from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from .fairness_constraints import (
    FairnessConstrainedClassifier,
    ConstraintType,
    OptimizationAlgorithm
)
from .adversarial_debiasing import AdversarialDebiaser
from .fair_classifiers import FairLogisticRegression, FairGradientBoosting

logger = logging.getLogger(__name__)


@dataclass
class InprocessingResult:
    """Result of in-processing bias mitigation"""
    technique: str
    fitted_model: Any
    training_details: Dict
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'technique': self.technique,
            'training_details': self.training_details,
            'metadata': self.metadata
        }


class InprocessingEngine:
    """
    Unified engine for in-processing bias mitigation.
    
    Supports:
    - Auto-technique selection based on data and model type
    - Fairness constraints (Fairlearn)
    - Adversarial debiasing (neural networks)
    - Fair classifiers (custom implementations)
    - Comprehensive validation
    """
    
    def __init__(self,
                 technique: Literal['auto', 'fairness_constraints', 
                                   'adversarial', 'fair_classifier'] = 'auto',
                 constraint_type: str = 'demographic_parity',
                 algorithm: str = 'exponentiated_gradient',
                 fairness_penalty: float = 1.0,
                 **kwargs):
        """
        Initialize in-processing engine.
        
        Args:
            technique: Mitigation technique ('auto' for automatic selection)
            constraint_type: For fairness_constraints ('demographic_parity', 'equalized_odds')
            algorithm: For fairness_constraints ('exponentiated_gradient', 'grid_search')
            fairness_penalty: Penalty weight for fairness
            **kwargs: Additional parameters for specific techniques
        """
        self.technique = technique
        self.constraint_type = constraint_type
        self.algorithm = algorithm
        self.fairness_penalty = fairness_penalty
        self.kwargs = kwargs
        
        self.selected_technique_: Optional[str] = None
        self.fitted_model_: Optional[Any] = None
        self.result_: Optional[InprocessingResult] = None
    
    def train_fair_model(self,
                        base_estimator: Optional[BaseEstimator],
                        X: np.ndarray,
                        y: np.ndarray,
                        sensitive_features: np.ndarray,
                        sample_weight: Optional[np.ndarray] = None) -> InprocessingResult:
        """
        Train model with in-processing bias mitigation.
        
        Args:
            base_estimator: Base ML estimator (None for auto-selection)
            X: Training features
            y: Training labels
            sensitive_features: Protected attributes
            sample_weight: Optional sample weights
            
        Returns:
            InprocessingResult with trained model and details
        """
        logger.info(f"Starting in-processing mitigation with technique: {self.technique}")
        
        # Auto-select technique if needed
        if self.technique == 'auto':
            self.selected_technique_ = self._select_technique(
                base_estimator, X, y, sensitive_features
            )
        else:
            self.selected_technique_ = self.technique
        
        logger.info(f"Using technique: {self.selected_technique_}")
        
        # Apply selected technique
        if self.selected_technique_ == 'fairness_constraints':
            result = self._apply_fairness_constraints(
                base_estimator, X, y, sensitive_features, sample_weight
            )
        elif self.selected_technique_ == 'adversarial':
            result = self._apply_adversarial_debiasing(
                X, y, sensitive_features
            )
        elif self.selected_technique_ == 'fair_classifier':
            result = self._apply_fair_classifier(
                base_estimator, X, y, sensitive_features, sample_weight
            )
        else:
            raise ValueError(f"Unknown technique: {self.selected_technique_}")
        
        self.fitted_model_ = result.fitted_model
        self.result_ = result
        
        logger.info("In-processing mitigation complete")
        
        return result
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions with trained fair model"""
        if self.fitted_model_ is None:
            raise ValueError("Model must be trained before prediction")
        
        return self.fitted_model_.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict probabilities with trained fair model"""
        if self.fitted_model_ is None:
            raise ValueError("Model must be trained before prediction")
        
        return self.fitted_model_.predict_proba(X)
    
    def _select_technique(self,
                         base_estimator: Optional[BaseEstimator],
                         X: np.ndarray,
                         y: np.ndarray,
                         sensitive_features: np.ndarray) -> str:
        """
        Auto-select best in-processing technique.
        
        Decision logic:
        1. If no base estimator & large dataset -> Adversarial debiasing
        2. If linear model (LR) -> Fair classifier
        3. If tree-based (RF, XGB) -> Fair classifier
        4. Default -> Fairness constraints (most versatile)
        """
        n_samples, n_features = X.shape
        
        # No estimator provided - use neural approach for large datasets
        if base_estimator is None:
            if n_samples > 5000 and n_features > 10:
                return 'adversarial'
            else:
                return 'fair_classifier'
        
        # Check estimator type
        estimator_name = base_estimator.__class__.__name__
        
        if 'Logistic' in estimator_name:
            return 'fair_classifier'
        elif 'XGB' in estimator_name or 'GradientBoosting' in estimator_name:
            return 'fair_classifier'
        elif 'RandomForest' in estimator_name or 'Tree' in estimator_name:
            return 'fairness_constraints'
        else:
            # Default to fairness constraints (works with any sklearn estimator)
            return 'fairness_constraints'
    
    def _apply_fairness_constraints(self,
                                    base_estimator: BaseEstimator,
                                    X: np.ndarray,
                                    y: np.ndarray,
                                    sensitive_features: np.ndarray,
                                    sample_weight: Optional[np.ndarray]) -> InprocessingResult:
        """Apply Fairlearn fairness constraints"""
        
        # Default estimator if none provided
        if base_estimator is None:
            base_estimator = LogisticRegression(max_iter=1000)
        
        # Create constrained classifier
        constraint_enum = ConstraintType(self.constraint_type)
        algorithm_enum = OptimizationAlgorithm(self.algorithm)
        
        fair_clf = FairnessConstrainedClassifier(
            base_estimator=base_estimator,
            constraint=constraint_enum,
            algorithm=algorithm_enum,
            eps=self.kwargs.get('eps', 0.01),
            max_iter=self.kwargs.get('max_iter', 50)
        )
        
        # Train
        fair_clf.fit(X, y, sensitive_features=sensitive_features, 
                    sample_weight=sample_weight)
        
        # Get training details
        training_details = fair_clf.get_training_summary()
        
        return InprocessingResult(
            technique='fairness_constraints',
            fitted_model=fair_clf,
            training_details=training_details,
            metadata={
                'constraint_type': self.constraint_type,
                'algorithm': self.algorithm,
                'base_estimator': base_estimator.__class__.__name__
            }
        )
    
    def _apply_adversarial_debiasing(self,
                                     X: np.ndarray,
                                     y: np.ndarray,
                                     sensitive_features: np.ndarray) -> InprocessingResult:
        """Apply adversarial debiasing"""
        
        n_features = X.shape[1]
        
        debiaser = AdversarialDebiaser(
            input_dim=n_features,
            classifier_hidden=self.kwargs.get('classifier_hidden', (64, 32)),
            adversary_hidden=self.kwargs.get('adversary_hidden', (32,)),
            adversary_loss_weight=self.fairness_penalty,
            n_epochs=self.kwargs.get('n_epochs', 50),
            batch_size=self.kwargs.get('batch_size', 64)
        )
        
        # Train
        debiaser.fit(X, y, protected_attr=sensitive_features)
        
        # Get training details
        training_details = debiaser.get_training_summary()
        
        return InprocessingResult(
            technique='adversarial',
            fitted_model=debiaser,
            training_details=training_details,
            metadata={
                'adversary_loss_weight': self.fairness_penalty,
                'input_dim': n_features
            }
        )
    
    def _apply_fair_classifier(self,
                               base_estimator: Optional[BaseEstimator],
                                X: np.ndarray,
                               y: np.ndarray,
                               sensitive_features: np.ndarray,
                               sample_weight: Optional[np.ndarray]) -> InprocessingResult:
        """Apply custom fair classifier"""
        
        # Determine which fair classifier to use
        if base_estimator is None:
            # Default to Fair Logistic Regression
            fair_model = FairLogisticRegression(
                fairness_penalty=self.fairness_penalty,
                max_iter=self.kwargs.get('max_iter', 1000)
            )
        elif 'Logistic' in base_estimator.__class__.__name__:
            fair_model = FairLogisticRegression(
                fairness_penalty=self.fairness_penalty,
                max_iter=self.kwargs.get('max_iter', 1000)
            )
        else:
            # Try Fair Gradient Boosting for tree-based models
            try:
                fair_model = FairGradientBoosting(
                    fairness_weight=self.fairness_penalty,
                    n_estimators=self.kwargs.get('n_estimators', 100),
                    max_depth=self.kwargs.get('max_depth', 6)
                )
            except ImportError:
                # Fallback to Fair LR if XGBoost not available
                fair_model = FairLogisticRegression(
                    fairness_penalty=self.fairness_penalty,
                    max_iter=self.kwargs.get('max_iter', 1000)
                )
        
        # Train
        fair_model.fit(X, y, sensitive_features=sensitive_features,
                      sample_weight=sample_weight)
        
        # Get training details
        training_details = fair_model.get_training_summary()
        
        return InprocessingResult(
            technique='fair_classifier',
            fitted_model=fair_model,
            training_details=training_details,
            metadata={
                'fairness_penalty': self.fairness_penalty,
                'model_type': fair_model.__class__.__name__
            }
        )
    
    def get_result_summary(self) -> Dict:
        """Get summary of in-processing results"""
        if self.result_ is None:
            raise ValueError("Model must be trained first")
        
        return self.result_.to_dict()


def main():
    """Test in-processing engine"""
    print("🧪 Testing In-processing Engine")
    
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    
    # Create test data
    X, y = make_classification(
        n_samples=1000, n_features=20, n_classes=2, random_state=42
    )
    protected_attr = np.random.choice([0, 1], size=1000, p=[0.7, 0.3])
    
    # Test auto-selection
    print("\n✅ Testing auto-selection...")
    engine = InprocessingEngine(technique='auto', fairness_penalty=1.0)
    
    base_est = LogisticRegression(max_iter=1000)
    result = engine.train_fair_model(
        base_est, X[:800], y[:800], protected_attr[:800]
    )
    
    print(f"   Selected technique: {engine.selected_technique_}")
    print(f"   Result: {result.to_dict()}")
    
    # Test prediction
    predictions = engine.predict(X[800:])
    accuracy = np.mean(predictions == y[800:])
    print(f"   Test accuracy: {accuracy:.3f}")
    
    print("\n✅ In-processing engine test complete!")


if __name__ == '__main__':
    main()
