#!/usr/bin/env python3
"""
REGIQ AI/ML - Chart Engine
Core chart generation engine with 15+ chart types.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Configure logging
logger = logging.getLogger(__name__)


class ChartType(Enum):
    """Supported chart types."""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    GAUGE = "gauge"
    RADAR = "radar"
    AREA = "area"
    HISTOGRAM = "histogram"
    BOX = "box"
    VIOLIN = "violin"
    TREEMAP = "treemap"
    SANKEY = "sankey"
    TIMELINE = "timeline"
    MATRIX = "matrix"
    WATERFALL = "waterfall"


@dataclass
class ChartConfig:
    """Chart configuration."""
    chart_id: str
    chart_type: ChartType
    title: str
    data: Dict[str, Any]
    width: int = 800
    height: int = 600
    theme: str = "regiq"
    interactive: bool = True
    export_formats: List[str] = None
    
    def __post_init__(self):
        if self.export_formats is None:
            self.export_formats = ["png", "svg"]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        config_dict = asdict(self)
        config_dict["chart_type"] = self.chart_type.value
        return config_dict


@dataclass
class ChartTemplate:
    """Chart template definition."""
    template_id: str
    chart_type: ChartType
    name: str
    description: str
    required_data_fields: List[str]
    optional_data_fields: List[str]
    default_config: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        template_dict = asdict(self)
        template_dict["chart_type"] = self.chart_type.value
        return template_dict


class ChartEngine:
    """
    Core chart generation engine.
    
    Provides chart templates, data validation, and chart generation
    for compliance dashboards and reports.
    """
    
    def __init__(self):
        """Initialize chart engine."""
        self.logger = logging.getLogger(__name__)
        self.templates: Dict[str, ChartTemplate] = {}
        self.themes: Dict[str, Dict[str, Any]] = {}
        
        # Initialize chart templates and themes
        self._initialize_templates()
        self._initialize_themes()
        
        self.logger.info(f"Chart engine initialized with {len(self.templates)} templates")
    
    def _initialize_templates(self) -> None:
        """Initialize chart templates."""
        
        # Compliance Score Gauge
        self.templates["compliance_gauge"] = ChartTemplate(
            template_id="compliance_gauge",
            chart_type=ChartType.GAUGE,
            name="Compliance Score Gauge",
            description="Gauge chart for compliance scores with traffic light colors",
            required_data_fields=["value"],
            optional_data_fields=["target", "max_value", "thresholds"],
            default_config={
                "color_scheme": "traffic_light",
                "show_target": True,
                "animate": True
            }
        )
        
        # Risk Assessment Matrix
        self.templates["risk_matrix"] = ChartTemplate(
            template_id="risk_matrix",
            chart_type=ChartType.HEATMAP,
            name="Risk Assessment Matrix",
            description="Heatmap showing risk probability vs impact",
            required_data_fields=["x_values", "y_values", "z_values"],
            optional_data_fields=["annotations", "color_scale"],
            default_config={
                "color_scale": "RdYlGn_r",
                "show_annotations": True,
                "grid": True
            }
        )
        
        # Compliance Trends
        self.templates["compliance_trends"] = ChartTemplate(
            template_id="compliance_trends",
            chart_type=ChartType.LINE,
            name="Compliance Trends",
            description="Line chart showing compliance trends over time",
            required_data_fields=["x_values", "y_values"],
            optional_data_fields=["multiple_series", "target_line"],
            default_config={
                "smooth": True,
                "markers": True,
                "fill_area": False
            }
        )
        
        # Model Performance Radar
        self.templates["model_performance"] = ChartTemplate(
            template_id="model_performance",
            chart_type=ChartType.RADAR,
            name="Model Performance Radar",
            description="Radar chart for model performance metrics",
            required_data_fields=["metrics", "values"],
            optional_data_fields=["comparison_values", "thresholds"],
            default_config={
                "fill": True,
                "opacity": 0.6,
                "grid": True
            }
        )
        
        # Bias Analysis Bar Chart
        self.templates["bias_analysis"] = ChartTemplate(
            template_id="bias_analysis",
            chart_type=ChartType.BAR,
            name="Bias Analysis",
            description="Bar chart for bias metrics comparison",
            required_data_fields=["categories", "values"],
            optional_data_fields=["comparison_values", "thresholds"],
            default_config={
                "orientation": "vertical",
                "grouped": True,
                "show_values": True
            }
        )
        
        # Financial Impact Waterfall
        self.templates["financial_waterfall"] = ChartTemplate(
            template_id="financial_waterfall",
            chart_type=ChartType.WATERFALL,
            name="Financial Impact Waterfall",
            description="Waterfall chart for financial impact analysis",
            required_data_fields=["categories", "values"],
            optional_data_fields=["colors", "cumulative"],
            default_config={
                "show_cumulative": True,
                "color_positive": "#2E8B57",
                "color_negative": "#DC143C"
            }
        )
        
        # Regulatory Timeline
        self.templates["regulatory_timeline"] = ChartTemplate(
            template_id="regulatory_timeline",
            chart_type=ChartType.TIMELINE,
            name="Regulatory Timeline",
            description="Timeline chart for regulatory deadlines and events",
            required_data_fields=["events"],
            optional_data_fields=["categories", "status_colors"],
            default_config={
                "show_today": True,
                "interactive": True,
                "zoom": True
            }
        )
        
        # Add more templates...
        self._add_additional_templates()
    
    def _add_additional_templates(self) -> None:
        """Add additional chart templates."""
        
        # KPI Cards (special chart type)
        self.templates["kpi_cards"] = ChartTemplate(
            template_id="kpi_cards",
            chart_type=ChartType.BAR,  # Base type, will be customized
            name="KPI Cards",
            description="Card-based KPI display",
            required_data_fields=["kpis"],
            optional_data_fields=["trends", "targets"],
            default_config={
                "layout": "horizontal",
                "show_trends": True,
                "color_coding": True
            }
        )
        
        # Feature Importance
        self.templates["feature_importance"] = ChartTemplate(
            template_id="feature_importance",
            chart_type=ChartType.BAR,
            name="Feature Importance",
            description="Horizontal bar chart for feature importance",
            required_data_fields=["features", "importance"],
            optional_data_fields=["categories", "colors"],
            default_config={
                "orientation": "horizontal",
                "sort_values": True,
                "top_n": 10
            }
        )
        
        # Compliance Distribution
        self.templates["compliance_distribution"] = ChartTemplate(
            template_id="compliance_distribution",
            chart_type=ChartType.PIE,
            name="Compliance Distribution",
            description="Pie chart for compliance status distribution",
            required_data_fields=["categories", "values"],
            optional_data_fields=["colors", "explode"],
            default_config={
                "show_percentages": True,
                "show_labels": True,
                "hole": 0.3  # Donut chart
            }
        )
    
    def _initialize_themes(self) -> None:
        """Initialize chart themes."""
        
        # REGIQ Corporate Theme
        self.themes["regiq"] = {
            "background_color": "#FFFFFF",
            "grid_color": "#E5E5E5",
            "text_color": "#333333",
            "primary_colors": ["#007ACC", "#28A745", "#FFC107", "#DC3545", "#6F42C1"],
            "compliance_colors": {
                "excellent": "#28A745",
                "good": "#6BC04F", 
                "fair": "#FFC107",
                "poor": "#FD7E14",
                "critical": "#DC3545"
            },
            "font_family": "Arial, sans-serif",
            "font_size": 12
        }
        
        # Dark Theme
        self.themes["dark"] = {
            "background_color": "#1E1E1E",
            "grid_color": "#404040",
            "text_color": "#FFFFFF",
            "primary_colors": ["#4FC3F7", "#81C784", "#FFB74D", "#F06292", "#BA68C8"],
            "compliance_colors": {
                "excellent": "#4CAF50",
                "good": "#8BC34A",
                "fair": "#FF9800", 
                "poor": "#FF5722",
                "critical": "#F44336"
            },
            "font_family": "Arial, sans-serif",
            "font_size": 12
        }
        
        # High Contrast Theme (Accessibility)
        self.themes["high_contrast"] = {
            "background_color": "#FFFFFF",
            "grid_color": "#000000",
            "text_color": "#000000",
            "primary_colors": ["#000000", "#0000FF", "#FF0000", "#008000", "#800080"],
            "compliance_colors": {
                "excellent": "#008000",
                "good": "#4B8B3B",
                "fair": "#FF8C00",
                "poor": "#FF4500", 
                "critical": "#FF0000"
            },
            "font_family": "Arial, sans-serif",
            "font_size": 14
        }
    
    def create_chart(self, config: ChartConfig) -> Dict[str, Any]:
        """
        Create chart based on configuration.
        
        Args:
            config: Chart configuration
            
        Returns:
            Chart specification dictionary
        """
        try:
            # Validate configuration
            is_valid, errors = self.validate_config(config)
            if not is_valid:
                raise ValueError(f"Invalid chart configuration: {', '.join(errors)}")
            
            # Get theme
            theme = self.themes.get(config.theme, self.themes["regiq"])
            
            # Generate chart specification based on type
            chart_spec = self._generate_chart_spec(config, theme)
            
            # Add metadata
            chart_spec["metadata"] = {
                "chart_id": config.chart_id,
                "chart_type": config.chart_type.value,
                "created_at": datetime.utcnow().isoformat(),
                "engine_version": "1.0.0"
            }
            
            self.logger.info(f"Created chart: {config.chart_id} ({config.chart_type.value})")
            
            return chart_spec
            
        except Exception as e:
            self.logger.error(f"Failed to create chart {config.chart_id}: {str(e)}")
            raise
    
    def _generate_chart_spec(self, config: ChartConfig, theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate chart specification based on type."""
        
        base_spec = {
            "title": config.title,
            "width": config.width,
            "height": config.height,
            "theme": theme,
            "interactive": config.interactive,
            "export_formats": config.export_formats
        }
        
        # Generate type-specific specification
        if config.chart_type == ChartType.GAUGE:
            return self._create_gauge_spec(config, base_spec, theme)
        elif config.chart_type == ChartType.HEATMAP:
            return self._create_heatmap_spec(config, base_spec, theme)
        elif config.chart_type == ChartType.LINE:
            return self._create_line_spec(config, base_spec, theme)
        elif config.chart_type == ChartType.BAR:
            return self._create_bar_spec(config, base_spec, theme)
        elif config.chart_type == ChartType.PIE:
            return self._create_pie_spec(config, base_spec, theme)
        elif config.chart_type == ChartType.RADAR:
            return self._create_radar_spec(config, base_spec, theme)
        else:
            return self._create_generic_spec(config, base_spec, theme)
    
    def _create_gauge_spec(self, config: ChartConfig, base_spec: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create gauge chart specification."""
        spec = {**base_spec}
        
        data = config.data
        value = data.get("value", 0)
        max_value = data.get("max_value", 1.0)
        target = data.get("target")
        
        spec.update({
            "type": "gauge",
            "data": {
                "value": value,
                "max_value": max_value,
                "target": target
            },
            "config": {
                "color_ranges": [
                    {"min": 0, "max": 0.6, "color": theme["compliance_colors"]["critical"]},
                    {"min": 0.6, "max": 0.8, "color": theme["compliance_colors"]["fair"]},
                    {"min": 0.8, "max": 1.0, "color": theme["compliance_colors"]["excellent"]}
                ],
                "show_target": target is not None,
                "animate": True
            }
        })
        
        return spec
    
    def _create_heatmap_spec(self, config: ChartConfig, base_spec: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create heatmap chart specification."""
        spec = {**base_spec}
        
        data = config.data
        
        spec.update({
            "type": "heatmap",
            "data": {
                "x": data.get("x_values", []),
                "y": data.get("y_values", []),
                "z": data.get("z_values", [])
            },
            "config": {
                "color_scale": "RdYlGn_r",
                "show_annotations": data.get("show_annotations", True),
                "grid": True
            }
        })
        
        return spec
    
    def _create_line_spec(self, config: ChartConfig, base_spec: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create line chart specification."""
        spec = {**base_spec}
        
        data = config.data
        
        spec.update({
            "type": "line",
            "data": {
                "x": data.get("x_values", []),
                "y": data.get("y_values", []),
                "series": data.get("multiple_series", [])
            },
            "config": {
                "smooth": True,
                "markers": True,
                "colors": theme["primary_colors"]
            }
        })
        
        return spec
    
    def _create_bar_spec(self, config: ChartConfig, base_spec: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create bar chart specification."""
        spec = {**base_spec}
        
        data = config.data
        
        spec.update({
            "type": "bar",
            "data": {
                "categories": data.get("categories", []),
                "values": data.get("values", [])
            },
            "config": {
                "orientation": data.get("orientation", "vertical"),
                "colors": theme["primary_colors"],
                "show_values": True
            }
        })
        
        return spec
    
    def _create_pie_spec(self, config: ChartConfig, base_spec: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create pie chart specification."""
        spec = {**base_spec}
        
        data = config.data
        
        spec.update({
            "type": "pie",
            "data": {
                "labels": data.get("categories", []),
                "values": data.get("values", [])
            },
            "config": {
                "colors": theme["primary_colors"],
                "show_percentages": True,
                "hole": data.get("hole", 0)
            }
        })
        
        return spec
    
    def _create_radar_spec(self, config: ChartConfig, base_spec: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create radar chart specification."""
        spec = {**base_spec}
        
        data = config.data
        
        spec.update({
            "type": "radar",
            "data": {
                "metrics": data.get("metrics", []),
                "values": data.get("values", [])
            },
            "config": {
                "fill": True,
                "opacity": 0.6,
                "colors": theme["primary_colors"]
            }
        })
        
        return spec
    
    def _create_generic_spec(self, config: ChartConfig, base_spec: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create generic chart specification."""
        spec = {**base_spec}
        
        spec.update({
            "type": config.chart_type.value,
            "data": config.data,
            "config": {
                "colors": theme["primary_colors"]
            }
        })
        
        return spec
    
    def validate_config(self, config: ChartConfig) -> Tuple[bool, List[str]]:
        """Validate chart configuration."""
        errors = []
        
        try:
            # Basic validation
            if not config.chart_id:
                errors.append("Chart ID is required")
            
            if not config.title:
                errors.append("Chart title is required")
            
            if config.width <= 0 or config.height <= 0:
                errors.append("Chart dimensions must be positive")
            
            # Data validation
            if not config.data:
                errors.append("Chart data is required")
            
            # Theme validation
            if config.theme not in self.themes:
                errors.append(f"Unknown theme: {config.theme}")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def get_template(self, template_id: str) -> Optional[ChartTemplate]:
        """Get chart template by ID."""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available chart templates."""
        return [template.to_dict() for template in self.templates.values()]
    
    def list_chart_types(self) -> List[str]:
        """List all supported chart types."""
        return [chart_type.value for chart_type in ChartType]
    
    def get_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """Get theme by name."""
        return self.themes.get(theme_name)
    
    def list_themes(self) -> List[str]:
        """List all available themes."""
        return list(self.themes.keys())
    
    def __str__(self) -> str:
        """String representation."""
        return f"ChartEngine({len(self.templates)} templates, {len(self.themes)} themes)"
