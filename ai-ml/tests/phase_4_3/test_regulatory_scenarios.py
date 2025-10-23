"""
Tests for regulatory_scenarios.py

Tests regulatory change scenario generation including new regulations,
amendments, sunsets, harmonization, and divergence.
"""

import pytest
import json
from datetime import datetime
from services.risk_simulator.scenarios.regulatory_scenarios import (
    RegulationChangeScenario,
    JurisdictionScenarioGenerator,
    RegulationType,
    RegulationSeverity,
    ImplementationTimeline
)


class TestRegulationChangeScenario:
    """Test regulation change scenario generator"""
    
    def test_initialization(self):
        """Test scenario generator initialization"""
        generator = RegulationChangeScenario(random_state=42)
        assert generator is not None
        assert generator.random_state == 42
    
    def test_create_new_regulation_low_severity(self):
        """Test new regulation with low severity"""
        generator = RegulationChangeScenario(random_state=42)
        
        change = generator.create_new_regulation_scenario(
            jurisdiction="USA",
            severity=RegulationSeverity.LOW,
            implementation_timeline=ImplementationTimeline.SHORT
        )
        
        assert change.change_type == RegulationType.NEW_REGULATION.value
        assert change.severity == RegulationSeverity.LOW.value
        assert change.jurisdiction == "USA"
        assert change.estimated_cost > 0
        assert change.penalty_multiplier == 1.0
    
    def test_create_new_regulation_critical_severity(self):
        """Test new regulation with critical severity"""
        generator = RegulationChangeScenario(random_state=42)
        
        change = generator.create_new_regulation_scenario(
            jurisdiction="EU",
            severity=RegulationSeverity.CRITICAL,
            implementation_timeline=ImplementationTimeline.LONG
        )
        
        assert change.severity == RegulationSeverity.CRITICAL.value
        assert change.estimated_cost > 1000000  # Should be high cost
        assert change.penalty_multiplier == 4.0  # Critical multiplier
    
    def test_create_amendment_scenario(self):
        """Test regulation amendment scenario"""
        generator = RegulationChangeScenario(random_state=42)
        
        change = generator.create_amendment_scenario(
            existing_regulation_id="REG-USA-12345",
            jurisdiction="USA",
            amendment_severity=RegulationSeverity.MEDIUM
        )
        
        assert change.change_type == RegulationType.AMENDMENT.value
        assert "AMEND-" in change.regulation_id
        assert change.penalty_multiplier == 1.2
        assert change.estimated_cost < 200000  # Amendments cheaper than new regs
    
    def test_create_sunset_scenario(self):
        """Test regulation sunset scenario"""
        generator = RegulationChangeScenario(random_state=42)
        
        change = generator.create_sunset_scenario(
            regulation_id="REG-USA-OLD",
            jurisdiction="USA"
        )
        
        assert change.change_type == RegulationType.SUNSET.value
        assert change.estimated_cost < 0  # Negative cost (savings)
        assert change.penalty_multiplier == 0.0  # No penalties after sunset
    
    def test_regulation_id_format(self):
        """Test regulation ID format"""
        generator = RegulationChangeScenario(random_state=42)
        
        change = generator.create_new_regulation_scenario(
            jurisdiction="UK",
            severity=RegulationSeverity.MEDIUM,
            implementation_timeline=ImplementationTimeline.MEDIUM
        )
        
        assert change.regulation_id.startswith("REG-UK-")
        assert len(change.regulation_id.split("-")) == 3
    
    def test_to_dict_serialization(self):
        """Test RegulatoryChange serialization"""
        generator = RegulationChangeScenario(random_state=42)
        
        change = generator.create_new_regulation_scenario(
            jurisdiction="USA",
            severity=RegulationSeverity.HIGH,
            implementation_timeline=ImplementationTimeline.MEDIUM
        )
        
        result_dict = change.to_dict()
        assert isinstance(result_dict, dict)
        assert 'regulation_id' in result_dict
        assert 'estimated_cost' in result_dict
        
        # Test JSON serialization
        json.dumps(result_dict)


