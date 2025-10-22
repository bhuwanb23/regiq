"""
Validation module for bias mitigation effectiveness.

Validates mitigation results using fairness metrics and generates
before/after comparison reports.

Author: REGIQ AI/ML Team
Phase: 3.5 - Mitigation Validation
"""

from .mitigation_validator import MitigationValidator, ValidationReport

__all__ = [
    'MitigationValidator',
    'ValidationReport',
]
