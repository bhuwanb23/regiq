#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Analysis Module Tests
Comprehensive test suite for bias analysis service.

Tests cover:
    - Metrics module (4 fairness analyzers)
    - Explainability module (SHAP/LIME)
    - Visualization module (BiasVisualizer with 7 chart types)
    - Integration tests for complete pipeline

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .test_metrics import *
from .test_explainability import *
from .test_visualization import *
from .test_integration import *
