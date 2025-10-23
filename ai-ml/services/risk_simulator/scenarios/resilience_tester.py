"""
Resilience Tester Module

This module implements system resilience testing including:
- Adaptive capacity scoring
- Recovery time estimation
- Mitigation effectiveness testing
- Contingency plan validation
- Preparedness measurement

Integrates with stress scenarios and extreme conditions.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import numpy as np


class ResilienceLevel(Enum):
    """Resilience levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    MODERATE = "moderate"
    POOR = "poor"
    CRITICAL = "critical"


class MitigationStrategy(Enum):
    """Types of mitigation strategies"""
    PREVENTIVE = "preventive"
    DETECTIVE = "detective"
    CORRECTIVE = "corrective"
    ADAPTIVE = "adaptive"


@dataclass
class ResilienceScore:
    """Resilience assessment result"""
    overall_score: float
    resilience_level: str
    adaptive_capacity: float
    recovery_capability: float
    stress_absorption: float
    component_scores: Dict[str, float]
    weaknesses: List[str]
    strengths: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'overall_score': float(self.overall_score),
            'resilience_level': self.resilience_level,
            'adaptive_capacity': float(self.adaptive_capacity),
            'recovery_capability': float(self.recovery_capability),
            'stress_absorption': float(self.stress_absorption),
            'component_scores': {k: float(v) for k, v in self.component_scores.items()},
            'weaknesses': self.weaknesses,
            'strengths': self.strengths
        }


@dataclass
class RecoveryEstimate:
    """Recovery time and cost estimate"""
    estimated_recovery_days: int
    recovery_cost: float
    resource_requirements: Dict[str, Any]
    recovery_phases: List[Dict[str, Any]]
    success_probability: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'estimated_recovery_days': int(self.estimated_recovery_days),
            'recovery_cost': float(self.recovery_cost),
            'resource_requirements': self.resource_requirements,
            'recovery_phases': self.recovery_phases,
            'success_probability': float(self.success_probability)
        }


