#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Alert Management System
Manages alert creation, deduplication, and escalation for bias detection.
"""

import logging
import time
import hashlib
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

from .risk_levels import RiskLevel


logger = logging.getLogger("bias_alert_system")


@dataclass
class BiasAlert:
    """Represents a bias detection alert."""
    alert_id: str
    model_id: str
    risk_level: str
    bias_score: float
    timestamp: str
    notification_channels: List[str]
    priority: str
    alert_message: str
    detailed_findings: Dict[str, Any]
    recommended_actions: List[str]
    escalation_required: bool
    deduplication_key: str
    acknowledged: bool = False
    acknowledged_at: Optional[str] = None
    acknowledged_by: Optional[str] = None


class BiasAlertManager:
    """
    Manages bias detection alerts.
    
    Features:
    - Alert creation based on risk level
    - Deduplication (avoid duplicate alerts)
    - Escalation tracking
    - Alert history management
    """
    
    def __init__(self, dedup_window_hours: int = 24):
        """
        Initialize alert manager.
        
        Args:
            dedup_window_hours: Deduplication time window in hours
        """
        self.logger = logger
        self.dedup_window = dedup_window_hours
        self.alert_history: List[BiasAlert] = []
        self.active_alerts: Dict[str, BiasAlert] = {}
    
    def create_alert(self,
                    model_id: str,
                    risk_classification: Dict[str, Any],
                    bias_score_data: Dict[str, Any],
                    interpretation_data: Dict[str, Any]) -> BiasAlert:
        """
        Create bias detection alert.
        
        Args:
            model_id: Model identifier
            risk_classification: Risk classification results
            bias_score_data: Bias score calculation results
            interpretation_data: Score interpretation data
            
        Returns:
            BiasAlert object
        """
        try:
            # Generate alert ID
            alert_id = self._generate_alert_id(model_id, risk_classification["risk_level"])
            
            # Generate deduplication key
            dedup_key = self._generate_dedup_key(model_id, risk_classification["risk_level"])
            
            # Check for duplicate
            if self._is_duplicate(dedup_key):
                self.logger.info(f"Duplicate alert suppressed for {model_id}")
                # Return existing alert instead of creating new one
                return self.active_alerts[dedup_key]
            
            # Determine notification channels
            notification_channels = risk_classification.get("notification_channels", ["in_app"])
            
            # Determine priority
            priority_map = {
                "LOW": "low",
                "MEDIUM": "medium",
                "HIGH": "high",
                "CRITICAL": "urgent"
            }
            priority = priority_map.get(risk_classification["risk_level"], "medium")
            
            # Generate alert message
            alert_message = self._generate_alert_message(
                model_id, risk_classification, interpretation_data
            )
            
            # Extract detailed findings
            detailed_findings = {
                "overall_bias_score": bias_score_data.get("overall_bias_score", 0.0),
                "confidence_interval": bias_score_data.get("confidence_interval", [0.0, 0.0]),
                "dominant_metric": bias_score_data.get("dominant_metric", "unknown"),
                "metric_contributions": bias_score_data.get("metric_contributions", {}),
                "severity_level": interpretation_data.get("severity_level", "UNKNOWN"),
                "key_concerns": interpretation_data.get("key_concerns", []),
                "regulatory_flags": risk_classification.get("regulatory_flags", [])
            }
            
            # Generate recommendations
            recommended_actions = self._generate_recommended_actions(
                risk_classification, interpretation_data
            )
            
            # Create alert
            alert = BiasAlert(
                alert_id=alert_id,
                model_id=model_id,
                risk_level=risk_classification["risk_level"],
                bias_score=bias_score_data.get("overall_bias_score", 0.0),
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                notification_channels=notification_channels,
                priority=priority,
                alert_message=alert_message,
                detailed_findings=detailed_findings,
                recommended_actions=recommended_actions,
                escalation_required=risk_classification.get("escalation_required", False),
                deduplication_key=dedup_key
            )
            
            # Store alert
            self.alert_history.append(alert)
            self.active_alerts[dedup_key] = alert
            
            self.logger.info(f"Created {priority} priority alert {alert_id} for model {model_id}")
            
            return alert
            
        except Exception as e:
            self.logger.error(f"Alert creation failed: {e}")
            raise
    
    def _generate_alert_id(self, model_id: str, risk_level: str) -> str:
        """Generate unique alert ID."""
        timestamp = int(time.time() * 1000)  # Milliseconds
        return f"ALERT_{model_id}_{risk_level}_{timestamp}"
    
    def _generate_dedup_key(self, model_id: str, risk_level: str) -> str:
        """Generate deduplication key."""
        date_str = datetime.now().strftime("%Y%m%d")
        key = f"{model_id}_{risk_level}_{date_str}"
        return hashlib.md5(key.encode()).hexdigest()[:16]
    
    def _is_duplicate(self, dedup_key: str) -> bool:
        """Check if alert is a duplicate within dedup window."""
        if dedup_key not in self.active_alerts:
            return False
        
        # Check if existing alert is within dedup window
        existing_alert = self.active_alerts[dedup_key]
        alert_time = datetime.strptime(existing_alert.timestamp, "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.now() - alert_time
        
        return time_diff < timedelta(hours=self.dedup_window)
    
    def _generate_alert_message(self,
                                model_id: str,
                                risk_classification: Dict[str, Any],
                                interpretation_data: Dict[str, Any]) -> str:
        """Generate human-readable alert message."""
        risk_level = risk_classification["risk_level"]
        severity = interpretation_data.get("severity_level", "UNKNOWN")
        
        messages = {
            "LOW": f"Routine bias check for model {model_id}: {severity} severity detected.",
            "MEDIUM": f"Moderate bias detected in model {model_id}. Review recommended within 30 days.",
            "HIGH": f"⚠️ Significant bias detected in model {model_id}. Remediation required within 14 days.",
            "CRITICAL": f"🚨 CRITICAL: Severe bias detected in model {model_id}. Immediate action required!"
        }
        
        return messages.get(risk_level, f"Bias alert for model {model_id}")
    
    def _generate_recommended_actions(self,
                                     risk_classification: Dict[str, Any],
                                     interpretation_data: Dict[str, Any]) -> List[str]:
        """Generate recommended actions based on alert."""
        actions = []
        risk_level = risk_classification["risk_level"]
        
        if risk_level == "LOW":
            actions.append("Continue routine monitoring")
            actions.append(f"Next review: {risk_classification.get('review_frequency', 'Quarterly')}")
        
        elif risk_level == "MEDIUM":
            actions.append("Review model fairness metrics within 30 days")
            actions.append("Investigate primary bias driver from key concerns")
            actions.append("Consider bias mitigation techniques")
        
        elif risk_level == "HIGH":
            actions.append("Immediate review of model fairness required")
            actions.append("Implement bias mitigation within 14 days")
            actions.append("Notify compliance team")
            actions.append("Consider suspending model deployment")
        
        elif risk_level == "CRITICAL":
            actions.append("⚠️ STOP: Suspend model deployment immediately")
            actions.append("Escalate to executive team")
            actions.append("Initiate emergency bias remediation")
            actions.append("Prepare regulatory compliance report")
            actions.append("Review training data for bias sources")
        
        # Add concern-specific actions
        key_concerns = interpretation_data.get("key_concerns", [])
        for concern in key_concerns[:2]:  # Top 2 concerns
            if "demographic parity" in concern.lower():
                actions.append("Address demographic parity violation through reweighting or resampling")
            elif "equalized odds" in concern.lower():
                actions.append("Implement fairness constraints to equalize error rates")
            elif "calibration" in concern.lower():
                actions.append("Apply Platt scaling or isotonic regression for better calibration")
            elif "individual fairness" in concern.lower():
                actions.append("Review similar case handling for consistency")
        
        return actions
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """
        Mark alert as acknowledged.
        
        Args:
            alert_id: Alert ID to acknowledge
            acknowledged_by: User who acknowledged the alert
            
        Returns:
            True if successful
        """
        try:
            for alert in self.alert_history:
                if alert.alert_id == alert_id:
                    alert.acknowledged = True
                    alert.acknowledged_at = time.strftime("%Y-%m-%d %H:%M:%S")
                    alert.acknowledged_by = acknowledged_by
                    self.logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
                    return True
            
            self.logger.warning(f"Alert {alert_id} not found")
            return False
            
        except Exception as e:
            self.logger.error(f"Alert acknowledgment failed: {e}")
            return False
    
    def get_active_alerts(self, model_id: Optional[str] = None) -> List[BiasAlert]:
        """
        Get active alerts (within dedup window).
        
        Args:
            model_id: Filter by model ID (optional)
            
        Returns:
            List of active alerts
        """
        active = []
        cutoff_time = datetime.now() - timedelta(hours=self.dedup_window)
        
        for alert in self.alert_history:
            alert_time = datetime.strptime(alert.timestamp, "%Y-%m-%d %H:%M:%S")
            if alert_time > cutoff_time:
                if model_id is None or alert.model_id == model_id:
                    active.append(alert)
        
        return active
    
    def to_dict(self, alert: BiasAlert) -> Dict[str, Any]:
        """Convert alert to dictionary for JSON serialization."""
        return asdict(alert)


def main():
    """Test the bias alert manager."""
    print("🧪 Testing Bias Alert Manager")
    
    # Create alert manager
    manager = BiasAlertManager(dedup_window_hours=24)
    
    # Mock data
    risk_classification = {
        "risk_level": "HIGH",
        "risk_score": 0.68,
        "notification_channels": ["in_app", "email", "webhook"],
        "escalation_required": True,
        "review_frequency": "Weekly",
        "regulatory_flags": ["EU_AI_ACT", "GDPR"]
    }
    
    bias_score_data = {
        "overall_bias_score": 0.68,
        "confidence_interval": [0.65, 0.71],
        "dominant_metric": "equalized_odds",
        "metric_contributions": {
            "demographic_parity": 0.105,
            "equalized_odds": 0.238,
            "calibration": 0.112,
            "individual_fairness": 0.225
        }
    }
    
    interpretation_data = {
        "severity_level": "POOR",
        "key_concerns": [
            "Equalized odds violation (52%) exceeds threshold",
            "Individual fairness inconsistency (40%) detected"
        ]
    }
    
    # Create alert
    alert = manager.create_alert(
        "credit_model_v3",
        risk_classification,
        bias_score_data,
        interpretation_data
    )
    
    print("✅ Alert created successfully")
    print(f"✅ Alert ID: {alert.alert_id}")
    print(f"✅ Priority: {alert.priority}")
    print(f"✅ Message: {alert.alert_message}")
    print(f"✅ Channels: {alert.notification_channels}")
    print(f"✅ Actions ({len(alert.recommended_actions)}): {alert.recommended_actions[:2]}")
    
    # Test deduplication
    alert2 = manager.create_alert(
        "credit_model_v3",
        risk_classification,
        bias_score_data,
        interpretation_data
    )
    print(f"✅ Deduplication test: {'Same alert' if alert.alert_id == alert2.alert_id else 'New alert'}")
    
    # Acknowledge alert
    success = manager.acknowledge_alert(alert.alert_id, "john.doe@regiq.com")
    print(f"✅ Alert acknowledged: {success}")
    
    # Get active alerts
    active_alerts = manager.get_active_alerts()
    print(f"✅ Active alerts: {len(active_alerts)}")


if __name__ == "__main__":
    main()
