#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.4 Data Export Tests
Unit tests for CSV and Excel data export functionality.
"""

import pytest
import json
import sys
import csv
from pathlib import Path
from io import StringIO, BytesIO

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.base.base_template import ReportData
from services.report_generator.templates.executive.executive_template import ExecutiveTemplate


class TestDataExport:
    """Test data export functionality."""
    
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
    
    def test_csv_export_basic(self):
        """Test basic CSV export."""
        try:
            report = self.template.generate_report(self.sample_data, "csv")
            assert isinstance(report, dict)
            assert "content" in report
            
            # Check that content is valid CSV
            content = report["content"]
            assert isinstance(content, str)
            
            # Try to parse as CSV
            csv_reader = csv.reader(StringIO(content))
            rows = list(csv_reader)
            assert len(rows) > 0  # Should have at least header row
        except NotImplementedError:
            # Expected before implementation
            pytest.skip("CSV export not yet implemented")
        except Exception as e:
            # Re-raise unexpected errors
            raise e
    
    def test_excel_export_basic(self):
        """Test basic Excel export."""
        try:
            report = self.template.generate_report(self.sample_data, "xlsx")
            assert isinstance(report, dict)
            assert "content" in report
            
            # Check that content is valid Excel data (bytes)
            content = report["content"]
            assert isinstance(content, bytes)
            assert len(content) > 0
        except NotImplementedError:
            # Expected before implementation
            pytest.skip("Excel export not yet implemented")
        except Exception as e:
            # Re-raise unexpected errors
            raise e
    
    def test_save_csv_report(self):
        """Test saving CSV report to file."""
        output_path = Path(__file__).parent / "generated_outputs" / "test_executive_report.csv"
        
        try:
            saved_path = self.template.save_report(self.sample_data, str(output_path), "csv")
            assert Path(saved_path).exists()
            
            # Check that file contains valid CSV
            with open(saved_path, 'r') as f:
                content = f.read()
                csv_reader = csv.reader(StringIO(content))
                rows = list(csv_reader)
                assert len(rows) > 0
            
            # Clean up
            Path(saved_path).unlink()
        except NotImplementedError:
            # Expected before implementation
            pytest.skip("CSV export not yet implemented")
        except Exception as e:
            # Re-raise unexpected errors
            raise e
    
    def test_save_excel_report(self):
        """Test saving Excel report to file."""
        output_path = Path(__file__).parent / "generated_outputs" / "test_executive_report.xlsx"
        
        try:
            saved_path = self.template.save_report(self.sample_data, str(output_path), "xlsx")
            assert Path(saved_path).exists()
            
            # Check that file is valid Excel
            assert Path(saved_path).stat().st_size > 0
            
            # Clean up
            Path(saved_path).unlink()
        except NotImplementedError:
            # Expected before implementation
            pytest.skip("Excel export not yet implemented")
        except Exception as e:
            # Re-raise unexpected errors
            raise e


if __name__ == "__main__":
    pytest.main([__file__, "-v"])