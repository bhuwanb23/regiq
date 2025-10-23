"""
Tests for implementation_time.py

Tests implementation time estimation models including PERT,
critical path analysis, and Monte Carlo timeline simulation.
"""

import pytest
import numpy as np
from services.risk_simulator.models.implementation_time import (
    PERTEstimator,
    CriticalPathAnalyzer,
    TimelineSimulator,
    TaskPriority,
    PERTEstimate
)


class TestPERTEstimator:
    """Test PERT estimator"""
    
    def test_initialization(self):
        """Test estimator initialization"""
        estimator = PERTEstimator()
        assert estimator is not None
    
    def test_estimate_basic(self):
        """Test basic PERT estimation"""
        estimator = PERTEstimator()
        
        result = estimator.estimate(
            optimistic=10.0,
            most_likely=15.0,
            pessimistic=25.0
        )
        
        assert isinstance(result, PERTEstimate)
        assert result.optimistic == 10.0
        assert result.most_likely == 15.0
        assert result.pessimistic == 25.0
        assert result.expected_duration > 0
        assert result.std_deviation > 0
    
    def test_estimate_expected_duration_calculation(self):
        """Test expected duration formula: (O + 4M + P) / 6"""
        estimator = PERTEstimator()
        
        opt, ml, pess = 10.0, 15.0, 20.0
        result = estimator.estimate(opt, ml, pess)
        
        expected = (opt + 4 * ml + pess) / 6
        assert abs(result.expected_duration - expected) < 0.01
    
    def test_estimate_std_deviation_calculation(self):
        """Test std deviation formula: (P - O) / 6"""
        estimator = PERTEstimator()
        
        opt, ml, pess = 10.0, 15.0, 30.0
        result = estimator.estimate(opt, ml, pess)
        
        expected_std = (pess - opt) / 6
        assert abs(result.std_deviation - expected_std) < 0.01
    
    def test_estimate_confidence_interval(self):
        """Test 95% confidence interval calculation"""
        estimator = PERTEstimator()
        
        result = estimator.estimate(
            optimistic=10.0,
            most_likely=15.0,
            pessimistic=25.0
        )
        
        ci_lower, ci_upper = result.confidence_interval_95
        
        # CI should bracket expected duration
        assert ci_lower < result.expected_duration < ci_upper
        
        # CI width should be ~4 std deviations (±1.96)
        expected_width = 2 * 1.96 * result.std_deviation
        actual_width = ci_upper - ci_lower
        assert abs(actual_width - expected_width) < 0.1
    
    def test_estimate_zero_variance(self):
        """Test PERT estimate with zero variance (all same)"""
        estimator = PERTEstimator()
        
        result = estimator.estimate(
            optimistic=15.0,
            most_likely=15.0,
            pessimistic=15.0
        )
        
        assert result.expected_duration == 15.0
        assert result.std_deviation == 0.0
    
    def test_to_dict_serialization(self):
        """Test PERTEstimate serialization"""
        estimator = PERTEstimator()
        
        result = estimator.estimate(
            optimistic=10.0,
            most_likely=15.0,
            pessimistic=25.0
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert 'expected_duration' in result_dict
        assert 'std_deviation' in result_dict
        assert 'confidence_interval_95' in result_dict
        
        # Test JSON serialization
        import json
        json.dumps(result_dict)


class TestCriticalPathAnalyzer:
    """Test critical path analyzer"""
    
    def test_initialization(self):
        """Test analyzer initialization"""
        analyzer = CriticalPathAnalyzer()
        assert analyzer is not None
    
    def test_analyze_critical_path_basic(self):
        """Test basic critical path analysis"""
        analyzer = CriticalPathAnalyzer()
        
        tasks = [
            {'name': 'Task 1', 'duration': 10.0},
            {'name': 'Task 2', 'duration': 15.0},
            {'name': 'Task 3', 'duration': 8.0}
        ]
        
        result = analyzer.analyze_critical_path(tasks)
        
        assert isinstance(result, dict)
        assert 'critical_path_duration' in result
        assert 'critical_tasks' in result
        assert 'num_critical_tasks' in result
    
    def test_analyze_critical_path_duration_sum(self):
        """Test critical path duration is sum of tasks"""
        analyzer = CriticalPathAnalyzer()
        
        tasks = [
            {'name': 'Design', 'duration': 20.0},
            {'name': 'Development', 'duration': 60.0},
            {'name': 'Testing', 'duration': 30.0}
        ]
        
        result = analyzer.analyze_critical_path(tasks)
        
        expected_duration = sum(t['duration'] for t in tasks)
        assert result['critical_path_duration'] == expected_duration
    
    def test_analyze_critical_path_empty_tasks(self):
        """Test critical path with no tasks"""
        analyzer = CriticalPathAnalyzer()
        
        result = analyzer.analyze_critical_path([])
        
        assert result['critical_path_duration'] == 0
        assert result['critical_tasks'] == []
    
    def test_analyze_critical_path_task_names(self):
        """Test critical tasks include all task names"""
        analyzer = CriticalPathAnalyzer()
        
        tasks = [
            {'name': 'Planning', 'duration': 10.0},
            {'name': 'Execution', 'duration': 20.0}
        ]
        
        result = analyzer.analyze_critical_path(tasks)
        
        assert 'Planning' in result['critical_tasks']
        assert 'Execution' in result['critical_tasks']
        assert result['num_critical_tasks'] == 2


class TestTimelineSimulator:
    """Test Monte Carlo timeline simulator"""
    
    def test_initialization(self):
        """Test simulator initialization"""
        simulator = TimelineSimulator(random_state=42)
        assert simulator is not None
        assert simulator.random_state == 42
    
    def test_simulate_timeline_basic(self):
        """Test basic timeline simulation"""
        simulator = TimelineSimulator(random_state=42)
        
        tasks = [
            {'duration': 10.0, 'optimistic': 8.0, 'most_likely': 10.0, 'pessimistic': 15.0},
            {'duration': 20.0, 'optimistic': 15.0, 'most_likely': 20.0, 'pessimistic': 30.0}
        ]
        
        result = simulator.simulate_timeline(tasks, n_simulations=1000)
        
        assert isinstance(result, dict)
        assert 'expected_duration_days' in result
        assert 'median_duration_days' in result
        assert 'std_deviation_days' in result
    
    def test_simulate_timeline_percentiles(self):
        """Test percentile calculations"""
        simulator = TimelineSimulator(random_state=42)
        
        tasks = [
            {'duration': 10.0, 'optimistic': 8.0, 'most_likely': 10.0, 'pessimistic': 15.0}
        ]
        
        result = simulator.simulate_timeline(tasks, n_simulations=5000)
        
        # Check percentiles are in ascending order
        assert result['percentile_50'] <= result['percentile_75']
        assert result['percentile_75'] <= result['percentile_90']
        assert result['percentile_90'] <= result['percentile_95']
    
    def test_simulate_timeline_median_vs_p50(self):
        """Test median equals 50th percentile"""
        simulator = TimelineSimulator(random_state=42)
        
        tasks = [
            {'duration': 15.0}
        ]
        
        result = simulator.simulate_timeline(tasks, n_simulations=10000)
        
        # Median should equal P50 (within tolerance)
        assert abs(result['median_duration_days'] - result['percentile_50']) < 0.1
    
    def test_simulate_timeline_multiple_tasks(self):
        """Test simulation with multiple tasks"""
        simulator = TimelineSimulator(random_state=42)
        
        tasks = [
            {'duration': 10.0, 'optimistic': 8.0, 'most_likely': 10.0, 'pessimistic': 15.0},
            {'duration': 15.0, 'optimistic': 12.0, 'most_likely': 15.0, 'pessimistic': 20.0},
            {'duration': 20.0, 'optimistic': 18.0, 'most_likely': 20.0, 'pessimistic': 25.0}
        ]
        
        result = simulator.simulate_timeline(tasks, n_simulations=5000)
        
        # Expected duration should be around sum of most likely
        expected_approx = sum(t['most_likely'] for t in tasks)
        assert result['expected_duration_days'] > 0
        assert result['expected_duration_days'] < expected_approx * 2
    
    def test_simulate_timeline_reproducibility(self):
        """Test simulation reproducibility with same random state"""
        tasks = [
            {'duration': 10.0, 'optimistic': 8.0, 'most_likely': 10.0, 'pessimistic': 15.0}
        ]
        
        sim1 = TimelineSimulator(random_state=42)
        result1 = sim1.simulate_timeline(tasks, n_simulations=1000)
        
        sim2 = TimelineSimulator(random_state=42)
        result2 = sim2.simulate_timeline(tasks, n_simulations=1000)
        
        # Results should be identical with same random state
        assert abs(result1['expected_duration_days'] - result2['expected_duration_days']) < 0.01
    
    def test_simulate_timeline_json_serialization(self):
        """Test timeline simulation result JSON serialization"""
        simulator = TimelineSimulator(random_state=42)
        
        tasks = [
            {'duration': 10.0}
        ]
        
        result = simulator.simulate_timeline(tasks, n_simulations=1000)
        
        # Test JSON serialization
        import json
        json.dumps(result)
    
    def test_simulate_timeline_probability_within_budget(self):
        """Test probability within budget calculation"""
        simulator = TimelineSimulator(random_state=42)
        
        tasks = [
            {'duration': 10.0, 'optimistic': 8.0, 'most_likely': 10.0, 'pessimistic': 15.0}
        ]
        
        result = simulator.simulate_timeline(tasks, n_simulations=10000)
        
        # Probability should be between 0 and 1
        assert 0 <= result['probability_within_budget'] <= 1
