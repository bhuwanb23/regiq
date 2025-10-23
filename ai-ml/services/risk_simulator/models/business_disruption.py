"""
Business Disruption Models

This module implements advanced models for quantifying business disruption
from regulatory compliance issues, including operational impacts, supply chain
disruptions, and market consequences.

Models:
- OperationalDisruptionModel: Quantify operational capacity loss
- SupplyChainImpactModel: Model supply chain disruptions
- MarketConsequenceModel: Estimate market and competitive impacts
- IntegratedDisruptionAnalyzer: Comprehensive disruption analysis
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats


class OperationalPhase(Enum):
    """Operational phases affected"""
    PRODUCTION = "production"
    DISTRIBUTION = "distribution"
    SALES = "sales"
    SUPPORT = "support"
    RND = "research_development"


class SupplyChainTier(Enum):
    """Supply chain tier levels"""
    TIER_1 = "tier_1"  # Direct suppliers
    TIER_2 = "tier_2"  # Secondary suppliers
    TIER_3 = "tier_3"  # Tertiary suppliers


@dataclass
class OperationalImpact:
    """Result container for operational disruption"""
    capacity_loss_pct: float
    affected_operations: List[str]
    productivity_impact: float
    recovery_time_days: float
    total_cost: float
    cost_breakdown: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'capacity_loss_pct': float(self.capacity_loss_pct),
            'affected_operations': self.affected_operations,
            'productivity_impact': float(self.productivity_impact),
            'recovery_time_days': float(self.recovery_time_days),
            'total_cost': float(self.total_cost),
            'cost_breakdown': {k: float(v) for k, v in self.cost_breakdown.items()}
        }


@dataclass
class SupplyChainImpact:
    """Result container for supply chain disruption"""
    disrupted_suppliers: int
    alternative_sourcing_cost: float
    delay_cost: float
    inventory_impact: float
    total_cost: float
    recovery_strategy: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'disrupted_suppliers': int(self.disrupted_suppliers),
            'alternative_sourcing_cost': float(self.alternative_sourcing_cost),
            'delay_cost': float(self.delay_cost),
            'inventory_impact': float(self.inventory_impact),
            'total_cost': float(self.total_cost),
            'recovery_strategy': self.recovery_strategy
        }


@dataclass
class MarketImpact:
    """Result container for market consequences"""
    market_share_loss_pct: float
    competitive_disadvantage: float
    customer_acquisition_cost_increase: float
    brand_value_loss: float
    total_market_impact: float
    recovery_likelihood: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'market_share_loss_pct': float(self.market_share_loss_pct),
            'competitive_disadvantage': float(self.competitive_disadvantage),
            'customer_acquisition_cost_increase': float(self.customer_acquisition_cost_increase),
            'brand_value_loss': float(self.brand_value_loss),
            'total_market_impact': float(self.total_market_impact),
            'recovery_likelihood': float(self.recovery_likelihood)
        }


class OperationalDisruptionModel:
    """
    Model for operational capacity loss and productivity impact.
    
    Quantifies impact on different operational phases and estimates
    recovery time and costs.
    """
    
    # Productivity loss factors by phase
    PHASE_CRITICALITY = {
        OperationalPhase.PRODUCTION: 1.0,
        OperationalPhase.DISTRIBUTION: 0.7,
        OperationalPhase.SALES: 0.8,
        OperationalPhase.SUPPORT: 0.5,
        OperationalPhase.RND: 0.6
    }
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize operational disruption model"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_disruption(self,
                          affected_phases: List[OperationalPhase],
                          disruption_severity: float,
                          annual_revenue: float,
                          annual_operational_cost: float,
                          baseline_capacity: float = 1.0) -> OperationalImpact:
        """
        Estimate operational disruption impact.
        
        Args:
            affected_phases: List of affected operational phases
            disruption_severity: Severity score (0-1)
            annual_revenue: Annual revenue
            annual_operational_cost: Annual operational costs
            baseline_capacity: Baseline capacity utilization (0-1)
            
        Returns:
            OperationalImpact with detailed analysis
        """
        # Calculate weighted capacity loss
        total_criticality = sum(
            self.PHASE_CRITICALITY[phase] for phase in affected_phases
        )
        max_criticality = sum(self.PHASE_CRITICALITY.values())
        
        capacity_loss_pct = (total_criticality / max_criticality) * disruption_severity * 100
        
        # Productivity impact (exponential relationship with capacity loss)
        productivity_impact = 1 - np.exp(-capacity_loss_pct / 30)
        
        # Recovery time estimation (days)
        # More severe disruptions take longer to recover
        base_recovery_days = 30
        recovery_time_days = base_recovery_days * (1 + disruption_severity * 2)
        
        # Cost calculations
        daily_revenue = annual_revenue / 365
        daily_op_cost = annual_operational_cost / 365
        
        # Lost revenue during disruption
        revenue_loss = daily_revenue * recovery_time_days * (capacity_loss_pct / 100)
        
        # Additional operational costs (inefficiencies, overtime, etc.)
        additional_op_cost = daily_op_cost * recovery_time_days * productivity_impact * 0.3
        
        # Recovery/remediation costs
        recovery_cost = annual_operational_cost * 0.05 * disruption_severity
        
        total_cost = revenue_loss + additional_op_cost + recovery_cost
        
        cost_breakdown = {
            'revenue_loss': float(revenue_loss),
            'additional_operational_cost': float(additional_op_cost),
            'recovery_cost': float(recovery_cost)
        }
        
        return OperationalImpact(
            capacity_loss_pct=capacity_loss_pct,
            affected_operations=[phase.value for phase in affected_phases],
            productivity_impact=productivity_impact,
            recovery_time_days=recovery_time_days,
            total_cost=total_cost,
            cost_breakdown=cost_breakdown
        )
    
    def estimate_cascading_effects(self,
                                  initial_phases: List[OperationalPhase],
                                  propagation_probability: float = 0.3) -> List[OperationalPhase]:
        """
        Estimate cascading effects across operational phases.
        
        Args:
            initial_phases: Initially affected phases
            propagation_probability: Probability of disruption propagating
            
        Returns:
            List of all affected phases including cascading effects
        """
        all_phases = set(initial_phases)
        
        # Define phase dependencies
        dependencies = {
            OperationalPhase.PRODUCTION: [OperationalPhase.DISTRIBUTION],
            OperationalPhase.DISTRIBUTION: [OperationalPhase.SALES],
            OperationalPhase.SALES: [OperationalPhase.SUPPORT],
            OperationalPhase.RND: [OperationalPhase.PRODUCTION]
        }
        
        # Propagate disruption
        for phase in initial_phases:
            if phase in dependencies:
                for dependent_phase in dependencies[phase]:
                    if self.rng.random() < propagation_probability:
                        all_phases.add(dependent_phase)
        
        return list(all_phases)


class SupplyChainImpactModel:
    """
    Model for supply chain disruption impacts.
    
    Estimates costs from supplier disruptions, alternative sourcing,
    and inventory impacts.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize supply chain impact model"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_supplier_disruption(self,
                                    total_suppliers: int,
                                    disruption_probability: float,
                                    annual_supplier_spend: float,
                                    alternative_cost_premium: float = 0.25,
                                    delay_days: float = 30) -> SupplyChainImpact:
        """
        Estimate supply chain disruption impact.
        
        Args:
            total_suppliers: Total number of suppliers
            disruption_probability: Probability each supplier is disrupted
            annual_supplier_spend: Annual spend with suppliers
            alternative_cost_premium: Cost premium for alternative sourcing (%)
            delay_days: Average delay in days
            
        Returns:
            SupplyChainImpact with cost analysis
        """
        # Monte Carlo simulation of supplier disruptions
        disrupted_count = int(self.rng.binomial(total_suppliers, disruption_probability))
        
        # Alternative sourcing costs
        disrupted_spend = (annual_supplier_spend / total_suppliers) * disrupted_count
        alternative_sourcing_cost = disrupted_spend * alternative_cost_premium
        
        # Delay costs (opportunity cost and expedited shipping)
        daily_revenue_impact = (annual_supplier_spend / 365) * 0.5  # 50% revenue impact
        delay_cost = daily_revenue_impact * delay_days * (disrupted_count / total_suppliers)
        
        # Inventory impact (holding costs or shortage costs)
        inventory_impact = disrupted_spend * 0.15  # 15% of disrupted spend
        
        total_cost = alternative_sourcing_cost + delay_cost + inventory_impact
        
        # Recovery strategy based on disruption level
        disruption_pct = disrupted_count / total_suppliers
        if disruption_pct < 0.2:
            recovery_strategy = "tactical_sourcing"
        elif disruption_pct < 0.5:
            recovery_strategy = "diversification"
        else:
            recovery_strategy = "strategic_restructuring"
        
        return SupplyChainImpact(
            disrupted_suppliers=disrupted_count,
            alternative_sourcing_cost=alternative_sourcing_cost,
            delay_cost=delay_cost,
            inventory_impact=inventory_impact,
            total_cost=total_cost,
            recovery_strategy=recovery_strategy
        )
    
    def estimate_tier_propagation(self,
                                 tier_1_disruption: float,
                                 propagation_factor: float = 0.6) -> Dict[str, float]:
        """
        Estimate disruption propagation across supply chain tiers.
        
        Args:
            tier_1_disruption: Tier 1 disruption level (0-1)
            propagation_factor: Propagation damping factor
            
        Returns:
            Dictionary of disruption levels by tier
        """
        tier_disruptions = {
            'tier_1': tier_1_disruption,
            'tier_2': tier_1_disruption * propagation_factor,
            'tier_3': tier_1_disruption * (propagation_factor ** 2)
        }
        
        return {k: float(v) for k, v in tier_disruptions.items()}


