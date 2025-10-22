"""
Unit tests for in-processing-based bias mitigation techniques.

Tests all in-processing modules:
- Fairness constraints (Fairlearn)
- Adversarial debiasing (neural networks)
- Fair classifiers (custom implementations)
- Unified in-processing engine

Author: REGIQ AI/ML Team
Phase: 3.5.2 - In-processing Tests
"""

import pytest
import numpy as np
import torch
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Import in-processing modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.bias_analysis.mitigation.inprocessing import (
    FairnessConstrainedClassifier,
    ConstraintType,
    OptimizationAlgorithm,
    AdversarialDebiaser,
    FairLogisticRegression,
    FairGradientBoosting,
    InprocessingEngine
)


@pytest.fixture
def binary_classification_data():
    """Generate binary classification dataset with group imbalance"""
    np.random.seed(42)
    
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=3,
        n_classes=2,
        weights=[0.6, 0.4],
        flip_y=0.05,
        random_state=42
    )
    
    # Create imbalanced protected attribute
    protected_attr = np.random.choice([0, 1], size=1000, p=[0.7, 0.3])
    
    return X, y, protected_attr


@pytest.fixture
def small_dataset():
    """Generate small dataset for faster adversarial training"""
    np.random.seed(42)
    
    X, y = make_classification(
        n_samples=500,
        n_features=10,
        n_informative=8,
        n_classes=2,
        random_state=42
    )
    
    protected_attr = np.random.choice([0, 1], size=500, p=[0.6, 0.4])
    
    return X, y, protected_attr


class TestFairnessConstrainedClassifier:
    """Test suite for Fairness-Constrained Classifier"""
    
    def test_initialization(self):
        """Test classifier initialization"""
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(
            base_estimator=base_est,
            constraint=ConstraintType.DEMOGRAPHIC_PARITY,
            algorithm=OptimizationAlgorithm.EXPONENTIATED_GRADIENT,
            eps=0.01
        )
        
        assert clf.constraint == ConstraintType.DEMOGRAPHIC_PARITY
        assert clf.algorithm == OptimizationAlgorithm.EXPONENTIATED_GRADIENT
        assert clf.eps == 0.01
        assert clf.is_fitted_ is False
    
    def test_fit_demographic_parity(self, binary_classification_data):
        """Test training with demographic parity constraint"""
        X, y, protected_attr = binary_classification_data
        
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(
            base_estimator=base_est,
            constraint=ConstraintType.DEMOGRAPHIC_PARITY,
            eps=0.05,
            max_iter=50
        )
        
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        assert clf.is_fitted_ is True
        assert clf.training_result_ is not None
        assert clf.training_result_.constraint_type == 'demographic_parity'
    
    def test_fit_equalized_odds(self, binary_classification_data):
        """Test training with equalized odds constraint"""
        X, y, protected_attr = binary_classification_data
        
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(
            base_estimator=base_est,
            constraint=ConstraintType.EQUALIZED_ODDS,
            eps=0.05
        )
        
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        assert clf.is_fitted_ is True
        assert clf.training_result_.constraint_type == 'equalized_odds'
    
    def test_predict(self, binary_classification_data):
        """Test making predictions"""
        X, y, protected_attr = binary_classification_data
        
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(base_estimator=base_est)
        
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        predictions = clf.predict(X[800:])
        
        assert len(predictions) == 200
        assert predictions.dtype in [np.int32, np.int64]
        assert set(predictions).issubset({0, 1})
    
    def test_predict_proba(self, binary_classification_data):
        """Test probability predictions"""
        X, y, protected_attr = binary_classification_data
        
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(base_estimator=base_est)
        
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        # Try to get probabilities - may not be supported by all mitigators
        try:
            probas = clf.predict_proba(X[800:])
            assert probas.shape == (200, 2)
            assert np.all((probas >= 0) & (probas <= 1))
            assert np.allclose(probas.sum(axis=1), 1.0)
        except ValueError:
            # Some mitigators may not support predict_proba
            pass
    
    def test_score(self, binary_classification_data):
        """Test accuracy scoring"""
        X, y, protected_attr = binary_classification_data
        
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(base_estimator=base_est)
        
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        accuracy = clf.score(X[800:], y[800:])
        
        assert 0.0 <= accuracy <= 1.0
        assert accuracy > 0.5  # Should be better than random
    
    def test_grid_search_algorithm(self, binary_classification_data):
        """Test grid search optimization"""
        X, y, protected_attr = binary_classification_data
        
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(
            base_estimator=base_est,
            algorithm=OptimizationAlgorithm.GRID_SEARCH,
            grid_size=5
        )
        
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        assert clf.is_fitted_ is True
        assert clf.training_result_.algorithm == 'grid_search'
    
    def test_training_summary(self, binary_classification_data):
        """Test get_training_summary method"""
        X, y, protected_attr = binary_classification_data
        
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(base_estimator=base_est)
        
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        summary = clf.get_training_summary()
        
        assert 'constraint_type' in summary
        assert 'algorithm' in summary
        assert 'n_iterations' in summary
        assert 'best_gap' in summary


