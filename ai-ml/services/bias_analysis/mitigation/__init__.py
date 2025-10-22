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

from .inprocessing import (
    FairnessConstrainedClassifier,
    ConstraintType,
    OptimizationAlgorithm,
    AdversarialDebiaser,
    FairLogisticRegression,
    FairGradientBoosting,
    InprocessingEngine
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
    
    # In-processing
    "FairnessConstrainedClassifier",
    "ConstraintType",
    "OptimizationAlgorithm",
    "AdversarialDebiaser",
    "FairLogisticRegression",
    "FairGradientBoosting",
    "InprocessingEngine",
    
    # Validation
    "MitigationValidator",
    "ValidationReport",
]

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"
