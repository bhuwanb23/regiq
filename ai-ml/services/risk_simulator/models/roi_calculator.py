"""
ROI Calculator for Compliance Investments

This module implements return on investment (ROI) calculations for compliance
and remediation initiatives, including NPV, IRR, payback period, and
cost-benefit analysis with risk adjustment.

Models:
- NPVCalculator: Net Present Value calculations
- IRRCalculator: Internal Rate of Return calculations
- PaybackAnalyzer: Payback period analysis
- CostBenefitAnalyzer: Comprehensive cost-benefit analysis
- RiskAdjustedROICalculator: ROI with risk adjustments
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats
from scipy.optimize import newton


class DiscountMethod(Enum):
    """Discount rate methods"""
    WACC = "weighted_average_cost_of_capital"
    HURDLE_RATE = "hurdle_rate"
    RISK_FREE_PLUS_PREMIUM = "risk_free_plus_premium"


@dataclass
class NPVResult:
    """Result container for NPV analysis"""
    npv: float
    present_value_benefits: float
    present_value_costs: float
    discount_rate: float
    time_horizon_years: int
    cash_flows_by_year: Dict[int, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'npv': float(self.npv),
            'present_value_benefits': float(self.present_value_benefits),
            'present_value_costs': float(self.present_value_costs),
            'discount_rate': float(self.discount_rate),
            'time_horizon_years': int(self.time_horizon_years),
            'cash_flows_by_year': {int(k): float(v) for k, v in self.cash_flows_by_year.items()}
        }


@dataclass
class ROIAnalysis:
    """Comprehensive ROI analysis result"""
    roi_percentage: float
    npv: float
    irr: float
    payback_period_years: float
    benefit_cost_ratio: float
    profitability_index: float
    recommendation: str
    sensitivity_analysis: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'roi_percentage': float(self.roi_percentage),
            'npv': float(self.npv),
            'irr': float(self.irr),
            'payback_period_years': float(self.payback_period_years),
            'benefit_cost_ratio': float(self.benefit_cost_ratio),
            'profitability_index': float(self.profitability_index),
            'recommendation': self.recommendation,
            'sensitivity_analysis': {k: float(v) for k, v in self.sensitivity_analysis.items()}
        }


class NPVCalculator:
    """
    Net Present Value calculator for compliance investments.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize NPV calculator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def calculate_npv(self,
                     initial_investment: float,
                     annual_benefits: List[float],
                     annual_costs: List[float],
                     discount_rate: float,
                     terminal_value: float = 0.0) -> NPVResult:
        """
        Calculate Net Present Value.
        
        Args:
            initial_investment: Initial investment (negative cash flow)
            annual_benefits: List of annual benefits
            annual_costs: List of annual costs
            discount_rate: Annual discount rate (e.g., 0.10 for 10%)
            terminal_value: Terminal value at end of period
            
        Returns:
            NPVResult with detailed NPV analysis
        """
        n_years = max(len(annual_benefits), len(annual_costs))
        
        # Pad shorter list with zeros
        if len(annual_benefits) < n_years:
            annual_benefits = annual_benefits + [0] * (n_years - len(annual_benefits))
        if len(annual_costs) < n_years:
            annual_costs = annual_costs + [0] * (n_years - len(annual_costs))
        
        # Calculate present values
        pv_benefits = 0
        pv_costs = initial_investment  # Include initial investment in costs
        cash_flows = {}
        
        for year in range(n_years):
            discount_factor = 1 / ((1 + discount_rate) ** (year + 1))
            
            pv_benefit = annual_benefits[year] * discount_factor
            pv_cost = annual_costs[year] * discount_factor
            
            pv_benefits += pv_benefit
            pv_costs += pv_cost
            
            # Net cash flow for this year
            cash_flows[year + 1] = annual_benefits[year] - annual_costs[year]
        
        # Add terminal value
        if terminal_value != 0:
            terminal_pv = terminal_value / ((1 + discount_rate) ** n_years)
            pv_benefits += terminal_pv
        
        # Initial investment as year 0
        cash_flows[0] = -initial_investment
        
        # NPV
        npv = pv_benefits - pv_costs
        
        return NPVResult(
            npv=npv,
            present_value_benefits=pv_benefits,
            present_value_costs=pv_costs,
            discount_rate=discount_rate,
            time_horizon_years=n_years,
            cash_flows_by_year=cash_flows
        )
    
    def calculate_npv_with_uncertainty(self,
                                      initial_investment: float,
                                      annual_benefits_range: List[Tuple[float, float]],
                                      annual_costs_range: List[Tuple[float, float]],
                                      discount_rate_range: Tuple[float, float],
                                      n_simulations: int = 10000) -> Dict[str, Any]:
        """
        Calculate NPV with Monte Carlo uncertainty quantification.
        
        Args:
            initial_investment: Initial investment
            annual_benefits_range: List of (min, max) for each year's benefits
            annual_costs_range: List of (min, max) for each year's costs
            discount_rate_range: (min, max) discount rate
            n_simulations: Number of Monte Carlo simulations
            
        Returns:
            Dictionary with NPV statistics
        """
        npv_samples = []
        
        for _ in range(n_simulations):
            # Sample discount rate
            discount_rate = self.rng.uniform(*discount_rate_range)
            
            # Sample annual benefits and costs
            annual_benefits = [
                self.rng.uniform(min_val, max_val)
                for min_val, max_val in annual_benefits_range
            ]
            annual_costs = [
                self.rng.uniform(min_val, max_val)
                for min_val, max_val in annual_costs_range
            ]
            
            # Calculate NPV for this simulation
            npv_result = self.calculate_npv(
                initial_investment,
                annual_benefits,
                annual_costs,
                discount_rate
            )
            npv_samples.append(npv_result.npv)
        
        npv_array = np.array(npv_samples)
        
        return {
            'expected_npv': float(np.mean(npv_array)),
            'median_npv': float(np.median(npv_array)),
            'std_npv': float(np.std(npv_array)),
            'npv_range_90pct': (float(np.percentile(npv_array, 5)), float(np.percentile(npv_array, 95))),
            'probability_positive_npv': float(np.mean(npv_array > 0)),
            'value_at_risk_5pct': float(np.percentile(npv_array, 5))
        }


