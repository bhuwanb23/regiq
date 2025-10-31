#!/usr/bin/env python3
"""
REGIQ AI/ML - Technical Template
Technical report template for data scientists and engineers.

This template provides:
- Detailed methodology documentation
- Statistical analysis results
- Model performance metrics
- Technical implementation details
- Code snippets and algorithms

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
from .methodology_sections import TechnicalMethodologyBuilder
from .statistical_analysis import TechnicalStatisticalAnalysis
from .appendices import TechnicalAppendices

# Configure logging
logger = logging.getLogger(__name__)


class TechnicalTemplate(BaseTemplate):
    """
    Technical Report Template for data scientists and engineers.
    
    Generates detailed technical reports focusing on:
    - Methodology and implementation details
    - Statistical analysis and validation
    - Model performance and metrics
    - Technical specifications
    - Code documentation and algorithms
    """
    
    def __init__(self, template_id: str = "technical_report", template_name: str = "Technical Report", version: str = "1.0.0"):
        """Initialize technical template."""
        super().__init__(template_id, template_name, version)
        
        # Initialize component builders
        self.section_builder = SectionBuilder()
        self.methodology_builder = TechnicalMethodologyBuilder()
        self.statistical_analysis = TechnicalStatisticalAnalysis()
        self.appendices = TechnicalAppendices()
        
        self.logger = logging.getLogger(__name__)
    
    def get_description(self) -> str:
        """Get template description."""
        return ("Technical Report Template for data scientists and engineers. "
                "Provides detailed methodology, statistical analysis, model performance metrics, "
                "and comprehensive technical documentation.")
    
    def get_supported_formats(self) -> List[str]:
        """Get supported output formats."""
        return ["html", "pdf", "json"]
    
    def validate_data(self, data: ReportData) -> Tuple[bool, List[str]]:
        """
        Validate input data for technical template.
        
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
            
            # Technical-specific validation
            has_technical_data = any([
                data.bias_analysis_data,  # Most important for technical reports
                data.risk_simulation_data,
                data.regulatory_data
            ])
            
            if not has_technical_data:
                errors.append("Technical report requires at least bias analysis or risk simulation data")
            
            # Check for technical details
            if data.bias_analysis_data:
                bias_data = data.bias_analysis_data
                if not bias_data.get("model_info"):
                    errors.append("Bias analysis data missing model information")
                if not bias_data.get("fairness_metrics"):
                    errors.append("Bias analysis data missing fairness metrics")
            
            if data.risk_simulation_data:
                risk_data = data.risk_simulation_data
                if not risk_data.get("simulation_results"):
                    errors.append("Risk simulation data missing simulation results")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            self.logger.error(f"Data validation error: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def generate_sections(self, data: ReportData) -> List[ReportSection]:
        """
        Generate technical report sections.
        
        Args:
            data: Report data
            
        Returns:
            List of report sections
        """
        try:
            sections = []
            
            # 1. Technical Overview (Order: 1)
            overview_section = self._generate_technical_overview(data)
            sections.append(overview_section)
            
            # 2. Methodology (Order: 2)
            methodology_section = self._generate_methodology_section(data)
            sections.append(methodology_section)
            
            # 3. Data Analysis (Order: 3)
            data_analysis_section = self._generate_data_analysis_section(data)
            sections.append(data_analysis_section)
            
            # 4. Model Performance (Order: 4)
            performance_section = self._generate_model_performance_section(data)
            sections.append(performance_section)
            
            # 5. Statistical Analysis (Order: 5)
            statistical_section = self._generate_statistical_analysis_section(data)
            sections.append(statistical_section)
            
            # 6. Results and Findings (Order: 6)
            results_section = self._generate_results_section(data)
            sections.append(results_section)
            
            # 7. Technical Recommendations (Order: 7)
            tech_recommendations_section = self._generate_technical_recommendations(data)
            sections.append(tech_recommendations_section)
            
            # 8. Technical Appendices (Order: 8)
            appendices_section = self._generate_appendices_section(data)
            sections.append(appendices_section)
            
            self.logger.info(f"Generated {len(sections)} technical report sections")
            return sections
            
        except Exception as e:
            self.logger.error(f"Failed to generate technical sections: {str(e)}")
            raise
    
    def _generate_technical_overview(self, data: ReportData) -> ReportSection:
        """Generate technical overview section."""
        try:
            overview_data = {
                "analysis_scope": self._determine_analysis_scope(data),
                "data_sources": self._identify_data_sources(data),
                "methodologies_used": self._list_methodologies(data),
                "key_technologies": self._identify_technologies(data),
                "analysis_period": "Current analysis",
                "technical_summary": self._generate_technical_summary(data)
            }
            
            return self.section_builder.build_summary_section(
                title="Technical Overview",
                summary_data=overview_data,
                section_id="technical_overview",
                order=1
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate technical overview: {str(e)}")
            return ReportSection(
                section_id="technical_overview",
                title="Technical Overview",
                content="<p><em>Technical overview could not be generated.</em></p>",
                section_type="summary",
                order=1
            )
    
    def _generate_methodology_section(self, data: ReportData) -> ReportSection:
        """Generate methodology section."""
        try:
            methodology_content = self.methodology_builder.build_methodology_documentation(data)
            
            return self.section_builder.build_text_section(
                title="Methodology",
                text_content=methodology_content,
                section_id="methodology",
                order=2,
                format_as_html=True
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate methodology section: {str(e)}")
            return ReportSection(
                section_id="methodology",
                title="Methodology",
                content="<p><em>Methodology documentation could not be generated.</em></p>",
                section_type="text",
                order=2
            )
    
    def _generate_data_analysis_section(self, data: ReportData) -> ReportSection:
        """Generate data analysis section."""
        try:
            analysis_data = []
            
            # Bias analysis data
            if data.bias_analysis_data:
                model_info = data.bias_analysis_data.get("model_info", {})
                analysis_data.append({
                    "analysis_type": "Bias Analysis",
                    "model_id": model_info.get("model_id", "unknown"),
                    "model_type": model_info.get("model_type", "unknown"),
                    "dataset_size": "N/A",  # Would be extracted from actual data
                    "features_analyzed": len(data.bias_analysis_data.get("explainability", {}).get("feature_importance", {}))
                })
            
            # Risk simulation data
            if data.risk_simulation_data:
                sim_results = data.risk_simulation_data.get("simulation_results", {})
                analysis_data.append({
                    "analysis_type": "Risk Simulation",
                    "simulation_id": sim_results.get("simulation_id", "unknown"),
                    "simulation_type": sim_results.get("simulation_type", "monte_carlo"),
                    "iterations": sim_results.get("iterations", 0),
                    "convergence": sim_results.get("convergence", "unknown")
                })
            
            # Regulatory analysis data
            if data.regulatory_data:
                analysis_data.append({
                    "analysis_type": "Regulatory Analysis",
                    "regulations_analyzed": data.regulatory_data.get("summary", {}).get("total_regulations", 0),
                    "compliance_score": data.regulatory_data.get("summary", {}).get("compliance_score", 0.0),
                    "risk_level": data.regulatory_data.get("risk_assessment", {}).get("risk_level", "unknown")
                })
            
            return self.section_builder.build_data_table_section(
                title="Data Analysis Summary",
                table_data=analysis_data,
                section_id="data_analysis",
                order=3
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate data analysis section: {str(e)}")
            return ReportSection(
                section_id="data_analysis",
                title="Data Analysis Summary",
                content="<p><em>Data analysis summary could not be generated.</em></p>",
                section_type="data_table",
                order=3
            )
    
    def _generate_model_performance_section(self, data: ReportData) -> ReportSection:
        """Generate model performance section."""
        try:
            performance_metrics = {}
            
            if data.bias_analysis_data:
                model_info = data.bias_analysis_data.get("model_info", {})
                perf_metrics = model_info.get("performance_metrics", {})
                
                # Add model performance metrics
                performance_metrics.update(perf_metrics)
                
                # Add fairness metrics
                fairness_metrics = data.bias_analysis_data.get("fairness_metrics", {})
                for metric, value in fairness_metrics.items():
                    performance_metrics[f"fairness_{metric}"] = value
                
                # Add bias score
                bias_score = data.bias_analysis_data.get("bias_score", {})
                performance_metrics["overall_bias_score"] = bias_score.get("overall_score", 0.0)
            
            if not performance_metrics:
                performance_metrics = {"status": "No model performance data available"}
            
            return self.section_builder.build_metrics_section(
                title="Model Performance Metrics",
                metrics_data=performance_metrics,
                section_id="model_performance",
                order=4
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate model performance section: {str(e)}")
            return ReportSection(
                section_id="model_performance",
                title="Model Performance Metrics",
                content="<p><em>Model performance metrics could not be generated.</em></p>",
                section_type="metrics",
                order=4
            )
    
    def _generate_statistical_analysis_section(self, data: ReportData) -> ReportSection:
        """Generate statistical analysis section."""
        try:
            statistical_content = self.statistical_analysis.build_statistical_analysis(data)
            
            return self.section_builder.build_text_section(
                title="Statistical Analysis",
                text_content=statistical_content,
                section_id="statistical_analysis",
                order=5,
                format_as_html=True
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate statistical analysis section: {str(e)}")
            return ReportSection(
                section_id="statistical_analysis",
                title="Statistical Analysis",
                content="<p><em>Statistical analysis could not be generated.</em></p>",
                section_type="text",
                order=5
            )
    
    def _generate_results_section(self, data: ReportData) -> ReportSection:
        """Generate results and findings section."""
        try:
            results_data = {
                "key_findings": self._extract_key_findings(data),
                "technical_insights": self._extract_technical_insights(data),
                "performance_summary": self._summarize_performance(data),
                "limitations": self._identify_limitations(data),
                "validation_results": self._summarize_validation(data)
            }
            
            return self.section_builder.build_summary_section(
                title="Results and Findings",
                summary_data=results_data,
                section_id="results_findings",
                order=6
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate results section: {str(e)}")
            return ReportSection(
                section_id="results_findings",
                title="Results and Findings",
                content="<p><em>Results and findings could not be generated.</em></p>",
                section_type="summary",
                order=6
            )
    
    def _generate_technical_recommendations(self, data: ReportData) -> ReportSection:
        """Generate technical recommendations section."""
        try:
            tech_recommendations = []
            
            # Bias analysis recommendations
            if data.bias_analysis_data:
                bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 1.0)
                if bias_score < 0.8:
                    tech_recommendations.extend([
                        "Implement additional bias mitigation techniques in preprocessing pipeline",
                        "Consider ensemble methods to reduce model bias",
                        "Increase training data diversity for underrepresented groups"
                    ])
                
                flagged_attrs = data.bias_analysis_data.get("bias_score", {}).get("flagged_attributes", [])
                if flagged_attrs:
                    tech_recommendations.append(f"Focus bias mitigation on attributes: {', '.join(flagged_attrs)}")
            
            # Risk simulation recommendations
            if data.risk_simulation_data:
                risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                if risk_prob > 0.2:
                    tech_recommendations.extend([
                        "Enhance risk monitoring with real-time alerting systems",
                        "Implement additional scenario testing for edge cases",
                        "Improve model calibration for better risk prediction accuracy"
                    ])
            
            # Regulatory recommendations
            if data.regulatory_data:
                compliance_score = data.regulatory_data.get("summary", {}).get("compliance_score", 1.0)
                if compliance_score < 0.9:
                    tech_recommendations.extend([
                        "Automate compliance checking in CI/CD pipeline",
                        "Implement automated regulatory change detection",
                        "Enhance documentation and audit trail generation"
                    ])
            
            # General technical recommendations
            tech_recommendations.extend([
                "Implement comprehensive model monitoring and alerting",
                "Establish automated testing for model fairness and performance",
                "Create detailed technical documentation for all models and processes"
            ])
            
            return self.section_builder.build_recommendations_section(
                title="Technical Recommendations",
                recommendations=tech_recommendations,
                section_id="technical_recommendations",
                order=7
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate technical recommendations: {str(e)}")
            return ReportSection(
                section_id="technical_recommendations",
                title="Technical Recommendations",
                content="<p><em>Technical recommendations could not be generated.</em></p>",
                section_type="recommendations",
                order=7
            )
    
    def _generate_appendices_section(self, data: ReportData) -> ReportSection:
        """Generate technical appendices section."""
        try:
            appendices_content = self.appendices.build_technical_appendices(data)
            
            return self.section_builder.build_text_section(
                title="Technical Appendices",
                text_content=appendices_content,
                section_id="technical_appendices",
                order=8,
                format_as_html=True
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate appendices section: {str(e)}")
            return ReportSection(
                section_id="technical_appendices",
                title="Technical Appendices",
                content="<p><em>Technical appendices could not be generated.</em></p>",
                section_type="text",
                order=8
            )
    
    # Helper methods for data extraction
    def _determine_analysis_scope(self, data: ReportData) -> str:
        """Determine the scope of analysis."""
        scopes = []
        if data.regulatory_data:
            scopes.append("Regulatory Compliance Analysis")
        if data.bias_analysis_data:
            scopes.append("AI Model Bias and Fairness Analysis")
        if data.risk_simulation_data:
            scopes.append("Risk Simulation and Prediction")
        
        return ", ".join(scopes) if scopes else "General Analysis"
    
    def _identify_data_sources(self, data: ReportData) -> List[str]:
        """Identify data sources used in analysis."""
        sources = []
        if data.regulatory_data:
            sources.append("Regulatory Intelligence Engine (Phase 2)")
        if data.bias_analysis_data:
            sources.append("Bias Analysis System (Phase 3)")
        if data.risk_simulation_data:
            sources.append("Risk Simulation Engine (Phase 4)")
        
        return sources
    
    def _list_methodologies(self, data: ReportData) -> List[str]:
        """List methodologies used in analysis."""
        methodologies = []
        
        if data.bias_analysis_data:
            methodologies.extend([
                "SHAP (SHapley Additive exPlanations)",
                "LIME (Local Interpretable Model-agnostic Explanations)",
                "Fairness Metrics (Demographic Parity, Equalized Odds)",
                "Bias Mitigation Techniques"
            ])
        
        if data.risk_simulation_data:
            sim_type = data.risk_simulation_data.get("simulation_results", {}).get("simulation_type", "")
            if sim_type:
                methodologies.append(f"{sim_type.replace('_', ' ').title()} Simulation")
            methodologies.extend([
                "Monte Carlo Methods",
                "Bayesian Inference",
                "Scenario Analysis"
            ])
        
        if data.regulatory_data:
            methodologies.extend([
                "Natural Language Processing",
                "Regulatory Text Analysis",
                "Compliance Mapping"
            ])
        
        return methodologies
    
    def _identify_technologies(self, data: ReportData) -> List[str]:
        """Identify key technologies used."""
        return [
            "Python 3.9+",
            "scikit-learn",
            "SHAP",
            "LIME", 
            "Fairlearn",
            "AIF360",
            "PyMC5",
            "NumPy",
            "Pandas"
        ]
    
    def _generate_technical_summary(self, data: ReportData) -> str:
        """Generate technical summary text."""
        summary_parts = []
        
        if data.bias_analysis_data:
            bias_score = data.bias_analysis_data.get("bias_score", {}).get("overall_score", 0.0)
            summary_parts.append(f"Bias analysis completed with overall fairness score of {bias_score:.3f}")
        
        if data.risk_simulation_data:
            risk_prob = data.risk_simulation_data.get("risk_metrics", {}).get("risk_probability", 0.0)
            summary_parts.append(f"Risk simulation indicates {risk_prob:.1%} probability of compliance violations")
        
        if data.regulatory_data:
            compliance_score = data.regulatory_data.get("summary", {}).get("compliance_score", 0.0)
            summary_parts.append(f"Regulatory analysis shows {compliance_score:.1%} compliance rate")
        
        return ". ".join(summary_parts) if summary_parts else "Technical analysis completed successfully"
    
    def _extract_key_findings(self, data: ReportData) -> List[str]:
        """Extract key technical findings."""
        findings = []
        
        if data.bias_analysis_data:
            bias_score = data.bias_analysis_data.get("bias_score", {})
            overall_score = bias_score.get("overall_score", 0.0)
            findings.append(f"Model fairness score: {overall_score:.3f}")
            
            flagged_attrs = bias_score.get("flagged_attributes", [])
            if flagged_attrs:
                findings.append(f"Bias detected in attributes: {', '.join(flagged_attrs)}")
        
        if data.risk_simulation_data:
            risk_metrics = data.risk_simulation_data.get("risk_metrics", {})
            findings.append(f"Risk probability: {risk_metrics.get('risk_probability', 0.0):.3f}")
            findings.append(f"Expected impact: {risk_metrics.get('expected_impact', 0.0):.2f}")
        
        return findings
    
    def _extract_technical_insights(self, data: ReportData) -> List[str]:
        """Extract technical insights."""
        insights = []
        
        if data.bias_analysis_data:
            explainability = data.bias_analysis_data.get("explainability", {})
            top_features = explainability.get("top_features", [])
            if top_features:
                insights.append(f"Top influential features: {', '.join(top_features[:3])}")
        
        if data.risk_simulation_data:
            scenarios = data.risk_simulation_data.get("scenarios", [])
            if scenarios:
                insights.append(f"Analyzed {len(scenarios)} risk scenarios")
        
        return insights
    
    def _summarize_performance(self, data: ReportData) -> str:
        """Summarize model performance."""
        if data.bias_analysis_data:
            model_info = data.bias_analysis_data.get("model_info", {})
            perf_metrics = model_info.get("performance_metrics", {})
            
            if perf_metrics:
                metrics_str = ", ".join([f"{k}: {v:.3f}" for k, v in perf_metrics.items() if isinstance(v, (int, float))])
                return f"Model performance metrics: {metrics_str}"
        
        return "Performance metrics not available"
    
    def _identify_limitations(self, data: ReportData) -> List[str]:
        """Identify analysis limitations."""
        limitations = [
            "Analysis based on available data at time of report generation",
            "Results may vary with different datasets or model configurations",
            "Recommendations should be validated in specific deployment contexts"
        ]
        
        if not data.bias_analysis_data:
            limitations.append("Bias analysis not available - fairness assessment limited")
        
        if not data.risk_simulation_data:
            limitations.append("Risk simulation not available - predictive insights limited")
        
        return limitations
    
    def _summarize_validation(self, data: ReportData) -> str:
        """Summarize validation results."""
        validation_parts = []
        
        if data.bias_analysis_data:
            validation_parts.append("Bias analysis validation: Statistical significance tests applied")
        
        if data.risk_simulation_data:
            sim_results = data.risk_simulation_data.get("simulation_results", {})
            convergence = sim_results.get("convergence", "unknown")
            validation_parts.append(f"Risk simulation validation: Convergence status - {convergence}")
        
        return "; ".join(validation_parts) if validation_parts else "Validation results not available"
    
    def __str__(self) -> str:
        """String representation."""
        return f"TechnicalTemplate(id={self.template_id})"