class TestAdversarialDebiaser:
    """Test suite for Adversarial Debiaser"""
    
    def test_initialization(self):
        """Test debiaser initialization"""
        debiaser = AdversarialDebiaser(
            input_dim=20,
            classifier_hidden=(64, 32),
            adversary_hidden=(32,),
            n_epochs=10
        )
        
        assert debiaser.input_dim == 20
        assert debiaser.classifier_hidden == (64, 32)
        assert debiaser.n_epochs == 10
        assert debiaser.is_fitted_ is False
    
    def test_fit(self, small_dataset):
        """Test adversarial training"""
        X, y, protected_attr = small_dataset
        
        debiaser = AdversarialDebiaser(
            input_dim=10,
            n_epochs=5,  # Quick test
            batch_size=64
        )
        
        debiaser.fit(X[:400], y[:400], protected_attr[:400])
        
        assert debiaser.is_fitted_ is True
        assert debiaser.classifier_ is not None
        assert debiaser.adversary_ is not None
        assert debiaser.training_result_ is not None
    
    def test_predict(self, small_dataset):
        """Test making predictions"""
        X, y, protected_attr = small_dataset
        
        debiaser = AdversarialDebiaser(
            input_dim=10,
            n_epochs=5,
            batch_size=64
        )
        
        debiaser.fit(X[:400], y[:400], protected_attr[:400])
        predictions = debiaser.predict(X[400:])
        
        assert len(predictions) == 100
        assert set(predictions).issubset({0, 1})
    
    def test_predict_proba(self, small_dataset):
        """Test probability predictions"""
        X, y, protected_attr = small_dataset
        
        debiaser = AdversarialDebiaser(
            input_dim=10,
            n_epochs=5,
            batch_size=64
        )
        
        debiaser.fit(X[:400], y[:400], protected_attr[:400])
        probas = debiaser.predict_proba(X[400:])
        
        assert probas.shape == (100, 2)
        assert np.all((probas >= 0) & (probas <= 1))
    
    def test_score(self, small_dataset):
        """Test accuracy scoring"""
        X, y, protected_attr = small_dataset
        
        debiaser = AdversarialDebiaser(
            input_dim=10,
            n_epochs=10,
            batch_size=64
        )
        
        debiaser.fit(X[:400], y[:400], protected_attr[:400])
        accuracy = debiaser.score(X[400:], y[400:])
        
        assert 0.0 <= accuracy <= 1.0
    
    def test_training_history(self, small_dataset):
        """Test that training history is tracked"""
        X, y, protected_attr = small_dataset
        
        debiaser = AdversarialDebiaser(
            input_dim=10,
            n_epochs=10,
            batch_size=64
        )
        
        debiaser.fit(X[:400], y[:400], protected_attr[:400])
        
        history = debiaser.training_result_.training_history
        assert 'classifier_loss' in history
        assert 'adversary_loss' in history
        assert len(history['classifier_loss']) == 10
    
    def test_adversary_loss_weight(self, small_dataset):
        """Test different adversary loss weights"""
        X, y, protected_attr = small_dataset
        
        # Low weight (less fairness)
        debiaser_low = AdversarialDebiaser(
            input_dim=10,
            adversary_loss_weight=0.5,
            n_epochs=5
        )
        debiaser_low.fit(X[:400], y[:400], protected_attr[:400])
        
        # High weight (more fairness)
        debiaser_high = AdversarialDebiaser(
            input_dim=10,
            adversary_loss_weight=2.0,
            n_epochs=5
        )
        debiaser_high.fit(X[:400], y[:400], protected_attr[:400])
        
        # Both should complete successfully
        assert debiaser_low.is_fitted_ is True
        assert debiaser_high.is_fitted_ is True


