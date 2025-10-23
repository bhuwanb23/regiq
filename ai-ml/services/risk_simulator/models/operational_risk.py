"""
Operational Risk Models

This module implements models for operational risks from regulatory compliance
issues, including system downtime, performance degradation, and operational
capacity impacts with probabilistic modeling.

Models:
- SystemDowntimeModel: Model system availability and downtime
- PerformanceDegradationModel: Model system performance impacts
- CapacityUtilizationModel: Model capacity utilization changes
- OperationalRiskAggregator: Comprehensive operational risk assessment
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats


class SystemCriticality(Enum):
    """System criticality levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DowntimeCategory(Enum):
    """Downtime categories"""
    PLANNED = "planned"
    UNPLANNED = "unplanned"
    EMERGENCY = "emergency"


@dataclass
class DowntimeImpact:
    """Result container for downtime impact analysis"""
    expected_downtime_hours: float
    downtime_probability: float
    revenue_impact_per_hour: float
    total_revenue_impact: float
    recovery_time_hours: float
    mitigation_cost: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'expected_downtime_hours': float(self.expected_downtime_hours),
            'downtime_probability': float(self.downtime_probability),
            'revenue_impact_per_hour': float(self.revenue_impact_per_hour),
            'total_revenue_impact': float(self.total_revenue_impact),
            'recovery_time_hours': float(self.recovery_time_hours),
            'mitigation_cost': float(self.mitigation_cost)
        }


@dataclass
class PerformanceImpact:
    """Result container for performance degradation"""
    performance_degradation_pct: float
    affected_transactions: int
    transaction_delay_ms: float
    user_experience_score: float
    productivity_loss_pct: float
    total_cost: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'performance_degradation_pct': float(self.performance_degradation_pct),
            'affected_transactions': int(self.affected_transactions),
            'transaction_delay_ms': float(self.transaction_delay_ms),
            'user_experience_score': float(self.user_experience_score),
            'productivity_loss_pct': float(self.productivity_loss_pct),
            'total_cost': float(self.total_cost)
        }


@dataclass
class OperationalRiskResult:
    """Comprehensive operational risk assessment"""
    total_operational_risk_score: float
    downtime_impact: DowntimeImpact
    performance_impact: PerformanceImpact
    capacity_utilization_pct: float
    risk_category: str
    mitigation_priority: str
    estimated_annual_cost: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'total_operational_risk_score': float(self.total_operational_risk_score),
            'downtime_impact': self.downtime_impact.to_dict(),
            'performance_impact': self.performance_impact.to_dict(),
            'capacity_utilization_pct': float(self.capacity_utilization_pct),
            'risk_category': self.risk_category,
            'mitigation_priority': self.mitigation_priority,
            'estimated_annual_cost': float(self.estimated_annual_cost)
        }


class SystemDowntimeModel:
    """
    Model for system downtime and availability impacts.
    
    Uses exponential and Weibull distributions for failure modeling.
    """
    
    # Criticality to impact multipliers
    CRITICALITY_MULTIPLIERS = {
        SystemCriticality.LOW: 0.25,
        SystemCriticality.MEDIUM: 0.5,
        SystemCriticality.HIGH: 1.0,
        SystemCriticality.CRITICAL: 2.0
    }
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize system downtime model"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_downtime(self,
                         system_criticality: SystemCriticality,
                         mtbf_hours: float,
                         mttr_hours: float,
                         annual_revenue: float,
                         downtime_category: DowntimeCategory = DowntimeCategory.UNPLANNED) -> DowntimeImpact:
        """
        Estimate system downtime impact.
        
        Args:
            system_criticality: Criticality level of system
            mtbf_hours: Mean Time Between Failures
            mttr_hours: Mean Time To Repair
            annual_revenue: Annual revenue for impact calculation
            downtime_category: Category of downtime
            
        Returns:
            DowntimeImpact with detailed analysis
        """
        # Calculate expected downtime per year
        # Using reliability theory: failures per year = 8760 / MTBF
        hours_per_year = 8760
        expected_failures_per_year = hours_per_year / mtbf_hours
        expected_downtime_hours = expected_failures_per_year * mttr_hours
        
        # Apply criticality multiplier
        criticality_mult = self.CRITICALITY_MULTIPLIERS[system_criticality]
        
        # Downtime probability (availability = 1 - downtime/total_time)
        availability = 1 - (expected_downtime_hours / hours_per_year)
        downtime_probability = 1 - availability
        
        # Revenue impact
        revenue_per_hour = annual_revenue / hours_per_year
        revenue_impact_per_hour = revenue_per_hour * criticality_mult
        total_revenue_impact = revenue_impact_per_hour * expected_downtime_hours
        
        # Recovery time (depends on downtime category)
        if downtime_category == DowntimeCategory.PLANNED:
            recovery_mult = 1.0
        elif downtime_category == DowntimeCategory.UNPLANNED:
            recovery_mult = 1.5
        else:  # EMERGENCY
            recovery_mult = 2.5
        
        recovery_time_hours = mttr_hours * recovery_mult
        
        # Mitigation cost (redundancy, backup systems, etc.)
        mitigation_cost = total_revenue_impact * 0.15  # 15% of impact
        
        return DowntimeImpact(
            expected_downtime_hours=expected_downtime_hours,
            downtime_probability=downtime_probability,
            revenue_impact_per_hour=revenue_impact_per_hour,
            total_revenue_impact=total_revenue_impact,
            recovery_time_hours=recovery_time_hours,
            mitigation_cost=mitigation_cost
        )
    
    def monte_carlo_downtime(self,
                            mtbf_hours: float,
                            mttr_hours: float,
                            n_simulations: int = 10000,
                            simulation_period_hours: float = 8760) -> Dict[str, Any]:
        """
        Monte Carlo simulation of downtime events.
        
        Args:
            mtbf_hours: Mean Time Between Failures
            mttr_hours: Mean Time To Repair
            n_simulations: Number of simulations
            simulation_period_hours: Simulation period in hours
            
        Returns:
            Dictionary with downtime statistics
        """
        downtime_samples = []
        
        for _ in range(n_simulations):
            # Simulate failures using exponential distribution
            failure_times = []
            cumulative_time = 0
            
            while cumulative_time < simulation_period_hours:
                time_to_failure = self.rng.exponential(mtbf_hours)
                cumulative_time += time_to_failure
                
                if cumulative_time < simulation_period_hours:
                    failure_times.append(cumulative_time)
            
            # Simulate repair times
            num_failures = len(failure_times)
            repair_times = self.rng.exponential(mttr_hours, size=num_failures)
            total_downtime = np.sum(repair_times)
            
            downtime_samples.append(total_downtime)
        
        samples_array = np.array(downtime_samples)
        
        return {
            'mean_downtime_hours': float(np.mean(samples_array)),
            'median_downtime_hours': float(np.median(samples_array)),
            'std_downtime_hours': float(np.std(samples_array)),
            'percentile_90': float(np.percentile(samples_array, 90)),
            'percentile_95': float(np.percentile(samples_array, 95)),
            'percentile_99': float(np.percentile(samples_array, 99)),
            'max_downtime': float(np.max(samples_array))
        }


