#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.1 Base Template Tests
Unit tests for base template system components.
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.base.base_template import (
    BaseTemplate, ReportSection, ReportData, TemplateMetadata
)
from services.report_generator.templates.base.template_registry import (
    TemplateRegistry, register_template, get_template
)
from services.report_generator.templates.base.template_validator import (
    TemplateValidator, validate_template, ValidationResult
)


class MockTemplate(BaseTemplate):
    """Mock template for testing."""
    
    def get_description(self) -> str:
        return "Mock template for testing"
    
    def get_supported_formats(self) -> list:
        return ["html", "json"]
    
    def generate_sections(self, data: ReportData) -> list:
        return [
            ReportSection(
                section_id="test_section",
                title="Test Section",
                content="<p>Test content</p>",
                section_type="test",
                order=1
            )
        ]
    
    def validate_data(self, data: ReportData) -> tuple:
        return True, []


class TestReportData:
    """Test ReportData class."""
    
    def test_report_data_creation(self):
        """Test ReportData creation."""
        data = ReportData(
            regulatory_data={"test": "data"},
            bias_analysis_data={"bias": "data"},
            risk_simulation_data={"risk": "data"}
        )
        
        assert data.regulatory_data == {"test": "data"}
        assert data.bias_analysis_data == {"bias": "data"}
        assert data.risk_simulation_data == {"risk": "data"}
    
    def test_report_data_validation_success(self):
        """Test successful ReportData validation."""
        data = ReportData(regulatory_data={"test": "data"})
        is_valid, errors = data.validate()
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_report_data_validation_failure(self):
        """Test ReportData validation failure."""
        data = ReportData()  # No data sources
        is_valid, errors = data.validate()
        
        assert is_valid is False
        assert len(errors) > 0
        assert "At least one data source must be provided" in errors[0]
    
    def test_report_data_validation_invalid_types(self):
        """Test ReportData validation with invalid types."""
        data = ReportData(
            regulatory_data="invalid",  # Should be dict
            bias_analysis_data=123      # Should be dict
        )
        is_valid, errors = data.validate()
        
        assert is_valid is False
        assert len(errors) >= 2


class TestReportSection:
    """Test ReportSection class."""
    
    def test_report_section_creation(self):
        """Test ReportSection creation."""
        section = ReportSection(
            section_id="test_section",
            title="Test Section",
            content="<p>Test content</p>",
            section_type="test",
            order=1
        )
        
        assert section.section_id == "test_section"
        assert section.title == "Test Section"
        assert section.content == "<p>Test content</p>"
        assert section.section_type == "test"
        assert section.order == 1
    
    def test_report_section_to_dict(self):
        """Test ReportSection to_dict method."""
        section = ReportSection(
            section_id="test_section",
            title="Test Section", 
            content="<p>Test content</p>",
            section_type="test",
            order=1
        )
        
        section_dict = section.to_dict()
        
        assert isinstance(section_dict, dict)
        assert section_dict["section_id"] == "test_section"
        assert section_dict["title"] == "Test Section"


