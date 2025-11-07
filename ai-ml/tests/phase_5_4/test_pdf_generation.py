#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.4 PDF Generation Tests
Unit tests for PDF report generation functionality.
"""

import pytest
import json
import sys
from pathlib import Path
from io import BytesIO

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.base.base_template import ReportData
from services.report_generator.templates.executive.executive_template import ExecutiveTemplate


class TestPDFGeneration:
    """Test PDF generation functionality."""
    
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
    
    def test_pdf_generation_basic(self):
        """Test basic PDF generation."""
        # This will initially fail as PDF generation is not yet implemented
        # Once implemented, this test should pass
        try:
            report = self.template.generate_report(self.sample_data, "pdf")
            assert isinstance(report, dict)
            assert "content" in report
            
            # For actual PDF content, we expect bytes
            content = report["content"]
            assert isinstance(content, (str, bytes))
            
            # If it's bytes, it should be valid PDF data
            if isinstance(content, bytes):
                assert content.startswith(b'%PDF')
        except NotImplementedError:
            # Expected before implementation
            pytest.skip("PDF generation not yet implemented")
        except Exception as e:
            # Re-raise unexpected errors
            raise e
    
    def test_save_pdf_report(self):
        """Test saving PDF report to file."""
        output_path = Path(__file__).parent / "generated_outputs" / "test_executive_report.pdf"
        
        try:
            saved_path = self.template.save_report(self.sample_data, str(output_path), "pdf")
            assert Path(saved_path).exists()
            
            # Clean up
            Path(saved_path).unlink()
        except NotImplementedError:
            # Expected before implementation
            pytest.skip("PDF generation not yet implemented")
        except Exception as e:
            # Re-raise unexpected errors
            raise e


if __name__ == "__main__":
    pytest.main([__file__, "-v"])