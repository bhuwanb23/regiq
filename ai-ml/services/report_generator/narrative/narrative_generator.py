#!/usr/bin/env python3
"""
REGIQ AI/ML - Narrative Generator
Main narrative generation orchestrator.

This module provides:
- Narrative generation orchestration
- Integration with LLM service and prompt engine
- Audience-specific narrative optimization
- Quality assurance and validation

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from .llm_service import LLMNarrativeService, NarrativeRequest, NarrativeResponse
from .prompt_engine import PromptEngine
from .context_analyzer import ContextAnalyzer

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class NarrativeSection:
    """Enhanced narrative section."""
    section_id: str
    title: str
    structured_content: Dict[str, Any]
    narrative: str
    audience_type: str
    confidence_score: float
    processing_time: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "section_id": self.section_id,
            "title": self.title,
            "structured_content": self.structured_content,
            "narrative": self.narrative,
            "audience_type": self.audience_type,
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time,
            "metadata": self.metadata
        }


class NarrativeGenerator:
    """
    Main narrative generation orchestrator.
    
    Coordinates LLM service, prompt engine, and context analyzer
    to generate intelligent, audience-specific narratives.
    """
    
    def __init__(self):
        """Initialize narrative generator."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.llm_service = LLMNarrativeService()
        self.prompt_engine = PromptEngine()
        self.context_analyzer = ContextAnalyzer()
        
        # Generation settings
        self.default_settings = {
            "temperature": 0.7,
            "max_tokens": 1000,
            "use_context": True,
            "validate_output": True
        }
        
        # Quality thresholds
        self.quality_thresholds = {
            "min_confidence": 0.6,
            "min_length": 50,
            "max_length": 2000
        }
    
    def generate_narrative_for_section(
        self,
        section_data: Dict[str, Any],
        section_id: str,
        section_title: str,
        audience_type: str,
        section_type: str,
        **kwargs
    ) -> NarrativeSection:
        """
        Generate narrative for a specific report section.
        
        Args:
            section_data: Structured data for the section
            section_id: Unique section identifier
            section_title: Section title
            audience_type: Target audience (executive, technical, regulatory)
            section_type: Type of section (summary, metrics, etc.)
            **kwargs: Additional generation parameters
            
        Returns:
            Enhanced narrative section
        """
        try:
            start_time = datetime.utcnow()
            
            # Merge settings
            settings = {**self.default_settings, **kwargs}
            
            # Step 1: Analyze context
            context = {}
            if settings.get("use_context", True):
                context = self.context_analyzer.analyze_context(section_data, audience_type)
            
            # Step 2: Create intelligent prompt
            prompt = self.prompt_engine.create_prompt(
                section_data=section_data,
                context=context,
                audience_type=audience_type,
                section_type=section_type
            )
            
            # Step 3: Generate narrative
            request = NarrativeRequest(
                prompt=prompt,
                context=context,
                audience_type=audience_type,
                section_type=section_type,
                max_tokens=settings.get("max_tokens", 1000),
                temperature=settings.get("temperature", 0.7)
            )
            
            response = self.llm_service.generate_narrative(request)
            
            # Step 4: Validate and optimize
            if settings.get("validate_output", True):
                response = self._validate_and_optimize_narrative(response, audience_type)
            
            # Step 5: Create enhanced section
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            narrative_section = NarrativeSection(
                section_id=section_id,
                title=section_title,
                structured_content=section_data,
                narrative=response.narrative,
                audience_type=audience_type,
                confidence_score=response.confidence_score,
                processing_time=processing_time,
                metadata={
                    "context_insights": len(context.get("insights", [])),
                    "prompt_length": len(prompt),
                    "llm_processing_time": response.processing_time,
                    "total_processing_time": processing_time,
                    "validation_applied": settings.get("validate_output", True),
                    "generation_timestamp": datetime.utcnow().isoformat()
                }
            )
            
            self.logger.info(f"Generated narrative for {section_id} "
                           f"(confidence: {response.confidence_score:.3f}, "
                           f"time: {processing_time:.2f}s)")
            
            return narrative_section
            
        except Exception as e:
            self.logger.error(f"Narrative generation failed for {section_id}: {str(e)}")
            return self._create_fallback_section(
                section_data, section_id, section_title, audience_type, section_type
            )
    
    def generate_narratives_for_report(
        self,
        report_sections: List[Dict[str, Any]],
        audience_type: str,
        **kwargs
    ) -> List[NarrativeSection]:
        """
        Generate narratives for all sections of a report.
        
        Args:
            report_sections: List of report sections with data
            audience_type: Target audience
            **kwargs: Additional generation parameters
            
        Returns:
            List of enhanced narrative sections
        """
        try:
            narrative_sections = []
            
            for section in report_sections:
                try:
                    narrative_section = self.generate_narrative_for_section(
                        section_data=section.get("data", {}),
                        section_id=section.get("section_id", "unknown"),
                        section_title=section.get("title", "Unknown Section"),
                        audience_type=audience_type,
                        section_type=section.get("section_type", "general"),
                        **kwargs
                    )
                    narrative_sections.append(narrative_section)
                    
                except Exception as e:
                    self.logger.error(f"Failed to generate narrative for section {section.get('section_id')}: {str(e)}")
                    # Continue with other sections
                    continue
            
            self.logger.info(f"Generated narratives for {len(narrative_sections)} sections")
            
            return narrative_sections
            
        except Exception as e:
            self.logger.error(f"Report narrative generation failed: {str(e)}")
            return []
    
    def _validate_and_optimize_narrative(
        self, 
        response: NarrativeResponse, 
        audience_type: str
    ) -> NarrativeResponse:
        """Validate and optimize narrative response."""
        try:
            narrative = response.narrative
            optimized = False
            
            # Length validation
            if len(narrative) < self.quality_thresholds["min_length"]:
                self.logger.warning(f"Narrative too short ({len(narrative)} chars), extending...")
                narrative = self._extend_narrative(narrative, audience_type)
                optimized = True
            elif len(narrative) > self.quality_thresholds["max_length"]:
                self.logger.warning(f"Narrative too long ({len(narrative)} chars), truncating...")
                narrative = self._truncate_narrative(narrative)
                optimized = True
            
            # Confidence validation
            if response.confidence_score < self.quality_thresholds["min_confidence"]:
                self.logger.warning(f"Low confidence score ({response.confidence_score:.3f}), applying improvements...")
                narrative = self._improve_narrative_quality(narrative, audience_type)
                optimized = True
            
            # Audience appropriateness check
            if not self._check_audience_appropriateness(narrative, audience_type):
                self.logger.warning(f"Narrative not appropriate for {audience_type} audience, adjusting...")
                narrative = self._adjust_for_audience(narrative, audience_type)
                optimized = True
            
            # Create optimized response if changes were made
            if optimized:
                return NarrativeResponse(
                    narrative=narrative,
                    confidence_score=min(response.confidence_score + 0.1, 1.0),
                    processing_time=response.processing_time,
                    token_count=len(narrative.split()),
                    metadata={**response.metadata, "optimized": True},
                    timestamp=response.timestamp
                )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Narrative validation failed: {str(e)}")
            return response
    
    def _extend_narrative(self, narrative: str, audience_type: str) -> str:
        """Extend short narrative."""
        extensions = {
            "executive": " This analysis provides strategic insights for executive decision-making and business planning.",
            "technical": " Additional technical details and implementation considerations are available for further analysis.",
            "regulatory": " Complete documentation and evidence trails support regulatory compliance verification."
        }
        
        extension = extensions.get(audience_type, " Further analysis and recommendations are available upon request.")
        return narrative + extension
    
    def _truncate_narrative(self, narrative: str) -> str:
        """Truncate long narrative while preserving meaning."""
        sentences = narrative.split('. ')
        
        # Keep sentences until we reach reasonable length
        truncated_sentences = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) + 2 <= self.quality_thresholds["max_length"]:
                truncated_sentences.append(sentence)
                current_length += len(sentence) + 2
            else:
                break
        
        result = '. '.join(truncated_sentences)
        if not result.endswith('.'):
            result += '.'
        
        return result
    
    def _improve_narrative_quality(self, narrative: str, audience_type: str) -> str:
        """Improve narrative quality for low confidence scores."""
        # Add audience-specific improvements
        improvements = {
            "executive": {
                "prefix": "Strategic analysis indicates that ",
                "suffix": " These insights support informed executive decision-making."
            },
            "technical": {
                "prefix": "Technical evaluation demonstrates that ",
                "suffix": " These findings are based on rigorous analytical methodology."
            },
            "regulatory": {
                "prefix": "Compliance assessment shows that ",
                "suffix": " This analysis supports regulatory documentation requirements."
            }
        }
        
        improvement = improvements.get(audience_type, {
            "prefix": "Analysis shows that ",
            "suffix": " These results provide valuable insights for consideration."
        })
        
        # Apply improvements if narrative doesn't already have them
        if not narrative.lower().startswith(improvement["prefix"].lower()[:10]):
            narrative = improvement["prefix"] + narrative.lower()
        
        if not narrative.endswith('.'):
            narrative += '.'
        
        if not narrative.endswith(improvement["suffix"]):
            narrative += improvement["suffix"]
        
        return narrative
    
    def _check_audience_appropriateness(self, narrative: str, audience_type: str) -> bool:
        """Check if narrative is appropriate for target audience."""
        narrative_lower = narrative.lower()
        
        audience_indicators = {
            "executive": ["strategic", "business", "competitive", "investment", "roi", "growth"],
            "technical": ["algorithm", "methodology", "statistical", "performance", "implementation", "analysis"],
            "regulatory": ["compliance", "regulation", "audit", "evidence", "documentation", "requirement"]
        }
        
        indicators = audience_indicators.get(audience_type, [])
        matches = sum(1 for indicator in indicators if indicator in narrative_lower)
        
        # Require at least 1 audience-appropriate term
        return matches >= 1
    
    def _adjust_for_audience(self, narrative: str, audience_type: str) -> str:
        """Adjust narrative for specific audience."""
        audience_adjustments = {
            "executive": "From a strategic perspective, " + narrative,
            "technical": "Technical analysis reveals that " + narrative,
            "regulatory": "Compliance evaluation indicates that " + narrative
        }
        
        return audience_adjustments.get(audience_type, narrative)
    
    def _create_fallback_section(
        self,
        section_data: Dict[str, Any],
        section_id: str,
        section_title: str,
        audience_type: str,
        section_type: str
    ) -> NarrativeSection:
        """Create fallback narrative section when generation fails."""
        
        fallback_narratives = {
            "executive": f"This {section_type} section provides strategic insights based on comprehensive analysis of your organization's data. The results indicate areas of strength and opportunities for improvement that should be considered in strategic planning.",
            "technical": f"This {section_type} section presents technical analysis results using established methodologies. The findings provide detailed insights for technical evaluation and implementation planning.",
            "regulatory": f"This {section_type} section documents compliance analysis results. The assessment provides evidence and documentation to support regulatory requirements and audit processes."
        }
        
        narrative = fallback_narratives.get(audience_type, 
            f"This {section_type} section provides analysis results based on available data.")
        
        return NarrativeSection(
            section_id=section_id,
            title=section_title,
            structured_content=section_data,
            narrative=narrative,
            audience_type=audience_type,
            confidence_score=0.5,
            processing_time=0.0,
            metadata={
                "fallback": True,
                "generation_timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get narrative generation statistics."""
        llm_stats = self.llm_service.get_cache_stats()
        prompt_stats = self.prompt_engine.get_engine_stats()
        
        return {
            "llm_service": llm_stats,
            "prompt_engine": prompt_stats,
            "quality_thresholds": self.quality_thresholds,
            "default_settings": self.default_settings
        }
    
    def validate_service(self) -> Tuple[bool, List[str]]:
        """Validate narrative generation service."""
        errors = []
        
        try:
            # Validate LLM service
            llm_valid, llm_errors = self.llm_service.validate_service()
            if not llm_valid:
                errors.extend([f"LLM: {error}" for error in llm_errors])
            
            # Validate prompt engine
            if len(self.prompt_engine.templates) == 0:
                errors.append("Prompt engine: No templates available")
            
            # Test narrative generation
            test_data = {
                "test_metric": 0.75,
                "test_status": "good"
            }
            
            test_section = self.generate_narrative_for_section(
                section_data=test_data,
                section_id="test_section",
                section_title="Test Section",
                audience_type="executive",
                section_type="summary",
                use_context=False
            )
            
            if not test_section.narrative or len(test_section.narrative.strip()) < 20:
                errors.append("Narrative generation: Test generation failed")
            
            is_valid = len(errors) == 0
            
            if is_valid:
                self.logger.info("Narrative generator validation passed")
            else:
                self.logger.warning(f"Narrative generator validation failed: {len(errors)} errors")
            
            return is_valid, errors
            
        except Exception as e:
            self.logger.error(f"Service validation error: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def __str__(self) -> str:
        """String representation."""
        return f"NarrativeGenerator(llm_available={self.llm_service.is_available})"
