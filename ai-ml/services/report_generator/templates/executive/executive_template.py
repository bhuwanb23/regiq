#!/usr/bin/env python3
"""
REGIQ AI/ML - Executive Template
Executive report template for C-suite stakeholders.

This template provides:
- High-level compliance overview
- Key risk indicators
- Strategic recommendations
- Executive summary
- Business impact assessment

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from ..base.base_template import BaseTemplate, ReportSection, ReportData
from ..utils.section_builder import SectionBuilder
from .summary_sections import ExecutiveSummaryBuilder
from .metrics_display import ExecutiveMetricsDisplay
from .recommendations import ExecutiveRecommendations

# Configure logging
logger = logging.getLogger(__name__)


class ExecutiveTemplate(BaseTemplate):
    """
    Executive Report Template for C-suite stakeholders.
    
    Generates high-level reports focusing on:
    - Strategic compliance overview
    - Key business risks
    - Executive recommendations
    - Financial impact assessment
    - Action items and priorities
    """
    
    def __init__(self, template_id: str = "executive_report", template_name: str = "Executive Report", version: str = "1.0.0"):
        """Initialize executive template."""
        super().__init__(template_id, template_name, version)
        
        # Initialize component builders
        self.section_builder = SectionBuilder()
        self.summary_builder = ExecutiveSummaryBuilder()
        self.metrics_display = ExecutiveMetricsDisplay()
        self.recommendations = ExecutiveRecommendations()
        
        self.logger = logging.getLogger(__name__)
    
    def get_description(self) -> str:
        """Get template description."""
        return ("Executive Report Template for C-suite stakeholders. "
                "Provides high-level compliance overview, strategic insights, "
                "and actionable recommendations for business leadership.")
    
    def get_supported_formats(self) -> List[str]:
        """Get supported output formats."""
        return ["html", "pdf", "json"]
    
    def validate_data(self, data: ReportData) -> Tuple[bool, List[str]]:
        """
        Validate input data for executive template.
        
        Args:
            data: Report data to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        try:
            # Basic data validation
            base_valid, base_errors = data.validate()
            if not base_valid:
                errors.extend(base_errors)
            
            # Executive-specific validation
            has_any_data = any([
                data.regulatory_data,
                data.bias_analysis_data, 
                data.risk_simulation_data
            ])
            
            if not has_any_data:
                errors.append("Executive report requires at least one data source")
            
            # Check for key executive metrics
            if data.regulatory_data:
                reg_data = data.regulatory_data
                if not reg_data.get("summary"):
                    errors.append("Regulatory data missing executive summary")
            
            if data.bias_analysis_data:
                bias_data = data.bias_analysis_data
                if not bias_data.get("bias_score"):
                    errors.append("Bias analysis data missing overall bias score")
            
            if data.risk_simulation_data:
                risk_data = data.risk_simulation_data
                if not risk_data.get("risk_metrics"):
                    errors.append("Risk simulation data missing key metrics")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            self.logger.error(f"Data validation error: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def generate_sections(self, data: ReportData) -> List[ReportSection]:
        """
        Generate executive report sections.
        
        Args:
            data: Report data
            
        Returns:
            List of report sections
        """
        try:
            sections = []
            
            # 1. Executive Summary (Order: 1)
            summary_section = self._generate_executive_summary(data)
            sections.append(summary_section)
            
            # 2. Key Metrics Dashboard (Order: 2)
            metrics_section = self._generate_key_metrics(data)
            sections.append(metrics_section)
            
            # 3. Risk Overview (Order: 3)
            risk_section = self._generate_risk_overview(data)
            sections.append(risk_section)
            
            # 4. Compliance Status (Order: 4)
            compliance_section = self._generate_compliance_status(data)
            sections.append(compliance_section)
            
            # 5. Strategic Recommendations (Order: 5)
            recommendations_section = self._generate_strategic_recommendations(data)
            sections.append(recommendations_section)
            
            # 6. Financial Impact (Order: 6)
            financial_section = self._generate_financial_impact(data)
            sections.append(financial_section)
            
            # 7. Action Items (Order: 7)
            action_section = self._generate_action_items(data)
            sections.append(action_section)
            
            self.logger.info(f"Generated {len(sections)} executive report sections")
            return sections
            
        except Exception as e:
            self.logger.error(f"Failed to generate executive sections: {str(e)}")
            raise
    
    def _generate_executive_summary(self, data: ReportData) -> ReportSection:
        """Generate executive summary section."""
        try:
            summary_data = self.summary_builder.build_executive_summary(data)
            
            return self.section_builder.build_summary_section(
                title="Executive Summary",
                summary_data=summary_data,
                section_id="executive_summary",
                order=1
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate executive summary: {str(e)}")
            # Return fallback section
            return ReportSection(
                section_id="executive_summary",
                title="Executive Summary",
                content="<p><em>Executive summary could not be generated.</em></p>",
                section_type="summary",
                order=1
            )
    
    def _generate_key_metrics(self, data: ReportData) -> ReportSection:
        """Generate key metrics dashboard section."""
        try:
            metrics_data = self.metrics_display.build_executive_metrics(data)
            
            return self.section_builder.build_metrics_section(
                title="Key Performance Indicators",
                metrics_data=metrics_data,
                section_id="key_metrics",
                order=2
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate key metrics: {str(e)}")
            return ReportSection(
                section_id="key_metrics",
                title="Key Performance Indicators", 
                content="<p><em>Metrics could not be generated.</em></p>",
                section_type="metrics",
                order=2
            )
    
    def _generate_risk_overview(self, data: ReportData) -> ReportSection:
        """Generate risk overview section."""
        try:
            risk_data = {}
            
            # Aggregate risk information from all sources
            if data.regulatory_data and "risk_assessment" in data.regulatory_data:
                reg_risk = data.regulatory_data["risk_assessment"]
                risk_data["regulatory_risk_level"] = reg_risk.get("risk_level", "unknown")
                risk_data["regulatory_risk_score"] = reg_risk.get("risk_score", 0.0)
            
            if data.bias_analysis_data and "bias_score" in data.bias_analysis_data:
                bias_info = data.bias_analysis_data["bias_score"]
                risk_data["bias_risk_level"] = bias_info.get("risk_level", "unknown")
                risk_data["overall_bias_score"] = bias_info.get("overall_score", 0.0)
            
            if data.risk_simulation_data and "risk_metrics" in data.risk_simulation_data:
                sim_risk = data.risk_simulation_data["risk_metrics"]
                risk_data["simulation_risk_level"] = sim_risk.get("risk_level", "unknown")
                risk_data["risk_probability"] = sim_risk.get("risk_probability", 0.0)
            
            # Overall risk assessment
            risk_levels = [v for k, v in risk_data.items() if k.endswith("_risk_level")]
            if risk_levels:
                # Simple risk level aggregation (could be more sophisticated)
                high_count = risk_levels.count("high")
                medium_count = risk_levels.count("medium") 
                if high_count > 0:
                    risk_data["overall_risk_level"] = "high"
                elif medium_count > 0:
                    risk_data["overall_risk_level"] = "medium"
                else:
                    risk_data["overall_risk_level"] = "low"
            
            return self.section_builder.build_status_section(
                title="Risk Overview",
                status_data=risk_data,
                section_id="risk_overview",
                order=3
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate risk overview: {str(e)}")
            return ReportSection(
                section_id="risk_overview",
                title="Risk Overview",
                content="<p><em>Risk overview could not be generated.</em></p>",
                section_type="status",
                order=3
            )
    
    def _generate_compliance_status(self, data: ReportData) -> ReportSection:
        """Generate compliance status section."""
        try:
            compliance_data = {}
            
            if data.regulatory_data and "compliance_status" in data.regulatory_data:
                comp_status = data.regulatory_data["compliance_status"]
                compliance_data.update(comp_status)
            
            # Add bias compliance indicators
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {})
                overall_score = bias_score.get("overall_score", 0.0)
                if overall_score >= 0.8:
                    compliance_data["ai_fairness_status"] = "compliant"
                elif overall_score >= 0.6:
                    compliance_data["ai_fairness_status"] = "needs_attention"
                else:
                    compliance_data["ai_fairness_status"] = "non_compliant"
            
            return self.section_builder.build_status_section(
                title="Compliance Status",
                status_data=compliance_data,
                section_id="compliance_status", 
                order=4
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate compliance status: {str(e)}")
            return ReportSection(
                section_id="compliance_status",
                title="Compliance Status",
                content="<p><em>Compliance status could not be generated.</em></p>",
                section_type="status",
                order=4
            )
    
    def _generate_strategic_recommendations(self, data: ReportData) -> ReportSection:
        """Generate strategic recommendations section."""
        try:
            recommendations = self.recommendations.build_executive_recommendations(data)
            
            return self.section_builder.build_recommendations_section(
                title="Strategic Recommendations",
                recommendations=recommendations,
                section_id="strategic_recommendations",
                order=5
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate strategic recommendations: {str(e)}")
            return ReportSection(
                section_id="strategic_recommendations",
                title="Strategic Recommendations",
                content="<p><em>Recommendations could not be generated.</em></p>",
                section_type="recommendations",
                order=5
            )
    
    def _generate_financial_impact(self, data: ReportData) -> ReportSection:
        """Generate financial impact section."""
        try:
            financial_data = {}
            
            if data.risk_simulation_data and "financial_impact" in data.risk_simulation_data:
                fin_impact = data.risk_simulation_data["financial_impact"]
                financial_data.update(fin_impact)
            
            # Add estimated costs from other sources
            if data.regulatory_data:
                # Estimate potential regulatory fines
                reg_risk = data.regulatory_data.get("risk_assessment", {})
                risk_score = reg_risk.get("risk_score", 0.0)
                # Simple estimation (in production, this would be more sophisticated)
                estimated_fine = risk_score * 100000  # Base fine estimation
                financial_data["estimated_regulatory_fines"] = estimated_fine
            
            if not financial_data:
                financial_data = {"status": "No financial impact data available"}
            
            return self.section_builder.build_summary_section(
                title="Financial Impact Assessment",
                summary_data=financial_data,
                section_id="financial_impact",
                order=6
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate financial impact: {str(e)}")
            return ReportSection(
                section_id="financial_impact",
                title="Financial Impact Assessment",
                content="<p><em>Financial impact could not be assessed.</em></p>",
                section_type="summary",
                order=6
            )
    
    def _generate_action_items(self, data: ReportData) -> ReportSection:
        """Generate action items section."""
        try:
            action_items = []
            
            # Collect action items from all data sources
            if data.regulatory_data and "recommendations" in data.regulatory_data:
                reg_recs = data.regulatory_data["recommendations"]
                action_items.extend([f"Regulatory: {rec}" for rec in reg_recs[:3]])  # Top 3
            
            if data.bias_analysis_data and "recommendations" in data.bias_analysis_data:
                bias_recs = data.bias_analysis_data["recommendations"] 
                action_items.extend([f"AI Fairness: {rec}" for rec in bias_recs[:3]])  # Top 3
            
            if data.risk_simulation_data and "mitigation_strategies" in data.risk_simulation_data:
                risk_strategies = data.risk_simulation_data["mitigation_strategies"]
                for strategy in risk_strategies[:2]:  # Top 2
                    if isinstance(strategy, dict):
                        action_items.append(f"Risk Mitigation: {strategy.get('strategy', 'Unknown strategy')}")
                    else:
                        action_items.append(f"Risk Mitigation: {strategy}")
            
            if not action_items:
                action_items = ["Review compliance status", "Assess AI model fairness", "Monitor regulatory changes"]
            
            return self.section_builder.build_recommendations_section(
                title="Immediate Action Items",
                recommendations=action_items,
                section_id="action_items",
                order=7
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate action items: {str(e)}")
            return ReportSection(
                section_id="action_items",
                title="Immediate Action Items",
                content="<p><em>Action items could not be generated.</em></p>",
                section_type="recommendations",
                order=7
            )
    
    def get_executive_insights(self, data: ReportData) -> Dict[str, Any]:
        """
        Get executive-level insights from the data.
        
        Args:
            data: Report data
            
        Returns:
            Dictionary of executive insights
        """
        try:
            insights = {
                "overall_health_score": 0.0,
                "critical_issues": [],
                "opportunities": [],
                "risk_factors": [],
                "compliance_gaps": []
            }
            
            # Calculate overall health score
            scores = []
            
            if data.regulatory_data:
                reg_score = data.regulatory_data.get("compliance_score", 0.0)
                scores.append(reg_score)
                
                if reg_score < 0.7:
                    insights["critical_issues"].append("Regulatory compliance below acceptable threshold")
            
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 0.0)
                scores.append(bias_score)
                
                if bias_score < 0.7:
                    insights["critical_issues"].append("AI model fairness concerns identified")
            
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                risk_score = 1.0 - risk_prob  # Convert probability to score
                scores.append(risk_score)
                
                if risk_prob > 0.3:
                    insights["risk_factors"].append("High probability of compliance violations")
            
            # Calculate overall health
            if scores:
                insights["overall_health_score"] = sum(scores) / len(scores)
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Failed to generate executive insights: {str(e)}")
            return {"error": "Could not generate insights"}
    
    def __str__(self) -> str:
        """String representation."""
        return f"ExecutiveTemplate(id={self.template_id})"
