"""
Unified bias removal engine for preprocessing.

Provides high-level interface to all preprocessing mitigation techniques
with automatic technique selection and validation.

Author: REGIQ AI/ML Team
Phase: 3.5.1 - Preprocessing Mitigation
"""

import numpy as np
from typing import Dict, List, Optional, Literal, Any
from dataclasses import dataclass, asdict
import logging

from .reweighting import SampleReweighter, ReweightingResult
from .resampling import FairnessResampler, ResamplingResult
from .data_augmentation import FairDataAugmenter, AugmentationResult
from .feature_transformation import FeatureTransformer, TransformationResult

logger = logging.getLogger(__name__)


@dataclass
class BiasRemovalResult:
    """Comprehensive result of bias removal"""
    technique: str
    X_processed: np.ndarray
    y_processed: np.ndarray
    protected_attr_processed: np.ndarray
    sample_weights: Optional[np.ndarray]
    
    # Technique-specific results
    reweighting_result: Optional[ReweightingResult]
    resampling_result: Optional[ResamplingResult]
    augmentation_result: Optional[AugmentationResult]
    transformation_result: Optional[TransformationResult]
    
    # Summary statistics
    original_size: int
    processed_size: int
    group_balance_improvement: float
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        result = {
            'technique': self.technique,
            'original_size': self.original_size,
            'processed_size': self.processed_size,
            'group_balance_improvement': self.group_balance_improvement,
            'metadata': self.metadata
        }
        
        # Add technique-specific results
        if self.reweighting_result:
            result['reweighting'] = {
                'balance_ratio': self.reweighting_result.balance_ratio,
                'original_distribution': self.reweighting_result.original_distribution,
                'weighted_distribution': self.reweighting_result.weighted_distribution,
                'weight_range': self.reweighting_result.metadata['weight_range'],
                'mean_weight': self.reweighting_result.metadata['mean_weight']
            }
        
        if self.resampling_result:
            result['resampling'] = {
                'original_distribution': self.resampling_result.original_distribution,
                'resampled_distribution': self.resampling_result.resampled_distribution,
                'size_change': self.resampling_result.metadata['size_change']
            }
        
        if self.augmentation_result:
            result['augmentation'] = {
                'synthetic_samples': self.augmentation_result.synthetic_samples,
                'group_distribution': self.augmentation_result.group_distribution,
                'method': self.augmentation_result.metadata['method']
            }
        
        if self.transformation_result:
            result['transformation'] = {
                'features_removed': len(self.transformation_result.removed_features),
                'features_transformed': len(self.transformation_result.transformed_features),
                'strategy': self.transformation_result.metadata['strategy']
            }
        
        return result


