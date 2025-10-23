"""
Remediation Cost Estimation Models

This module implements models for estimating the costs of remediation activities
required to address regulatory compliance issues, including technical fixes,
process improvements, training, and ongoing compliance monitoring.

Models:
- TechnicalRemediationEstimator: Estimate technical system fixes
- ProcessImprovementEstimator: Estimate process change costs
- TrainingCostEstimator: Estimate compliance training costs
- OngoingComplianceEstimator: Estimate ongoing monitoring costs
- ComprehensiveRemediationPlanner: Integrated remediation cost planning
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats


class RemediationType(Enum):
    """Types of remediation activities"""
    TECHNICAL = "technical"
    PROCESS = "process"
    TRAINING = "training"
    MONITORING = "monitoring"
    AUDIT = "audit"


class ComplexityLevel(Enum):
    """Complexity levels for remediation"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class RemediationEstimate:
    """Result container for remediation cost estimate"""
    total_cost: float
    cost_range: Tuple[float, float]
    timeline_months: float
    resource_requirements: Dict[str, int]
    cost_breakdown: Dict[str, float]
    complexity_level: str
    confidence_level: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'total_cost': float(self.total_cost),
            'cost_range': tuple(float(x) for x in self.cost_range),
            'timeline_months': float(self.timeline_months),
            'resource_requirements': {k: int(v) for k, v in self.resource_requirements.items()},
            'cost_breakdown': {k: float(v) for k, v in self.cost_breakdown.items()},
            'complexity_level': self.complexity_level,
            'confidence_level': float(self.confidence_level)
        }


class TechnicalRemediationEstimator:
    """
    Estimator for technical remediation costs.
    
    Includes system modifications, data fixes, infrastructure updates,
    and technical debt resolution.
    """
    
    # Base hourly rates (USD)
    HOURLY_RATES = {
        'senior_engineer': 150,
        'engineer': 100,
        'junior_engineer': 75,
        'architect': 200,
        'qa_engineer': 90
    }
    
    # Complexity multipliers for effort estimation
    COMPLEXITY_MULTIPLIERS = {
        ComplexityLevel.LOW: 1.0,
        ComplexityLevel.MEDIUM: 2.0,
        ComplexityLevel.HIGH: 4.0,
        ComplexityLevel.VERY_HIGH: 8.0
    }
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize technical remediation estimator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_technical_fix(self,
                               complexity: ComplexityLevel,
                               num_systems_affected: int,
                               base_effort_hours: float = 160,
                               include_testing: bool = True,
                               include_documentation: bool = True) -> RemediationEstimate:
        """
        Estimate technical remediation costs.
        
        Args:
            complexity: Complexity level of remediation
            num_systems_affected: Number of systems requiring changes
            base_effort_hours: Base effort hours per system
            include_testing: Include testing effort
            include_documentation: Include documentation effort
            
        Returns:
            RemediationEstimate with detailed breakdown
        """
        # Apply complexity multiplier
        multiplier = self.COMPLEXITY_MULTIPLIERS[complexity]
        total_effort_hours = base_effort_hours * multiplier * num_systems_affected
        
        # Add testing effort (typically 40% of development)
        if include_testing:
            testing_hours = total_effort_hours * 0.4
        else:
            testing_hours = 0
        
        # Add documentation effort (typically 15% of development)
        if include_documentation:
            documentation_hours = total_effort_hours * 0.15
        else:
            documentation_hours = 0
        
        # Total hours
        total_hours = total_effort_hours + testing_hours + documentation_hours
        
        # Resource allocation
        resource_requirements = {
            'senior_engineers': max(1, int(num_systems_affected * 0.3)),
            'engineers': max(2, int(num_systems_affected * 0.5)),
            'qa_engineers': max(1, int(num_systems_affected * 0.2)) if include_testing else 0,
            'architects': 1 if complexity in [ComplexityLevel.HIGH, ComplexityLevel.VERY_HIGH] else 0
        }
        
        # Calculate costs
        development_cost = (
            resource_requirements['senior_engineers'] * total_effort_hours * 0.3 * self.HOURLY_RATES['senior_engineer'] +
            resource_requirements['engineers'] * total_effort_hours * 0.5 * self.HOURLY_RATES['engineer'] +
            resource_requirements['architects'] * total_effort_hours * 0.2 * self.HOURLY_RATES['architect']
        )
        
        testing_cost = resource_requirements['qa_engineers'] * testing_hours * self.HOURLY_RATES['qa_engineer']
        
        # Infrastructure costs (servers, tools, licenses)
        infrastructure_cost = num_systems_affected * 5000 * multiplier
        
        # Contingency (20%)
        subtotal = development_cost + testing_cost + infrastructure_cost
        contingency = subtotal * 0.20
        
        total_cost = subtotal + contingency
        
        # Cost range (±30% for uncertainty)
        cost_range = (total_cost * 0.7, total_cost * 1.3)
        
        # Timeline estimation (months)
        # Assuming 160 hours per month per resource
        total_resources = sum(resource_requirements.values())
        timeline_months = total_hours / (160 * max(1, total_resources))
        
        # Cost breakdown
        cost_breakdown = {
            'development': float(development_cost),
            'testing': float(testing_cost),
            'infrastructure': float(infrastructure_cost),
            'contingency': float(contingency)
        }
        
        return RemediationEstimate(
            total_cost=total_cost,
            cost_range=cost_range,
            timeline_months=timeline_months,
            resource_requirements=resource_requirements,
            cost_breakdown=cost_breakdown,
            complexity_level=complexity.value,
            confidence_level=0.70
        )


