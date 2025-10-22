"""
Sample reweighting for bias mitigation.

Adjusts sample weights to balance representation across protected groups,
ensuring fair treatment during model training.

Author: REGIQ AI/ML Team
Phase: 3.5.1 - Preprocessing Mitigation
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ReweightingResult:
    """Result of sample reweighting operation"""
    weights: np.ndarray
    original_distribution: Dict[str, float]
    weighted_distribution: Dict[str, float]
    balance_ratio: float
    metadata: Dict


class SampleReweighter:
    """
    Reweight samples to balance protected group representation.
    
    Uses inverse frequency weighting to give higher weights to
    underrepresented groups and lower weights to overrepresented groups.
    
    Supports both binary and multi-class classification.
    """
    
    def __init__(self, 
                 method: str = 'inverse_frequency',
                 normalize: bool = True,
                 min_weight: float = 0.1,
                 max_weight: float = 10.0):
        """
        Initialize sample reweighter.
        
        Args:
            method: Weighting method ('inverse_frequency', 'balanced')
            normalize: Whether to normalize weights to sum to n_samples
            min_weight: Minimum allowed weight value
            max_weight: Maximum allowed weight value
        """
        self.method = method
        self.normalize = normalize
        self.min_weight = min_weight
        self.max_weight = max_weight
        
        self.group_weights_: Optional[Dict] = None
        self.is_fitted_ = False
    
    def fit(self, 
            y: np.ndarray, 
            protected_attr: np.ndarray) -> 'SampleReweighter':
        """
        Compute weights for each protected group.
        
        Args:
            y: Target labels
            protected_attr: Protected attribute values
            
        Returns:
            self
        """
        logger.info(f"Computing sample weights using {self.method} method")
        
        # Calculate group-class distributions
        unique_groups = np.unique(protected_attr)
        unique_classes = np.unique(y)
        
        group_class_counts = {}
        for group in unique_groups:
            group_mask = protected_attr == group
            group_y = y[group_mask]
            
            for cls in unique_classes:
                key = (group, cls)
                group_class_counts[key] = np.sum(group_y == cls)
        
        # Calculate weights based on method
        if self.method == 'inverse_frequency':
            self.group_weights_ = self._inverse_frequency_weights(
                group_class_counts, unique_groups, unique_classes, len(y)
            )
        elif self.method == 'balanced':
            self.group_weights_ = self._balanced_weights(
                group_class_counts, unique_groups, unique_classes
            )
        else:
            raise ValueError(f"Unknown weighting method: {self.method}")
        
        self.is_fitted_ = True
        logger.info(f"Computed weights for {len(unique_groups)} groups")
        
        return self
    
    def transform(self, 
                  y: np.ndarray, 
                  protected_attr: np.ndarray) -> ReweightingResult:
        """
        Apply computed weights to samples.
        
        Args:
            y: Target labels
            protected_attr: Protected attribute values
            
        Returns:
            ReweightingResult with weights and statistics
        """
        if not self.is_fitted_ or self.group_weights_ is None:
            raise ValueError("Reweighter must be fitted before transform")
        
        # Assign weights to each sample
        weights = np.zeros(len(y))
        
        for i in range(len(y)):
            group = protected_attr[i]
            cls = y[i]
            key = (group, cls)
            weights[i] = self.group_weights_.get(key, 1.0)
        
        # Clip weights to valid range
        weights = np.clip(weights, self.min_weight, self.max_weight)
        
        # Normalize if requested
        if self.normalize:
            weights = weights * (len(weights) / np.sum(weights))
        
        # Calculate distributions
        original_dist = self._calculate_distribution(y, protected_attr, None)
        weighted_dist = self._calculate_distribution(y, protected_attr, weights)
        
        # Calculate balance ratio (closer to 1.0 = more balanced)
        balance_ratio = float(self._calculate_balance_ratio(weighted_dist))
        
        logger.info(f"Applied weights. Balance ratio: {balance_ratio:.3f}")
        
        return ReweightingResult(
            weights=weights,
            original_distribution=original_dist,
            weighted_distribution=weighted_dist,
            balance_ratio=balance_ratio,
            metadata={
                'method': self.method,
                'n_samples': len(weights),
                'weight_range': [float(weights.min()), float(weights.max())],
                'mean_weight': float(weights.mean())
            }
        )
    
    def fit_transform(self, 
                      y: np.ndarray, 
                      protected_attr: np.ndarray) -> ReweightingResult:
        """Fit and transform in one step"""
        return self.fit(y, protected_attr).transform(y, protected_attr)
    
    def _inverse_frequency_weights(self, 
                                   group_class_counts: Dict,
                                   unique_groups: np.ndarray,
                                   unique_classes: np.ndarray,
                                   total_samples: int) -> Dict:
        """Calculate inverse frequency weights"""
        weights = {}
        
        for group in unique_groups:
            for cls in unique_classes:
                key = (group, cls)
                count = group_class_counts.get(key, 0)
                
                if count > 0:
                    # Weight = total_samples / (n_groups * n_classes * count)
                    weight = total_samples / (len(unique_groups) * len(unique_classes) * count)
                    weights[key] = weight
                else:
                    weights[key] = 1.0
        
        return weights
    
    def _balanced_weights(self, 
                         group_class_counts: Dict,
                         unique_groups: np.ndarray,
                         unique_classes: np.ndarray) -> Dict:
        """Calculate balanced weights (sklearn-style)"""
        weights = {}
        
        # Calculate per-class weights
        class_weights = {}
        for cls in unique_classes:
            total_cls = sum(group_class_counts.get((g, cls), 0) for g in unique_groups)
            if total_cls > 0:
                class_weights[cls] = len(unique_classes) / total_cls
            else:
                class_weights[cls] = 1.0
        
        # Calculate per-group weights
        group_weights = {}
        for group in unique_groups:
            total_group = sum(group_class_counts.get((group, c), 0) for c in unique_classes)
            if total_group > 0:
                group_weights[group] = len(unique_groups) / total_group
            else:
                group_weights[group] = 1.0
        
        # Combine class and group weights
        for group in unique_groups:
            for cls in unique_classes:
                key = (group, cls)
                weights[key] = class_weights[cls] * group_weights[group]
        
        return weights
    
    def _calculate_distribution(self, 
                               y: np.ndarray,
                               protected_attr: np.ndarray,
                               weights: Optional[np.ndarray]) -> Dict[str, float]:
        """Calculate group distribution (weighted or unweighted)"""
        unique_groups = np.unique(protected_attr)
        distribution = {}
        
        if weights is None:
            # Unweighted distribution
            for group in unique_groups:
                count = np.sum(protected_attr == group)
                distribution[str(group)] = float(count / len(protected_attr))
        else:
            # Weighted distribution
            total_weight = np.sum(weights)
            for group in unique_groups:
                group_mask = protected_attr == group
                group_weight = np.sum(weights[group_mask])
                distribution[str(group)] = float(group_weight / total_weight)
        
        return distribution
    
    def _calculate_balance_ratio(self, distribution: Dict[str, float]) -> float:
        """
        Calculate how balanced the distribution is.
        Returns value between 0 and 1 (1 = perfectly balanced)
        """
        proportions = list(distribution.values())
        if len(proportions) == 0:
            return 0.0
        
        # Calculate coefficient of variation
        mean_prop = np.mean(proportions)
        if mean_prop == 0:
            return 0.0
        
        std_prop = np.std(proportions)
        cv = std_prop / mean_prop
        
        # Convert to balance ratio (0 = unbalanced, 1 = balanced)
        balance_ratio = 1.0 / (1.0 + cv)
        
        return balance_ratio
    
    def get_weights_summary(self) -> Dict:
        """Get summary of computed weights"""
        if not self.is_fitted_ or self.group_weights_ is None:
            raise ValueError("Reweighter must be fitted first")
        
        return {
            'n_groups': len(set(k[0] for k in self.group_weights_.keys())),
            'n_classes': len(set(k[1] for k in self.group_weights_.keys())),
            'weight_range': [
                float(min(self.group_weights_.values())),
                float(max(self.group_weights_.values()))
            ],
            'mean_weight': float(np.mean(list(self.group_weights_.values()))),
            'method': self.method
        }
