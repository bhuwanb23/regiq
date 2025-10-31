#!/usr/bin/env python3
"""
REGIQ AI/ML - Executive Metrics Display
Executive-level metrics and KPI display for C-suite dashboards.

This module provides:
- Key performance indicator calculation
- Executive dashboard metrics
- Business-focused metric presentation
- Trend analysis and scoring

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from ..base.base_template import ReportData

# Configure logging
logger = logging.getLogger(__name__)


class ExecutiveMetricsDisplay:
    """
    Executive metrics display builder for C-suite KPI dashboards.
    
    Focuses on business-relevant metrics and strategic indicators
    that matter to executive decision-making.
    """
    
    def __init__(self):
        """Initialize executive metrics display."""
        self.logger = logging.getLogger(__name__)
    
    def build_executive_metrics(self, data: ReportData) -> Dict[str, Any]:
        """
        Build executive-level metrics from all data sources.
        
        Args:
            data: Report data from Phase 2-4
            
        Returns:
            Executive metrics dictionary
        """
        try:
            metrics = {}
            
            # Core business metrics
            metrics.update(self._calculate_core_metrics(data))
            
            # Risk metrics
            metrics.update(self._calculate_risk_metrics(data))
            
            # Compliance metrics
            metrics.update(self._calculate_compliance_metrics(data))
            
            # Performance metrics
            metrics.update(self._calculate_performance_metrics(data))
            
            # Financial metrics
            metrics.update(self._calculate_financial_metrics(data))
            
            self.logger.info(f"Built {len(metrics)} executive metrics")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to build executive metrics: {str(e)}")
            return self._get_fallback_metrics()
    
    def _calculate_core_metrics(self, data: ReportData) -> Dict[str, float]:
        """Calculate core business metrics."""
        try:
            metrics = {}
            
            # Overall Health Score (0-1)
            health_components = []
            
            if data.regulatory_data:
                reg_score = data.regulatory_data.get("summary", {}).get("compliance_score", 0.0)
                health_components.append(reg_score)
            
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 0.0)
                health_components.append(bias_score)
            
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                risk_score = 1.0 - risk_prob  # Convert to positive score
                health_components.append(risk_score)
            
            metrics["overall_health_score"] = (
                sum(health_components) / len(health_components) 
                if health_components else 0.0
            )
            
            # Operational Excellence Score
            metrics["operational_excellence"] = self._calculate_operational_excellence(data)
            
            # Strategic Readiness Score
            metrics["strategic_readiness"] = self._calculate_strategic_readiness(data)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to calculate core metrics: {str(e)}")
            return {}
    
    def _calculate_risk_metrics(self, data: ReportData) -> Dict[str, float]:
        """Calculate risk-related metrics."""
        try:
            metrics = {}
            
            # Regulatory Risk Score
            if data.regulatory_data:
                reg_risk = data.regulatory_data.get("risk_assessment", {})
                risk_score = reg_risk.get("risk_score", 0.0)
                metrics["regulatory_risk_score"] = risk_score
            
            # AI Bias Risk Score
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {})
                overall_score = bias_score.get("overall_score", 1.0)
                # Convert to risk score (lower fairness = higher risk)
                metrics["ai_bias_risk_score"] = 1.0 - overall_score
            
            # Predicted Compliance Risk
            if data.risk_simulation_data:
                risk_metrics = data.risk_simulation_data.get("risk_metrics", {})
                risk_prob = risk_metrics.get("risk_probability", 0.0)
                metrics["compliance_violation_risk"] = risk_prob
            
            # Composite Risk Score
            risk_scores = [v for k, v in metrics.items() if "risk" in k]
            if risk_scores:
                metrics["composite_risk_score"] = sum(risk_scores) / len(risk_scores)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to calculate risk metrics: {str(e)}")
            return {}
    
    def _calculate_compliance_metrics(self, data: ReportData) -> Dict[str, float]:
        """Calculate compliance-related metrics."""
        try:
            metrics = {}
            
            # Regulatory Compliance Rate
            if data.regulatory_data:
                compliance_status = data.regulatory_data.get("compliance_status", {})
                compliant = compliance_status.get("compliant_count", 0)
                non_compliant = compliance_status.get("non_compliant_count", 0)
                total = compliant + non_compliant
                
                if total > 0:
                    metrics["regulatory_compliance_rate"] = compliant / total
                
                # Overall compliance score
                metrics["compliance_effectiveness"] = data.regulatory_data.get("summary", {}).get("compliance_score", 0.0)
            
            # AI Fairness Compliance
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {})
                fairness_score = bias_score.get("overall_score", 0.0)
                
                # Convert to compliance metric (>0.8 = compliant)
                metrics["ai_fairness_compliance"] = min(fairness_score / 0.8, 1.0)
            
            # Predictive Compliance Score
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                # Higher risk probability = lower compliance score
                metrics["predictive_compliance_score"] = 1.0 - risk_prob
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to calculate compliance metrics: {str(e)}")
            return {}
    
    def _calculate_performance_metrics(self, data: ReportData) -> Dict[str, float]:
        """Calculate performance-related metrics."""
        try:
            metrics = {}
            
            # Model Performance (if available)
            if data.bias_analysis_data:
                model_info = data.bias_analysis_data.get("model_info", {})
                performance_metrics = model_info.get("performance_metrics", {})
                
                if "accuracy" in performance_metrics:
                    metrics["model_accuracy"] = performance_metrics["accuracy"]
                if "precision" in performance_metrics:
                    metrics["model_precision"] = performance_metrics["precision"]
                if "recall" in performance_metrics:
                    metrics["model_recall"] = performance_metrics["recall"]
            
            # System Reliability Score
            metrics["system_reliability"] = self._calculate_system_reliability(data)
            
            # Process Efficiency Score
            metrics["process_efficiency"] = self._calculate_process_efficiency(data)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to calculate performance metrics: {str(e)}")
            return {}
    
    def _calculate_financial_metrics(self, data: ReportData) -> Dict[str, float]:
        """Calculate financial impact metrics."""
        try:
            metrics = {}
            
            if data.risk_simulation_data:
                financial_impact = data.risk_simulation_data.get("financial_impact", {})
                
                # Potential financial exposure
                total_impact = financial_impact.get("total_impact", 0.0)
                metrics["financial_exposure"] = total_impact
                
                # Cost-benefit ratios
                remediation_costs = financial_impact.get("remediation_costs", 0.0)
                if remediation_costs > 0 and total_impact > 0:
                    metrics["cost_benefit_ratio"] = total_impact / remediation_costs
                
                # Risk-adjusted financial impact
                if data.risk_simulation_data.get("risk_metrics"):
                    risk_prob = data.risk_simulation_data["risk_metrics"].get("risk_probability", 0.0)
                    metrics["risk_adjusted_exposure"] = total_impact * risk_prob
            
            # ROI on compliance investments (estimated)
            metrics["compliance_roi_estimate"] = self._estimate_compliance_roi(data)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to calculate financial metrics: {str(e)}")
            return {}
    
    def _calculate_operational_excellence(self, data: ReportData) -> float:
        """Calculate operational excellence score."""
        try:
            excellence_factors = []
            
            # Regulatory process excellence
            if data.regulatory_data:
                compliance_score = data.regulatory_data.get("summary", {}).get("compliance_score", 0.0)
                excellence_factors.append(compliance_score)
            
            # AI governance excellence
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 0.0)
                excellence_factors.append(bias_score)
            
            # Risk management excellence
            if data.risk_simulation_data:
                # Lower risk probability indicates better risk management
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                risk_mgmt_score = 1.0 - risk_prob
                excellence_factors.append(risk_mgmt_score)
            
            return sum(excellence_factors) / len(excellence_factors) if excellence_factors else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate operational excellence: {str(e)}")
            return 0.0
    
    def _calculate_strategic_readiness(self, data: ReportData) -> float:
        """Calculate strategic readiness score."""
        try:
            readiness_factors = []
            
            # Compliance readiness
            if data.regulatory_data:
                deadlines = data.regulatory_data.get("deadlines", [])
                urgent_deadlines = len([d for d in deadlines if d.get("priority") == "high"])
                # Lower urgent deadlines = higher readiness
                compliance_readiness = max(0.0, 1.0 - (urgent_deadlines / 10))  # Normalize to 10 max
                readiness_factors.append(compliance_readiness)
            
            # AI readiness
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 0.0)
                readiness_factors.append(bias_score)
            
            # Risk preparedness
            if data.risk_simulation_data:
                mitigation_strategies = data.risk_simulation_data.get("mitigation_strategies", [])
                # More strategies = higher preparedness
                preparedness = min(1.0, len(mitigation_strategies) / 5)  # Normalize to 5 strategies
                readiness_factors.append(preparedness)
            
            return sum(readiness_factors) / len(readiness_factors) if readiness_factors else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate strategic readiness: {str(e)}")
            return 0.0
    
    def _calculate_system_reliability(self, data: ReportData) -> float:
        """Calculate system reliability score."""
        try:
            reliability_factors = []
            
            # Data availability and quality
            data_sources = 0
            if data.regulatory_data:
                data_sources += 1
            if data.bias_analysis_data:
                data_sources += 1
            if data.risk_simulation_data:
                data_sources += 1
            
            data_reliability = data_sources / 3.0  # Normalize to 3 sources
            reliability_factors.append(data_reliability)
            
            # Model performance reliability
            if data.bias_analysis_data:
                model_info = data.bias_analysis_data.get("model_info", {})
                performance = model_info.get("performance_metrics", {})
                
                if performance:
                    # Average of available performance metrics
                    perf_values = [v for v in performance.values() if isinstance(v, (int, float))]
                    if perf_values:
                        avg_performance = sum(perf_values) / len(perf_values)
                        reliability_factors.append(avg_performance)
            
            return sum(reliability_factors) / len(reliability_factors) if reliability_factors else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate system reliability: {str(e)}")
            return 0.0
    
    def _calculate_process_efficiency(self, data: ReportData) -> float:
        """Calculate process efficiency score."""
        try:
            efficiency_factors = []
            
            # Regulatory process efficiency
            if data.regulatory_data:
                compliance_status = data.regulatory_data.get("compliance_status", {})
                compliant = compliance_status.get("compliant_count", 0)
                total_regs = data.regulatory_data.get("summary", {}).get("total_regulations", 1)
                
                reg_efficiency = compliant / total_regs if total_regs > 0 else 0.0
                efficiency_factors.append(reg_efficiency)
            
            # AI process efficiency (bias mitigation effectiveness)
            if data.bias_analysis_data:
                mitigation_results = data.bias_analysis_data.get("mitigation_results", {})
                effectiveness = mitigation_results.get("effectiveness", 0.0)
                efficiency_factors.append(effectiveness)
            
            # Risk management efficiency
            if data.risk_simulation_data:
                # Efficiency based on number of mitigation strategies vs risk level
                strategies = data.risk_simulation_data.get("mitigation_strategies", [])
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                
                if risk_prob > 0:
                    # More strategies for higher risk = higher efficiency
                    strategy_efficiency = min(1.0, len(strategies) / (risk_prob * 10))
                    efficiency_factors.append(strategy_efficiency)
            
            return sum(efficiency_factors) / len(efficiency_factors) if efficiency_factors else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate process efficiency: {str(e)}")
            return 0.0
    
    def _estimate_compliance_roi(self, data: ReportData) -> float:
        """Estimate return on investment for compliance efforts."""
        try:
            # Simple ROI estimation based on risk reduction vs costs
            if data.risk_simulation_data:
                financial_impact = data.risk_simulation_data.get("financial_impact", {})
                potential_fines = financial_impact.get("total_impact", 0.0)
                remediation_costs = financial_impact.get("remediation_costs", 0.0)
                
                if remediation_costs > 0:
                    # ROI = (Avoided costs - Investment) / Investment
                    # Simplified: assume 70% of potential fines avoided
                    avoided_costs = potential_fines * 0.7
                    roi = (avoided_costs - remediation_costs) / remediation_costs
                    return max(0.0, roi)  # Cap at 0 for negative ROI
            
            return 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to estimate compliance ROI: {str(e)}")
            return 0.0
    
    def get_metric_interpretation(self, metric_name: str, value: float) -> Dict[str, str]:
        """
        Get interpretation for a specific metric.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            
        Returns:
            Interpretation dictionary with status and description
        """
        try:
            interpretations = {
                "overall_health_score": {
                    0.8: ("excellent", "System is in excellent health"),
                    0.6: ("good", "System is performing well"),
                    0.4: ("fair", "System needs attention"),
                    0.0: ("poor", "System requires immediate action")
                },
                "compliance_effectiveness": {
                    0.9: ("excellent", "Outstanding compliance performance"),
                    0.8: ("good", "Strong compliance posture"),
                    0.7: ("fair", "Adequate compliance with room for improvement"),
                    0.0: ("poor", "Significant compliance gaps")
                },
                "composite_risk_score": {
                    0.3: ("low", "Low risk exposure"),
                    0.5: ("medium", "Moderate risk requiring monitoring"),
                    0.7: ("high", "High risk requiring action"),
                    1.0: ("critical", "Critical risk requiring immediate intervention")
                }
            }
            
            if metric_name in interpretations:
                thresholds = interpretations[metric_name]
                for threshold in sorted(thresholds.keys(), reverse=True):
                    if value >= threshold:
                        status, description = thresholds[threshold]
                        return {"status": status, "description": description}
            
            # Default interpretation
            return {"status": "unknown", "description": "Metric interpretation not available"}
            
        except Exception as e:
            self.logger.error(f"Failed to interpret metric {metric_name}: {str(e)}")
            return {"status": "error", "description": "Interpretation error"}
    
    def _get_fallback_metrics(self) -> Dict[str, float]:
        """Get fallback metrics when calculation fails."""
        return {
            "overall_health_score": 0.0,
            "operational_excellence": 0.0,
            "strategic_readiness": 0.0,
            "composite_risk_score": 0.0,
            "compliance_effectiveness": 0.0
        }
    
    def __str__(self) -> str:
        """String representation."""
        return "ExecutiveMetricsDisplay()"
