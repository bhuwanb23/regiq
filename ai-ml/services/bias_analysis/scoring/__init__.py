#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Scoring System
Composite bias scoring, risk classification, and alert management.
"""

from .scoring_algorithm import BiasScoreAlgorithm
from .weight_profiles import WeightProfileManager
from .composite_calculator import BiasScoreCalculator
from .score_interpreter import ScoreInterpreter
from .risk_levels import RiskLevel, RISK_THRESHOLDS, RISK_METADATA
from .classification_engine import RiskClassifier
from .alert_system import BiasAlertManager
from .report_generator import BiasRiskReportGenerator

__all__ = [
    "BiasScoreAlgorithm",
    "WeightProfileManager",
    "BiasScoreCalculator",
    "ScoreInterpreter",
    "RiskLevel",
    "RISK_THRESHOLDS",
    "RISK_METADATA",
    "RiskClassifier",
    "BiasAlertManager",
    "BiasRiskReportGenerator",
]

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"
