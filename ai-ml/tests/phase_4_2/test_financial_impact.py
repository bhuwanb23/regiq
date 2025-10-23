"""
Tests for Financial Impact Models

Test coverage:
- PotentialFineCalculator (6 tests)
- BusinessDisruptionModel (4 tests)
- FinancialImpactAggregator (4 tests)

Total: 14 tests
"""

import pytest
import numpy as np
from services.risk_simulator.models.financial_impact import (
    PotentialFineCalculator,
    BusinessDisruptionModel,
    FinancialImpactAggregator,
    FineCategory,
    DisruptionSeverity,
    FineEstimate,
    DisruptionCost,
    FinancialImpactResult
)


class TestPotentialFineCalculator:
    """Test suite for PotentialFineCalculator"""
    
    def test_initialization(self):
        """Test initialization"""
        calc = PotentialFineCalculator(jurisdiction="federal", random_state=42)
        assert calc.jurisdiction == "federal"
        assert calc.random_state == 42
    
    def test_estimate_fine_administrative(self):
        """Test fine estimation for administrative category"""
        calc = PotentialFineCalculator(random_state=42)
        estimate = calc.estimate_fine(
            fine_category=FineCategory.ADMINISTRATIVE,
            violation_severity=0.5
        )
        
        assert isinstance(estimate, FineEstimate)
        assert estimate.expected_fine > 0
        assert estimate.fine_range[0] < estimate.fine_range[1]
        assert estimate.fine_category == 'administrative'
    
    def test_estimate_fine_with_revenue_factor(self):
        """Test fine estimation with revenue factor"""
        calc = PotentialFineCalculator(random_state=42)
        estimate = calc.estimate_fine(
            fine_category=FineCategory.CIVIL,
            violation_severity=0.7,
            revenue_factor=2.0
        )
        
        assert estimate.expected_fine > 0
        assert 'revenue_adjustment' in estimate.breakdown
    
    def test_estimate_fine_with_historical_data(self):
        """Test fine estimation calibrated with historical data"""
        calc = PotentialFineCalculator(random_state=42)
        historical_fines = [50000.0, 75000.0, 100000.0, 60000.0, 90000.0, 80000.0]
        
        estimate = calc.estimate_fine(
            fine_category=FineCategory.STATUTORY,
            violation_severity=0.6,
            historical_fines=historical_fines
        )
        
        assert estimate.probability_distribution == 'lognormal'
        assert estimate.expected_fine > 0
    
    def test_estimate_multiple_violations(self):
        """Test estimation for multiple violations"""
        calc = PotentialFineCalculator(random_state=42)
        violations = [
            {'category': FineCategory.ADMINISTRATIVE, 'severity': 0.3},
            {'category': FineCategory.CIVIL, 'severity': 0.6},
            {'category': FineCategory.STATUTORY, 'severity': 0.4}
        ]
        
        result = calc.estimate_multiple_violations(violations, correlation=0.3)
        
        assert 'total_expected_fine' in result
        assert result['number_of_violations'] == 3
        assert len(result['individual_estimates']) == 3
    
    def test_fine_estimate_to_dict(self):
        """Test FineEstimate serialization"""
        calc = PotentialFineCalculator(random_state=42)
        estimate = calc.estimate_fine(
            fine_category=FineCategory.CRIMINAL,
            violation_severity=0.8
        )
        
        estimate_dict = estimate.to_dict()
        
        assert isinstance(estimate_dict, dict)
        assert 'expected_fine' in estimate_dict
        assert isinstance(estimate_dict['expected_fine'], float)


class TestBusinessDisruptionModel:
    """Test suite for BusinessDisruptionModel"""
    
    def test_initialization(self):
        """Test initialization"""
        model = BusinessDisruptionModel(random_state=42)
        assert model.random_state == 42
    
    def test_estimate_disruption_minimal(self):
        """Test disruption estimation for minimal severity"""
        model = BusinessDisruptionModel(random_state=42)
        estimate = model.estimate_disruption_cost(
            annual_revenue=10000000.0,
            disruption_severity=DisruptionSeverity.MINIMAL,
            disruption_duration_days=5.0
        )
        
        assert isinstance(estimate, DisruptionCost)
        assert estimate.total_cost > 0
        assert estimate.disruption_severity == 'minimal'
    
    def test_estimate_disruption_severe(self):
        """Test disruption estimation for severe severity"""
        model = BusinessDisruptionModel(random_state=42)
        estimate = model.estimate_disruption_cost(
            annual_revenue=10000000.0,
            disruption_severity=DisruptionSeverity.SEVERE,
            disruption_duration_days=30.0,
            reputation_impact_factor=0.2
        )
        
        assert estimate.total_cost > 0
        assert estimate.revenue_impact > 0
        assert estimate.reputation_cost > 0
    
    def test_estimate_market_impact(self):
        """Test market capitalization impact"""
        model = BusinessDisruptionModel()
        market_impact = model.estimate_market_impact(
            market_cap=1000000000.0,
            stock_price_impact_pct=5.0
        )
        
        assert market_impact == 50000000.0
    
    def test_estimate_customer_churn(self):
        """Test customer churn cost estimation"""
        model = BusinessDisruptionModel()
        churn_cost = model.estimate_customer_churn_cost(
            annual_revenue_per_customer=1000.0,
            num_customers=10000,
            churn_rate=0.05,
            customer_lifetime_years=3.0
        )
        
        assert churn_cost > 0


