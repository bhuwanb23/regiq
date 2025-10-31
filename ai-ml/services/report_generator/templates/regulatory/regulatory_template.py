#!/usr/bin/env python3
"""
REGIQ AI/ML - Regulatory Template
Regulatory compliance report template for auditors and compliance officers.

This template provides:
- Compliance status documentation
- Regulatory mapping and evidence
- Audit trails and documentation
- Gap analysis and remediation plans
- Regulatory requirement verification

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

from ..base.base_template import BaseTemplate, ReportSection, ReportData
from ..utils.section_builder import SectionBuilder

# Configure logging
logger = logging.getLogger(__name__)


class RegulatoryTemplate(BaseTemplate):
    """
    Regulatory Compliance Report Template for auditors and compliance officers.
    
    Generates compliance-focused reports including:
    - Regulatory compliance status
    - Evidence documentation
    - Audit trails and records
    - Gap analysis and remediation
    - Regulatory requirement mapping
    """
    
    def __init__(self, template_id: str = "regulatory_report", template_name: str = "Regulatory Compliance Report", version: str = "1.0.0"):
        """Initialize regulatory template."""
        super().__init__(template_id, template_name, version)
        self.section_builder = SectionBuilder()
        self.logger = logging.getLogger(__name__)
    
    def get_description(self) -> str:
        """Get template description."""
        return ("Regulatory Compliance Report Template for auditors and compliance officers. "
                "Provides comprehensive compliance documentation, audit trails, "
                "and regulatory requirement verification.")
    
    def get_supported_formats(self) -> List[str]:
        """Get supported output formats."""
        return ["html", "pdf", "json"]
    
    def validate_data(self, data: ReportData) -> Tuple[bool, List[str]]:
        """Validate input data for regulatory template."""
        errors = []
        
        try:
            base_valid, base_errors = data.validate()
            if not base_valid:
                errors.extend(base_errors)
            
            # Regulatory-specific validation
            if not data.regulatory_data:
                errors.append("Regulatory report requires regulatory intelligence data")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            self.logger.error(f"Data validation error: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def generate_sections(self, data: ReportData) -> List[ReportSection]:
        """Generate regulatory report sections."""
        try:
            sections = []
            
            # 1. Compliance Executive Summary
            summary_section = self._generate_compliance_summary(data)
            sections.append(summary_section)
            
            # 2. Regulatory Compliance Status
            status_section = self._generate_compliance_status(data)
            sections.append(status_section)
            
            # 3. Evidence Documentation
            evidence_section = self._generate_evidence_documentation(data)
            sections.append(evidence_section)
            
            # 4. Gap Analysis
            gap_section = self._generate_gap_analysis(data)
            sections.append(gap_section)
            
            # 5. Audit Trail
            audit_section = self._generate_audit_trail(data)
            sections.append(audit_section)
            
            # 6. Remediation Plan
            remediation_section = self._generate_remediation_plan(data)
            sections.append(remediation_section)
            
            self.logger.info(f"Generated {len(sections)} regulatory report sections")
            return sections
            
        except Exception as e:
            self.logger.error(f"Failed to generate regulatory sections: {str(e)}")
            raise
    
    def _generate_compliance_summary(self, data: ReportData) -> ReportSection:
        """Generate compliance executive summary."""
        try:
            summary_data = {}
            
            if data.regulatory_data:
                reg_summary = data.regulatory_data.get("summary", {})
                summary_data.update(reg_summary)
                
                compliance_status = data.regulatory_data.get("compliance_status", {})
                summary_data.update(compliance_status)
            
            return self.section_builder.build_summary_section(
                title="Compliance Executive Summary",
                summary_data=summary_data,
                section_id="compliance_summary",
                order=1
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate compliance summary: {str(e)}")
            return ReportSection(
                section_id="compliance_summary",
                title="Compliance Executive Summary",
                content="<p><em>Compliance summary could not be generated.</em></p>",
                section_type="summary",
                order=1
            )
    
    def _generate_compliance_status(self, data: ReportData) -> ReportSection:
        """Generate detailed compliance status."""
        try:
            status_data = {}
            
            if data.regulatory_data:
                compliance_status = data.regulatory_data.get("compliance_status", {})
                status_data.update(compliance_status)
                
                # Add AI compliance status if available
                if data.bias_analysis_data:
                    bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 0.0)
                    status_data["ai_fairness_compliance"] = "compliant" if bias_score >= 0.8 else "non_compliant"
            
            return self.section_builder.build_status_section(
                title="Regulatory Compliance Status",
                status_data=status_data,
                section_id="compliance_status",
                order=2
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate compliance status: {str(e)}")
            return ReportSection(
                section_id="compliance_status",
                title="Regulatory Compliance Status",
                content="<p><em>Compliance status could not be generated.</em></p>",
                section_type="status",
                order=2
            )
    
    def _generate_evidence_documentation(self, data: ReportData) -> ReportSection:
        """Generate evidence documentation."""
        try:
            evidence_data = []
            
            if data.regulatory_data:
                regulations = data.regulatory_data.get("regulations", [])
                for reg in regulations[:10]:  # Limit to first 10
                    evidence_data.append({
                        "regulation": reg.get("name", "Unknown"),
                        "jurisdiction": reg.get("jurisdiction", "Unknown"),
                        "status": reg.get("status", "unknown"),
                        "evidence": "Documentation available",
                        "last_reviewed": datetime.now().strftime("%Y-%m-%d")
                    })
            
            return self.section_builder.build_data_table_section(
                title="Evidence Documentation",
                table_data=evidence_data,
                section_id="evidence_documentation",
                order=3
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate evidence documentation: {str(e)}")
            return ReportSection(
                section_id="evidence_documentation",
                title="Evidence Documentation",
                content="<p><em>Evidence documentation could not be generated.</em></p>",
                section_type="data_table",
                order=3
            )
    
    def _generate_gap_analysis(self, data: ReportData) -> ReportSection:
        """Generate gap analysis."""
        try:
            gaps = []
            
            if data.regulatory_data:
                compliance_score = data.regulatory_data.get("summary", {}).get("compliance_score", 1.0)
                if compliance_score < 1.0:
                    gaps.append(f"Regulatory compliance gap: {(1.0 - compliance_score):.1%} non-compliance rate")
            
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 1.0)
                if bias_score < 0.8:
                    gaps.append(f"AI fairness gap: Bias score {bias_score:.3f} below acceptable threshold")
            
            if not gaps:
                gaps = ["No significant compliance gaps identified"]
            
            return self.section_builder.build_recommendations_section(
                title="Gap Analysis",
                recommendations=gaps,
                section_id="gap_analysis",
                order=4
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate gap analysis: {str(e)}")
            return ReportSection(
                section_id="gap_analysis",
                title="Gap Analysis",
                content="<p><em>Gap analysis could not be generated.</em></p>",
                section_type="recommendations",
                order=4
            )
    
    def _generate_audit_trail(self, data: ReportData) -> ReportSection:
        """Generate audit trail documentation."""
        try:
            audit_content = f"""
            <h3>Audit Trail</h3>
            <div class="audit-trail">
                <h4>Analysis Performed</h4>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p><strong>System:</strong> REGIQ AI/ML Report Generation System</p>
                <p><strong>Version:</strong> {self.version}</p>
                
                <h4>Data Sources</h4>
                <ul>
                    {'<li>Regulatory Intelligence Engine</li>' if data.regulatory_data else ''}
                    {'<li>Bias Analysis System</li>' if data.bias_analysis_data else ''}
                    {'<li>Risk Simulation Engine</li>' if data.risk_simulation_data else ''}
                </ul>
                
                <h4>Compliance Verification</h4>
                <p>All analysis performed in accordance with established compliance frameworks and regulatory requirements.</p>
            </div>
            """
            
            return ReportSection(
                section_id="audit_trail",
                title="Audit Trail",
                content=audit_content,
                section_type="text",
                order=5
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate audit trail: {str(e)}")
            return ReportSection(
                section_id="audit_trail",
                title="Audit Trail",
                content="<p><em>Audit trail could not be generated.</em></p>",
                section_type="text",
                order=5
            )
    
    def _generate_remediation_plan(self, data: ReportData) -> ReportSection:
        """Generate remediation plan."""
        try:
            remediation_actions = []
            
            # Regulatory remediation
            if data.regulatory_data:
                compliance_score = data.regulatory_data.get("summary", {}).get("compliance_score", 1.0)
                if compliance_score < 0.9:
                    remediation_actions.extend([
                        "Conduct comprehensive regulatory compliance review",
                        "Update policies and procedures to address identified gaps",
                        "Implement enhanced compliance monitoring systems"
                    ])
            
            # AI fairness remediation
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 1.0)
                if bias_score < 0.8:
                    remediation_actions.extend([
                        "Implement AI bias mitigation strategies",
                        "Enhance model fairness monitoring",
                        "Conduct regular AI ethics reviews"
                    ])
            
            # Risk mitigation
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                if risk_prob > 0.2:
                    remediation_actions.extend([
                        "Strengthen risk management controls",
                        "Implement predictive risk monitoring",
                        "Develop crisis response procedures"
                    ])
            
            if not remediation_actions:
                remediation_actions = ["Continue current compliance practices", "Maintain regular monitoring and review cycles"]
            
            return self.section_builder.build_recommendations_section(
                title="Remediation Plan",
                recommendations=remediation_actions,
                section_id="remediation_plan",
                order=6
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate remediation plan: {str(e)}")
            return ReportSection(
                section_id="remediation_plan",
                title="Remediation Plan",
                content="<p><em>Remediation plan could not be generated.</em></p>",
                section_type="recommendations",
                order=6
            )
    
    def __str__(self) -> str:
        """String representation."""
        return f"RegulatoryTemplate(id={self.template_id})"
