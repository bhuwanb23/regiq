#!/usr/bin/env python3
"""
REGIQ AI/ML - Executive Summary Builder
Executive summary section builder for high-level stakeholder reports.

This module provides:
- Executive summary generation
- Key insights extraction
- Business impact assessment
- Strategic overview creation

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from ..base.base_template import ReportData

# Configure logging
logger = logging.getLogger(__name__)


class ExecutiveSummaryBuilder:
    """
    Builder class for executive summary sections.
    
    Creates high-level summaries suitable for C-suite stakeholders,
    focusing on strategic insights and business impact.
    """
    
    def __init__(self):
        """Initialize executive summary builder."""
        self.logger = logging.getLogger(__name__)
    
    def build_executive_summary(self, data: ReportData) -> Dict[str, Any]:
        """
        Build comprehensive executive summary from all data sources.
        
        Args:
            data: Report data from Phase 2-4
            
        Returns:
            Executive summary data dictionary
        """
        try:
            summary = {
                "overview": self._generate_overview(data),
                "key_points": self._extract_key_points(data),
                "business_impact": self._assess_business_impact(data),
                "strategic_priorities": self._identify_strategic_priorities(data),
                "executive_metrics": self._calculate_executive_metrics(data),
                "risk_summary": self._summarize_risks(data),
                "compliance_summary": self._summarize_compliance(data)
            }
            
            self.logger.info("Executive summary built successfully")
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to build executive summary: {str(e)}")
            return self._get_fallback_summary()
    
    def _generate_overview(self, data: ReportData) -> str:
        """Generate high-level overview text."""
        try:
            overview_parts = []
            
            # Analyze data sources available
            sources = []
            if data.regulatory_data:
                sources.append("regulatory compliance")
            if data.bias_analysis_data:
                sources.append("AI model fairness")
            if data.risk_simulation_data:
                sources.append("risk assessment")
            
            if sources:
                overview_parts.append(f"This executive report provides a comprehensive analysis of {', '.join(sources)} "
                                    f"for your organization's AI and compliance systems.")
            
            # Overall health assessment
            health_score = self._calculate_overall_health(data)
            if health_score >= 0.8:
                health_status = "excellent condition with strong compliance posture"
            elif health_score >= 0.6:
                health_status = "good condition with some areas for improvement"
            elif health_score >= 0.4:
                health_status = "moderate condition requiring attention"
            else:
                health_status = "concerning condition requiring immediate action"
            
            overview_parts.append(f"Your systems are currently in {health_status}.")
            
            # Key findings
            critical_issues = self._identify_critical_issues(data)
            if critical_issues:
                overview_parts.append(f"Critical areas requiring executive attention include: {', '.join(critical_issues)}.")
            else:
                overview_parts.append("No critical issues requiring immediate executive intervention were identified.")
            
            return " ".join(overview_parts)
            
        except Exception as e:
            self.logger.error(f"Failed to generate overview: {str(e)}")
            return "Executive overview could not be generated due to data processing issues."
    
    def _extract_key_points(self, data: ReportData) -> List[str]:
        """Extract key executive points from all data sources."""
        try:
            key_points = []
            
            # Regulatory key points
            if data.regulatory_data:
                reg_data = data.regulatory_data
                compliance_score = reg_data.get("summary", {}).get("compliance_score", 0.0)
                total_regs = reg_data.get("summary", {}).get("total_regulations", 0)
                
                key_points.append(f"Regulatory Compliance: {compliance_score:.1%} compliance rate across {total_regs} regulations")
                
                # Deadlines
                deadlines = reg_data.get("deadlines", [])
                urgent_deadlines = [d for d in deadlines if d.get("priority") == "high"]
                if urgent_deadlines:
                    key_points.append(f"Urgent Action Required: {len(urgent_deadlines)} high-priority regulatory deadlines approaching")
            
            # Bias analysis key points
            if data.bias_analysis_data:
                bias_data = data.bias_analysis_data
                bias_score = bias_data.get("bias_score", {})
                overall_score = bias_score.get("overall_score", 0.0)
                risk_level = bias_score.get("risk_level", "unknown")
                
                key_points.append(f"AI Fairness: {overall_score:.1%} fairness score with {risk_level} risk level")
                
                flagged_attrs = bias_score.get("flagged_attributes", [])
                if flagged_attrs:
                    key_points.append(f"Bias Concerns: {len(flagged_attrs)} protected attributes showing potential bias")
            
            # Risk simulation key points
            if data.risk_simulation_data:
                risk_data = data.risk_simulation_data
                risk_metrics = risk_data.get("risk_metrics", {})
                risk_prob = risk_metrics.get("risk_probability", 0.0)
                
                key_points.append(f"Risk Assessment: {risk_prob:.1%} probability of compliance violations")
                
                financial_impact = risk_data.get("financial_impact", {})
                total_impact = financial_impact.get("total_impact", 0.0)
                if total_impact > 0:
                    key_points.append(f"Financial Exposure: ${total_impact:,.0f} potential financial impact")
            
            # Ensure we have at least some key points
            if not key_points:
                key_points = [
                    "Comprehensive analysis completed across all available data sources",
                    "Detailed findings and recommendations provided in subsequent sections"
                ]
            
            return key_points[:5]  # Limit to top 5 key points
            
        except Exception as e:
            self.logger.error(f"Failed to extract key points: {str(e)}")
            return ["Key points could not be extracted from available data"]
    
    def _assess_business_impact(self, data: ReportData) -> Dict[str, Any]:
        """Assess business impact across all dimensions."""
        try:
            impact = {
                "financial_risk": "low",
                "operational_risk": "low", 
                "reputational_risk": "low",
                "strategic_implications": [],
                "immediate_actions_required": False
            }
            
            # Financial impact assessment
            if data.risk_simulation_data:
                financial_data = data.risk_simulation_data.get("financial_impact", {})
                total_impact = financial_data.get("total_impact", 0.0)
                
                if total_impact > 1000000:  # $1M+
                    impact["financial_risk"] = "high"
                    impact["immediate_actions_required"] = True
                elif total_impact > 100000:  # $100K+
                    impact["financial_risk"] = "medium"
                
                impact["strategic_implications"].append(f"Potential financial exposure: ${total_impact:,.0f}")
            
            # Operational risk from bias analysis
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {})
                risk_level = bias_score.get("risk_level", "").lower()
                
                if risk_level in ["high", "critical"]:
                    impact["operational_risk"] = "high"
                    impact["reputational_risk"] = "high"
                    impact["immediate_actions_required"] = True
                    impact["strategic_implications"].append("AI model bias poses operational and reputational risks")
                elif risk_level == "medium":
                    impact["operational_risk"] = "medium"
            
            # Regulatory compliance impact
            if data.regulatory_data:
                compliance_score = data.regulatory_data.get("summary", {}).get("compliance_score", 1.0)
                
                if compliance_score < 0.7:
                    impact["reputational_risk"] = "high"
                    impact["immediate_actions_required"] = True
                    impact["strategic_implications"].append("Regulatory compliance gaps require immediate attention")
            
            return impact
            
        except Exception as e:
            self.logger.error(f"Failed to assess business impact: {str(e)}")
            return {"error": "Business impact assessment unavailable"}
    
    def _identify_strategic_priorities(self, data: ReportData) -> List[str]:
        """Identify strategic priorities for executive action."""
        try:
            priorities = []
            
            # Priority 1: Critical compliance issues
            if data.regulatory_data:
                compliance_score = data.regulatory_data.get("summary", {}).get("compliance_score", 1.0)
                if compliance_score < 0.8:
                    priorities.append("Strengthen regulatory compliance framework")
            
            # Priority 2: AI fairness and bias mitigation
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 1.0)
                if bias_score < 0.8:
                    priorities.append("Implement AI fairness and bias mitigation strategies")
            
            # Priority 3: Risk management enhancement
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                if risk_prob > 0.2:
                    priorities.append("Enhance risk management and monitoring capabilities")
            
            # Priority 4: Operational excellence
            priorities.append("Establish continuous monitoring and improvement processes")
            
            # Priority 5: Stakeholder communication
            priorities.append("Develop transparent reporting and communication frameworks")
            
            return priorities[:4]  # Top 4 strategic priorities
            
        except Exception as e:
            self.logger.error(f"Failed to identify strategic priorities: {str(e)}")
            return ["Strategic priorities could not be determined"]
    
    def _calculate_executive_metrics(self, data: ReportData) -> Dict[str, float]:
        """Calculate key executive-level metrics."""
        try:
            metrics = {}
            
            # Overall health score
            metrics["overall_health_score"] = self._calculate_overall_health(data)
            
            # Compliance effectiveness
            if data.regulatory_data:
                metrics["compliance_effectiveness"] = data.regulatory_data.get("summary", {}).get("compliance_score", 0.0)
            
            # AI fairness score
            if data.bias_analysis_data:
                metrics["ai_fairness_score"] = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 0.0)
            
            # Risk management effectiveness
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                metrics["risk_management_score"] = 1.0 - risk_prob  # Convert to positive score
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to calculate executive metrics: {str(e)}")
            return {"overall_health_score": 0.0}
    
    def _calculate_overall_health(self, data: ReportData) -> float:
        """Calculate overall organizational health score."""
        try:
            scores = []
            
            if data.regulatory_data:
                reg_score = data.regulatory_data.get("summary", {}).get("compliance_score", 0.0)
                scores.append(reg_score)
            
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 0.0)
                scores.append(bias_score)
            
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                risk_score = 1.0 - risk_prob
                scores.append(risk_score)
            
            return sum(scores) / len(scores) if scores else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate overall health: {str(e)}")
            return 0.0
    
    def _summarize_risks(self, data: ReportData) -> Dict[str, Any]:
        """Summarize key risks across all areas."""
        try:
            risks = {
                "high_priority_risks": [],
                "medium_priority_risks": [],
                "risk_trend": "stable"
            }
            
            # Regulatory risks
            if data.regulatory_data:
                reg_risk = data.regulatory_data.get("risk_assessment", {})
                risk_level = reg_risk.get("risk_level", "").lower()
                
                if risk_level == "high":
                    risks["high_priority_risks"].append("Regulatory compliance violations")
                elif risk_level == "medium":
                    risks["medium_priority_risks"].append("Regulatory compliance gaps")
            
            # AI bias risks
            if data.bias_analysis_data:
                bias_risk = data.bias_analysis_data.get("bias_score", {}).get("risk_level", "").lower()
                
                if bias_risk in ["high", "critical"]:
                    risks["high_priority_risks"].append("AI model bias and fairness issues")
                elif bias_risk == "medium":
                    risks["medium_priority_risks"].append("AI model fairness concerns")
            
            # Simulation risks
            if data.risk_simulation_data:
                sim_risk = data.risk_simulation_data.get("risk_metrics", {}).get("risk_level", "").lower()
                
                if sim_risk == "high":
                    risks["high_priority_risks"].append("Predicted compliance violations")
                elif sim_risk == "medium":
                    risks["medium_priority_risks"].append("Potential compliance issues")
            
            return risks
            
        except Exception as e:
            self.logger.error(f"Failed to summarize risks: {str(e)}")
            return {"high_priority_risks": [], "medium_priority_risks": []}
    
    def _summarize_compliance(self, data: ReportData) -> Dict[str, Any]:
        """Summarize compliance status across all areas."""
        try:
            compliance = {
                "overall_status": "unknown",
                "compliant_areas": 0,
                "non_compliant_areas": 0,
                "areas_needing_attention": []
            }
            
            if data.regulatory_data:
                reg_compliance = data.regulatory_data.get("compliance_status", {})
                compliance["compliant_areas"] += reg_compliance.get("compliant_count", 0)
                compliance["non_compliant_areas"] += reg_compliance.get("non_compliant_count", 0)
                
                if reg_compliance.get("overall_status") == "non_compliant":
                    compliance["areas_needing_attention"].append("Regulatory compliance")
            
            # Determine overall status
            total_areas = compliance["compliant_areas"] + compliance["non_compliant_areas"]
            if total_areas > 0:
                compliance_rate = compliance["compliant_areas"] / total_areas
                if compliance_rate >= 0.9:
                    compliance["overall_status"] = "excellent"
                elif compliance_rate >= 0.8:
                    compliance["overall_status"] = "good"
                elif compliance_rate >= 0.7:
                    compliance["overall_status"] = "fair"
                else:
                    compliance["overall_status"] = "needs_improvement"
            
            return compliance
            
        except Exception as e:
            self.logger.error(f"Failed to summarize compliance: {str(e)}")
            return {"overall_status": "unknown"}
    
    def _identify_critical_issues(self, data: ReportData) -> List[str]:
        """Identify critical issues requiring executive attention."""
        try:
            issues = []
            
            # Check regulatory compliance
            if data.regulatory_data:
                compliance_score = data.regulatory_data.get("summary", {}).get("compliance_score", 1.0)
                if compliance_score < 0.7:
                    issues.append("regulatory compliance gaps")
            
            # Check AI bias
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 1.0)
                if bias_score < 0.7:
                    issues.append("AI model bias concerns")
            
            # Check risk levels
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                if risk_prob > 0.3:
                    issues.append("high compliance violation risk")
            
            return issues
            
        except Exception as e:
            self.logger.error(f"Failed to identify critical issues: {str(e)}")
            return []
    
    def _get_fallback_summary(self) -> Dict[str, Any]:
        """Get fallback summary when data processing fails."""
        return {
            "overview": "Executive summary could not be generated due to data processing issues.",
            "key_points": ["Data processing error occurred", "Manual review recommended"],
            "business_impact": {"error": "Impact assessment unavailable"},
            "strategic_priorities": ["Review data sources", "Ensure system connectivity"],
            "executive_metrics": {"overall_health_score": 0.0},
            "risk_summary": {"high_priority_risks": ["Data processing failure"]},
            "compliance_summary": {"overall_status": "unknown"}
        }
    
    def __str__(self) -> str:
        """String representation."""
        return "ExecutiveSummaryBuilder()"