class TestBaseTemplate:
    """Test BaseTemplate abstract class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.template = MockTemplate("test_template", "Test Template")
        self.sample_data = ReportData(regulatory_data={"test": "data"})
    
    def test_template_initialization(self):
        """Test template initialization."""
        assert self.template.template_id == "test_template"
        assert self.template.template_name == "Test Template"
        assert self.template.version == "1.0.0"
        assert isinstance(self.template.metadata, TemplateMetadata)
    
    def test_template_metadata(self):
        """Test template metadata."""
        metadata = self.template.metadata
        
        assert metadata.template_id == "test_template"
        assert metadata.template_name == "Test Template"
        assert metadata.template_type == "MockTemplate"
        assert metadata.version == "1.0.0"
        assert "Mock template for testing" in metadata.description
    
    def test_add_section(self):
        """Test adding sections to template."""
        section = ReportSection(
            section_id="test_section",
            title="Test Section",
            content="<p>Test</p>",
            section_type="test",
            order=1
        )
        
        initial_count = len(self.template.sections)
        self.template.add_section(section)
        
        assert len(self.template.sections) == initial_count + 1
        assert self.template.sections[-1].section_id == "test_section"
    
    def test_remove_section(self):
        """Test removing sections from template."""
        section = ReportSection(
            section_id="test_section",
            title="Test Section",
            content="<p>Test</p>",
            section_type="test",
            order=1
        )
        
        self.template.add_section(section)
        initial_count = len(self.template.sections)
        
        removed = self.template.remove_section("test_section")
        
        assert removed is True
        assert len(self.template.sections) == initial_count - 1
    
    def test_remove_nonexistent_section(self):
        """Test removing non-existent section."""
        removed = self.template.remove_section("nonexistent")
        assert removed is False
    
    def test_get_section(self):
        """Test getting section by ID."""
        section = ReportSection(
            section_id="test_section",
            title="Test Section",
            content="<p>Test</p>",
            section_type="test",
            order=1
        )
        
        self.template.add_section(section)
        retrieved = self.template.get_section("test_section")
        
        assert retrieved is not None
        assert retrieved.section_id == "test_section"
    
    def test_get_nonexistent_section(self):
        """Test getting non-existent section."""
        retrieved = self.template.get_section("nonexistent")
        assert retrieved is None
    
    def test_reorder_sections(self):
        """Test section reordering."""
        section1 = ReportSection("s1", "Section 1", "<p>1</p>", "test", 3)
        section2 = ReportSection("s2", "Section 2", "<p>2</p>", "test", 1)
        section3 = ReportSection("s3", "Section 3", "<p>3</p>", "test", 2)
        
        self.template.add_section(section1)
        self.template.add_section(section2)
        self.template.add_section(section3)
        
        self.template.reorder_sections()
        
        assert self.template.sections[0].order == 1
        assert self.template.sections[1].order == 2
        assert self.template.sections[2].order == 3
    
    def test_generate_report_html(self):
        """Test HTML report generation."""
        report = self.template.generate_report(self.sample_data, "html")
        
        assert isinstance(report, dict)
        assert "template_metadata" in report
        assert "content" in report
        assert report["output_format"] == "html"
        assert "<!DOCTYPE html>" in report["content"]
    
    def test_generate_report_json(self):
        """Test JSON report generation."""
        report = self.template.generate_report(self.sample_data, "json")
        
        assert isinstance(report, dict)
        assert "template_metadata" in report
        assert "content" in report
        assert report["output_format"] == "json"
        assert isinstance(report["content"], dict)
    
    def test_generate_report_invalid_format(self):
        """Test report generation with invalid format."""
        with pytest.raises(ValueError, match="Unsupported output format"):
            self.template.generate_report(self.sample_data, "invalid")
    
    def test_save_report(self, tmp_path):
        """Test saving report to file."""
        output_file = tmp_path / "test_report.html"
        
        saved_path = self.template.save_report(
            self.sample_data,
            str(output_file),
            "html"
        )
        
        assert saved_path == str(output_file)
        assert output_file.exists()
        
        # Check file content
        content = output_file.read_text(encoding='utf-8')
        assert "<!DOCTYPE html>" in content
    
    def test_get_template_info(self):
        """Test getting template information."""
        info = self.template.get_template_info()
        
        assert isinstance(info, dict)
        assert "metadata" in info
        assert "sections_count" in info
        assert "current_sections" in info


class TestTemplateRegistry:
    """Test TemplateRegistry class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.registry = TemplateRegistry()
        self.registry.clear_registry()  # Start with clean registry
    
    def test_registry_singleton(self):
        """Test registry singleton pattern."""
        registry1 = TemplateRegistry()
        registry2 = TemplateRegistry()
        
        assert registry1 is registry2
    
    def test_register_template(self):
        """Test template registration."""
        success = self.registry.register_template(MockTemplate)
        
        assert success is True
        assert len(self.registry) > 0
    
    def test_register_duplicate_template(self):
        """Test registering duplicate template."""
        self.registry.register_template(MockTemplate, template_id="test_template")
        success = self.registry.register_template(MockTemplate, template_id="test_template")
        
        assert success is False
    
    def test_get_template(self):
        """Test getting template instance."""
        self.registry.register_template(MockTemplate, template_id="test_template")
        
        template = self.registry.get_template("test_template")
        
        assert template is not None
        assert isinstance(template, MockTemplate)
        assert template.template_id == "test_template"
    
    def test_get_nonexistent_template(self):
        """Test getting non-existent template."""
        template = self.registry.get_template("nonexistent")
        assert template is None
    
    def test_unregister_template(self):
        """Test template unregistration."""
        self.registry.register_template(MockTemplate, template_id="test_template")
        
        success = self.registry.unregister_template("test_template")
        assert success is True
        
        template = self.registry.get_template("test_template")
        assert template is None
    
    def test_list_templates(self):
        """Test listing templates."""
        self.registry.register_template(MockTemplate, template_id="test_template")
        
        templates = self.registry.list_templates()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert any(t["template_id"] == "test_template" for t in templates)
    
    def test_template_exists(self):
        """Test checking template existence."""
        self.registry.register_template(MockTemplate, template_id="test_template")
        
        assert self.registry.template_exists("test_template") is True
        assert self.registry.template_exists("nonexistent") is False
    
    def test_registry_validation(self):
        """Test registry validation."""
        self.registry.register_template(MockTemplate, template_id="test_template")
        
        is_valid, errors = self.registry.validate_registry()
        
        assert is_valid is True
        assert len(errors) == 0


