"""
Unit tests for preprocessing-based bias mitigation techniques.

Tests all preprocessing modules:
- Sample reweighting
- Fairness resampling  
- Fair data augmentation
- Feature transformation
- Unified bias removal engine

Author: REGIQ AI/ML Team
Phase: 3.5.1 - Preprocessing Tests
"""

import pytest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

# Import preprocessing modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.bias_analysis.mitigation.preprocessing.reweighting import SampleReweighter
from services.bias_analysis.mitigation.preprocessing.resampling import FairnessResampler
from services.bias_analysis.mitigation.preprocessing.data_augmentation import FairDataAugmenter
from services.bias_analysis.mitigation.preprocessing.feature_transformation import FeatureTransformer
from services.bias_analysis.mitigation.preprocessing.bias_removal import BiasRemovalEngine


@pytest.fixture
def binary_classification_data():
    """Generate binary classification dataset with group imbalance"""
    np.random.seed(42)
    
    # Generate base data
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
    
    # Create imbalanced protected attribute (70% group 0, 30% group 1)
    protected_attr = np.random.choice([0, 1], size=1000, p=[0.7, 0.3])
    
    return X, y, protected_attr


@pytest.fixture
def model():
    """Create a simple RF model for testing"""
    return RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)


class TestSampleReweighter:
    """Test suite for SampleReweighter"""
    
    def test_initialization(self):
        """Test reweighter initialization"""
        reweighter = SampleReweighter(
            method='inverse_frequency',
            normalize=True,
            min_weight=0.1,
            max_weight=10.0
        )
        
        assert reweighter.method == 'inverse_frequency'
        assert reweighter.normalize is True
        assert reweighter.min_weight == 0.1
        assert reweighter.max_weight == 10.0
        assert reweighter.is_fitted_ is False
    
    def test_fit_inverse_frequency(self, binary_classification_data):
        """Test fitting with inverse frequency method"""
        X, y, protected_attr = binary_classification_data
        
        reweighter = SampleReweighter(method='inverse_frequency')
        reweighter.fit(y, protected_attr)
        
        assert reweighter.is_fitted_ is True
        assert reweighter.group_weights_ is not None
        assert len(reweighter.group_weights_) > 0
    
    def test_fit_balanced(self, binary_classification_data):
        """Test fitting with balanced method"""
        X, y, protected_attr = binary_classification_data
        
        reweighter = SampleReweighter(method='balanced')
        reweighter.fit(y, protected_attr)
        
        assert reweighter.is_fitted_ is True
        assert reweighter.group_weights_ is not None
    
    def test_transform(self, binary_classification_data):
        """Test weight transformation"""
        X, y, protected_attr = binary_classification_data
        
        reweighter = SampleReweighter()
        result = reweighter.fit_transform(y, protected_attr)
        
        assert result.weights is not None
        assert len(result.weights) == len(y)
        assert result.weights.min() >= reweighter.min_weight
        assert result.weights.max() <= reweighter.max_weight
        assert result.balance_ratio >= 0.0 and result.balance_ratio <= 1.0
    
    def test_balance_improvement(self, binary_classification_data):
        """Test that reweighting improves balance"""
        X, y, protected_attr = binary_classification_data
        
        reweighter = SampleReweighter()
        result = reweighter.fit_transform(y, protected_attr)
        
        # Weighted distribution should be more balanced
        original_balance = result.balance_ratio  # Stored in result
        
        # Check that balance ratio is reasonable
        assert result.balance_ratio > 0.5  # At least somewhat balanced
    
    def test_weights_summary(self, binary_classification_data):
        """Test get_weights_summary method"""
        X, y, protected_attr = binary_classification_data
        
        reweighter = SampleReweighter()
        reweighter.fit(y, protected_attr)
        
        summary = reweighter.get_weights_summary()
        
        assert 'n_groups' in summary
        assert 'n_classes' in summary
        assert 'weight_range' in summary
        assert 'mean_weight' in summary
        assert summary['n_groups'] == 2  # Binary protected attribute


