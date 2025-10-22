"""
Preprocessing-based bias mitigation techniques.

This module provides data-level bias mitigation methods that work
before model training. These techniques modify the training data to
reduce bias while preserving utility.

Available Techniques:
- Reweighting: Adjust sample weights by protected groups
- Resampling: Over/undersample to balance group representation
- Data Augmentation: Generate synthetic samples (SMOTE, ADASYN)
- Feature Transformation: Remove or decorrelate biased features
- Bias Removal: Unified engine with auto-selection

Author: REGIQ AI/ML Team
Phase: 3.5.1 - Preprocessing Mitigation
"""

from .reweighting import SampleReweighter
from .resampling import FairnessResampler
from .data_augmentation import FairDataAugmenter
from .feature_transformation import FeatureTransformer
from .bias_removal import BiasRemovalEngine

__all__ = [
    'SampleReweighter',
    'FairnessResampler',
    'FairDataAugmenter',
    'FeatureTransformer',
    'BiasRemovalEngine',
]
