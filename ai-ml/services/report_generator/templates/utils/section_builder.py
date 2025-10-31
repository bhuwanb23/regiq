#!/usr/bin/env python3
"""
REGIQ AI/ML - Section Builder
Utility for building report sections from formatted data.

This module provides:
- Section construction utilities
- Content formatting helpers
- Template section builders
- HTML/text generation utilities

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from ..base.base_template import ReportSection

# Configure logging
logger = logging.getLogger(__name__)


class SectionBuilder:
    """
    Utility class for building report sections from formatted data.
    
    Provides helpers for:
    - Section content generation
    - HTML formatting
    - Data visualization preparation
    - Content structuring
    """
    
    def __init__(self):
        """Initialize section builder."""
        self.logger = logging.getLogger(__name__)
    
    def build_summary_section(
        self, 
        title: str, 
        summary_data: Dict[str, Any], 
        section_id: str,
        order: int = 1
    ) -> ReportSection:
        """
        Build a summary section.
        
        Args:
            title: Section title
            summary_data: Summary data dictionary
            section_id: Unique section identifier
            order: Section order
            
        Returns:
            ReportSection object
        """
        try:
            content_parts = [f"<h3>{title}</h3>"]
            
            # Overview
            if "overview" in summary_data:
                content_parts.append(f"<p><strong>Overview:</strong> {summary_data['overview']}</p>")
            
            # Key points
            if "key_points" in summary_data and summary_data["key_points"]:
                content_parts.append("<h4>Key Points:</h4>")
                content_parts.append("<ul>")
                for point in summary_data["key_points"]:
                    content_parts.append(f"<li>{point}</li>")
                content_parts.append("</ul>")
            
            # Metrics
            metrics = {}
            for key, value in summary_data.items():
                if key not in ["overview", "key_points"] and isinstance(value, (int, float)):
                    metrics[key] = value
            
            if metrics:
                content_parts.append("<h4>Key Metrics:</h4>")
                content_parts.append("<table style='border-collapse: collapse; width: 100%;'>")
                content_parts.append("<tr style='background-color: #f2f2f2;'>")
                content_parts.append("<th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Metric</th>")
                content_parts.append("<th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Value</th>")
                content_parts.append("</tr>")
                
                for metric, value in metrics.items():
                    formatted_metric = metric.replace("_", " ").title()
                    formatted_value = f"{value:.2f}" if isinstance(value, float) else str(value)
                    content_parts.append("<tr>")
                    content_parts.append(f"<td style='border: 1px solid #ddd; padding: 8px;'>{formatted_metric}</td>")
                    content_parts.append(f"<td style='border: 1px solid #ddd; padding: 8px;'>{formatted_value}</td>")
                    content_parts.append("</tr>")
                
                content_parts.append("</table>")
            
            content = "\n".join(content_parts)
            
            return ReportSection(
                section_id=section_id,
                title=title,
                content=content,
                section_type="summary",
                order=order,
                metadata={"data_keys": list(summary_data.keys())}
            )
            
        except Exception as e:
            self.logger.error(f"Failed to build summary section: {str(e)}")
            raise
    
    def build_metrics_section(
        self,
        title: str,
        metrics_data: Dict[str, Any],
        section_id: str,
        order: int = 2
    ) -> ReportSection:
        """
        Build a metrics section with formatted tables and charts.
        
        Args:
            title: Section title
            metrics_data: Metrics data dictionary
            section_id: Unique section identifier
            order: Section order
            
        Returns:
            ReportSection object
        """
        try:
            content_parts = [f"<h3>{title}</h3>"]
            
            # Create metrics table
            if metrics_data:
                content_parts.append("<div class='metrics-container'>")
                content_parts.append("<table class='metrics-table' style='border-collapse: collapse; width: 100%; margin: 20px 0;'>")
                content_parts.append("<thead>")
                content_parts.append("<tr style='background-color: #007acc; color: white;'>")
                content_parts.append("<th style='border: 1px solid #ddd; padding: 12px; text-align: left;'>Metric</th>")
                content_parts.append("<th style='border: 1px solid #ddd; padding: 12px; text-align: left;'>Value</th>")
                content_parts.append("<th style='border: 1px solid #ddd; padding: 12px; text-align: left;'>Status</th>")
                content_parts.append("</tr>")
                content_parts.append("</thead>")
                content_parts.append("<tbody>")
                
                for metric_name, metric_value in metrics_data.items():
                    formatted_name = metric_name.replace("_", " ").title()
                    
                    # Format value based on type
                    if isinstance(metric_value, float):
                        if 0 <= metric_value <= 1:
                            formatted_value = f"{metric_value:.3f}"
                            status = self._get_metric_status(metric_value)
                        else:
                            formatted_value = f"{metric_value:.2f}"
                            status = "N/A"
                    elif isinstance(metric_value, int):
                        formatted_value = str(metric_value)
                        status = "N/A"
                    else:
                        formatted_value = str(metric_value)
                        status = "N/A"
                    
                    status_color = self._get_status_color(status)
                    
                    content_parts.append("<tr>")
                    content_parts.append(f"<td style='border: 1px solid #ddd; padding: 8px;'>{formatted_name}</td>")
                    content_parts.append(f"<td style='border: 1px solid #ddd; padding: 8px;'>{formatted_value}</td>")
                    content_parts.append(f"<td style='border: 1px solid #ddd; padding: 8px; background-color: {status_color};'>{status}</td>")
                    content_parts.append("</tr>")
                
                content_parts.append("</tbody>")
                content_parts.append("</table>")
                content_parts.append("</div>")
            
            content = "\n".join(content_parts)
            
            return ReportSection(
                section_id=section_id,
                title=title,
                content=content,
                section_type="metrics",
                order=order,
                metadata={"metrics_count": len(metrics_data)}
            )
            
        except Exception as e:
            self.logger.error(f"Failed to build metrics section: {str(e)}")
            raise
    
    def build_recommendations_section(
        self,
        title: str,
        recommendations: List[str],
        section_id: str,
        order: int = 3,
        priority_levels: Optional[List[str]] = None
    ) -> ReportSection:
        """
        Build a recommendations section.
        
        Args:
            title: Section title
            recommendations: List of recommendations
            section_id: Unique section identifier
            order: Section order
            priority_levels: Optional priority levels for recommendations
            
        Returns:
            ReportSection object
        """
        try:
            content_parts = [f"<h3>{title}</h3>"]
            
            if not recommendations:
                content_parts.append("<p><em>No recommendations available.</em></p>")
            else:
                content_parts.append("<div class='recommendations-container'>")
                
                # Group by priority if provided
                if priority_levels and len(priority_levels) == len(recommendations):
                    priority_groups = {}
                    for rec, priority in zip(recommendations, priority_levels):
                        if priority not in priority_groups:
                            priority_groups[priority] = []
                        priority_groups[priority].append(rec)
                    
                    # Display by priority
                    priority_order = ["high", "medium", "low"]
                    for priority in priority_order:
                        if priority in priority_groups:
                            priority_color = {"high": "#ff6b6b", "medium": "#ffd93d", "low": "#6bcf7f"}.get(priority, "#ddd")
                            content_parts.append(f"<h4 style='color: {priority_color};'>{priority.title()} Priority</h4>")
                            content_parts.append("<ol>")
                            for rec in priority_groups[priority]:
                                content_parts.append(f"<li style='margin-bottom: 10px;'>{rec}</li>")
                            content_parts.append("</ol>")
                else:
                    # Simple numbered list
                    content_parts.append("<ol>")
                    for rec in recommendations:
                        content_parts.append(f"<li style='margin-bottom: 10px;'>{rec}</li>")
                    content_parts.append("</ol>")
                
                content_parts.append("</div>")
            
            content = "\n".join(content_parts)
            
            return ReportSection(
                section_id=section_id,
                title=title,
                content=content,
                section_type="recommendations",
                order=order,
                metadata={"recommendations_count": len(recommendations)}
            )
            
        except Exception as e:
            self.logger.error(f"Failed to build recommendations section: {str(e)}")
            raise
    
    def build_data_table_section(
        self,
        title: str,
        table_data: List[Dict[str, Any]],
        section_id: str,
        order: int = 4,
        columns: Optional[List[str]] = None
    ) -> ReportSection:
        """
        Build a data table section.
        
        Args:
            title: Section title
            table_data: List of dictionaries representing table rows
            section_id: Unique section identifier
            order: Section order
            columns: Optional list of columns to display
            
        Returns:
            ReportSection object
        """
        try:
            content_parts = [f"<h3>{title}</h3>"]
            
            if not table_data:
                content_parts.append("<p><em>No data available.</em></p>")
            else:
                # Determine columns
                if columns is None:
                    columns = list(table_data[0].keys()) if table_data else []
                
                content_parts.append("<div class='table-container' style='overflow-x: auto;'>")
                content_parts.append("<table style='border-collapse: collapse; width: 100%; margin: 20px 0;'>")
                
                # Header
                content_parts.append("<thead>")
                content_parts.append("<tr style='background-color: #007acc; color: white;'>")
                for col in columns:
                    formatted_col = col.replace("_", " ").title()
                    content_parts.append(f"<th style='border: 1px solid #ddd; padding: 12px; text-align: left;'>{formatted_col}</th>")
                content_parts.append("</tr>")
                content_parts.append("</thead>")
                
                # Body
                content_parts.append("<tbody>")
                for i, row in enumerate(table_data):
                    bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
                    content_parts.append(f"<tr style='background-color: {bg_color};'>")
                    
                    for col in columns:
                        value = row.get(col, "N/A")
                        if isinstance(value, float):
                            formatted_value = f"{value:.3f}"
                        else:
                            formatted_value = str(value)
                        content_parts.append(f"<td style='border: 1px solid #ddd; padding: 8px;'>{formatted_value}</td>")
                    
                    content_parts.append("</tr>")
                content_parts.append("</tbody>")
                content_parts.append("</table>")
                content_parts.append("</div>")
            
            content = "\n".join(content_parts)
            
            return ReportSection(
                section_id=section_id,
                title=title,
                content=content,
                section_type="data_table",
                order=order,
                metadata={"rows_count": len(table_data), "columns": columns}
            )
            
        except Exception as e:
            self.logger.error(f"Failed to build data table section: {str(e)}")
            raise
    
    def build_text_section(
        self,
        title: str,
        text_content: str,
        section_id: str,
        order: int = 5,
        format_as_html: bool = True
    ) -> ReportSection:
        """
        Build a text content section.
        
        Args:
            title: Section title
            text_content: Text content
            section_id: Unique section identifier
            order: Section order
            format_as_html: Whether to format text as HTML
            
        Returns:
            ReportSection object
        """
        try:
            content_parts = [f"<h3>{title}</h3>"]
            
            if format_as_html:
                # Convert line breaks to paragraphs
                paragraphs = text_content.split('\n\n')
                for paragraph in paragraphs:
                    if paragraph.strip():
                        content_parts.append(f"<p>{paragraph.strip()}</p>")
            else:
                content_parts.append(f"<pre>{text_content}</pre>")
            
            content = "\n".join(content_parts)
            
            return ReportSection(
                section_id=section_id,
                title=title,
                content=content,
                section_type="text",
                order=order,
                metadata={"content_length": len(text_content)}
            )
            
        except Exception as e:
            self.logger.error(f"Failed to build text section: {str(e)}")
            raise
    
    def build_status_section(
        self,
        title: str,
        status_data: Dict[str, Any],
        section_id: str,
        order: int = 6
    ) -> ReportSection:
        """
        Build a status overview section.
        
        Args:
            title: Section title
            status_data: Status data dictionary
            section_id: Unique section identifier
            order: Section order
            
        Returns:
            ReportSection object
        """
        try:
            content_parts = [f"<h3>{title}</h3>"]
            
            # Overall status
            overall_status = status_data.get("overall_status", "unknown")
            status_color = self._get_status_color(overall_status)
            
            content_parts.append("<div class='status-container'>")
            content_parts.append(f"<div class='overall-status' style='background-color: {status_color}; padding: 15px; border-radius: 5px; margin: 10px 0;'>")
            content_parts.append(f"<h4 style='margin: 0; color: white;'>Overall Status: {overall_status.title()}</h4>")
            content_parts.append("</div>")
            
            # Status breakdown
            status_items = {k: v for k, v in status_data.items() if k != "overall_status"}
            if status_items:
                content_parts.append("<div class='status-breakdown'>")
                content_parts.append("<table style='border-collapse: collapse; width: 100%; margin: 10px 0;'>")
                
                for item, value in status_items.items():
                    formatted_item = item.replace("_", " ").title()
                    content_parts.append("<tr>")
                    content_parts.append(f"<td style='border: 1px solid #ddd; padding: 8px; font-weight: bold;'>{formatted_item}</td>")
                    content_parts.append(f"<td style='border: 1px solid #ddd; padding: 8px;'>{value}</td>")
                    content_parts.append("</tr>")
                
                content_parts.append("</table>")
                content_parts.append("</div>")
            
            content_parts.append("</div>")
            
            content = "\n".join(content_parts)
            
            return ReportSection(
                section_id=section_id,
                title=title,
                content=content,
                section_type="status",
                order=order,
                metadata={"status_items": len(status_items)}
            )
            
        except Exception as e:
            self.logger.error(f"Failed to build status section: {str(e)}")
            raise
    
    def _get_metric_status(self, value: float) -> str:
        """Get status based on metric value (0-1 scale)."""
        if value >= 0.8:
            return "Excellent"
        elif value >= 0.6:
            return "Good"
        elif value >= 0.4:
            return "Fair"
        elif value >= 0.2:
            return "Poor"
        else:
            return "Critical"
    
    def _get_status_color(self, status: str) -> str:
        """Get color for status indicators."""
        status_colors = {
            "excellent": "#28a745",
            "good": "#6bcf7f",
            "fair": "#ffc107",
            "poor": "#fd7e14",
            "critical": "#dc3545",
            "compliant": "#28a745",
            "non_compliant": "#dc3545",
            "pending": "#ffc107",
            "active": "#007acc",
            "inactive": "#6c757d",
            "unknown": "#6c757d"
        }
        return status_colors.get(status.lower(), "#6c757d")
    
    def combine_sections(self, sections: List[ReportSection]) -> str:
        """
        Combine multiple sections into a single HTML content.
        
        Args:
            sections: List of ReportSection objects
            
        Returns:
            Combined HTML content
        """
        try:
            # Sort sections by order
            sorted_sections = sorted(sections, key=lambda x: x.order)
            
            content_parts = []
            for section in sorted_sections:
                content_parts.append(f"<div class='report-section' id='{section.section_id}'>")
                content_parts.append(section.content)
                content_parts.append("</div>")
            
            return "\n".join(content_parts)
            
        except Exception as e:
            self.logger.error(f"Failed to combine sections: {str(e)}")
            raise
    
    def __str__(self) -> str:
        """String representation."""
        return "SectionBuilder()"