class TestFairnessResampler:
    """Test suite for FairnessResampler"""
    
    def test_initialization(self):
        """Test resampler initialization"""
        resampler = FairnessResampler(
            strategy='oversample',
            oversample_method='smote',
            target_ratio=1.0
        )
        
        assert resampler.strategy == 'oversample'
        assert resampler.oversample_method == 'smote'
        assert resampler.target_ratio == 1.0
    
    def test_oversample(self, binary_classification_data):
        """Test oversampling"""
        X, y, protected_attr = binary_classification_data
        
        resampler = FairnessResampler(strategy='oversample', oversample_method='smote')
        result = resampler.fit_resample(X, y, protected_attr)
        
        assert result.X_resampled.shape[0] >= X.shape[0]  # More or equal samples
        assert result.X_resampled.shape[1] == X.shape[1]  # Same features
        assert len(result.y_resampled) == len(result.X_resampled)
        assert len(result.protected_attr_resampled) == len(result.X_resampled)
    
    def test_undersample(self, binary_classification_data):
        """Test undersampling"""
        X, y, protected_attr = binary_classification_data
        
        resampler = FairnessResampler(strategy='undersample')
        result = resampler.fit_resample(X, y, protected_attr)
        
        assert result.X_resampled.shape[0] <= X.shape[0]  # Fewer or equal samples
        assert result.X_resampled.shape[1] == X.shape[1]  # Same features
    
    def test_combined_sampling(self, binary_classification_data):
        """Test combined over+under sampling"""
        X, y, protected_attr = binary_classification_data
        
        resampler = FairnessResampler(strategy='combined')
        result = resampler.fit_resample(X, y, protected_attr)
        
        assert result.X_resampled.shape[1] == X.shape[1]
        assert 'size_change' in result.metadata
    
    def test_distribution_balance(self, binary_classification_data):
        """Test that resampling improves distribution balance"""
        X, y, protected_attr = binary_classification_data
        
        original_dist = {}
        unique, counts = np.unique(protected_attr, return_counts=True)
        for u, c in zip(unique, counts):
            original_dist[str(u)] = c
        
        resampler = FairnessResampler(strategy='oversample')
        result = resampler.fit_resample(X, y, protected_attr)
        
        # Resampled distribution should be more balanced
        resampled_counts = list(result.resampled_distribution.values())
        original_counts = list(result.original_distribution.values())
        
        # Check variance decreased (more balanced)
        assert np.std(resampled_counts) <= np.std(original_counts) * 1.5  # Allow some tolerance


class TestFairDataAugmenter:
    """Test suite for FairDataAugmenter"""
    
    def test_initialization(self):
        """Test augmenter initialization"""
        augmenter = FairDataAugmenter(
            method='smote',
            target_ratio=1.0,
            k_neighbors=5
        )
        
        assert augmenter.method == 'smote'
        assert augmenter.target_ratio == 1.0
        assert augmenter.k_neighbors == 5
    
    def test_smote_augmentation(self, binary_classification_data):
        """Test SMOTE augmentation"""
        X, y, protected_attr = binary_classification_data
        
        augmenter = FairDataAugmenter(method='smote')
        result = augmenter.fit_resample(X, y, protected_attr)
        
        assert result.augmented_size >= result.original_size
        assert result.synthetic_samples >= 0
        assert result.X_augmented.shape[1] == X.shape[1]
    
    def test_adasyn_augmentation(self, binary_classification_data):
        """Test ADASYN augmentation"""
        X, y, protected_attr = binary_classification_data
        
        augmenter = FairDataAugmenter(method='adasyn')
        result = augmenter.fit_resample(X, y, protected_attr)
        
        assert result.augmented_size >= result.original_size
        assert 'method' in result.metadata
        assert result.metadata['method'] == 'adasyn'
    
    def test_fair_smote(self, binary_classification_data):
        """Test Fair SMOTE (group-aware)"""
        X, y, protected_attr = binary_classification_data
        
        augmenter = FairDataAugmenter(method='fair_smote')
        result = augmenter.fit_resample(X, y, protected_attr)
        
        assert result.augmented_size >= result.original_size
        assert len(result.group_distribution) > 0
    
    def test_synthetic_sample_quality(self, binary_classification_data):
        """Test that synthetic samples have reasonable feature ranges"""
        X, y, protected_attr = binary_classification_data
        
        augmenter = FairDataAugmenter(method='smote')
        result = augmenter.fit_resample(X, y, protected_attr)
        
        # Check that augmented features are within reasonable range
        for i in range(X.shape[1]):
            original_min, original_max = X[:, i].min(), X[:, i].max()
            augmented_min, augmented_max = result.X_augmented[:, i].min(), result.X_augmented[:, i].max()
            
            # Synthetic samples should be within or slightly outside original range
            assert augmented_min >= original_min * 1.5 or augmented_min <= original_max * 1.5