class PerformanceDegradationModel:
    """
    Model for system performance degradation impacts.
    
    Quantifies effects of reduced system performance on operations.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize performance degradation model"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_performance_impact(self,
                                   baseline_performance: float,
                                   degraded_performance: float,
                                   daily_transactions: int,
                                   transaction_value: float,
                                   num_users: int) -> PerformanceImpact:
        """
        Estimate performance degradation impact.
        
        Args:
            baseline_performance: Baseline performance (transactions/sec)
            degraded_performance: Degraded performance (transactions/sec)
            daily_transactions: Average daily transactions
            transaction_value: Average transaction value
            num_users: Number of affected users
            
        Returns:
            PerformanceImpact with detailed analysis
        """
        # Performance degradation percentage
        performance_degradation_pct = ((baseline_performance - degraded_performance) / baseline_performance) * 100
        
        # Affected transactions (those that experience delays)
        affected_transactions = int(daily_transactions * (performance_degradation_pct / 100))
        
        # Transaction delay in milliseconds
        # Assuming linear relationship with degradation
        baseline_response_ms = 100  # Baseline response time
        transaction_delay_ms = baseline_response_ms * (performance_degradation_pct / 100) * 2
        
        # User experience score (0-100, inversely proportional to delay)
        # Perfect UX = 100, degrades with delay
        ux_score = max(0, 100 - (transaction_delay_ms / 10))
        
        # Productivity loss
        # Employees lose productivity waiting for slow systems
        avg_delay_seconds = transaction_delay_ms / 1000
        transactions_per_user_per_day = daily_transactions / max(1, num_users)
        time_lost_per_user_per_day = (transactions_per_user_per_day * avg_delay_seconds) / 3600  # hours
        
        productivity_loss_pct = (time_lost_per_user_per_day / 8) * 100  # 8-hour workday
        
        # Cost calculation
        # Lost transactions (some customers abandon)
        abandonment_rate = min(0.5, performance_degradation_pct / 200)  # Up to 50%
        lost_transaction_value = affected_transactions * transaction_value * abandonment_rate * 365
        
        # Productivity cost
        avg_hourly_wage = 50
        annual_productivity_cost = num_users * time_lost_per_user_per_day * avg_hourly_wage * 250  # 250 workdays
        
        total_cost = lost_transaction_value + annual_productivity_cost
        
        return PerformanceImpact(
            performance_degradation_pct=performance_degradation_pct,
            affected_transactions=affected_transactions,
            transaction_delay_ms=transaction_delay_ms,
            user_experience_score=ux_score,
            productivity_loss_pct=productivity_loss_pct,
            total_cost=total_cost
        )


class CapacityUtilizationModel:
    """
    Model for capacity utilization and resource constraints.
    
    Analyzes operational capacity impacts from compliance requirements.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize capacity utilization model"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_capacity_impact(self,
                                current_utilization: float,
                                compliance_overhead: float,
                                max_capacity: float,
                                demand_growth_rate: float = 0.10) -> Dict[str, Any]:
        """
        Estimate capacity utilization impact.
        
        Args:
            current_utilization: Current capacity utilization (0-1)
            compliance_overhead: Compliance overhead as fraction (0-1)
            max_capacity: Maximum capacity units
            demand_growth_rate: Annual demand growth rate
            
        Returns:
            Dictionary with capacity analysis
        """
        # Effective capacity after compliance overhead
        effective_capacity = max_capacity * (1 - compliance_overhead)
        
        # New utilization
        current_demand = current_utilization * max_capacity
        new_utilization = current_demand / effective_capacity
        
        # Time to capacity constraint (years)
        # Assuming linear demand growth
        if new_utilization >= 0.85:  # Already near capacity
            time_to_constraint = 0
        else:
            available_headroom = 0.85 - new_utilization
            years_of_growth = available_headroom / demand_growth_rate if demand_growth_rate > 0 else float('inf')
            time_to_constraint = max(0, years_of_growth)
        
        # Capacity expansion cost (if needed)
        if new_utilization > 0.85:
            capacity_deficit = (new_utilization - 0.85) * effective_capacity
            cost_per_unit = 10000  # Example cost per capacity unit
            expansion_cost = capacity_deficit * cost_per_unit
        else:
            expansion_cost = 0
        
        return {
            'current_utilization_pct': float(current_utilization * 100),
            'new_utilization_pct': float(new_utilization * 100),
            'effective_capacity': float(effective_capacity),
            'capacity_reduction_pct': float(compliance_overhead * 100),
            'time_to_constraint_years': float(time_to_constraint),
            'expansion_required': bool(new_utilization > 0.85),
            'estimated_expansion_cost': float(expansion_cost),
            'utilization_category': self._categorize_utilization(new_utilization)
        }
    
    def _categorize_utilization(self, utilization: float) -> str:
        """Categorize utilization level"""
        if utilization < 0.5:
            return "LOW"
        elif utilization < 0.70:
            return "MODERATE"
        elif utilization < 0.85:
            return "HIGH"
        else:
            return "CRITICAL"


