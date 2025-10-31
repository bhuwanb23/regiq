#!/usr/bin/env python3
"""
REGIQ AI/ML - Prompt Engine
Intelligent prompt generation for narrative creation.

This module provides:
- Context-aware prompt generation
- Audience-specific prompt templates
- Dynamic prompt construction
- Prompt optimization and validation

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
import re

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class PromptTemplate:
    """Prompt template structure."""
    template_id: str
    audience_type: str
    section_type: str
    template: str
    variables: List[str]
    instructions: str
    examples: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "template_id": self.template_id,
            "audience_type": self.audience_type,
            "section_type": self.section_type,
            "template": self.template,
            "variables": self.variables,
            "instructions": self.instructions,
            "examples": self.examples
        }


class PromptEngine:
    """
    Intelligent prompt engine for narrative generation.
    
    Creates context-aware, audience-specific prompts for different
    report sections and stakeholder types.
    """
    
    def __init__(self):
        """Initialize prompt engine."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize prompt templates
        self.templates: Dict[str, PromptTemplate] = {}
        self._initialize_templates()
        
        # Prompt optimization settings
        self.max_prompt_length = 4000
        self.context_window = 2000
    
    def _initialize_templates(self) -> None:
        """Initialize prompt templates for different audiences and sections."""
        
        # Executive Templates
        self._add_executive_templates()
        
        # Technical Templates
        self._add_technical_templates()
        
        # Regulatory Templates
        self._add_regulatory_templates()
        
        self.logger.info(f"Initialized {len(self.templates)} prompt templates")
    
    def _add_executive_templates(self) -> None:
        """Add executive audience prompt templates."""
        
        # Executive Summary Template
        self.templates["executive_summary"] = PromptTemplate(
            template_id="executive_summary",
            audience_type="executive",
            section_type="summary",
            template="""
You are an executive consultant writing a strategic summary for C-suite leaders. 

CONTEXT:
- Organization: {organization_name}
- Analysis Period: {analysis_period}
- Key Metrics: {key_metrics}
- Overall Health Score: {health_score}
- Critical Issues: {critical_issues}

TASK:
Write a compelling executive summary that:
1. Opens with the current strategic position
2. Highlights 3-4 most critical insights
3. Emphasizes business impact and opportunities
4. Uses confident, strategic language
5. Focuses on actionable outcomes

TONE: Strategic, confident, business-focused
LENGTH: 150-200 words
AVOID: Technical jargon, implementation details, uncertainty

Generate an executive summary that tells the strategic story behind the data:
            """.strip(),
            variables=["organization_name", "analysis_period", "key_metrics", "health_score", "critical_issues"],
            instructions="Focus on strategic insights and business impact",
            examples=[
                "Your organization demonstrates strong compliance fundamentals with a 78% regulatory adherence rate, positioning you well for continued growth...",
                "Strategic analysis reveals significant opportunities to strengthen your competitive advantage through targeted AI governance improvements..."
            ]
        )
        
        # Executive Metrics Template
        self.templates["executive_metrics"] = PromptTemplate(
            template_id="executive_metrics",
            audience_type="executive",
            section_type="metrics",
            template="""
You are translating technical metrics into executive insights.

METRICS DATA:
{metrics_data}

CONTEXT:
- Industry Benchmarks: {benchmarks}
- Risk Levels: {risk_levels}
- Trends: {trends}

TASK:
Create an executive interpretation of these metrics that:
1. Explains what the numbers mean for the business
2. Identifies performance against industry standards
3. Highlights areas of strength and concern
4. Provides strategic context for decision-making

TONE: Analytical, strategic, results-oriented
LENGTH: 100-150 words
FOCUS: Business implications, not technical details

Interpret these metrics for executive decision-making:
            """.strip(),
            variables=["metrics_data", "benchmarks", "risk_levels", "trends"],
            instructions="Translate technical metrics to business insights",
            examples=[
                "Your 74% overall health score places you in the top quartile of industry performers, indicating strong operational foundations...",
                "The composite risk score of 0.40 suggests moderate exposure requiring strategic attention in the next quarter..."
            ]
        )
        
        # Executive Recommendations Template
        self.templates["executive_recommendations"] = PromptTemplate(
            template_id="executive_recommendations",
            audience_type="executive",
            section_type="recommendations",
            template="""
You are a strategic advisor providing executive recommendations.

ANALYSIS RESULTS:
{analysis_results}

CONTEXT:
- Current Performance: {current_performance}
- Risk Factors: {risk_factors}
- Resource Constraints: {resource_constraints}
- Timeline: {timeline}

TASK:
Provide strategic recommendations that:
1. Address the highest-impact opportunities
2. Consider resource allocation and ROI
3. Include implementation priorities
4. Focus on competitive advantage
5. Align with business objectives

TONE: Authoritative, strategic, action-oriented
FORMAT: Prioritized list with business rationale
LENGTH: 200-250 words

Generate strategic recommendations for executive action:
            """.strip(),
            variables=["analysis_results", "current_performance", "risk_factors", "resource_constraints", "timeline"],
            instructions="Focus on strategic priorities and business impact",
            examples=[
                "Immediate Priority: Establish AI governance framework to capture $2M+ in compliance cost savings...",
                "Strategic Investment: Enhanced monitoring systems will reduce risk exposure by 40% within 6 months..."
            ]
        )
    
    def _add_technical_templates(self) -> None:
        """Add technical audience prompt templates."""
        
        # Technical Overview Template
        self.templates["technical_overview"] = PromptTemplate(
            template_id="technical_overview",
            audience_type="technical",
            section_type="overview",
            template="""
You are a senior data scientist explaining technical analysis to peers.

TECHNICAL DATA:
- Model Performance: {model_performance}
- Methodology: {methodology}
- Data Quality: {data_quality}
- Statistical Significance: {statistical_significance}

ANALYSIS SCOPE:
{analysis_scope}

TASK:
Create a technical overview that:
1. Summarizes the analytical approach
2. Highlights key technical findings
3. Discusses methodology and validation
4. Identifies technical limitations
5. Provides implementation context

TONE: Analytical, precise, technically accurate
AUDIENCE: Data scientists, ML engineers
LENGTH: 200-300 words

Generate a comprehensive technical overview:
            """.strip(),
            variables=["model_performance", "methodology", "data_quality", "statistical_significance", "analysis_scope"],
            instructions="Focus on technical accuracy and methodological rigor",
            examples=[
                "The XGBoost classifier achieves 84.7% accuracy with cross-validated performance metrics indicating robust generalization...",
                "Bias analysis employs demographic parity and equalized odds metrics, revealing significant disparities in protected attributes..."
            ]
        )
        
        # Technical Methodology Template
        self.templates["technical_methodology"] = PromptTemplate(
            template_id="technical_methodology",
            audience_type="technical",
            section_type="methodology",
            template="""
You are documenting technical methodology for peer review.

METHODOLOGY DETAILS:
{methodology_details}

IMPLEMENTATION:
- Algorithms Used: {algorithms}
- Validation Approach: {validation}
- Statistical Tests: {statistical_tests}
- Performance Metrics: {performance_metrics}

TASK:
Document the methodology with:
1. Clear algorithmic descriptions
2. Validation and testing procedures
3. Statistical rigor and assumptions
4. Reproducibility considerations
5. Limitations and constraints

TONE: Precise, methodical, academically rigorous
AUDIENCE: Technical reviewers, researchers
LENGTH: 250-350 words

Document the technical methodology:
            """.strip(),
            variables=["methodology_details", "algorithms", "validation", "statistical_tests", "performance_metrics"],
            instructions="Ensure technical precision and reproducibility",
            examples=[
                "The bias detection framework implements Fairlearn's demographic parity metrics with bootstrap confidence intervals...",
                "Monte Carlo simulation employs 10,000 iterations with convergence validation using Gelman-Rubin diagnostics..."
            ]
        )
    
    def _add_regulatory_templates(self) -> None:
        """Add regulatory audience prompt templates."""
        
        # Regulatory Compliance Template
        self.templates["regulatory_compliance"] = PromptTemplate(
            template_id="regulatory_compliance",
            audience_type="regulatory",
            section_type="compliance",
            template="""
You are a compliance officer documenting regulatory adherence.

COMPLIANCE STATUS:
{compliance_status}

REGULATORY FRAMEWORK:
- Applicable Regulations: {regulations}
- Compliance Gaps: {gaps}
- Evidence Documentation: {evidence}
- Audit Requirements: {audit_requirements}

TASK:
Create compliance documentation that:
1. Clearly states compliance status
2. Documents evidence and verification
3. Identifies gaps and remediation needs
4. Provides audit trail references
5. Ensures regulatory language precision

TONE: Formal, precise, compliance-focused
AUDIENCE: Auditors, regulatory bodies, compliance teams
LENGTH: 200-250 words

Generate regulatory compliance documentation:
            """.strip(),
            variables=["compliance_status", "regulations", "gaps", "evidence", "audit_requirements"],
            instructions="Use precise regulatory language and documentation standards",
            examples=[
                "Compliance assessment demonstrates adherence to 19 of 25 applicable regulations with documented evidence...",
                "EU AI Act implementation requires immediate attention to avoid potential violations by August 2025 deadline..."
            ]
        )
        
        # Regulatory Evidence Template
        self.templates["regulatory_evidence"] = PromptTemplate(
            template_id="regulatory_evidence",
            audience_type="regulatory",
            section_type="evidence",
            template="""
You are documenting evidence for regulatory compliance verification.

EVIDENCE INVENTORY:
{evidence_inventory}

DOCUMENTATION:
- Audit Trails: {audit_trails}
- Verification Methods: {verification_methods}
- Supporting Documents: {supporting_documents}
- Compliance Records: {compliance_records}

TASK:
Document evidence that:
1. Provides clear audit trail
2. References supporting documentation
3. Demonstrates verification methods
4. Ensures traceability and accountability
5. Meets regulatory documentation standards

TONE: Formal, detailed, audit-ready
AUDIENCE: External auditors, regulatory inspectors
LENGTH: 150-200 words

Generate comprehensive evidence documentation:
            """.strip(),
            variables=["evidence_inventory", "audit_trails", "verification_methods", "supporting_documents", "compliance_records"],
            instructions="Ensure audit-ready documentation with full traceability",
            examples=[
                "Evidence documentation includes comprehensive model validation records with timestamped audit trails...",
                "Verification procedures demonstrate systematic compliance monitoring with documented review cycles..."
            ]
        )
    
    def create_prompt(
        self,
        section_data: Dict[str, Any],
        context: Dict[str, Any],
        audience_type: str,
        section_type: str
    ) -> str:
        """
        Create context-aware prompt for narrative generation.
        
        Args:
            section_data: Data for the specific section
            context: Additional context information
            audience_type: Target audience (executive, technical, regulatory)
            section_type: Type of section (summary, metrics, etc.)
            
        Returns:
            Generated prompt string
        """
        try:
            # Find appropriate template
            template_key = f"{audience_type}_{section_type}"
            
            if template_key not in self.templates:
                # Fallback to generic template
                template_key = self._find_fallback_template(audience_type, section_type)
            
            if template_key not in self.templates:
                return self._create_generic_prompt(section_data, context, audience_type, section_type)
            
            template = self.templates[template_key]
            
            # Prepare variables for substitution
            variables = self._extract_variables(section_data, context, template.variables)
            
            # Substitute variables in template
            prompt = self._substitute_variables(template.template, variables)
            
            # Optimize prompt length
            prompt = self._optimize_prompt_length(prompt)
            
            self.logger.debug(f"Created prompt for {audience_type}_{section_type} ({len(prompt)} chars)")
            
            return prompt
            
        except Exception as e:
            self.logger.error(f"Failed to create prompt: {str(e)}")
            return self._create_generic_prompt(section_data, context, audience_type, section_type)
    
    def _find_fallback_template(self, audience_type: str, section_type: str) -> Optional[str]:
        """Find fallback template for audience/section combination."""
        # Try audience-specific templates
        for template_key, template in self.templates.items():
            if template.audience_type == audience_type:
                return template_key
        
        # Try section-specific templates
        for template_key, template in self.templates.items():
            if template.section_type == section_type:
                return template_key
        
        return None
    
    def _extract_variables(
        self, 
        section_data: Dict[str, Any], 
        context: Dict[str, Any], 
        required_variables: List[str]
    ) -> Dict[str, str]:
        """Extract and format variables for prompt substitution."""
        variables = {}
        
        for var in required_variables:
            if var in section_data:
                variables[var] = self._format_variable(section_data[var])
            elif var in context:
                variables[var] = self._format_variable(context[var])
            else:
                # Provide sensible defaults
                variables[var] = self._get_default_variable(var, section_data, context)
        
        return variables
    
    def _format_variable(self, value: Any) -> str:
        """Format variable value for prompt inclusion."""
        if isinstance(value, dict):
            # Format dictionary as key-value pairs
            items = [f"{k}: {v}" for k, v in value.items()]
            return ", ".join(items[:5])  # Limit to first 5 items
        elif isinstance(value, list):
            # Format list as comma-separated items
            return ", ".join(str(item) for item in value[:5])  # Limit to first 5 items
        elif isinstance(value, (int, float)):
            # Format numbers with appropriate precision
            if isinstance(value, float):
                return f"{value:.3f}"
            return str(value)
        else:
            return str(value)
    
    def _get_default_variable(self, var_name: str, section_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Get default value for missing variable."""
        defaults = {
            "organization_name": "Your organization",
            "analysis_period": "Current analysis period",
            "key_metrics": "Key performance indicators",
            "health_score": "Overall system health",
            "critical_issues": "Areas requiring attention",
            "benchmarks": "Industry standards",
            "risk_levels": "Current risk assessment",
            "trends": "Performance trends",
            "methodology": "Analysis methodology",
            "algorithms": "Applied algorithms",
            "compliance_status": "Compliance assessment results",
            "regulations": "Applicable regulatory framework"
        }
        
        return defaults.get(var_name, f"[{var_name}]")
    
    def _substitute_variables(self, template: str, variables: Dict[str, str]) -> str:
        """Substitute variables in template."""
        try:
            return template.format(**variables)
        except KeyError as e:
            self.logger.warning(f"Missing variable in template: {str(e)}")
            # Replace missing variables with placeholder
            for var_name in re.findall(r'\{(\w+)\}', template):
                if var_name not in variables:
                    variables[var_name] = f"[{var_name}]"
            return template.format(**variables)
    
    def _optimize_prompt_length(self, prompt: str) -> str:
        """Optimize prompt length for LLM processing."""
        if len(prompt) <= self.max_prompt_length:
            return prompt
        
        # Truncate while preserving structure
        lines = prompt.split('\n')
        optimized_lines = []
        current_length = 0
        
        for line in lines:
            if current_length + len(line) + 1 <= self.max_prompt_length:
                optimized_lines.append(line)
                current_length += len(line) + 1
            else:
                # Add truncation indicator
                optimized_lines.append("... [content truncated for length]")
                break
        
        return '\n'.join(optimized_lines)
    
    def _create_generic_prompt(
        self, 
        section_data: Dict[str, Any], 
        context: Dict[str, Any], 
        audience_type: str, 
        section_type: str
    ) -> str:
        """Create generic prompt when no template is available."""
        
        audience_instructions = {
            "executive": "Write for C-suite executives focusing on strategic insights and business impact.",
            "technical": "Write for data scientists and engineers with technical depth and precision.",
            "regulatory": "Write for compliance officers using formal regulatory language."
        }
        
        section_instructions = {
            "summary": "Create a comprehensive summary of the key findings and insights.",
            "metrics": "Explain the significance and implications of the performance metrics.",
            "recommendations": "Provide actionable recommendations based on the analysis.",
            "overview": "Give an overview of the analysis scope and approach.",
            "methodology": "Describe the technical methodology and implementation details.",
            "compliance": "Document compliance status and regulatory adherence."
        }
        
        audience_instruction = audience_instructions.get(audience_type, "Write clearly and professionally.")
        section_instruction = section_instructions.get(section_type, "Provide relevant insights based on the data.")
        
        return f"""
You are writing a {section_type} section for a {audience_type} audience.

INSTRUCTIONS:
{audience_instruction}
{section_instruction}

DATA:
{self._format_variable(section_data)}

CONTEXT:
{self._format_variable(context)}

Generate a well-structured narrative that provides valuable insights based on this information.
        """.strip()
    
    def validate_prompt(self, prompt: str) -> Tuple[bool, List[str]]:
        """Validate prompt quality and structure."""
        errors = []
        
        # Length validation
        if len(prompt) < 50:
            errors.append("Prompt too short (minimum 50 characters)")
        elif len(prompt) > self.max_prompt_length:
            errors.append(f"Prompt too long (maximum {self.max_prompt_length} characters)")
        
        # Structure validation
        if "TASK:" not in prompt and "Generate" not in prompt:
            errors.append("Prompt missing clear task instruction")
        
        # Variable substitution validation
        unresolved_vars = re.findall(r'\{(\w+)\}', prompt)
        if unresolved_vars:
            errors.append(f"Unresolved variables: {', '.join(unresolved_vars)}")
        
        return len(errors) == 0, errors
    
    def get_template_info(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific template."""
        if template_id in self.templates:
            return self.templates[template_id].to_dict()
        return None
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates."""
        return [template.to_dict() for template in self.templates.values()]
    
    def get_engine_stats(self) -> Dict[str, Any]:
        """Get prompt engine statistics."""
        audience_counts = {}
        section_counts = {}
        
        for template in self.templates.values():
            audience_counts[template.audience_type] = audience_counts.get(template.audience_type, 0) + 1
            section_counts[template.section_type] = section_counts.get(template.section_type, 0) + 1
        
        return {
            "total_templates": len(self.templates),
            "audience_types": list(audience_counts.keys()),
            "section_types": list(section_counts.keys()),
            "audience_distribution": audience_counts,
            "section_distribution": section_counts
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"PromptEngine({len(self.templates)} templates)"
