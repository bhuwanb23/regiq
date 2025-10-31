#!/usr/bin/env python3
"""
REGIQ AI/ML - Data Visualization System
Phase 5.3: Interactive data visualization and dashboard generation.

This module provides:
- Chart generation with 15+ chart types
- Interactive dashboard creation
- Data binding from Phase 5.1/5.2
- Export capabilities (PNG, SVG, PDF)
- Responsive design system
- Accessibility features

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .chart_engine import ChartEngine, ChartTemplate, ChartConfig
from .data_binder import DataBinder, DataBinding
from .dashboard_engine import DashboardEngine, DashboardLayout
from .export_engine import ExportEngine, ExportConfig
from .visualization_generator import VisualizationGenerator

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    "ChartEngine",
    "ChartTemplate", 
    "ChartConfig",
    "DataBinder",
    "DataBinding",
    "DashboardEngine",
    "DashboardLayout",
    "ExportEngine",
    "ExportConfig",
    "VisualizationGenerator"
]