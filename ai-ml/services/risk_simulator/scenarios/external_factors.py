"""
External Factors Module

This module implements external event simulation including:
- Political changes
- Global events (pandemics, conflicts)
- Public sentiment shifts
- Black swan events

Integrates with all Phase 4.2 risk models.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import numpy as np


class EventType(Enum):
    """External event types"""
    POLITICAL_CHANGE = "political_change"
    GLOBAL_CRISIS = "global_crisis"
    PUBLIC_SENTIMENT = "public_sentiment"
    TECHNOLOGICAL_DISRUPTION = "technological_disruption"
    BLACK_SWAN = "black_swan"


class EventSeverity(Enum):
    """Event severity levels"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CATASTROPHIC = "catastrophic"


@dataclass
class ExternalEvent:
    """External event container"""
    event_id: str
    event_type: str
    event_name: str
    severity: str
    probability: float
    regulatory_impact_score: float
    financial_impact_multiplier: float
    duration_days: int
    cascading_effects: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'event_name': self.event_name,
            'severity': self.severity,
            'probability': float(self.probability),
            'regulatory_impact_score': float(self.regulatory_impact_score),
            'financial_impact_multiplier': float(self.financial_impact_multiplier),
            'duration_days': int(self.duration_days),
            'cascading_effects': self.cascading_effects
        }


