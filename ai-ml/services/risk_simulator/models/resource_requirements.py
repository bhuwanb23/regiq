"""
Resource Requirements Models

This module implements models for estimating resource requirements for compliance
remediation and ongoing operations, including personnel, technology, and budget needs.

Models:
- PersonnelRequirementsEstimator: Estimate staffing needs
- TechnologyResourceEstimator: Estimate technology and infrastructure needs
- BudgetAllocationOptimizer: Optimize budget allocation across resources
- ResourcePlanningModel: Integrated resource planning
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np


class ResourceType(Enum):
    """Types of resources"""
    PERSONNEL = "personnel"
    TECHNOLOGY = "technology"
    INFRASTRUCTURE = "infrastructure"
    EXTERNAL_SERVICES = "external_services"


class SkillLevel(Enum):
    """Skill levels for personnel"""
    JUNIOR = "junior"
    MID_LEVEL = "mid_level"
    SENIOR = "senior"
    EXPERT = "expert"


@dataclass
class ResourceEstimate:
    """Result container for resource requirements"""
    resource_type: str
    quantity_needed: float
    annual_cost: float
    one_time_cost: float
    skill_breakdown: Dict[str, int]
    timeline_months: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'resource_type': self.resource_type,
            'quantity_needed': float(self.quantity_needed),
            'annual_cost': float(self.annual_cost),
            'one_time_cost': float(self.one_time_cost),
            'skill_breakdown': {k: int(v) for k, v in self.skill_breakdown.items()},
            'timeline_months': float(self.timeline_months)
        }


class PersonnelRequirementsEstimator:
    """Estimate personnel resource needs"""
    
    ANNUAL_SALARIES = {
        SkillLevel.JUNIOR: 70000,
        SkillLevel.MID_LEVEL: 100000,
        SkillLevel.SENIOR: 140000,
        SkillLevel.EXPERT: 200000
    }
    
    def estimate_compliance_staff(self,
                                 num_regulations: int,
                                 num_systems: int,
                                 company_size: str = "medium") -> ResourceEstimate:
        """Estimate compliance personnel needs"""
        # Base on regulations (1 person per 10 regulations)
        base_staff = max(1, num_regulations // 10)
        
        # Adjust for systems complexity
        systems_factor = 1 + (num_systems * 0.05)
        
        # Company size multiplier
        size_multipliers = {"small": 0.7, "medium": 1.0, "large": 1.5, "enterprise": 2.5}
        size_mult = size_multipliers.get(company_size, 1.0)
        
        total_staff = int(base_staff * systems_factor * size_mult)
        
        # Skill distribution
        skill_breakdown = {
            SkillLevel.JUNIOR.value: int(total_staff * 0.3),
            SkillLevel.MID_LEVEL.value: int(total_staff * 0.4),
            SkillLevel.SENIOR.value: int(total_staff * 0.25),
            SkillLevel.EXPERT.value: int(total_staff * 0.05)
        }
        
        # Annual cost
        annual_cost = sum(
            self.ANNUAL_SALARIES[SkillLevel(k)] * v
            for k, v in skill_breakdown.items()
        )
        
        # One-time costs (recruiting, onboarding)
        one_time_cost = total_staff * 15000
        
        return ResourceEstimate(
            resource_type=ResourceType.PERSONNEL.value,
            quantity_needed=total_staff,
            annual_cost=annual_cost,
            one_time_cost=one_time_cost,
            skill_breakdown=skill_breakdown,
            timeline_months=3  # Hiring timeline
        )


class TechnologyResourceEstimator:
    """Estimate technology and infrastructure needs"""
    
    def estimate_technology_needs(self,
                                 num_systems: int,
                                 data_volume_tb: float,
                                 concurrent_users: int) -> ResourceEstimate:
        """Estimate technology resource requirements"""
        # Server/compute resources
        servers_needed = max(2, num_systems // 3)  # Redundancy included
        server_cost_annual = servers_needed * 5000  # Cloud costs
        
        # Storage costs
        storage_cost_annual = data_volume_tb * 100  # Per TB
        
        # Monitoring/compliance tools
        tool_licenses = num_systems * 2000
        
        # Network/security
        security_tools = 50000  # Annual
        
        annual_cost = (server_cost_annual + storage_cost_annual + 
                      tool_licenses + security_tools)
        
        # One-time setup
        one_time_cost = servers_needed * 10000
        
        return ResourceEstimate(
            resource_type=ResourceType.TECHNOLOGY.value,
            quantity_needed=servers_needed,
            annual_cost=annual_cost,
            one_time_cost=one_time_cost,
            skill_breakdown={'servers': servers_needed},
            timeline_months=2
        )


class ResourcePlanningModel:
    """Integrated resource planning model"""
    
    def __init__(self):
        """Initialize resource planner"""
        self.personnel_estimator = PersonnelRequirementsEstimator()
        self.tech_estimator = TechnologyResourceEstimator()
    
    def create_resource_plan(self,
                            planning_params: Dict[str, Any],
                            budget_constraint: Optional[float] = None) -> Dict[str, Any]:
        """Create comprehensive resource plan"""
        # Estimate personnel
        personnel = self.personnel_estimator.estimate_compliance_staff(
            planning_params.get('num_regulations', 50),
            planning_params.get('num_systems', 10),
            planning_params.get('company_size', 'medium')
        )
        
        # Estimate technology
        technology = self.tech_estimator.estimate_technology_needs(
            planning_params.get('num_systems', 10),
            planning_params.get('data_volume_tb', 100),
            planning_params.get('concurrent_users', 1000)
        )
        
        # Total costs
        total_annual = personnel.annual_cost + technology.annual_cost
        total_one_time = personnel.one_time_cost + technology.one_time_cost
        
        # Budget fit
        within_budget = True
        if budget_constraint:
            within_budget = (total_one_time + total_annual) <= budget_constraint
        
        return {
            'personnel': personnel.to_dict(),
            'technology': technology.to_dict(),
            'total_annual_cost': float(total_annual),
            'total_one_time_cost': float(total_one_time),
            'total_first_year_cost': float(total_one_time + total_annual),
            'within_budget': within_budget,
            'budget_utilization_pct': float((total_one_time + total_annual) / budget_constraint * 100) if budget_constraint else 0
        }
