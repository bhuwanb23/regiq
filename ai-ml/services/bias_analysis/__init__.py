#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Analysis Service
Complete pipeline for AI model bias detection, mitigation, and explainability.

Pipeline:
    1. model_input      → Upload & validate model + dataset
    2. dataset_processor → Preprocess data, detect protected attributes
    3. metrics          → Calculate fairness metrics (DP, EO, Calibration, IF)
    4. explainability   → SHAP / LIME / feature attribution
    5. mitigation       → Pre / In / Post-processing bias mitigation
    6. scoring          → Composite bias score, risk classification, alerts
    7. visualization    → Charts and dashboards for reports
    8. utils            → Model persistence (save/load trained mitigators)

Integration:
    Results from this service feed directly into:
    - report_generator (via FairnessExplainer, ReportOutputGenerator)
    - risk_simulator   (bias risk probability inputs)

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

# ── Dataset & Model Input ──────────────────────────────────────────────── #
from .dataset_processor import (
    DatasetProcessor,
    DatasetMetadata,
    ProtectedAttributeInfo,
    DatasetProcessingConfig,
)
from .model_input import (
    ModelUploader,
    ModelMetadata,
    ModelUploadConfig,
)

# ── Fairness Metrics ───────────────────────────────────────────────────── #
from .metrics import (
    DemographicParityAnalyzer,
    DemographicParityResult,
    ParityThreshold,
    EqualizedOddsAnalyzer,
    EqualizedOddsResult,
    EqualizedOddsThreshold,
    CalibrationAnalyzer,
    CalibrationResult,
    CalibrationThreshold,
    IndividualFairnessAnalyzer,
    IndividualFairnessResult,
    IndividualFairnessThreshold,
)

# ── Explainability ─────────────────────────────────────────────────────── #
from .explainability import (
    SHAPExplainer,
    SHAPExplanation,
    SHAPConfig,
    LIMEExplainer,
    LIMEExplanation,
    LIMEConfig,
    FeatureAttributionAnalyzer,
    FeatureAttribution,
    AttributionConfig,
)

# ── Mitigation ─────────────────────────────────────────────────────────── #
from .mitigation import (
    # Preprocessing
    SampleReweighter,
    FairnessResampler,
    FairDataAugmenter,
    FeatureTransformer,
    BiasRemovalEngine,
    # In-processing
    FairnessConstrainedClassifier,
    ConstraintType,
    OptimizationAlgorithm,
    AdversarialDebiaser,
    FairLogisticRegression,
    FairGradientBoosting,
    InprocessingEngine,
    # Validation
    MitigationValidator,
    ValidationReport,
)

# ── Scoring ────────────────────────────────────────────────────────────── #
from .scoring import (
    BiasScoreAlgorithm,
    WeightProfileManager,
    BiasScoreCalculator,
    ScoreInterpreter,
    RiskLevel,
    RISK_THRESHOLDS,
    RISK_METADATA,
    RiskClassifier,
    BiasAlertManager,
    BiasRiskReportGenerator,
)

# ── Visualization ──────────────────────────────────────────────────────── #
from .visualization import BiasVisualizer

# ── Persistence Utilities ──────────────────────────────────────────────── #
from .utils.fairness_model_persistence import (
    FairnessModelPersistence,
    save_mitigation_model,
    load_mitigation_model,
    save_explanation_model,
    load_explanation_model,
)

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    # Dataset & Model Input
    "DatasetProcessor", "DatasetMetadata", "ProtectedAttributeInfo", "DatasetProcessingConfig",
    "ModelUploader", "ModelMetadata", "ModelUploadConfig",
    # Metrics
    "DemographicParityAnalyzer", "DemographicParityResult", "ParityThreshold",
    "EqualizedOddsAnalyzer", "EqualizedOddsResult", "EqualizedOddsThreshold",
    "CalibrationAnalyzer", "CalibrationResult", "CalibrationThreshold",
    "IndividualFairnessAnalyzer", "IndividualFairnessResult", "IndividualFairnessThreshold",
    # Explainability
    "SHAPExplainer", "SHAPExplanation", "SHAPConfig",
    "LIMEExplainer", "LIMEExplanation", "LIMEConfig",
    "FeatureAttributionAnalyzer", "FeatureAttribution", "AttributionConfig",
    # Mitigation
    "SampleReweighter", "FairnessResampler", "FairDataAugmenter",
    "FeatureTransformer", "BiasRemovalEngine",
    "FairnessConstrainedClassifier", "ConstraintType", "OptimizationAlgorithm",
    "AdversarialDebiaser", "FairLogisticRegression", "FairGradientBoosting",
    "InprocessingEngine", "MitigationValidator", "ValidationReport",
    # Scoring
    "BiasScoreAlgorithm", "WeightProfileManager", "BiasScoreCalculator",
    "ScoreInterpreter", "RiskLevel", "RISK_THRESHOLDS", "RISK_METADATA",
    "RiskClassifier", "BiasAlertManager", "BiasRiskReportGenerator",
    # Visualization
    "BiasVisualizer",
    # Persistence
    "FairnessModelPersistence", "save_mitigation_model", "load_mitigation_model",
    "save_explanation_model", "load_explanation_model",
]