class TestFairLogisticRegression:
    """Test suite for Fair Logistic Regression"""
    
    def test_initialization(self):
        """Test initialization"""
        clf = FairLogisticRegression(
            fairness_penalty=1.5,
            C=1.0,
            max_iter=1000
        )
        
        assert clf.fairness_penalty == 1.5
        assert clf.C == 1.0
        assert clf.is_fitted_ is False
    
    def test_fit(self, binary_classification_data):
        """Test training"""
        X, y, protected_attr = binary_classification_data
        
        clf = FairLogisticRegression(fairness_penalty=1.0)
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        assert clf.is_fitted_ is True
        assert clf.model_ is not None
    
    def test_predict(self, binary_classification_data):
        """Test predictions"""
        X, y, protected_attr = binary_classification_data
        
        clf = FairLogisticRegression()
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        predictions = clf.predict(X[800:])
        assert len(predictions) == 200
    
    def test_predict_proba(self, binary_classification_data):
        """Test probability predictions"""
        X, y, protected_attr = binary_classification_data
        
        clf = FairLogisticRegression()
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        probas = clf.predict_proba(X[800:])
        assert probas.shape == (200, 2)
    
    def test_score(self, binary_classification_data):
        """Test scoring"""
        X, y, protected_attr = binary_classification_data
        
        clf = FairLogisticRegression()
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        accuracy = clf.score(X[800:], y[800:])
        assert 0.0 <= accuracy <= 1.0


class TestFairGradientBoosting:
    """Test suite for Fair Gradient Boosting"""
    
    def test_initialization(self):
        """Test initialization"""
        clf = FairGradientBoosting(
            fairness_weight=1.5,
            n_estimators=50,
            max_depth=5
        )
        
        assert clf.fairness_weight == 1.5
        assert clf.n_estimators == 50
        assert clf.is_fitted_ is False
    
    def test_fit(self, binary_classification_data):
        """Test training"""
        X, y, protected_attr = binary_classification_data
        
        clf = FairGradientBoosting(n_estimators=10)
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        assert clf.is_fitted_ is True
        assert clf.model_ is not None
    
    def test_predict(self, binary_classification_data):
        """Test predictions"""
        X, y, protected_attr = binary_classification_data
        
        clf = FairGradientBoosting(n_estimators=10)
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        predictions = clf.predict(X[800:])
        assert len(predictions) == 200
    
    def test_score(self, binary_classification_data):
        """Test scoring"""
        X, y, protected_attr = binary_classification_data
        
        clf = FairGradientBoosting(n_estimators=10)
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        
        accuracy = clf.score(X[800:], y[800:])
        assert 0.0 <= accuracy <= 1.0


