"""
Tests for stress_scenarios.py

Tests stress test scenario design including worst-case scenarios,
multi-factor stress, cascade failures, and historical crisis replays.
"""

import pytest
import json
from services.risk_simulator.scenarios.stress_scenarios import (
    StressScenarioDesigner,
    HistoricalCrisisReplicator,
    StressLevel,
    StressCategory
)


class TestStressScenarioDesigner:
    """Test stress scenario designer"""
    
    def test_initialization(self):
        """Test designer initialization"""
        designer = StressScenarioDesigner(random_state=42)
        assert designer is not None
    
    def test_create_regulatory_worst_case(self):
        """Test worst-case regulatory scenario"""
        designer = StressScenarioDesigner(random_state=42)
        
        scenario = designer.create_regulatory_worst_case()
        
        assert scenario.stress_level == StressLevel.CATASTROPHIC.value
        assert scenario.category == StressCategory.REGULATORY_ONLY.value
        assert len(scenario.stress_factors) >= 3
        assert scenario.combined_severity_score > 200
        assert scenario.expected_financial_impact > 1000000
    
    def test_create_multi_factor_moderate(self):
        """Test moderate multi-factor stress"""
        designer = StressScenarioDesigner(random_state=42)
        
        scenario = designer.create_multi_factor_stress(
            stress_level=StressLevel.MODERATE
        )
        
        assert scenario.stress_level == StressLevel.MODERATE.value
        assert scenario.category == StressCategory.COMBINED.value
        assert len(scenario.stress_factors) >= 4
        assert scenario.mitigation_difficulty in ["high", "extreme"]
    
    def test_create_multi_factor_catastrophic(self):
        """Test catastrophic multi-factor stress"""
        designer = StressScenarioDesigner(random_state=42)
        
        scenario = designer.create_multi_factor_stress(
            stress_level=StressLevel.CATASTROPHIC
        )
        
        assert scenario.stress_level == StressLevel.CATASTROPHIC.value
        assert scenario.expected_financial_impact > 10000000
        assert scenario.combined_severity_score > 300
    
    def test_create_cascade_failure(self):
        """Test cascade failure scenario"""
        designer = StressScenarioDesigner(random_state=42)
        
        scenario = designer.create_cascade_failure_scenario()
        
        assert scenario.category == StressCategory.CASCADE.value
        assert len(scenario.stress_factors) >= 5  # Multiple cascade stages
        assert scenario.time_horizon_days >= 365
        assert scenario.mitigation_difficulty == "extreme"
    
    def test_stress_factor_serialization(self):
        """Test stress factor serialization"""
        designer = StressScenarioDesigner(random_state=42)
        
        scenario = designer.create_regulatory_worst_case()
        factor = scenario.stress_factors[0]
        
        factor_dict = factor.to_dict()
        assert isinstance(factor_dict, dict)
        assert 'factor_id' in factor_dict
        assert 'severity_multiplier' in factor_dict
        
        # Test JSON serialization
        json.dumps(factor_dict)
    
    def test_scenario_to_dict_serialization(self):
        """Test stress scenario serialization"""
        designer = StressScenarioDesigner(random_state=42)
        
        scenario = designer.create_multi_factor_stress()
        
        result_dict = scenario.to_dict()
        assert isinstance(result_dict, dict)
        assert 'scenario_id' in result_dict
        assert 'stress_factors' in result_dict
        
        # Test JSON serialization
        json.dumps(result_dict)


class TestHistoricalCrisisReplicator:
    """Test historical crisis replication"""
    
    def test_initialization(self):
        """Test replicator initialization"""
        replicator = HistoricalCrisisReplicator(random_state=42)
        assert replicator is not None
    
    def test_replicate_2008_crisis(self):
        """Test 2008 financial crisis replication"""
        replicator = HistoricalCrisisReplicator(random_state=42)
        
        result = replicator.replicate_crisis("2008_financial_crisis")
        
        assert result['crisis_name'] == "2008_financial_crisis"
        assert result['enforcement_escalation_factor'] > 3.0
        assert result['expected_duration_months'] > 24
        assert 'historical_lessons' in result
    
    def test_replicate_cambridge_analytica(self):
        """Test Cambridge Analytica crisis replication"""
        replicator = HistoricalCrisisReplicator(random_state=42)
        
        result = replicator.replicate_crisis("cambridge_analytica_2018")
        
        assert result['regulatory_response_delay_days'] < 60
        assert 'Privacy' in str(result['historical_lessons']) or 'privacy' in str(result['historical_lessons'])
    
    def test_adaptation_factor(self):
        """Test crisis adaptation factor"""
        replicator = HistoricalCrisisReplicator(random_state=42)
        
        result_normal = replicator.replicate_crisis("2008_financial_crisis", adaptation_factor=1.0)
        result_adapted = replicator.replicate_crisis("2008_financial_crisis", adaptation_factor=1.5)
        
        assert result_adapted['enforcement_escalation_factor'] > result_normal['enforcement_escalation_factor']
        assert result_adapted['penalty_increase_factor'] > result_normal['penalty_increase_factor']
    
    def test_modern_applicability_score(self):
        """Test modern applicability scoring"""
        replicator = HistoricalCrisisReplicator(random_state=42)
        
        result = replicator.replicate_crisis("equifax_breach_2017")
        
        assert 'modern_applicability_score' in result
        assert 0 < result['modern_applicability_score'] <= 1.0
