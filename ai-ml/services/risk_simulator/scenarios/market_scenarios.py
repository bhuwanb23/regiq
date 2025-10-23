"""
Market Scenarios Module

This module implements market condition simulation including:
- Economic boom/recession scenarios
- Market volatility modeling
- Industry-specific changes
- Competitive landscape shifts

Integrates with Phase 4.2 financial impact models.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import numpy as np


class EconomicCondition(Enum):
    """Economic condition types"""
    DEEP_RECESSION = "deep_recession"
    RECESSION = "recession"
    SLOWDOWN = "slowdown"
    STABLE = "stable"
    GROWTH = "growth"
    BOOM = "boom"


class MarketVolatility(Enum):
    """Market volatility levels"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EXTREME = "extreme"


class IndustryTrend(Enum):
    """Industry trend directions"""
    DECLINING = "declining"
    STABLE = "stable"
    GROWING = "growing"
    TRANSFORMING = "transforming"


@dataclass
class MarketConditions:
    """Market conditions snapshot"""
    condition_id: str
    economic_condition: str
    volatility_level: str
    gdp_growth_rate: float
    unemployment_rate: float
    interest_rate: float
    compliance_budget_multiplier: float
    market_risk_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'condition_id': self.condition_id,
            'economic_condition': self.economic_condition,
            'volatility_level': self.volatility_level,
            'gdp_growth_rate': float(self.gdp_growth_rate),
            'unemployment_rate': float(self.unemployment_rate),
            'interest_rate': float(self.interest_rate),
            'compliance_budget_multiplier': float(self.compliance_budget_multiplier),
            'market_risk_score': float(self.market_risk_score)
        }


@dataclass
class MarketScenario:
    """Complete market scenario"""
    scenario_id: str
    scenario_name: str
    description: str
    conditions: List[MarketConditions]
    time_horizon_days: int
    probability: float
    overall_impact_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'scenario_id': self.scenario_id,
            'scenario_name': self.scenario_name,
            'description': self.description,
            'conditions': [c.to_dict() for c in self.conditions],
            'time_horizon_days': int(self.time_horizon_days),
            'probability': float(self.probability),
            'overall_impact_score': float(self.overall_impact_score)
        }


