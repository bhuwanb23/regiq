"""
Capacity Constraints Models

This module implements models for analyzing and managing capacity constraints
in compliance operations, including queue theory, resource allocation, and
bottleneck analysis.

Models:
- QueueTheoryModel: Queue analysis for compliance workloads
- BottleneckAnalyzer: Identify and analyze bottlenecks
- ResourceAllocationOptimizer: Optimize resource allocation
- CapacityPlanningModel: Integrated capacity planning
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from scipy import stats


@dataclass
class QueueAnalysis:
    """Queue theory analysis result"""
    avg_queue_length: float
    avg_wait_time: float
    system_utilization: float
    service_level_pct: float
    capacity_sufficient: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'avg_queue_length': float(self.avg_queue_length),
            'avg_wait_time': float(self.avg_wait_time),
            'system_utilization': float(self.system_utilization),
            'service_level_pct': float(self.service_level_pct),
            'capacity_sufficient': bool(self.capacity_sufficient)
        }


class QueueTheoryModel:
    """Queue theory for compliance workload analysis"""
    
    def analyze_mm1_queue(self,
                         arrival_rate: float,
                         service_rate: float) -> QueueAnalysis:
        """Analyze M/M/1 queue (single server)"""
        # Utilization
        rho = arrival_rate / service_rate
        
        if rho >= 1:
            # System is unstable
            return QueueAnalysis(
                avg_queue_length=float('inf'),
                avg_wait_time=float('inf'),
                system_utilization=rho,
                service_level_pct=0.0,
                capacity_sufficient=False
            )
        
        # Average queue length
        avg_queue = rho / (1 - rho)
        
        # Average wait time
        avg_wait = 1 / (service_rate - arrival_rate)
        
        # Service level (% served within threshold)
        service_level = (1 - rho) * 100
        
        return QueueAnalysis(
            avg_queue_length=avg_queue,
            avg_wait_time=avg_wait,
            system_utilization=rho,
            service_level_pct=service_level,
            capacity_sufficient=rho < 0.85
        )


class BottleneckAnalyzer:
    """Identify and analyze system bottlenecks"""
    
    def identify_bottlenecks(self,
                            processes: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Identify bottlenecks in process chain"""
        bottlenecks = []
        
        for name, metrics in processes.items():
            capacity = metrics.get('capacity', 100)
            demand = metrics.get('demand', 50)
            utilization = demand / capacity if capacity > 0 else 1.0
            
            if utilization > 0.85:
                bottlenecks.append({
                    'process': name,
                    'utilization': float(utilization),
                    'capacity': float(capacity),
                    'demand': float(demand),
                    'shortfall': float(max(0, demand - capacity * 0.85))
                })
        
        return {
            'bottlenecks': bottlenecks,
            'num_bottlenecks': len(bottlenecks),
            'system_constrained': len(bottlenecks) > 0
        }


class CapacityPlanningModel:
    """Integrated capacity planning"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.queue_model = QueueTheoryModel()
        self.bottleneck_analyzer = BottleneckAnalyzer()
    
    def plan_capacity(self,
                     current_capacity: float,
                     projected_demand: float,
                     growth_rate: float,
                     planning_horizon_years: int = 3) -> Dict[str, Any]:
        """Create capacity plan"""
        capacity_plan = []
        
        for year in range(planning_horizon_years):
            year_demand = projected_demand * ((1 + growth_rate) ** year)
            utilization = year_demand / current_capacity
            
            capacity_plan.append({
                'year': year + 1,
                'projected_demand': float(year_demand),
                'capacity': float(current_capacity),
                'utilization_pct': float(utilization * 100),
                'capacity_gap': float(max(0, year_demand - current_capacity * 0.85)),
                'expansion_needed': bool(utilization > 0.85)
            })
        
        return {
            'capacity_plan': capacity_plan,
            'requires_expansion': any(y['expansion_needed'] for y in capacity_plan),
            'planning_horizon_years': planning_horizon_years
        }