class ExternalEventSimulator:
    """Simulate external events and their impacts"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def create_political_change_event(self,
                                      change_magnitude: str = "moderate") -> ExternalEvent:
        """Create political change event"""
        
        severity_params = {
            "minor": (EventSeverity.MINOR, 0.3, (1.0, 1.2), 180),
            "moderate": (EventSeverity.MODERATE, 0.15, (1.2, 1.5), 365),
            "major": (EventSeverity.MAJOR, 0.05, (1.5, 2.5), 730)
        }
        
        severity, prob, impact_range, duration = severity_params.get(
            change_magnitude, severity_params["moderate"]
        )
        
        regulatory_impact = self.rng.uniform(30, 70)
        financial_mult = self.rng.uniform(*impact_range)
        
        cascading = [
            "regulatory_uncertainty",
            "enforcement_changes",
            "policy_shifts"
        ]
        
        event_id = f"POL-{change_magnitude.upper()}-{self.rng.randint(1000, 9999)}"
        
        return ExternalEvent(
            event_id=event_id,
            event_type=EventType.POLITICAL_CHANGE.value,
            event_name=f"{change_magnitude.capitalize()} Political Change",
            severity=severity.value,
            probability=prob,
            regulatory_impact_score=regulatory_impact,
            financial_impact_multiplier=financial_mult,
            duration_days=duration,
            cascading_effects=cascading
        )
    
    def create_global_crisis_event(self,
                                   crisis_type: str = "pandemic") -> ExternalEvent:
        """Create global crisis event"""
        
        severity = EventSeverity.CATASTROPHIC
        prob = 0.02  # Low probability
        
        if crisis_type == "pandemic":
            regulatory_impact = self.rng.uniform(70, 95)
            financial_mult = self.rng.uniform(2.0, 4.0)
            duration = self.rng.randint(365, 1095)  # 1-3 years
            cascading = [
                "emergency_regulations",
                "business_disruption",
                "supply_chain_collapse",
                "remote_work_mandates"
            ]
        elif crisis_type == "conflict":
            regulatory_impact = self.rng.uniform(60, 85)
            financial_mult = self.rng.uniform(1.8, 3.5)
            duration = self.rng.randint(180, 730)
            cascading = [
                "sanctions",
                "trade_restrictions",
                "data_sovereignty",
                "cybersecurity_requirements"
            ]
        else:  # financial_crisis
            regulatory_impact = self.rng.uniform(75, 90)
            financial_mult = self.rng.uniform(2.5, 4.5)
            duration = self.rng.randint(365, 1460)
            cascading = [
                "stricter_oversight",
                "capital_requirements",
                "stress_testing",
                "transparency_mandates"
            ]
        
        event_id = f"CRISIS-{crisis_type.upper()}-{self.rng.randint(1000, 9999)}"
        
        return ExternalEvent(
            event_id=event_id,
            event_type=EventType.GLOBAL_CRISIS.value,
            event_name=f"Global {crisis_type.capitalize()} Crisis",
            severity=severity.value,
            probability=prob,
            regulatory_impact_score=regulatory_impact,
            financial_impact_multiplier=financial_mult,
            duration_days=duration,
            cascading_effects=cascading
        )
    
    def create_public_sentiment_shift(self,
                                      sentiment_driver: str = "privacy") -> ExternalEvent:
        """Create public sentiment shift event"""
        
        severity = EventSeverity.MODERATE
        prob = 0.25
        
        drivers = {
            "privacy": (40, 60, 1.3, 1.7),
            "ai_ethics": (50, 70, 1.4, 1.9),
            "environmental": (35, 55, 1.2, 1.5),
            "social_justice": (45, 65, 1.3, 1.8)
        }
        
        impact_low, impact_high, mult_low, mult_high = drivers.get(
            sentiment_driver, drivers["privacy"]
        )
        
        regulatory_impact = self.rng.uniform(impact_low, impact_high)
        financial_mult = self.rng.uniform(mult_low, mult_high)
        
        cascading = [
            "new_regulations",
            "reputation_risk",
            "stakeholder_pressure"
        ]
        
        event_id = f"SENT-{sentiment_driver.upper()}-{self.rng.randint(1000, 9999)}"
        
        return ExternalEvent(
            event_id=event_id,
            event_type=EventType.PUBLIC_SENTIMENT.value,
            event_name=f"Public Sentiment Shift: {sentiment_driver}",
            severity=severity.value,
            probability=prob,
            regulatory_impact_score=regulatory_impact,
            financial_impact_multiplier=financial_mult,
            duration_days=365,
            cascading_effects=cascading
        )


class BlackSwanEventGenerator:
    """Generate black swan (rare, high-impact) events"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def generate_black_swan(self,
                           event_category: str = "regulatory") -> ExternalEvent:
        """Generate a black swan event"""
        
        severity = EventSeverity.CATASTROPHIC
        prob = self.rng.uniform(0.001, 0.01)  # Very low probability
        
        # Black swans have extreme impacts
        regulatory_impact = self.rng.uniform(85, 100)
        financial_mult = self.rng.uniform(3.0, 10.0)
        duration = self.rng.randint(180, 730)
        
        cascading = [
            "systemic_regulatory_change",
            "market_collapse",
            "industry_restructuring",
            "unprecedented_penalties",
            "emergency_legislation"
        ]
        
        event_id = f"BLACKSWAN-{self.rng.randint(10000, 99999)}"
        
        return ExternalEvent(
            event_id=event_id,
            event_type=EventType.BLACK_SWAN.value,
            event_name=f"Black Swan Event: {event_category}",
            severity=severity.value,
            probability=prob,
            regulatory_impact_score=regulatory_impact,
            financial_impact_multiplier=financial_mult,
            duration_days=duration,
            cascading_effects=cascading
        )
    
    def simulate_historical_crisis_replay(self,
                                         crisis_name: str = "2008_financial") -> Dict[str, Any]:
        """Replay historical crisis adapted to current context"""
        
        historical_crises = {
            "2008_financial": {
                "regulatory_surge": 2.8,
                "enforcement_increase": 3.2,
                "penalty_escalation": 4.5,
                "duration_days": 1460
            },
            "dot_com_bust": {
                "regulatory_surge": 1.8,
                "enforcement_increase": 2.0,
                "penalty_escalation": 2.2,
                "duration_days": 730
            },
            "enron_scandal": {
                "regulatory_surge": 3.5,
                "enforcement_increase": 4.0,
                "penalty_escalation": 5.0,
                "duration_days": 1095
            }
        }
        
        params = historical_crises.get(crisis_name, historical_crises["2008_financial"])
        
        return {
            'crisis_name': crisis_name,
            'regulatory_surge_multiplier': params['regulatory_surge'],
            'enforcement_increase_multiplier': params['enforcement_increase'],
            'penalty_escalation_multiplier': params['penalty_escalation'],
            'expected_duration_days': params['duration_days'],
            'probability': 0.05,
            'lessons_learned': [
                "Proactive compliance is critical",
                "Regulatory backlash can be severe",
                "Industry-wide impacts are common"
            ]
        }
