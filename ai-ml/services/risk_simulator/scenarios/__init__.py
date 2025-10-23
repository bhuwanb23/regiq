"""
Risk Simulator Scenarios Package

This package provides comprehensive scenario generation and stress testing capabilities
for regulatory compliance risk simulation.

Modules:
- regulatory_scenarios: Regulatory change scenario generation
- enforcement_scenarios: Enforcement variation modeling  
- market_scenarios: Market condition simulation
- external_factors: External event modeling
- stress_scenarios: Stress test scenario design
- extreme_conditions: Extreme condition simulation
- resilience_tester: System resilience testing
- stress_reporter: Stress test report generation
- scenario_engine: Unified scenario orchestration

All scenarios integrate with Phase 4.2 risk models.
"""

# Regulatory Scenarios
from .regulatory_scenarios import (
    RegulationType,
    RegulationSeverity,
    ImplementationTimeline,
    RegulatoryChange,
    RegulatoryScenario,
    RegulationChangeScenario,
    JurisdictionScenarioGenerator
)

# Enforcement Scenarios
from .enforcement_scenarios import (
    EnforcementRegime,
    EnforcementFocus,
    EnforcementTrend,
    EnforcementPeriod,
    EnforcementScenario,
    EnforcementPatternModel,
    PenaltyEscalationSimulator
)

# Market Scenarios
from .market_scenarios import (
    EconomicCondition,
    MarketVolatility,
    IndustryTrend,
    MarketConditions,
    MarketScenario,
    EconomicScenarioGenerator,
    CompetitiveLandscapeSimulator
)

# External Factors
from .external_factors import (
    EventType,
    EventSeverity,
    ExternalEvent,
    ExternalEventSimulator,
    BlackSwanEventGenerator
)

# Stress Scenarios
from .stress_scenarios import (
    StressLevel,
    StressCategory,
    StressFactor,
    StressTestScenario,
    StressScenarioDesigner,
    HistoricalCrisisReplicator
)

# Extreme Conditions
from .extreme_conditions import (
    ExtremeScenarioType,
    ResourceType,
    ExtremeCondition,
    BreakingPoint,
    ExtremeConditionSimulator,
    BreakingPointAnalyzer
)

# Resilience Testing
from .resilience_tester import (
    ResilienceLevel,
    MitigationStrategy,
    ResilienceScore,
    RecoveryEstimate,
    ResilienceAnalyzer,
    ContingencyValidator
)

# Stress Reporting
from .stress_reporter import (
    ReportType,
    Priority,
    VulnerabilityReport,
    StressTestReportGenerator,
    ExecutiveSummaryGenerator
)

# Scenario Engine
from .scenario_engine import (
    IndustryTemplate,
    CombinedScenarioResult,
    ScenarioOrchestrator,
    ScenarioLibrary
)

__all__ = [
    # Regulatory
    'RegulationType',
    'RegulationSeverity',
    'ImplementationTimeline',
    'RegulatoryChange',
    'RegulatoryScenario',
    'RegulationChangeScenario',
    'JurisdictionScenarioGenerator',
    # Enforcement
    'EnforcementRegime',
    'EnforcementFocus',
    'EnforcementTrend',
    'EnforcementPeriod',
    'EnforcementScenario',
    'EnforcementPatternModel',
    'PenaltyEscalationSimulator',
    # Market
    'EconomicCondition',
    'MarketVolatility',
    'IndustryTrend',
    'MarketConditions',
    'MarketScenario',
    'EconomicScenarioGenerator',
    'CompetitiveLandscapeSimulator',
    # External
    'EventType',
    'EventSeverity',
    'ExternalEvent',
    'ExternalEventSimulator',
    'BlackSwanEventGenerator',
    # Stress
    'StressLevel',
    'StressCategory',
    'StressFactor',
    'StressTestScenario',
    'StressScenarioDesigner',
    'HistoricalCrisisReplicator',
    # Extreme
    'ExtremeScenarioType',
    'ResourceType',
    'ExtremeCondition',
    'BreakingPoint',
    'ExtremeConditionSimulator',
    'BreakingPointAnalyzer',
    # Resilience
    'ResilienceLevel',
    'MitigationStrategy',
    'ResilienceScore',
    'RecoveryEstimate',
    'ResilienceAnalyzer',
    'ContingencyValidator',
    # Reporting
    'ReportType',
    'Priority',
    'VulnerabilityReport',
    'StressTestReportGenerator',
    'ExecutiveSummaryGenerator',
    # Engine
    'IndustryTemplate',
    'CombinedScenarioResult',
    'ScenarioOrchestrator',
    'ScenarioLibrary'
]

__version__ = '1.0.0'
