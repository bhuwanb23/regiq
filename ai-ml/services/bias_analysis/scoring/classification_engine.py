#!/usr/bin/env python3
"""
REGIQ AI/ML - Risk Classification Engine
Classifies bias scores into risk levels with context-aware rules and overrides.
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple

from .risk_levels import RiskLevel, get_risk_level_from_score, get_risk_metadata, get_risk_threshold_info


logger = logging.getLogger("classification_engine")


class RiskClassifier:
    """
    Classifies bias scores into risk levels.
    
    Features:
    - Score-based classification
    - Conditional overrides (e.g., auto-escalate if DP > 0.8)
    - Regulatory context adjustments
    - Industry-specific rules
    """
    
    def __init__(self, rules_config_path: Optional[str] = None):
        """
        Initialize risk classifier.
        
        Args:
            rules_config_path: Path to classification rules YAML (optional)
        """
        self.logger = logger
        
        # Load classification rules
        if rules_config_path is None:
            base_dir = Path(__file__).parent.parent.parent.parent
            rules_config_path = str(base_dir / "config" / "classification_rules.yaml")
        
        self.rules_config_path = Path(rules_config_path)
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        """Load classification rules from YAML."""
        try:
            if not self.rules_config_path.exists():
                self.logger.warning(f"Rules config not found: {self.rules_config_path}, using defaults")
                return self._get_default_rules()
            
            with open(self.rules_config_path, 'r') as f:
                rules = yaml.safe_load(f)
            
            self.logger.info(f"Loaded classification rules from {self.rules_config_path}")
            return rules
            
        except Exception as e:
            self.logger.error(f"Failed to load rules: {e}, using defaults")
            return self._get_default_rules()
    
    def _get_default_rules(self) -> Dict:
        """Get default classification rules."""
        return {
            "base_rules": {
                "LOW": {"score_range": [0.0, 0.25]},
                "MEDIUM": {"score_range": [0.26, 0.50]},
                "HIGH": {"score_range": [0.51, 0.75]},
                "CRITICAL": {"score_range": [0.76, 1.0]}
            },
            "override_rules": {},
            "regulatory_rules": {},
            "industry_rules": {}
        }
    
    def classify_risk(self,
                     bias_score: float,
                     metric_breakdown: Dict[str, float],
                     regulatory_context: Optional[str] = None,
                     industry: Optional[str] = None) -> Dict[str, Any]:
        """
        Classify bias score into risk level.
        
        Args:
            bias_score: Composite bias score
            metric_breakdown: Individual metric scores
            regulatory_context: Regulatory context (e.g., "eu_ai_act_high_risk")
            industry: Industry context (e.g., "lending")
            
        Returns:
            Dictionary with classification results
        """
        try:
            # Step 1: Base classification from score
            base_risk_level = self._classify_from_score(bias_score, regulatory_context)
            
            # Step 2: Check for override rules
            override_applied, override_result = self._check_override_rules(
                base_risk_level, bias_score, metric_breakdown
            )
            
            if override_applied and override_result:
                final_risk_level = override_result["escalated_level"]
                override_reason = override_result["reason"]
            else:
                final_risk_level = base_risk_level
                override_reason = None
            
            # Step 3: Get risk metadata
            metadata = get_risk_metadata(final_risk_level)
            threshold_info = get_risk_threshold_info(final_risk_level)
            
            # Step 4: Determine urgency and regulatory flags
            regulatory_flags = self._get_regulatory_flags(
                final_risk_level, regulatory_context
            )
            
            return {
                "risk_level": final_risk_level.value,
                "risk_score": bias_score,
                "base_classification": base_risk_level.value,
                "classification_reason": f"Score {bias_score:.3f} falls in {base_risk_level.value} range",
                "override_applied": override_applied,
                "override_reason": override_reason,
                "action_timeline": threshold_info["action_timeline"],
                "action_days": threshold_info["action_days"],
                "urgency": metadata["urgency"],
                "regulatory_flags": regulatory_flags,
                "notification_channels": metadata["notification_channels"],
                "stakeholder_notification": metadata["stakeholder_notification"],
                "escalation_required": metadata["escalation_required"],
                "deployment_recommendation": metadata["deployment_recommendation"],
                "review_frequency": metadata["review_frequency"],
                "regulatory_context": regulatory_context,
                "industry_context": industry
            }
            
        except Exception as e:
            self.logger.error(f"Risk classification failed: {e}")
            return {
                "risk_level": "UNKNOWN",
                "risk_score": bias_score,
                "error": str(e)
            }
    
    def _classify_from_score(self,
                            bias_score: float,
                            regulatory_context: Optional[str] = None) -> RiskLevel:
        """Classify risk level from bias score."""
        # Check for regulatory-specific thresholds
        if regulatory_context and regulatory_context in self.rules.get("regulatory_rules", {}):
            reg_rules = self.rules["regulatory_rules"][regulatory_context]
            if "score_adjustments" in reg_rules:
                # Use adjusted thresholds
                adjustments = reg_rules["score_adjustments"]
                for level, (min_score, max_score) in adjustments.items():
                    if min_score <= bias_score <= max_score:
                        return RiskLevel[level]
        
        # Use base classification
        return get_risk_level_from_score(bias_score)
    
    def _check_override_rules(self,
                             base_risk_level: RiskLevel,
                             bias_score: float,
                             metric_breakdown: Dict[str, float]) -> Tuple[bool, Optional[Dict]]:
        """
        Check if any override rules apply.
        
        Args:
            base_risk_level: Base classification
            bias_score: Overall bias score
            metric_breakdown: Individual metrics
            
        Returns:
            Tuple of (override_applied, override_result)
        """
        override_rules = self.rules.get("override_rules", {})
        
        for rule_name, rule_config in override_rules.items():
            condition = rule_config.get("condition", "")
            
            # Check if condition is met
            if self._evaluate_condition(condition, bias_score, metric_breakdown):
                escalate_to = rule_config.get("escalate_to") or rule_config.get("de_escalate_to")
                if escalate_to:
                    return (True, {
                        "escalated_level": RiskLevel[escalate_to],
                        "rule_name": rule_name,
                        "reason": rule_config.get("reason", "Override rule triggered"),
                        "priority": rule_config.get("priority", 999)
                    })
        
        return (False, None)
    
    def _evaluate_condition(self,
                           condition: str,
                           bias_score: float,
                           metric_breakdown: Dict[str, float]) -> bool:
        """
        Evaluate a condition string.
        
        Args:
            condition: Condition string (e.g., "demographic_parity > 0.80")
            bias_score: Overall score
            metric_breakdown: Individual metrics
            
        Returns:
            True if condition is met
        """
        try:
            # Handle simple comparisons
            if ">" in condition:
                metric, threshold = condition.split(">")
                metric = metric.strip()
                threshold = float(threshold.strip())
                
                if metric in metric_breakdown:
                    return metric_breakdown[metric] > threshold
            
            # Handle count-based conditions
            if "count" in condition:
                # Example: "count(metric > 0.60) >= 2"
                import re
                match = re.search(r"count\(metric > ([\d.]+)\) >= (\d+)", condition)
                if match:
                    threshold = float(match.group(1))
                    required_count = int(match.group(2))
                    count = sum(1 for val in metric_breakdown.values() if val > threshold)
                    return count >= required_count
            
            # Handle all() conditions
            if "all(" in condition:
                # Example: "all(metric < 0.30)"
                import re
                match = re.search(r"all\(metric < ([\d.]+)\)", condition)
                if match:
                    threshold = float(match.group(1))
                    return all(val < threshold for val in metric_breakdown.values())
            
            return False
            
        except Exception as e:
            self.logger.warning(f"Condition evaluation failed: {e}")
            return False
    
    def _get_regulatory_flags(self,
                             risk_level: RiskLevel,
                             regulatory_context: Optional[str] = None) -> List[str]:
        """Get regulatory flags based on risk level and context."""
        flags = []
        
        if risk_level == RiskLevel.CRITICAL:
            flags.append("REGULATORY_VIOLATION")
            flags.append("DEPLOYMENT_BLOCKED")
        elif risk_level == RiskLevel.HIGH:
            flags.append("COMPLIANCE_RISK")
            flags.append("REMEDIATION_REQUIRED")
        
        if regulatory_context:
            if "eu_ai_act" in regulatory_context.lower():
                flags.append("EU_AI_ACT")
            if "gdpr" in regulatory_context.lower():
                flags.append("GDPR")
            if "fair_credit" in regulatory_context.lower():
                flags.append("FCRA")
        
        return flags


def main():
    """Test the risk classifier."""
    print("🧪 Testing Risk Classifier")
    
    # Create classifier
    classifier = RiskClassifier()
    
    # Test cases
    test_cases = [
        {
            "name": "Low bias",
            "score": 0.20,
            "metrics": {
                "demographic_parity": 0.15,
                "equalized_odds": 0.18,
                "calibration": 0.12,
                "individual_fairness": 0.10
            }
        },
        {
            "name": "High bias with DP override",
            "score": 0.55,
            "metrics": {
                "demographic_parity": 0.85,  # Should trigger override
                "equalized_odds": 0.40,
                "calibration": 0.30,
                "individual_fairness": 0.25
            }
        },
        {
            "name": "Critical bias",
            "score": 0.82,
            "metrics": {
                "demographic_parity": 0.75,
                "equalized_odds": 0.80,
                "calibration": 0.65,
                "individual_fairness": 0.50
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        result = classifier.classify_risk(
            test_case["score"],
            test_case["metrics"],
            regulatory_context="eu_ai_act_high_risk"
        )
        
        print(f"✅ Risk Level: {result['risk_level']}")
        print(f"✅ Override Applied: {result['override_applied']}")
        if result['override_applied']:
            print(f"   Reason: {result['override_reason']}")
        print(f"✅ Action Timeline: {result['action_timeline']}")
        print(f"✅ Urgency: {result['urgency']}")


if __name__ == "__main__":
    main()
