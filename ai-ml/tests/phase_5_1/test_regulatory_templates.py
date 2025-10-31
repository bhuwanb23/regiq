#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.1 Regulatory Template Tests
Unit tests for regulatory template components.
"""

import pytest
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.base.base_template import ReportData
from services.report_generator.templates.regulatory.regulatory_template import RegulatoryTemplate


class TestRegulatoryTemplate:
    """Test RegulatoryTemplate class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.template = RegulatoryTemplate()
        
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
    
    def test_template_initialization(self):
        """Test regulatory template initialization."""
        assert self.template.template_id == "regulatory_report"
        assert self.template.template_name == "Regulatory Compliance Report"
        assert "Regulatory Compliance Report Template" in self.template.get_description()
        assert "html" in self.template.get_supported_formats()
    
    def test_data_validation_success(self):
        """Test successful data validation."""
        is_valid, errors = self.template.validate_data(self.sample_data)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_data_validation_failure_no_regulatory_data(self):
        """Test data validation failure without regulatory data."""
        data_without_regulatory = ReportData(bias_analysis_data={"test": "data"})
        is_valid, errors = self.template.validate_data(data_without_regulatory)
        assert is_valid is False
        assert any("regulatory intelligence data" in error for error in errors)
    
    def test_generate_sections(self):
        """Test section generation."""
        sections = self.template.generate_sections(self.sample_data)
        
        assert len(sections) == 6  # Expected number of sections
        
        # Check section IDs
        section_ids = [s.section_id for s in sections]
        expected_ids = [
            "compliance_summary",
            "compliance_status",
            "evidence_documentation",
            "gap_analysis",
            "audit_trail",
            "remediation_plan"
        ]
        
        for expected_id in expected_ids:
            assert expected_id in section_ids
    
    def test_generate_report_html(self):
        """Test HTML report generation."""
        report = self.template.generate_report(self.sample_data, "html")
        
        assert isinstance(report, dict)
        assert "content" in report
        assert "<!DOCTYPE html>" in report["content"]
        assert "Regulatory Compliance Report" in report["content"]
    
    def test_generate_report_json(self):
        """Test JSON report generation."""
        report = self.template.generate_report(self.sample_data, "json")
        
        assert isinstance(report, dict)
        assert "content" in report
        assert isinstance(report["content"], dict)
        assert "sections" in report["content"]


class TestRegulatoryTemplateIntegration:
    """Test regulatory template integration."""
    
    def test_end_to_end_regulatory_report(self):
        """Test complete regulatory report generation."""
        template = RegulatoryTemplate()
        
        # Load sample data
        sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
        
        with open(sample_data_path / "regulatory_intelligence_output.json") as f:
            regulatory_data = json.load(f)
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            bias_data = json.load(f)
        
        sample_data = ReportData(
            regulatory_data=regulatory_data,
            bias_analysis_data=bias_data
        )
        
        # Generate HTML report
        html_report = template.generate_report(sample_data, "html")
        
        assert isinstance(html_report, dict)
        assert "content" in html_report
        assert "template_metadata" in html_report
        
        # Check HTML content
        html_content = html_report["content"]
        assert "<!DOCTYPE html>" in html_content
        assert "Compliance Executive Summary" in html_content
        assert "Audit Trail" in html_content
        assert "Remediation Plan" in html_content


if __name__ == "__main__":
    pytest.main([__file__])