class TestTemplateValidator:
    """Test TemplateValidator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = TemplateValidator()
        self.template = MockTemplate("test_template", "Test Template")
        self.sample_data = ReportData(regulatory_data={"test": "data"})
    
    def test_validator_initialization(self):
        """Test validator initialization."""
        assert len(self.validator.validation_rules) > 0
    
    def test_validate_template_success(self):
        """Test successful template validation."""
        result = self.validator.validate_template(self.template, self.sample_data)
        
        assert isinstance(result, ValidationResult)
        assert result.validation_type == "comprehensive"
    
    def test_validate_template_with_rule_types(self):
        """Test template validation with specific rule types."""
        result = self.validator.validate_template(
            self.template, 
            self.sample_data,
            rule_types=["structure"]
        )
        
        assert isinstance(result, ValidationResult)
        assert len(result.details) > 0
    
    def test_validate_output_format_html(self):
        """Test HTML output format validation."""
        html_output = "<!DOCTYPE html><html><head></head><body><h1>Test</h1></body></html>"
        
        result = self.validator.validate_output_format(html_output, "html")
        
        assert isinstance(result, ValidationResult)
        assert result.validation_type == "html_output"
    
    def test_validate_output_format_json(self):
        """Test JSON output format validation."""
        json_output = '{"test": "data", "valid": true}'
        
        result = self.validator.validate_output_format(json_output, "json")
        
        assert isinstance(result, ValidationResult)
        assert result.validation_type == "json_output"
    
    def test_validate_invalid_json(self):
        """Test validation of invalid JSON."""
        invalid_json = '{"test": "data", "invalid": true'  # Missing closing brace
        
        result = self.validator.validate_output_format(invalid_json, "json")
        
        assert result.is_valid is False
        assert len(result.errors) > 0
    
    def test_get_validation_rules(self):
        """Test getting validation rules."""
        rules = self.validator.get_validation_rules()
        
        assert isinstance(rules, list)
        assert len(rules) > 0
        assert all("rule_id" in rule for rule in rules)
    
    def test_get_validation_stats(self):
        """Test getting validation statistics."""
        stats = self.validator.get_validation_stats()
        
        assert isinstance(stats, dict)
        assert "total_rules" in stats
        assert "rule_types" in stats
        assert "severities" in stats


# Integration tests
class TestTemplateIntegration:
    """Test template system integration."""
    
    def test_end_to_end_template_workflow(self):
        """Test complete template workflow."""
        # Register template
        registry = TemplateRegistry()
        registry.clear_registry()
        
        success = register_template(MockTemplate, template_id="integration_test")
        assert success is True
        
        # Get template instance
        template = get_template("integration_test")
        assert template is not None
        
        # Validate template
        validator = TemplateValidator()
        sample_data = ReportData(regulatory_data={"test": "data"})
        
        validation_result = validate_template(template, sample_data)
        assert isinstance(validation_result, ValidationResult)
        
        # Generate report
        report = template.generate_report(sample_data, "html")
        assert isinstance(report, dict)
        assert "content" in report
        
        # Validate output
        output_validation = validator.validate_output_format(report["content"], "html")
        assert isinstance(output_validation, ValidationResult)


if __name__ == "__main__":
    pytest.main([__file__])
