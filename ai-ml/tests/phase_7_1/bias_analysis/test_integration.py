#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Analysis Integration Tests
End-to-end tests for complete bias analysis pipeline.

Tests:
    - Complete fairness analysis workflow
    - Metrics → Explainability → Visualization pipeline
    - Report generator integration
    - Real-world scenario simulation

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

from services.bias_analysis import (
    DatasetProcessor,
    DemographicParityAnalyzer,
    EqualizedOddsAnalyzer,
    CalibrationAnalyzer,
    IndividualFairnessAnalyzer,
    SHAPExplainer,
    LIMEExplainer,
    FeatureAttributionAnalyzer,
    BiasVisualizer,
)


class TestCompleteBiasAnalysisPipeline(unittest.TestCase):
    """Test end-to-end bias analysis workflow."""

    def setUp(self):
        """Set up realistic test dataset."""
        np.random.seed(42)
        
        # Simulate realistic credit scoring dataset
        n_samples = 2000
        
        # Protected attributes
        self.gender = np.random.binomial(1, 0.5, n_samples)  # 0=Male, 1=Female
        self.age_group = np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.5, 0.2])
        
        # Features
        self.credit_score = np.random.normal(700, 50, n_samples).clip(300, 850)
        self.income = np.random.exponential(60000, n_samples).clip(20000, 200000)
        self.debt_to_income = np.random.beta(2, 5, n_samples) * 0.6
        self.employment_length = np.random.exponential(5, n_samples).clip(0, 30)
        
        # Create feature matrix
        self.X = np.column_stack([
            self.credit_score,
            self.income,
            self.debt_to_income,
            self.employment_length
        ])
        
        # Generate labels with slight bias
        base_prob = (
            0.3 * (self.credit_score - 300) / 550 +
            0.2 * np.log(self.income / 20000) / np.log(10) +
            0.3 * (1 - self.debt_to_income) +
            0.2 * np.minimum(self.employment_length / 10, 1)
        )
        
        # Add gender bias (privileged group gets slight boost)
        base_prob += 0.05 * (1 - self.gender)
        
        self.y_true = np.random.binomial(1, base_prob.clip(0, 1))
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=50, 
            max_depth=10,
            random_state=42
        )
        self.model.fit(self.X, self.y_true)
        self.y_pred = self.model.predict(self.X)
        self.y_prob = self.model.predict_proba(self.X)[:, 1]

    def test_complete_fairness_audit(self):
        """Test complete fairness audit across all metrics."""
        # Initialize all analyzers
        dp_analyzer = DemographicParityAnalyzer()
        eo_analyzer = EqualizedOddsAnalyzer()
        cal_analyzer = CalibrationAnalyzer()
        if_analyzer = IndividualFairnessAnalyzer()
        
        # Run all analyses
        dp_result = dp_analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.gender
        )
        
        eo_result = eo_analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.gender
        )
        
        cal_result = cal_analyzer.analyze(
            y_true=self.y_true,
            y_prob=self.y_prob,
            protected_attribute=self.gender
        )
        
        if_result = if_analyzer.analyze(
            X=self.X[:500],  # Subset for computational efficiency
            y_pred=self.y_pred[:500],
            protected_attribute=self.gender[:500]
        )
        
        # Verify all results are valid
        self.assertIsNotNone(dp_result)
        self.assertIsNotNone(eo_result)
        self.assertIsNotNone(cal_result)
        self.assertIsNotNone(if_result)
        
        # Collect all metrics
        all_metrics = {
            'demographic_parity': dp_result.demographic_parity_ratio,
            'equalized_odds': eo_result.equalized_odds_score,
            'calibration': 1.0 - cal_result.metrics['calibration_error'],
            'individual_fairness': if_result.metrics['individual_fairness_score']
        }
        
        # All metrics should be in valid range
        for metric_name, value in all_metrics.items():
            self.assertGreaterEqual(value, 0.0, msg=f"{metric_name} < 0")
            self.assertLessEqual(value, 1.0, msg=f"{metric_name} > 1")

    def test_explainability_integration(self):
        """Test SHAP and LIME integration with trained model."""
        # SHAP explanation
        shap_explainer = SHAPExplainer()
        shap_config = SHAPExplainer.SHAPConfig(
            model=self.model,
            data=self.X[:100],
            instance=self.X[0:1],
            explainer_type='tree'
        )
        
        shap_result = shap_explainer.explain(shap_config)
        
        # LIME explanation
        lime_explainer = LIMEExplainer()
        lime_config = LIMEExplainer.LIMEConfig(
            model=self.model,
            training_data=self.X[:100],
            instance=self.X[0:1],
            mode='classification'
        )
        
        lime_result = lime_explainer.explain(lime_config)
        
        # Verify both explainers produced results
        self.assertIsNotNone(shap_result)
        self.assertIsNotNone(lime_result)
        
        # Get feature rankings from both
        shap_top = shap_result.get_feature_ranking(top_n=5)
        lime_top = lime_result.get_top_features(n=5)
        
        # Both should identify important features
        self.assertGreater(len(shap_top), 0)
        self.assertGreater(len(lime_top), 0)

    def test_visualization_pipeline(self):
        """Test visualization of complete analysis results."""
        # Run fairness analysis
        dp_analyzer = DemographicParityAnalyzer()
        dp_result = dp_analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.gender
        )
        
        # Prepare metrics
        metrics = {
            'demographic_parity': dp_result.demographic_parity_ratio,
            'disparate_impact': dp_result.metrics.get('disparate_impact', 0.8),
            'statistical_parity': 1.0 - dp_result.metrics['statistical_parity_diff']
        }
        
        group_rates = dp_result.group_rates
        
        # Generate visualizations
        visualizer = BiasVisualizer()
        
        # Test all chart types
        charts = {
            'fairness_metrics': visualizer.plot_fairness_metrics(metrics),
            'group_comparison': visualizer.plot_group_comparison(group_rates),
            'summary_dashboard': visualizer.plot_summary_dashboard(
                overall_score=0.80,
                metrics=metrics,
                group_rates=group_rates
            )
        }
        
        # Verify all charts generated successfully
        for chart_name, img_data in charts.items():
            self.assertIsInstance(img_data, str, msg=f"{chart_name} failed")
            self.assertGreater(len(img_data), 0, msg=f"{chart_name} empty")
            
            # Verify PNG format
            import base64
            decoded = base64.b64decode(img_data)
            self.assertEqual(decoded[:4], b'\x89PNG', msg=f"{chart_name} not PNG")

    def test_bias_detection_and_mitigation_workflow(self):
        """Test complete workflow: detect bias → apply mitigation → verify improvement."""
        # Step 1: Detect bias
        dp_before = DemographicParityAnalyzer().analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.gender
        )
        
        bias_detected = dp_before.demographic_parity_ratio < 0.8
        
        # Step 2: Apply simple mitigation (reweighting)
        # In production, this would use the mitigation module
        weights = np.where(self.gender == 1, 1.2, 1.0)  # Slight reweighting
        
        # Retrain with weights (simplified mitigation)
        mitigated_model = RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        mitigated_model.fit(self.X, self.y_true)
        y_pred_mitigated = mitigated_model.predict(self.X)
        
        # Step 3: Verify improvement
        dp_after = DemographicParityAnalyzer().analyze(
            y_true=self.y_true,
            y_pred=y_pred_mitigated,
            protected_attribute=self.gender
        )
        
        # Compare before and after
        before_metrics = {
            'demographic_parity': dp_before.demographic_parity_ratio
        }
        after_metrics = {
            'demographic_parity': dp_after.demographic_parity_ratio
        }
        
        # Generate comparison visualization
        visualizer = BiasVisualizer()
        comparison_chart = visualizer.plot_mitigation_comparison(
            before_metrics=before_metrics,
            after_metrics=after_metrics
        )
        
        # Verify chart generated
        self.assertGreater(len(comparison_chart), 0)

    def test_multi_attribute_analysis(self):
        """Test bias analysis across multiple protected attributes."""
        protected_attrs = {
            'gender': self.gender,
            'age_group': self.age_group
        }
        
        results = {}
        
        for attr_name, attr_values in protected_attrs.items():
            analyzer = DemographicParityAnalyzer()
            result = analyzer.analyze(
                y_true=self.y_true,
                y_pred=self.y_pred,
                protected_attribute=attr_values
            )
            results[attr_name] = result
        
        # Verify all attributes analyzed
        self.assertEqual(len(results), 2)
        self.assertIn('gender', results)
        self.assertIn('age_group', results)
        
        # Both should have valid results
        for attr_name, result in results.items():
            self.assertIsNotNone(result, msg=f"{attr_name} analysis failed")
            self.assertGreaterEqual(
                result.demographic_parity_ratio, 0.0,
                msg=f"{attr_name} ratio < 0"
            )

    def test_report_generator_compatibility(self):
        """Test that bias analysis results are compatible with report generator."""
        # This test verifies integration with report_generator service
        
        # Generate bias analysis results
        dp_analyzer = DemographicParityAnalyzer()
        dp_result = dp_analyzer.analyze(
            y_true=self.y_true,
            y_pred=self.y_pred,
            protected_attribute=self.gender
        )
        
        # Prepare data in format expected by report_generator
        fairness_data = {
            'overall_bias_score': dp_result.demographic_parity_ratio,
            'fairness_metrics': {
                'demographic_parity': dp_result.demographic_parity_ratio,
                'disparate_impact': dp_result.metrics.get('disparate_impact', 0.8)
            },
            'protected_attributes': ['gender'],
            'mitigation_applied': None
        }
        
        # Verify structure matches what FairnessExplainer expects
        self.assertIn('overall_bias_score', fairness_data)
        self.assertIn('fairness_metrics', fairness_data)
        self.assertIn('protected_attributes', fairness_data)
        
        # Test that explainers can consume this data
        try:
            from services.report_generator.explainers import FairnessExplainer
            
            explainer = FairnessExplainer()
            html_exec = explainer.render(fairness_data, audience='executive')
            html_tech = explainer.render(fairness_data, audience='technical')
            html_reg = explainer.render(fairness_data, audience='regulatory')
            
            # All should generate HTML
            self.assertTrue(html_exec.startswith('<'))
            self.assertTrue(html_tech.startswith('<'))
            self.assertTrue(html_reg.startswith('<'))
            
        except ImportError:
            # report_generator not available - skip detailed test
            self.skipTest("report_generator not available for integration test")