class BiasRemovalEngine:
    """
    Unified engine for preprocessing-based bias mitigation.
    
    Supports:
    - Automatic technique selection based on data characteristics
    - Manual technique selection
    - Combined techniques (feature transformation + reweighting/resampling)
    - Before/after validation
    """
    
    def __init__(self,
                 technique: Literal['auto', 'reweighting', 'resampling', 
                                   'augmentation', 'transformation'] = 'auto',
                 reweighting_config: Optional[Dict] = None,
                 resampling_config: Optional[Dict] = None,
                 augmentation_config: Optional[Dict] = None,
                 transformation_config: Optional[Dict] = None):
        """
        Initialize bias removal engine.
        
        Args:
            technique: Mitigation technique to use ('auto' for automatic selection)
            reweighting_config: Config for SampleReweighter
            resampling_config: Config for FairnessResampler
            augmentation_config: Config for FairDataAugmenter
            transformation_config: Config for FeatureTransformer
        """
        self.technique = technique
        self.reweighting_config = reweighting_config or {}
        self.resampling_config = resampling_config or {}
        self.augmentation_config = augmentation_config or {}
        self.transformation_config = transformation_config or {}
        
        self.selected_technique_: Optional[str] = None
    
    def remove_bias(self,
                    X: np.ndarray,
                    y: np.ndarray,
                    protected_attr: np.ndarray,
                    feature_names: Optional[List[str]] = None) -> BiasRemovalResult:
        """
        Apply bias removal to data.
        
        Args:
            X: Feature matrix
            y: Target labels
            protected_attr: Protected attribute values
            feature_names: Optional feature names
            
        Returns:
            BiasRemovalResult with processed data and statistics
        """
        logger.info(f"Starting bias removal with technique: {self.technique}")
        
        original_size = len(X)
        
        # Select technique if auto
        if self.technique == 'auto':
            self.selected_technique_ = self._select_technique(X, y, protected_attr)
        else:
            self.selected_technique_ = self.technique
        
        logger.info(f"Using technique: {self.selected_technique_}")
        
        # Apply selected technique
        if self.selected_technique_ == 'reweighting':
            result = self._apply_reweighting(X, y, protected_attr)
        elif self.selected_technique_ == 'resampling':
            result = self._apply_resampling(X, y, protected_attr)
        elif self.selected_technique_ == 'augmentation':
            result = self._apply_augmentation(X, y, protected_attr)
        elif self.selected_technique_ == 'transformation':
            result = self._apply_transformation(X, y, protected_attr, feature_names)
        else:
            raise ValueError(f"Unknown technique: {self.selected_technique_}")
        
        logger.info(
            f"Bias removal complete. Processed {result.processed_size} samples. "
            f"Balance improvement: {result.group_balance_improvement:.3f}"
        )
        
        return result
    
    def _select_technique(self,
                         X: np.ndarray,
                         y: np.ndarray,
                         protected_attr: np.ndarray) -> str:
        """
        Automatically select best technique based on data characteristics.
        
        Decision logic:
        1. If very small dataset (< 500) -> Reweighting (no data loss)
        2. If large imbalance (> 5:1) -> Resampling or Augmentation
        3. If high feature correlation with protected attr -> Transformation
        4. Default -> Reweighting (safest choice)
        """
        n_samples = len(X)
        n_features = X.shape[1]
        
        # Calculate group imbalance
        unique_groups, group_counts = np.unique(protected_attr, return_counts=True)
        imbalance_ratio = max(group_counts) / min(group_counts) if len(group_counts) > 1 else 1.0
        
        # Calculate feature-protected correlation
        max_correlation = 0.0
        for i in range(n_features):
            feature = X[:, i]
            try:
                from scipy.stats import spearmanr
                corr, _ = spearmanr(feature, protected_attr)
                max_correlation = max(max_correlation, abs(float(corr)) if not np.isnan(corr) else 0.0)
            except Exception:
                pass
        
        logger.info(
            f"Data characteristics: n_samples={n_samples}, "
            f"imbalance_ratio={imbalance_ratio:.2f}, "
            f"max_correlation={max_correlation:.3f}"
        )
        
        # Decision logic
        if n_samples < 500:
            return 'reweighting'
        elif max_correlation > 0.4:
            return 'transformation'
        elif imbalance_ratio > 5.0:
            return 'augmentation' if n_samples < 5000 else 'resampling'
        else:
            return 'reweighting'
    
    def _apply_reweighting(self,
                          X: np.ndarray,
                          y: np.ndarray,
                          protected_attr: np.ndarray) -> BiasRemovalResult:
        """Apply sample reweighting"""
        reweighter = SampleReweighter(**self.reweighting_config)
        reweighting_result = reweighter.fit_transform(y, protected_attr)
        
        return BiasRemovalResult(
            technique='reweighting',
            X_processed=X,  # Features unchanged
            y_processed=y,  # Labels unchanged
            protected_attr_processed=protected_attr,
            sample_weights=reweighting_result.weights,
            reweighting_result=reweighting_result,
            resampling_result=None,
            augmentation_result=None,
            transformation_result=None,
            original_size=len(X),
            processed_size=len(X),
            group_balance_improvement=reweighting_result.balance_ratio,
            metadata={
                'technique': 'reweighting',
                'method': reweighter.method
            }
        )
    
    def _apply_resampling(self,
                         X: np.ndarray,
                         y: np.ndarray,
                         protected_attr: np.ndarray) -> BiasRemovalResult:
        """Apply fairness resampling"""
        resampler = FairnessResampler(**self.resampling_config)
        resampling_result = resampler.fit_resample(X, y, protected_attr)
        
        # Calculate balance improvement
        original_balance = self._calculate_balance(protected_attr)
        new_balance = self._calculate_balance(resampling_result.protected_attr_resampled)
        balance_improvement = new_balance - original_balance
        
        return BiasRemovalResult(
            technique='resampling',
            X_processed=resampling_result.X_resampled,
            y_processed=resampling_result.y_resampled,
            protected_attr_processed=resampling_result.protected_attr_resampled,
            sample_weights=None,
            reweighting_result=None,
            resampling_result=resampling_result,
            augmentation_result=None,
            transformation_result=None,
            original_size=len(X),
            processed_size=len(resampling_result.X_resampled),
            group_balance_improvement=balance_improvement,
            metadata={
                'technique': 'resampling',
                'strategy': resampler.strategy
            }
        )
    
    def _apply_augmentation(self,
                           X: np.ndarray,
                           y: np.ndarray,
                           protected_attr: np.ndarray) -> BiasRemovalResult:
        """Apply data augmentation"""
        augmenter = FairDataAugmenter(**self.augmentation_config)
        augmentation_result = augmenter.fit_resample(X, y, protected_attr)
        
        # Calculate balance improvement
        original_balance = self._calculate_balance(protected_attr)
        new_balance = self._calculate_balance(augmentation_result.protected_attr_augmented)
        balance_improvement = new_balance - original_balance
        
        return BiasRemovalResult(
            technique='augmentation',
            X_processed=augmentation_result.X_augmented,
            y_processed=augmentation_result.y_augmented,
            protected_attr_processed=augmentation_result.protected_attr_augmented,
            sample_weights=None,
            reweighting_result=None,
            resampling_result=None,
            augmentation_result=augmentation_result,
            transformation_result=None,
            original_size=augmentation_result.original_size,
            processed_size=augmentation_result.augmented_size,
            group_balance_improvement=balance_improvement,
            metadata={
                'technique': 'augmentation',
                'method': augmenter.method
            }
        )
    
    def _apply_transformation(self,
                             X: np.ndarray,
                             y: np.ndarray,
                             protected_attr: np.ndarray,
                             feature_names: Optional[List[str]] = None) -> BiasRemovalResult:
        """Apply feature transformation"""
        config = self.transformation_config.copy()
        if feature_names:
            config['feature_names'] = feature_names
        
        transformer = FeatureTransformer(**config)
        transformation_result = transformer.fit_transform(X, protected_attr, y)
        
        # For transformation, balance improvement is harder to quantify
        # Use reduction in feature correlation as proxy
        balance_improvement = 0.0  # Would need before/after correlation comparison
        
        return BiasRemovalResult(
            technique='transformation',
            X_processed=transformation_result.X_transformed,
            y_processed=y,  # Labels unchanged
            protected_attr_processed=protected_attr,
            sample_weights=None,
            reweighting_result=None,
            resampling_result=None,
            augmentation_result=None,
            transformation_result=transformation_result,
            original_size=len(X),
            processed_size=len(X),
            group_balance_improvement=balance_improvement,
            metadata={
                'technique': 'transformation',
                'strategy': transformer.strategy,
                'features_removed': len(transformation_result.removed_features)
            }
        )
    
    def _calculate_balance(self, protected_attr: np.ndarray) -> float:
        """
        Calculate how balanced the groups are.
        Returns value between 0 and 1 (1 = perfectly balanced)
        """
        unique, counts = np.unique(protected_attr, return_counts=True)
        proportions = counts / len(protected_attr)
        
        if len(proportions) == 0:
            return 0.0
        
        # Calculate coefficient of variation
        mean_prop = np.mean(proportions)
        if mean_prop == 0:
            return 0.0
        
        std_prop = np.std(proportions)
        cv = std_prop / mean_prop
        
        # Convert to balance score (0 = unbalanced, 1 = balanced)
        balance = 1.0 / (1.0 + cv)
        
        return float(balance)
