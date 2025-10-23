"""
Regulatory Scenarios Module

This module implements regulatory change scenario generation including:
- New regulation introduction
- Existing regulation amendments
- Multi-jurisdiction changes
- Regulatory convergence/divergence

All scenarios are designed to integrate with Phase 4.2 risk models.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import numpy as np


class RegulationType(Enum):
    """Types of regulatory changes"""
    NEW_REGULATION = "new_regulation"
    AMENDMENT = "amendment"
    SUNSET = "sunset"
    HARMONIZATION = "harmonization"
    DIVERGENCE = "divergence"


class RegulationSeverity(Enum):
    """Severity levels for regulatory changes"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ImplementationTimeline(Enum):
    """Standard implementation timelines"""
    IMMEDIATE = 30  # 30 days
    SHORT = 90  # 3 months
    MEDIUM = 180  # 6 months
    LONG = 365  # 1 year
    EXTENDED = 730  # 2 years


@dataclass
class RegulatoryChange:
    """Container for a single regulatory change"""
    regulation_id: str
    change_type: str
    severity: str
    effective_date: str
    jurisdiction: str
    description: str
    impact_areas: List[str]
    compliance_deadline: str
    estimated_cost: float
    penalty_multiplier: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'regulation_id': self.regulation_id,
            'change_type': self.change_type,
            'severity': self.severity,
            'effective_date': self.effective_date,
            'jurisdiction': self.jurisdiction,
            'description': self.description,
            'impact_areas': self.impact_areas,
            'compliance_deadline': self.compliance_deadline,
            'estimated_cost': float(self.estimated_cost),
            'penalty_multiplier': float(self.penalty_multiplier)
        }


@dataclass
class RegulatoryScenario:
    """Complete regulatory scenario with multiple changes"""
    scenario_id: str
    scenario_name: str
    description: str
    changes: List[RegulatoryChange]
    time_horizon_days: int
    probability: float
    total_estimated_cost: float
    total_impact_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'scenario_id': self.scenario_id,
            'scenario_name': self.scenario_name,
            'description': self.description,
            'changes': [c.to_dict() for c in self.changes],
            'time_horizon_days': int(self.time_horizon_days),
            'probability': float(self.probability),
            'total_estimated_cost': float(self.total_estimated_cost),
            'total_impact_score': float(self.total_impact_score)
        }


