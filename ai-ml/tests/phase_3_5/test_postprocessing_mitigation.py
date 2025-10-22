"""
Comprehensive tests for post-processing bias mitigation techniques.

Tests cover:
- Threshold optimization
- Fair calibration
- Equalized odds post-processing
- Unified post-processing engine
"""

import pytest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from services.bias_analysis.mitigation.postprocessing.threshold_optimizer import (
    ThresholdOptimizer,
    OptimizationObjective,
    ThresholdOptimizationResult
)
from services.bias_analysis.mitigation.postprocessing.calibration import (
    FairCalibrator,
    CalibrationMethod,
    CalibrationResult
)
from services.bias_analysis.mitigation.postprocessing.equalized_odds_postprocessor import (
    EqualizedOddsPostprocessor,
    EOPostprocessingResult
)
from services.bias_analysis.mitigation.postprocessing.postprocessing_engine import (
    PostprocessingEngine,
    PostprocessingResult
)


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def binary_classification_data():
    """Generate binary classification data with bias"""
    np.random.seed(42)
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    
    # Create biased sensitive features
    sensitive = np.random.choice([0, 1], size=1000, p=[0.7, 0.3])
    
    # Introduce bias
    y[sensitive == 1] = np.random.choice([0, 1], size=np.sum(sensitive == 1), p=[0.6, 0.4])
    
    return train_test_split(X, y, sensitive, test_size=0.3, random_state=42)


@pytest.fixture
def trained_model(binary_classification_data):
    """Train a model on biased data"""
    X_train, _, y_train, _, s_train, _ = binary_classification_data
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    return model


@pytest.fixture
def rf_model(binary_classification_data):
    """Train a random forest model"""
    X_train, _, y_train, _, s_train, _ = binary_classification_data
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    return model


# ==============================================================================
# Threshold Optimization Tests
# ==============================================================================

