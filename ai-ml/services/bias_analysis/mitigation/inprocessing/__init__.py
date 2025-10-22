"""
In-processing-based bias mitigation techniques.

This module provides algorithm-level bias mitigation methods that work
during model training by incorporating fairness constraints directly into
the learning process.

Available Techniques:
- Fairness Constraints: Demographic parity, equalized odds (Fairlearn)
- Adversarial Debiasing: Neural network-based debiasing (AIF360)
- Fair Classifiers: Custom fair training algorithms
- In-processing Engine: Unified interface with auto-selection

Author: REGIQ AI/ML Team
Phase: 3.5.2 - In-processing Mitigation
"""

from .fairness_constraints import (
    FairnessConstrainedClassifier,
    ConstraintType,
    OptimizationAlgorithm
)
from .adversarial_debiasing import AdversarialDebiaser
from .fair_classifiers import (
    FairLogisticRegression,
    FairGradientBoosting
)
from .inprocessing_engine import InprocessingEngine

__all__ = [
    # Fairness Constraints
    'FairnessConstrainedClassifier',
    'ConstraintType',
    'OptimizationAlgorithm',
    
    # Adversarial Debiasing
    'AdversarialDebiaser',
    
    # Fair Classifiers
    'FairLogisticRegression',
    'FairGradientBoosting',
    
    # Unified Engine
    'InprocessingEngine',
]