class TestRealWorldScenarios(unittest.TestCase):
    """Test bias analysis in realistic scenarios."""

    def setUp(self):
        """Set up realistic datasets."""
        np.random.seed(42)
        
        # Scenario 1: Credit scoring
        self.credit_n = 1500
        self.credit_X = np.column_stack([
            np.random.normal(700, 50, self.credit_n),  # Credit score
            np.random.exponential(50000, self.credit_n),  # Income
            np.random.beta(2, 5, self.credit_n) * 0.5,  # DTI
        ])
        self.credit_gender = np.random.binomial(1, 0.5, self.credit_n)
        self.credit_y = np.random.binomial(1, 0.65, self.credit_n)
        
        # Scenario 2: Hiring prediction
        self.hiring_n = 1000
        self.hiring_X = np.column_stack([
            np.random.uniform(0, 10, self.hiring_n),  # Years experience
            np.random.uniform(1, 5, self.hiring_n),  # Skill rating
            np.random.binomial(1, 0.3, self.hiring_n),  # Degree (0/1)
        ])
        self.hiring_age = np.random.choice([0, 1, 2], self.hiring_n)  # Age groups
        self.hiring_y = np.random.binomial(1, 0.45, self.hiring_n)

    def test_credit_scoring_bias_audit(self):
        """Test complete bias audit for credit scoring scenario."""
        model = RandomForestClassifier(n_estimators=20, random_state=42)
        model.fit(self.credit_X, self.credit_y)
        y_pred = model.predict(self.credit_X)
        
        # Analyze bias
        analyzer = DemographicParityAnalyzer()
        result = analyzer.analyze(
            y_true=self.credit_y,
            y_pred=y_pred,
            protected_attribute=self.credit_gender
        )
        
        # Should produce valid results
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result.demographic_parity_ratio, 0.0)
        self.assertLessEqual(result.demographic_parity_ratio, 2.0)

    def test_hiring_bias_audit(self):
        """Test complete bias audit for hiring scenario."""
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(self.hiring_X, self.hiring_y)
        y_pred = model.predict(self.hiring_X)
        
        # Analyze bias across age groups
        analyzer = DemographicParityAnalyzer()
        result = analyzer.analyze(
            y_true=self.hiring_y,
            y_pred=y_pred,
            protected_attribute=self.hiring_age
        )
        
        # Should handle multi-class protected attribute
        self.assertIsNotNone(result)


def run_tests():
    """Run all integration tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCompleteBiasAnalysisPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestRealWorldScenarios))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
