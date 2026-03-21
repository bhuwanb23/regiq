#!/usr/bin/env python3
"""
REGIQ AI/ML - Risk Simulator Regulations Registry
Static regulatory framework definitions and simulation parameters.

Provides the regulatory data that feeds into the risk simulation engine:
    - RegulatoryFramework: Full framework definition with penalty ranges
    - REGULATORY_FRAMEWORKS: Registry of 8 supported regulations
    - Helper functions: query by jurisdiction, type, AI applicability

Supported Frameworks:
    EU AI Act, GDPR, ECOA/Reg B, SR 11-7, NIST AI RMF,
    BCBS 239, CCPA/CPRA, MiFID II

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .regulatory_frameworks import (
    RegulatoryFramework,
    PenaltyRange,
    REGULATORY_FRAMEWORKS,
    get_framework,
    get_frameworks_by_jurisdiction,
    get_frameworks_by_type,
    get_ai_frameworks,
    get_high_risk_frameworks,
    get_framework_ids,
    get_penalty_range,
    get_simulation_params,
    list_all_frameworks,
    get_registry_stats,
)

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    "RegulatoryFramework",
    "PenaltyRange",
    "REGULATORY_FRAMEWORKS",
    "get_framework",
    "get_frameworks_by_jurisdiction",
    "get_frameworks_by_type",
    "get_ai_frameworks",
    "get_high_risk_frameworks",
    "get_framework_ids",
    "get_penalty_range",
    "get_simulation_params",
    "list_all_frameworks",
    "get_registry_stats",
]