class RegulationChangeScenario:
    """Generate regulatory change scenarios"""
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize scenario generator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def create_new_regulation_scenario(self,
                                       jurisdiction: str,
                                       severity: RegulationSeverity,
                                       implementation_timeline: ImplementationTimeline,
                                       impact_areas: Optional[List[str]] = None) -> RegulatoryChange:
        """
        Create a new regulation introduction scenario
        
        Args:
            jurisdiction: Target jurisdiction
            severity: Severity level
            implementation_timeline: Time to implement
            impact_areas: Affected business areas
            
        Returns:
            RegulatoryChange object
        """
        if impact_areas is None:
            impact_areas = ["data_privacy", "model_governance"]
        
        # Calculate effective date
        effective_date = datetime.now() + timedelta(days=30)
        compliance_deadline = effective_date + timedelta(days=implementation_timeline.value)
        
        # Estimate cost based on severity
        cost_multipliers = {
            RegulationSeverity.LOW: 50000,
            RegulationSeverity.MEDIUM: 200000,
            RegulationSeverity.HIGH: 500000,
            RegulationSeverity.CRITICAL: 1500000
        }
        base_cost = cost_multipliers[severity]
        estimated_cost = base_cost * (1 + self.rng.uniform(-0.2, 0.3))
        
        # Penalty multiplier
        penalty_multipliers = {
            RegulationSeverity.LOW: 1.0,
            RegulationSeverity.MEDIUM: 1.5,
            RegulationSeverity.HIGH: 2.5,
            RegulationSeverity.CRITICAL: 4.0
        }
        
        return RegulatoryChange(
            regulation_id=f"REG-{jurisdiction.upper()}-{self.rng.randint(10000, 99999)}",
            change_type=RegulationType.NEW_REGULATION.value,
            severity=severity.value,
            effective_date=effective_date.strftime("%Y-%m-%d"),
            jurisdiction=jurisdiction,
            description=f"New {severity.value} regulation in {jurisdiction}",
            impact_areas=impact_areas,
            compliance_deadline=compliance_deadline.strftime("%Y-%m-%d"),
            estimated_cost=estimated_cost,
            penalty_multiplier=penalty_multipliers[severity]
        )
    
    def create_amendment_scenario(self,
                                  existing_regulation_id: str,
                                  jurisdiction: str,
                                  amendment_severity: RegulationSeverity) -> RegulatoryChange:
        """
        Create a regulation amendment scenario
        
        Args:
            existing_regulation_id: ID of regulation being amended
            jurisdiction: Target jurisdiction
            amendment_severity: Severity of the amendment
            
        Returns:
            RegulatoryChange object
        """
        # Amendments typically have shorter timelines
        effective_date = datetime.now() + timedelta(days=15)
        compliance_deadline = effective_date + timedelta(days=90)
        
        # Amendment costs are typically 30-50% of new regulation
        cost_multipliers = {
            RegulationSeverity.LOW: 20000,
            RegulationSeverity.MEDIUM: 80000,
            RegulationSeverity.HIGH: 200000,
            RegulationSeverity.CRITICAL: 600000
        }
        base_cost = cost_multipliers[amendment_severity]
        estimated_cost = base_cost * (1 + self.rng.uniform(-0.15, 0.25))
        
        return RegulatoryChange(
            regulation_id=f"AMEND-{existing_regulation_id}",
            change_type=RegulationType.AMENDMENT.value,
            severity=amendment_severity.value,
            effective_date=effective_date.strftime("%Y-%m-%d"),
            jurisdiction=jurisdiction,
            description=f"Amendment to {existing_regulation_id}",
            impact_areas=["compliance_updates", "policy_revision"],
            compliance_deadline=compliance_deadline.strftime("%Y-%m-%d"),
            estimated_cost=estimated_cost,
            penalty_multiplier=1.2
        )
    
    def create_sunset_scenario(self,
                               regulation_id: str,
                               jurisdiction: str) -> RegulatoryChange:
        """
        Create a regulation sunset/expiration scenario
        
        Args:
            regulation_id: ID of regulation expiring
            jurisdiction: Target jurisdiction
            
        Returns:
            RegulatoryChange object
        """
        effective_date = datetime.now() + timedelta(days=180)
        
        # Sunset typically has negative cost (savings)
        estimated_cost = -self.rng.uniform(10000, 50000)
        
        return RegulatoryChange(
            regulation_id=f"SUNSET-{regulation_id}",
            change_type=RegulationType.SUNSET.value,
            severity=RegulationSeverity.LOW.value,
            effective_date=effective_date.strftime("%Y-%m-%d"),
            jurisdiction=jurisdiction,
            description=f"Sunset of {regulation_id}",
            impact_areas=["compliance_reduction"],
            compliance_deadline=effective_date.strftime("%Y-%m-%d"),
            estimated_cost=estimated_cost,
            penalty_multiplier=0.0  # No penalties after sunset
        )