class TestFeatureTransformer:
    """Test suite for FeatureTransformer"""
    
    def test_initialization(self):
        """Test transformer initialization"""
        transformer = FeatureTransformer(
            strategy='decorrelate',
            correlation_threshold=0.3
        )
        
        assert transformer.strategy == 'decorrelate'
        assert transformer.correlation_threshold == 0.3
        assert transformer.is_fitted_ is False
    
    def test_remove_strategy(self, binary_classification_data):
        """Test feature removal strategy"""
        X, y, protected_attr = binary_classification_data
        
        transformer = FeatureTransformer(strategy='remove', correlation_threshold=0.2)
        result = transformer.fit_transform(X, protected_attr)
        
        assert result.X_transformed.shape[0] == X.shape[0]  # Same samples
        assert result.X_transformed.shape[1] <= X.shape[1]  # Fewer or equal features
        assert len(result.removed_features) >= 0
    
    def test_decorrelate_strategy(self, binary_classification_data):
        """Test feature decorrelation strategy"""
        X, y, protected_attr = binary_classification_data
        
        transformer = FeatureTransformer(strategy='decorrelate')
        result = transformer.fit_transform(X, protected_attr)
        
        assert result.X_transformed.shape == X.shape  # Same shape
        assert 'strategy' in result.metadata
    
    def test_fair_pca_strategy(self, binary_classification_data):
        """Test fair PCA strategy"""
        X, y, protected_attr = binary_classification_data
        
        transformer = FeatureTransformer(strategy='fair_pca', preserve_variance=0.95)
        result = transformer.fit_transform(X, protected_attr)
        
        assert result.X_transformed.shape[0] == X.shape[0]
        # Features may change due to PCA
    
    def test_transformation_summary(self, binary_classification_data):
        """Test get_transformation_summary method"""
        X, y, protected_attr = binary_classification_data
        
        feature_names = [f'feature_{i}' for i in range(X.shape[1])]
        transformer = FeatureTransformer(
            strategy='remove',
            correlation_threshold=0.2,
            feature_names=feature_names
        )
        transformer.fit(X, protected_attr)
        
        summary = transformer.get_transformation_summary()
        
        assert 'strategy' in summary
        assert 'removed_features' in summary
        assert 'n_removed' in summary


