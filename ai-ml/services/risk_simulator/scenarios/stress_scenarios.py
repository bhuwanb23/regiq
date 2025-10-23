"""
Stress Scenarios Module

This module implements stress test scenario design including:
- Worst-case regulatory scenarios
- Multi-factor stress combinations
- Cascade failure scenarios
- Historical crisis replays

Combines all Phase 4.2 risk models for comprehensive stress testing.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import numpy as np


class StressLevel(Enum):
    """Stress test severity levels"""
    MODERATE = "moderate"
    SEVERE = "severe"
    EXTREME = "extreme"
    CATASTROPHIC = "catastrophic"


class StressCategory(Enum):
    """Categories of stress tests"""
    REGULATORY_ONLY = "regulatory_only"
    FINANCIAL_ONLY = "financial_only"
    OPERATIONAL_ONLY = "operational_only"
    COMBINED = "combined"
    CASCADE = "cascade"


@dataclass
class StressFactor:
    """Individual stress factor"""
    factor_id: str
    factor_name: str
    factor_type: str
    severity_multiplier: float
    probability_override: Optional[float]
    impact_description: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'factor_id': self.factor_id,
            'factor_name': self.factor_name,
            'factor_type': self.factor_type,
            'severity_multiplier': float(self.severity_multiplier),
            'probability_override': float(self.probability_override) if self.probability_override else None,
            'impact_description': self.impact_description
        }


@dataclass
class StressTestScenario:
    """Complete stress test scenario"""
    scenario_id: str
    scenario_name: str
    description: str
    stress_level: str
    category: str
    stress_factors: List[StressFactor]
    time_horizon_days: int
    combined_severity_score: float
    expected_financial_impact: float
    mitigation_difficulty: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'scenario_id': self.scenario_id,
            'scenario_name': self.scenario_name,
            'description': self.description,
            'stress_level': self.stress_level,
            'category': self.category,
            'stress_factors': [f.to_dict() for f in self.stress_factors],
            'time_horizon_days': int(self.time_horizon_days),
            'combined_severity_score': float(self.combined_severity_score),
            'expected_financial_impact': float(self.expected_financial_impact),
            'mitigation_difficulty': self.mitigation_difficulty
        }


class StressScenarioDesigner:
    """Design comprehensive stress test scenarios"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def create_regulatory_worst_case(self) -> StressTestScenario:
        """Create worst-case regulatory scenario"""
        
        stress_factors = [
            StressFactor(
                factor_id="REG-STRESS-001",
                factor_name="Simultaneous Multi-Jurisdiction Regulations",
                factor_type="regulatory",
                severity_multiplier=3.5,
                probability_override=0.05,
                impact_description="New strict regulations in 5+ jurisdictions simultaneously"
            ),
            StressFactor(
                factor_id="REG-STRESS-002",
                factor_name="Aggressive Enforcement Campaign",
                factor_type="enforcement",
                severity_multiplier=4.0,
                probability_override=0.10,
                impact_description="Coordinated global enforcement with maximum penalties"
            ),
            StressFactor(
                factor_id="REG-STRESS-003",
                factor_name="Retroactive Compliance Requirements",
                factor_type="compliance",
                severity_multiplier=2.8,
                probability_override=0.03,
                impact_description="Retroactive application of new standards"
            ),
            StressFactor(
                factor_id="REG-STRESS-004",
                factor_name="Shortened Implementation Timelines",
                factor_type="timeline",
                severity_multiplier=2.5,
                probability_override=0.15,
                impact_description="30-day implementation instead of standard 180-day"
            )
        ]
        
        # Calculate combined severity
        severity_score = sum(f.severity_multiplier for f in stress_factors) * 100 / len(stress_factors)
        
        # Estimate financial impact (placeholder - would integrate with Phase 4.2)
        base_impact = 5000000  # $5M base
        financial_impact = base_impact * severity_score / 50
        
        scenario_id = f"STRESS-REG-WORST-{self.rng.randint(1000, 9999)}"
        
        return StressTestScenario(
            scenario_id=scenario_id,
            scenario_name="Regulatory Perfect Storm",
            description="Worst-case regulatory scenario with multiple simultaneous adverse factors",
            stress_level=StressLevel.CATASTROPHIC.value,
            category=StressCategory.REGULATORY_ONLY.value,
            stress_factors=stress_factors,
            time_horizon_days=365,
            combined_severity_score=severity_score,
            expected_financial_impact=financial_impact,
            mitigation_difficulty="extreme"
        )
    
    def create_multi_factor_stress(self,
                                   stress_level: StressLevel = StressLevel.SEVERE) -> StressTestScenario:
        """Create multi-factor combined stress scenario"""
        
        # Severity multipliers based on stress level
        level_mults = {
            StressLevel.MODERATE: 1.5,
            StressLevel.SEVERE: 2.5,
            StressLevel.EXTREME: 3.5,
            StressLevel.CATASTROPHIC: 5.0
        }
        base_mult = level_mults[stress_level]
        
        stress_factors = [
            StressFactor(
                factor_id="MULTI-001",
                factor_name="Economic Recession",
                factor_type="economic",
                severity_multiplier=base_mult * 0.8,
                probability_override=None,
                impact_description="Reduced budgets and resource constraints"
            ),
            StressFactor(
                factor_id="MULTI-002",
                factor_name="New Regulations",
                factor_type="regulatory",
                severity_multiplier=base_mult * 1.0,
                probability_override=None,
                impact_description="Introduction of stringent new requirements"
            ),
            StressFactor(
                factor_id="MULTI-003",
                factor_name="System Failures",
                factor_type="operational",
                severity_multiplier=base_mult * 0.7,
                probability_override=None,
                impact_description="Critical compliance system downtime"
            ),
            StressFactor(
                factor_id="MULTI-004",
                factor_name="Staff Turnover",
                factor_type="human_resources",
                severity_multiplier=base_mult * 0.6,
                probability_override=None,
                impact_description="Loss of key compliance personnel"
            ),
            StressFactor(
                factor_id="MULTI-005",
                factor_name="Market Disruption",
                factor_type="market",
                severity_multiplier=base_mult * 0.9,
                probability_override=None,
                impact_description="Competitive pressure and margin compression"
            )
        ]
        
        severity_score = sum(f.severity_multiplier for f in stress_factors) * 100 / len(stress_factors)
        financial_impact = 3000000 * base_mult
        
        scenario_id = f"STRESS-MULTI-{stress_level.value.upper()}-{self.rng.randint(1000, 9999)}"
        
        return StressTestScenario(
            scenario_id=scenario_id,
            scenario_name=f"Multi-Factor Stress: {stress_level.value.upper()}",
            description="Combined regulatory, financial, and operational stress",
            stress_level=stress_level.value,
            category=StressCategory.COMBINED.value,
            stress_factors=stress_factors,
            time_horizon_days=540,
            combined_severity_score=severity_score,
            expected_financial_impact=financial_impact,
            mitigation_difficulty="high" if base_mult < 3.0 else "extreme"
        )
    
    def create_cascade_failure_scenario(self) -> StressTestScenario:
        """Create cascade failure scenario"""
        
        stress_factors = [
            StressFactor(
                factor_id="CASCADE-001",
                factor_name="Initial Violation",
                factor_type="trigger",
                severity_multiplier=1.5,
                probability_override=0.20,
                impact_description="Single compliance violation triggers investigation"
            ),
            StressFactor(
                factor_id="CASCADE-002",
                factor_name="Expanded Investigation",
                factor_type="enforcement",
                severity_multiplier=2.5,
                probability_override=0.60,
                impact_description="Investigation uncovers systemic issues"
            ),
            StressFactor(
                factor_id="CASCADE-003",
                factor_name="Multi-Jurisdiction Attention",
                factor_type="regulatory",
                severity_multiplier=3.0,
                probability_override=0.40,
                impact_description="Other jurisdictions launch parallel investigations"
            ),
            StressFactor(
                factor_id="CASCADE-004",
                factor_name="Reputation Damage",
                factor_type="market",
                severity_multiplier=2.8,
                probability_override=0.70,
                impact_description="Market confidence loss and business impact"
            ),
            StressFactor(
                factor_id="CASCADE-005",
                factor_name="Resource Exhaustion",
                factor_type="operational",
                severity_multiplier=3.2,
                probability_override=0.50,
                impact_description="Compliance team overwhelmed by multiple investigations"
            ),
            StressFactor(
                factor_id="CASCADE-006",
                factor_name="Secondary Violations",
                factor_type="compliance",
                severity_multiplier=4.0,
                probability_override=0.30,
                impact_description="New violations occur due to resource strain"
            )
        ]
        
        severity_score = sum(f.severity_multiplier for f in stress_factors) * 100 / len(stress_factors)
        financial_impact = 10000000  # $10M
        
        scenario_id = f"STRESS-CASCADE-{self.rng.randint(1000, 9999)}"
        
        return StressTestScenario(
            scenario_id=scenario_id,
            scenario_name="Cascade Failure Scenario",
            description="Single violation cascading into systemic failure",
            stress_level=StressLevel.EXTREME.value,
            category=StressCategory.CASCADE.value,
            stress_factors=stress_factors,
            time_horizon_days=730,
            combined_severity_score=severity_score,
            expected_financial_impact=financial_impact,
            mitigation_difficulty="extreme"
        )


