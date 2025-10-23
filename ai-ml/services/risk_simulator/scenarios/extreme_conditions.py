"""
Extreme Conditions Module

This module implements extreme condition simulation including:
- Maximum penalty scenarios
- Simultaneous multi-jurisdiction violations
- Resource exhaustion scenarios
- Timeline compression scenarios
- Breaking point analysis

Integrates with all Phase 4.2 risk models for stress testing.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import numpy as np


class ExtremeScenarioType(Enum):
    """Types of extreme scenarios"""
    MAX_PENALTY = "max_penalty"
    SIMULTANEOUS_VIOLATIONS = "simultaneous_violations"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    TIMELINE_COMPRESSION = "timeline_compression"
    PERFECT_STORM = "perfect_storm"


class ResourceType(Enum):
    """Resource types that can be exhausted"""
    FINANCIAL = "financial"
    PERSONNEL = "personnel"
    TECHNICAL = "technical"
    TIME = "time"


@dataclass
class ExtremeCondition:
    """Extreme condition definition"""
    condition_id: str
    condition_type: str
    severity_multiplier: float
    description: str
    impact_areas: List[str]
    probability: float
    mitigation_cost_multiplier: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'condition_id': self.condition_id,
            'condition_type': self.condition_type,
            'severity_multiplier': float(self.severity_multiplier),
            'description': self.description,
            'impact_areas': self.impact_areas,
            'probability': float(self.probability),
            'mitigation_cost_multiplier': float(self.mitigation_cost_multiplier)
        }


@dataclass
class BreakingPoint:
    """Breaking point analysis result"""
    resource_type: str
    threshold_value: float
    current_capacity: float
    safety_margin: float
    time_to_exhaustion_days: int
    recovery_requirements: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'resource_type': self.resource_type,
            'threshold_value': float(self.threshold_value),
            'current_capacity': float(self.current_capacity),
            'safety_margin': float(self.safety_margin),
            'time_to_exhaustion_days': int(self.time_to_exhaustion_days),
            'recovery_requirements': self.recovery_requirements
        }


class ExtremeConditionSimulator:
    """Simulate extreme conditions and scenarios"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def create_max_penalty_scenario(self,
                                    base_penalty: float,
                                    num_violations: int = 5) -> Dict[str, Any]:
        """
        Create maximum penalty scenario
        
        Args:
            base_penalty: Base penalty amount
            num_violations: Number of simultaneous violations
            
        Returns:
            Dictionary with penalty details
        """
        # Maximum penalty multipliers
        jurisdiction_mult = 3.0  # Multiple jurisdictions
        severity_mult = 4.0  # Critical severity
        repeat_mult = 2.5  # Repeat offender
        timing_mult = 1.8  # During strict enforcement
        
        total_multiplier = jurisdiction_mult * severity_mult * repeat_mult * timing_mult
        
        max_single_penalty = base_penalty * total_multiplier
        total_penalty = max_single_penalty * num_violations
        
        # Add daily accrual penalties
        daily_penalty = base_penalty * 0.05  # 5% per day
        accrual_days = 180  # 6 months
        accrued_penalties = daily_penalty * accrual_days * num_violations
        
        grand_total = total_penalty + accrued_penalties
        
        return {
            'scenario_type': ExtremeScenarioType.MAX_PENALTY.value,
            'base_penalty': float(base_penalty),
            'num_violations': int(num_violations),
            'total_multiplier': float(total_multiplier),
            'max_single_penalty': float(max_single_penalty),
            'total_initial_penalty': float(total_penalty),
            'daily_accrual_penalty': float(daily_penalty),
            'accrual_days': int(accrual_days),
            'total_accrued_penalties': float(accrued_penalties),
            'grand_total_penalty': float(grand_total),
            'probability': 0.001  # Very low probability
        }
    
    def create_simultaneous_violations_scenario(self,
                                                jurisdictions: List[str],
                                                violation_types: List[str]) -> ExtremeCondition:
        """
        Create simultaneous multi-jurisdiction violation scenario
        
        Args:
            jurisdictions: List of jurisdictions
            violation_types: Types of violations
            
        Returns:
            ExtremeCondition object
        """
        num_jurisdictions = len(jurisdictions)
        num_violations = len(violation_types)
        
        # Severity multiplier increases exponentially with jurisdictions
        severity_mult = 1.5 ** num_jurisdictions * num_violations
        
        # Probability decreases with complexity
        probability = max(0.001, 0.1 / (num_jurisdictions * num_violations))
        
        # Mitigation becomes exponentially harder
        mitigation_mult = 2.0 ** num_jurisdictions
        
        condition_id = f"EXTREME-SIMUL-{self.rng.randint(1000, 9999)}"
        
        impact_areas = [
            f"{j}_{v}" for j in jurisdictions for v in violation_types
        ]
        
        return ExtremeCondition(
            condition_id=condition_id,
            condition_type=ExtremeScenarioType.SIMULTANEOUS_VIOLATIONS.value,
            severity_multiplier=severity_mult,
            description=f"Simultaneous violations across {num_jurisdictions} jurisdictions",
            impact_areas=impact_areas[:10],  # Limit for readability
            probability=probability,
            mitigation_cost_multiplier=mitigation_mult
        )
    
    def create_resource_exhaustion_scenario(self,
                                           resource_type: ResourceType,
                                           current_capacity: float,
                                           demand_rate: float) -> Dict[str, Any]:
        """
        Create resource exhaustion scenario
        
        Args:
            resource_type: Type of resource
            current_capacity: Current resource capacity
            demand_rate: Rate of resource consumption
            
        Returns:
            Dictionary with exhaustion details
        """
        # Calculate time to exhaustion
        if demand_rate > 0:
            time_to_exhaustion = current_capacity / demand_rate
        else:
            time_to_exhaustion = float('inf')
        
        # Critical threshold (80% capacity)
        critical_threshold = current_capacity * 0.8
        time_to_critical = critical_threshold / demand_rate if demand_rate > 0 else float('inf')
        
        # Recovery requirements
        recovery_cost_multipliers = {
            ResourceType.FINANCIAL: 1.5,
            ResourceType.PERSONNEL: 2.0,
            ResourceType.TECHNICAL: 1.8,
            ResourceType.TIME: 1.2
        }
        
        recovery_mult = recovery_cost_multipliers.get(resource_type, 1.5)
        recovery_cost = current_capacity * recovery_mult
        recovery_time_days = int(30 * recovery_mult)
        
        return {
            'scenario_type': ExtremeScenarioType.RESOURCE_EXHAUSTION.value,
            'resource_type': resource_type.value,
            'current_capacity': float(current_capacity),
            'demand_rate': float(demand_rate),
            'time_to_exhaustion_days': float(time_to_exhaustion) if time_to_exhaustion != float('inf') else None,
            'time_to_critical_days': float(time_to_critical) if time_to_critical != float('inf') else None,
            'critical_threshold': float(critical_threshold),
            'recovery_cost': float(recovery_cost),
            'recovery_time_days': int(recovery_time_days),
            'severity': 'critical' if time_to_exhaustion < 90 else 'high' if time_to_exhaustion < 180 else 'moderate'
        }
    
    def create_timeline_compression_scenario(self,
                                            normal_timeline_days: int,
                                            compression_factor: float = 0.2) -> Dict[str, Any]:
        """
        Create timeline compression scenario
        
        Args:
            normal_timeline_days: Normal implementation timeline
            compression_factor: Compression factor (0.2 = 20% of normal time)
            
        Returns:
            Dictionary with compression details
        """
        compressed_timeline = int(normal_timeline_days * compression_factor)
        time_saved = normal_timeline_days - compressed_timeline
        
        # Cost multiplier increases exponentially with compression
        cost_multiplier = 1.0 / (compression_factor ** 1.5)
        
        # Resource multiplier (need more resources for faster completion)
        resource_multiplier = 1.0 / compression_factor
        
        # Risk multiplier (higher risk with rushed timeline)
        risk_multiplier = 2.0 / compression_factor
        
        # Probability of success decreases with compression
        success_probability = max(0.1, compression_factor ** 0.5)
        
        return {
            'scenario_type': ExtremeScenarioType.TIMELINE_COMPRESSION.value,
            'normal_timeline_days': int(normal_timeline_days),
            'compressed_timeline_days': int(compressed_timeline),
            'compression_factor': float(compression_factor),
            'time_saved_days': int(time_saved),
            'cost_multiplier': float(cost_multiplier),
            'resource_multiplier': float(resource_multiplier),
            'risk_multiplier': float(risk_multiplier),
            'success_probability': float(success_probability),
            'recommended': bool(compression_factor >= 0.5)  # Don't compress below 50%
        }