class TestFinancialImpactAggregator:
    """Test suite for FinancialImpactAggregator"""
    
    def test_initialization(self):
        """Test initialization"""
        aggregator = FinancialImpactAggregator(random_state=42)
        assert aggregator.random_state == 42
    
    def test_calculate_total_impact(self):
        """Test total financial impact calculation"""
        aggregator = FinancialImpactAggregator(random_state=42)
        
        # Create fine estimates
        fine_calc = PotentialFineCalculator(random_state=42)
        fine1 = fine_calc.estimate_fine(FineCategory.ADMINISTRATIVE, 0.5)
        fine2 = fine_calc.estimate_fine(FineCategory.CIVIL, 0.7)
        
        # Create disruption costs
        disruption_model = BusinessDisruptionModel(random_state=42)
        disruption1 = disruption_model.estimate_disruption_cost(
            5000000.0,
            DisruptionSeverity.MODERATE,
            10.0
        )
        
        result = aggregator.calculate_total_impact(
            fine_estimates=[fine1, fine2],
            disruption_costs=[disruption1],
            n_simulations=1000
        )
        
        assert isinstance(result, FinancialImpactResult)
        assert result.total_financial_impact > 0
        assert result.expected_fines > 0
        assert result.business_disruption_cost > 0
        assert result.risk_category in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    def test_calculate_with_other_costs(self):
        """Test calculation with other costs"""
        aggregator = FinancialImpactAggregator(random_state=42)
        
        fine_calc = PotentialFineCalculator(random_state=42)
        fine1 = fine_calc.estimate_fine(FineCategory.STATUTORY, 0.6)
        
        disruption_model = BusinessDisruptionModel(random_state=42)
        disruption1 = disruption_model.estimate_disruption_cost(
            3000000.0,
            DisruptionSeverity.SIGNIFICANT,
            15.0
        )
        
        other_costs = {
            'legal_fees': 100000.0,
            'consulting_fees': 50000.0
        }
        
        result = aggregator.calculate_total_impact(
            fine_estimates=[fine1],
            disruption_costs=[disruption1],
            other_costs=other_costs,
            n_simulations=1000
        )
        
        assert result.other_costs == 150000.0
        assert 'legal_fees' in result.cost_components
    
    def test_sensitivity_analysis(self):
        """Test sensitivity analysis"""
        aggregator = FinancialImpactAggregator(random_state=42)
        
        fine_calc = PotentialFineCalculator(random_state=42)
        fine1 = fine_calc.estimate_fine(FineCategory.CIVIL, 0.5)
        
        disruption_model = BusinessDisruptionModel(random_state=42)
        disruption1 = disruption_model.estimate_disruption_cost(
            5000000.0,
            DisruptionSeverity.MODERATE,
            10.0
        )
        
        result = aggregator.calculate_total_impact(
            fine_estimates=[fine1],
            disruption_costs=[disruption1]
        )
        
        sensitivity = aggregator.sensitivity_analysis(
            result,
            parameter_variations={'fine_severity': 20, 'disruption_duration': 15}
        )
        
        assert isinstance(sensitivity, dict)
        assert len(sensitivity) > 0


class TestFinancialImpactIntegration:
    """Integration tests"""
    
    def test_end_to_end_financial_assessment(self):
        """Test complete financial impact assessment"""
        aggregator = FinancialImpactAggregator(random_state=42)
        
        # Multiple fines
        fine_calc = PotentialFineCalculator(random_state=42)
        violations = [
            {'category': FineCategory.ADMINISTRATIVE, 'severity': 0.4},
            {'category': FineCategory.CIVIL, 'severity': 0.7}
        ]
        
        fines = [
            fine_calc.estimate_fine(v['category'], v['severity'])
            for v in violations
        ]
        
        # Disruptions
        disruption_model = BusinessDisruptionModel(random_state=42)
        disruptions = [
            disruption_model.estimate_disruption_cost(
                8000000.0,
                DisruptionSeverity.MODERATE,
                12.0
            )
        ]
        
        # Total impact
        result = aggregator.calculate_total_impact(
            fine_estimates=fines,
            disruption_costs=disruptions,
            n_simulations=1000
        )
        
        # Verify comprehensive output
        assert result.total_financial_impact > 0
        assert result.impact_range[0] < result.impact_range[1]
        assert len(result.confidence_intervals) > 0
        
        # Serialize
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        
        import json
        json.dumps(result_dict)  # Ensure JSON serializable


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
