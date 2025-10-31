#!/usr/bin/env python3
"""
REGIQ AI/ML - Technical Statistical Analysis
Statistical analysis builder for technical reports.
"""

import logging
from typing import Any, Dict
from ..base.base_template import ReportData

logger = logging.getLogger(__name__)

class TechnicalStatisticalAnalysis:
    """Builder for technical statistical analysis."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def build_statistical_analysis(self, data: ReportData) -> str:
        """Build comprehensive statistical analysis."""
        try:
            analysis_parts = ["<h3>Statistical Analysis</h3>"]
            
            # Descriptive statistics
            analysis_parts.append("<h4>Descriptive Statistics</h4>")
            analysis_parts.append("<p>Statistical summaries and distributions of key variables analyzed.</p>")
            
            # Inferential statistics
            if data.bias_analysis_data:
                analysis_parts.append("<h4>Fairness Statistical Tests</h4>")
                fairness_metrics = data.bias_analysis_data.get("fairness_metrics", {})
                for metric, value in fairness_metrics.items():
                    analysis_parts.append(f"<p><strong>{metric.replace('_', ' ').title()}:</strong> {value:.4f}</p>")
            
            # Confidence intervals
            if data.risk_simulation_data:
                analysis_parts.append("<h4>Risk Analysis Statistics</h4>")
                risk_metrics = data.risk_simulation_data.get("risk_metrics", {})
                confidence_interval = risk_metrics.get("confidence_interval", [])
                if confidence_interval:
                    analysis_parts.append(f"<p><strong>Confidence Interval:</strong> [{confidence_interval[0]:.4f}, {confidence_interval[1]:.4f}]</p>")
            
            return "\n".join(analysis_parts)
            
        except Exception as e:
            self.logger.error(f"Failed to build statistical analysis: {str(e)}")
            return "<p>Statistical analysis could not be generated.</p>"