class BreakingPointAnalyzer:
    """Analyze breaking points and failure thresholds"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def identify_breaking_point(self,
                                resource_type: ResourceType,
                                current_capacity: float,
                                stress_load: float,
                                sustained_duration_days: int = 30) -> BreakingPoint:
        """
        Identify breaking point for a resource under stress
        
        Args:
            resource_type: Type of resource
            current_capacity: Current resource capacity
            stress_load: Stress load on resource
            sustained_duration_days: Duration stress is sustained
            
        Returns:
            BreakingPoint object
        """
        # Calculate threshold (point of failure)
        threshold_factors = {
            ResourceType.FINANCIAL: 0.95,  # Can leverage 95% before breaking
            ResourceType.PERSONNEL: 0.85,  # Burnout at 85%
            ResourceType.TECHNICAL: 0.90,  # System failure at 90%
            ResourceType.TIME: 1.00  # No buffer for time
        }
        
        threshold_factor = threshold_factors.get(resource_type, 0.90)
        threshold_value = current_capacity * threshold_factor
        
        # Calculate safety margin
        safety_margin = (threshold_value - stress_load) / threshold_value if threshold_value > 0 else 0
        
        # Time to exhaustion
        if stress_load > current_capacity:
            time_to_exhaustion = 0  # Already exceeded
        elif stress_load > 0:
            remaining_capacity = threshold_value - stress_load
            # Assume linear degradation
            degradation_rate = stress_load / sustained_duration_days
            time_to_exhaustion = int(remaining_capacity / degradation_rate) if degradation_rate > 0 else 999
        else:
            time_to_exhaustion = 999  # No stress
        
        # Recovery requirements
        recovery_requirements = self._calculate_recovery_requirements(
            resource_type,
            current_capacity,
            stress_load
        )
        
        return BreakingPoint(
            resource_type=resource_type.value,
            threshold_value=threshold_value,
            current_capacity=current_capacity,
            safety_margin=safety_margin,
            time_to_exhaustion_days=time_to_exhaustion,
            recovery_requirements=recovery_requirements
        )
    
    def _calculate_recovery_requirements(self,
                                        resource_type: ResourceType,
                                        capacity: float,
                                        stress: float) -> Dict[str, Any]:
        """Calculate requirements to recover from breaking point"""
        
        overstress = max(0, stress - capacity)
        recovery_multipliers = {
            ResourceType.FINANCIAL: 1.2,
            ResourceType.PERSONNEL: 2.5,
            ResourceType.TECHNICAL: 1.8,
            ResourceType.TIME: 1.0
        }
        
        mult = recovery_multipliers.get(resource_type, 1.5)
        
        return {
            'additional_capacity_needed': float(overstress * mult),
            'recovery_time_days': int(30 * mult),
            'recovery_cost_multiplier': float(mult),
            'emergency_measures_required': bool(overstress > capacity * 0.2)
        }
    
    def calculate_system_resilience(self,
                                   breaking_points: List[BreakingPoint]) -> Dict[str, Any]:
        """
        Calculate overall system resilience from multiple breaking points
        
        Args:
            breaking_points: List of breaking points
            
        Returns:
            Dictionary with resilience metrics
        """
        if not breaking_points:
            return {
                'overall_resilience_score': 100.0,
                'weakest_resource': None,
                'time_to_system_failure_days': 999
            }
        
        # Calculate resilience scores (0-100)
        resilience_scores = []
        for bp in breaking_points:
            # Score based on safety margin
            score = max(0, min(100, bp.safety_margin * 100))
            resilience_scores.append(score)
        
        overall_score = float(np.mean(resilience_scores))
        
        # Identify weakest link
        min_margin_idx = np.argmin([bp.safety_margin for bp in breaking_points])
        weakest_bp = breaking_points[min_margin_idx]
        
        # Time to system failure = time to first breaking point
        time_to_failure = min(bp.time_to_exhaustion_days for bp in breaking_points)
        
        return {
            'overall_resilience_score': float(overall_score),
            'weakest_resource': weakest_bp.resource_type,
            'weakest_safety_margin': float(weakest_bp.safety_margin),
            'time_to_system_failure_days': int(time_to_failure),
            'num_resources_at_risk': sum(1 for bp in breaking_points if bp.safety_margin < 0.2),
            'recommended_actions': self._get_recommended_actions(breaking_points)
        }
    
    def _get_recommended_actions(self, breaking_points: List[BreakingPoint]) -> List[str]:
        """Get recommended actions based on breaking points"""
        actions = []
        
        for bp in breaking_points:
            if bp.safety_margin < 0.1:
                actions.append(f"URGENT: Increase {bp.resource_type} capacity immediately")
            elif bp.safety_margin < 0.2:
                actions.append(f"HIGH PRIORITY: Plan {bp.resource_type} capacity expansion")
            elif bp.safety_margin < 0.3:
                actions.append(f"MONITOR: Watch {bp.resource_type} utilization closely")
        
        return actions
