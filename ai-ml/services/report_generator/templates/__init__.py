#!/usr/bin/env python3
"""
REGIQ AI/ML - Report Templates Module
Phase 5.1: Report Templates Implementation

This module provides comprehensive report template functionality for:
- Executive Reports: High-level business insights
- Technical Reports: Detailed analysis for data scientists
- Regulatory Reports: Compliance documentation for auditors

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .base.base_template import BaseTemplate
from .base.template_registry import TemplateRegistry
from .base.template_validator import TemplateValidator

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    "BaseTemplate",
    "TemplateRegistry", 
    "TemplateValidator"
]