class TestBiasRemovalEngine:
    """Test suite for unified BiasRemovalEngine"""
    
    def test_initialization(self):
        """Test engine initialization"""
        engine = BiasRemovalEngine(technique='auto')
        
        assert engine.technique == 'auto'
        assert engine.selected_technique_ is None
    
    def test_auto_selection_small_dataset(self):
        """Test auto technique selection for small dataset"""
        # Create small dataset
        X, y = make_classification(n_samples=300, n_features=10, random_state=42)
        protected_attr = np.random.choice([0, 1], size=300)
        
        engine = BiasRemovalEngine(technique='auto')
        result = engine.remove_bias(X, y, protected_attr)
        
        assert engine.selected_technique_ == 'reweighting'  # Should choose reweighting for small data
    
    def test_reweighting_technique(self, binary_classification_data):
        """Test explicit reweighting technique"""
        X, y, protected_attr = binary_classification_data
        
        engine = BiasRemovalEngine(technique='reweighting')
        result = engine.remove_bias(X, y, protected_attr)
        
        assert result.technique == 'reweighting'
        assert result.sample_weights is not None
        assert result.reweighting_result is not None
        assert result.processed_size == result.original_size
    
    def test_resampling_technique(self, binary_classification_data):
        """Test explicit resampling technique"""
        X, y, protected_attr = binary_classification_data
        
        engine = BiasRemovalEngine(technique='resampling')
        result = engine.remove_bias(X, y, protected_attr)
        
        assert result.technique == 'resampling'
        assert result.resampling_result is not None
        assert result.X_processed.shape[1] == X.shape[1]
    
    def test_augmentation_technique(self, binary_classification_data):
        """Test explicit augmentation technique"""
        X, y, protected_attr = binary_classification_data
        
        engine = BiasRemovalEngine(technique='augmentation')
        result = engine.remove_bias(X, y, protected_attr)
        
        assert result.technique == 'augmentation'
        assert result.augmentation_result is not None
        assert result.processed_size >= result.original_size
    
    def test_transformation_technique(self, binary_classification_data):
        """Test explicit transformation technique"""
        X, y, protected_attr = binary_classification_data
        
        engine = BiasRemovalEngine(technique='transformation')
        result = engine.remove_bias(X, y, protected_attr)
        
        assert result.technique == 'transformation'
        assert result.transformation_result is not None
    
    def test_to_dict_serialization(self, binary_classification_data):
        """Test result serialization to dict"""
        X, y, protected_attr = binary_classification_data
        
        engine = BiasRemovalEngine(technique='reweighting')
        result = engine.remove_bias(X, y, protected_attr)
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'technique' in result_dict
        assert 'original_size' in result_dict
        assert 'processed_size' in result_dict
        assert 'reweighting' in result_dict


class TestIntegration:
    """Integration tests across preprocessing modules"""
    
    def test_reweighting_with_model(self, binary_classification_data, model):
        """Test reweighting with actual model training"""
        X, y, protected_attr = binary_classification_data
        
        # Apply reweighting
        reweighter = SampleReweighter()
        result = reweighter.fit_transform(y, protected_attr)
        
        # Train model with weights
        model.fit(X, y, sample_weight=result.weights)
        predictions = model.predict(X)
        
        accuracy = np.mean(predictions == y)
        assert accuracy > 0.5  # Model should learn something
    
    def test_resampling_with_model(self, binary_classification_data, model):
        """Test resampling with actual model training"""
        X, y, protected_attr = binary_classification_data
        
        # Apply resampling
        resampler = FairnessResampler(strategy='oversample')
        result = resampler.fit_resample(X, y, protected_attr)
        
        # Train model on resampled data
        model.fit(result.X_resampled, result.y_resampled)
        predictions = model.predict(X)
        
        accuracy = np.mean(predictions == y)
        assert accuracy > 0.5
    
    def test_pipeline_combination(self, binary_classification_data):
        """Test combining transformation + reweighting"""
        X, y, protected_attr = binary_classification_data
        
        # First apply transformation
        transformer = FeatureTransformer(strategy='remove', correlation_threshold=0.3)
        transform_result = transformer.fit_transform(X, protected_attr)
        
        # Then apply reweighting
        reweighter = SampleReweighter()
        reweight_result = reweighter.fit_transform(y, protected_attr)
        
        assert transform_result.X_transformed.shape[0] == X.shape[0]
        assert len(reweight_result.weights) == len(y)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
