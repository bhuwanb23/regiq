"""
Risk Simulator Visualization Package

This package provides comprehensive visualization data generation for risk analysis,
scenario results, and compliance tracking. All modules generate JSON-serializable
data structures for frontend integration (React Native, web, etc.).

Modules:
- heatmap_generator: Risk heatmap data generation (probability×impact, jurisdiction×regulation, time×risk)
- distribution_analyzer: Probability distribution analysis with histograms, PDF/CDF, confidence intervals
- timeline_projector: Timeline visualization data (risk evolution, compliance deadlines, mitigation actions)
- export_manager: Multi-format data export (JSON, CSV, compressed variants)
- visualization_utils: Shared utilities for data validation, transformation, and normalization

All visualization modules follow backend-only architecture:
- Pure Python data generation (no HTML/JavaScript)
- JSON-serializable outputs
- Ready for React Native/frontend integration
"""

# Heatmap Generation
from .heatmap_generator import (
    RiskDimension,
    AggregationMethod,
    HeatmapCell,
    HeatmapData,
    HeatmapGenerator
)

# Distribution Analysis
from .distribution_analyzer import (
    DistributionType,
    HistogramData,
    PDFCDFData,
    ConfidenceInterval,
    DistributionAnalysis,
    DistributionAnalyzer
)

# Timeline Projection
from .timeline_projector import (
    EventType,
    EventSeverity,
    TimelineEvent,
    TimeSeriesPoint,
    ActionPlan,
    TimelineProjection,
    TimelineProjector
)

# Export Management
from .export_manager import (
    ExportFormat,
    ExportResult,
    ExportManager
)

# Utilities
from .visualization_utils import (
    DataValidator,
    DataTransformer,
    ColorMapper,
    DataAggregator
)

__all__ = [
    # Heatmap
    'RiskDimension',
    'AggregationMethod',
    'HeatmapCell',
    'HeatmapData',
    'HeatmapGenerator',
    # Distribution
    'DistributionType',
    'HistogramData',
    'PDFCDFData',
    'ConfidenceInterval',
    'DistributionAnalysis',
    'DistributionAnalyzer',
    # Timeline
    'EventType',
    'EventSeverity',
    'TimelineEvent',
    'TimeSeriesPoint',
    'ActionPlan',
    'TimelineProjection',
    'TimelineProjector',
    # Export
    'ExportFormat',
    'ExportResult',
    'ExportManager',
    # Utils
    'DataValidator',
    'DataTransformer',
    'ColorMapper',
    'DataAggregator'
]

__version__ = '1.0.0'
