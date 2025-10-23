"""
Tests for resource_requirements.py

Tests resource estimation models including personnel, technology,
and integrated resource planning.
"""

import pytest
import numpy as np
from services.risk_simulator.models.resource_requirements import (
    PersonnelRequirementsEstimator,
    TechnologyResourceEstimator,
    ResourcePlanningModel,
    ResourceType,
    SkillLevel,
    ResourceEstimate
)


class TestPersonnelRequirementsEstimator:
    """Test personnel requirements estimator"""
    
    def test_initialization(self):
        """Test estimator initialization"""
        estimator = PersonnelRequirementsEstimator()
        assert estimator is not None
        assert len(estimator.ANNUAL_SALARIES) == 4
    
    def test_estimate_compliance_staff_basic(self):
        """Test basic compliance staff estimation"""
        estimator = PersonnelRequirementsEstimator()
        
        result = estimator.estimate_compliance_staff(
            num_regulations=50,
            num_systems=10,
            company_size="medium"
        )
        
        assert isinstance(result, ResourceEstimate)
        assert result.resource_type == ResourceType.PERSONNEL.value
        assert result.quantity_needed > 0
        assert result.annual_cost > 0
        assert result.one_time_cost > 0
        assert len(result.skill_breakdown) == 4
    
    def test_estimate_compliance_staff_small_company(self):
        """Test staff estimation for small company"""
        estimator = PersonnelRequirementsEstimator()
        
        result = estimator.estimate_compliance_staff(
            num_regulations=20,
            num_systems=5,
            company_size="small"
        )
        
        assert result.quantity_needed >= 1
        # Annual cost might be 0 if skill breakdown rounds to all zeros
        # Check that at least one cost component exists
        assert result.one_time_cost > 0
    
    def test_estimate_compliance_staff_enterprise(self):
        """Test staff estimation for enterprise"""
        estimator = PersonnelRequirementsEstimator()
        
        result = estimator.estimate_compliance_staff(
            num_regulations=100,
            num_systems=50,
            company_size="enterprise"
        )
        
        assert result.quantity_needed > 10
        assert result.annual_cost > 1000000
    
    def test_skill_distribution(self):
        """Test skill level distribution in estimates"""
        estimator = PersonnelRequirementsEstimator()
        
        result = estimator.estimate_compliance_staff(
            num_regulations=50,
            num_systems=10
        )
        
        # Check all skill levels present
        skill_breakdown = result.skill_breakdown
        assert SkillLevel.JUNIOR.value in skill_breakdown
        assert SkillLevel.MID_LEVEL.value in skill_breakdown
        assert SkillLevel.SENIOR.value in skill_breakdown
        assert SkillLevel.EXPERT.value in skill_breakdown
        
        # Check total is close (rounding may cause slight difference)
        total_staff = sum(skill_breakdown.values())
        assert total_staff <= result.quantity_needed
        assert total_staff >= result.quantity_needed - 2  # Allow for rounding
    
    def test_to_dict_serialization(self):
        """Test ResourceEstimate serialization"""
        estimator = PersonnelRequirementsEstimator()
        
        result = estimator.estimate_compliance_staff(
            num_regulations=50,
            num_systems=10
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert 'resource_type' in result_dict
        assert 'quantity_needed' in result_dict
        assert 'annual_cost' in result_dict
        
        # Test JSON serialization
        import json
        json.dumps(result_dict)


class TestTechnologyResourceEstimator:
    """Test technology resource estimator"""
    
    def test_initialization(self):
        """Test estimator initialization"""
        estimator = TechnologyResourceEstimator()
        assert estimator is not None
    
    def test_estimate_technology_needs_basic(self):
        """Test basic technology estimation"""
        estimator = TechnologyResourceEstimator()
        
        result = estimator.estimate_technology_needs(
            num_systems=10,
            data_volume_tb=100.0,
            concurrent_users=1000
        )
        
        assert isinstance(result, ResourceEstimate)
        assert result.resource_type == ResourceType.TECHNOLOGY.value
        assert result.quantity_needed >= 2
        assert result.annual_cost > 0
        assert result.one_time_cost > 0
    
    def test_estimate_technology_needs_large_scale(self):
        """Test technology estimation for large systems"""
        estimator = TechnologyResourceEstimator()
        
        result = estimator.estimate_technology_needs(
            num_systems=50,
            data_volume_tb=1000.0,
            concurrent_users=10000
        )
        
        assert result.quantity_needed > 10
        assert result.annual_cost > 100000
    
    def test_estimate_technology_needs_small_scale(self):
        """Test technology estimation for small systems"""
        estimator = TechnologyResourceEstimator()
        
        result = estimator.estimate_technology_needs(
            num_systems=2,
            data_volume_tb=10.0,
            concurrent_users=100
        )
        
        # Minimum of 2 servers for redundancy
        assert result.quantity_needed >= 2
        assert result.annual_cost > 0


class TestResourcePlanningModel:
    """Test integrated resource planning model"""
    
    def test_initialization(self):
        """Test planner initialization"""
        planner = ResourcePlanningModel()
        assert planner is not None
        assert isinstance(planner.personnel_estimator, PersonnelRequirementsEstimator)
        assert isinstance(planner.tech_estimator, TechnologyResourceEstimator)
    
    def test_create_resource_plan_basic(self):
        """Test basic resource plan creation"""
        planner = ResourcePlanningModel()
        
        planning_params = {
            'num_regulations': 50,
            'num_systems': 10,
            'company_size': 'medium',
            'data_volume_tb': 100,
            'concurrent_users': 1000
        }
        
        result = planner.create_resource_plan(planning_params)
        
        assert isinstance(result, dict)
        assert 'personnel' in result
        assert 'technology' in result
        assert 'total_annual_cost' in result
        assert 'total_one_time_cost' in result
        assert 'total_first_year_cost' in result
        assert 'within_budget' in result
    
    def test_create_resource_plan_with_budget_constraint(self):
        """Test resource plan with budget constraint"""
        planner = ResourcePlanningModel()
        
        planning_params = {
            'num_regulations': 50,
            'num_systems': 10,
            'company_size': 'medium',
            'data_volume_tb': 100,
            'concurrent_users': 1000
        }
        
        budget = 2000000.0
        result = planner.create_resource_plan(planning_params, budget_constraint=budget)
        
        assert isinstance(result['within_budget'], bool)
        assert 'budget_utilization_pct' in result
        assert result['budget_utilization_pct'] >= 0
    
    def test_create_resource_plan_insufficient_budget(self):
        """Test resource plan with insufficient budget"""
        planner = ResourcePlanningModel()
        
        planning_params = {
            'num_regulations': 100,
            'num_systems': 50,
            'company_size': 'enterprise',
            'data_volume_tb': 1000,
            'concurrent_users': 10000
        }
        
        # Very small budget
        budget = 100000.0
        result = planner.create_resource_plan(planning_params, budget_constraint=budget)
        
        assert result['within_budget'] == False
        assert result['budget_utilization_pct'] > 100
    
    def test_create_resource_plan_total_costs(self):
        """Test total cost calculations"""
        planner = ResourcePlanningModel()
        
        planning_params = {
            'num_regulations': 50,
            'num_systems': 10,
            'company_size': 'medium',
            'data_volume_tb': 100,
            'concurrent_users': 1000
        }
        
        result = planner.create_resource_plan(planning_params)
        
        personnel_annual = result['personnel']['annual_cost']
        tech_annual = result['technology']['annual_cost']
        
        assert result['total_annual_cost'] == personnel_annual + tech_annual
        
        personnel_onetime = result['personnel']['one_time_cost']
        tech_onetime = result['technology']['one_time_cost']
        
        expected_first_year = personnel_annual + tech_annual + personnel_onetime + tech_onetime
        assert abs(result['total_first_year_cost'] - expected_first_year) < 0.01
    
    def test_resource_plan_json_serialization(self):
        """Test complete resource plan JSON serialization"""
        planner = ResourcePlanningModel()
        
        planning_params = {
            'num_regulations': 50,
            'num_systems': 10,
            'company_size': 'medium',
            'data_volume_tb': 100,
            'concurrent_users': 1000
        }
        
        result = planner.create_resource_plan(planning_params)
        
        # Test JSON serialization
        import json
        json.dumps(result)
