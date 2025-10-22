#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Mitigation Strategies
Preprocessing, in-processing, and post-processing bias mitigation techniques.
"""

from .preprocessing import (
    SampleReweighter,
    FairnessResampler,
    FairDataAugmenter,
    FeatureTransformer,
    BiasRemovalEngine
)

from .validation import (
    MitigationValidator,
    ValidationReport
)

__all__ = [
    # Preprocessing
    "SampleReweighter",
    "FairnessResampler",
    "FairDataAugmenter",
    "FeatureTransformer",
    "BiasRemovalEngine",
    
    # Validation
    "MitigationValidator",
    "ValidationReport",
]

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"