class ResilienceAnalyzer:
    """Analyze system resilience and adaptive capacity"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def calculate_resilience_score(self,
                                   stress_test_results: Dict[str, Any],
                                   current_capabilities: Dict[str, float]) -> ResilienceScore:
        """
        Calculate overall resilience score
        
        Args:
            stress_test_results: Results from stress testing
            current_capabilities: Current system capabilities
            
        Returns:
            ResilienceScore object
        """
        # Calculate component scores (0-100)
        adaptive_capacity = self._calculate_adaptive_capacity(current_capabilities)
        recovery_capability = self._calculate_recovery_capability(current_capabilities)
        stress_absorption = self._calculate_stress_absorption(stress_test_results)
        
        # Component weights
        weights = {
            'adaptive_capacity': 0.35,
            'recovery_capability': 0.35,
            'stress_absorption': 0.30
        }
        
        # Overall score
        overall = (
            adaptive_capacity * weights['adaptive_capacity'] +
            recovery_capability * weights['recovery_capability'] +
            stress_absorption * weights['stress_absorption']
        )
        
        # Determine resilience level
        if overall >= 85:
            level = ResilienceLevel.EXCELLENT
        elif overall >= 70:
            level = ResilienceLevel.GOOD
        elif overall >= 55:
            level = ResilienceLevel.MODERATE
        elif overall >= 40:
            level = ResilienceLevel.POOR
        else:
            level = ResilienceLevel.CRITICAL
        
        # Identify weaknesses and strengths
        component_scores = {
            'adaptive_capacity': adaptive_capacity,
            'recovery_capability': recovery_capability,
            'stress_absorption': stress_absorption
        }
        
        weaknesses = [k for k, v in component_scores.items() if v < 60]
        strengths = [k for k, v in component_scores.items() if v >= 75]
        
        return ResilienceScore(
            overall_score=overall,
            resilience_level=level.value,
            adaptive_capacity=adaptive_capacity,
            recovery_capability=recovery_capability,
            stress_absorption=stress_absorption,
            component_scores=component_scores,
            weaknesses=weaknesses,
            strengths=strengths
        )
    
    def _calculate_adaptive_capacity(self, capabilities: Dict[str, float]) -> float:
        """Calculate adaptive capacity score"""
        flexibility = capabilities.get('flexibility', 50.0)
        learning_rate = capabilities.get('learning_rate', 50.0)
        innovation = capabilities.get('innovation', 50.0)
        
        return float(np.mean([flexibility, learning_rate, innovation]))
    
    def _calculate_recovery_capability(self, capabilities: Dict[str, float]) -> float:
        """Calculate recovery capability score"""
        response_speed = capabilities.get('response_speed', 50.0)
        resource_availability = capabilities.get('resource_availability', 50.0)
        redundancy = capabilities.get('redundancy', 50.0)
        
        return float(np.mean([response_speed, resource_availability, redundancy]))
    
    def _calculate_stress_absorption(self, stress_results: Dict[str, Any]) -> float:
        """Calculate stress absorption capacity"""
        if not stress_results:
            return 50.0
        
        # Extract metrics from stress test
        failures = stress_results.get('failures', 0)
        max_stress_handled = stress_results.get('max_stress_handled', 0.5)
        degradation_rate = stress_results.get('degradation_rate', 0.5)
        
        # Score based on performance under stress
        failure_score = max(0, 100 - (failures * 20))
        stress_score = max_stress_handled * 100
        degradation_score = max(0, 100 - (degradation_rate * 100))
        
        return float(np.mean([failure_score, stress_score, degradation_score]))
    
    def estimate_recovery_time(self,
                               failure_severity: float,
                               available_resources: Dict[str, float],
                               mitigation_strategies: List[str]) -> RecoveryEstimate:
        """
        Estimate recovery time from failure
        
        Args:
            failure_severity: Severity of failure (0-1)
            available_resources: Available recovery resources
            mitigation_strategies: Active mitigation strategies
            
        Returns:
            RecoveryEstimate object
        """
        # Base recovery time (days) based on severity
        base_recovery = int(30 * failure_severity)
        
        # Adjust for resources
        resource_factor = available_resources.get('personnel', 1.0) * available_resources.get('financial', 1.0)
        resource_factor = max(0.5, min(2.0, resource_factor))  # Bound between 0.5x and 2x
        
        # Adjust for mitigation strategies
        strategy_factor = 1.0 - (len(mitigation_strategies) * 0.1)  # 10% faster per strategy
        strategy_factor = max(0.5, strategy_factor)
        
        # Calculate adjusted recovery time
        adjusted_recovery = int(base_recovery * resource_factor * strategy_factor)
        
        # Estimate cost
        daily_cost = 50000  # $50k per day baseline
        recovery_cost = adjusted_recovery * daily_cost * (1 + failure_severity)
        
        # Define recovery phases
        phases = [
            {
                'phase': 'Assessment',
                'duration_days': max(1, int(adjusted_recovery * 0.1)),
                'cost': recovery_cost * 0.05,
                'key_activities': ['Damage assessment', 'Resource mobilization']
            },
            {
                'phase': 'Stabilization',
                'duration_days': int(adjusted_recovery * 0.3),
                'cost': recovery_cost * 0.25,
                'key_activities': ['Stop degradation', 'Implement emergency measures']
            },
            {
                'phase': 'Restoration',
                'duration_days': int(adjusted_recovery * 0.4),
                'cost': recovery_cost * 0.50,
                'key_activities': ['Restore systems', 'Rebuild capabilities']
            },
            {
                'phase': 'Improvement',
                'duration_days': int(adjusted_recovery * 0.2),
                'cost': recovery_cost * 0.20,
                'key_activities': ['Implement learnings', 'Enhance resilience']
            }
        ]
        
        # Success probability
        success_prob = min(0.95, 0.7 + (len(mitigation_strategies) * 0.05) + (resource_factor * 0.1))
        
        # Resource requirements
        resource_reqs = {
            'personnel_fte': int(5 * failure_severity),
            'financial_budget': float(recovery_cost),
            'technology_investment': float(recovery_cost * 0.3),
            'external_support': bool(failure_severity > 0.7)
        }
        
        return RecoveryEstimate(
            estimated_recovery_days=adjusted_recovery,
            recovery_cost=recovery_cost,
            resource_requirements=resource_reqs,
            recovery_phases=phases,
            success_probability=success_prob
        )


class ContingencyValidator:
    """Validate contingency plans and preparedness"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def validate_contingency_plan(self,
                                  plan: Dict[str, Any],
                                  stress_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate contingency plan against stress scenario
        
        Args:
            plan: Contingency plan details
            stress_scenario: Stress scenario to test against
            
        Returns:
            Dictionary with validation results
        """
        # Extract plan elements
        triggers = plan.get('triggers', [])
        responses = plan.get('responses', [])
        resources = plan.get('resources', {})
        timeline = plan.get('timeline_days', 30)
        
        # Validate coverage
        scenario_severity = stress_scenario.get('severity_score', 50)
        coverage_score = self._calculate_coverage(triggers, responses, scenario_severity)
        
        # Validate adequacy
        adequacy_score = self._validate_resource_adequacy(resources, stress_scenario)
        
        # Validate timeliness
        timeliness_score = self._validate_timeline(timeline, stress_scenario)
        
        # Overall effectiveness
        effectiveness = float(np.mean([coverage_score, adequacy_score, timeliness_score]))
        
        # Identify gaps
        gaps = []
        if coverage_score < 70:
            gaps.append("Insufficient trigger coverage")
        if adequacy_score < 70:
            gaps.append("Inadequate resource allocation")
        if timeliness_score < 70:
            gaps.append("Timeline too slow for scenario")
        
        # Recommendations
        recommendations = self._generate_recommendations(coverage_score, adequacy_score, timeliness_score)
        
        return {
            'overall_effectiveness': float(effectiveness),
            'coverage_score': float(coverage_score),
            'adequacy_score': float(adequacy_score),
            'timeliness_score': float(timeliness_score),
            'gaps_identified': gaps,
            'recommendations': recommendations,
            'plan_valid': bool(effectiveness >= 70)
        }
    
    def _calculate_coverage(self, triggers: List[str], responses: List[str], severity: float) -> float:
        """Calculate scenario coverage"""
        # More triggers/responses = better coverage
        trigger_coverage = min(100, len(triggers) * 20)
        response_coverage = min(100, len(responses) * 15)
        severity_adjustment = (100 - severity) / 100  # Harder to cover severe scenarios
        
        return float((trigger_coverage + response_coverage) / 2 * severity_adjustment)
    
    def _validate_resource_adequacy(self, resources: Dict[str, Any], scenario: Dict[str, Any]) -> float:
        """Validate resource adequacy"""
        required_budget = scenario.get('expected_financial_impact', 1000000)
        available_budget = resources.get('financial_budget', 0)
        
        required_personnel = scenario.get('personnel_required', 10)
        available_personnel = resources.get('personnel_fte', 0)
        
        budget_ratio = min(1.0, available_budget / required_budget) if required_budget > 0 else 0.5
        personnel_ratio = min(1.0, available_personnel / required_personnel) if required_personnel > 0 else 0.5
        
        return float((budget_ratio + personnel_ratio) / 2 * 100)
    
    def _validate_timeline(self, plan_timeline: int, scenario: Dict[str, Any]) -> float:
        """Validate timeline adequacy"""
        required_timeline = scenario.get('time_horizon_days', 30)
        
        if plan_timeline <= required_timeline:
            return 100.0  # Perfect
        elif plan_timeline <= required_timeline * 1.5:
            return 75.0  # Acceptable
        elif plan_timeline <= required_timeline * 2:
            return 50.0  # Marginal
        else:
            return 25.0  # Too slow
    
    def _generate_recommendations(self, coverage: float, adequacy: float, timeliness: float) -> List[str]:
        """Generate improvement recommendations"""
        recs = []
        
        if coverage < 70:
            recs.append("Add more scenario triggers and response procedures")
        if adequacy < 70:
            recs.append("Increase resource allocation (budget and personnel)")
        if timeliness < 70:
            recs.append("Compress timeline and improve response speed")
        
        if all(score >= 70 for score in [coverage, adequacy, timeliness]):
            recs.append("Plan is adequate - focus on testing and refinement")
        
        return recs
    
    def measure_preparedness(self,
                            contingency_plans: List[Dict[str, Any]],
                            identified_risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Measure overall preparedness
        
        Args:
            contingency_plans: List of contingency plans
            identified_risks: List of identified risks
            
        Returns:
            Dictionary with preparedness metrics
        """
        num_plans = len(contingency_plans)
        num_risks = len(identified_risks)
        
        # Coverage ratio
        coverage_ratio = min(1.0, num_plans / num_risks) if num_risks > 0 else 0.0
        
        # Plan quality (average effectiveness)
        plan_quality_scores = []
        for plan in contingency_plans:
            # Simple quality score based on completeness
            has_triggers = bool(plan.get('triggers'))
            has_responses = bool(plan.get('responses'))
            has_resources = bool(plan.get('resources'))
            has_timeline = bool(plan.get('timeline_days'))
            
            quality = sum([has_triggers, has_responses, has_resources, has_timeline]) / 4 * 100
            plan_quality_scores.append(quality)
        
        avg_quality = float(np.mean(plan_quality_scores)) if plan_quality_scores else 0.0
        
        # Overall preparedness score
        preparedness = (coverage_ratio * 0.5 + avg_quality / 100 * 0.5) * 100
        
        return {
            'preparedness_score': float(preparedness),
            'coverage_ratio': float(coverage_ratio),
            'num_plans': num_plans,
            'num_risks': num_risks,
            'average_plan_quality': float(avg_quality),
            'gaps': max(0, num_risks - num_plans),
            'preparedness_level': 'excellent' if preparedness >= 85 else
                                 'good' if preparedness >= 70 else
                                 'moderate' if preparedness >= 55 else
                                 'poor'
        }
