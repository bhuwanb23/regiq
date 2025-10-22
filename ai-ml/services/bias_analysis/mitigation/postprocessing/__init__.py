"""
Post-processing-based bias mitigation techniques.

This module provides output-level bias mitigation methods that work
after model training by adjusting predictions and decision thresholds
to improve fairness.

Available Techniques:
- Threshold Optimization: Per-group threshold adjustment for fairness
- Calibration: Group-aware probability calibration
- Equalized Odds Post-processing: Fairlearn's EO postprocessor
- Post-processing Engine: Unified interface with auto-selection

Author: REGIQ AI/ML Team
Phase: 3.5.3 - Post-processing Mitigation
"""

from .threshold_optimizer import (
    ThresholdOptimizer,
    OptimizationObjective,
    ThresholdOptimizationResult
)
from .calibration import (
    FairCalibrator,
    CalibrationMethod,
    CalibrationResult
)
from .equalized_odds_postprocessor import (
    EqualizedOddsPostprocessor,
    EOPostprocessingResult
)
from .postprocessing_engine import (
    PostprocessingEngine,
    PostprocessingResult
)

__all__ = [
    # Threshold Optimization
    'ThresholdOptimizer',
    'OptimizationObjective',
    'ThresholdOptimizationResult',
    
    # Calibration
    'FairCalibrator',
    'CalibrationMethod',
    'CalibrationResult',
    
    # Equalized Odds
    'EqualizedOddsPostprocessor',
    'EOPostprocessingResult',
    
    # Unified Engine
    'PostprocessingEngine',
    'PostprocessingResult',
]