class IRRCalculator:
    """
    Internal Rate of Return calculator.
    """
    
    def calculate_irr(self, cash_flows: List[float], initial_guess: float = 0.1) -> float:
        """
        Calculate Internal Rate of Return.
        
        Args:
            cash_flows: List of cash flows (year 0 is initial investment)
            initial_guess: Initial guess for IRR
            
        Returns:
            IRR as decimal (e.g., 0.15 for 15%)
        """
        def npv_at_rate(rate):
            return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))
        
        try:
            irr = newton(npv_at_rate, initial_guess, maxiter=100)
            return float(irr)
        except (RuntimeError, ValueError):
            # If Newton's method fails, return NaN
            return float('nan')
    
    def calculate_mirr(self,
                      cash_flows: List[float],
                      finance_rate: float,
                      reinvest_rate: float) -> float:
        """
        Calculate Modified Internal Rate of Return.
        
        Args:
            cash_flows: List of cash flows
            finance_rate: Rate for financing negative cash flows
            reinvest_rate: Rate for reinvesting positive cash flows
            
        Returns:
            MIRR as decimal
        """
        n = len(cash_flows) - 1
        
        # Present value of negative cash flows
        negative_pv = sum(
            cf / ((1 + finance_rate) ** i)
            for i, cf in enumerate(cash_flows) if cf < 0
        )
        
        # Future value of positive cash flows
        positive_fv = sum(
            cf * ((1 + reinvest_rate) ** (n - i))
            for i, cf in enumerate(cash_flows) if cf > 0
        )
        
        # MIRR calculation
        if negative_pv == 0:
            return float('nan')
        
        mirr = (positive_fv / abs(negative_pv)) ** (1 / n) - 1
        return float(mirr)


