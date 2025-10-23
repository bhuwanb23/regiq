"""
Penalty Calculator Models

This module implements models for calculating regulatory penalties and fines
based on violation characteristics, jurisdiction, and regulatory frameworks.

Models:
- BasePenaltyCalculator: Base class for penalty calculations
- TieredPenaltyCalculator: Multi-tier penalty structure
- ProportionalPenaltyCalculator: Revenue/transaction-based penalties
- DailyPenaltyCalculator: Per-diem penalties for ongoing violations
- PenaltyAggregator: Combined penalty estimation with uncertainty
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats


class PenaltyTier(Enum):
    """Penalty tier levels"""
    TIER_1 = "tier_1"  # Minor violations
    TIER_2 = "tier_2"  # Moderate violations
    TIER_3 = "tier_3"  # Serious violations
    TIER_4 = "tier_4"  # Severe violations
    TIER_5 = "tier_5"  # Critical violations


class PenaltyType(Enum):
    """Types of penalties"""
    FIXED = "fixed"
    TIERED = "tiered"
    PROPORTIONAL = "proportional"
    DAILY = "daily"
    HYBRID = "hybrid"


@dataclass
class PenaltyResult:
    """Result container for penalty calculations"""
    base_penalty: float
    adjusted_penalty: float
    penalty_range: Tuple[float, float]
    penalty_breakdown: Dict[str, float]
    aggravating_factors: List[str]
    mitigating_factors: List[str]
    confidence_level: float
    jurisdiction: str
    penalty_type: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        # Convert penalty breakdown values carefully (can be strings or numbers)
        breakdown_dict = {}
        for k, v in self.penalty_breakdown.items():
            if isinstance(v, (int, float, np.integer, np.floating)):
                breakdown_dict[k] = float(v)
            else:
                breakdown_dict[k] = v  # Keep strings as is
        
        return {
            'base_penalty': float(self.base_penalty),
            'adjusted_penalty': float(self.adjusted_penalty),
            'penalty_range': tuple(float(x) for x in self.penalty_range),
            'penalty_breakdown': breakdown_dict,
            'aggravating_factors': self.aggravating_factors,
            'mitigating_factors': self.mitigating_factors,
            'confidence_level': float(self.confidence_level),
            'jurisdiction': self.jurisdiction,
            'penalty_type': self.penalty_type
        }


class BasePenaltyCalculator:
    """
    Base class for penalty calculations.
    
    Provides common functionality for all penalty calculator types.
    """
    
    def __init__(self,
                 jurisdiction: str = "federal",
                 random_state: Optional[int] = None):
        """
        Initialize penalty calculator.
        
        Args:
            jurisdiction: Regulatory jurisdiction
            random_state: Random seed for reproducibility
        """
        self.jurisdiction = jurisdiction
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def apply_adjustments(self,
                         base_penalty: float,
                         aggravating_factors: Optional[Dict[str, float]] = None,
                         mitigating_factors: Optional[Dict[str, float]] = None) -> Tuple[float, List[str], List[str]]:
        """
        Apply aggravating and mitigating factors to base penalty.
        
        Args:
            base_penalty: Base penalty amount
            aggravating_factors: Dictionary of aggravating factors and multipliers
            mitigating_factors: Dictionary of mitigating factors and reductions
            
        Returns:
            Tuple of (adjusted penalty, aggravating list, mitigating list)
        """
        aggravating_list = []
        mitigating_list = []
        adjusted_penalty = base_penalty
        
        # Apply aggravating factors (multiplicative)
        if aggravating_factors:
            for factor, multiplier in aggravating_factors.items():
                if multiplier > 1.0:
                    adjusted_penalty *= multiplier
                    aggravating_list.append(factor)
        
        # Apply mitigating factors (reductive)
        if mitigating_factors:
            for factor, reduction in mitigating_factors.items():
                if 0 < reduction < 1.0:
                    adjusted_penalty *= reduction
                    mitigating_list.append(factor)
        
        return adjusted_penalty, aggravating_list, mitigating_list
    
    def calculate_uncertainty_range(self,
                                   penalty: float,
                                   uncertainty_pct: float = 0.20) -> Tuple[float, float]:
        """
        Calculate uncertainty range around penalty estimate.
        
        Args:
            penalty: Estimated penalty amount
            uncertainty_pct: Uncertainty percentage (default 20%)
            
        Returns:
            Tuple of (lower bound, upper bound)
        """
        lower = penalty * (1 - uncertainty_pct)
        upper = penalty * (1 + uncertainty_pct)
        return (lower, upper)


class TieredPenaltyCalculator(BasePenaltyCalculator):
    """
    Calculator for tiered penalty structures.
    
    Implements multi-tier penalty frameworks common in regulatory systems.
    """
    
    # Default tier structure (can be customized)
    DEFAULT_TIERS = {
        PenaltyTier.TIER_1: (0, 10000),
        PenaltyTier.TIER_2: (10000, 50000),
        PenaltyTier.TIER_3: (50000, 250000),
        PenaltyTier.TIER_4: (250000, 1000000),
        PenaltyTier.TIER_5: (1000000, 5000000)
    }
    
    def __init__(self,
                 tier_structure: Optional[Dict[PenaltyTier, Tuple[float, float]]] = None,
                 jurisdiction: str = "federal",
                 random_state: Optional[int] = None):
        """
        Initialize tiered penalty calculator.
        
        Args:
            tier_structure: Custom tier structure (min, max) per tier
            jurisdiction: Regulatory jurisdiction
            random_state: Random seed
        """
        super().__init__(jurisdiction, random_state)
        self.tier_structure = tier_structure or self.DEFAULT_TIERS
    
    def determine_tier(self,
                      violation_score: float,
                      violation_count: int = 1) -> PenaltyTier:
        """
        Determine penalty tier based on violation characteristics.
        
        Args:
            violation_score: Violation severity score (0-1)
            violation_count: Number of violations
            
        Returns:
            Appropriate PenaltyTier
        """
        # Adjust score by violation count
        adjusted_score = min(1.0, violation_score * (1 + 0.1 * (violation_count - 1)))
        
        if adjusted_score >= 0.9:
            return PenaltyTier.TIER_5
        elif adjusted_score >= 0.7:
            return PenaltyTier.TIER_4
        elif adjusted_score >= 0.5:
            return PenaltyTier.TIER_3
        elif adjusted_score >= 0.3:
            return PenaltyTier.TIER_2
        else:
            return PenaltyTier.TIER_1
    
    def calculate(self,
                 violation_score: float,
                 violation_count: int = 1,
                 aggravating_factors: Optional[Dict[str, float]] = None,
                 mitigating_factors: Optional[Dict[str, float]] = None) -> PenaltyResult:
        """
        Calculate tiered penalty.
        
        Args:
            violation_score: Violation severity score (0-1)
            violation_count: Number of violations
            aggravating_factors: Aggravating factor multipliers
            mitigating_factors: Mitigating factor reductions
            
        Returns:
            PenaltyResult with calculated penalty
        """
        # Determine tier
        tier = self.determine_tier(violation_score, violation_count)
        tier_min, tier_max = self.tier_structure[tier]
        
        # Base penalty (within tier range, scaled by score)
        tier_range = tier_max - tier_min
        base_penalty = tier_min + (tier_range * violation_score)
        
        # Apply adjustments
        adjusted_penalty, agg_list, mit_list = self.apply_adjustments(
            base_penalty,
            aggravating_factors,
            mitigating_factors
        )
        
        # Calculate uncertainty range
        penalty_range = self.calculate_uncertainty_range(adjusted_penalty)
        
        # Breakdown
        breakdown = {
            'tier': tier.value,
            'tier_min': tier_min,
            'tier_max': tier_max,
            'base_penalty': base_penalty,
            'adjusted_penalty': adjusted_penalty
        }
        
        return PenaltyResult(
            base_penalty=base_penalty,
            adjusted_penalty=adjusted_penalty,
            penalty_range=penalty_range,
            penalty_breakdown=breakdown,
            aggravating_factors=agg_list,
            mitigating_factors=mit_list,
            confidence_level=0.80,
            jurisdiction=self.jurisdiction,
            penalty_type=PenaltyType.TIERED.value
        )


class ProportionalPenaltyCalculator(BasePenaltyCalculator):
    """
    Calculator for proportional (revenue/transaction-based) penalties.
    
    Common for GDPR, antitrust, and financial regulations.
    """
    
    def __init__(self,
                 max_revenue_percentage: float = 0.04,
                 min_fixed_amount: float = 10000,
                 jurisdiction: str = "federal",
                 random_state: Optional[int] = None):
        """
        Initialize proportional penalty calculator.
        
        Args:
            max_revenue_percentage: Maximum penalty as % of revenue (e.g., 0.04 for 4%)
            min_fixed_amount: Minimum fixed penalty amount
            jurisdiction: Regulatory jurisdiction
            random_state: Random seed
        """
        super().__init__(jurisdiction, random_state)
        self.max_revenue_percentage = max_revenue_percentage
        self.min_fixed_amount = min_fixed_amount
    
    def calculate(self,
                 annual_revenue: float,
                 violation_severity: float,
                 affected_transactions: Optional[int] = None,
                 transaction_value: Optional[float] = None,
                 aggravating_factors: Optional[Dict[str, float]] = None,
                 mitigating_factors: Optional[Dict[str, float]] = None) -> PenaltyResult:
        """
        Calculate proportional penalty.
        
        Args:
            annual_revenue: Annual revenue of organization
            violation_severity: Severity score (0-1)
            affected_transactions: Number of affected transactions
            transaction_value: Average transaction value
            aggravating_factors: Aggravating factor multipliers
            mitigating_factors: Mitigating factor reductions
            
        Returns:
            PenaltyResult with calculated penalty
        """
        # Revenue-based penalty
        revenue_penalty = annual_revenue * self.max_revenue_percentage * violation_severity
        
        # Transaction-based penalty (if applicable)
        transaction_penalty = 0
        if affected_transactions and transaction_value:
            transaction_penalty = affected_transactions * transaction_value * 0.05  # 5% of transaction value
        
        # Base penalty is higher of revenue-based or transaction-based
        base_penalty = max(revenue_penalty, transaction_penalty, self.min_fixed_amount)
        
        # Apply adjustments
        adjusted_penalty, agg_list, mit_list = self.apply_adjustments(
            base_penalty,
            aggravating_factors,
            mitigating_factors
        )
        
        # Calculate uncertainty range
        penalty_range = self.calculate_uncertainty_range(adjusted_penalty, uncertainty_pct=0.25)
        
        # Breakdown
        breakdown = {
            'revenue_penalty': revenue_penalty,
            'transaction_penalty': transaction_penalty,
            'min_fixed_amount': self.min_fixed_amount,
            'base_penalty': base_penalty,
            'adjusted_penalty': adjusted_penalty
        }
        
        return PenaltyResult(
            base_penalty=base_penalty,
            adjusted_penalty=adjusted_penalty,
            penalty_range=penalty_range,
            penalty_breakdown=breakdown,
            aggravating_factors=agg_list,
            mitigating_factors=mit_list,
            confidence_level=0.75,
            jurisdiction=self.jurisdiction,
            penalty_type=PenaltyType.PROPORTIONAL.value
        )


class DailyPenaltyCalculator(BasePenaltyCalculator):
    """
    Calculator for daily (per diem) penalties for ongoing violations.
    
    Common for environmental, safety, and operational violations.
    """
    
    def __init__(self,
                 daily_rate: float = 1000,
                 max_total_penalty: Optional[float] = None,
                 jurisdiction: str = "federal",
                 random_state: Optional[int] = None):
        """
        Initialize daily penalty calculator.
        
        Args:
            daily_rate: Base daily penalty rate
            max_total_penalty: Maximum total penalty (if capped)
            jurisdiction: Regulatory jurisdiction
            random_state: Random seed
        """
        super().__init__(jurisdiction, random_state)
        self.daily_rate = daily_rate
        self.max_total_penalty = max_total_penalty
    
    def calculate(self,
                 violation_days: int,
                 severity_multiplier: float = 1.0,
                 aggravating_factors: Optional[Dict[str, float]] = None,
                 mitigating_factors: Optional[Dict[str, float]] = None) -> PenaltyResult:
        """
        Calculate daily penalty.
        
        Args:
            violation_days: Number of days in violation
            severity_multiplier: Multiplier based on severity
            aggravating_factors: Aggravating factor multipliers
            mitigating_factors: Mitigating factor reductions
            
        Returns:
            PenaltyResult with calculated penalty
        """
        # Base daily penalty
        base_penalty = self.daily_rate * violation_days * severity_multiplier
        
        # Apply cap if exists
        if self.max_total_penalty:
            base_penalty = min(base_penalty, self.max_total_penalty)
        
        # Apply adjustments
        adjusted_penalty, agg_list, mit_list = self.apply_adjustments(
            base_penalty,
            aggravating_factors,
            mitigating_factors
        )
        
        # Apply cap again after adjustments
        if self.max_total_penalty:
            adjusted_penalty = min(adjusted_penalty, self.max_total_penalty)
        
        # Calculate uncertainty range
        penalty_range = self.calculate_uncertainty_range(adjusted_penalty, uncertainty_pct=0.15)
        
        # Breakdown
        breakdown = {
            'daily_rate': self.daily_rate,
            'violation_days': violation_days,
            'severity_multiplier': severity_multiplier,
            'base_penalty': base_penalty,
            'adjusted_penalty': adjusted_penalty,
            'capped': bool(self.max_total_penalty and adjusted_penalty >= self.max_total_penalty)
        }
        
        return PenaltyResult(
            base_penalty=base_penalty,
            adjusted_penalty=adjusted_penalty,
            penalty_range=penalty_range,
            penalty_breakdown=breakdown,
            aggravating_factors=agg_list,
            mitigating_factors=mit_list,
            confidence_level=0.85,
            jurisdiction=self.jurisdiction,
            penalty_type=PenaltyType.DAILY.value
        )


class PenaltyAggregator:
    """
    Aggregates penalties from multiple sources with uncertainty quantification.
    
    Combines different penalty types and provides Monte Carlo simulation
    for total penalty estimation.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize penalty aggregator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        self.penalties: List[PenaltyResult] = []
    
    def add_penalty(self, penalty_result: PenaltyResult):
        """
        Add a penalty result to the aggregator.
        
        Args:
            penalty_result: PenaltyResult to add
        """
        self.penalties.append(penalty_result)
    
    def calculate_total(self,
                       n_simulations: int = 10000,
                       correlation: float = 0.3) -> Dict[str, Any]:
        """
        Calculate total penalty with uncertainty.
        
        Args:
            n_simulations: Number of Monte Carlo simulations
            correlation: Correlation between penalty components
            
        Returns:
            Dictionary with total penalty statistics
        """
        if not self.penalties:
            raise ValueError("No penalties added to aggregator")
        
        # Monte Carlo simulation
        total_samples = np.zeros(n_simulations)
        
        for penalty in self.penalties:
            # Sample from penalty range (triangular distribution)
            lower, upper = penalty.penalty_range
            mode = penalty.adjusted_penalty
            
            samples = self.rng.triangular(lower, mode, upper, size=n_simulations)
            total_samples += samples
        
        # Calculate statistics
        mean_total = np.mean(total_samples)
        median_total = np.median(total_samples)
        std_total = np.std(total_samples)
        
        # Confidence intervals
        ci_90 = np.percentile(total_samples, [5, 95])
        ci_95 = np.percentile(total_samples, [2.5, 97.5])
        ci_99 = np.percentile(total_samples, [0.5, 99.5])
        
        # Breakdown by penalty type
        breakdown = {}
        for penalty in self.penalties:
            penalty_type = penalty.penalty_type
            if penalty_type not in breakdown:
                breakdown[penalty_type] = 0
            breakdown[penalty_type] += penalty.adjusted_penalty
        
        return {
            'mean_total': float(mean_total),
            'median_total': float(median_total),
            'std_total': float(std_total),
            'confidence_interval_90': tuple(float(x) for x in ci_90),
            'confidence_interval_95': tuple(float(x) for x in ci_95),
            'confidence_interval_99': tuple(float(x) for x in ci_99),
            'min_possible': float(np.min(total_samples)),
            'max_possible': float(np.max(total_samples)),
            'breakdown_by_type': {k: float(v) for k, v in breakdown.items()},
            'n_components': len(self.penalties),
            'n_simulations': n_simulations
        }
    
    def get_percentile_estimate(self, percentile: float = 95) -> float:
        """
        Get penalty estimate at specific percentile.
        
        Args:
            percentile: Percentile level (0-100)
            
        Returns:
            Penalty amount at specified percentile
        """
        if not self.penalties:
            raise ValueError("No penalties added to aggregator")
        
        # Simple approach: sum of adjusted penalties at percentile
        total = sum(p.adjusted_penalty for p in self.penalties)
        
        # Adjust for uncertainty (wider range at higher percentiles)
        if percentile >= 95:
            multiplier = 1.3
        elif percentile >= 90:
            multiplier = 1.2
        elif percentile >= 75:
            multiplier = 1.1
        else:
            multiplier = 1.0
        
        return total * multiplier
    
    def export_results(self) -> Dict[str, Any]:
        """
        Export all penalty results.
        
        Returns:
            Dictionary with all penalty details
        """
        return {
            'penalties': [p.to_dict() for p in self.penalties],
            'summary': self.calculate_total() if self.penalties else {}
        }
