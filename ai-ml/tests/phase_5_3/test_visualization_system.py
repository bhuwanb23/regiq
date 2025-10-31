#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.3 Visualization System Tests
Comprehensive tests for data visualization system.
"""

import pytest
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.visualization.chart_engine import (
    ChartEngine, ChartConfig, ChartTemplate, ChartType
)
from services.report_generator.visualization.data_binder import (
    DataBinder, DataBinding
)
from services.report_generator.visualization.visualization_generator import (
    VisualizationGenerator, VisualizationRequest
)


class TestChartEngine:
    """Test chart engine functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = ChartEngine()
    
    def test_engine_initialization(self):
        """Test chart engine initialization."""
        assert isinstance(self.engine, ChartEngine)
        assert len(self.engine.templates) > 0
        assert len(self.engine.themes) > 0
    
    def test_chart_types_available(self):
        """Test available chart types."""
        chart_types = self.engine.list_chart_types()
        
        assert len(chart_types) >= 10
        assert "bar" in chart_types
        assert "line" in chart_types
        assert "pie" in chart_types
        assert "gauge" in chart_types
        assert "heatmap" in chart_types
    
    def test_templates_loaded(self):
        """Test chart templates are loaded."""
        templates = self.engine.list_templates()
        
        assert len(templates) > 0
        
        # Check for key templates
        template_ids = [t["template_id"] for t in templates]
        assert "compliance_gauge" in template_ids
        assert "risk_matrix" in template_ids
        assert "compliance_trends" in template_ids
    
    def test_themes_available(self):
        """Test available themes."""
        themes = self.engine.list_themes()
        
        assert "regiq" in themes
        assert "dark" in themes
        assert "high_contrast" in themes
        
        # Test theme structure
        regiq_theme = self.engine.get_theme("regiq")
        assert "background_color" in regiq_theme
        assert "compliance_colors" in regiq_theme
        assert "primary_colors" in regiq_theme
    
    def test_gauge_chart_creation(self):
        """Test gauge chart creation."""
        config = ChartConfig(
            chart_id="test_gauge",
            chart_type=ChartType.GAUGE,
            title="Test Gauge",
            data={"value": 0.78, "max_value": 1.0, "target": 0.9}
        )
        
        chart = self.engine.create_chart(config)
        
        assert chart["type"] == "gauge"
        assert chart["title"] == "Test Gauge"
        assert chart["data"]["value"] == 0.78
        assert "metadata" in chart
    
    def test_bar_chart_creation(self):
        """Test bar chart creation."""
        config = ChartConfig(
            chart_id="test_bar",
            chart_type=ChartType.BAR,
            title="Test Bar Chart",
            data={
                "categories": ["A", "B", "C"],
                "values": [10, 20, 15]
            }
        )
        
        chart = self.engine.create_chart(config)
        
        assert chart["type"] == "bar"
        assert chart["data"]["categories"] == ["A", "B", "C"]
        assert chart["data"]["values"] == [10, 20, 15]
    
    def test_heatmap_chart_creation(self):
        """Test heatmap chart creation."""
        config = ChartConfig(
            chart_id="test_heatmap",
            chart_type=ChartType.HEATMAP,
            title="Test Heatmap",
            data={
                "x_values": ["Low", "High"],
                "y_values": ["Impact", "Probability"],
                "z_values": [[0.1, 0.3], [0.2, 0.8]]
            }
        )
        
        chart = self.engine.create_chart(config)
        
        assert chart["type"] == "heatmap"
        assert len(chart["data"]["x"]) == 2
        assert len(chart["data"]["y"]) == 2
    
    def test_config_validation(self):
        """Test chart configuration validation."""
        # Valid config
        valid_config = ChartConfig(
            chart_id="valid",
            chart_type=ChartType.BAR,
            title="Valid Chart",
            data={"categories": ["A"], "values": [1]}
        )
        
        is_valid, errors = self.engine.validate_config(valid_config)
        assert is_valid is True
        assert len(errors) == 0
        
        # Invalid config (missing title)
        invalid_config = ChartConfig(
            chart_id="invalid",
            chart_type=ChartType.BAR,
            title="",
            data={}
        )
        
        is_valid, errors = self.engine.validate_config(invalid_config)
        assert is_valid is False
        assert len(errors) > 0
    
    def test_template_retrieval(self):
        """Test template retrieval."""
        template = self.engine.get_template("compliance_gauge")
        
        assert template is not None
        assert template.template_id == "compliance_gauge"
        assert template.chart_type == ChartType.GAUGE
        assert len(template.required_data_fields) > 0


