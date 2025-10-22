#!/usr/bin/env python3
"""
REGIQ AI/ML - Model Wrapper
Unified interface for different model types (scikit-learn, XGBoost, etc.).
"""

import logging
import numpy as np
from typing import Any, Optional, Union
from dataclasses import dataclass


logger = logging.getLogger("model_wrapper")


@dataclass
class ModelMetadata:
    """Metadata about a wrapped model."""
    model_type: str  # 'sklearn', 'xgboost', 'pytorch', 'tensorflow'
    has_predict_proba: bool
    has_feature_importances: bool
    n_features: Optional[int] = None
    classes: Optional[list] = None


class ModelWrapper:
    """
    Unified wrapper for different model types.
    
    Provides consistent interface for:
    - Training
    - Prediction
    - Probability estimation
    - Feature importance extraction
    
    Supports:
    - scikit-learn models
    - XGBoost
    - LightGBM
    - Basic PyTorch models (via wrapper)
    """
    
    def __init__(self, model: Any):
        """
        Initialize model wrapper.
        
        Args:
            model: ML model instance
        """
        self.model = model
        self.logger = logger
        self.metadata = self._detect_model_type()
    
    def _detect_model_type(self) -> ModelMetadata:
        """Detect model type and capabilities."""
        model_class = self.model.__class__.__name__
        module = self.model.__class__.__module__
        
        # Detect type
        if 'sklearn' in module:
            model_type = 'sklearn'
        elif 'xgboost' in module:
            model_type = 'xgboost'
        elif 'lightgbm' in module:
            model_type = 'lightgbm'
        elif 'torch' in module:
            model_type = 'pytorch'
        elif 'tensorflow' in module or 'keras' in module:
            model_type = 'tensorflow'
        else:
            model_type = 'unknown'
        
        # Check capabilities
        has_predict_proba = hasattr(self.model, 'predict_proba')
        has_feature_importances = hasattr(self.model, 'feature_importances_')
        
        # Get attributes if available
        n_features = getattr(self.model, 'n_features_in_', None)
        classes = getattr(self.model, 'classes_', None)
        
        return ModelMetadata(
            model_type=model_type,
            has_predict_proba=has_predict_proba,
            has_feature_importances=has_feature_importances,
            n_features=n_features,
            classes=classes.tolist() if classes is not None and hasattr(classes, 'tolist') else classes
        )
    
    def fit(self, X: np.ndarray, y: np.ndarray, sample_weight: Optional[np.ndarray] = None) -> 'ModelWrapper':
        """
        Train the model.
        
        Args:
            X: Features
            y: Labels
            sample_weight: Optional sample weights
            
        Returns:
            Self for chaining
        """
        try:
            if sample_weight is not None and self._supports_sample_weight():
                self.model.fit(X, y, sample_weight=sample_weight)
            else:
                self.model.fit(X, y)
            
            # Update metadata after fitting
            self.metadata = self._detect_model_type()
            
            return self
            
        except Exception as e:
            self.logger.error(f"Model fitting failed: {e}")
            raise
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Features
            
        Returns:
            Predictions
        """
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict probabilities.
        
        Args:
            X: Features
            
        Returns:
            Class probabilities
        """
        if not self.metadata.has_predict_proba:
            raise ValueError(f"Model type '{self.metadata.model_type}' does not support probability predictions")
        
        return self.model.predict_proba(X)
    
    def get_feature_importances(self) -> Optional[np.ndarray]:
        """
        Get feature importances if available.
        
        Returns:
            Feature importances or None
        """
        if self.metadata.has_feature_importances:
            return self.model.feature_importances_
        return None
    
    def _supports_sample_weight(self) -> bool:
        """Check if model supports sample_weight parameter."""
        # Most sklearn models support it
        if self.metadata.model_type in ['sklearn', 'xgboost', 'lightgbm']:
            return True
        return False
    
    def clone(self) -> 'ModelWrapper':
        """
        Clone the model.
        
        Returns:
            New ModelWrapper with cloned model
        """
        try:
            if self.metadata.model_type == 'sklearn':
                from sklearn.base import clone
                cloned_model = clone(self.model)
            elif self.metadata.model_type == 'xgboost':
                # XGBoost models need to be recreated
                import copy
                cloned_model = copy.deepcopy(self.model)
            else:
                import copy
                cloned_model = copy.deepcopy(self.model)
            
            return ModelWrapper(cloned_model)
            
        except Exception as e:
            self.logger.error(f"Model cloning failed: {e}")
            raise
    
    def get_params(self) -> dict:
        """Get model parameters."""
        if hasattr(self.model, 'get_params'):
            return self.model.get_params()
        return {}
    
    def set_params(self, **params) -> 'ModelWrapper':
        """Set model parameters."""
        if hasattr(self.model, 'set_params'):
            self.model.set_params(**params)
        return self


def main():
    """Test the model wrapper."""
    print("🧪 Testing Model Wrapper")
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    
    # Create test data
    X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
    
    # Create model
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    
    # Wrap model
    wrapper = ModelWrapper(model)
    
    print(f"✅ Model type: {wrapper.metadata.model_type}")
    print(f"✅ Has predict_proba: {wrapper.metadata.has_predict_proba}")
    print(f"✅ Has feature importances: {wrapper.metadata.has_feature_importances}")
    
    # Test fitting
    wrapper.fit(X[:800], y[:800])
    print("✅ Model fitted successfully")
    
    # Test prediction
    preds = wrapper.predict(X[800:])
    print(f"✅ Predictions shape: {preds.shape}")
    
    # Test probability prediction
    proba = wrapper.predict_proba(X[800:])
    print(f"✅ Probabilities shape: {proba.shape}")
    
    # Test feature importances
    importances = wrapper.get_feature_importances()
    if importances is not None:
        print(f"✅ Feature importances shape: {importances.shape}")
    else:
        print("✅ No feature importances available")
    
    # Test cloning
    cloned = wrapper.clone()
    print(f"✅ Model cloned: {cloned.metadata.model_type}")


if __name__ == "__main__":
    main()
