"""
Tests for Operational Risk Models

Total: 12 tests
"""

import pytest
from services.risk_simulator.models.operational_risk import (
    SystemDowntimeModel,
    PerformanceDegradationModel,
    CapacityUtilizationModel,
    OperationalRiskAggregator,
    SystemCriticality,
    DowntimeCategory
)


class TestSystemDowntimeModel:
    
    def test_initialization(self):
        model = SystemDowntimeModel(random_state=42)
        assert model.random_state == 42
    
    def test_estimate_downtime(self):
        model = SystemDowntimeModel(random_state=42)
        result = model.estimate_downtime(
            system_criticality=SystemCriticality.HIGH,
            mtbf_hours=720.0,
            mttr_hours=4.0,
            annual_revenue=5000000.0
        )
        
        assert result.expected_downtime_hours > 0
        assert result.total_revenue_impact > 0
    
    def test_monte_carlo_downtime(self):
        model = SystemDowntimeModel(random_state=42)
        result = model.monte_carlo_downtime(
            mtbf_hours=500.0,
            mttr_hours=3.0,
            n_simulations=1000,
            simulation_period_hours=8760.0
        )
        
        assert 'mean_downtime_hours' in result
        assert result['mean_downtime_hours'] > 0


class TestPerformanceDegradationModel:
    
    def test_initialization(self):
        model = PerformanceDegradationModel(random_state=42)
        assert model.random_state == 42
    
    def test_estimate_performance_impact(self):
        model = PerformanceDegradationModel(random_state=42)
        result = model.estimate_performance_impact(
            baseline_performance=100.0,
            degraded_performance=70.0,
            daily_transactions=10000,
            transaction_value=50.0,
            num_users=500
        )
        
        assert result.performance_degradation_pct > 0
        assert result.total_cost >= 0


class TestCapacityUtilizationModel:
    
    def test_initialization(self):
        model = CapacityUtilizationModel(random_state=42)
        assert model.random_state == 42
    
    def test_estimate_capacity_impact(self):
        model = CapacityUtilizationModel(random_state=42)
        result = model.estimate_capacity_impact(
            current_utilization=0.7,
            compliance_overhead=0.15,
            max_capacity=1000.0,
            demand_growth_rate=0.10
        )
        
        assert 'new_utilization_pct' in result
        assert 'time_to_constraint_years' in result


class TestOperationalRiskAggregator:
    
    def test_initialization(self):
        aggregator = OperationalRiskAggregator(random_state=42)
        assert aggregator.random_state == 42
    
    def test_assess_operational_risk(self):
        aggregator = OperationalRiskAggregator(random_state=42)
        
        result = aggregator.assess_operational_risk(
            downtime_params={
                'system_criticality': SystemCriticality.HIGH,
                'mtbf_hours': 720.0,
                'mttr_hours': 4.0,
                'annual_revenue': 5000000.0
            },
            performance_params={
                'baseline_performance': 100.0,
                'degraded_performance': 80.0,
                'daily_transactions': 5000,
                'transaction_value': 100.0,
                'num_users': 200
            },
            capacity_params={
                'current_utilization': 0.65,
                'compliance_overhead': 0.10,
                'max_capacity': 1000.0
            }
        )
        
        assert result.total_operational_risk_score >= 0
        assert result.risk_category in ['LOW', 'MODERATE', 'HIGH', 'CRITICAL']
        assert result.mitigation_priority in ['IMMEDIATE', 'HIGH', 'MEDIUM', 'LOW']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
