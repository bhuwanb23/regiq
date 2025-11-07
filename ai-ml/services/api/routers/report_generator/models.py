"""Pydantic models for Report Generation API"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ReportCreateRequest(BaseModel):
    """Request model for report creation"""
    report_type: str = Field(..., description="Type of report (executive, technical, regulatory)")
    title: str = Field(..., description="Title of the report")
    content: Dict[str, Any] = Field(..., description="Content of the report")
    template_id: Optional[str] = Field(default=None, description="ID of the template to use")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Additional parameters for report generation")


class ReportCreateResponse(BaseModel):
    """Response model for report creation"""
    report_id: str = Field(..., description="Unique identifier for the report")
    report_type: str = Field(..., description="Type of report")
    title: str = Field(..., description="Title of the report")
    status: str = Field(..., description="Status of report generation (pending, in_progress, completed, failed)")
    created_at: str = Field(..., description="Timestamp when report was created")


class TemplateListResponse(BaseModel):
    """Response model for template listing"""
    templates: List[Dict[str, Any]] = Field(..., description="List of available templates")
    total_templates: int = Field(..., description="Total number of templates")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of templates per page")


class TemplateCreateRequest(BaseModel):
    """Request model for template creation"""
    name: str = Field(..., description="Name of the template")
    description: str = Field(default="", description="Description of the template")
    template_type: str = Field(..., description="Type of template (executive, technical, regulatory)")
    content: str = Field(..., description="Template content")
    variables: List[str] = Field(..., description="Variables used in the template")


class TemplateCreateResponse(BaseModel):
    """Response model for template creation"""
    template_id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Name of the template")
    template_type: str = Field(..., description="Type of template")
    status: str = Field(..., description="Status of template creation")
    created_at: str = Field(..., description="Timestamp when template was created")


class ExportRequest(BaseModel):
    """Request model for report export"""
    report_id: str = Field(..., description="ID of the report to export")
    format: str = Field(..., description="Format to export (pdf, csv, excel, html, json)")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Export options")


class ExportResponse(BaseModel):
    """Response model for report export"""
    export_id: str = Field(..., description="Unique identifier for the export")
    report_id: str = Field(..., description="ID of the report")
    format: str = Field(..., description="Export format")
    status: str = Field(..., description="Status of export (pending, in_progress, completed, failed)")
    download_url: Optional[str] = Field(default=None, description="URL to download the exported file")
    created_at: str = Field(..., description="Timestamp when export was requested")


class ReportStatusResponse(BaseModel):
    """Response model for report status"""
    report_id: str = Field(..., description="ID of the report")
    status: str = Field(..., description="Current status of the report")
    progress: float = Field(..., description="Progress percentage (0-100)")
    estimated_completion_time: Optional[str] = Field(default=None, description="Estimated completion time")
    last_updated: str = Field(..., description="Timestamp of last status update")