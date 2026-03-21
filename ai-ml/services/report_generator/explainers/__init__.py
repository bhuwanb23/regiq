#!/usr/bin/env python3
"""
REGIQ AI/ML - Report Explainers Module
Bridges SHAP/LIME/fairness/risk outputs into audience-ready HTML sections.

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .report_explainers import (
    ReportExplainerFactory,
    SHAPExplainer,
    LIMEExplainer,
    FairnessExplainer,
    RiskSimulationExplainer,
)

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    "ReportExplainerFactory",
    "SHAPExplainer",
    "LIMEExplainer",
    "FairnessExplainer",
    "RiskSimulationExplainer",
]
