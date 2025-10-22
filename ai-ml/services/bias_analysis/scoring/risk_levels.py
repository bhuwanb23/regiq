#!/usr/bin/env python3
"""
REGIQ AI/ML - Risk Level Definitions
Defines risk levels, thresholds, and metadata for bias classification.
"""

from enum import Enum
from typing import Dict, Any


class RiskLevel(Enum):
    """Risk level classification for model bias."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Risk threshold configuration
RISK_THRESHOLDS = {
    "LOW": {
        "range": [0.0, 0.25],
        "action_timeline": "routine_monitoring",
        "action_days": None,
        "description": "Minimal bias detected - routine monitoring sufficient"
    },
    "MEDIUM": {
        "range": [0.26, 0.50],
        "action_timeline": "30_days",
        "action_days": 30,
        "description": "Moderate bias - review and mitigation within 30 days"
    },
    "HIGH": {
        "range": [0.51, 0.75],
        "action_timeline": "14_days",
        "action_days": 14,
        "description": "Significant bias - remediation required within 14 days"
    },
    "CRITICAL": {
        "range": [0.76, 1.0],
        "action_timeline": "immediate",
        "action_days": 0,
        "description": "Severe bias - immediate action required"
    }
}


# Risk metadata (regulatory implications, urgency levels, etc.)
RISK_METADATA = {
    "LOW": {
        "urgency": "LOW",
        "notification_channels": ["in_app"],
        "regulatory_impact": "Compliant",
        "deployment_recommendation": "Approved for deployment",
        "review_frequency": "Quarterly",
        "stakeholder_notification": ["Model Owner"],
        "escalation_required": False
    },
    "MEDIUM": {
        "urgency": "MEDIUM",
        "notification_channels": ["in_app", "email"],
        "regulatory_impact": "Potential compliance issues",
        "deployment_recommendation": "Conditional - requires monitoring",
        "review_frequency": "Monthly",
        "stakeholder_notification": ["Model Owner", "Compliance Team"],
        "escalation_required": False
    },
    "HIGH": {
        "urgency": "HIGH",
        "notification_channels": ["in_app", "email", "dashboard"],
        "regulatory_impact": "Non-compliant - action required",
        "deployment_recommendation": "Not recommended - remediation first",
        "review_frequency": "Weekly",
        "stakeholder_notification": ["Model Owner", "Compliance Team", "Risk Management"],
        "escalation_required": True
    },
    "CRITICAL": {
        "urgency": "URGENT",
        "notification_channels": ["in_app", "email", "sms", "webhook"],
        "regulatory_impact": "Severe violations - regulatory risk",
        "deployment_recommendation": "Blocked - immediate remediation required",
        "review_frequency": "Daily",
        "stakeholder_notification": ["Model Owner", "Compliance Team", "Risk Management", "Executive Team"],
        "escalation_required": True
    }
}


def get_risk_level_from_score(bias_score: float) -> RiskLevel:
    """
    Determine risk level from bias score.
    
    Args:
        bias_score: Composite bias score [0, 1]
        
    Returns:
        RiskLevel enum
    """
    if bias_score <= 0.25:
        return RiskLevel.LOW
    elif bias_score <= 0.50:
        return RiskLevel.MEDIUM
    elif bias_score <= 0.75:
        return RiskLevel.HIGH
    else:
        return RiskLevel.CRITICAL


def get_risk_metadata(risk_level: RiskLevel) -> Dict[str, Any]:
    """
    Get metadata for a risk level.
    
    Args:
        risk_level: RiskLevel enum
        
    Returns:
        Dictionary of risk metadata
    """
    return RISK_METADATA.get(risk_level.value, RISK_METADATA["LOW"])


def get_risk_threshold_info(risk_level: RiskLevel) -> Dict[str, Any]:
    """
    Get threshold information for a risk level.
    
    Args:
        risk_level: RiskLevel enum
        
    Returns:
        Dictionary of threshold information
    """
    return RISK_THRESHOLDS.get(risk_level.value, RISK_THRESHOLDS["LOW"])
