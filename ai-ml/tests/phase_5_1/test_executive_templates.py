#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.1 Executive Template Tests
Unit tests for executive template components.
"""

import pytest
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.base.base_template import ReportData
from services.report_generator.templates.executive.executive_template import ExecutiveTemplate
from services.report_generator.templates.executive.summary_sections import ExecutiveSummaryBuilder
from services.report_generator.templates.executive.metrics_display import ExecutiveMetricsDisplay
from services.report_generator.templates.executive.recommendations import ExecutiveRecommendations


class TestExecutiveTemplate:
    """Test ExecutiveTemplate class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.template = ExecutiveTemplate()
        
        # Load sample data
        sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
        
        with open(sample_data_path / "regulatory_intelligence_output.json") as f:
            regulatory_data = json.load(f)
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            bias_data = json.load(f)
        
        with open(sample_data_path / "risk_simulation_output.json") as f:
            risk_data = json.load(f)
        
        self.sample_data = ReportData(
            regulatory_data=regulatory_data,
            bias_analysis_data=bias_data,
            risk_simulation_data=risk_data
        )
    
    def test_template_initialization(self):
        """Test executive template initialization."""
        assert self.template.template_id == "executive_report"
        assert self.template.template_name == "Executive Report"
        assert "Executive Report Template" in self.template.get_description()
        assert "html" in self.template.get_supported_formats()
    
    def test_data_validation_success(self):
        """Test successful data validation."""
        is_valid, errors = self.template.validate_data(self.sample_data)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_data_validation_failure(self):
        """Test data validation failure."""
        empty_data = ReportData()
        is_valid, errors = self.template.validate_data(empty_data)
        assert is_valid is False
        assert len(errors) > 0
    
    def test_generate_sections(self):
        """Test section generation."""
        sections = self.template.generate_sections(self.sample_data)
        
        assert len(sections) == 7  # Expected number of sections
        
        # Check section IDs
        section_ids = [s.section_id for s in sections]
        expected_ids = [
            "executive_summary",
            "key_metrics", 
            "risk_overview",
            "compliance_status",
            "strategic_recommendations",
            "financial_impact",
            "action_items"
        ]
        
        for expected_id in expected_ids:
            assert expected_id in section_ids
    
    def test_generate_report_html(self):
        """Test HTML report generation."""
        report = self.template.generate_report(self.sample_data, "html")
        
        assert isinstance(report, dict)
        assert "content" in report
        assert "<!DOCTYPE html>" in report["content"]
        assert "Executive Report" in report["content"]
    
    def test_generate_report_json(self):
        """Test JSON report generation."""
        report = self.template.generate_report(self.sample_data, "json")
        
        assert isinstance(report, dict)
        assert "content" in report
        assert isinstance(report["content"], dict)
        assert "sections" in report["content"]
    
    def test_get_executive_insights(self):
        """Test executive insights generation."""
        insights = self.template.get_executive_insights(self.sample_data)
        
        assert isinstance(insights, dict)
        assert "overall_health_score" in insights
        assert "critical_issues" in insights
        assert "opportunities" in insights
        assert "risk_factors" in insights


