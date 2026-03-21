#!/usr/bin/env python3
"""
REGIQ AI/ML - Risk Simulator Service
Algorithmic compliance risk simulation using Monte Carlo, Bayesian inference,
and stress testing — no pre-trained models required.

Pipeline:
    1. regulations  → Regulatory framework definitions and penalty parameters
    2. models       → Risk models (regulatory, financial, operational)
    3. simulation   → Monte Carlo + Bayesian + MCMC + diagnostics
    4. scenarios    → Scenario generation and stress testing
    5. visualization → Heatmaps, distributions, timelines, export

Quick Start:
    from services.risk_simulator.simulation import MonteCarloSimulator, SamplingMethod
    from services.risk_simulator.regulations import get_simulation_params

    params = get_simulation_params('eu_ai_act')
    simulator = MonteCarloSimulator(n_simulations=10000)
    result = simulator.run(params)

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

# ── Regulations ────────────────────────────────────────────────────────── #
from .regulations import (
    RegulatoryFramework,
    PenaltyRange,
    REGULATORY_FRAMEWORKS,
    get_framework,
    get_frameworks_by_jurisdiction,
    get_frameworks_by_type,
    get_ai_frameworks,
    get_high_risk_frameworks,
    get_framework_ids,
    get_penalty_range,
    get_simulation_params,
    list_all_frameworks,
    get_registry_stats,
)

# ── Risk Models ────────────────────────────────────────────────────────── #
from .models import (
    # Regulatory Risk
    ViolationProbabilityModel, ViolationFrequencyModel,
    ViolationSeverityClassifier, RegulatoryRiskAssessor,
    RegulatoryRiskResult, ViolationSeverity, JurisdictionType,
    # Penalty
    BasePenaltyCalculator, TieredPenaltyCalculator,
    ProportionalPenaltyCalculator, DailyPenaltyCalculator,
    PenaltyAggregator, PenaltyResult, PenaltyTier, PenaltyType,
    # Timeline
    TimeToDetectionModel, TimeToRemediationModel,
    ViolationForecastModel, RegulatoryResponseTimeModel,
    TimelineResult, ForecastResult, TimelinePhase,
    # Uncertainty
    SensitivityAnalyzer, ScenarioAnalyzer, UncertaintyPropagator,
    SensitivityResult, ScenarioResult, UncertaintyResult,
    SensitivityMethod, ScenarioType,
    # Financial Impact
    PotentialFineCalculator, BusinessDisruptionModel,
    FinancialImpactAggregator, FineEstimate, DisruptionCost,
    FinancialImpactResult, FineCategory, DisruptionSeverity,
    # Business Disruption
    OperationalDisruptionModel, SupplyChainImpactModel,
    MarketConsequenceModel, IntegratedDisruptionAnalyzer,
    OperationalImpact, SupplyChainImpact, MarketImpact,
    OperationalPhase, SupplyChainTier,
    # Remediation Costs
    TechnicalRemediationEstimator, ProcessImprovementEstimator,
    TrainingCostEstimator, OngoingComplianceEstimator,
    ComprehensiveRemediationPlanner, RemediationEstimate,
    RemediationType, ComplexityLevel,
    # ROI
    NPVCalculator, IRRCalculator, PaybackAnalyzer,
    CostBenefitAnalyzer, RiskAdjustedROICalculator,
    NPVResult, ROIAnalysis, DiscountMethod,
    # Operational Risk
    SystemDowntimeModel, PerformanceDegradationModel,
    CapacityUtilizationModel, OperationalRiskAggregator,
    DowntimeImpact, PerformanceImpact, OperationalRiskResult,
    SystemCriticality, DowntimeCategory,
    # Resources
    PersonnelRequirementsEstimator, TechnologyResourceEstimator,
    ResourcePlanningModel, ResourceEstimate, ResourceType, SkillLevel,
    # Implementation
    PERTEstimator, CriticalPathAnalyzer, TimelineSimulator,
    PERTEstimate, TaskPriority,
    # Capacity
    QueueTheoryModel, BottleneckAnalyzer, CapacityPlanningModel, QueueAnalysis,
)

# ── Simulation Engine ──────────────────────────────────────────────────── #
from .simulation import (
    MonteCarloSimulator, SamplingMethod, DistributionType, SimulationResult,
    Parameter, ParameterSpace,
    BayesianRiskModel, BayesianModelResult, ComplianceViolationModel,
    PenaltyAmountModel, TimeToViolationModel, HierarchicalRiskModel, compare_models,
    MCMCSampler, MCMCConfig, MCMCSamplingResult,
    ConvergenceDiagnostics, check_convergence, geweke_test,
    compute_autocorrelation, effective_sample_size_simple, diagnose_divergences,
)

# ── Scenarios ──────────────────────────────────────────────────────────── #
from .scenarios import (
    RegulationType, RegulationSeverity, ImplementationTimeline,
    RegulatoryChange, RegulatoryScenario, RegulationChangeScenario,
    JurisdictionScenarioGenerator,
    EnforcementRegime, EnforcementFocus, EnforcementTrend,
    EnforcementPeriod, EnforcementScenario,
    EnforcementPatternModel, PenaltyEscalationSimulator,
    EconomicCondition, MarketVolatility, IndustryTrend,
    MarketConditions, MarketScenario,
    EconomicScenarioGenerator, CompetitiveLandscapeSimulator,
    EventType, EventSeverity, ExternalEvent,
    ExternalEventSimulator, BlackSwanEventGenerator,
    StressLevel, StressCategory, StressFactor,
    StressTestScenario, StressScenarioDesigner, HistoricalCrisisReplicator,
    ExtremeScenarioType, ExtremeCondition, BreakingPoint,
    ExtremeConditionSimulator, BreakingPointAnalyzer,
    ResilienceLevel, MitigationStrategy, ResilienceScore,
    RecoveryEstimate, ResilienceAnalyzer, ContingencyValidator,
    ReportType, Priority, VulnerabilityReport,
    StressTestReportGenerator, ExecutiveSummaryGenerator,
    IndustryTemplate, CombinedScenarioResult,
    ScenarioOrchestrator, ScenarioLibrary,
)

# ── Visualization ──────────────────────────────────────────────────────── #
from .visualization import (
    RiskDimension, AggregationMethod, HeatmapCell, HeatmapData, HeatmapGenerator,
    HistogramData, PDFCDFData, ConfidenceInterval,
    DistributionAnalysis, DistributionAnalyzer,
    TimelineEvent, TimeSeriesPoint, ActionPlan,
    TimelineProjection, TimelineProjector,
    ExportFormat, ExportResult, ExportManager,
    DataValidator, DataTransformer, ColorMapper, DataAggregator,
)

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    # Regulations
    "RegulatoryFramework", "PenaltyRange", "REGULATORY_FRAMEWORKS",
    "get_framework", "get_frameworks_by_jurisdiction", "get_frameworks_by_type",
    "get_ai_frameworks", "get_high_risk_frameworks", "get_framework_ids",
    "get_penalty_range", "get_simulation_params", "list_all_frameworks", "get_registry_stats",
    # Models
    "ViolationProbabilityModel", "ViolationFrequencyModel", "ViolationSeverityClassifier",
    "RegulatoryRiskAssessor", "RegulatoryRiskResult", "ViolationSeverity", "JurisdictionType",
    "BasePenaltyCalculator", "TieredPenaltyCalculator", "ProportionalPenaltyCalculator",
    "DailyPenaltyCalculator", "PenaltyAggregator", "PenaltyResult", "PenaltyTier", "PenaltyType",
    "TimeToDetectionModel", "TimeToRemediationModel", "ViolationForecastModel",
    "RegulatoryResponseTimeModel", "TimelineResult", "ForecastResult", "TimelinePhase",
    "SensitivityAnalyzer", "ScenarioAnalyzer", "UncertaintyPropagator",
    "SensitivityResult", "ScenarioResult", "UncertaintyResult", "SensitivityMethod", "ScenarioType",
    "PotentialFineCalculator", "BusinessDisruptionModel", "FinancialImpactAggregator",
    "FineEstimate", "DisruptionCost", "FinancialImpactResult", "FineCategory", "DisruptionSeverity",
    "OperationalDisruptionModel", "SupplyChainImpactModel", "MarketConsequenceModel",
    "IntegratedDisruptionAnalyzer", "OperationalImpact", "SupplyChainImpact", "MarketImpact",
    "OperationalPhase", "SupplyChainTier",
    "TechnicalRemediationEstimator", "ProcessImprovementEstimator", "TrainingCostEstimator",
    "OngoingComplianceEstimator", "ComprehensiveRemediationPlanner",
    "RemediationEstimate", "RemediationType", "ComplexityLevel",
    "NPVCalculator", "IRRCalculator", "PaybackAnalyzer", "CostBenefitAnalyzer",
    "RiskAdjustedROICalculator", "NPVResult", "ROIAnalysis", "DiscountMethod",
    "SystemDowntimeModel", "PerformanceDegradationModel", "CapacityUtilizationModel",
    "OperationalRiskAggregator", "DowntimeImpact", "PerformanceImpact",
    "OperationalRiskResult", "SystemCriticality", "DowntimeCategory",
    "PersonnelRequirementsEstimator", "TechnologyResourceEstimator",
    "ResourcePlanningModel", "ResourceEstimate", "ResourceType", "SkillLevel",
    "PERTEstimator", "CriticalPathAnalyzer", "TimelineSimulator", "PERTEstimate", "TaskPriority",
    "QueueTheoryModel", "BottleneckAnalyzer", "CapacityPlanningModel", "QueueAnalysis",
    # Simulation
    "MonteCarloSimulator", "SamplingMethod", "DistributionType", "SimulationResult",
    "Parameter", "ParameterSpace",
    "BayesianRiskModel", "BayesianModelResult", "ComplianceViolationModel",
    "PenaltyAmountModel", "TimeToViolationModel", "HierarchicalRiskModel", "compare_models",
    "MCMCSampler", "MCMCConfig", "MCMCSamplingResult",
    "ConvergenceDiagnostics", "check_convergence", "geweke_test",
    "compute_autocorrelation", "effective_sample_size_simple", "diagnose_divergences",
    # Scenarios
    "RegulationType", "RegulationSeverity", "ImplementationTimeline",
    "RegulatoryChange", "RegulatoryScenario", "RegulationChangeScenario",
    "JurisdictionScenarioGenerator",
    "EnforcementRegime", "EnforcementFocus", "EnforcementTrend",
    "EnforcementPeriod", "EnforcementScenario", "EnforcementPatternModel", "PenaltyEscalationSimulator",
    "EconomicCondition", "MarketVolatility", "IndustryTrend",
    "MarketConditions", "MarketScenario", "EconomicScenarioGenerator", "CompetitiveLandscapeSimulator",
    "EventType", "EventSeverity", "ExternalEvent", "ExternalEventSimulator", "BlackSwanEventGenerator",
    "StressLevel", "StressCategory", "StressFactor",
    "StressTestScenario", "StressScenarioDesigner", "HistoricalCrisisReplicator",
    "ExtremeScenarioType", "ExtremeCondition", "BreakingPoint",
    "ExtremeConditionSimulator", "BreakingPointAnalyzer",
    "ResilienceLevel", "MitigationStrategy", "ResilienceScore",
    "RecoveryEstimate", "ResilienceAnalyzer", "ContingencyValidator",
    "ReportType", "Priority", "VulnerabilityReport",
    "StressTestReportGenerator", "ExecutiveSummaryGenerator",
    "IndustryTemplate", "CombinedScenarioResult", "ScenarioOrchestrator", "ScenarioLibrary",
    # Visualization
    "RiskDimension", "AggregationMethod", "HeatmapCell", "HeatmapData", "HeatmapGenerator",
    "HistogramData", "PDFCDFData", "ConfidenceInterval", "DistributionAnalysis", "DistributionAnalyzer",
    "TimelineEvent", "TimeSeriesPoint", "ActionPlan", "TimelineProjection", "TimelineProjector",
    "ExportFormat", "ExportResult", "ExportManager",
    "DataValidator", "DataTransformer", "ColorMapper", "DataAggregator",
]