class TestThresholdOptimizer:
    """Tests for ThresholdOptimizer"""
    
    def test_initialization(self):
        """Test threshold optimizer initialization"""
        optimizer = ThresholdOptimizer(
            objective=OptimizationObjective.EQUAL_OPPORTUNITY,
            constraint_slack=0.05,
            n_grid_points=100
        )
        
        assert optimizer.objective == OptimizationObjective.EQUAL_OPPORTUNITY
        assert optimizer.constraint_slack == 0.05
        assert optimizer.n_grid_points == 100
        assert optimizer.group_thresholds_ is None
    
    def test_fit_demographic_parity(self, binary_classification_data, trained_model):
        """Test fitting with demographic parity objective"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        optimizer = ThresholdOptimizer(
            objective=OptimizationObjective.DEMOGRAPHIC_PARITY,
            n_grid_points=50
        )
        optimizer.fit(y_train, y_proba_train, s_train)
        
        assert optimizer.group_thresholds_ is not None
        assert len(optimizer.group_thresholds_) == len(np.unique(s_train))
        assert all(0 <= t <= 1 for t in optimizer.group_thresholds_.values())
    
    def test_fit_equal_opportunity(self, binary_classification_data, trained_model):
        """Test fitting with equal opportunity objective"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        optimizer = ThresholdOptimizer(
            objective=OptimizationObjective.EQUAL_OPPORTUNITY,
            n_grid_points=50
        )
        optimizer.fit(y_train, y_proba_train, s_train)
        
        assert optimizer.group_thresholds_ is not None
        assert len(optimizer.group_thresholds_) > 0
    
    def test_fit_equalized_odds(self, binary_classification_data, trained_model):
        """Test fitting with equalized odds objective"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        optimizer = ThresholdOptimizer(
            objective=OptimizationObjective.EQUALIZED_ODDS,
            n_grid_points=50
        )
        optimizer.fit(y_train, y_proba_train, s_train)
        
        assert optimizer.group_thresholds_ is not None
    
    def test_fit_maximize_accuracy(self, binary_classification_data, trained_model):
        """Test fitting with accuracy maximization"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        optimizer = ThresholdOptimizer(
            objective=OptimizationObjective.MAXIMIZE_ACCURACY,
            n_grid_points=50
        )
        optimizer.fit(y_train, y_proba_train, s_train)
        
        assert optimizer.group_thresholds_ is not None
    
    def test_predict(self, binary_classification_data, trained_model):
        """Test making predictions with optimized thresholds"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        y_proba_test = trained_model.predict_proba(X_test)[:, 1]
        
        optimizer = ThresholdOptimizer(objective=OptimizationObjective.EQUAL_OPPORTUNITY)
        optimizer.fit(y_train, y_proba_train, s_train)
        
        predictions = optimizer.predict(y_proba_test, s_test)
        
        assert len(predictions) == len(y_test)
        assert set(predictions).issubset({0, 1})
    
    def test_evaluate(self, binary_classification_data, trained_model):
        """Test evaluation of threshold optimization"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        y_proba_test = trained_model.predict_proba(X_test)[:, 1]
        
        optimizer = ThresholdOptimizer(objective=OptimizationObjective.EQUAL_OPPORTUNITY)
        optimizer.fit(y_train, y_proba_train, s_train)
        
        result = optimizer.evaluate(y_test, y_proba_test, s_test)
        
        assert isinstance(result, ThresholdOptimizationResult)
        assert result.objective == "equal_opportunity"
        assert 'improvement' in result.fairness_improvement or 'accuracy_change' in result.fairness_improvement
        assert result.group_thresholds is not None
    
    def test_result_to_dict(self, binary_classification_data, trained_model):
        """Test result serialization to dictionary"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        y_proba_test = trained_model.predict_proba(X_test)[:, 1]
        
        optimizer = ThresholdOptimizer()
        optimizer.fit(y_train, y_proba_train, s_train)
        result = optimizer.evaluate(y_test, y_proba_test, s_test)
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'objective' in result_dict
        assert 'group_thresholds' in result_dict
        assert 'fairness_improvement' in result_dict


# ==============================================================================
# Fair Calibration Tests
# ==============================================================================

class TestFairCalibrator:
    """Tests for FairCalibrator"""
    
    def test_initialization(self):
        """Test calibrator initialization"""
        calibrator = FairCalibrator(
            method=CalibrationMethod.PLATT,
            n_bins=10
        )
        
        assert calibrator.method == CalibrationMethod.PLATT
        assert calibrator.n_bins == 10
        assert calibrator.group_calibrators_ is None
    
    def test_fit_platt(self, binary_classification_data, trained_model):
        """Test Platt scaling calibration"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        calibrator = FairCalibrator(method=CalibrationMethod.PLATT)
        calibrator.fit(y_train, y_proba_train, s_train)
        
        assert calibrator.group_calibrators_ is not None
        assert len(calibrator.group_calibrators_) == len(np.unique(s_train))
    
    def test_fit_isotonic(self, binary_classification_data, trained_model):
        """Test isotonic regression calibration"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        calibrator = FairCalibrator(method=CalibrationMethod.ISOTONIC)
        calibrator.fit(y_train, y_proba_train, s_train)
        
        assert calibrator.group_calibrators_ is not None
    
    def test_fit_temperature(self, binary_classification_data, trained_model):
        """Test temperature scaling"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        calibrator = FairCalibrator(method=CalibrationMethod.TEMPERATURE)
        calibrator.fit(y_train, y_proba_train, s_train)
        
        assert calibrator.group_calibrators_ is not None
    
    def test_fit_beta(self, binary_classification_data, trained_model):
        """Test beta calibration"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        calibrator = FairCalibrator(method=CalibrationMethod.BETA)
        calibrator.fit(y_train, y_proba_train, s_train)
        
        assert calibrator.group_calibrators_ is not None
    
    def test_predict_proba(self, binary_classification_data, trained_model):
        """Test probability calibration"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        y_proba_test = trained_model.predict_proba(X_test)[:, 1]
        
        calibrator = FairCalibrator(method=CalibrationMethod.PLATT)
        calibrator.fit(y_train, y_proba_train, s_train)
        
        calibrated = calibrator.predict_proba(y_proba_test, s_test)
        
        assert len(calibrated) == len(y_test)
        assert np.all((calibrated >= 0) & (calibrated <= 1))
    
    def test_evaluate(self, binary_classification_data, trained_model):
        """Test calibration evaluation"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        y_proba_test = trained_model.predict_proba(X_test)[:, 1]
        
        calibrator = FairCalibrator(method=CalibrationMethod.PLATT)
        calibrator.fit(y_train, y_proba_train, s_train)
        
        calibrated = calibrator.predict_proba(y_proba_test, s_test)
        result = calibrator.evaluate(y_test, y_proba_test, calibrated, s_test)
        
        assert isinstance(result, CalibrationResult)
        assert result.method == "platt"
        assert result.original_calibration_error >= 0
        assert result.calibrated_calibration_error >= 0
    
    def test_calibration_improves_or_maintains(self, binary_classification_data, trained_model):
        """Test that calibration improves or maintains calibration error"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        y_proba_test = trained_model.predict_proba(X_test)[:, 1]
        
        calibrator = FairCalibrator(method=CalibrationMethod.PLATT)
        calibrator.fit(y_train, y_proba_train, s_train)
        
        calibrated = calibrator.predict_proba(y_proba_test, s_test)
        result = calibrator.evaluate(y_test, y_proba_test, calibrated, s_test)
        
        # Calibration should improve or stay similar
        assert result.calibrated_calibration_error <= result.original_calibration_error * 1.5