class ProcessImprovementEstimator:
    """
    Estimator for process improvement and change management costs.
    
    Includes process redesign, change management, and organizational updates.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize process improvement estimator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_process_change(self,
                               num_processes: int,
                               num_employees_affected: int,
                               change_magnitude: float,
                               requires_external_consultant: bool = False) -> RemediationEstimate:
        """
        Estimate process improvement costs.
        
        Args:
            num_processes: Number of processes to change
            num_employees_affected: Number of employees affected
            change_magnitude: Magnitude of change (0-1)
            requires_external_consultant: Whether external consultants needed
            
        Returns:
            RemediationEstimate with detailed breakdown
        """
        # Process analysis and redesign costs
        # Estimate 80 hours per process for analysis and design
        analysis_hours = num_processes * 80
        analysis_cost = analysis_hours * 125  # $125/hour for business analyst
        
        # Change management costs
        # Based on number of affected employees
        change_mgmt_cost_per_employee = 500 * change_magnitude
        change_mgmt_cost = num_employees_affected * change_mgmt_cost_per_employee
        
        # Communication and stakeholder management
        communication_cost = num_employees_affected * 100
        
        # External consultant costs (if needed)
        if requires_external_consultant:
            consultant_cost = num_processes * 50000  # $50k per process
        else:
            consultant_cost = 0
        
        # Implementation support costs
        implementation_cost = num_processes * num_employees_affected * 50
        
        # Total cost
        total_cost = (
            analysis_cost +
            change_mgmt_cost +
            communication_cost +
            consultant_cost +
            implementation_cost
        )
        
        # Cost range
        cost_range = (total_cost * 0.75, total_cost * 1.4)
        
        # Timeline (months)
        # Process changes typically take 3-12 months depending on complexity
        base_timeline = 3
        timeline_months = base_timeline + (num_processes * 2) + (change_magnitude * 6)
        
        # Resource requirements
        resource_requirements = {
            'business_analysts': max(1, num_processes // 2),
            'change_managers': max(1, num_employees_affected // 50),
            'project_managers': 1,
            'external_consultants': num_processes if requires_external_consultant else 0
        }
        
        # Cost breakdown
        cost_breakdown = {
            'analysis_redesign': float(analysis_cost),
            'change_management': float(change_mgmt_cost),
            'communication': float(communication_cost),
            'external_consultants': float(consultant_cost),
            'implementation_support': float(implementation_cost)
        }
        
        # Complexity based on change magnitude
        if change_magnitude < 0.3:
            complexity = ComplexityLevel.LOW
        elif change_magnitude < 0.6:
            complexity = ComplexityLevel.MEDIUM
        else:
            complexity = ComplexityLevel.HIGH
        
        return RemediationEstimate(
            total_cost=total_cost,
            cost_range=cost_range,
            timeline_months=timeline_months,
            resource_requirements=resource_requirements,
            cost_breakdown=cost_breakdown,
            complexity_level=complexity.value,
            confidence_level=0.65
        )


class TrainingCostEstimator:
    """
    Estimator for compliance training costs.
    
    Includes training development, delivery, and ongoing refresher training.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize training cost estimator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_training_program(self,
                                 num_employees: int,
                                 training_hours_per_employee: float,
                                 requires_custom_content: bool = True,
                                 delivery_method: str = 'hybrid',
                                 refresher_frequency_years: float = 1.0) -> RemediationEstimate:
        """
        Estimate compliance training costs.
        
        Args:
            num_employees: Number of employees to train
            training_hours_per_employee: Hours of training per employee
            requires_custom_content: Whether custom content development needed
            delivery_method: 'online', 'classroom', or 'hybrid'
            refresher_frequency_years: Frequency of refresher training
            
        Returns:
            RemediationEstimate with detailed breakdown
        """
        # Content development costs
        if requires_custom_content:
            # Estimate 40 hours of development per 1 hour of training
            development_hours = training_hours_per_employee * 40
            content_development_cost = development_hours * 100  # $100/hour
        else:
            # Off-the-shelf content licensing
            content_development_cost = num_employees * 50
        
        # Delivery costs
        sessions_needed = 0  # Initialize
        if delivery_method == 'online':
            # Online platform costs
            platform_cost = 5000 + (num_employees * 20)
            instructor_cost = 0
            venue_cost = 0
        elif delivery_method == 'classroom':
            # Classroom delivery
            platform_cost = 0
            sessions_needed = int(np.ceil(num_employees / 25))  # 25 per session
            instructor_cost = sessions_needed * training_hours_per_employee * 150
            venue_cost = sessions_needed * 500
        else:  # hybrid
            # Mix of online and classroom
            platform_cost = 3000 + (num_employees * 10)
            sessions_needed = int(np.ceil(num_employees / 50))
            instructor_cost = sessions_needed * training_hours_per_employee * 150 * 0.5
            venue_cost = sessions_needed * 500 * 0.5
        
        # Employee time costs (opportunity cost)
        avg_hourly_rate = 50  # Average employee hourly rate
        employee_time_cost = num_employees * training_hours_per_employee * avg_hourly_rate
        
        # Assessment and certification costs
        assessment_cost = num_employees * 25
        
        # First year total
        first_year_cost = (
            content_development_cost +
            platform_cost +
            instructor_cost +
            venue_cost +
            employee_time_cost +
            assessment_cost
        )
        
        # Annual refresher costs (no content development)
        annual_refresher_cost = (
            platform_cost * 0.5 +  # Reduced platform cost
            instructor_cost * 0.3 +  # Reduced instructor time
            venue_cost * 0.3 +  # Fewer sessions
            employee_time_cost * 0.5 +  # Shorter refresher
            assessment_cost
        )
        
        # 3-year total cost
        years = 3
        refreshers_needed = int(years / refresher_frequency_years) - 1
        total_cost = first_year_cost + (annual_refresher_cost * refreshers_needed)
        
        # Cost range
        cost_range = (total_cost * 0.85, total_cost * 1.25)
        
        # Timeline (months for initial rollout)
        if requires_custom_content:
            timeline_months = 4 + (training_hours_per_employee / 4)
        else:
            timeline_months = 2
        
        # Resource requirements
        resource_requirements = {
            'instructional_designers': 2 if requires_custom_content else 0,
            'trainers': max(1, sessions_needed // 5) if delivery_method != 'online' else 0,
            'program_managers': 1
        }
        
        # Cost breakdown
        cost_breakdown = {
            'content_development': float(content_development_cost),
            'platform_technology': float(platform_cost),
            'instruction_delivery': float(instructor_cost),
            'venue_logistics': float(venue_cost),
            'employee_time': float(employee_time_cost),
            'assessment_certification': float(assessment_cost),
            'refresher_training': float(annual_refresher_cost * refreshers_needed)
        }
        
        return RemediationEstimate(
            total_cost=total_cost,
            cost_range=cost_range,
            timeline_months=timeline_months,
            resource_requirements=resource_requirements,
            cost_breakdown=cost_breakdown,
            complexity_level=ComplexityLevel.MEDIUM.value,
            confidence_level=0.80
        )


class OngoingComplianceEstimator:
    """
    Estimator for ongoing compliance monitoring and maintenance costs.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize ongoing compliance estimator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_ongoing_costs(self,
                              num_compliance_controls: int,
                              monitoring_frequency: str = 'monthly',
                              requires_automated_tools: bool = True,
                              annual_audit_required: bool = True) -> Dict[str, Any]:
        """
        Estimate ongoing compliance costs.
        
        Args:
            num_compliance_controls: Number of compliance controls to monitor
            monitoring_frequency: 'daily', 'weekly', 'monthly', 'quarterly'
            requires_automated_tools: Whether automated monitoring tools needed
            annual_audit_required: Whether annual audits are required
            
        Returns:
            Dictionary with annual ongoing costs
        """
        # Monitoring frequency multiplier
        frequency_multipliers = {
            'daily': 12,
            'weekly': 6,
            'monthly': 3,
            'quarterly': 1
        }
        freq_mult = frequency_multipliers.get(monitoring_frequency, 3)
        
        # Compliance staff costs
        # Estimate 1 FTE per 20 controls
        num_compliance_staff = max(1, num_compliance_controls // 20)
        annual_compliance_staff_cost = num_compliance_staff * 120000  # $120k per FTE
        
        # Automated monitoring tools
        if requires_automated_tools:
            tool_licensing_cost = num_compliance_controls * 1000  # $1k per control
            tool_maintenance_cost = tool_licensing_cost * 0.2  # 20% annual maintenance
            automation_cost = tool_licensing_cost + tool_maintenance_cost
        else:
            automation_cost = 0
        
        # Reporting and documentation costs
        reporting_hours_per_year = num_compliance_controls * freq_mult * 4
        reporting_cost = reporting_hours_per_year * 75
        
        # Annual audit costs
        if annual_audit_required:
            audit_cost = 50000 + (num_compliance_controls * 500)
        else:
            audit_cost = 0
        
        # Training and updates
        annual_training_cost = num_compliance_staff * 2000
        
        # Total annual cost
        total_annual_cost = (
            annual_compliance_staff_cost +
            automation_cost +
            reporting_cost +
            audit_cost +
            annual_training_cost
        )
        
        return {
            'total_annual_cost': float(total_annual_cost),
            'cost_breakdown': {
                'compliance_staff': float(annual_compliance_staff_cost),
                'automation_tools': float(automation_cost),
                'reporting': float(reporting_cost),
                'annual_audit': float(audit_cost),
                'training_updates': float(annual_training_cost)
            },
            'staff_requirements': {
                'compliance_officers': int(num_compliance_staff)
            },
            'monitoring_frequency': monitoring_frequency
        }


class ComprehensiveRemediationPlanner:
    """
    Integrated remediation cost planner combining all remediation types.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize comprehensive remediation planner"""
        self.random_state = random_state
        self.technical_estimator = TechnicalRemediationEstimator(random_state=random_state)
        self.process_estimator = ProcessImprovementEstimator(random_state=random_state)
        self.training_estimator = TrainingCostEstimator(random_state=random_state)
        self.ongoing_estimator = OngoingComplianceEstimator(random_state=random_state)
    
    def create_remediation_plan(self,
                               technical_params: Optional[Dict[str, Any]] = None,
                               process_params: Optional[Dict[str, Any]] = None,
                               training_params: Optional[Dict[str, Any]] = None,
                               ongoing_params: Optional[Dict[str, Any]] = None,
                               planning_horizon_years: int = 3) -> Dict[str, Any]:
        """
        Create comprehensive remediation plan with costs.
        
        Args:
            technical_params: Parameters for technical remediation
            process_params: Parameters for process changes
            training_params: Parameters for training program
            ongoing_params: Parameters for ongoing compliance
            planning_horizon_years: Planning horizon in years
            
        Returns:
            Dictionary with comprehensive remediation plan
        """
        remediation_components = {}
        total_upfront_cost = 0
        total_annual_ongoing_cost = 0
        
        # Technical remediation
        if technical_params:
            tech_estimate = self.technical_estimator.estimate_technical_fix(**technical_params)
            remediation_components['technical'] = tech_estimate.to_dict()
            total_upfront_cost += tech_estimate.total_cost
        
        # Process improvement
        if process_params:
            process_estimate = self.process_estimator.estimate_process_change(**process_params)
            remediation_components['process'] = process_estimate.to_dict()
            total_upfront_cost += process_estimate.total_cost
        
        # Training program
        if training_params:
            training_estimate = self.training_estimator.estimate_training_program(**training_params)
            remediation_components['training'] = training_estimate.to_dict()
            total_upfront_cost += training_estimate.total_cost
        
        # Ongoing compliance
        if ongoing_params:
            ongoing_estimate = self.ongoing_estimator.estimate_ongoing_costs(**ongoing_params)
            remediation_components['ongoing'] = ongoing_estimate
            total_annual_ongoing_cost = ongoing_estimate['total_annual_cost']
        
        # Total cost over planning horizon
        total_cost_over_horizon = total_upfront_cost + (total_annual_ongoing_cost * planning_horizon_years)
        
        # Timeline (longest timeline among components)
        max_timeline = max([
            remediation_components.get('technical', {}).get('timeline_months', 0),
            remediation_components.get('process', {}).get('timeline_months', 0),
            remediation_components.get('training', {}).get('timeline_months', 0)
        ])
        
        return {
            'total_upfront_cost': float(total_upfront_cost),
            'total_annual_ongoing_cost': float(total_annual_ongoing_cost),
            'total_cost_over_horizon': float(total_cost_over_horizon),
            'planning_horizon_years': planning_horizon_years,
            'implementation_timeline_months': float(max_timeline),
            'remediation_components': remediation_components,
            'cost_breakdown_by_year': {
                f'year_{i+1}': float(total_annual_ongoing_cost if i > 0 else total_upfront_cost + total_annual_ongoing_cost)
                for i in range(planning_horizon_years)
            }
        }
