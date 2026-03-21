#!/usr/bin/env python3
"""
REGIQ AI/ML - Report Generator Service
Complete report generation pipeline: templates → narrative → explainers → output.

Modules:
    narrative    - LLM-powered narrative generation (Gemini 1.5 Pro)
    templates    - Executive, Technical, Regulatory report templates
    visualization - Chart and dashboard generation
    terminology  - Domain-specific term management and glossary generation
    explainers   - SHAP / LIME / Fairness / Risk explanation formatters
    output       - HTML, PDF, JSON report export

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .narrative import LLMNarrativeService, PromptEngine, ContextAnalyzer, NarrativeGenerator
from .templates import BaseTemplate, TemplateRegistry, TemplateValidator
from .visualization import (
    ChartEngine, ChartTemplate, ChartConfig,
    DataBinder, DataBinding,
    DashboardEngine, DashboardLayout,
    ExportEngine, ExportConfig,
    VisualizationGenerator,
)
from .terminology import TerminologyManager, Term
from .explainers import (
    ReportExplainerFactory,
    SHAPExplainer,
    LIMEExplainer,
    FairnessExplainer,
    RiskSimulationExplainer,
)
from .output import ReportOutputGenerator

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    # Narrative
    "LLMNarrativeService",
    "PromptEngine",
    "ContextAnalyzer",
    "NarrativeGenerator",
    # Templates
    "BaseTemplate",
    "TemplateRegistry",
    "TemplateValidator",
    # Visualization
    "ChartEngine",
    "ChartTemplate",
    "ChartConfig",
    "DataBinder",
    "DataBinding",
    "DashboardEngine",
    "DashboardLayout",
    "ExportEngine",
    "ExportConfig",
    "VisualizationGenerator",
    # Terminology
    "TerminologyManager",
    "Term",
    # Explainers
    "ReportExplainerFactory",
    "SHAPExplainer",
    "LIMEExplainer",
    "FairnessExplainer",
    "RiskSimulationExplainer",
    # Output
    "ReportOutputGenerator",
]
