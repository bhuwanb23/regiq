#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.1 Data Formatter Tests
Unit tests for data formatter and utilities.
"""

import pytest
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.utils.data_formatter import DataFormatter
from services.report_generator.templates.base.base_template import ReportData


class TestDataFormatter:
    """Test DataFormatter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = DataFormatter()
        
        # Load sample data
        sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
        
        with open(sample_data_path / "regulatory_intelligence_output.json") as f:
            self.regulatory_data = json.load(f)
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            self.bias_data = json.load(f)
        
        with open(sample_data_path / "risk_simulation_output.json") as f:
            self.risk_data = json.load(f)
    
    def test_formatter_initialization(self):
        """Test data formatter initialization."""
        assert len(self.formatter.supported_phases) == 3
        assert "phase_2" in self.formatter.supported_phases
        assert "phase_3" in self.formatter.supported_phases
        assert "phase_4" in self.formatter.supported_phases
    
    def test_format_regulatory_data(self):
        """Test regulatory data formatting."""
        formatted = self.formatter.format_regulatory_data(self.regulatory_data)
        
        assert formatted.source_phase == "phase_2"
        assert formatted.data_type == "regulatory_intelligence"
        assert isinstance(formatted.formatted_data, dict)
        
        # Check required fields
        assert "summary" in formatted.formatted_data
        assert "regulations" in formatted.formatted_data
        assert "compliance_status" in formatted.formatted_data
    
    def test_format_bias_analysis_data(self):
        """Test bias analysis data formatting."""
        formatted = self.formatter.format_bias_analysis_data(self.bias_data)
        
        assert formatted.source_phase == "phase_3"
        assert formatted.data_type == "bias_analysis"
        assert isinstance(formatted.formatted_data, dict)
        
        # Check required fields
        assert "model_info" in formatted.formatted_data
        assert "fairness_metrics" in formatted.formatted_data
        assert "bias_score" in formatted.formatted_data
    
    def test_format_risk_simulation_data(self):
        """Test risk simulation data formatting."""
        formatted = self.formatter.format_risk_simulation_data(self.risk_data)
        
        assert formatted.source_phase == "phase_4"
        assert formatted.data_type == "risk_simulation"
        assert isinstance(formatted.formatted_data, dict)
        
        # Check required fields
        assert "simulation_results" in formatted.formatted_data
        assert "risk_metrics" in formatted.formatted_data
        assert "scenarios" in formatted.formatted_data
    
    def test_create_report_data_all_sources(self):
        """Test creating ReportData with all data sources."""
        report_data = self.formatter.create_report_data(
            regulatory_data=self.regulatory_data,
            bias_data=self.bias_data,
            risk_data=self.risk_data
        )
        
        assert isinstance(report_data, ReportData)
        assert report_data.regulatory_data is not None
        assert report_data.bias_analysis_data is not None
        assert report_data.risk_simulation_data is not None
        
        # Validate the created data
        is_valid, errors = report_data.validate()
        assert is_valid is True
        assert len(errors) == 0
    
    def test_create_report_data_single_source(self):
        """Test creating ReportData with single data source."""
        report_data = self.formatter.create_report_data(
            bias_data=self.bias_data
        )
        
        assert isinstance(report_data, ReportData)
        assert report_data.regulatory_data is None
        assert report_data.bias_analysis_data is not None
        assert report_data.risk_simulation_data is None
    
    def test_get_formatter_stats(self):
        """Test getting formatter statistics."""
        stats = self.formatter.get_formatter_stats()
        
        assert isinstance(stats, dict)
        assert "supported_phases" in stats
        assert "cache_size" in stats
        assert len(stats["supported_phases"]) == 3
    
    def test_clear_cache(self):
        """Test clearing formatter cache."""
        # Add some data to cache first
        self.formatter.format_regulatory_data(self.regulatory_data)
        
        initial_cache_size = len(self.formatter.data_cache)
        self.formatter.clear_cache()
        
        assert len(self.formatter.data_cache) == 0


if __name__ == "__main__":
    pytest.main([__file__])
