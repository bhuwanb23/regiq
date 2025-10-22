#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Risk Report Generator
Generates comprehensive JSON-structured risk reports with visualization data.
"""

import sys
import logging
import time
from pathlib import Path
from typing import Dict, Optional, List, Any

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.gemini_config import GeminiAPIManager
from .llm_prompts import get_recommendations_prompt, get_executive_summary_prompt


logger = logging.getLogger("bias_risk_report_generator")


class BiasRiskReportGenerator:
    """
    Generates bias risk reports in structured JSON format.
    
    Report includes:
    - Executive summary (LLM-generated)
    - Detailed analysis
    - Visualization data structures
    - Actionable recommendations
    - Regulatory compliance checklist
    """
    
    def __init__(self, use_llm: bool = True):
        """
        Initialize report generator.
        
        Args:
            use_llm: Whether to use LLM for narrative generation
        """
        self.logger = logger
        self.use_llm = use_llm
        
        if use_llm:
            try:
                self.llm_manager = GeminiAPIManager()
                self.logger.info("Initialized Gemini LLM for report generation")
            except Exception as e:
                self.logger.warning(f"Failed to initialize LLM: {e}")
                self.use_llm = False
    
    def generate_report_data(self,
                            model_id: str,
                            bias_score_data: Dict[str, Any],
                            risk_classification: Dict[str, Any],
                            interpretation_data: Dict[str, Any],
                            alert_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate comprehensive bias risk report in JSON format.
        
        Args:
            model_id: Model identifier
            bias_score_data: Bias score calculation results
            risk_classification: Risk classification results
            interpretation_data: Score interpretation data
            alert_data: Alert information (optional)
            
        Returns:
            Dictionary with complete report data
        """
        try:
            report_id = self._generate_report_id(model_id)
            
            # Generate executive summary
            executive_summary = self._generate_executive_summary(
                model_id, bias_score_data, risk_classification, interpretation_data
            )
            
            # Detailed analysis
            detailed_analysis = self._generate_detailed_analysis(
                bias_score_data, risk_classification, interpretation_data
            )
            
            # Visualization data
            visualizations = self._generate_visualization_data(
                bias_score_data, risk_classification, interpretation_data
            )
            
            # Recommendations
            recommendations = self._generate_recommendations(
                bias_score_data, risk_classification, interpretation_data
            )
            
            # Regulatory compliance
            compliance_checklist = self._generate_compliance_checklist(
                risk_classification, interpretation_data
            )
            
            # Appendix
            appendix = self._generate_appendix(
                bias_score_data, risk_classification
            )
            
            # Complete report structure
            report = {
                "report_id": report_id,
                "model_id": model_id,
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "report_type": "bias_risk_assessment",
                "executive_summary": executive_summary,
                "detailed_analysis": detailed_analysis,
                "visualizations": visualizations,
                "recommendations": recommendations,
                "compliance_checklist": compliance_checklist,
                "appendix": appendix,
                "alert_info": alert_data if alert_data else None,
                "metadata": {
                    "report_version": "1.0",
                    "llm_used": self.use_llm,
                    "generation_method": "automated"
                }
            }
            
            self.logger.info(f"Generated report {report_id} for model {model_id}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return {
                "report_id": "ERROR",
                "model_id": model_id,
                "error": str(e)
            }
    
    def _generate_report_id(self, model_id: str) -> str:
        """Generate unique report ID."""
        timestamp = int(time.time())
        return f"REPORT_{model_id}_{timestamp}"
    
    def _generate_executive_summary(self,
                                    model_id: str,
                                    bias_score_data: Dict[str, Any],
                                    risk_classification: Dict[str, Any],
                                    interpretation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary section."""
        bias_score = bias_score_data.get("overall_bias_score", 0.0)
        risk_level = risk_classification.get("risk_level", "UNKNOWN")
        key_findings = interpretation_data.get("interpretation", "")
        
        # Generate LLM summary if available
        llm_summary = None
        if self.use_llm and key_findings:
            prompt = get_executive_summary_prompt(model_id, bias_score, risk_level, key_findings)
            response = self.llm_manager.generate_content(prompt, temperature=0.3, max_tokens=200)
            if response:
                llm_summary = response.strip()
        
        return {
            "overall_bias_score": bias_score,
            "risk_classification": risk_level,
            "severity_level": interpretation_data.get("severity_level", "UNKNOWN"),
            "key_findings": [
                interpretation_data.get("interpretation", "No interpretation available"),
                f"Primary concern: {bias_score_data.get('dominant_metric', 'unknown')}",
                f"Action required: {risk_classification.get('action_timeline', 'immediate')}"
            ],
            "llm_summary": llm_summary,
            "action_urgency": risk_classification.get("urgency", "MEDIUM")
        }
    
    def _generate_detailed_analysis(self,
                                    bias_score_data: Dict[str, Any],
                                    risk_classification: Dict[str, Any],
                                    interpretation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed analysis section."""
        return {
            "metric_breakdown": {
                "normalized_metrics": bias_score_data.get("normalized_metrics", {}),
                "raw_metrics": bias_score_data.get("raw_metrics", {}),
                "metric_contributions": bias_score_data.get("metric_contributions", {})
            },
            "protected_groups_affected": self._identify_affected_groups(interpretation_data),
            "feature_contributions": {
                "dominant_metric": bias_score_data.get("dominant_metric", "unknown"),
                "dominant_contribution": bias_score_data.get("dominant_contribution", 0.0),
                "secondary_concerns": interpretation_data.get("key_concerns", [])
            },
            "confidence_analysis": {
                "confidence_interval": bias_score_data.get("confidence_interval", [0.0, 0.0]),
                "confidence_level": 0.95,
                "score_stability": self._assess_stability(bias_score_data)
            },
            "regulatory_assessment": {
                "flags": risk_classification.get("regulatory_flags", []),
                "context": risk_classification.get("regulatory_context", "None"),
                "compliance_status": risk_classification.get("deployment_recommendation", "Unknown")
            }
        }
    
    def _generate_visualization_data(self,
                                    bias_score_data: Dict[str, Any],
                                    risk_classification: Dict[str, Any],
                                    interpretation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visualization data structures (for frontend rendering)."""
        metric_contributions = bias_score_data.get("metric_contributions", {})
        normalized_metrics = bias_score_data.get("normalized_metrics", {})
        
        return {
            "risk_heatmap_data": {
                "type": "heatmap",
                "metrics": list(normalized_metrics.keys()),
                "values": list(normalized_metrics.values()),
                "threshold": 0.5,
                "colorscale": [[0, "green"], [0.5, "yellow"], [1, "red"]]
            },
            "metric_contributions_chart": {
                "type": "pie",
                "labels": list(metric_contributions.keys()),
                "values": list(metric_contributions.values()),
                "title": "Bias Score Contribution by Metric"
            },
            "score_gauge": {
                "type": "gauge",
                "value": bias_score_data.get("overall_bias_score", 0.0),
                "min": 0.0,
                "max": 1.0,
                "threshold_ranges": [
                    {"range": [0.0, 0.25], "color": "green", "label": "LOW"},
                    {"range": [0.26, 0.50], "color": "yellow", "label": "MEDIUM"},
                    {"range": [0.51, 0.75], "color": "orange", "label": "HIGH"},
                    {"range": [0.76, 1.0], "color": "red", "label": "CRITICAL"}
                ]
            },
            "confidence_interval_chart": {
                "type": "error_bar",
                "value": bias_score_data.get("overall_bias_score", 0.0),
                "confidence_interval": bias_score_data.get("confidence_interval", [0.0, 0.0]),
                "confidence_level": 0.95
            },
            "metric_breakdown_bars": {
                "type": "bar",
                "x_labels": list(normalized_metrics.keys()),
                "y_values": list(normalized_metrics.values()),
                "threshold_line": 0.5,
                "title": "Normalized Fairness Metrics"
            }
        }
    
    def _generate_recommendations(self,
                                 bias_score_data: Dict[str, Any],
                                 risk_classification: Dict[str, Any],
                                 interpretation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations section."""
        # Generate LLM recommendations if available
        llm_recommendations = None
        if self.use_llm:
            prompt = get_recommendations_prompt(
                bias_score_data.get("overall_bias_score", 0.0),
                risk_classification.get("risk_level", "MEDIUM"),
                bias_score_data.get("normalized_metrics", {}),
                risk_classification.get("regulatory_context")
            )
            response = self.llm_manager.generate_content(prompt, temperature=0.3, max_tokens=400)
            if response:
                llm_recommendations = response.strip()
        
        # Template-based recommendations
        immediate_actions = self._get_immediate_actions(risk_classification)
        long_term_strategies = self._get_long_term_strategies(bias_score_data, interpretation_data)
        
        return {
            "immediate_actions": immediate_actions,
            "short_term_strategies": self._get_short_term_strategies(interpretation_data),
            "long_term_strategies": long_term_strategies,
            "llm_recommendations": llm_recommendations,
            "timeline": {
                "immediate": "0-7 days",
                "short_term": "7-30 days",
                "long_term": "30+ days"
            }
        }
    
    def _generate_compliance_checklist(self,
                                      risk_classification: Dict[str, Any],
                                      interpretation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate regulatory compliance checklist."""
        regulatory_flags = risk_classification.get("regulatory_flags", [])
        
        checklist = {
            "gdpr_compliance": {
                "status": "PASS" if "REGULATORY_VIOLATION" not in regulatory_flags else "FAIL",
                "requirements": [
                    "Right to explanation implemented",
                    "Consent for automated decision-making",
                    "Data protection impact assessment",
                    "Bias monitoring in place"
                ]
            },
            "eu_ai_act_compliance": {
                "status": "PASS" if risk_classification.get("risk_level") not in ["HIGH", "CRITICAL"] else "FAIL",
                "requirements": [
                    "Risk assessment documentation",
                    "Human oversight mechanisms",
                    "Bias testing and mitigation",
                    "Transparency and explainability"
                ]
            },
            "fair_credit_compliance": {
                "status": "PASS" if "FCRA" not in regulatory_flags else "REVIEW_NEEDED",
                "requirements": [
                    "Equal opportunity in credit decisions",
                    "Adverse action notices",
                    "Model fairness documentation",
                    "Disparate impact testing"
                ]
            }
        }
        
        return checklist
    
    def _generate_appendix(self,
                          bias_score_data: Dict[str, Any],
                          risk_classification: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appendix with raw data and methodology."""
        return {
            "raw_metrics": bias_score_data.get("raw_metrics", {}),
            "statistical_analysis": {
                "confidence_interval": bias_score_data.get("confidence_interval", [0.0, 0.0]),
                "weight_profile": bias_score_data.get("weight_profile_used", "default"),
                "weights_applied": bias_score_data.get("weights", {})
            },
            "methodology": {
                "scoring_algorithm": "weighted_composite_sum",
                "normalization_method": "min_max_scaling",
                "confidence_estimation": "bootstrap_resampling",
                "classification_rules": "threshold_based_with_overrides"
            },
            "data_sources": {
                "demographic_parity": "Phase 3.2 - Demographic Parity Analyzer",
                "equalized_odds": "Phase 3.2 - Equalized Odds Analyzer",
                "calibration": "Phase 3.2 - Calibration Analyzer",
                "individual_fairness": "Phase 3.2 - Individual Fairness Analyzer"
            }
        }
    
    def _identify_affected_groups(self, interpretation_data: Dict[str, Any]) -> List[str]:
        """Identify which protected groups are most affected."""
        # Placeholder - would extract from Phase 3.2 results in real implementation
        key_concerns = interpretation_data.get("key_concerns", [])
        affected_groups = []
        
        for concern in key_concerns:
            if "demographic parity" in concern.lower():
                affected_groups.append("Groups with unequal positive rates detected")
            if "equalized odds" in concern.lower():
                affected_groups.append("Groups with unequal error rates detected")
        
        return affected_groups if affected_groups else ["All groups - general fairness concerns"]
    
    def _assess_stability(self, bias_score_data: Dict[str, Any]) -> str:
        """Assess score stability from confidence interval."""
        ci = bias_score_data.get("confidence_interval", [0.0, 0.0])
        width = ci[1] - ci[0] if len(ci) == 2 else 0.0
        
        if width < 0.05:
            return "HIGH - Score is stable"
        elif width < 0.10:
            return "MEDIUM - Score has moderate variance"
        else:
            return "LOW - Score is unstable, additional data recommended"
    
    def _get_immediate_actions(self, risk_classification: Dict[str, Any]) -> List[str]:
        """Get immediate action items based on risk level."""
        risk_level = risk_classification.get("risk_level", "LOW")
        
        actions_map = {
            "LOW": ["Continue monitoring", "Schedule next review"],
            "MEDIUM": ["Review model fairness", "Document findings", "Plan mitigation if needed"],
            "HIGH": ["Suspend deployment if not yet deployed", "Initiate bias mitigation", "Notify compliance team"],
            "CRITICAL": ["STOP all deployments immediately", "Escalate to executive team", "Begin emergency remediation"]
        }
        
        return actions_map.get(risk_level, [])
    
    def _get_short_term_strategies(self, interpretation_data: Dict[str, Any]) -> List[str]:
        """Get short-term strategies."""
        return [
            "Implement monitoring dashboard for bias metrics",
            "Set up automated alerts for metric changes",
            "Review training data for bias sources",
            "Consider temporary fairness constraints"
        ]
    
    def _get_long_term_strategies(self,
                                  bias_score_data: Dict[str, Any],
                                  interpretation_data: Dict[str, Any]) -> List[str]:
        """Get long-term strategies."""
        dominant = bias_score_data.get("dominant_metric", "")
        
        strategies = [
            "Implement comprehensive bias testing in CI/CD pipeline",
            "Establish regular fairness auditing schedule",
            "Invest in diverse training data collection",
            "Train team on fairness-aware machine learning"
        ]
        
        if "demographic_parity" in dominant:
            strategies.append("Implement algorithmic reweighting or resampling techniques")
        elif "equalized_odds" in dominant:
            strategies.append("Apply fairness constraints during model training")
        elif "calibration" in dominant:
            strategies.append("Invest in better model calibration techniques")
        
        return strategies


def main():
    """Test the bias risk report generator."""
    print("🧪 Testing Bias Risk Report Generator")
    
    # Create generator
    generator = BiasRiskReportGenerator(use_llm=True)
    
    # Mock data
    bias_score_data = {
        "overall_bias_score": 0.68,
        "confidence_interval": [0.65, 0.71],
        "normalized_metrics": {
            "demographic_parity": 0.35,
            "equalized_odds": 0.52,
            "calibration": 0.28,
            "individual_fairness": 0.40
        },
        "metric_contributions": {
            "demographic_parity": 0.105,
            "equalized_odds": 0.182,
            "calibration": 0.056,
            "individual_fairness": 0.137
        },
        "dominant_metric": "equalized_odds",
        "dominant_contribution": 0.182,
        "weight_profile_used": "default",
        "weights": {
            "demographic_parity": 0.30,
            "equalized_odds": 0.35,
            "calibration": 0.20,
            "individual_fairness": 0.15
        },
        "raw_metrics": {
            "demographic_parity": 0.35,
            "equalized_odds": 0.52,
            "calibration": 0.28,
            "individual_fairness": 0.60
        }
    }
    
    risk_classification = {
        "risk_level": "HIGH",
        "risk_score": 0.68,
        "urgency": "HIGH",
        "action_timeline": "14_days",
        "regulatory_flags": ["COMPLIANCE_RISK", "REMEDIATION_REQUIRED"],
        "regulatory_context": "eu_ai_act_high_risk",
        "deployment_recommendation": "Not recommended - remediation first"
    }
    
    interpretation_data = {
        "severity_level": "POOR",
        "interpretation": "The model exhibits significant bias requiring immediate attention.",
        "key_concerns": [
            "Equalized odds violation (52%) exceeds threshold",
            "Individual fairness inconsistency (40%) detected"
        ]
    }
    
    # Generate report
    report = generator.generate_report_data(
        "credit_model_v3",
        bias_score_data,
        risk_classification,
        interpretation_data
    )
    
    print("✅ Report generated successfully")
    print(f"✅ Report ID: {report['report_id']}")
    print(f"✅ Sections: {list(report.keys())}")
    print(f"✅ Executive summary keys: {list(report['executive_summary'].keys())}")
    print(f"✅ Visualizations: {list(report['visualizations'].keys())}")
    print(f"✅ Recommendations: {len(report['recommendations']['immediate_actions'])} immediate actions")


if __name__ == "__main__":
    main()
