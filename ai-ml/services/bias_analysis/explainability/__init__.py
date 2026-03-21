#!/usr/bin/env python3
"""
REGIQ AI/ML - Model Explainability
SHAP, LIME, and feature attribution for bias analysis explainability.

Modules:
    - SHAPExplainer: TreeExplainer / KernelExplainer integration
    - LIMEExplainer: Local surrogate model explanations
    - FeatureAttributionAnalyzer: Unified feature importance ranking

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .shap_integration import (
    SHAPExplainer,
    SHAPExplanation,
    SHAPConfig,
)
from .lime_implementation import (
    LIMEExplainer,
    LIMEExplanation,
    LIMEConfig,
)
from .feature_attribution import (
    FeatureAttributionAnalyzer,
    FeatureAttribution,
    AttributionConfig,
)

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    # SHAP
    "SHAPExplainer",
    "SHAPExplanation",
    "SHAPConfig",
    # LIME
    "LIMEExplainer",
    "LIMEExplanation",
    "LIMEConfig",
    # Feature Attribution
    "FeatureAttributionAnalyzer",
    "FeatureAttribution",
    "AttributionConfig",
]