class EconomicScenarioGenerator:
    """Generate economic scenarios"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        
        # Economic condition parameters
        self.condition_params = {
            EconomicCondition.DEEP_RECESSION: {
                'gdp': (-0.08, -0.03), 'unemployment': (0.10, 0.15),
                'interest': (0.0, 0.02), 'budget_mult': (0.5, 0.7)
            },
            EconomicCondition.RECESSION: {
                'gdp': (-0.03, 0.0), 'unemployment': (0.07, 0.10),
                'interest': (0.01, 0.03), 'budget_mult': (0.7, 0.85)
            },
            EconomicCondition.SLOWDOWN: {
                'gdp': (0.0, 0.02), 'unemployment': (0.05, 0.07),
                'interest': (0.02, 0.04), 'budget_mult': (0.85, 0.95)
            },
            EconomicCondition.STABLE: {
                'gdp': (0.02, 0.04), 'unemployment': (0.04, 0.05),
                'interest': (0.025, 0.045), 'budget_mult': (0.95, 1.05)
            },
            EconomicCondition.GROWTH: {
                'gdp': (0.04, 0.06), 'unemployment': (0.03, 0.04),
                'interest': (0.03, 0.05), 'budget_mult': (1.05, 1.20)
            },
            EconomicCondition.BOOM: {
                'gdp': (0.06, 0.10), 'unemployment': (0.02, 0.03),
                'interest': (0.04, 0.06), 'budget_mult': (1.20, 1.50)
            }
        }
    
    def create_market_condition(self,
                                economic_condition: EconomicCondition,
                                volatility: MarketVolatility) -> MarketConditions:
        """Create market conditions snapshot"""
        params = self.condition_params[economic_condition]
        
        # Sample parameters
        gdp = self.rng.uniform(*params['gdp'])
        unemployment = self.rng.uniform(*params['unemployment'])
        interest = self.rng.uniform(*params['interest'])
        budget_mult = self.rng.uniform(*params['budget_mult'])
        
        # Risk score based on volatility and economic condition
        vol_scores = {
            MarketVolatility.LOW: 1.0,
            MarketVolatility.MODERATE: 1.5,
            MarketVolatility.HIGH: 2.5,
            MarketVolatility.EXTREME: 4.0
        }
        
        base_risk = 50.0  # Base risk score
        condition_impact = abs(gdp) * 100  # GDP impact
        risk_score = base_risk + condition_impact + (vol_scores[volatility] * 10)
        
        condition_id = f"MKT-{economic_condition.value.upper()}-{self.rng.randint(1000, 9999)}"
        
        return MarketConditions(
            condition_id=condition_id,
            economic_condition=economic_condition.value,
            volatility_level=volatility.value,
            gdp_growth_rate=gdp,
            unemployment_rate=unemployment,
            interest_rate=interest,
            compliance_budget_multiplier=budget_mult,
            market_risk_score=risk_score
        )
    
    def create_recession_scenario(self,
                                  severity: str = "moderate",
                                  duration_months: int = 18) -> MarketScenario:
        """Create recession scenario"""
        conditions = []
        
        # Recession phases
        if severity == "mild":
            phases = [
                (EconomicCondition.SLOWDOWN, 3),
                (EconomicCondition.RECESSION, 6),
                (EconomicCondition.SLOWDOWN, 6),
                (EconomicCondition.STABLE, 3)
            ]
            volatility = MarketVolatility.MODERATE
        else:  # moderate/severe
            phases = [
                (EconomicCondition.SLOWDOWN, 2),
                (EconomicCondition.RECESSION, 8),
                (EconomicCondition.DEEP_RECESSION, 4),
                (EconomicCondition.RECESSION, 4)
            ]
            volatility = MarketVolatility.HIGH
        
        for condition, _ in phases:
            market_cond = self.create_market_condition(condition, volatility)
            conditions.append(market_cond)
        
        avg_risk = float(np.mean([c.market_risk_score for c in conditions]))
        
        scenario_id = f"RECESSION-{severity.upper()}-{self.rng.randint(1000, 9999)}"
        
        return MarketScenario(
            scenario_id=scenario_id,
            scenario_name=f"{severity.capitalize()} Recession Scenario",
            description=f"Economic recession with {severity} severity over {duration_months} months",
            conditions=conditions,
            time_horizon_days=duration_months * 30,
            probability=0.15 if severity == "mild" else 0.08,
            overall_impact_score=avg_risk
        )
    
    def create_boom_scenario(self,
                            duration_months: int = 24) -> MarketScenario:
        """Create economic boom scenario"""
        conditions = []
        volatility = MarketVolatility.LOW
        
        phases = [
            (EconomicCondition.STABLE, 3),
            (EconomicCondition.GROWTH, 6),
            (EconomicCondition.BOOM, 12),
            (EconomicCondition.GROWTH, 3)
        ]
        
        for condition, _ in phases:
            market_cond = self.create_market_condition(condition, volatility)
            conditions.append(market_cond)
        
        avg_risk = float(np.mean([c.market_risk_score for c in conditions]))
        
        scenario_id = f"BOOM-{self.rng.randint(1000, 9999)}"
        
        return MarketScenario(
            scenario_id=scenario_id,
            scenario_name="Economic Boom Scenario",
            description=f"Sustained economic growth over {duration_months} months",
            conditions=conditions,
            time_horizon_days=duration_months * 30,
            probability=0.12,
            overall_impact_score=avg_risk
        )


class CompetitiveLandscapeSimulator:
    """Simulate competitive landscape changes"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def simulate_technology_adoption(self,
                                    technology_type: str,
                                    adoption_rate: float = 0.3) -> Dict[str, Any]:
        """Simulate technology adoption impact on compliance"""
        
        # Calculate compliance complexity from tech adoption
        complexity_increase = adoption_rate * self.rng.uniform(1.2, 1.8)
        
        # Budget impact
        initial_investment_mult = 1 + (adoption_rate * 2.0)
        ongoing_cost_mult = 1 + (adoption_rate * 0.5)
        
        # Risk impact
        risk_reduction = adoption_rate * 0.3  # Better tech = lower risk
        
        return {
            'technology_type': technology_type,
            'adoption_rate': float(adoption_rate),
            'complexity_increase_factor': float(complexity_increase),
            'initial_investment_multiplier': float(initial_investment_mult),
            'ongoing_cost_multiplier': float(ongoing_cost_mult),
            'risk_reduction_factor': float(risk_reduction),
            'net_compliance_impact': float(complexity_increase - risk_reduction)
        }
