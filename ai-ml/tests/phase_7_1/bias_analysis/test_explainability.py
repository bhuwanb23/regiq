#!/usr/bin/env python3
"""
REGIQ AI/ML - Explainability Tests
Test suite for SHAP and LIME explainers.

Tests:
    - SHAP Explainer integration
    - LIME Explainer integration
    - Feature Attribution Analyzer

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.bias_analysis.explainability import (
    SHAPExplainer,
    SHAPExplanation,
    SHAPConfig,
    LIMEExplainer,
    LIMEExplanation,
    LIMEConfig,
    FeatureAttributionAnalyzer,
    FeatureAttribution,
    AttributionConfig,
)


class TestSHAPExplainer(unittest.TestCase):
    """Test SHAP explanation generation."""

    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        
        # Create sample dataset
        n_samples = 500
        n_features = 10
        
        self.X = np.random.randn(n_samples, n_features)
        self.y = np.random.binomial(1, 0.5, n_samples)
        
        # Train a simple model
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.model.fit(self.X, self.y)
        
        # Sample instance for explanation
        self.instance = self.X[0:1]
        self.instance_idx = 0
        
        self.explainer = SHAPExplainer()

    def test_shap_explanation_basic(self):
        """Test basic SHAP explanation generation."""
        config = SHAPConfig(
            model=self.model,
            data=self.X[:100],  # Use subset for speed
            instance=self.instance,
            explainer_type='tree'  # TreeExplainer for tree models
        )
        
        result = self.explainer.explain(config)
        
        self.assertIsInstance(result, SHAPExplanation)
        self.assertIn('shap_values', result.explanation_data)
        self.assertIn('feature_importances', result.explanation_data)

    def test_shap_kernel_explainer(self):
        """Test SHAP with KernelExplainer (model-agnostic)."""
        config = SHAPConfig(
            model=self.model.predict_proba,
            data=self.X[:50],  # Smaller subset for kernel
            instance=self.instance,
            explainer_type='kernel'
        )
        
        result = self.explainer.explain(config)
        
        self.assertIsInstance(result, SHAPExplanation)
        self.assertTrue(len(result.explanation_data) > 0)

    def test_shap_feature_ranking(self):
        """Test feature importance ranking."""
        config = SHAPConfig(
            model=self.model,
            data=self.X[:100],
            instance=self.instance,
            explainer_type='tree'
        )
        
        result = self.explainer.explain(config)
        
        # Get feature rankings
        rankings = result.get_feature_ranking(top_n=5)
        
        self.assertIsInstance(rankings, list)
        self.assertLessEqual(len(rankings), 5)
        
        # Verify rankings are ordered by absolute SHAP value
        shap_values = result.explanation_data['feature_importances']
        sorted_indices = np.argsort(np.abs(shap_values))[::-1]
        
        for i in range(len(rankings) - 1):
            idx_current = sorted_indices[i]
            self.assertEqual(rankings[i][0], idx_current)

    def test_shap_summary_statistics(self):
        """Test SHAP summary statistics calculation."""
        config = SHAPConfig(
            model=self.model,
            data=self.X[:100],
            instance=self.instance,
            explainer_type='tree'
        )
        
        result = self.explainer.explain(config)
        
        summary = result.get_summary_statistics()
        
        self.assertIn('mean_absolute_shap', summary)
        self.assertIn('max_shap', summary)
        self.assertIn('min_shap', summary)
        self.assertGreaterEqual(summary['mean_absolute_shap'], 0.0)

    def test_invalid_explainer_type(self):
        """Test error handling for invalid explainer type."""
        config = SHAPConfig(
            model=self.model,
            data=self.X[:100],
            instance=self.instance,
            explainer_type='invalid_type'
        )
        
        with self.assertRaises(ValueError):
            self.explainer.explain(config)


class TestLIMEExplainer(unittest.TestCase):
    """Test LIME explanation generation."""

    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        
        # Create sample dataset
        n_samples = 500
        n_features = 10
        
        self.X = np.random.randn(n_samples, n_features)
        self.y = np.random.binomial(1, 0.5, n_samples)
        
        # Train a simple model
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.model.fit(self.X, self.y)
        
        # Sample instance for explanation
        self.instance = self.X[0:1]
        
        self.explainer = LIMEExplainer()

    def test_lime_explanation_basic(self):
        """Test basic LIME explanation generation."""
        config = LIMEConfig(
            model=self.model,
            training_data=self.X[:100],
            instance=self.instance,
            mode='classification'
        )
        
        result = self.explainer.explain(config)
        
        self.assertIsInstance(result, LIMEExplanation)
        self.assertIn('local_weights', result.explanation_data)
        self.assertIn('local_intercept', result.explanation_data)

    def test_lime_feature_weights(self):
        """Test LIME local feature weights."""
        config = LIMEConfig(
            model=self.model,
            training_data=self.X[:100],
            instance=self.instance,
            mode='classification'
        )
        
        result = self.explainer.explain(config)
        
        weights = result.explanation_data['local_weights']
        
        # Should have weights for each feature
        self.assertEqual(len(weights), self.X.shape[1])
        
        # Weights should sum to approximately 1 (normalized)
        self.assertAlmostEqual(np.sum(np.abs(weights)), 1.0, places=1)

    def test_lime_explanation_quality(self):
        """Test LIME explanation quality metrics."""
        config = LIMEConfig(
            model=self.model,
            training_data=self.X[:100],
            instance=self.instance,
            mode='classification',
            n_samples=1000,  # More samples for better fit
            width=0.5
        )
        
        result = self.explainer.explain(config)
        
        # Check R-squared value (goodness of fit)
        if 'r_squared' in result.explanation_data:
            r2 = result.explanation_data['r_squared']
            self.assertGreaterEqual(r2, 0.0)
            self.assertLessEqual(r2, 1.0)

    def test_lime_regression_mode(self):
        """Test LIME in regression mode."""
        # Create regression model
        y_reg = np.random.randn(500)
        model_reg = LogisticRegression(random_state=42, max_iter=1000)
        model_reg.fit(self.X, y_reg)
        
        config = LIMEConfig(
            model=model_reg,
            training_data=self.X[:100],
            instance=self.instance,
            mode='regression'
        )
        
        result = self.explainer.explain(config)
        
        self.assertIsInstance(result, LIMEExplanation)

    def test_lime_top_features(self):
        """Test getting top contributing features."""
        config = LIMEConfig(
            model=self.model,
            training_data=self.X[:100],
            instance=self.instance,
            mode='classification'
        )
        
        result = self.explainer.explain(config)
        
        # Get top 3 features
        top_features = result.get_top_features(n=3)
        
        self.assertIsInstance(top_features, list)
        self.assertLessEqual(len(top_features), 3)


class TestFeatureAttributionAnalyzer(unittest.TestCase):
    """Test unified feature attribution analysis."""

    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        
        # Create sample dataset
        n_samples = 500
        n_features = 10
        
        self.X = np.random.randn(n_samples, n_features)
        self.y = np.random.binomial(1, 0.5, n_samples)
        
        # Train a simple model
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.model.fit(self.X, self.y)
        
        self.analyzer = FeatureAttributionAnalyzer()

    def test_permutation_importance(self):
        """Test permutation-based feature importance."""
        config = AttributionConfig(
            model=self.model,
            X=self.X,
            y=self.y,
            method='permutation',
            n_repeats=5
        )
        
        result = self.analyzer.analyze(config)
        
        self.assertIsInstance(result, FeatureAttribution)
        self.assertIn('importance_scores', result.attribution_data)
        
        # Should have importance for each feature
        scores = result.attribution_data['importance_scores']
        self.assertEqual(len(scores), self.X.shape[1])
        self.assertTrue(all(score >= 0 for score in scores))

    def test_shap_attribution(self):
        """Test SHAP-based feature attribution."""
        config = AttributionConfig(
            model=self.model,
            X=self.X[:100],  # Subset for speed
            y=self.y[:100],
            method='shap'
        )
        
        result = self.analyzer.analyze(config)
        
        self.assertIsInstance(result, FeatureAttribution)
        self.assertIn('shap_values', result.attribution_data)

    def test_mean_decrease_impurity(self):
        """Test mean decrease impurity (built-in RF importance)."""
        config = AttributionConfig(
            model=self.model,
            X=self.X,
            y=self.y,
            method='mdi'
        )
        
        result = self.analyzer.analyze(config)
        
        self.assertIsInstance(result, FeatureAttribution)
        self.assertIn('mdi_scores', result.attribution_data)
        
        # MDI scores should be non-negative
        mdi_scores = result.attribution_data['mdi_scores']
        self.assertTrue(all(score >= 0 for score in mdi_scores))
        
        # Sum should be approximately 1 (normalized)
        self.assertAlmostEqual(np.sum(mdi_scores), 1.0, places=1)

    def test_feature_ranking_consistency(self):
        """Test that different methods produce consistent top features."""
        # Permutation importance
        config_perm = AttributionConfig(
            model=self.model,
            X=self.X,
            y=self.y,
            method='permutation',
            n_repeats=5
        )
        result_perm = self.analyzer.analyze(config_perm)
        
        # MDI importance
        config_mdi = AttributionConfig(
            model=self.model,
            X=self.X,
            y=self.y,
            method='mdi'
        )
        result_mdi = self.analyzer.analyze(config_mdi)
        
        # Get top 3 features from each method
        perm_scores = result_perm.attribution_data['importance_scores']
        mdi_scores = result_mdi.attribution_data['mdi_scores']
        
        perm_top_3 = np.argsort(perm_scores)[::-1][:3]
        mdi_top_3 = np.argsort(mdi_scores)[::-1][:3]
        
        # Should have at least some overlap in top features
        overlap = len(set(perm_top_3) & set(mdi_top_3))
        self.assertGreaterEqual(overlap, 1)

    def test_invalid_method(self):
        """Test error handling for invalid method."""
        config = AttributionConfig(
            model=self.model,
            X=self.X,
            y=self.y,
            method='invalid_method'
        )
        
        with self.assertRaises(ValueError):
            self.analyzer.analyze(config)


def run_tests():
    """Run all explainability tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSHAPExplainer))
    suite.addTests(loader.loadTestsFromTestCase(TestLIMEExplainer))
    suite.addTests(loader.loadTestsFromTestCase(TestFeatureAttributionAnalyzer))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