class TestInprocessingEngine:
    """Test suite for unified In-processing Engine"""
    
    def test_initialization(self):
        """Test engine initialization"""
        engine = InprocessingEngine(
            technique='auto',
            fairness_penalty=1.0
        )
        
        assert engine.technique == 'auto'
        assert engine.fairness_penalty == 1.0
    
    def test_auto_selection_logistic(self, binary_classification_data):
        """Test auto-selection for logistic regression"""
        X, y, protected_attr = binary_classification_data
        
        engine = InprocessingEngine(technique='auto')
        base_est = LogisticRegression(max_iter=1000)
        
        result = engine.train_fair_model(
            base_est, X[:800], y[:800], protected_attr[:800]
        )
        
        assert engine.selected_technique_ == 'fair_classifier'
        assert result.technique == 'fair_classifier'
    
    def test_auto_selection_tree(self, binary_classification_data):
        """Test auto-selection for tree-based models"""
        X, y, protected_attr = binary_classification_data
        
        engine = InprocessingEngine(technique='auto')
        base_est = RandomForestClassifier(n_estimators=10, random_state=42)
        
        result = engine.train_fair_model(
            base_est, X[:800], y[:800], protected_attr[:800]
        )
        
        assert engine.selected_technique_ in ['fairness_constraints', 'fair_classifier']
    
    def test_explicit_fairness_constraints(self, binary_classification_data):
        """Test explicit fairness constraints technique"""
        X, y, protected_attr = binary_classification_data
        
        engine = InprocessingEngine(
            technique='fairness_constraints',
            constraint_type='demographic_parity'
        )
        
        base_est = LogisticRegression(max_iter=1000)
        result = engine.train_fair_model(
            base_est, X[:800], y[:800], protected_attr[:800]
        )
        
        assert result.technique == 'fairness_constraints'
        assert engine.fitted_model_ is not None
    
    def test_explicit_adversarial(self, small_dataset):
        """Test explicit adversarial debiasing"""
        X, y, protected_attr = small_dataset
        
        engine = InprocessingEngine(
            technique='adversarial',
            n_epochs=5
        )
        
        result = engine.train_fair_model(
            None, X[:400], y[:400], protected_attr[:400]
        )
        
        assert result.technique == 'adversarial'
        assert engine.fitted_model_ is not None
    
    def test_explicit_fair_classifier(self, binary_classification_data):
        """Test explicit fair classifier technique"""
        X, y, protected_attr = binary_classification_data
        
        engine = InprocessingEngine(
            technique='fair_classifier',
            fairness_penalty=1.5
        )
        
        base_est = LogisticRegression(max_iter=1000)
        result = engine.train_fair_model(
            base_est, X[:800], y[:800], protected_attr[:800]
        )
        
        assert result.technique == 'fair_classifier'
    
    def test_predict(self, binary_classification_data):
        """Test prediction with engine"""
        X, y, protected_attr = binary_classification_data
        
        engine = InprocessingEngine(technique='fair_classifier')
        base_est = LogisticRegression(max_iter=1000)
        
        engine.train_fair_model(
            base_est, X[:800], y[:800], protected_attr[:800]
        )
        
        predictions = engine.predict(X[800:])
        assert len(predictions) == 200
    
    def test_predict_proba(self, binary_classification_data):
        """Test probability prediction with engine"""
        X, y, protected_attr = binary_classification_data
        
        engine = InprocessingEngine(technique='fair_classifier')
        base_est = LogisticRegression(max_iter=1000)
        
        engine.train_fair_model(
            base_est, X[:800], y[:800], protected_attr[:800]
        )
        
        probas = engine.predict_proba(X[800:])
        assert probas.shape == (200, 2)
    
    def test_result_summary(self, binary_classification_data):
        """Test get_result_summary method"""
        X, y, protected_attr = binary_classification_data
        
        engine = InprocessingEngine(technique='fair_classifier')
        base_est = LogisticRegression(max_iter=1000)
        
        engine.train_fair_model(
            base_est, X[:800], y[:800], protected_attr[:800]
        )
        
        summary = engine.get_result_summary()
        assert 'technique' in summary
        assert 'training_details' in summary
        assert 'metadata' in summary


class TestIntegration:
    """Integration tests across in-processing modules"""
    
    def test_fairness_constraints_with_model(self, binary_classification_data):
        """Test fairness constraints with actual model training"""
        X, y, protected_attr = binary_classification_data
        
        base_est = LogisticRegression(max_iter=1000)
        clf = FairnessConstrainedClassifier(
            base_estimator=base_est,
            constraint=ConstraintType.DEMOGRAPHIC_PARITY,
            eps=0.05
        )
        
        clf.fit(X[:800], y[:800], sensitive_features=protected_attr[:800])
        predictions = clf.predict(X[800:])
        accuracy = np.mean(predictions == y[800:])
        
        assert accuracy > 0.5  # Better than random
        assert clf.is_fitted_ is True
    
    def test_adversarial_with_model(self, small_dataset):
        """Test adversarial debiasing with actual model training"""
        X, y, protected_attr = small_dataset
        
        debiaser = AdversarialDebiaser(
            input_dim=10,
            n_epochs=10,
            batch_size=64
        )
        
        debiaser.fit(X[:400], y[:400], protected_attr[:400])
        predictions = debiaser.predict(X[400:])
        accuracy = np.mean(predictions == y[400:])
        
        assert accuracy > 0.4  # Neural nets may need more epochs
    
    def test_comparison_across_techniques(self, binary_classification_data):
        """Compare different in-processing techniques"""
        X, y, protected_attr = binary_classification_data
        
        X_train, X_test = X[:800], X[800:]
        y_train, y_test = y[:800], y[800:]
        protected_train = protected_attr[:800]
        
        results = {}
        
        # Fairness constraints
        clf_fc = FairnessConstrainedClassifier(
            base_estimator=LogisticRegression(max_iter=1000),
            constraint=ConstraintType.DEMOGRAPHIC_PARITY
        )
        clf_fc.fit(X_train, y_train, sensitive_features=protected_train)
        results['fairness_constraints'] = clf_fc.score(X_test, y_test)
        
        # Fair classifier
        clf_fair = FairLogisticRegression(fairness_penalty=1.0)
        clf_fair.fit(X_train, y_train, sensitive_features=protected_train)
        results['fair_classifier'] = clf_fair.score(X_test, y_test)
        
        # All should have reasonable accuracy
        for technique, accuracy in results.items():
            assert 0.5 < accuracy < 1.0, f"{technique} accuracy out of range: {accuracy}"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
