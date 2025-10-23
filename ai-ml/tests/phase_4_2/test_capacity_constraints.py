"""
Tests for capacity_constraints.py

Tests capacity constraint models including queue theory,
bottleneck analysis, and capacity planning.
"""

import pytest
import numpy as np
from services.risk_simulator.models.capacity_constraints import (
    QueueTheoryModel,
    BottleneckAnalyzer,
    CapacityPlanningModel,
    QueueAnalysis
)


class TestQueueTheoryModel:
    """Test queue theory model"""
    
    def test_initialization(self):
        """Test model initialization"""
        model = QueueTheoryModel()
        assert model is not None
    
    def test_analyze_mm1_queue_stable(self):
        """Test M/M/1 queue analysis with stable system"""
        model = QueueTheoryModel()
        
        # Arrival rate < service rate (stable)
        result = model.analyze_mm1_queue(
            arrival_rate=5.0,
            service_rate=10.0
        )
        
        assert isinstance(result, QueueAnalysis)
        assert result.system_utilization < 1.0
        assert result.avg_queue_length >= 0
        assert result.avg_wait_time >= 0
        assert result.capacity_sufficient is True
    
    def test_analyze_mm1_queue_high_utilization(self):
        """Test M/M/1 queue with high utilization"""
        model = QueueTheoryModel()
        
        # High utilization (90%)
        result = model.analyze_mm1_queue(
            arrival_rate=9.0,
            service_rate=10.0
        )
        
        assert result.system_utilization == 0.9
        assert result.avg_queue_length > 5  # Long queues at high utilization
        assert result.capacity_sufficient is False  # Above 85% threshold
    
    def test_analyze_mm1_queue_unstable(self):
        """Test M/M/1 queue with unstable system"""
        model = QueueTheoryModel()
        
        # Arrival rate >= service rate (unstable)
        result = model.analyze_mm1_queue(
            arrival_rate=10.0,
            service_rate=10.0
        )
        
        assert result.system_utilization >= 1.0
        assert result.avg_queue_length == float('inf')
        assert result.avg_wait_time == float('inf')
        assert result.capacity_sufficient is False
    
    def test_analyze_mm1_queue_overloaded(self):
        """Test M/M/1 queue with demand exceeding capacity"""
        model = QueueTheoryModel()
        
        result = model.analyze_mm1_queue(
            arrival_rate=15.0,
            service_rate=10.0
        )
        
        assert result.system_utilization > 1.0
        assert result.capacity_sufficient is False
    
    def test_analyze_mm1_queue_low_utilization(self):
        """Test M/M/1 queue with low utilization"""
        model = QueueTheoryModel()
        
        result = model.analyze_mm1_queue(
            arrival_rate=2.0,
            service_rate=10.0
        )
        
        assert result.system_utilization == 0.2
        assert result.capacity_sufficient is True
        assert result.service_level_pct > 70
    
    def test_queue_analysis_utilization_calculation(self):
        """Test utilization (rho) = arrival_rate / service_rate"""
        model = QueueTheoryModel()
        
        arrival = 6.0
        service = 12.0
        result = model.analyze_mm1_queue(arrival, service)
        
        expected_rho = arrival / service
        assert result.system_utilization == expected_rho
    
    def test_to_dict_serialization(self):
        """Test QueueAnalysis serialization"""
        model = QueueTheoryModel()
        
        result = model.analyze_mm1_queue(
            arrival_rate=5.0,
            service_rate=10.0
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert 'avg_queue_length' in result_dict
        assert 'avg_wait_time' in result_dict
        assert 'system_utilization' in result_dict
        assert 'capacity_sufficient' in result_dict
        
        # Test JSON serialization
        import json
        json.dumps(result_dict)


class TestBottleneckAnalyzer:
    """Test bottleneck analyzer"""
    
    def test_initialization(self):
        """Test analyzer initialization"""
        analyzer = BottleneckAnalyzer()
        assert analyzer is not None
    
    def test_identify_bottlenecks_none(self):
        """Test bottleneck identification with no bottlenecks"""
        analyzer = BottleneckAnalyzer()
        
        processes = {
            'process1': {'capacity': 100.0, 'demand': 50.0},
            'process2': {'capacity': 200.0, 'demand': 100.0}
        }
        
        result = analyzer.identify_bottlenecks(processes)
        
        assert isinstance(result, dict)
        assert result['num_bottlenecks'] == 0
        assert result['system_constrained'] is False
    
    def test_identify_bottlenecks_single(self):
        """Test identification of single bottleneck"""
        analyzer = BottleneckAnalyzer()
        
        processes = {
            'process1': {'capacity': 100.0, 'demand': 50.0},
            'process2': {'capacity': 100.0, 'demand': 95.0}  # 95% utilization
        }
        
        result = analyzer.identify_bottlenecks(processes)
        
        assert result['num_bottlenecks'] == 1
        assert result['system_constrained'] is True
        assert len(result['bottlenecks']) == 1
        assert result['bottlenecks'][0]['process'] == 'process2'
    
    def test_identify_bottlenecks_multiple(self):
        """Test identification of multiple bottlenecks"""
        analyzer = BottleneckAnalyzer()
        
        processes = {
            'process1': {'capacity': 100.0, 'demand': 90.0},  # Bottleneck
            'process2': {'capacity': 100.0, 'demand': 50.0},  # OK
            'process3': {'capacity': 100.0, 'demand': 95.0}   # Bottleneck
        }
        
        result = analyzer.identify_bottlenecks(processes)
        
        assert result['num_bottlenecks'] == 2
        assert result['system_constrained'] is True
    
    def test_identify_bottlenecks_threshold(self):
        """Test 85% utilization threshold for bottlenecks"""
        analyzer = BottleneckAnalyzer()
        
        processes = {
            'at_threshold': {'capacity': 100.0, 'demand': 85.0},     # Exactly 85%
            'above_threshold': {'capacity': 100.0, 'demand': 86.0},  # Above 85%
            'below_threshold': {'capacity': 100.0, 'demand': 84.0}   # Below 85%
        }
        
        result = analyzer.identify_bottlenecks(processes)
        
        # At or below 85% should not be bottleneck
        bottleneck_names = [b['process'] for b in result['bottlenecks']]
        assert 'above_threshold' in bottleneck_names
        assert 'at_threshold' not in bottleneck_names
        assert 'below_threshold' not in bottleneck_names
    
    def test_identify_bottlenecks_shortfall_calculation(self):
        """Test shortfall calculation for bottlenecks"""
        analyzer = BottleneckAnalyzer()
        
        capacity = 100.0
        demand = 95.0
        processes = {
            'process1': {'capacity': capacity, 'demand': demand}
        }
        
        result = analyzer.identify_bottlenecks(processes)
        
        # Shortfall = demand - (capacity * 0.85)
        expected_shortfall = max(0, demand - capacity * 0.85)
        assert result['bottlenecks'][0]['shortfall'] == expected_shortfall
    
    def test_identify_bottlenecks_zero_capacity(self):
        """Test bottleneck with zero capacity"""
        analyzer = BottleneckAnalyzer()
        
        processes = {
            'zero_capacity': {'capacity': 0.0, 'demand': 50.0}
        }
        
        result = analyzer.identify_bottlenecks(processes)
        
        assert result['num_bottlenecks'] == 1
        assert result['bottlenecks'][0]['utilization'] == 1.0


class TestCapacityPlanningModel:
    """Test integrated capacity planning model"""
    
    def test_initialization(self):
        """Test planner initialization"""
        planner = CapacityPlanningModel(random_state=42)
        assert planner is not None
        assert isinstance(planner.queue_model, QueueTheoryModel)
        assert isinstance(planner.bottleneck_analyzer, BottleneckAnalyzer)
    
    def test_plan_capacity_basic(self):
        """Test basic capacity planning"""
        planner = CapacityPlanningModel(random_state=42)
        
        result = planner.plan_capacity(
            current_capacity=100.0,
            projected_demand=80.0,
            growth_rate=0.1,
            planning_horizon_years=3
        )
        
        assert isinstance(result, dict)
        assert 'capacity_plan' in result
        assert 'requires_expansion' in result
        assert len(result['capacity_plan']) == 3
    
    def test_plan_capacity_growth_projection(self):
        """Test demand growth projection over years"""
        planner = CapacityPlanningModel(random_state=42)
        
        initial_demand = 50.0
        growth_rate = 0.2
        
        result = planner.plan_capacity(
            current_capacity=100.0,
            projected_demand=initial_demand,
            growth_rate=growth_rate,
            planning_horizon_years=3
        )
        
        # Check year-over-year growth
        plan = result['capacity_plan']
        for year_data in plan:
            year = year_data['year']
            expected_demand = initial_demand * ((1 + growth_rate) ** (year - 1))
            assert abs(year_data['projected_demand'] - expected_demand) < 0.01
    
    def test_plan_capacity_expansion_needed(self):
        """Test capacity expansion detection"""
        planner = CapacityPlanningModel(random_state=42)
        
        # High growth will exceed capacity
        result = planner.plan_capacity(
            current_capacity=100.0,
            projected_demand=80.0,
            growth_rate=0.2,
            planning_horizon_years=5
        )
        
        assert result['requires_expansion'] is True
        
        # Check some years need expansion
        expansion_years = [y for y in result['capacity_plan'] if y['expansion_needed']]
        assert len(expansion_years) > 0
    
    def test_plan_capacity_no_expansion_needed(self):
        """Test scenario with sufficient capacity"""
        planner = CapacityPlanningModel(random_state=42)
        
        # Low demand, no growth
        result = planner.plan_capacity(
            current_capacity=100.0,
            projected_demand=50.0,
            growth_rate=0.0,
            planning_horizon_years=3
        )
        
        assert result['requires_expansion'] is False
    
    def test_plan_capacity_utilization_calculation(self):
        """Test utilization percentage calculation"""
        planner = CapacityPlanningModel(random_state=42)
        
        capacity = 100.0
        demand = 75.0
        
        result = planner.plan_capacity(
            current_capacity=capacity,
            projected_demand=demand,
            growth_rate=0.0,
            planning_horizon_years=1
        )
        
        year1 = result['capacity_plan'][0]
        expected_utilization_pct = (demand / capacity) * 100
        assert abs(year1['utilization_pct'] - expected_utilization_pct) < 0.01
    
    def test_plan_capacity_gap_calculation(self):
        """Test capacity gap calculation"""
        planner = CapacityPlanningModel(random_state=42)
        
        capacity = 100.0
        demand = 95.0
        
        result = planner.plan_capacity(
            current_capacity=capacity,
            projected_demand=demand,
            growth_rate=0.0,
            planning_horizon_years=1
        )
        
        year1 = result['capacity_plan'][0]
        # Gap = max(0, demand - capacity * 0.85)
        expected_gap = max(0, demand - capacity * 0.85)
        assert abs(year1['capacity_gap'] - expected_gap) < 0.01
    
    def test_plan_capacity_json_serialization(self):
        """Test capacity plan JSON serialization"""
        planner = CapacityPlanningModel(random_state=42)
        
        result = planner.plan_capacity(
            current_capacity=100.0,
            projected_demand=80.0,
            growth_rate=0.1,
            planning_horizon_years=3
        )
        
        # Test JSON serialization
        import json
        json.dumps(result)
    
    def test_plan_capacity_extended_horizon(self):
        """Test planning with extended horizon"""
        planner = CapacityPlanningModel(random_state=42)
        
        result = planner.plan_capacity(
            current_capacity=100.0,
            projected_demand=50.0,
            growth_rate=0.15,
            planning_horizon_years=10
        )
        
        assert len(result['capacity_plan']) == 10
        assert result['capacity_plan'][-1]['year'] == 10