class HistoricalCrisisReplicator:
    """Replicate and adapt historical crises"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def replicate_crisis(self,
                        crisis_name: str,
                        adaptation_factor: float = 1.0) -> Dict[str, Any]:
        """Replicate historical crisis with modern adaptation"""
        
        historical_patterns = {
            "2008_financial_crisis": {
                "regulatory_response_delay_days": 180,
                "enforcement_escalation_factor": 3.2,
                "penalty_increase_factor": 4.5,
                "duration_months": 36,
                "lessons": [
                    "Regulatory response was delayed but severe",
                    "Penalties increased exponentially",
                    "New regulations emerged rapidly post-crisis"
                ]
            },
            "cambridge_analytica_2018": {
                "regulatory_response_delay_days": 30,
                "enforcement_escalation_factor": 2.8,
                "penalty_increase_factor": 3.5,
                "duration_months": 18,
                "lessons": [
                    "Privacy violations triggered global response",
                    "Reputational damage exceeded financial penalties",
                    "Led to GDPR enforcement acceleration"
                ]
            },
            "equifax_breach_2017": {
                "regulatory_response_delay_days": 60,
                "enforcement_escalation_factor": 2.5,
                "penalty_increase_factor": 3.0,
                "duration_months": 24,
                "lessons": [
                    "Data breach led to multi-jurisdiction action",
                    "Class-action lawsuits compounded regulatory penalties",
                    "New data protection requirements emerged"
                ]
            }
        }
        
        pattern = historical_patterns.get(crisis_name, historical_patterns["2008_financial_crisis"])
        
        # Adapt to modern context
        adapted_pattern = {
            'crisis_name': crisis_name,
            'regulatory_response_delay_days': int(pattern['regulatory_response_delay_days'] * adaptation_factor),
            'enforcement_escalation_factor': pattern['enforcement_escalation_factor'] * adaptation_factor,
            'penalty_increase_factor': pattern['penalty_increase_factor'] * adaptation_factor,
            'expected_duration_months': int(pattern['duration_months'] * adaptation_factor),
            'historical_lessons': pattern['lessons'],
            'adaptation_factor': float(adaptation_factor),
            'modern_applicability_score': float(self.rng.uniform(0.7, 0.95))
        }
        
        return adapted_pattern
