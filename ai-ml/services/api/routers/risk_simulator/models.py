"""Pydantic models for Risk Simulation API"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SimulationSetupRequest(BaseModel):
    """Request model for simulation setup"""
    name: str = Field(..., description="Name of the simulation")
    description: str = Field(default="", description="Description of the simulation")
    model_parameters: Dict[str, Any] = Field(..., description="Model parameters for the simulation")
    scenario_id: str = Field(..., description="ID of the risk scenario to simulate")
    simulation_type: str = Field(default="monte_carlo", description="Type of simulation (monte_carlo, bayesian, stress_test)")
    iterations: int = Field(default=1000, description="Number of simulation iterations")
    time_horizon: int = Field(default=365, description="Time horizon in days")


class SimulationSetupResponse(BaseModel):
    """Response model for simulation setup"""
    simulation_id: str = Field(..., description="Unique identifier for the simulation")
    name: str = Field(..., description="Name of the simulation")
    status: str = Field(..., description="Status of the simulation (pending, configured, running, completed, failed)")
    created_at: str = Field(..., description="Timestamp when simulation was created")


class SimulationExecutionRequest(BaseModel):
    """Request model for simulation execution"""
    simulation_id: str = Field(..., description="ID of the simulation to execute")
    execution_parameters: Optional[Dict[str, Any]] = Field(default=None, description="Additional execution parameters")


class SimulationExecutionResponse(BaseModel):
    """Response model for simulation execution"""
    job_id: str = Field(..., description="Unique identifier for the execution job")
    simulation_id: str = Field(..., description="ID of the simulation being executed")
    status: str = Field(..., description="Status of the execution (pending, running, completed, failed)")
    started_at: str = Field(..., description="Timestamp when execution started")


class SimulationResult(BaseModel):
    """Model for individual simulation results"""
    timestamp: str = Field(..., description="Timestamp of the result")
    value: float = Field(..., description="Simulated value")
    confidence_interval: List[float] = Field(..., description="Confidence interval [lower, upper]")
    risk_metrics: Dict[str, float] = Field(..., description="Risk metrics at this timestamp")


class SimulationResultsResponse(BaseModel):
    """Response model for simulation results"""
    job_id: str = Field(..., description="ID of the execution job")
    simulation_id: str = Field(..., description="ID of the simulation")
    results: List[SimulationResult] = Field(..., description="List of simulation results")
    summary_statistics: Dict[str, float] = Field(..., description="Summary statistics of the simulation")
    completion_time: str = Field(..., description="Timestamp when simulation completed")


class ScenarioListResponse(BaseModel):
    """Response model for scenario listing"""
    scenarios: List[Dict[str, Any]] = Field(..., description="List of available scenarios")
    total_scenarios: int = Field(..., description="Total number of scenarios")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of scenarios per page")


class ScenarioCreateRequest(BaseModel):
    """Request model for scenario creation"""
    name: str = Field(..., description="Name of the scenario")
    description: str = Field(default="", description="Description of the scenario")
    parameters: Dict[str, Any] = Field(..., description="Scenario parameters")
    risk_factors: List[str] = Field(..., description="Risk factors in this scenario")


class ScenarioCreateResponse(BaseModel):
    """Response model for scenario creation"""
    scenario_id: str = Field(..., description="Unique identifier for the scenario")
    name: str = Field(..., description="Name of the scenario")
    status: str = Field(..., description="Status of scenario creation")
    created_at: str = Field(..., description="Timestamp when scenario was created")