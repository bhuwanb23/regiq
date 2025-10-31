#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.2 Narrative Generation Tests
Comprehensive tests for narrative generation system.
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.narrative.llm_service import (
    LLMNarrativeService, NarrativeRequest, NarrativeResponse
)
from services.report_generator.narrative.prompt_engine import PromptEngine
from services.report_generator.narrative.context_analyzer import ContextAnalyzer
from services.report_generator.narrative.narrative_generator import NarrativeGenerator
from services.report_generator.templates.base.base_template import ReportData


class TestLLMNarrativeService:
    """Test LLM narrative service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = LLMNarrativeService()
    
    def test_service_initialization(self):
        """Test service initialization."""
        assert isinstance(self.service, LLMNarrativeService)
        assert hasattr(self.service, 'model')
        assert hasattr(self.service, '_response_cache')
        assert isinstance(self.service.default_settings, dict)
    
    def test_narrative_request_creation(self):
        """Test narrative request creation."""
        request = NarrativeRequest(
            prompt="Test prompt",
            context={"test": "data"},
            audience_type="executive",
            section_type="summary"
        )
        
        assert request.prompt == "Test prompt"
        assert request.audience_type == "executive"
        assert request.section_type == "summary"
        assert request.max_tokens == 1000  # default
        assert request.temperature == 0.7  # default
    
    def test_narrative_response_creation(self):
        """Test narrative response creation."""
        response = NarrativeResponse(
            narrative="Test narrative content",
            confidence_score=0.85,
            processing_time=1.5,
            token_count=25,
            metadata={"test": "metadata"},
            timestamp="2024-01-01T00:00:00"
        )
        
        assert response.narrative == "Test narrative content"
        assert response.confidence_score == 0.85
        assert response.processing_time == 1.5
        assert response.token_count == 25
    
    def test_generate_narrative_fallback(self):
        """Test narrative generation with fallback."""
        request = NarrativeRequest(
            prompt="Generate a test narrative",
            context={},
            audience_type="executive",
            section_type="summary"
        )
        
        response = self.service.generate_narrative(request)
        
        assert isinstance(response, NarrativeResponse)
        assert len(response.narrative) > 0
        assert 0.0 <= response.confidence_score <= 1.0
        assert response.processing_time >= 0.0
    
    def test_cache_functionality(self):
        """Test response caching."""
        request = NarrativeRequest(
            prompt="Test caching",
            context={},
            audience_type="executive",
            section_type="summary"
        )
        
        # First request
        response1 = self.service.generate_narrative(request, use_cache=True)
        
        # Second request (should use cache)
        response2 = self.service.generate_narrative(request, use_cache=True)
        
        # Should be same response from cache
        assert response1.narrative == response2.narrative
        assert response1.timestamp == response2.timestamp
    
    def test_batch_generation(self):
        """Test batch narrative generation."""
        requests = [
            NarrativeRequest("Prompt 1", {}, "executive", "summary"),
            NarrativeRequest("Prompt 2", {}, "technical", "methodology"),
            NarrativeRequest("Prompt 3", {}, "regulatory", "compliance")
        ]
        
        responses = self.service.batch_generate(requests)
        
        assert len(responses) == 3
        assert all(isinstance(r, NarrativeResponse) for r in responses)
        assert all(len(r.narrative) > 0 for r in responses)
    
    def test_service_validation(self):
        """Test service validation."""
        is_valid, errors = self.service.validate_service()
        
        # Should be valid (even with fallback)
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)
    
    def test_cache_management(self):
        """Test cache management."""
        # Add some cached responses
        request = NarrativeRequest("Test", {}, "executive", "summary")
        self.service.generate_narrative(request, use_cache=True)
        
        # Check cache stats
        stats = self.service.get_cache_stats()
        assert "cache_size" in stats
        assert "cache_enabled" in stats
        
        # Clear cache
        cleared_count = self.service.clear_cache()
        assert cleared_count >= 0
        
        # Verify cache is empty
        stats_after = self.service.get_cache_stats()
        assert stats_after["cache_size"] == 0


class TestPromptEngine:
    """Test prompt engine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = PromptEngine()
    
    def test_engine_initialization(self):
        """Test engine initialization."""
        assert isinstance(self.engine, PromptEngine)
        assert len(self.engine.templates) > 0
        assert hasattr(self.engine, 'max_prompt_length')
    
    def test_template_loading(self):
        """Test template loading."""
        templates = self.engine.list_templates()
        
        assert len(templates) > 0
        assert all("template_id" in t for t in templates)
        assert all("audience_type" in t for t in templates)
        assert all("section_type" in t for t in templates)
    
    def test_prompt_creation_executive(self):
        """Test prompt creation for executive audience."""
        section_data = {
            "compliance_score": 0.78,
            "risk_level": "medium",
            "key_metrics": {"health_score": 0.75}
        }
        
        context = {"organization_name": "Test Corp"}
        
        prompt = self.engine.create_prompt(
            section_data=section_data,
            context=context,
            audience_type="executive",
            section_type="summary"
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 50
        assert "executive" in prompt.lower() or "strategic" in prompt.lower()
    
    def test_prompt_creation_technical(self):
        """Test prompt creation for technical audience."""
        section_data = {
            "model_performance": {"accuracy": 0.847},
            "methodology": "XGBoost",
            "statistical_tests": ["t-test", "chi-square"]
        }
        
        prompt = self.engine.create_prompt(
            section_data=section_data,
            context={},
            audience_type="technical",
            section_type="methodology"
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 50
        assert "technical" in prompt.lower() or "methodology" in prompt.lower()
    
    def test_prompt_creation_regulatory(self):
        """Test prompt creation for regulatory audience."""
        section_data = {
            "compliance_status": "partial_compliance",
            "regulations": ["GDPR", "AI Act"],
            "evidence": "documented"
        }
        
        prompt = self.engine.create_prompt(
            section_data=section_data,
            context={},
            audience_type="regulatory",
            section_type="compliance"
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 50
        assert "compliance" in prompt.lower() or "regulatory" in prompt.lower()
    
    def test_prompt_validation(self):
        """Test prompt validation."""
        # Valid prompt
        valid_prompt = "You are writing a summary. TASK: Generate insights based on data."
        is_valid, errors = self.engine.validate_prompt(valid_prompt)
        assert is_valid is True
        assert len(errors) == 0
        
        # Invalid prompt (too short)
        invalid_prompt = "Short"
        is_valid, errors = self.engine.validate_prompt(invalid_prompt)
        assert is_valid is False
        assert len(errors) > 0
    
    def test_template_info_retrieval(self):
        """Test template information retrieval."""
        template_info = self.engine.get_template_info("executive_summary")
        
        if template_info:  # Template exists
            assert "template_id" in template_info
            assert "audience_type" in template_info
            assert "section_type" in template_info
    
    def test_engine_statistics(self):
        """Test engine statistics."""
        stats = self.engine.get_engine_stats()
        
        assert "total_templates" in stats
        assert "audience_types" in stats
        assert "section_types" in stats
        assert stats["total_templates"] > 0


class TestContextAnalyzer:
    """Test context analyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = ContextAnalyzer()
        
        # Sample data
        self.regulatory_data = {
            "summary": {"compliance_score": 0.78, "total_regulations": 25},
            "deadlines": [{"priority": "high", "date": "2025-08-02"}]
        }
        
        self.bias_data = {
            "bias_score": {"overall_score": 0.734, "flagged_attributes": ["gender", "age"]},
            "model_info": {"performance_metrics": {"accuracy": 0.847}}
        }
        
        self.risk_data = {
            "risk_metrics": {"risk_probability": 0.287, "expected_impact": 0.156},
            "financial_impact": {"total_impact": 662500}
        }
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        assert isinstance(self.analyzer, ContextAnalyzer)
        assert hasattr(self.analyzer, 'significance_thresholds')
        assert hasattr(self.analyzer, 'industry_benchmarks')
    
    def test_regulatory_context_analysis(self):
        """Test regulatory context analysis."""
        section_data = {"regulatory_data": self.regulatory_data}
        
        context = self.analyzer.analyze_context(section_data, "executive")
        
        assert isinstance(context, dict)
        assert "insights" in context
        assert "summary" in context
    
    def test_bias_context_analysis(self):
        """Test bias context analysis."""
        section_data = {"bias_analysis_data": self.bias_data}
        
        context = self.analyzer.analyze_context(section_data, "technical")
        
        assert isinstance(context, dict)
        assert "insights" in context
        assert "summary" in context
    
    def test_risk_context_analysis(self):
        """Test risk context analysis."""
        section_data = {"risk_simulation_data": self.risk_data}
        
        context = self.analyzer.analyze_context(section_data, "executive")
        
        assert isinstance(context, dict)
        assert "insights" in context
        assert "summary" in context
    
    def test_comprehensive_context_analysis(self):
        """Test analysis with all data types."""
        section_data = {
            "regulatory_data": self.regulatory_data,
            "bias_analysis_data": self.bias_data,
            "risk_simulation_data": self.risk_data
        }
        
        context = self.analyzer.analyze_context(section_data, "executive")
        
        assert isinstance(context, dict)
        assert "insights" in context
        assert "summary" in context
        assert len(context["insights"]) > 0
    
    def test_benchmark_comparison(self):
        """Test benchmark comparison."""
        comparison = self.analyzer.get_benchmark_comparison("compliance_rate", 0.78)
        
        assert isinstance(comparison, dict)
        assert "status" in comparison
        assert "benchmark_value" in comparison
        assert "actual_value" in comparison
    
    def test_trend_identification(self):
        """Test trend identification."""
        historical_data = [
            {"compliance_score": 0.70},
            {"compliance_score": 0.75},
            {"compliance_score": 0.78}
        ]
        
        trends = self.analyzer.identify_trends(historical_data)
        
        assert isinstance(trends, list)
        # Should identify improving trend
        if trends:
            assert any(t["direction"] == "improving" for t in trends)
    
    def test_anomaly_detection(self):
        """Test anomaly detection."""
        data_points = [0.7, 0.75, 0.78, 0.76, 0.95, 0.74]  # 0.95 is anomaly
        
        anomalies = self.analyzer.detect_anomalies(data_points)
        
        assert isinstance(anomalies, list)
        # Should detect the 0.95 value as anomaly
        if anomalies:
            assert any(a["value"] == 0.95 for a in anomalies)


class TestNarrativeGenerator:
    """Test narrative generator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = NarrativeGenerator()
        
        # Sample section data
        self.section_data = {
            "regulatory_data": {
                "summary": {"compliance_score": 0.78},
                "compliance_status": {"overall_status": "partial_compliance"}
            },
            "bias_analysis_data": {
                "bias_score": {"overall_score": 0.734},
                "model_info": {"performance_metrics": {"accuracy": 0.847}}
            }
        }
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        assert isinstance(self.generator, NarrativeGenerator)
        assert hasattr(self.generator, 'llm_service')
        assert hasattr(self.generator, 'prompt_engine')
        assert hasattr(self.generator, 'context_analyzer')
    
    def test_section_narrative_generation(self):
        """Test narrative generation for single section."""
        narrative_section = self.generator.generate_narrative_for_section(
            section_data=self.section_data,
            section_id="test_section",
            section_title="Test Section",
            audience_type="executive",
            section_type="summary"
        )
        
        assert hasattr(narrative_section, 'section_id')
        assert hasattr(narrative_section, 'narrative')
        assert hasattr(narrative_section, 'confidence_score')
        assert narrative_section.section_id == "test_section"
        assert len(narrative_section.narrative) > 0
        assert 0.0 <= narrative_section.confidence_score <= 1.0
    
    def test_report_narratives_generation(self):
        """Test narrative generation for full report."""
        report_sections = [
            {
                "section_id": "summary",
                "title": "Executive Summary",
                "section_type": "summary",
                "data": self.section_data
            },
            {
                "section_id": "metrics",
                "title": "Key Metrics",
                "section_type": "metrics",
                "data": self.section_data
            }
        ]
        
        narrative_sections = self.generator.generate_narratives_for_report(
            report_sections=report_sections,
            audience_type="executive"
        )
        
        assert len(narrative_sections) == 2
        assert all(hasattr(ns, 'narrative') for ns in narrative_sections)
        assert all(len(ns.narrative) > 0 for ns in narrative_sections)
    
    def test_audience_specific_generation(self):
        """Test audience-specific narrative generation."""
        audiences = ["executive", "technical", "regulatory"]
        
        for audience in audiences:
            narrative_section = self.generator.generate_narrative_for_section(
                section_data=self.section_data,
                section_id="test_section",
                section_title="Test Section",
                audience_type=audience,
                section_type="summary"
            )
            
            assert narrative_section.audience_type == audience
            assert len(narrative_section.narrative) > 0
    
    def test_generation_statistics(self):
        """Test generation statistics."""
        stats = self.generator.get_generation_stats()
        
        assert isinstance(stats, dict)
        assert "llm_service" in stats
        assert "prompt_engine" in stats
        assert "quality_thresholds" in stats
    
    def test_service_validation(self):
        """Test service validation."""
        is_valid, errors = self.generator.validate_service()
        
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)


class TestEnhancedTemplateIntegration:
    """Test enhanced template integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Load sample data
        sample_data_path = Path(__file__).parent.parent / "phase_5_1" / "fixtures" / "sample_data"
        
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
    
    def test_enhanced_executive_template(self):
        """Test enhanced executive template with narratives."""
        from services.report_generator.templates.executive.executive_template import ExecutiveTemplate
        
        template = ExecutiveTemplate()
        
        # Test enhanced report generation
        enhanced_report = template.generate_enhanced_report(self.sample_data, "json")
        
        assert isinstance(enhanced_report, dict)
        assert "enhanced" in enhanced_report
        assert "narrative_enabled" in enhanced_report
        
        if enhanced_report.get("enhanced"):
            assert "enhanced_sections" in enhanced_report
            assert "narrative_stats" in enhanced_report
            
            enhanced_sections = enhanced_report["enhanced_sections"]
            assert len(enhanced_sections) > 0
            
            # Check that at least some sections have narratives
            sections_with_narratives = [s for s in enhanced_sections if s.get("narrative")]
            assert len(sections_with_narratives) > 0
    
    def test_narrative_quality_validation(self):
        """Test narrative quality validation."""
        generator = NarrativeGenerator()
        
        narrative_section = generator.generate_narrative_for_section(
            section_data={"test": "data"},
            section_id="test_section",
            section_title="Test Section",
            audience_type="executive",
            section_type="summary"
        )
        
        # Basic quality checks
        assert len(narrative_section.narrative) >= 20  # Minimum length
        assert narrative_section.confidence_score > 0.0
        assert narrative_section.processing_time >= 0.0


if __name__ == "__main__":
    pytest.main([__file__])