class JurisdictionScenarioGenerator:
    """Generate multi-jurisdiction regulatory scenarios"""
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize jurisdiction scenario generator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        self.change_generator = RegulationChangeScenario(random_state)
    
    def create_harmonization_scenario(self,
                                      jurisdictions: List[str],
                                      severity: RegulationSeverity,
                                      time_horizon_years: int = 2) -> RegulatoryScenario:
        """
        Create a regulatory harmonization scenario across jurisdictions
        
        Args:
            jurisdictions: List of jurisdictions harmonizing
            severity: Severity of harmonization
            time_horizon_years: Years to complete harmonization
            
        Returns:
            RegulatoryScenario object
        """
        changes = []
        total_cost = 0.0
        
        # Create aligned regulations for each jurisdiction
        for jurisdiction in jurisdictions:
            change = self.change_generator.create_new_regulation_scenario(
                jurisdiction=jurisdiction,
                severity=severity,
                implementation_timeline=ImplementationTimeline.LONG,
                impact_areas=["cross_border_compliance", "data_governance"]
            )
            changes.append(change)
            total_cost += change.estimated_cost
        
        # Calculate impact score (harmonization reduces long-term cost)
        num_jurisdictions = len(jurisdictions)
        impact_score = num_jurisdictions * 10.0 * (severity.value == "high" and 1.5 or 1.0)
        
        # Harmonization probability based on complexity
        probability = max(0.3, 1.0 - (num_jurisdictions * 0.1))
        
        scenario_id = f"HARM-{'-'.join([j[:3].upper() for j in jurisdictions])}-{self.rng.randint(1000, 9999)}"
        
        return RegulatoryScenario(
            scenario_id=scenario_id,
            scenario_name=f"Harmonization across {', '.join(jurisdictions)}",
            description=f"Regulatory harmonization scenario involving {num_jurisdictions} jurisdictions",
            changes=changes,
            time_horizon_days=time_horizon_years * 365,
            probability=probability,
            total_estimated_cost=total_cost,
            total_impact_score=impact_score
        )
    
    def create_divergence_scenario(self,
                                   jurisdictions: List[str],
                                   divergence_factor: float = 0.5) -> RegulatoryScenario:
        """
        Create a regulatory divergence scenario
        
        Args:
            jurisdictions: List of jurisdictions diverging
            divergence_factor: Degree of divergence (0-1)
            
        Returns:
            RegulatoryScenario object
        """
        changes = []
        total_cost = 0.0
        
        # Create conflicting regulations
        severities = [RegulationSeverity.MEDIUM, RegulationSeverity.HIGH]
        
        for i, jurisdiction in enumerate(jurisdictions):
            severity = severities[i % len(severities)]
            change = self.change_generator.create_new_regulation_scenario(
                jurisdiction=jurisdiction,
                severity=severity,
                implementation_timeline=ImplementationTimeline.MEDIUM,
                impact_areas=["cross_border_conflict", "compliance_complexity"]
            )
            # Divergence increases costs
            change.estimated_cost *= (1 + divergence_factor)
            changes.append(change)
            total_cost += change.estimated_cost
        
        # Impact score increases with divergence
        num_jurisdictions = len(jurisdictions)
        impact_score = num_jurisdictions * 15.0 * (1 + divergence_factor)
        
        # Divergence has higher probability than harmonization
        probability = min(0.7, 0.5 + (divergence_factor * 0.3))
        
        scenario_id = f"DIV-{'-'.join([j[:3].upper() for j in jurisdictions])}-{self.rng.randint(1000, 9999)}"
        
        return RegulatoryScenario(
            scenario_id=scenario_id,
            scenario_name=f"Divergence across {', '.join(jurisdictions)}",
            description=f"Regulatory divergence creating conflicting requirements",
            changes=changes,
            time_horizon_days=365,
            probability=probability,
            total_estimated_cost=total_cost,
            total_impact_score=impact_score
        )
    
    def create_cascade_scenario(self,
                                leading_jurisdiction: str,
                                follower_jurisdictions: List[str],
                                delay_months: int = 6) -> RegulatoryScenario:
        """
        Create a cascade scenario where one jurisdiction leads and others follow
        
        Args:
            leading_jurisdiction: First mover jurisdiction
            follower_jurisdictions: Jurisdictions that follow
            delay_months: Delay in months for followers
            
        Returns:
            RegulatoryScenario object
        """
        changes = []
        total_cost = 0.0
        
        # Lead jurisdiction implements first
        lead_change = self.change_generator.create_new_regulation_scenario(
            jurisdiction=leading_jurisdiction,
            severity=RegulationSeverity.HIGH,
            implementation_timeline=ImplementationTimeline.MEDIUM,
            impact_areas=["regulatory_leadership", "market_impact"]
        )
        changes.append(lead_change)
        total_cost += lead_change.estimated_cost
        
        # Follower jurisdictions implement with delay
        for follower in follower_jurisdictions:
            follower_change = self.change_generator.create_new_regulation_scenario(
                jurisdiction=follower,
                severity=RegulationSeverity.MEDIUM,
                implementation_timeline=ImplementationTimeline.LONG,
                impact_areas=["regulatory_adoption", "compliance_alignment"]
            )
            # Adjust effective date
            lead_date = datetime.strptime(lead_change.effective_date, "%Y-%m-%d")
            follower_date = lead_date + timedelta(days=delay_months * 30)
            follower_change.effective_date = follower_date.strftime("%Y-%m-%d")
            
            # Follower costs are typically lower (learn from leader)
            follower_change.estimated_cost *= 0.8
            
            changes.append(follower_change)
            total_cost += follower_change.estimated_cost
        
        num_jurisdictions = 1 + len(follower_jurisdictions)
        impact_score = num_jurisdictions * 12.0
        probability = 0.6  # Moderate probability
        
        scenario_id = f"CASCADE-{leading_jurisdiction[:3].upper()}-{self.rng.randint(1000, 9999)}"
        
        return RegulatoryScenario(
            scenario_id=scenario_id,
            scenario_name=f"Cascade from {leading_jurisdiction}",
            description=f"Regulatory cascade starting from {leading_jurisdiction}",
            changes=changes,
            time_horizon_days=365 + (delay_months * 30),
            probability=probability,
            total_estimated_cost=total_cost,
            total_impact_score=impact_score
        )
