"""
Tests for ROI Calculator Models

Total: 14 tests
"""

import pytest
import numpy as np
from services.risk_simulator.models.roi_calculator import (
    NPVCalculator,
    IRRCalculator,
    PaybackAnalyzer,
    CostBenefitAnalyzer,
    RiskAdjustedROICalculator,
    NPVResult,
    ROIAnalysis
)


class TestNPVCalculator:
    
    def test_initialization(self):
        calc = NPVCalculator(random_state=42)
        assert calc.random_state == 42
    
    def test_calculate_npv(self):
        calc = NPVCalculator()
        result = calc.calculate_npv(
            initial_investment=100000.0,
            annual_benefits=[50000.0, 50000.0, 50000.0],
            annual_costs=[20000.0, 20000.0, 20000.0],
            discount_rate=0.10
        )
        
        assert isinstance(result, NPVResult)
        assert result.npv != 0
        assert result.discount_rate == 0.10
    
    def test_calculate_npv_with_uncertainty(self):
        calc = NPVCalculator(random_state=42)
        result = calc.calculate_npv_with_uncertainty(
            initial_investment=100000.0,
            annual_benefits_range=[(40000.0, 60000.0), (40000.0, 60000.0)],
            annual_costs_range=[(15000.0, 25000.0), (15000.0, 25000.0)],
            discount_rate_range=(0.08, 0.12),
            n_simulations=1000
        )
        
        assert 'expected_npv' in result
        assert 'probability_positive_npv' in result


class TestIRRCalculator:
    
    def test_calculate_irr(self):
        calc = IRRCalculator()
        cash_flows = [-100000.0, 30000.0, 40000.0, 50000.0, 60000.0]
        irr = calc.calculate_irr(cash_flows)
        
        assert irr > 0
    
    def test_calculate_mirr(self):
        calc = IRRCalculator()
        cash_flows = [-100000.0, 30000.0, 40000.0, 50000.0]
        mirr = calc.calculate_mirr(cash_flows, finance_rate=0.10, reinvest_rate=0.12)
        
        assert mirr > 0


class TestPaybackAnalyzer:
    
    def test_calculate_payback_period(self):
        analyzer = PaybackAnalyzer()
        payback = analyzer.calculate_payback_period(
            initial_investment=100000.0,
            annual_net_benefits=[30000.0, 40000.0, 50000.0]
        )
        
        assert payback > 0
        assert payback < 4
    
    def test_calculate_discounted_payback(self):
        analyzer = PaybackAnalyzer()
        payback = analyzer.calculate_discounted_payback(
            initial_investment=100000.0,
            annual_net_benefits=[30000.0, 40000.0, 50000.0],
            discount_rate=0.10
        )
        
        assert payback > 0


class TestCostBenefitAnalyzer:
    
    def test_analyze(self):
        analyzer = CostBenefitAnalyzer(random_state=42)
        result = analyzer.analyze(
            benefits={'revenue_increase': [50000.0, 50000.0]},
            costs={'operational': [20000.0, 20000.0]},
            discount_rate=0.10,
            initial_investment=100000.0
        )
        
        assert 'npv' in result
        assert 'benefit_cost_ratio' in result
        assert result['benefit_cost_ratio'] > 0


class TestRiskAdjustedROICalculator:
    
    def test_calculate_comprehensive_roi(self):
        calc = RiskAdjustedROICalculator(random_state=42)
        result = calc.calculate_comprehensive_roi(
            initial_investment=100000.0,
            annual_benefits=[50000.0, 50000.0, 50000.0],
            annual_costs=[20000.0, 20000.0, 20000.0],
            discount_rate=0.10,
            risk_premium=0.02
        )
        
        assert isinstance(result, ROIAnalysis)
        assert result.roi_percentage != 0
        assert result.recommendation in ['STRONG_ACCEPT', 'ACCEPT', 'MARGINAL_ACCEPT', 'NEUTRAL', 'REJECT']
    
    def test_sensitivity_analysis(self):
        calc = RiskAdjustedROICalculator(random_state=42)
        result = calc.calculate_comprehensive_roi(
            initial_investment=100000.0,
            annual_benefits=[50000.0, 50000.0],
            annual_costs=[20000.0, 20000.0],
            discount_rate=0.10
        )
        
        assert len(result.sensitivity_analysis) > 0
    
    def test_result_serialization(self):
        calc = RiskAdjustedROICalculator(random_state=42)
        result = calc.calculate_comprehensive_roi(
            initial_investment=50000.0,
            annual_benefits=[25000.0, 25000.0],
            annual_costs=[10000.0, 10000.0],
            discount_rate=0.10
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        import json
        json.dumps(result_dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
