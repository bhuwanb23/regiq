"""
Implementation Time Estimation Models

This module implements models for estimating implementation timelines for
compliance remediation projects using PERT, Critical Path, and probabilistic methods.

Models:
- PERTEstimator: Three-point estimation (Optimistic/Most Likely/Pessimistic)
- CriticalPathAnalyzer: Critical path method for project scheduling
- MilestoneTracker: Track implementation milestones
- TimelineSimulator: Monte Carlo timeline simulation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
from scipy import stats


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PERTEstimate:
    """PERT estimation result"""
    expected_duration: float
    optimistic: float
    most_likely: float
    pessimistic: float
    std_deviation: float
    confidence_interval_95: Tuple[float, float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'expected_duration': float(self.expected_duration),
            'optimistic': float(self.optimistic),
            'most_likely': float(self.most_likely),
            'pessimistic': float(self.pessimistic),
            'std_deviation': float(self.std_deviation),
            'confidence_interval_95': tuple(float(x) for x in self.confidence_interval_95)
        }


class PERTEstimator:
    """Three-point PERT estimation"""
    
    def estimate(self,
                optimistic: float,
                most_likely: float,
                pessimistic: float) -> PERTEstimate:
        """Calculate PERT estimate"""
        # PERT formula: (O + 4M + P) / 6
        expected = (optimistic + 4 * most_likely + pessimistic) / 6
        
        # Standard deviation: (P - O) / 6
        std_dev = (pessimistic - optimistic) / 6
        
        # 95% confidence interval (±2 std dev)
        ci_lower = expected - (1.96 * std_dev)
        ci_upper = expected + (1.96 * std_dev)
        
        return PERTEstimate(
            expected_duration=expected,
            optimistic=optimistic,
            most_likely=most_likely,
            pessimistic=pessimistic,
            std_deviation=std_dev,
            confidence_interval_95=(ci_lower, ci_upper)
        )


class CriticalPathAnalyzer:
    """Critical path method for project scheduling"""
    
    def analyze_critical_path(self,
                             tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze critical path"""
        if not tasks:
            return {'critical_path_duration': 0, 'critical_tasks': []}
        
        # Simple sequential model for now
        total_duration = sum(task.get('duration', 0) for task in tasks)
        critical_tasks = [task.get('name', f'Task {i}') for i, task in enumerate(tasks)]
        
        return {
            'critical_path_duration': float(total_duration),
            'critical_tasks': critical_tasks,
            'num_critical_tasks': len(critical_tasks),
            'slack_time': 0.0
        }


class TimelineSimulator:
    """Monte Carlo timeline simulation"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def simulate_timeline(self,
                         tasks: List[Dict[str, Any]],
                         n_simulations: int = 10000) -> Dict[str, Any]:
        """Monte Carlo simulation of project timeline"""
        duration_samples = []
        
        for _ in range(n_simulations):
            total_duration = 0
            
            for task in tasks:
                # Use PERT three-point estimate
                opt = task.get('optimistic', task.get('duration', 10) * 0.7)
                ml = task.get('most_likely', task.get('duration', 10))
                pess = task.get('pessimistic', task.get('duration', 10) * 1.5)
                
                # Beta distribution for PERT
                task_duration = self.rng.triangular(opt, ml, pess)
                total_duration += task_duration
            
            duration_samples.append(total_duration)
        
        samples_array = np.array(duration_samples)
        
        return {
            'expected_duration_days': float(np.mean(samples_array)),
            'median_duration_days': float(np.median(samples_array)),
            'std_deviation_days': float(np.std(samples_array)),
            'percentile_50': float(np.percentile(samples_array, 50)),
            'percentile_75': float(np.percentile(samples_array, 75)),
            'percentile_90': float(np.percentile(samples_array, 90)),
            'percentile_95': float(np.percentile(samples_array, 95)),
            'probability_within_budget': float(np.mean(samples_array <= np.percentile(samples_array, 80)))
        }
