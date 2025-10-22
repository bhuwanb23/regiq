"""
Fair data augmentation using synthetic sample generation.

Generates synthetic samples for underrepresented groups using
SMOTE, ADASYN, and fair variants to improve group balance.

Author: REGIQ AI/ML Team
Phase: 3.5.1 - Preprocessing Mitigation
"""

import numpy as np
from typing import Dict, Tuple, Optional, Literal
from dataclasses import dataclass
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE
import logging

logger = logging.getLogger(__name__)


@dataclass
class AugmentationResult:
    """Result of data augmentation operation"""
    X_augmented: np.ndarray
    y_augmented: np.ndarray
    protected_attr_augmented: np.ndarray
    original_size: int
    augmented_size: int
    synthetic_samples: int
    group_distribution: Dict[str, int]
    metadata: Dict


class FairDataAugmenter:
    """
    Generate synthetic samples to balance protected groups.
    
    Uses advanced oversampling techniques:
    - SMOTE: Synthetic Minority Oversampling Technique
    - ADASYN: Adaptive Synthetic Sampling
    - Borderline-SMOTE: Focus on borderline samples
    - Fair-SMOTE: Group-aware SMOTE variant
    """
    
    def __init__(self,
                 method: Literal['smote', 'adasyn', 'borderline', 'fair_smote'] = 'smote',
                 target_ratio: float = 1.0,
                 k_neighbors: int = 5,
                 random_state: Optional[int] = 42):
        """
        Initialize fair data augmenter.
        
        Args:
            method: Augmentation method to use
            target_ratio: Target ratio minority/majority (1.0 = balanced)
            k_neighbors: Number of nearest neighbors for SMOTE
            random_state: Random seed for reproducibility
        """
        self.method = method
        self.target_ratio = target_ratio
        self.k_neighbors = k_neighbors
        self.random_state = random_state
    
    def fit_resample(self,
                     X: np.ndarray,
                     y: np.ndarray,
                     protected_attr: np.ndarray) -> AugmentationResult:
        """
        Generate synthetic samples for minority groups.
        
        Args:
            X: Feature matrix
            y: Target labels
            protected_attr: Protected attribute values
            
        Returns:
            AugmentationResult with augmented data
        """
        logger.info(f"Augmenting data using {self.method} method")
        
        original_size = len(X)
        
        # Apply group-aware augmentation
        if self.method == 'fair_smote':
            X_aug, y_aug, protected_aug = self._fair_smote(
                X, y, protected_attr
            )
        else:
            X_aug, y_aug, protected_aug = self._standard_augmentation(
                X, y, protected_attr
            )
        
        augmented_size = len(X_aug)
        synthetic_samples = augmented_size - original_size
        
        # Calculate group distribution
        group_dist = self._calculate_distribution(protected_aug)
        
        logger.info(
            f"Augmented from {original_size} to {augmented_size} samples "
            f"({synthetic_samples} synthetic). Distribution: {group_dist}"
        )
        
        return AugmentationResult(
            X_augmented=X_aug,
            y_augmented=y_aug,
            protected_attr_augmented=protected_aug,
            original_size=original_size,
            augmented_size=augmented_size,
            synthetic_samples=synthetic_samples,
            group_distribution=group_dist,
            metadata={
                'method': self.method,
                'target_ratio': self.target_ratio,
                'k_neighbors': self.k_neighbors
            }
        )
    
    def _standard_augmentation(self,
                              X: np.ndarray,
                              y: np.ndarray,
                              protected_attr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Apply standard SMOTE/ADASYN augmentation"""
        
        # Create composite target (group, class)
        composite_target = self._create_composite_target(y, protected_attr)
        
        # Determine sampling strategy
        sampling_strategy = self._determine_sampling_strategy(composite_target)
        
        # Check minimum samples for SMOTE
        min_samples = min(np.bincount(composite_target))
        k_neighbors = min(self.k_neighbors, min_samples - 1) if min_samples > 1 else 1
        
        # Create sampler based on method
        try:
            if self.method == 'smote':
                sampler = SMOTE(
                    sampling_strategy=sampling_strategy,
                    k_neighbors=k_neighbors,
                    random_state=self.random_state
                )
            elif self.method == 'adasyn':
                sampler = ADASYN(
                    sampling_strategy=sampling_strategy,
                    n_neighbors=k_neighbors,
                    random_state=self.random_state
                )
            elif self.method == 'borderline':
                sampler = BorderlineSMOTE(
                    sampling_strategy=sampling_strategy,
                    k_neighbors=k_neighbors,
                    random_state=self.random_state
                )
            else:
                raise ValueError(f"Unknown method: {self.method}")
            
            # Apply sampling
            X_resampled, composite_resampled = sampler.fit_resample(X, composite_target)
            
        except Exception as e:
            logger.warning(f"Augmentation failed: {e}, returning original data")
            return X, y, protected_attr
        
        # Decompose composite target
        y_resampled, protected_resampled = self._decompose_composite_target(
            composite_resampled, y, protected_attr
        )
        
        return X_resampled, y_resampled, protected_resampled
    
    def _fair_smote(self,
                   X: np.ndarray,
                   y: np.ndarray,
                   protected_attr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Fair SMOTE: Apply SMOTE separately to each protected group.
        
        This ensures synthetic samples are generated within groups,
        maintaining group-specific characteristics.
        """
        unique_groups = np.unique(protected_attr)
        unique_classes = np.unique(y)
        
        # Calculate target counts per group-class
        group_class_counts = {}
        for group in unique_groups:
            for cls in unique_classes:
                mask = (protected_attr == group) & (y == cls)
                group_class_counts[(group, cls)] = np.sum(mask)
        
        max_count = max(group_class_counts.values())
        target_count = int(max_count * self.target_ratio)
        
        # Process each group separately
        X_groups = []
        y_groups = []
        protected_groups = []
        
        for group in unique_groups:
            group_mask = protected_attr == group
            X_group = X[group_mask]
            y_group = y[group_mask]
            
            if len(X_group) == 0:
                continue
            
            # Determine sampling strategy for this group
            group_strategy = {}
            for cls in unique_classes:
                cls_count = np.sum(y_group == cls)
                if cls_count > 0 and cls_count < target_count:
                    group_strategy[cls] = target_count
            
            # Apply SMOTE to this group if needed
            if group_strategy:
                try:
                    min_samples = min(np.bincount(y_group))
                    k_neighbors = min(self.k_neighbors, min_samples - 1) if min_samples > 1 else 1
                    
                    sampler = SMOTE(
                        sampling_strategy=group_strategy,
                        k_neighbors=k_neighbors,
                        random_state=self.random_state
                    )
                    X_group_aug, y_group_aug = sampler.fit_resample(X_group, y_group)
                except Exception as e:
                    logger.warning(f"Fair SMOTE failed for group {group}: {e}")
                    X_group_aug, y_group_aug = X_group, y_group
            else:
                X_group_aug, y_group_aug = X_group, y_group
            
            # Store augmented group data
            X_groups.append(X_group_aug)
            y_groups.append(y_group_aug)
            protected_groups.append(np.full(len(y_group_aug), group))
        
        # Combine all groups
        X_combined = np.vstack(X_groups)
        y_combined = np.concatenate(y_groups)
        protected_combined = np.concatenate(protected_groups)
        
        return X_combined, y_combined, protected_combined
    
    def _create_composite_target(self,
                                 y: np.ndarray,
                                 protected_attr: np.ndarray) -> np.ndarray:
        """Create composite target from y and protected_attr"""
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
    
    def _determine_sampling_strategy(self, composite_target: np.ndarray) -> Dict:
        """Determine sampling strategy for composite target"""
        unique, counts = np.unique(composite_target, return_counts=True)
        max_count = max(counts)
        target_count = int(max_count * self.target_ratio)
        
        sampling_strategy = {}
        for val, count in zip(unique, counts):
            if count < target_count:
                sampling_strategy[int(val)] = target_count
        
        return sampling_strategy
    
    def _calculate_distribution(self, protected_attr: np.ndarray) -> Dict[str, int]:
        """Calculate group distribution"""
        unique, counts = np.unique(protected_attr, return_counts=True)
        return {str(g): int(c) for g, c in zip(unique, counts)}