class PaybackAnalyzer:
    """
    Payback period analyzer for investment recovery analysis.
    """
    
    def calculate_payback_period(self,
                                initial_investment: float,
                                annual_net_benefits: List[float]) -> float:
        """
        Calculate simple payback period.
        
        Args:
            initial_investment: Initial investment amount
            annual_net_benefits: List of annual net benefits
            
        Returns:
            Payback period in years (fractional)
        """
        cumulative = 0
        
        for year, benefit in enumerate(annual_net_benefits):
            cumulative += benefit
            
            if cumulative >= initial_investment:
                # Fractional year calculation
                remaining = initial_investment - (cumulative - benefit)
                fraction = remaining / benefit if benefit > 0 else 0
                return year + fraction
        
        # If never pays back, return total years + 1
        return len(annual_net_benefits) + 1.0
    
    def calculate_discounted_payback(self,
                                    initial_investment: float,
                                    annual_net_benefits: List[float],
                                    discount_rate: float) -> float:
        """
        Calculate discounted payback period.
        
        Args:
            initial_investment: Initial investment amount
            annual_net_benefits: List of annual net benefits
            discount_rate: Discount rate
            
        Returns:
            Discounted payback period in years
        """
        cumulative_pv = 0
        
        for year, benefit in enumerate(annual_net_benefits):
            pv_benefit = benefit / ((1 + discount_rate) ** (year + 1))
            cumulative_pv += pv_benefit
            
            if cumulative_pv >= initial_investment:
                remaining = initial_investment - (cumulative_pv - pv_benefit)
                fraction = remaining / pv_benefit if pv_benefit > 0 else 0
                return year + 1 + fraction
        
        return len(annual_net_benefits) + 1.0


class CostBenefitAnalyzer:
    """
    Comprehensive cost-benefit analyzer.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize cost-benefit analyzer"""
        self.random_state = random_state
        self.npv_calculator = NPVCalculator(random_state=random_state)
    
    def analyze(self,
               benefits: Dict[str, List[float]],
               costs: Dict[str, List[float]],
               discount_rate: float,
               initial_investment: float = 0) -> Dict[str, Any]:
        """
        Perform comprehensive cost-benefit analysis.
        
        Args:
            benefits: Dictionary of benefit categories and annual values
            costs: Dictionary of cost categories and annual values
            discount_rate: Discount rate
            initial_investment: Initial investment
            
        Returns:
            Dictionary with comprehensive CBA results
        """
        # Aggregate benefits and costs
        n_years = max(
            max(len(v) for v in benefits.values()),
            max(len(v) for v in costs.values())
        )
        
        total_benefits = [0.0] * n_years
        total_costs = [0.0] * n_years
        
        for benefit_values in benefits.values():
            for i, val in enumerate(benefit_values):
                if i < n_years:
                    total_benefits[i] += val
        
        for cost_values in costs.values():
            for i, val in enumerate(cost_values):
                if i < n_years:
                    total_costs[i] += val
        
        # Calculate NPV
        npv_result = self.npv_calculator.calculate_npv(
            initial_investment,
            total_benefits,
            total_costs,
            discount_rate
        )
        
        # Benefit-Cost Ratio
        bc_ratio = npv_result.present_value_benefits / npv_result.present_value_costs if npv_result.present_value_costs > 0 else 0
        
        # Profitability Index
        profitability_index = npv_result.present_value_benefits / initial_investment if initial_investment > 0 else 0
        
        # Breakdown by category
        benefits_pv_by_category = {}
        for category, values in benefits.items():
            pv = sum(
                val / ((1 + discount_rate) ** (i + 1))
                for i, val in enumerate(values)
            )
            benefits_pv_by_category[category] = float(pv)
        
        costs_pv_by_category = {}
        for category, values in costs.items():
            pv = sum(
                val / ((1 + discount_rate) ** (i + 1))
                for i, val in enumerate(values)
            )
            costs_pv_by_category[category] = float(pv)
        
        return {
            'npv': npv_result.to_dict(),
            'benefit_cost_ratio': float(bc_ratio),
            'profitability_index': float(profitability_index),
            'benefits_by_category_pv': benefits_pv_by_category,
            'costs_by_category_pv': costs_pv_by_category,
            'total_benefits_pv': float(npv_result.present_value_benefits),
            'total_costs_pv': float(npv_result.present_value_costs)
        }


