#!/usr/bin/env python3
"""
REGIQ AI/ML - Technical Appendices
Technical appendices builder for detailed documentation.
"""

import logging
from typing import Any, Dict
from ..base.base_template import ReportData

logger = logging.getLogger(__name__)

class TechnicalAppendices:
    """Builder for technical appendices."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def build_technical_appendices(self, data: ReportData) -> str:
        """Build comprehensive technical appendices."""
        try:
            appendices_parts = ["<h3>Technical Appendices</h3>"]
            
            # Appendix A: Model Details
            appendices_parts.append("<h4>Appendix A: Model Specifications</h4>")
            if data.bias_analysis_data:
                model_info = data.bias_analysis_data.get("model_info", {})
                appendices_parts.append(f"<p><strong>Model ID:</strong> {model_info.get('model_id', 'N/A')}</p>")
                appendices_parts.append(f"<p><strong>Model Type:</strong> {model_info.get('model_type', 'N/A')}</p>")
            
            # Appendix B: Configuration Parameters
            appendices_parts.append("<h4>Appendix B: Configuration Parameters</h4>")
            appendices_parts.append("<p>Analysis configuration and parameter settings used in the evaluation.</p>")
            
            # Appendix C: Raw Data Summary
            appendices_parts.append("<h4>Appendix C: Data Summary</h4>")
            appendices_parts.append("<p>Summary of datasets and variables used in the analysis.</p>")
            
            return "\n".join(appendices_parts)
            
        except Exception as e:
            self.logger.error(f"Failed to build technical appendices: {str(e)}")
            return "<p>Technical appendices could not be generated.</p>"
