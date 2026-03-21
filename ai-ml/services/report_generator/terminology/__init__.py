#!/usr/bin/env python3
"""
REGIQ AI/ML - Terminology Management Module
Domain-specific terminology for financial AI compliance reports.

Provides audience-aware definitions, glossary generation, and
term standardization for executive, technical, and regulatory audiences.

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .terminology_manager import TerminologyManager, Term

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    "TerminologyManager",
    "Term",
]
