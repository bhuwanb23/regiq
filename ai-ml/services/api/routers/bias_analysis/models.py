"""Pydantic models for Bias Analysis API"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ModelUploadRequest(BaseModel):
    """Request model for model upload"""
    model_name: str = Field(..., description="Name of the model")
    description: str = Field(default="", description="Description of the model")
    target_variable: str = Field(..., description="Target variable for the model")
    protected_attributes: List[str] = Field(..., description="Protected attributes for bias analysis")


class ModelMetadataResponse(BaseModel):
    """Response model for model metadata"""
    model_id: str = Field(..., description="Unique identifier for the model")
    name: str = Field(..., description="Name of the model")
    model_type: str = Field(..., description="Type of model (sklearn, pytorch, onnx, etc.)")
    framework: str = Field(..., description="Framework used (sklearn, pytorch, tensorflow, etc.)")
    version: str = Field(..., description="Model version")
    upload_date: str = Field(..., description="Date when model was uploaded")
    file_size: int = Field(..., description="Size of the model file in bytes")
    description: str = Field(..., description="Description of the model")
    target_variable: str = Field(..., description="Target variable for the model")
    feature_columns: List[str] = Field(..., description="Feature columns used in the model")
    protected_attributes: List[str] = Field(..., description="Protected attributes for bias analysis")
    training_data_size: int = Field(..., description="Size of training data")
    performance_metrics: Dict[str, float] = Field(..., description="Performance metrics of the model")
    bias_analysis_status: str = Field(..., description="Status of bias analysis (pending, in_progress, completed, failed)")


class AnalysisTriggerRequest(BaseModel):
    """Request model for triggering bias analysis"""
    model_id: str = Field(..., description="ID of the model to analyze")
    analysis_parameters: Optional[Dict[str, Any]] = Field(default=None, description="Parameters for bias analysis")


class AnalysisJobResponse(BaseModel):
    """Response model for analysis job"""
    analysis_id: str = Field(..., description="Unique identifier for the analysis")
    model_id: str = Field(..., description="ID of the model being analyzed")
    status: str = Field(..., description="Status of the analysis (pending, in_progress, completed, failed)")
    created_at: str = Field(..., description="Timestamp when analysis was triggered")
    started_at: Optional[str] = Field(default=None, description="Timestamp when analysis started")
    completed_at: Optional[str] = Field(default=None, description="Timestamp when analysis completed")


class BiasMetricsResponse(BaseModel):
    """Response model for bias metrics"""
    analysis_id: str = Field(..., description="ID of the analysis")
    demographic_parity_difference: float = Field(..., description="Demographic parity difference")
    equal_opportunity_difference: float = Field(..., description="Equal opportunity difference")
    disparate_impact: float = Field(..., description="Disparate impact ratio")
    statistical_parity_difference: float = Field(..., description="Statistical parity difference")
    consistency_score: float = Field(..., description="Model consistency score")
    feature_importance_bias: Dict[str, float] = Field(..., description="Bias in feature importance")
    group_metrics: Dict[str, Dict[str, float]] = Field(..., description="Metrics by protected groups")


class ReportGenerationRequest(BaseModel):
    """Request model for report generation"""
    analysis_id: str = Field(..., description="ID of the analysis to generate report for")
    report_type: str = Field(default="executive", description="Type of report (executive, technical, detailed)")
    format: str = Field(default="pdf", description="Format of the report (pdf, html, json)")


class ReportGenerationResponse(BaseModel):
    """Response model for report generation"""
    report_id: str = Field(..., description="Unique identifier for the report")
    analysis_id: str = Field(..., description="ID of the analysis")
    status: str = Field(..., description="Status of report generation (pending, in_progress, completed, failed)")
    created_at: str = Field(..., description="Timestamp when report generation was triggered")
    format: str = Field(..., description="Format of the report")