#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.1 Technical Template Tests
Unit tests for technical template components.
"""

import pytest
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.base.base_template import ReportData
from services.report_generator.templates.technical.technical_template import TechnicalTemplate


class TestTechnicalTemplate:
    """Test TechnicalTemplate class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.template = TechnicalTemplate()
        
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
    
    def test_template_initialization(self):
        """Test technical template initialization."""
        assert self.template.template_id == "technical_report"
        assert self.template.template_name == "Technical Report"
        assert "Technical Report Template" in self.template.get_description()
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
        
        assert len(sections) == 8  # Expected number of sections
        
        # Check section IDs
        section_ids = [s.section_id for s in sections]
        expected_ids = [
            "technical_overview",
            "methodology",
            "data_analysis",
            "model_performance",
            "statistical_analysis",
            "results_findings",
            "technical_recommendations",
            "technical_appendices"
        ]
        
        for expected_id in expected_ids:
            assert expected_id in section_ids
    
    def test_generate_report_html(self):
        """Test HTML report generation."""
        report = self.template.generate_report(self.sample_data, "html")
        
        assert isinstance(report, dict)
        assert "content" in report
        assert "<!DOCTYPE html>" in report["content"]
        assert "Technical Report" in report["content"]
    
    def test_generate_report_json(self):
        """Test JSON report generation."""
        report = self.template.generate_report(self.sample_data, "json")
        
        assert isinstance(report, dict)
        assert "content" in report
        assert isinstance(report["content"], dict)
        assert "sections" in report["content"]


class TestTechnicalTemplateIntegration:
    """Test technical template integration."""
    
    def test_end_to_end_technical_report(self):
        """Test complete technical report generation."""
        template = TechnicalTemplate()
        
        # Load sample data
        sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            bias_data = json.load(f)
        
        with open(sample_data_path / "risk_simulation_output.json") as f:
            risk_data = json.load(f)
        
        sample_data = ReportData(
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
        assert "Technical Overview" in html_content
        assert "Methodology" in html_content
        assert "Model Performance" in html_content


if __name__ == "__main__":
    pytest.main([__file__])
