"""
Fairness-aware resampling techniques.

Implements oversampling and undersampling strategies to balance
protected group representation in training data.

Author: REGIQ AI/ML Team
Phase: 3.5.1 - Preprocessing Mitigation
"""

import numpy as np
from typing import Dict, Tuple, Optional, Literal
from dataclasses import dataclass
from imblearn.over_sampling import SMOTE, ADASYN, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
import logging

logger = logging.getLogger(__name__)


@dataclass
class ResamplingResult:
    """Result of fairness resampling operation"""
    X_resampled: np.ndarray
    y_resampled: np.ndarray
    protected_attr_resampled: np.ndarray
    original_distribution: Dict[str, int]
    resampled_distribution: Dict[str, int]
    sampling_strategy: Dict
    metadata: Dict


class FairnessResampler:
    """
    Resample data to balance protected group representation.
    
    Supports multiple strategies:
    - Oversampling: SMOTE, ADASYN, Random
    - Undersampling: Random
    - Combined: Over + Under sampling
    """
    
    def __init__(self,
                 strategy: Literal['oversample', 'undersample', 'combined'] = 'oversample',
                 oversample_method: str = 'smote',
                 target_ratio: float = 1.0,
                 random_state: Optional[int] = 42):
        """
        Initialize fairness resampler.
        
        Args:
            strategy: Resampling strategy ('oversample', 'undersample', 'combined')
            oversample_method: Method for oversampling ('smote', 'adasyn', 'random')
            target_ratio: Target ratio of minority/majority (1.0 = balanced)
            random_state: Random seed for reproducibility
        """
        self.strategy = strategy
        self.oversample_method = oversample_method
        self.target_ratio = target_ratio
        self.random_state = random_state
        
        self.sampling_strategy_: Optional[Dict] = None
    
    def fit_resample(self,
                     X: np.ndarray,
                     y: np.ndarray,
                     protected_attr: np.ndarray) -> ResamplingResult:
        """
        Resample data to balance protected groups.
        
        Args:
            X: Feature matrix
            y: Target labels
            protected_attr: Protected attribute values
            
        Returns:
            ResamplingResult with resampled data and statistics
        """
        logger.info(f"Resampling data using {self.strategy} strategy")
        
        # Calculate original distribution
        original_dist = self._calculate_distribution(protected_attr)
        
        # Determine sampling strategy
        self.sampling_strategy_ = self._determine_sampling_strategy(
            y, protected_attr
        )
        
        # Apply resampling based on strategy
        if self.strategy == 'oversample':
            X_res, y_res, protected_res = self._oversample(
                X, y, protected_attr
            )
        elif self.strategy == 'undersample':
            X_res, y_res, protected_res = self._undersample(
                X, y, protected_attr
            )
        elif self.strategy == 'combined':
            X_res, y_res, protected_res = self._combined_sampling(
                X, y, protected_attr
            )
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
        
        # Calculate resampled distribution
        resampled_dist = self._calculate_distribution(protected_res)
        
        logger.info(
            f"Resampled from {len(X)} to {len(X_res)} samples. "
            f"Original dist: {original_dist}, New dist: {resampled_dist}"
        )
        
        return ResamplingResult(
            X_resampled=X_res,
            y_resampled=y_res,
            protected_attr_resampled=protected_res,
            original_distribution=original_dist,
            resampled_distribution=resampled_dist,
            sampling_strategy=self.sampling_strategy_,
            metadata={
                'strategy': self.strategy,
                'oversample_method': self.oversample_method,
                'original_size': len(X),
                'resampled_size': len(X_res),
                'size_change': len(X_res) - len(X)
            }
        )
    
    def _oversample(self,
                   X: np.ndarray,
                   y: np.ndarray,
                   protected_attr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Apply oversampling to minority groups"""
        
        # Create composite target: (group, class)
        composite_target = self._create_composite_target(y, protected_attr)
        
        # Select oversampling method
        if self.oversample_method == 'smote':
            # Check if we have enough samples for SMOTE
            min_samples = min(np.bincount(composite_target))
            if min_samples < 2:
                logger.warning("Not enough samples for SMOTE, using random oversampling")
                sampler = RandomOverSampler(
                    sampling_strategy=self.sampling_strategy_,
                    random_state=self.random_state
                )
            else:
                try:
                    sampler = SMOTE(
                        sampling_strategy=self.sampling_strategy_,
                        random_state=self.random_state,
                        k_neighbors=min(5, min_samples - 1)
                    )
                except Exception as e:
                    logger.warning(f"SMOTE failed: {e}, using random oversampling")
                    sampler = RandomOverSampler(
                        sampling_strategy=self.sampling_strategy_,
                        random_state=self.random_state
                    )
        elif self.oversample_method == 'adasyn':
            try:
                sampler = ADASYN(
                    sampling_strategy=self.sampling_strategy_,
                    random_state=self.random_state
                )
            except Exception as e:
                logger.warning(f"ADASYN failed: {e}, using random oversampling")
                sampler = RandomOverSampler(
                    sampling_strategy=self.sampling_strategy_,
                    random_state=self.random_state
                )
        else:  # random
            sampler = RandomOverSampler(
                sampling_strategy=self.sampling_strategy_,
                random_state=self.random_state
            )
        
        # Apply oversampling
        X_resampled, composite_resampled = sampler.fit_resample(X, composite_target)
        
        # Decompose composite target back to y and protected_attr
        y_resampled, protected_resampled = self._decompose_composite_target(
            composite_resampled, y, protected_attr
        )
        
        return X_resampled, y_resampled, protected_resampled
    
    def _undersample(self,
                    X: np.ndarray,
                    y: np.ndarray,
                    protected_attr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Apply undersampling to majority groups"""
        
        # Create composite target
        composite_target = self._create_composite_target(y, protected_attr)
        
        # Apply undersampling
        sampler = RandomUnderSampler(
            sampling_strategy=self.sampling_strategy_,
            random_state=self.random_state
        )
        
        X_resampled, composite_resampled = sampler.fit_resample(X, composite_target)
        
        # Decompose composite target
        y_resampled, protected_resampled = self._decompose_composite_target(
            composite_resampled, y, protected_attr
        )
        
        return X_resampled, y_resampled, protected_resampled
    
    def _combined_sampling(self,
                          X: np.ndarray,
                          y: np.ndarray,
                          protected_attr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Apply both over and undersampling"""
        
        # First oversample minority groups
        X_over, y_over, protected_over = self._oversample(X, y, protected_attr)
        
        # Then undersample majority groups
        X_final, y_final, protected_final = self._undersample(
            X_over, y_over, protected_over
        )
        
        return X_final, y_final, protected_final
    
    def _determine_sampling_strategy(self,
                                    y: np.ndarray,
                                    protected_attr: np.ndarray) -> Dict:
        """Determine sampling strategy for each group-class combination"""
        
        # Calculate group-class counts
        unique_groups = np.unique(protected_attr)
        unique_classes = np.unique(y)
        
        composite_target = self._create_composite_target(y, protected_attr)
        unique_composite, counts = np.unique(composite_target, return_counts=True)
        
        # Find target count based on strategy
        if self.strategy == 'oversample':
            # Target: max count * target_ratio
            target_count = int(max(counts) * self.target_ratio)
        elif self.strategy == 'undersample':
            # Target: min count / target_ratio (but ensure it's less than max)
            target_count = max(int(min(counts) / self.target_ratio), min(counts))
        else:  # combined
            # Target: median count
            target_count = int(np.median(counts))
        
        # Create sampling strategy dict
        sampling_strategy = {}
        for composite_val, count in zip(unique_composite, counts):
            if self.strategy == 'oversample':
                # Only oversample minority classes (must sample >= current count)
                if count < target_count:
                    sampling_strategy[composite_val] = target_count
            elif self.strategy == 'undersample':
                # Only undersample majority classes
                if count > target_count:
                    sampling_strategy[composite_val] = target_count
            else:  # combined
                # Resample all to target
                if count < target_count:
                    # Oversample if below target
                    sampling_strategy[composite_val] = target_count
                # Note: undersampling will happen in second step
        
        return sampling_strategy
    
    def _create_composite_target(self,
                                 y: np.ndarray,
                                 protected_attr: np.ndarray) -> np.ndarray:
        """Create composite target from y and protected_attr"""
        # Encode as unique integers
        unique_groups = np.unique(protected_attr)
        unique_classes = np.unique(y)
        
        group_to_idx = {g: i for i, g in enumerate(unique_groups)}
        class_to_idx = {c: i for i, c in enumerate(unique_classes)}
        
        composite = np.zeros(len(y), dtype=int)
        for i in range(len(y)):
            group_idx = group_to_idx[protected_attr[i]]
            class_idx = class_to_idx[y[i]]
            composite[i] = group_idx * len(unique_classes) + class_idx
        
        return composite
    
    def _decompose_composite_target(self,
                                    composite: np.ndarray,
                                    original_y: np.ndarray,
                                    original_protected: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Decompose composite target back to y and protected_attr"""
        unique_groups = np.unique(original_protected)
        unique_classes = np.unique(original_y)
        
        n_classes = len(unique_classes)
        
        y_new = np.zeros(len(composite), dtype=original_y.dtype)
        protected_new = np.zeros(len(composite), dtype=original_protected.dtype)
        
        for i in range(len(composite)):
            group_idx = composite[i] // n_classes
            class_idx = composite[i] % n_classes
            
            y_new[i] = unique_classes[class_idx]
            protected_new[i] = unique_groups[group_idx]
        
        return y_new, protected_new
    
    def _calculate_distribution(self, protected_attr: np.ndarray) -> Dict[str, int]:
        """Calculate group distribution"""
        unique, counts = np.unique(protected_attr, return_counts=True)
        return {str(g): int(c) for g, c in zip(unique, counts)}
