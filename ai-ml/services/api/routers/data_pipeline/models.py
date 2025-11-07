"""Pydantic models for Data Pipeline API"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class FileFormat(str, Enum):
    """Supported file formats"""
    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"
    PARQUET = "parquet"


class ProcessingPriority(str, Enum):
    """Processing priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class JobStatus(str, Enum):
    """Job status types"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class UploadRequest(BaseModel):
    """Request model for file upload"""
    file_name: str = Field(..., description="Name of the file being uploaded")
    file_format: FileFormat = Field(..., description="Format of the file")
    description: Optional[str] = Field(default="", description="Description of the dataset")
    tags: List[str] = Field(default=[], description="Tags for categorizing the dataset")


class UploadResponse(BaseModel):
    """Response model for file upload"""
    upload_id: str = Field(..., description="Unique identifier for the upload")
    file_name: str = Field(..., description="Name of the uploaded file")
    file_size: int = Field(..., description="Size of the uploaded file in bytes")
    upload_time: datetime = Field(..., description="Timestamp of upload")
    status: str = Field(..., description="Status of the upload")


class BatchProcessRequest(BaseModel):
    """Request model for batch processing"""
    upload_id: str = Field(..., description="ID of the uploaded file to process")
    pipeline_type: str = Field(..., description="Type of processing pipeline to use")
    priority: ProcessingPriority = Field(default=ProcessingPriority.NORMAL, description="Processing priority")
    configuration: Optional[Dict[str, Any]] = Field(default=None, description="Processing configuration parameters")


class BatchProcessResponse(BaseModel):
    """Response model for batch processing"""
    job_id: str = Field(..., description="Unique identifier for the processing job")
    upload_id: str = Field(..., description="ID of the uploaded file")
    status: JobStatus = Field(..., description="Current status of the job")
    created_at: datetime = Field(..., description="Timestamp when job was created")
    estimated_completion_time: Optional[datetime] = Field(default=None, description="Estimated completion time")


class StreamDataRequest(BaseModel):
    """Request model for streaming data"""
    stream_id: str = Field(..., description="Unique identifier for the stream")
    data: Dict[str, Any] = Field(..., description="Data to be streamed")
    batch_size: int = Field(default=100, description="Number of records to process in each batch")


class ValidationRequest(BaseModel):
    """Request model for data validation"""
    upload_id: str = Field(..., description="ID of the uploaded file to validate")
    validation_rules: List[str] = Field(..., description="List of validation rules to apply")
    sample_size: Optional[int] = Field(default=None, description="Sample size for validation")


class ValidationResponse(BaseModel):
    """Response model for data validation"""
    validation_id: str = Field(..., description="Unique identifier for the validation")
    upload_id: str = Field(..., description="ID of the uploaded file")
    passed: bool = Field(..., description="Whether validation passed")
    errors: List[str] = Field(..., description="List of validation errors")
    warnings: List[str] = Field(..., description="List of validation warnings")
    validation_time: datetime = Field(..., description="Timestamp when validation completed")


class JobStatusResponse(BaseModel):
    """Response model for job status"""
    job_id: str = Field(..., description="Unique identifier for the job")
    status: JobStatus = Field(..., description="Current status of the job")
    progress: float = Field(..., description="Progress percentage (0-100)")
    stage: str = Field(..., description="Current processing stage")
    created_at: datetime = Field(..., description="Timestamp when job was created")
    started_at: Optional[datetime] = Field(default=None, description="Timestamp when job started")
    completed_at: Optional[datetime] = Field(default=None, description="Timestamp when job completed")
    estimated_completion_time: Optional[datetime] = Field(default=None, description="Estimated completion time")


class ProgressResponse(BaseModel):
    """Response model for progress monitoring"""
    job_id: str = Field(..., description="Unique identifier for the job")
    progress: float = Field(..., description="Progress percentage (0-100)")
    current_stage: str = Field(..., description="Current processing stage")
    records_processed: int = Field(..., description="Number of records processed")
    total_records: int = Field(..., description="Total number of records")
    throughput: float = Field(..., description="Processing throughput (records/second)")
    eta: Optional[datetime] = Field(default=None, description="Estimated time of arrival")


class ErrorReport(BaseModel):
    """Model for error reporting"""
    error_id: str = Field(..., description="Unique identifier for the error")
    job_id: str = Field(..., description="ID of the job that generated the error")
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Detailed error message")
    timestamp: datetime = Field(..., description="Timestamp when error occurred")
    stack_trace: Optional[str] = Field(default=None, description="Stack trace for debugging")
    recovery_suggestion: Optional[str] = Field(default=None, description="Suggested recovery action")


class RetryRequest(BaseModel):
    """Request model for retry mechanism"""
    job_id: str = Field(..., description="ID of the job to retry")
    retry_all: bool = Field(default=False, description="Whether to retry all failed stages")
    stages: List[str] = Field(default=[], description="Specific stages to retry")


class RetryResponse(BaseModel):
    """Response model for retry mechanism"""
    retry_job_id: str = Field(..., description="ID of the new retry job")
    original_job_id: str = Field(..., description="ID of the original job")
    status: JobStatus = Field(..., description="Status of the retry job")
    created_at: datetime = Field(..., description="Timestamp when retry job was created")


class ResultsStorageRequest(BaseModel):
    """Request model for results storage"""
    job_id: str = Field(..., description="ID of the job whose results to store")
    format: FileFormat = Field(default=FileFormat.JSON, description="Format to store results in")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata to associate with results")


class ResultsStorageResponse(BaseModel):
    """Response model for results storage"""
    result_id: str = Field(..., description="Unique identifier for the stored results")
    job_id: str = Field(..., description="ID of the job")
    storage_path: str = Field(..., description="Path where results are stored")
    format: FileFormat = Field(..., description="Format of stored results")
    size: int = Field(..., description="Size of stored results in bytes")
    stored_at: datetime = Field(..., description="Timestamp when results were stored")


class ResultsRetrievalResponse(BaseModel):
    """Response model for results retrieval"""
    result_id: str = Field(..., description="ID of the results")
    job_id: str = Field(..., description="ID of the job")
    data: Union[List[Dict[str, Any]], Dict[str, Any]] = Field(..., description="Results data")
    format: FileFormat = Field(..., description="Format of results")
    retrieved_at: datetime = Field(..., description="Timestamp when results were retrieved")


class ResultsFilterRequest(BaseModel):
    """Request model for filtering results"""
    job_id: Optional[str] = Field(default=None, description="Filter by job ID")
    status: Optional[JobStatus] = Field(default=None, description="Filter by job status")
    date_from: Optional[datetime] = Field(default=None, description="Filter by date range start")
    date_to: Optional[datetime] = Field(default=None, description="Filter by date range end")
    tags: List[str] = Field(default=[], description="Filter by tags")
    page: int = Field(default=1, description="Page number")
    page_size: int = Field(default=10, description="Number of results per page")