class TestDataBinder:
    """Test data binding system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.binder = DataBinder()
        
        # Sample data structure
        self.sample_data = {
            "regulatory_data": {
                "summary": {
                    "compliance_score": 0.78,
                    "total_regulations": 25
                },
                "compliance_status": {
                    "compliant_count": 19,
                    "non_compliant_count": 6
                }
            },
            "bias_analysis_data": {
                "bias_score": {
                    "overall_score": 0.734,
                    "flagged_attributes": ["gender", "age"]
                },
                "model_info": {
                    "performance_metrics": {
                        "accuracy": 0.847,
                        "precision": 0.823
                    }
                },
                "fairness_metrics": {
                    "demographic_parity": 0.156,
                    "equalized_odds": 0.089
                }
            },
            "risk_simulation_data": {
                "risk_metrics": {
                    "risk_probability": 0.287,
                    "expected_impact": 0.156
                },
                "financial_impact": {
                    "total_impact": 662500
                }
            }
        }
    
    def test_binder_initialization(self):
        """Test data binder initialization."""
        assert isinstance(self.binder, DataBinder)
        assert len(self.binder.transformations) > 0
    
    def test_data_extraction(self):
        """Test data extraction using JSONPath."""
        # Test simple path
        value = self.binder._extract_data(self.sample_data, "regulatory_data.summary.compliance_score")
        assert value == 0.78
        
        # Test with $.
        value = self.binder._extract_data(self.sample_data, "$.regulatory_data.summary.total_regulations")
        assert value == 25
        
        # Test array access
        value = self.binder._extract_data(self.sample_data, "bias_analysis_data.bias_score.flagged_attributes[0]")
        assert value == "gender"
        
        # Test non-existent path
        value = self.binder._extract_data(self.sample_data, "non.existent.path")
        assert value is None
    
    def test_transformations(self):
        """Test data transformations."""
        # Test percentage transformation
        result = self.binder._apply_transformation(0.78, "percentage")
        assert result == 78.0
        
        # Test rounding
        result = self.binder._apply_transformation(0.123456, "round_3")
        assert result == 0.123
        
        # Test compliance status transformation
        result = self.binder._apply_transformation(0.85, "compliance_status")
        assert result == "good"
        
        result = self.binder._apply_transformation(0.95, "compliance_status")
        assert result == "excellent"
        
        # Test risk level transformation
        result = self.binder._apply_transformation(0.3, "risk_level")
        assert result == "medium"
    
    def test_data_type_conversion(self):
        """Test data type conversion."""
        # String conversion
        result = self.binder._convert_data_type(123, "string")
        assert result == "123"
        
        # Number conversion
        result = self.binder._convert_data_type("123.45", "float")
        assert result == 123.45
        
        # Integer conversion
        result = self.binder._convert_data_type("123", "integer")
        assert result == 123
        
        # Boolean conversion
        result = self.binder._convert_data_type(1, "boolean")
        assert result is True
    
    def test_compliance_bindings(self):
        """Test compliance data bindings."""
        bindings = self.binder.create_compliance_bindings()
        
        assert len(bindings) > 0
        
        # Test binding structure
        for binding in bindings:
            assert hasattr(binding, 'binding_id')
            assert hasattr(binding, 'source_path')
            assert hasattr(binding, 'chart_field')
            assert hasattr(binding, 'data_type')
        
        # Test data binding
        bound_data = self.binder.bind_data(self.sample_data, bindings)
        
        assert "value" in bound_data  # compliance score
        assert "status" in bound_data  # compliance status
        assert bound_data["value"] == 0.78
        assert bound_data["status"] == "fair"  # 0.78 -> fair
    
    def test_bias_analysis_bindings(self):
        """Test bias analysis data bindings."""
        bindings = self.binder.create_bias_analysis_bindings()
        bound_data = self.binder.bind_data(self.sample_data, bindings)
        
        assert "value" in bound_data  # bias score
        assert "flagged" in bound_data  # flagged attributes
        assert "accuracy" in bound_data  # model accuracy
        
        assert bound_data["value"] == 0.734
        assert bound_data["flagged"] == ["gender", "age"]
        assert bound_data["accuracy"] == 0.847
    
    def test_risk_simulation_bindings(self):
        """Test risk simulation data bindings."""
        bindings = self.binder.create_risk_simulation_bindings()
        bound_data = self.binder.bind_data(self.sample_data, bindings)
        
        assert "probability" in bound_data
        assert "impact" in bound_data
        assert "financial_impact" in bound_data
        
        assert bound_data["probability"] == 0.287
        assert bound_data["impact"] == 0.156
        assert bound_data["financial_impact"] == 662500.0
    
    def test_compliance_dashboard_binding(self):
        """Test complete compliance dashboard data binding."""
        bound_data = self.binder.bind_compliance_dashboard_data(self.sample_data)
        
        # Should have data from all sources
        assert "value" in bound_data  # compliance score
        assert "probability" in bound_data  # risk probability
        assert "overall_health_score" in bound_data  # computed
        assert "compliance_distribution" in bound_data  # computed
        assert "risk_matrix_data" in bound_data  # computed
        
        # Test computed values
        assert isinstance(bound_data["overall_health_score"], float)
        assert "categories" in bound_data["compliance_distribution"]
        assert "values" in bound_data["compliance_distribution"]
    
    def test_binding_validation(self):
        """Test binding validation."""
        # Valid bindings
        valid_bindings = self.binder.create_compliance_bindings()
        is_valid, errors = self.binder.validate_bindings(valid_bindings)
        assert is_valid is True
        assert len(errors) == 0
        
        # Invalid binding (missing required fields)
        invalid_binding = DataBinding(
            binding_id="",  # Missing ID
            source_path="",  # Missing path
            chart_field="test",
            data_type="string"
        )
        
        is_valid, errors = self.binder.validate_bindings([invalid_binding])
        assert is_valid is False
        assert len(errors) > 0


class TestVisualizationGenerator:
    """Test visualization generator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = VisualizationGenerator()
        
        # Load sample data from Phase 5.1 fixtures
        sample_data_path = Path(__file__).parent.parent / "phase_5_1" / "fixtures" / "sample_data"
        
        with open(sample_data_path / "regulatory_intelligence_output.json") as f:
            regulatory_data = json.load(f)
        
        with open(sample_data_path / "bias_analysis_output.json") as f:
            bias_data = json.load(f)
        
        with open(sample_data_path / "risk_simulation_output.json") as f:
            risk_data = json.load(f)
        
        self.sample_data = {
            "regulatory_data": regulatory_data,
            "bias_analysis_data": bias_data,
            "risk_simulation_data": risk_data
        }
    
    def test_generator_initialization(self):
        """Test visualization generator initialization."""
        assert isinstance(self.generator, VisualizationGenerator)
        assert hasattr(self.generator, 'chart_engine')
        assert hasattr(self.generator, 'data_binder')
        assert len(self.generator.dashboard_templates) > 0
    
    def test_available_dashboards(self):
        """Test available dashboard templates."""
        dashboards = self.generator.get_available_dashboards()
        
        assert len(dashboards) > 0
        
        # Check for key dashboards
        dashboard_ids = [d["template_id"] for d in dashboards]
        assert "executive_dashboard" in dashboard_ids
        assert "technical_dashboard" in dashboard_ids
        assert "regulatory_dashboard" in dashboard_ids
        
        # Check dashboard structure
        for dashboard in dashboards:
            assert "template_id" in dashboard
            assert "name" in dashboard
            assert "description" in dashboard
            assert "chart_count" in dashboard
    
    def test_executive_dashboard_generation(self):
        """Test executive dashboard generation."""
        request = VisualizationRequest(
            request_id="test_exec_dashboard",
            visualization_type="dashboard",
            source_data=self.sample_data,
            config={"dashboard_type": "executive_dashboard"}
        )
        
        dashboard = self.generator.generate_visualization(request)
        
        assert "dashboard_id" in dashboard
        assert "name" in dashboard
        assert "charts" in dashboard
        assert "layout" in dashboard
        assert "metadata" in dashboard
        
        # Check charts were generated
        assert len(dashboard["charts"]) > 0
        
        # Check chart structure
        for chart in dashboard["charts"]:
            assert "type" in chart
            assert "title" in chart
            assert "data" in chart
            assert "position" in chart
    
    def test_technical_dashboard_generation(self):
        """Test technical dashboard generation."""
        request = VisualizationRequest(
            request_id="test_tech_dashboard",
            visualization_type="dashboard",
            source_data=self.sample_data,
            config={"dashboard_type": "technical_dashboard"}
        )
        
        dashboard = self.generator.generate_visualization(request)
        
        assert dashboard["name"] == "Technical Dashboard"
        assert len(dashboard["charts"]) > 0
        
        # Should have technical-specific charts
        chart_ids = [c.get("metadata", {}).get("chart_id", "") for c in dashboard["charts"]]
        # Note: chart_ids might be in metadata or other location, adjust as needed
    
    def test_single_chart_generation(self):
        """Test single chart generation."""
        request = VisualizationRequest(
            request_id="test_single_chart",
            visualization_type="single_chart",
            source_data=self.sample_data,
            config={
                "chart_type": "bar",
                "chart_id": "test_bar",
                "title": "Test Bar Chart",
                "data": {
                    "categories": ["A", "B", "C"],
                    "values": [10, 20, 15]
                }
            }
        )
        
        result = self.generator.generate_visualization(request)
        
        assert result["visualization_type"] == "single_chart"
        assert "chart" in result
        assert "metadata" in result
        
        chart = result["chart"]
        assert chart["type"] == "bar"
        assert chart["title"] == "Test Bar Chart"
    
    def test_report_charts_generation(self):
        """Test report charts generation."""
        request = VisualizationRequest(
            request_id="test_report_charts",
            visualization_type="report_charts",
            source_data=self.sample_data,
            config={}
        )
        
        result = self.generator.generate_visualization(request)
        
        assert result["visualization_type"] == "report_charts"
        assert "charts" in result
        assert "metadata" in result
        
        # Should generate standard report charts
        charts = result["charts"]
        assert len(charts) > 0
        
        # Check for key chart types
        chart_types = [c["type"] for c in charts]
        assert "gauge" in chart_types  # compliance gauge
    
    def test_request_validation(self):
        """Test visualization request validation."""
        # Valid request
        valid_request = VisualizationRequest(
            request_id="valid_request",
            visualization_type="dashboard",
            source_data=self.sample_data,
            config={"dashboard_type": "executive_dashboard"}
        )
        
        is_valid, errors = self.generator.validate_request(valid_request)
        assert is_valid is True
        assert len(errors) == 0
        
        # Invalid request (missing data)
        invalid_request = VisualizationRequest(
            request_id="",  # Missing ID
            visualization_type="invalid_type",  # Invalid type
            source_data={},  # Empty data
            config={}
        )
        
        is_valid, errors = self.generator.validate_request(invalid_request)
        assert is_valid is False
        assert len(errors) > 0
    
    def test_error_handling(self):
        """Test error handling in visualization generation."""
        # Request with invalid dashboard type
        request = VisualizationRequest(
            request_id="error_test",
            visualization_type="dashboard",
            source_data=self.sample_data,
            config={"dashboard_type": "nonexistent_dashboard"}
        )
        
        result = self.generator.generate_visualization(request)
        
        # Should return error response
        assert "error" in result
        assert result["error"] is True
        assert "message" in result