class MarketConsequenceModel:
    """
    Model for market and competitive consequences.
    
    Estimates market share loss, competitive positioning impact,
    and brand value effects.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize market consequence model"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def estimate_market_impact(self,
                              current_market_share: float,
                              compliance_issue_severity: float,
                              media_exposure: float,
                              competitor_strength: float,
                              customer_switching_cost: float = 0.3) -> MarketImpact:
        """
        Estimate market consequences of compliance issues.
        
        Args:
            current_market_share: Current market share (0-1)
            compliance_issue_severity: Issue severity (0-1)
            media_exposure: Media exposure level (0-1)
            competitor_strength: Competitor strength (0-1)
            customer_switching_cost: Cost for customers to switch (0-1)
            
        Returns:
            MarketImpact with detailed analysis
        """
        # Market share loss
        # Higher severity, media exposure, and competitor strength increase loss
        # Higher switching costs reduce loss
        base_loss_factor = compliance_issue_severity * media_exposure * competitor_strength
        switching_dampener = 1 - customer_switching_cost
        market_share_loss_pct = base_loss_factor * switching_dampener * 100
        
        # Competitive disadvantage (temporary market position weakness)
        competitive_disadvantage = compliance_issue_severity * (1 + media_exposure) * 0.5
        
        # Customer acquisition cost increase
        # Harder to acquire customers after compliance issues
        cac_increase_factor = 1 + (compliance_issue_severity * media_exposure * 0.5)
        customer_acquisition_cost_increase = cac_increase_factor
        
        # Brand value loss (estimated as % of revenue)
        brand_value_loss_pct = compliance_issue_severity * media_exposure * 10  # Up to 10% of revenue
        
        # Total market impact (composite metric)
        total_market_impact = (
            market_share_loss_pct * 0.4 +
            competitive_disadvantage * 100 * 0.3 +
            (cac_increase_factor - 1) * 100 * 0.15 +
            brand_value_loss_pct * 0.15
        )
        
        # Recovery likelihood
        # Depends on severity and how quickly issue is resolved
        recovery_base = 1 - compliance_issue_severity
        recovery_likelihood = recovery_base * (1 - media_exposure * 0.3)
        
        return MarketImpact(
            market_share_loss_pct=market_share_loss_pct,
            competitive_disadvantage=competitive_disadvantage,
            customer_acquisition_cost_increase=customer_acquisition_cost_increase,
            brand_value_loss=brand_value_loss_pct,
            total_market_impact=total_market_impact,
            recovery_likelihood=recovery_likelihood
        )
    
    def estimate_stock_price_impact(self,
                                   market_impact: MarketImpact,
                                   market_cap: float) -> Dict[str, float]:
        """
        Estimate stock price impact from market consequences.
        
        Args:
            market_impact: MarketImpact result
            market_cap: Current market capitalization
            
        Returns:
            Dictionary with stock price impact estimates
        """
        # Stock price typically overreacts to negative news
        overreaction_factor = 1.5
        
        # Estimated stock price drop (%)
        stock_price_drop_pct = market_impact.total_market_impact * overreaction_factor
        
        # Market cap loss
        market_cap_loss = market_cap * (stock_price_drop_pct / 100)
        
        # Recovery timeline (months)
        if market_impact.recovery_likelihood > 0.7:
            recovery_months = 6
        elif market_impact.recovery_likelihood > 0.5:
            recovery_months = 12
        elif market_impact.recovery_likelihood > 0.3:
            recovery_months = 24
        else:
            recovery_months = 36
        
        return {
            'stock_price_drop_pct': float(stock_price_drop_pct),
            'market_cap_loss': float(market_cap_loss),
            'estimated_recovery_months': int(recovery_months),
            'long_term_permanent_loss_pct': float((1 - market_impact.recovery_likelihood) * stock_price_drop_pct)
        }


class IntegratedDisruptionAnalyzer:
    """
    Comprehensive business disruption analyzer integrating all disruption models.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize integrated disruption analyzer"""
        self.random_state = random_state
        self.operational_model = OperationalDisruptionModel(random_state=random_state)
        self.supply_chain_model = SupplyChainImpactModel(random_state=random_state)
        self.market_model = MarketConsequenceModel(random_state=random_state)
    
    def analyze_total_disruption(self,
                                operational_params: Dict[str, Any],
                                supply_chain_params: Dict[str, Any],
                                market_params: Dict[str, Any],
                                annual_revenue: float) -> Dict[str, Any]:
        """
        Perform comprehensive disruption analysis.
        
        Args:
            operational_params: Parameters for operational disruption
            supply_chain_params: Parameters for supply chain disruption
            market_params: Parameters for market impact
            annual_revenue: Annual revenue for cost calculations
            
        Returns:
            Dictionary with comprehensive disruption analysis
        """
        # Operational disruption
        operational_impact = self.operational_model.estimate_disruption(**operational_params)
        
        # Supply chain disruption
        supply_chain_impact = self.supply_chain_model.estimate_supplier_disruption(**supply_chain_params)
        
        # Market consequences
        market_impact = self.market_model.estimate_market_impact(**market_params)
        
        # Calculate total disruption cost
        operational_cost = operational_impact.total_cost
        supply_chain_cost = supply_chain_impact.total_cost
        
        # Market impact in monetary terms
        market_share_revenue_loss = annual_revenue * (market_impact.market_share_loss_pct / 100)
        brand_value_loss = annual_revenue * (market_impact.brand_value_loss / 100)
        market_cost = market_share_revenue_loss + brand_value_loss
        
        total_disruption_cost = operational_cost + supply_chain_cost + market_cost
        
        # Disruption category
        if total_disruption_cost < annual_revenue * 0.01:
            disruption_category = "MINOR"
        elif total_disruption_cost < annual_revenue * 0.05:
            disruption_category = "MODERATE"
        elif total_disruption_cost < annual_revenue * 0.15:
            disruption_category = "MAJOR"
        else:
            disruption_category = "SEVERE"
        
        return {
            'total_disruption_cost': float(total_disruption_cost),
            'operational_impact': operational_impact.to_dict(),
            'supply_chain_impact': supply_chain_impact.to_dict(),
            'market_impact': market_impact.to_dict(),
            'cost_breakdown': {
                'operational': float(operational_cost),
                'supply_chain': float(supply_chain_cost),
                'market': float(market_cost)
            },
            'disruption_category': disruption_category,
            'cost_as_pct_of_revenue': float((total_disruption_cost / annual_revenue) * 100)
        }
    
    def monte_carlo_disruption(self,
                              base_params: Dict[str, Any],
                              uncertainty_ranges: Dict[str, Tuple[float, float]],
                              n_simulations: int = 10000) -> Dict[str, Any]:
        """
        Monte Carlo simulation of disruption scenarios.
        
        Args:
            base_params: Base parameters for analysis
            uncertainty_ranges: Ranges for uncertain parameters
            n_simulations: Number of simulations
            
        Returns:
            Dictionary with Monte Carlo results
        """
        rng = np.random.RandomState(self.random_state)
        
        disruption_samples = []
        
        for _ in range(n_simulations):
            # Sample parameters from uncertainty ranges
            sampled_params = base_params.copy()
            
            for param, (min_val, max_val) in uncertainty_ranges.items():
                sampled_params[param] = rng.uniform(min_val, max_val)
            
            # Run simulation (simplified - would call full analysis in practice)
            # Using simplified calculation for Monte Carlo
            sample_cost = rng.uniform(
                sampled_params.get('min_cost', 0),
                sampled_params.get('max_cost', 1000000)
            )
            disruption_samples.append(sample_cost)
        
        samples_array = np.array(disruption_samples)
        
        return {
            'mean_disruption_cost': float(np.mean(samples_array)),
            'median_disruption_cost': float(np.median(samples_array)),
            'std_disruption_cost': float(np.std(samples_array)),
            'percentile_90': float(np.percentile(samples_array, 90)),
            'percentile_95': float(np.percentile(samples_array, 95)),
            'percentile_99': float(np.percentile(samples_array, 99)),
            'confidence_interval_95': (
                float(np.percentile(samples_array, 2.5)),
                float(np.percentile(samples_array, 97.5))
            )
        }