class OperationalRiskAggregator:
    """
    Aggregates all operational risk factors into comprehensive assessment.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize operational risk aggregator"""
        self.random_state = random_state
        self.downtime_model = SystemDowntimeModel(random_state=random_state)
        self.performance_model = PerformanceDegradationModel(random_state=random_state)
        self.capacity_model = CapacityUtilizationModel(random_state=random_state)
    
    def assess_operational_risk(self,
                               downtime_params: Dict[str, Any],
                               performance_params: Dict[str, Any],
                               capacity_params: Dict[str, Any]) -> OperationalRiskResult:
        """
        Comprehensive operational risk assessment.
        
        Args:
            downtime_params: Parameters for downtime model
            performance_params: Parameters for performance model
            capacity_params: Parameters for capacity model
            
        Returns:
            OperationalRiskResult with comprehensive assessment
        """
        # Calculate individual impacts
        downtime_impact = self.downtime_model.estimate_downtime(**downtime_params)
        performance_impact = self.performance_model.estimate_performance_impact(**performance_params)
        capacity_analysis = self.capacity_model.estimate_capacity_impact(**capacity_params)
        
        # Calculate total operational risk score (0-100)
        # Weighted combination of factors
        downtime_score = min(100, (downtime_impact.downtime_probability * 1000))
        performance_score = performance_impact.performance_degradation_pct
        capacity_score = max(0, (capacity_analysis['new_utilization_pct'] - 50))  # Score increases above 50%
        
        total_risk_score = (
            downtime_score * 0.4 +
            performance_score * 0.35 +
            capacity_score * 0.25
        )
        
        # Risk category
        if total_risk_score < 20:
            risk_category = "LOW"
        elif total_risk_score < 40:
            risk_category = "MODERATE"
        elif total_risk_score < 60:
            risk_category = "HIGH"
        else:
            risk_category = "CRITICAL"
        
        # Mitigation priority
        if total_risk_score > 60 or downtime_impact.downtime_probability > 0.1:
            mitigation_priority = "IMMEDIATE"
        elif total_risk_score > 40:
            mitigation_priority = "HIGH"
        elif total_risk_score > 20:
            mitigation_priority = "MEDIUM"
        else:
            mitigation_priority = "LOW"
        
        # Estimated annual cost
        annual_cost = (
            downtime_impact.total_revenue_impact +
            performance_impact.total_cost +
            capacity_analysis['estimated_expansion_cost']
        )
        
        return OperationalRiskResult(
            total_operational_risk_score=total_risk_score,
            downtime_impact=downtime_impact,
            performance_impact=performance_impact,
            capacity_utilization_pct=capacity_analysis['new_utilization_pct'],
            risk_category=risk_category,
            mitigation_priority=mitigation_priority,
            estimated_annual_cost=annual_cost
        )