class RiskAdjustedROICalculator:
    """
    ROI calculator with risk adjustments for compliance investments.
    """
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize risk-adjusted ROI calculator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        self.npv_calculator = NPVCalculator(random_state=random_state)
        self.irr_calculator = IRRCalculator()
        self.payback_analyzer = PaybackAnalyzer()
        self.cba_analyzer = CostBenefitAnalyzer(random_state=random_state)
    
    def calculate_comprehensive_roi(self,
                                   initial_investment: float,
                                   annual_benefits: List[float],
                                   annual_costs: List[float],
                                   discount_rate: float,
                                   risk_premium: float = 0.02) -> ROIAnalysis:
        """
        Calculate comprehensive ROI with risk adjustments.
        
        Args:
            initial_investment: Initial investment
            annual_benefits: Annual benefits
            annual_costs: Annual costs
            discount_rate: Base discount rate
            risk_premium: Risk premium to add to discount rate
            
        Returns:
            ROIAnalysis with comprehensive metrics
        """
        # Risk-adjusted discount rate
        risk_adjusted_rate = discount_rate + risk_premium
        
        # NPV calculation
        npv_result = self.npv_calculator.calculate_npv(
            initial_investment,
            annual_benefits,
            annual_costs,
            risk_adjusted_rate
        )
        
        # IRR calculation
        net_cash_flows = [-initial_investment] + [
            annual_benefits[i] - annual_costs[i]
            for i in range(len(annual_benefits))
        ]
        irr = self.irr_calculator.calculate_irr(net_cash_flows)
        
        # Payback period
        net_annual_benefits = [
            annual_benefits[i] - annual_costs[i]
            for i in range(len(annual_benefits))
        ]
        payback = self.payback_analyzer.calculate_discounted_payback(
            initial_investment,
            net_annual_benefits,
            risk_adjusted_rate
        )
        
        # Benefit-cost ratio
        bc_ratio = npv_result.present_value_benefits / npv_result.present_value_costs if npv_result.present_value_costs > 0 else 0
        
        # Profitability index
        profitability_index = npv_result.present_value_benefits / initial_investment if initial_investment > 0 else 0
        
        # Simple ROI percentage
        total_benefits = sum(annual_benefits)
        total_costs = initial_investment + sum(annual_costs)
        roi_pct = ((total_benefits - total_costs) / total_costs) * 100 if total_costs > 0 else 0
        
        # Recommendation
        if npv_result.npv > 0 and irr > risk_adjusted_rate and payback < 3:
            recommendation = "STRONG_ACCEPT"
        elif npv_result.npv > 0 and irr > risk_adjusted_rate:
            recommendation = "ACCEPT"
        elif npv_result.npv > 0:
            recommendation = "MARGINAL_ACCEPT"
        elif npv_result.npv > -initial_investment * 0.1:
            recommendation = "NEUTRAL"
        else:
            recommendation = "REJECT"
        
        # Sensitivity analysis (simplified)
        sensitivity = self._simple_sensitivity_analysis(
            initial_investment,
            annual_benefits,
            annual_costs,
            risk_adjusted_rate
        )
        
        return ROIAnalysis(
            roi_percentage=roi_pct,
            npv=npv_result.npv,
            irr=irr,
            payback_period_years=payback,
            benefit_cost_ratio=bc_ratio,
            profitability_index=profitability_index,
            recommendation=recommendation,
            sensitivity_analysis=sensitivity
        )
    
    def _simple_sensitivity_analysis(self,
                                    initial_investment: float,
                                    annual_benefits: List[float],
                                    annual_costs: List[float],
                                    discount_rate: float) -> Dict[str, float]:
        """Perform simple sensitivity analysis"""
        base_npv = self.npv_calculator.calculate_npv(
            initial_investment,
            annual_benefits,
            annual_costs,
            discount_rate
        ).npv
        
        sensitivity = {}
        
        # Vary benefits by ±20%
        npv_benefits_up = self.npv_calculator.calculate_npv(
            initial_investment,
            [b * 1.2 for b in annual_benefits],
            annual_costs,
            discount_rate
        ).npv
        sensitivity['benefits_20pct_increase'] = ((npv_benefits_up - base_npv) / base_npv) * 100 if base_npv != 0 else 0
        
        # Vary costs by ±20%
        npv_costs_up = self.npv_calculator.calculate_npv(
            initial_investment,
            annual_benefits,
            [c * 1.2 for c in annual_costs],
            discount_rate
        ).npv
        sensitivity['costs_20pct_increase'] = ((npv_costs_up - base_npv) / base_npv) * 100 if base_npv != 0 else 0
        
        # Vary discount rate by ±2%
        npv_rate_up = self.npv_calculator.calculate_npv(
            initial_investment,
            annual_benefits,
            annual_costs,
            discount_rate + 0.02
        ).npv
        sensitivity['discount_rate_2pct_increase'] = ((npv_rate_up - base_npv) / base_npv) * 100 if base_npv != 0 else 0
        
        return sensitivity
