"""
Tests for Remediation Cost Models

Total: 12 tests
"""

import pytest
from services.risk_simulator.models.remediation_costs import (
    TechnicalRemediationEstimator,
    ProcessImprovementEstimator,
    TrainingCostEstimator,
    OngoingComplianceEstimator,
    ComprehensiveRemediationPlanner,
    ComplexityLevel
)


class TestTechnicalRemediationEstimator:
    
    def test_initialization(self):
        estimator = TechnicalRemediationEstimator(random_state=42)
        assert estimator.random_state == 42
    
    def test_estimate_low_complexity(self):
        estimator = TechnicalRemediationEstimator(random_state=42)
        result = estimator.estimate_technical_fix(
            complexity=ComplexityLevel.LOW,
            num_systems_affected=2
        )
        assert result.total_cost > 0
        assert result.complexity_level == 'low'
    
    def test_estimate_high_complexity(self):
        estimator = TechnicalRemediationEstimator(random_state=42)
        result = estimator.estimate_technical_fix(
            complexity=ComplexityLevel.VERY_HIGH,
            num_systems_affected=5,
            include_testing=True,
            include_documentation=True
        )
        assert result.total_cost > 0
        assert 'development' in result.cost_breakdown


class TestProcessImprovementEstimator:
    
    def test_initialization(self):
        estimator = ProcessImprovementEstimator(random_state=42)
        assert estimator.random_state == 42
    
    def test_estimate_process_change(self):
        estimator = ProcessImprovementEstimator(random_state=42)
        result = estimator.estimate_process_change(
            num_processes=3,
            num_employees_affected=50,
            change_magnitude=0.6
        )
        assert result.total_cost > 0
        assert result.timeline_months > 0


class TestTrainingCostEstimator:
    
    def test_initialization(self):
        estimator = TrainingCostEstimator(random_state=42)
        assert estimator.random_state == 42
    
    def test_estimate_online_training(self):
        estimator = TrainingCostEstimator(random_state=42)
        result = estimator.estimate_training_program(
            num_employees=100,
            training_hours_per_employee=4.0,
            delivery_method='online'
        )
        assert result.total_cost > 0
        assert 'platform_technology' in result.cost_breakdown
    
    def test_estimate_classroom_training(self):
        estimator = TrainingCostEstimator(random_state=42)
        result = estimator.estimate_training_program(
            num_employees=50,
            training_hours_per_employee=8.0,
            delivery_method='classroom'
        )
        assert result.total_cost > 0


class TestOngoingComplianceEstimator:
    
    def test_estimate_ongoing_costs(self):
        estimator = OngoingComplianceEstimator(random_state=42)
        result = estimator.estimate_ongoing_costs(
            num_compliance_controls=20,
            monitoring_frequency='monthly',
            requires_automated_tools=True,
            annual_audit_required=True
        )
        assert 'total_annual_cost' in result
        assert result['total_annual_cost'] > 0


class TestComprehensiveRemediationPlanner:
    
    def test_create_remediation_plan(self):
        planner = ComprehensiveRemediationPlanner(random_state=42)
        
        result = planner.create_remediation_plan(
            technical_params={'complexity': ComplexityLevel.MEDIUM, 'num_systems_affected': 3},
            process_params={'num_processes': 2, 'num_employees_affected': 30, 'change_magnitude': 0.5},
            training_params={'num_employees': 50, 'training_hours_per_employee': 4.0, 'delivery_method': 'hybrid'},
            ongoing_params={'num_compliance_controls': 15, 'monitoring_frequency': 'monthly'},
            planning_horizon_years=3
        )
        
        assert 'total_upfront_cost' in result
        assert 'total_annual_ongoing_cost' in result
        assert result['planning_horizon_years'] == 3
    
    def test_serialization(self):
        planner = ComprehensiveRemediationPlanner(random_state=42)
        result = planner.create_remediation_plan(
            technical_params={'complexity': ComplexityLevel.LOW, 'num_systems_affected': 1}
        )
        import json
        json.dumps(result)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
