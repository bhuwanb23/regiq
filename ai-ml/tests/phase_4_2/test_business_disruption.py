"""
Tests for Business Disruption Models

Test coverage:
- OperationalDisruptionModel (4 tests)
- SupplyChainImpactModel (3 tests)
- MarketConsequenceModel (3 tests)
- IntegratedDisruptionAnalyzer (2 tests)

Total: 12 tests
"""

import pytest
import numpy as np
from services.risk_simulator.models.business_disruption import (
    OperationalDisruptionModel,
    SupplyChainImpactModel,
    MarketConsequenceModel,
    IntegratedDisruptionAnalyzer,
    OperationalPhase,
    SupplyChainTier,
    OperationalImpact,
    SupplyChainImpact,
    MarketImpact
)


class TestOperationalDisruptionModel:
    """Test suite for OperationalDisruptionModel"""
    
    def test_initialization(self):
        """Test initialization"""
        model = OperationalDisruptionModel(random_state=42)
        assert model.random_state == 42
    
    def test_estimate_disruption(self):
        """Test disruption estimation"""
        model = OperationalDisruptionModel(random_state=42)
        result = model.estimate_disruption(
            affected_phases=[OperationalPhase.PRODUCTION, OperationalPhase.DISTRIBUTION],
            disruption_severity=0.6,
            annual_revenue=10000000.0,
            annual_operational_cost=3000000.0
        )
        
        assert isinstance(result, OperationalImpact)
        assert result.capacity_loss_pct > 0
        assert result.total_cost > 0
        assert len(result.affected_operations) == 2
    
    def test_cascading_effects(self):
        """Test cascading effect estimation"""
        model = OperationalDisruptionModel(random_state=42)
        initial = [OperationalPhase.PRODUCTION]
        all_affected = model.estimate_cascading_effects(initial, propagation_probability=0.5)
        
        assert len(all_affected) >= len(initial)
    
    def test_result_serialization(self):
        """Test OperationalImpact to_dict"""
        model = OperationalDisruptionModel(random_state=42)
        result = model.estimate_disruption(
            [OperationalPhase.SALES],
            0.5,
            5000000.0,
            1500000.0
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        import json
        json.dumps(result_dict)


class TestSupplyChainImpactModel:
    """Test suite for SupplyChainImpactModel"""
    
    def test_initialization(self):
        """Test initialization"""
        model = SupplyChainImpactModel(random_state=42)
        assert model.random_state == 42
    
    def test_estimate_supplier_disruption(self):
        """Test supplier disruption estimation"""
        model = SupplyChainImpactModel(random_state=42)
        result = model.estimate_supplier_disruption(
            total_suppliers=50,
            disruption_probability=0.2,
            annual_supplier_spend=2000000.0,
            alternative_cost_premium=0.3,
            delay_days=45.0
        )
        
        assert isinstance(result, SupplyChainImpact)
        assert result.total_cost > 0
        assert result.recovery_strategy in ['tactical_sourcing', 'diversification', 'strategic_restructuring']
    
    def test_tier_propagation(self):
        """Test supply chain tier propagation"""
        model = SupplyChainImpactModel(random_state=42)
        tiers = model.estimate_tier_propagation(
            tier_1_disruption=0.8,
            propagation_factor=0.6
        )
        
        assert 'tier_1' in tiers
        assert 'tier_2' in tiers
        assert 'tier_3' in tiers
        assert tiers['tier_1'] > tiers['tier_2'] > tiers['tier_3']


class TestMarketConsequenceModel:
    """Test suite for MarketConsequenceModel"""
    
    def test_initialization(self):
        """Test initialization"""
        model = MarketConsequenceModel(random_state=42)
        assert model.random_state == 42
    
    def test_estimate_market_impact(self):
        """Test market impact estimation"""
        model = MarketConsequenceModel(random_state=42)
        result = model.estimate_market_impact(
            current_market_share=0.15,
            compliance_issue_severity=0.7,
            media_exposure=0.8,
            competitor_strength=0.6,
            customer_switching_cost=0.4
        )
        
        assert isinstance(result, MarketImpact)
        assert result.market_share_loss_pct >= 0
        assert 0 <= result.recovery_likelihood <= 1
    
    def test_stock_price_impact(self):
        """Test stock price impact estimation"""
        model = MarketConsequenceModel(random_state=42)
        market_impact = model.estimate_market_impact(0.2, 0.6, 0.7, 0.5)
        
        stock_impact = model.estimate_stock_price_impact(
            market_impact,
            market_cap=5000000000.0
        )
        
        assert 'stock_price_drop_pct' in stock_impact
        assert 'market_cap_loss' in stock_impact
        assert stock_impact['market_cap_loss'] > 0


class TestIntegratedDisruptionAnalyzer:
    """Test suite for IntegratedDisruptionAnalyzer"""
    
    def test_initialization(self):
        """Test initialization"""
        analyzer = IntegratedDisruptionAnalyzer(random_state=42)
        assert analyzer.random_state == 42
    
    def test_analyze_total_disruption(self):
        """Test total disruption analysis"""
        analyzer = IntegratedDisruptionAnalyzer(random_state=42)
        
        operational_params = {
            'affected_phases': [OperationalPhase.PRODUCTION],
            'disruption_severity': 0.5,
            'annual_revenue': 8000000.0,
            'annual_operational_cost': 2400000.0
        }
        
        supply_chain_params = {
            'total_suppliers': 30,
            'disruption_probability': 0.15,
            'annual_supplier_spend': 1500000.0
        }
        
        market_params = {
            'current_market_share': 0.12,
            'compliance_issue_severity': 0.6,
            'media_exposure': 0.5,
            'competitor_strength': 0.4
        }
        
        result = analyzer.analyze_total_disruption(
            operational_params,
            supply_chain_params,
            market_params,
            annual_revenue=8000000.0
        )
        
        assert 'total_disruption_cost' in result
        assert 'disruption_category' in result
        assert result['disruption_category'] in ['MINOR', 'MODERATE', 'MAJOR', 'SEVERE']
        assert 'cost_breakdown' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