class TestJurisdictionScenarioGenerator:
    """Test multi-jurisdiction scenario generator"""
    
    def test_initialization(self):
        """Test generator initialization"""
        generator = JurisdictionScenarioGenerator(random_state=42)
        assert generator is not None
    
    def test_create_harmonization_scenario(self):
        """Test harmonization scenario"""
        generator = JurisdictionScenarioGenerator(random_state=42)
        
        scenario = generator.create_harmonization_scenario(
            jurisdictions=["USA", "EU", "UK"],
            severity=RegulationSeverity.HIGH,
            time_horizon_years=2
        )
        
        assert scenario.scenario_name.startswith("Harmonization")
        assert len(scenario.changes) == 3  # One per jurisdiction
        assert scenario.time_horizon_days == 730  # 2 years
        assert 0 < scenario.probability < 1
        assert scenario.total_estimated_cost > 0
    
    def test_create_divergence_scenario(self):
        """Test divergence scenario"""
        generator = JurisdictionScenarioGenerator(random_state=42)
        
        scenario = generator.create_divergence_scenario(
            jurisdictions=["USA", "China"],
            divergence_factor=0.7
        )
        
        assert scenario.scenario_name.startswith("Divergence")
        assert len(scenario.changes) == 2
        assert scenario.probability > 0.5  # Divergence more probable
        assert scenario.total_impact_score > 0
    
    def test_create_cascade_scenario(self):
        """Test cascade scenario"""
        generator = JurisdictionScenarioGenerator(random_state=42)
        
        scenario = generator.create_cascade_scenario(
            leading_jurisdiction="EU",
            follower_jurisdictions=["UK", "Canada", "Australia"],
            delay_months=6
        )
        
        assert scenario.scenario_name.startswith("Cascade")
        assert len(scenario.changes) == 4  # Leader + 3 followers
        assert scenario.time_horizon_days > 365
    
    def test_harmonization_cost_aggregation(self):
        """Test cost aggregation in harmonization"""
        generator = JurisdictionScenarioGenerator(random_state=42)
        
        scenario = generator.create_harmonization_scenario(
            jurisdictions=["USA", "EU"],
            severity=RegulationSeverity.MEDIUM
        )
        
        # Total cost should equal sum of individual changes
        individual_sum = sum(c.estimated_cost for c in scenario.changes)
        assert abs(scenario.total_estimated_cost - individual_sum) < 0.01
    
    def test_scenario_probability_bounds(self):
        """Test scenario probability is within bounds"""
        generator = JurisdictionScenarioGenerator(random_state=42)
        
        scenario = generator.create_harmonization_scenario(
            jurisdictions=["USA", "EU", "UK", "Japan", "Canada"],
            severity=RegulationSeverity.HIGH
        )
        
        assert 0 <= scenario.probability <= 1
    
    def test_scenario_to_dict_serialization(self):
        """Test RegulatoryScenario serialization"""
        generator = JurisdictionScenarioGenerator(random_state=42)
        
        scenario = generator.create_divergence_scenario(
            jurisdictions=["USA", "China"]
        )
        
        result_dict = scenario.to_dict()
        assert isinstance(result_dict, dict)
        assert 'scenario_id' in result_dict
        assert 'changes' in result_dict
        assert isinstance(result_dict['changes'], list)
        
        # Test JSON serialization
        json.dumps(result_dict)
    
    def test_cascade_delay_implementation(self):
        """Test follower delay in cascade scenario"""
        generator = JurisdictionScenarioGenerator(random_state=42)
        
        scenario = generator.create_cascade_scenario(
            leading_jurisdiction="USA",
            follower_jurisdictions=["Canada"],
            delay_months=12
        )
        
        lead_date = datetime.strptime(scenario.changes[0].effective_date, "%Y-%m-%d")
        follower_date = datetime.strptime(scenario.changes[1].effective_date, "%Y-%m-%d")
        
        # Follower should be ~12 months later
        diff_days = (follower_date - lead_date).days
        assert 350 < diff_days < 370  # Approximately 12 months