class TestExecutiveSummaryBuilder:
    """Test ExecutiveSummaryBuilder class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.builder = ExecutiveSummaryBuilder()
        
        # Load sample data
        sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
        
        with open(sample_data_path / "regulatory_intelligence_output.json") as f:
            regulatory_data = json.load(f)
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            bias_data = json.load(f)
        
        self.sample_data = ReportData(
            regulatory_data=regulatory_data,
            bias_analysis_data=bias_data
        )
    
    def test_build_executive_summary(self):
        """Test executive summary building."""
        summary = self.builder.build_executive_summary(self.sample_data)
        
        assert isinstance(summary, dict)
        assert "overview" in summary
        assert "key_points" in summary
        assert "business_impact" in summary
        assert "strategic_priorities" in summary
        
        # Check that overview is a string
        assert isinstance(summary["overview"], str)
        assert len(summary["overview"]) > 0
        
        # Check that key points is a list
        assert isinstance(summary["key_points"], list)
        assert len(summary["key_points"]) > 0


class TestExecutiveMetricsDisplay:
    """Test ExecutiveMetricsDisplay class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.metrics_display = ExecutiveMetricsDisplay()
        
        # Load sample data
        sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            bias_data = json.load(f)
        
        with open(sample_data_path / "risk_simulation_output.json") as f:
            risk_data = json.load(f)
        
        self.sample_data = ReportData(
            bias_analysis_data=bias_data,
            risk_simulation_data=risk_data
        )
    
    def test_build_executive_metrics(self):
        """Test executive metrics building."""
        metrics = self.metrics_display.build_executive_metrics(self.sample_data)
        
        assert isinstance(metrics, dict)
        assert len(metrics) > 0
        
        # Check for expected metric types
        assert "overall_health_score" in metrics
        assert isinstance(metrics["overall_health_score"], (int, float))
        assert 0.0 <= metrics["overall_health_score"] <= 1.0
    
    def test_get_metric_interpretation(self):
        """Test metric interpretation."""
        interpretation = self.metrics_display.get_metric_interpretation(
            "overall_health_score", 0.85
        )
        
        assert isinstance(interpretation, dict)
        assert "status" in interpretation
        assert "description" in interpretation
        assert interpretation["status"] in ["excellent", "good", "fair", "poor"]


class TestExecutiveRecommendations:
    """Test ExecutiveRecommendations class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.recommendations = ExecutiveRecommendations()
        
        # Load sample data
        sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
        
        with open(sample_data_path / "regulatory_intelligence_output.json") as f:
            regulatory_data = json.load(f)
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            bias_data = json.load(f)
        
        self.sample_data = ReportData(
            regulatory_data=regulatory_data,
            bias_analysis_data=bias_data
        )
    
    def test_build_executive_recommendations(self):
        """Test executive recommendations building."""
        recs = self.recommendations.build_executive_recommendations(self.sample_data)
        
        assert isinstance(recs, list)
        assert len(recs) > 0
        
        # Check that recommendations are strings
        for rec in recs:
            assert isinstance(rec, str)
            assert len(rec) > 0
    
    def test_get_implementation_guidance(self):
        """Test implementation guidance."""
        guidance = self.recommendations.get_implementation_guidance(
            "Implement comprehensive compliance framework"
        )
        
        assert isinstance(guidance, dict)
        assert "steps" in guidance
        assert "resources" in guidance
        assert "timeline" in guidance


class TestExecutiveTemplateIntegration:
    """Test executive template integration."""
    
    def test_end_to_end_executive_report(self):
        """Test complete executive report generation."""
        template = ExecutiveTemplate()
        
        # Load all sample data
        sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
        
        with open(sample_data_path / "regulatory_intelligence_output.json") as f:
            regulatory_data = json.load(f)
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            bias_data = json.load(f)
        
        with open(sample_data_path / "risk_simulation_output.json") as f:
            risk_data = json.load(f)
        
        sample_data = ReportData(
            regulatory_data=regulatory_data,
            bias_analysis_data=bias_data,
            risk_simulation_data=risk_data
        )
        
        # Generate HTML report
        html_report = template.generate_report(sample_data, "html")
        
        assert isinstance(html_report, dict)
        assert "content" in html_report
        assert "template_metadata" in html_report
        
        # Check HTML content
        html_content = html_report["content"]
        assert "<!DOCTYPE html>" in html_content
        assert "Executive Summary" in html_content
        assert "Key Performance Indicators" in html_content
        assert "Strategic Recommendations" in html_content
        
        # Generate JSON report
        json_report = template.generate_report(sample_data, "json")
        
        assert isinstance(json_report, dict)
        assert "content" in json_report
        assert isinstance(json_report["content"], dict)
        
        # Check JSON structure
        json_content = json_report["content"]
        assert "sections" in json_content
        assert len(json_content["sections"]) == 7


if __name__ == "__main__":
    pytest.main([__file__])
