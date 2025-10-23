"""
Financial Impact Models for Regulatory Violations

This module implements models for calculating the financial impact of regulatory
violations, including potential fines, business disruption costs, and total
financial exposure with uncertainty quantification.

Models:
- PotentialFineCalculator: Estimate fine amounts with probability distributions
- BusinessDisruptionModel: Model revenue loss and operational disruption costs
- FinancialImpactAggregator: Combine all financial impacts with uncertainty
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats


class FineCategory(Enum):
    """Categories of regulatory fines"""
    ADMINISTRATIVE = "administrative"
    CIVIL = "civil"
    CRIMINAL = "criminal"
    STATUTORY = "statutory"


class DisruptionSeverity(Enum):
    """Business disruption severity levels"""
    MINIMAL = "minimal"
    MODERATE = "moderate"
    SIGNIFICANT = "significant"
    SEVERE = "severe"
    CATASTROPHIC = "catastrophic"


@dataclass
class FineEstimate:
    """Result container for fine estimation"""
    expected_fine: float
    fine_range: Tuple[float, float]
    probability_distribution: str
    confidence_level: float
    fine_category: str
    jurisdiction: str
    breakdown: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'expected_fine': float(self.expected_fine),
            'fine_range': tuple(float(x) for x in self.fine_range),
            'probability_distribution': self.probability_distribution,
            'confidence_level': float(self.confidence_level),
            'fine_category': self.fine_category,
            'jurisdiction': self.jurisdiction,
            'breakdown': {k: float(v) for k, v in self.breakdown.items()}
        }


@dataclass
class DisruptionCost:
    """Result container for business disruption costs"""
    total_cost: float
    cost_breakdown: Dict[str, float]
    disruption_severity: str
    duration_days: float
    revenue_impact: float
    operational_cost: float
    reputation_cost: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'total_cost': float(self.total_cost),
            'cost_breakdown': {k: float(v) for k, v in self.cost_breakdown.items()},
            'disruption_severity': self.disruption_severity,
            'duration_days': float(self.duration_days),
            'revenue_impact': float(self.revenue_impact),
            'operational_cost': float(self.operational_cost),
            'reputation_cost': float(self.reputation_cost)
        }


@dataclass
class FinancialImpactResult:
    """Comprehensive financial impact assessment"""
    total_financial_impact: float
    expected_fines: float
    business_disruption_cost: float
    other_costs: float
    impact_range: Tuple[float, float]
    confidence_intervals: Dict[str, Tuple[float, float]]
    risk_category: str
    cost_components: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'total_financial_impact': float(self.total_financial_impact),
            'expected_fines': float(self.expected_fines),
            'business_disruption_cost': float(self.business_disruption_cost),
            'other_costs': float(self.other_costs),
            'impact_range': tuple(float(x) for x in self.impact_range),
            'confidence_intervals': {
                k: tuple(float(x) for x in v)
                for k, v in self.confidence_intervals.items()
            },
            'risk_category': self.risk_category,
            'cost_components': {k: float(v) for k, v in self.cost_components.items()}
        }


class PotentialFineCalculator:
    """
    Calculator for potential regulatory fines with probabilistic estimation.
    
    Uses historical data and regulatory guidelines to estimate fine amounts
    with uncertainty quantification.
    """
    
    # Base fine amounts by category (can be customized by jurisdiction)
    BASE_FINES = {
        FineCategory.ADMINISTRATIVE: (5000, 100000),
        FineCategory.CIVIL: (10000, 500000),
        FineCategory.CRIMINAL: (50000, 5000000),
        FineCategory.STATUTORY: (1000, 250000)
    }
    
    def __init__(self,
                 jurisdiction: str = "federal",
                 random_state: Optional[int] = None):
        """
        Initialize potential fine calculator.
        
        Args:
            jurisdiction: Regulatory jurisdiction
            random_state: Random seed for reproducibility
        """
        self.jurisdiction = jurisdiction
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_fine(self,
                     fine_category: FineCategory,
                     violation_severity: float,
                     revenue_factor: Optional[float] = None,
                     historical_fines: Optional[List[float]] = None,
                     n_simulations: int = 10000) -> FineEstimate:
        """
        Estimate potential fine amount.
        
        Args:
            fine_category: Category of fine
            violation_severity: Severity score (0-1)
            revenue_factor: Optional revenue-based multiplier
            historical_fines: Optional historical fine data for calibration
            n_simulations: Number of Monte Carlo simulations
            
        Returns:
            FineEstimate with probabilistic estimate
        """
        # Get base range for category
        base_min, base_max = self.BASE_FINES[fine_category]
        
        # Adjust based on severity
        severity_adjusted_min = base_min * (0.5 + 0.5 * violation_severity)
        severity_adjusted_max = base_max * violation_severity
        
        # Revenue-based adjustment if provided
        if revenue_factor is not None:
            severity_adjusted_min *= revenue_factor
            severity_adjusted_max *= revenue_factor
        
        # Fit distribution from historical data if available
        if historical_fines and len(historical_fines) > 5:
            # Use log-normal distribution fitted to historical data
            log_fines = np.log(historical_fines)
            mu = np.mean(log_fines)
            sigma = np.std(log_fines)
            
            # Sample from fitted distribution
            samples = self.rng.lognormal(mu, sigma, size=n_simulations)
        else:
            # Use triangular distribution (conservative estimate)
            mode = (severity_adjusted_min + severity_adjusted_max) / 2
            samples = self.rng.triangular(
                severity_adjusted_min,
                mode,
                severity_adjusted_max,
                size=n_simulations
            )
        
        # Calculate statistics
        expected_fine = float(np.mean(samples))
        fine_range = (float(np.percentile(samples, 5)), float(np.percentile(samples, 95)))
        
        # Breakdown
        breakdown = {
            'base_fine': float((base_min + base_max) / 2),
            'severity_adjustment': float(expected_fine - (base_min + base_max) / 2),
            'revenue_adjustment': float(expected_fine * (revenue_factor - 1)) if revenue_factor else 0.0
        }
        
        return FineEstimate(
            expected_fine=expected_fine,
            fine_range=fine_range,
            probability_distribution='lognormal' if historical_fines else 'triangular',
            confidence_level=0.90,
            fine_category=fine_category.value,
            jurisdiction=self.jurisdiction,
            breakdown=breakdown
        )
    
    def estimate_multiple_violations(self,
                                    violations: List[Dict[str, Any]],
                                    correlation: float = 0.3) -> Dict[str, Any]:
        """
        Estimate total fines for multiple violations.
        
        Args:
            violations: List of violation specifications
            correlation: Correlation between violation fines
            
        Returns:
            Dictionary with total fine estimates
        """
        individual_estimates = []
        
        for violation in violations:
            category = violation.get('category', FineCategory.ADMINISTRATIVE)
            severity = violation.get('severity', 0.5)
            revenue_factor = violation.get('revenue_factor')
            
            estimate = self.estimate_fine(
                fine_category=category,
                violation_severity=severity,
                revenue_factor=revenue_factor
            )
            individual_estimates.append(estimate)
        
        # Simple aggregation (could be enhanced with copulas for correlation)
        total_expected = sum(e.expected_fine for e in individual_estimates)
        
        # Adjust range for correlation
        total_min = sum(e.fine_range[0] for e in individual_estimates)
        total_max = sum(e.fine_range[1] for e in individual_estimates)
        
        # Account for correlation (reduces total variance)
        range_adjustment = 1 - (0.2 * correlation)
        adjusted_range = (
            total_expected - (total_expected - total_min) * range_adjustment,
            total_expected + (total_max - total_expected) * range_adjustment
        )
        
        return {
            'total_expected_fine': float(total_expected),
            'total_fine_range': tuple(float(x) for x in adjusted_range),
            'number_of_violations': len(violations),
            'individual_estimates': [e.to_dict() for e in individual_estimates],
            'correlation_factor': float(correlation)
        }


class BusinessDisruptionModel:
    """
    Model for business disruption costs from regulatory issues.
    
    Estimates costs from revenue loss, operational disruption, and
    reputational damage.
    """
    
    # Disruption severity multipliers
    SEVERITY_MULTIPLIERS = {
        DisruptionSeverity.MINIMAL: 0.01,
        DisruptionSeverity.MODERATE: 0.05,
        DisruptionSeverity.SIGNIFICANT: 0.15,
        DisruptionSeverity.SEVERE: 0.30,
        DisruptionSeverity.CATASTROPHIC: 0.60
    }
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize business disruption model"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_disruption_cost(self,
                                annual_revenue: float,
                                disruption_severity: DisruptionSeverity,
                                disruption_duration_days: float,
                                operational_cost_per_day: Optional[float] = None,
                                reputation_impact_factor: float = 0.1) -> DisruptionCost:
        """
        Estimate business disruption costs.
        
        Args:
            annual_revenue: Annual revenue
            disruption_severity: Severity of disruption
            disruption_duration_days: Duration in days
            operational_cost_per_day: Daily operational costs
            reputation_impact_factor: Reputational damage factor (0-1)
            
        Returns:
            DisruptionCost with detailed breakdown
        """
        # Revenue impact
        daily_revenue = annual_revenue / 365
        severity_multiplier = self.SEVERITY_MULTIPLIERS[disruption_severity]
        revenue_impact = daily_revenue * disruption_duration_days * severity_multiplier
        
        # Operational cost impact
        if operational_cost_per_day is None:
            # Estimate as 30% of daily revenue
            operational_cost_per_day = daily_revenue * 0.30
        
        # Additional operational costs during disruption (e.g., overtime, consultants)
        disruption_operational_cost = operational_cost_per_day * disruption_duration_days * severity_multiplier * 0.5
        
        # Reputation cost (long-term impact)
        reputation_cost = annual_revenue * reputation_impact_factor * severity_multiplier
        
        # Total cost
        total_cost = revenue_impact + disruption_operational_cost + reputation_cost
        
        # Breakdown
        cost_breakdown = {
            'revenue_loss': float(revenue_impact),
            'operational_disruption': float(disruption_operational_cost),
            'reputation_damage': float(reputation_cost),
            'total': float(total_cost)
        }
        
        return DisruptionCost(
            total_cost=total_cost,
            cost_breakdown=cost_breakdown,
            disruption_severity=disruption_severity.value,
            duration_days=disruption_duration_days,
            revenue_impact=revenue_impact,
            operational_cost=disruption_operational_cost,
            reputation_cost=reputation_cost
        )
    
    def estimate_market_impact(self,
                              market_cap: float,
                              stock_price_impact_pct: float) -> float:
        """
        Estimate market capitalization impact.
        
        Args:
            market_cap: Current market capitalization
            stock_price_impact_pct: Expected stock price impact (%)
            
        Returns:
            Estimated market cap loss
        """
        return market_cap * (stock_price_impact_pct / 100)
    
    def estimate_customer_churn_cost(self,
                                    annual_revenue_per_customer: float,
                                    num_customers: int,
                                    churn_rate: float,
                                    customer_lifetime_years: float = 5.0) -> float:
        """
        Estimate cost of customer churn due to regulatory issues.
        
        Args:
            annual_revenue_per_customer: Revenue per customer per year
            num_customers: Number of customers
            churn_rate: Expected churn rate (0-1)
            customer_lifetime_years: Customer lifetime value horizon
            
        Returns:
            Estimated customer churn cost
        """
        customers_lost = num_customers * churn_rate
        lifetime_value_per_customer = annual_revenue_per_customer * customer_lifetime_years
        total_churn_cost = customers_lost * lifetime_value_per_customer
        
        return float(total_churn_cost)


class FinancialImpactAggregator:
    """
    Aggregates all financial impacts from regulatory violations.
    
    Combines fines, disruption costs, and other impacts with
    Monte Carlo simulation for uncertainty quantification.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize financial impact aggregator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        self.fine_calculator = PotentialFineCalculator(random_state=random_state)
        self.disruption_model = BusinessDisruptionModel(random_state=random_state)
    
    def calculate_total_impact(self,
                              fine_estimates: List[FineEstimate],
                              disruption_costs: List[DisruptionCost],
                              other_costs: Optional[Dict[str, float]] = None,
                              n_simulations: int = 10000) -> FinancialImpactResult:
        """
        Calculate total financial impact with uncertainty.
        
        Args:
            fine_estimates: List of fine estimates
            disruption_costs: List of disruption cost estimates
            other_costs: Optional dictionary of other costs
            n_simulations: Number of Monte Carlo simulations
            
        Returns:
            FinancialImpactResult with comprehensive impact assessment
        """
        # Monte Carlo simulation
        total_samples = np.zeros(n_simulations)
        
        # Sample fines
        fine_samples = np.zeros(n_simulations)
        for fine in fine_estimates:
            # Sample from fine range using triangular distribution
            samples = self.rng.triangular(
                fine.fine_range[0],
                fine.expected_fine,
                fine.fine_range[1],
                size=n_simulations
            )
            fine_samples += samples
        
        total_samples += fine_samples
        
        # Add disruption costs (treated as more certain)
        disruption_total = sum(d.total_cost for d in disruption_costs)
        # Add some uncertainty around disruption costs (±20%)
        disruption_samples = self.rng.normal(
            disruption_total,
            disruption_total * 0.2,
            size=n_simulations
        )
        total_samples += disruption_samples
        
        # Add other costs
        other_costs_total = sum(other_costs.values()) if other_costs else 0
        total_samples += other_costs_total
        
        # Calculate statistics
        total_financial_impact = float(np.mean(total_samples))
        expected_fines = float(np.mean(fine_samples))
        business_disruption_cost = disruption_total
        
        # Confidence intervals
        confidence_intervals = {
            '68%': (float(np.percentile(total_samples, 16)), float(np.percentile(total_samples, 84))),
            '90%': (float(np.percentile(total_samples, 5)), float(np.percentile(total_samples, 95))),
            '95%': (float(np.percentile(total_samples, 2.5)), float(np.percentile(total_samples, 97.5)))
        }
        
        impact_range = confidence_intervals['90%']
        
        # Risk category based on total impact
        if total_financial_impact < 100000:
            risk_category = "LOW"
        elif total_financial_impact < 1000000:
            risk_category = "MEDIUM"
        elif total_financial_impact < 10000000:
            risk_category = "HIGH"
        else:
            risk_category = "CRITICAL"
        
        # Cost components
        cost_components = {
            'fines': expected_fines,
            'business_disruption': business_disruption_cost,
            'other_costs': other_costs_total
        }
        
        if other_costs:
            cost_components.update(other_costs)
        
        return FinancialImpactResult(
            total_financial_impact=total_financial_impact,
            expected_fines=expected_fines,
            business_disruption_cost=business_disruption_cost,
            other_costs=other_costs_total,
            impact_range=impact_range,
            confidence_intervals=confidence_intervals,
            risk_category=risk_category,
            cost_components=cost_components
        )
    
    def sensitivity_analysis(self,
                            base_impact: FinancialImpactResult,
                            parameter_variations: Dict[str, float]) -> Dict[str, float]:
        """
        Perform sensitivity analysis on financial impact.
        
        Args:
            base_impact: Base financial impact result
            parameter_variations: Dictionary of parameter variation percentages
            
        Returns:
            Dictionary of sensitivity indices
        """
        sensitivity_indices = {}
        
        for param, variation_pct in parameter_variations.items():
            # Simple sensitivity: impact change / parameter change
            variation_factor = 1 + (variation_pct / 100)
            
            # Estimate impact change (simplified)
            if 'fine' in param.lower():
                impact_change = base_impact.expected_fines * (variation_factor - 1)
            elif 'disruption' in param.lower():
                impact_change = base_impact.business_disruption_cost * (variation_factor - 1)
            else:
                impact_change = base_impact.other_costs * (variation_factor - 1)
            
            # Sensitivity index
            sensitivity = impact_change / base_impact.total_financial_impact
            sensitivity_indices[param] = float(sensitivity)
        
        return sensitivity_indices