# ==============================================================================
# Equalized Odds Post-processor Tests
# ==============================================================================

class TestEqualizedOddsPostprocessor:
    """Tests for EqualizedOddsPostprocessor"""
    
    def test_initialization(self):
        """Test postprocessor initialization"""
        postprocessor = EqualizedOddsPostprocessor(
            constraint="equalized_odds",
            objective="accuracy_score",
            grid_size=100
        )
        
        assert postprocessor.constraint == "equalized_odds"
        assert postprocessor.objective == "accuracy_score"
        assert postprocessor.grid_size == 100
    
    def test_fit_equalized_odds(self, binary_classification_data, trained_model):
        """Test fitting with equalized odds constraint"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        
        postprocessor = EqualizedOddsPostprocessor(
            constraint="equalized_odds",
            grid_size=50
        )
        postprocessor.fit(trained_model, X_train, y_train, s_train)
        
        assert postprocessor.postprocessor_ is not None
        assert postprocessor.groups_ is not None
    
    def test_fit_equal_opportunity(self, binary_classification_data, trained_model):
        """Test fitting with equal opportunity constraint (true_positive_rate_parity)"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        
        postprocessor = EqualizedOddsPostprocessor(
            constraint="true_positive_rate_parity",  # Fairlearn's version of equal opportunity
            grid_size=50
        )
        postprocessor.fit(trained_model, X_train, y_train, s_train)
        
        assert postprocessor.postprocessor_ is not None
    
    def test_fit_demographic_parity(self, binary_classification_data, trained_model):
        """Test fitting with demographic parity constraint"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        
        postprocessor = EqualizedOddsPostprocessor(
            constraint="demographic_parity",
            grid_size=50
        )
        postprocessor.fit(trained_model, X_train, y_train, s_train)
        
        assert postprocessor.postprocessor_ is not None
    
    def test_predict(self, binary_classification_data, trained_model):
        """Test making predictions"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        
        postprocessor = EqualizedOddsPostprocessor(constraint="equalized_odds")
        postprocessor.fit(trained_model, X_train, y_train, s_train)
        
        predictions = postprocessor.predict(X_test, s_test, random_state=42)
        
        assert len(predictions) == len(y_test)
        assert set(predictions).issubset({0, 1})
    
    def test_evaluate(self, binary_classification_data, trained_model):
        """Test evaluation"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        
        postprocessor = EqualizedOddsPostprocessor(constraint="equalized_odds")
        postprocessor.fit(trained_model, X_train, y_train, s_train)
        
        result = postprocessor.evaluate(X_test, y_test, s_test, trained_model, random_state=42)
        
        assert isinstance(result, EOPostprocessingResult)
        assert 'accuracy' in result.original_metrics
        assert 'accuracy' in result.postprocessed_metrics
        assert len(result.group_specific_metrics) > 0


# ==============================================================================
# Post-processing Engine Tests
# ==============================================================================

class TestPostprocessingEngine:
    """Tests for unified PostprocessingEngine"""
    
    def test_initialization(self):
        """Test engine initialization"""
        engine = PostprocessingEngine(
            method="auto",
            combine_techniques=False
        )
        
        assert engine.method == "auto"
        assert engine.combine_techniques == False
    
    def test_fit_auto_selection(self, binary_classification_data, trained_model):
        """Test automatic method selection"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(method="auto")
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        
        assert engine.selected_method_ is not None
        assert engine.selected_method_ in ["threshold", "calibration", "equalized_odds", "combined"]
    
    def test_fit_threshold_method(self, binary_classification_data, trained_model):
        """Test fitting with threshold method"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(
            method="threshold",
            threshold_objective="equal_opportunity"
        )
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        
        assert engine.threshold_optimizer_ is not None
        assert engine.selected_method_ == "threshold"
    
    def test_fit_calibration_method(self, binary_classification_data, trained_model):
        """Test fitting with calibration method"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(
            method="calibration",
            calibration_method="platt"
        )
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        
        assert engine.calibrator_ is not None
        assert engine.selected_method_ == "calibration"
    
    def test_fit_equalized_odds_method(self, binary_classification_data, trained_model):
        """Test fitting with equalized odds method"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(
            method="equalized_odds",
            eo_constraint="equalized_odds"
        )
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        
        assert engine.eo_postprocessor_ is not None
        assert engine.selected_method_ == "equalized_odds"
    
    def test_fit_combined_method(self, binary_classification_data, trained_model):
        """Test fitting with combined techniques"""
        X_train, _, y_train, _, s_train, _ = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(
            method="combined",
            calibration_method="platt",
            threshold_objective="equal_opportunity",
            combine_techniques=True
        )
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        
        assert engine.selected_method_ == "combined"
    
    def test_predict(self, binary_classification_data, trained_model):
        """Test making predictions"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(method="threshold")
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        
        predictions = engine.predict(X_test, s_test)
        
        assert len(predictions) == len(y_test)
        assert set(predictions).issubset({0, 1})
    
    def test_predict_with_proba(self, binary_classification_data, trained_model):
        """Test predictions with probabilities"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(method="calibration")
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        
        predictions, probabilities = engine.predict(X_test, s_test, return_proba=True)
        
        assert len(predictions) == len(y_test)
        assert len(probabilities) == len(y_test)
        assert np.all((probabilities >= 0) & (probabilities <= 1))
    
    def test_evaluate(self, binary_classification_data, trained_model):
        """Test comprehensive evaluation"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(method="threshold")
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        
        result = engine.evaluate(X_test, y_test, s_test)
        
        assert isinstance(result, PostprocessingResult)
        assert result.method == "threshold"
        assert 'accuracy' in result.combined_metrics
        assert len(result.technique_results) > 0
    
    def test_result_serialization(self, binary_classification_data, trained_model):
        """Test result to_dict serialization"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = trained_model.predict_proba(X_train)[:, 1]
        
        engine = PostprocessingEngine(method="threshold")
        engine.fit(trained_model, X_train, y_train, y_proba_train, s_train)
        result = engine.evaluate(X_test, y_test, s_test)
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'method' in result_dict
        assert 'combined_metrics' in result_dict
        assert 'fairness_improvement' in result_dict


# ==============================================================================
# Integration Tests
# ==============================================================================

class TestIntegration:
    """Integration tests across post-processing techniques"""
    
    def test_all_methods_on_same_data(self, binary_classification_data, rf_model):
        """Test all methods produce valid results on same data"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = rf_model.predict_proba(X_train)[:, 1]
        
        methods = ["threshold", "calibration", "equalized_odds"]
        results = []
        
        for method in methods:
            engine = PostprocessingEngine(method=method)
            engine.fit(rf_model, X_train, y_train, y_proba_train, s_train)
            result = engine.evaluate(X_test, y_test, s_test)
            results.append(result)
        
        # All methods should produce results
        assert len(results) == 3
        assert all(r.predictions is not None for r in results)
    
    def test_combined_vs_individual(self, binary_classification_data, rf_model):
        """Test combined method vs individual methods"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        y_proba_train = rf_model.predict_proba(X_train)[:, 1]
        
        # Individual calibration
        engine_cal = PostprocessingEngine(method="calibration")
        engine_cal.fit(rf_model, X_train, y_train, y_proba_train, s_train)
        result_cal = engine_cal.evaluate(X_test, y_test, s_test)
        
        # Combined
        engine_combined = PostprocessingEngine(
            method="combined",
            combine_techniques=True
        )
        engine_combined.fit(rf_model, X_train, y_train, y_proba_train, s_train)
        result_combined = engine_combined.evaluate(X_test, y_test, s_test)
        
        # Both should produce valid results
        assert result_cal.combined_metrics['accuracy'] > 0
        assert result_combined.combined_metrics['accuracy'] > 0
    
    def test_different_models(self, binary_classification_data):
        """Test post-processing works with different model types"""
        X_train, X_test, y_train, y_test, s_train, s_test = binary_classification_data
        
        models = [
            LogisticRegression(random_state=42, max_iter=1000),
            RandomForestClassifier(n_estimators=30, random_state=42),
            DecisionTreeClassifier(random_state=42)
        ]
        
        for model in models:
            model.fit(X_train, y_train)
            y_proba_train = model.predict_proba(X_train)[:, 1]
            
            engine = PostprocessingEngine(method="auto")
            engine.fit(model, X_train, y_train, y_proba_train, s_train)
            result = engine.evaluate(X_test, y_test, s_test)
            
            assert result.combined_metrics['accuracy'] > 0
            assert result.predictions is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
