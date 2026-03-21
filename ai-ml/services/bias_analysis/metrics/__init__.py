#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias & Fairness Metrics
Comprehensive fairness metric calculation for AI model auditing.

Metrics:
    - Demographic Parity: Group-level positive prediction rate equality
    - Equalized Odds: TPR and FPR equality across groups
    - Calibration: Predicted probability vs actual outcome alignment
    - Individual Fairness: Similar individuals receive similar predictions

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .demographic_parity import (
    DemographicParityAnalyzer,
    DemographicParityResult,
    ParityThreshold,
)
from .equalized_odds import (
    EqualizedOddsAnalyzer,
    EqualizedOddsResult,
    EqualizedOddsThreshold,
)
from .calibration_analysis import (
    CalibrationAnalyzer,
    CalibrationResult,
    CalibrationThreshold,
)
from .individual_fairness import (
    IndividualFairnessAnalyzer,
    IndividualFairnessResult,
    IndividualFairnessThreshold,
)

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    # Demographic Parity
    "DemographicParityAnalyzer",
    "DemographicParityResult",
    "ParityThreshold",
    # Equalized Odds
    "EqualizedOddsAnalyzer",
    "EqualizedOddsResult",
    "EqualizedOddsThreshold",
    # Calibration
    "CalibrationAnalyzer",
    "CalibrationResult",
    "CalibrationThreshold",
    # Individual Fairness
    "IndividualFairnessAnalyzer",
    "IndividualFairnessResult",
    "IndividualFairnessThreshold",
]