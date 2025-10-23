"""
Tests for scenario_engine.py

Tests scenario orchestration, industry templates, and combined scenarios.
"""

import pytest
import json
from services.risk_simulator.scenarios.scenario_engine import (
    ScenarioOrchestrator,
    ScenarioLibrary,
    IndustryTemplate
)


class TestScenarioOrchestrator:
    """Test scenario orchestrator"""
    
    def test_initialization(self):
        """Test orchestrator initialization"""
        orchestrator = ScenarioOrchestrator(random_state=42)
        assert orchestrator is not None
        assert orchestrator.random_state == 42
    
    def test_run_combined_scenario(self):
        """Test combined scenario execution"""
        orchestrator = ScenarioOrchestrator(random_state=42)
        
        config = {
            'jurisdictions': ['USA', 'EU'],
            'time_horizon_years': 2,
            'stress_level': 'moderate'
        }
        
        result = orchestrator.run_combined_scenario(config, include_stress_test=True)
        
        assert result is not None
        assert result.execution_time_seconds > 0
        assert len(result.regulatory_results) > 0
        assert len(result.enforcement_results) > 0
        assert result.aggregated_risk_score > 0
    
    def test_combined_scenario_serialization(self):
        """Test combined scenario result serialization"""
        orchestrator = ScenarioOrchestrator(random_state=42)
        
        config = {
            'jurisdictions': ['USA'],
            'time_horizon_years': 1,
            'stress_level': 'moderate'
        }
        
        result = orchestrator.run_combined_scenario(config)
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'scenario_id' in result_dict
        assert 'execution_time_seconds' in result_dict
        
        # Test JSON serialization
        json.dumps(result_dict)


class TestScenarioLibrary:
    """Test scenario library and templates"""
    
    def test_initialization(self):
        """Test library initialization"""
        library = ScenarioLibrary(random_state=42)
        assert library is not None
    
    def test_get_financial_services_template(self):
        """Test financial services template"""
        library = ScenarioLibrary(random_state=42)
        
        template = library.get_industry_template(IndustryTemplate.FINANCIAL_SERVICES)
        
        assert template is not None
        assert template['name'] == 'Financial Services Compliance Stress Test'
        assert 'USA' in template['jurisdictions']
        assert template['expected_severity'] == 'high'
    
    def test_get_healthcare_template(self):
        """Test healthcare template"""
        library = ScenarioLibrary(random_state=42)
        
        template = library.get_industry_template(IndustryTemplate.HEALTHCARE)
        
        assert template is not None
        assert 'HIPAA' in template['key_regulations']
        assert template['expected_severity'] == 'moderate'
    
    def test_get_technology_template(self):
        """Test technology template"""
        library = ScenarioLibrary(random_state=42)
        
        template = library.get_industry_template(IndustryTemplate.TECHNOLOGY)
        
        assert template is not None
        assert 'AI Act' in template['key_regulations']
        assert 'ai_governance' in template['focus_areas']
    
    def test_list_available_templates(self):
        """Test listing all templates"""
        library = ScenarioLibrary(random_state=42)
        
        templates = library.list_available_templates()
        
        assert len(templates) == 5  # All industry templates
        assert all('industry' in t for t in templates)
        assert all('name' in t for t in templates)
    
    def test_run_industry_scenario(self):
        """Test running industry-specific scenario"""
        library = ScenarioLibrary(random_state=42)
        
        result = library.run_industry_scenario(IndustryTemplate.RETAIL)
        
        assert result is not None
        assert result.execution_time_seconds > 0
        assert len(result.regulatory_results) > 0