class TestIntegrationScenarios:
    """Test integration scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = VisualizationGenerator()
        
        # Create realistic test data
        self.test_data = {
            "regulatory_data": {
                "summary": {
                    "compliance_score": 0.78,
                    "total_regulations": 25
                },
                "compliance_status": {
                    "compliant_count": 19,
                    "non_compliant_count": 6
                }
            },
            "bias_analysis_data": {
                "bias_score": {
                    "overall_score": 0.734,
                    "flagged_attributes": ["gender", "age"]
                },
                "model_info": {
                    "performance_metrics": {
                        "accuracy": 0.847
                    }
                },
                "fairness_metrics": {
                    "demographic_parity": 0.156
                }
            },
            "risk_simulation_data": {
                "risk_metrics": {
                    "risk_probability": 0.287,
                    "expected_impact": 0.156
                }
            }
        }
    
    def test_end_to_end_dashboard_generation(self):
        """Test complete dashboard generation workflow."""
        request = VisualizationRequest(
            request_id="e2e_test",
            visualization_type="dashboard",
            source_data=self.test_data,
            config={"dashboard_type": "executive_dashboard"}
        )
        
        # Validate request
        is_valid, errors = self.generator.validate_request(request)
        assert is_valid is True
        
        # Generate dashboard
        dashboard = self.generator.generate_visualization(request)
        
        # Verify dashboard structure
        assert "dashboard_id" in dashboard
        assert "charts" in dashboard
        assert len(dashboard["charts"]) > 0
        
        # Verify each chart has required structure
        for chart in dashboard["charts"]:
            assert "type" in chart
            assert "data" in chart
            assert "config" in chart or "title" in chart
            assert "metadata" in chart
    
    def test_data_flow_integrity(self):
        """Test data flow from source to visualization."""
        # Test that source data flows correctly through the system
        request = VisualizationRequest(
            request_id="data_flow_test",
            visualization_type="single_chart",
            source_data=self.test_data,
            config={
                "chart_type": "gauge",
                "chart_id": "compliance_gauge",
                "title": "Compliance Score",
                "data": {"value": 0.78, "max_value": 1.0}
            }
        )
        
        result = self.generator.generate_visualization(request)
        chart = result["chart"]
        
        # Verify data integrity
        assert chart["data"]["value"] == 0.78
        assert chart["data"]["max_value"] == 1.0
        assert chart["title"] == "Compliance Score"


if __name__ == "__main__":
    pytest.main([__file__])
