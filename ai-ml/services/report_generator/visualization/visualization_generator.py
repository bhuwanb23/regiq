#!/usr/bin/env python3
"""
REGIQ AI/ML - Visualization Generator
Main orchestrator for data visualization generation.
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
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from .chart_engine import ChartEngine, ChartConfig, ChartType
from .data_binder import DataBinder, DataBinding

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class VisualizationRequest:
    """Visualization generation request."""
    request_id: str
    visualization_type: str  # dashboard, single_chart, report_charts
    source_data: Dict[str, Any]
    config: Dict[str, Any]
    output_format: str = "json"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "request_id": self.request_id,
            "visualization_type": self.visualization_type,
            "source_data": self.source_data,
            "config": self.config,
            "output_format": self.output_format
        }


class VisualizationGenerator:
    """
    Main visualization generator.
    
    Orchestrates chart engine and data binder to create
    visualizations from Phase 5.1/5.2 data.
    """
    
    def __init__(self):
        """Initialize visualization generator."""
        self.logger = logging.getLogger(__name__)
        self.chart_engine = ChartEngine()
        self.data_binder = DataBinder()
        
        # Dashboard templates
        self.dashboard_templates = self._initialize_dashboard_templates()
        
        self.logger.info("Visualization generator initialized")
    
    def _initialize_dashboard_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize dashboard templates."""
        return {
            "executive_dashboard": {
                "name": "Executive Dashboard",
                "description": "High-level KPIs and strategic insights",
                "layout": {
                    "grid": {"columns": 12, "rows": 8, "gap": 16},
                    "responsive": True
                },
                "charts": [
                    {
                        "chart_id": "compliance_gauge",
                        "template": "compliance_gauge",
                        "position": {"col": 1, "row": 1, "span_col": 4, "span_row": 3},
                        "bindings": "compliance"
                    },
                    {
                        "chart_id": "risk_matrix",
                        "template": "risk_matrix", 
                        "position": {"col": 5, "row": 1, "span_col": 8, "span_row": 3},
                        "bindings": "risk"
                    },
                    {
                        "chart_id": "compliance_trends",
                        "template": "compliance_trends",
                        "position": {"col": 1, "row": 4, "span_col": 12, "span_row": 3},
                        "bindings": "trends"
                    },
                    {
                        "chart_id": "kpi_cards",
                        "template": "kpi_cards",
                        "position": {"col": 1, "row": 7, "span_col": 12, "span_row": 2},
                        "bindings": "kpis"
                    }
                ]
            },
            "technical_dashboard": {
                "name": "Technical Dashboard",
                "description": "Detailed technical analysis and model performance",
                "layout": {
                    "grid": {"columns": 12, "rows": 10, "gap": 16},
                    "responsive": True
                },
                "charts": [
                    {
                        "chart_id": "model_performance",
                        "template": "model_performance",
                        "position": {"col": 1, "row": 1, "span_col": 6, "span_row": 4},
                        "bindings": "model_metrics"
                    },
                    {
                        "chart_id": "bias_analysis",
                        "template": "bias_analysis",
                        "position": {"col": 7, "row": 1, "span_col": 6, "span_row": 4},
                        "bindings": "bias_metrics"
                    },
                    {
                        "chart_id": "feature_importance",
                        "template": "feature_importance",
                        "position": {"col": 1, "row": 5, "span_col": 12, "span_row": 3},
                        "bindings": "features"
                    },
                    {
                        "chart_id": "performance_trends",
                        "template": "compliance_trends",
                        "position": {"col": 1, "row": 8, "span_col": 12, "span_row": 3},
                        "bindings": "performance_trends"
                    }
                ]
            },
            "regulatory_dashboard": {
                "name": "Regulatory Dashboard", 
                "description": "Compliance status and regulatory tracking",
                "layout": {
                    "grid": {"columns": 12, "rows": 8, "gap": 16},
                    "responsive": True
                },
                "charts": [
                    {
                        "chart_id": "compliance_distribution",
                        "template": "compliance_distribution",
                        "position": {"col": 1, "row": 1, "span_col": 6, "span_row": 4},
                        "bindings": "compliance_dist"
                    },
                    {
                        "chart_id": "regulatory_timeline",
                        "template": "regulatory_timeline",
                        "position": {"col": 7, "row": 1, "span_col": 6, "span_row": 4},
                        "bindings": "timeline"
                    },
                    {
                        "chart_id": "evidence_flow",
                        "template": "compliance_trends",  # Placeholder
                        "position": {"col": 1, "row": 5, "span_col": 12, "span_row": 4},
                        "bindings": "evidence"
                    }
                ]
            }
        }
    
    def generate_visualization(self, request: VisualizationRequest) -> Dict[str, Any]:
        """
        Generate visualization based on request.
        
        Args:
            request: Visualization request
            
        Returns:
            Generated visualization
        """
        try:
            if request.visualization_type == "dashboard":
                return self._generate_dashboard(request)
            elif request.visualization_type == "single_chart":
                return self._generate_single_chart(request)
            elif request.visualization_type == "report_charts":
                return self._generate_report_charts(request)
            else:
                raise ValueError(f"Unknown visualization type: {request.visualization_type}")
                
        except Exception as e:
            self.logger.error(f"Visualization generation failed: {str(e)}")
            return self._create_error_response(request, str(e))
    
    def _generate_dashboard(self, request: VisualizationRequest) -> Dict[str, Any]:
        """Generate dashboard visualization."""
        try:
            dashboard_type = request.config.get("dashboard_type", "executive_dashboard")
            template = self.dashboard_templates.get(dashboard_type)
            
            if not template:
                raise ValueError(f"Unknown dashboard template: {dashboard_type}")
            
            # Bind data for all charts
            bound_data = self.data_binder.bind_compliance_dashboard_data(request.source_data)
            
            # Generate individual charts
            charts = []
            for chart_config in template["charts"]:
                try:
                    chart = self._generate_dashboard_chart(chart_config, bound_data, request.source_data)
                    charts.append(chart)
                except Exception as e:
                    self.logger.error(f"Failed to generate chart {chart_config['chart_id']}: {str(e)}")
                    continue
            
            # Create dashboard response
            dashboard = {
                "dashboard_id": request.request_id,
                "name": template["name"],
                "description": template["description"],
                "layout": template["layout"],
                "charts": charts,
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "chart_count": len(charts),
                    "dashboard_type": dashboard_type
                }
            }
            
            self.logger.info(f"Generated dashboard with {len(charts)} charts")
            return dashboard
            
        except Exception as e:
            self.logger.error(f"Dashboard generation failed: {str(e)}")
            raise
    
    def _generate_dashboard_chart(
        self, 
        chart_config: Dict[str, Any], 
        bound_data: Dict[str, Any],
        source_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate individual chart for dashboard."""
        
        chart_id = chart_config["chart_id"]
        template_id = chart_config["template"]
        
        # Get chart template
        template = self.chart_engine.get_template(template_id)
        if not template:
            raise ValueError(f"Unknown chart template: {template_id}")
        
        # Prepare chart data based on template and bindings
        chart_data = self._prepare_chart_data(template_id, bound_data, source_data)
        
        # Create chart configuration
        config = ChartConfig(
            chart_id=chart_id,
            chart_type=template.chart_type,
            title=template.name,
            data=chart_data,
            width=600,  # Will be adjusted by layout
            height=400
        )
        
        # Generate chart
        chart_spec = self.chart_engine.create_chart(config)
        
        # Add dashboard-specific metadata
        chart_spec["position"] = chart_config["position"]
        chart_spec["template_id"] = template_id
        
        return chart_spec
    
    def _prepare_chart_data(
        self, 
        template_id: str, 
        bound_data: Dict[str, Any],
        source_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare chart data based on template."""
        
        if template_id == "compliance_gauge":
            return {
                "value": bound_data.get("value", 0.0),
                "max_value": 1.0,
                "target": 0.9
            }
        
        elif template_id == "risk_matrix":
            return bound_data.get("risk_matrix_data", {
                "x_values": ["Low", "Medium", "High"],
                "y_values": ["Low", "Medium", "High"],
                "z_values": [[0.1, 0.2, 0.3], [0.2, 0.4, 0.6], [0.3, 0.6, 0.9]]
            })
        
        elif template_id == "compliance_trends":
            # Mock trend data - would be real historical data
            return {
                "x_values": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                "y_values": [0.72, 0.75, 0.73, 0.78, 0.76, bound_data.get("value", 0.78)]
            }
        
        elif template_id == "model_performance":
            fairness_metrics = bound_data.get("metrics", {})
            return {
                "metrics": list(fairness_metrics.keys()) if fairness_metrics else ["Accuracy", "Precision", "Recall", "F1"],
                "values": list(fairness_metrics.values()) if fairness_metrics else [0.85, 0.82, 0.79, 0.81]
            }
        
        elif template_id == "bias_analysis":
            flagged = bound_data.get("flagged", [])
            return {
                "categories": flagged if flagged else ["Gender", "Age", "Race"],
                "values": [0.15, 0.12, 0.08] if flagged else [0.0, 0.0, 0.0]
            }
        
        elif template_id == "compliance_distribution":
            return bound_data.get("compliance_distribution", {
                "categories": ["Compliant", "Non-Compliant"],
                "values": [19, 6]
            })
        
        elif template_id == "kpi_cards":
            return {
                "kpis": [
                    {"name": "Compliance Score", "value": bound_data.get("value", 0.0), "trend": "up"},
                    {"name": "Risk Level", "value": bound_data.get("level", "medium"), "trend": "stable"},
                    {"name": "Bias Score", "value": bound_data.get("bias_score", 0.0), "trend": "up"},
                    {"name": "Total Regulations", "value": bound_data.get("total", 0), "trend": "stable"}
                ]
            }
        
        else:
            # Default data structure
            return {"message": f"Data for {template_id} not implemented"}
    
    def _generate_single_chart(self, request: VisualizationRequest) -> Dict[str, Any]:
        """Generate single chart visualization."""
        try:
            chart_type = request.config.get("chart_type", "bar")
            chart_id = request.config.get("chart_id", f"chart_{datetime.utcnow().timestamp()}")
            
            # Create chart configuration
            config = ChartConfig(
                chart_id=chart_id,
                chart_type=ChartType(chart_type),
                title=request.config.get("title", "Chart"),
                data=request.config.get("data", {}),
                width=request.config.get("width", 800),
                height=request.config.get("height", 600)
            )
            
            # Generate chart
            chart = self.chart_engine.create_chart(config)
            
            return {
                "visualization_type": "single_chart",
                "chart": chart,
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "request_id": request.request_id
                }
            }
            
        except Exception as e:
            self.logger.error(f"Single chart generation failed: {str(e)}")
            raise
    
    def _generate_report_charts(self, request: VisualizationRequest) -> Dict[str, Any]:
        """Generate charts for report integration."""
        try:
            # Bind data
            bound_data = self.data_binder.bind_compliance_dashboard_data(request.source_data)
            
            # Generate standard report charts
            charts = []
            
            # Compliance gauge
            compliance_chart = self._create_report_chart(
                "compliance_overview",
                "compliance_gauge",
                "Compliance Overview",
                bound_data
            )
            charts.append(compliance_chart)
            
            # Risk assessment
            risk_chart = self._create_report_chart(
                "risk_assessment",
                "risk_matrix",
                "Risk Assessment",
                bound_data
            )
            charts.append(risk_chart)
            
            # Model performance (if bias data available)
            if "bias_score" in bound_data:
                performance_chart = self._create_report_chart(
                    "model_performance",
                    "model_performance",
                    "Model Performance",
                    bound_data
                )
                charts.append(performance_chart)
            
            return {
                "visualization_type": "report_charts",
                "charts": charts,
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "chart_count": len(charts),
                    "request_id": request.request_id
                }
            }
            
        except Exception as e:
            self.logger.error(f"Report charts generation failed: {str(e)}")
            raise
    
    def _create_report_chart(
        self, 
        chart_id: str, 
        template_id: str, 
        title: str, 
        bound_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create chart for report integration."""
        
        template = self.chart_engine.get_template(template_id)
        if not template:
            raise ValueError(f"Unknown template: {template_id}")
        
        chart_data = self._prepare_chart_data(template_id, bound_data, {})
        
        config = ChartConfig(
            chart_id=chart_id,
            chart_type=template.chart_type,
            title=title,
            data=chart_data,
            width=600,
            height=400
        )
        
        return self.chart_engine.create_chart(config)
    
    def _create_error_response(self, request: VisualizationRequest, error_message: str) -> Dict[str, Any]:
        """Create error response."""
        return {
            "error": True,
            "message": error_message,
            "request_id": request.request_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_available_dashboards(self) -> List[Dict[str, Any]]:
        """Get list of available dashboard templates."""
        return [
            {
                "template_id": template_id,
                "name": template["name"],
                "description": template["description"],
                "chart_count": len(template["charts"])
            }
            for template_id, template in self.dashboard_templates.items()
        ]
    
    def get_available_chart_types(self) -> List[str]:
        """Get list of available chart types."""
        return self.chart_engine.list_chart_types()
    
    def validate_request(self, request: VisualizationRequest) -> Tuple[bool, List[str]]:
        """Validate visualization request."""
        errors = []
        
        try:
            if not request.request_id:
                errors.append("Request ID is required")
            
            if not request.visualization_type:
                errors.append("Visualization type is required")
            
            if request.visualization_type not in ["dashboard", "single_chart", "report_charts"]:
                errors.append("Invalid visualization type")
            
            if not request.source_data:
                errors.append("Source data is required")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def __str__(self) -> str:
        """String representation."""
        return f"VisualizationGenerator({len(self.dashboard_templates)} dashboards)"
