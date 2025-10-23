"""
Risk Simulator Models Package

This package contains all risk modeling components for the REGIQ Risk Simulation Engine.

Phase 4.2 - Risk Modeling:
- 4.2.1 Regulatory Risk Models (4 modules)
- 4.2.2 Financial Impact Models (4 modules)  
- 4.2.3 Operational Risk Models (4 modules)

Total: 12 production modules with comprehensive risk assessment capabilities.
"""

# 4.2.1 Regulatory Risk Models
from .regulatory_risk import (
    ViolationProbabilityModel,
    ViolationFrequencyModel,
    ViolationSeverityClassifier,
    RegulatoryRiskAssessor,
    RegulatoryRiskResult,
    ViolationSeverity,
    JurisdictionType
)

from .penalty_calculator import (
    BasePenaltyCalculator,
    TieredPenaltyCalculator,
    ProportionalPenaltyCalculator,
    DailyPenaltyCalculator,
    PenaltyAggregator,
    PenaltyResult,
    PenaltyTier,
    PenaltyType
)

from .timeline_model import (
    TimeToDetectionModel,
    TimeToRemediationModel,
    ViolationForecastModel,
    RegulatoryResponseTimeModel,
    TimelineResult,
    ForecastResult,
    TimelinePhase
)

from .uncertainty_quantification import (
    SensitivityAnalyzer,
    ScenarioAnalyzer,
    UncertaintyPropagator,
    SensitivityResult,
    ScenarioResult,
    UncertaintyResult,
    SensitivityMethod,
    ScenarioType
)

# 4.2.2 Financial Impact Models
from .financial_impact import (
    PotentialFineCalculator,
    BusinessDisruptionModel,
    FinancialImpactAggregator,
    FineEstimate,
    DisruptionCost,
    FinancialImpactResult,
    FineCategory,
    DisruptionSeverity
)

from .business_disruption import (
    OperationalDisruptionModel,
    SupplyChainImpactModel,
    MarketConsequenceModel,
    IntegratedDisruptionAnalyzer,
    OperationalImpact,
    SupplyChainImpact,
    MarketImpact,
    OperationalPhase,
    SupplyChainTier
)

from .remediation_costs import (
    TechnicalRemediationEstimator,
    ProcessImprovementEstimator,
    TrainingCostEstimator,
    OngoingComplianceEstimator,
    ComprehensiveRemediationPlanner,
    RemediationEstimate,
    RemediationType,
    ComplexityLevel
)

from .roi_calculator import (
    NPVCalculator,
    IRRCalculator,
    PaybackAnalyzer,
    CostBenefitAnalyzer,
    RiskAdjustedROICalculator,
    NPVResult,
    ROIAnalysis,
    DiscountMethod
)

# 4.2.3 Operational Risk Models
from .operational_risk import (
    SystemDowntimeModel,
    PerformanceDegradationModel,
    CapacityUtilizationModel,
    OperationalRiskAggregator,
    DowntimeImpact,
    PerformanceImpact,
    OperationalRiskResult,
    SystemCriticality,
    DowntimeCategory
)

from .resource_requirements import (
    PersonnelRequirementsEstimator,
    TechnologyResourceEstimator,
    ResourcePlanningModel,
    ResourceEstimate,
    ResourceType,
    SkillLevel
)

from .implementation_time import (
    PERTEstimator,
    CriticalPathAnalyzer,
    TimelineSimulator,
    PERTEstimate,
    TaskPriority
)

from .capacity_constraints import (
    QueueTheoryModel,
    BottleneckAnalyzer,
    CapacityPlanningModel,
    QueueAnalysis
)

__all__ = [
    # Regulatory Risk Models
    'ViolationProbabilityModel',
    'ViolationFrequencyModel',
    'ViolationSeverityClassifier',
    'RegulatoryRiskAssessor',
    'RegulatoryRiskResult',
    'ViolationSeverity',
    'JurisdictionType',
    'BasePenaltyCalculator',
    'TieredPenaltyCalculator',
    'ProportionalPenaltyCalculator',
    'DailyPenaltyCalculator',
    'PenaltyAggregator',
    'PenaltyResult',
    'PenaltyTier',
    'PenaltyType',
    'TimeToDetectionModel',
    'TimeToRemediationModel',
    'ViolationForecastModel',
    'RegulatoryResponseTimeModel',
    'TimelineResult',
    'ForecastResult',
    'TimelinePhase',
    'SensitivityAnalyzer',
    'ScenarioAnalyzer',
    'UncertaintyPropagator',
    'SensitivityResult',
    'ScenarioResult',
    'UncertaintyResult',
    'SensitivityMethod',
    'ScenarioType',
    # Financial Impact Models
    'PotentialFineCalculator',
    'BusinessDisruptionModel',
    'FinancialImpactAggregator',
    'FineEstimate',
    'DisruptionCost',
    'FinancialImpactResult',
    'FineCategory',
    'DisruptionSeverity',
    'OperationalDisruptionModel',
    'SupplyChainImpactModel',
    'MarketConsequenceModel',
    'IntegratedDisruptionAnalyzer',
    'OperationalImpact',
    'SupplyChainImpact',
    'MarketImpact',
    'OperationalPhase',
    'SupplyChainTier',
    'TechnicalRemediationEstimator',
    'ProcessImprovementEstimator',
    'TrainingCostEstimator',
    'OngoingComplianceEstimator',
    'ComprehensiveRemediationPlanner',
    'RemediationEstimate',
    'RemediationType',
    'ComplexityLevel',
    'NPVCalculator',
    'IRRCalculator',
    'PaybackAnalyzer',
    'CostBenefitAnalyzer',
    'RiskAdjustedROICalculator',
    'NPVResult',
    'ROIAnalysis',
    'DiscountMethod',
    # Operational Risk Models
    'SystemDowntimeModel',
    'PerformanceDegradationModel',
    'CapacityUtilizationModel',
    'OperationalRiskAggregator',
    'DowntimeImpact',
    'PerformanceImpact',
    'OperationalRiskResult',
    'SystemCriticality',
    'DowntimeCategory',
    'PersonnelRequirementsEstimator',
    'TechnologyResourceEstimator',
    'ResourcePlanningModel',
    'ResourceEstimate',
    'ResourceType',
    'SkillLevel',
    'PERTEstimator',
    'CriticalPathAnalyzer',
    'TimelineSimulator',
    'PERTEstimate',
    'TaskPriority',
    'QueueTheoryModel',
    'BottleneckAnalyzer',
    'CapacityPlanningModel',
    'QueueAnalysis',
]
