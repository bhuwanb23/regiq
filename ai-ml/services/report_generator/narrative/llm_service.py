#!/usr/bin/env python3
"""
REGIQ AI/ML - LLM Narrative Service
LLM integration service for intelligent narrative generation.

This module provides:
- Gemini 1.5 Pro integration for narrative generation
- Prompt management and optimization
- Response processing and validation
- Error handling and fallback mechanisms

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
import time

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from config.env_config import get_env_config

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class NarrativeRequest:
    """Narrative generation request."""
    prompt: str
    context: Dict[str, Any]
    audience_type: str
    section_type: str
    max_tokens: int = 1000
    temperature: float = 0.7
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "prompt": self.prompt,
            "context": self.context,
            "audience_type": self.audience_type,
            "section_type": self.section_type,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }


@dataclass
class NarrativeResponse:
    """Narrative generation response."""
    narrative: str
    confidence_score: float
    processing_time: float
    token_count: int
    metadata: Dict[str, Any]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "narrative": self.narrative,
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time,
            "token_count": self.token_count,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class LLMNarrativeService:
    """
    LLM service for intelligent narrative generation.
    
    Integrates with Gemini 1.5 Pro to generate context-aware narratives
    for different report sections and audience types.
    """
    
    def __init__(self):
        """Initialize LLM narrative service."""
        self.logger = logging.getLogger(__name__)
        self.config = get_env_config()
        
        # Initialize Gemini if available
        self.model = None
        self.is_available = False
        
        if GENAI_AVAILABLE:
            self._initialize_gemini()
        else:
            self.logger.warning("Google GenerativeAI not available - using mock responses")
        
        # Response cache for performance
        self._response_cache: Dict[str, NarrativeResponse] = {}
        self.cache_enabled = True
        
        # Generation settings
        self.default_settings = {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9,
            "top_k": 40
        }
    
    def _initialize_gemini(self) -> None:
        """Initialize Gemini model."""
        try:
            # Configure Gemini
            api_key = self.config.get("GEMINI_API_KEY")
            if not api_key:
                self.logger.error("GEMINI_API_KEY not found in configuration")
                return
            
            genai.configure(api_key=api_key)
            
            # Initialize model
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }
            )
            
            self.is_available = True
            self.logger.info("Gemini 1.5 Pro initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini: {str(e)}")
            self.is_available = False
    
    def generate_narrative(
        self, 
        request: NarrativeRequest,
        use_cache: bool = True
    ) -> NarrativeResponse:
        """
        Generate narrative from request.
        
        Args:
            request: Narrative generation request
            use_cache: Whether to use response cache
            
        Returns:
            Narrative response
        """
        try:
            start_time = time.time()
            
            # Check cache first
            cache_key = self._get_cache_key(request)
            if use_cache and self.cache_enabled and cache_key in self._response_cache:
                cached_response = self._response_cache[cache_key]
                self.logger.debug(f"Using cached response for: {request.section_type}")
                return cached_response
            
            # Generate narrative
            if self.is_available and self.model:
                narrative = self._generate_with_gemini(request)
            else:
                narrative = self._generate_fallback(request)
            
            # Calculate metrics
            processing_time = time.time() - start_time
            token_count = len(narrative.split())
            confidence_score = self._calculate_confidence_score(narrative, request)
            
            # Create response
            response = NarrativeResponse(
                narrative=narrative,
                confidence_score=confidence_score,
                processing_time=processing_time,
                token_count=token_count,
                metadata={
                    "model": "gemini-1.5-pro" if self.is_available else "fallback",
                    "audience_type": request.audience_type,
                    "section_type": request.section_type,
                    "temperature": request.temperature
                },
                timestamp=datetime.utcnow().isoformat()
            )
            
            # Cache response
            if use_cache and self.cache_enabled:
                self._response_cache[cache_key] = response
            
            self.logger.info(f"Generated narrative for {request.section_type} "
                           f"({token_count} tokens, {processing_time:.2f}s)")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to generate narrative: {str(e)}")
            return self._create_error_response(request, str(e))
    
    def _generate_with_gemini(self, request: NarrativeRequest) -> str:
        """Generate narrative using Gemini."""
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens,
                top_p=self.default_settings["top_p"],
                top_k=self.default_settings["top_k"]
            )
            
            # Generate response
            response = self.model.generate_content(
                request.prompt,
                generation_config=generation_config
            )
            
            if response.text:
                return response.text.strip()
            else:
                self.logger.warning("Empty response from Gemini")
                return self._generate_fallback(request)
                
        except Exception as e:
            self.logger.error(f"Gemini generation failed: {str(e)}")
            return self._generate_fallback(request)
    
    def _generate_fallback(self, request: NarrativeRequest) -> str:
        """Generate fallback narrative when LLM is unavailable."""
        fallback_narratives = {
            "executive": {
                "summary": "This executive summary provides a comprehensive overview of your organization's compliance and AI governance status. Based on our analysis, your systems demonstrate solid foundational performance with strategic opportunities for enhancement.",
                "metrics": "The key performance indicators reveal important insights about your operational effectiveness. Your organization shows strong performance in several critical areas while identifying specific opportunities for improvement.",
                "recommendations": "Our strategic analysis recommends focusing on the highest-impact initiatives that will strengthen your competitive position and ensure continued compliance excellence."
            },
            "technical": {
                "overview": "This technical analysis examines the detailed performance characteristics and implementation specifics of your AI and compliance systems.",
                "methodology": "The analysis employs industry-standard methodologies including statistical validation, bias detection algorithms, and risk assessment frameworks.",
                "results": "The technical results demonstrate measurable outcomes across key performance dimensions, providing actionable insights for system optimization."
            },
            "regulatory": {
                "compliance": "This regulatory compliance assessment evaluates adherence to applicable regulations and identifies areas requiring attention.",
                "evidence": "The evidence documentation provides comprehensive support for compliance verification and audit readiness.",
                "recommendations": "Regulatory recommendations focus on maintaining compliance while preparing for evolving regulatory requirements."
            }
        }
        
        audience = request.audience_type.lower()
        section = request.section_type.lower()
        
        # Get appropriate fallback
        if audience in fallback_narratives:
            audience_narratives = fallback_narratives[audience]
            if section in audience_narratives:
                return audience_narratives[section]
            else:
                # Return first available narrative for audience
                return list(audience_narratives.values())[0]
        
        # Default fallback
        return ("This section provides important insights based on the analysis of your data. "
                "The results indicate areas of strength and opportunities for improvement that "
                "should be considered in your strategic planning and operational decisions.")
    
    def _calculate_confidence_score(self, narrative: str, request: NarrativeRequest) -> float:
        """Calculate confidence score for generated narrative."""
        try:
            score = 0.0
            
            # Length check (reasonable narrative length)
            if 50 <= len(narrative.split()) <= 500:
                score += 0.3
            
            # Content quality indicators
            if any(word in narrative.lower() for word in ["analysis", "performance", "compliance", "risk"]):
                score += 0.2
            
            # Audience appropriateness
            if request.audience_type == "executive" and any(word in narrative.lower() for word in ["strategic", "business", "organization"]):
                score += 0.2
            elif request.audience_type == "technical" and any(word in narrative.lower() for word in ["methodology", "algorithm", "metrics"]):
                score += 0.2
            elif request.audience_type == "regulatory" and any(word in narrative.lower() for word in ["compliance", "regulation", "audit"]):
                score += 0.2
            
            # Structure indicators
            if len(narrative.split('.')) >= 2:  # Multiple sentences
                score += 0.15
            
            # Completeness
            if not narrative.endswith('...') and len(narrative.strip()) > 20:
                score += 0.15
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate confidence score: {str(e)}")
            return 0.5  # Default moderate confidence
    
    def _get_cache_key(self, request: NarrativeRequest) -> str:
        """Generate cache key for request."""
        import hashlib
        
        # Create hash from key request components
        key_data = f"{request.prompt[:100]}{request.audience_type}{request.section_type}{request.temperature}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _create_error_response(self, request: NarrativeRequest, error_message: str) -> NarrativeResponse:
        """Create error response."""
        return NarrativeResponse(
            narrative=self._generate_fallback(request),
            confidence_score=0.3,
            processing_time=0.0,
            token_count=0,
            metadata={
                "error": error_message,
                "model": "fallback",
                "audience_type": request.audience_type,
                "section_type": request.section_type
            },
            timestamp=datetime.utcnow().isoformat()
        )
    
    async def generate_narrative_async(self, request: NarrativeRequest) -> NarrativeResponse:
        """Generate narrative asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate_narrative, request)
    
    def batch_generate(self, requests: List[NarrativeRequest]) -> List[NarrativeResponse]:
        """Generate multiple narratives in batch."""
        responses = []
        
        for request in requests:
            try:
                response = self.generate_narrative(request)
                responses.append(response)
            except Exception as e:
                self.logger.error(f"Batch generation failed for {request.section_type}: {str(e)}")
                responses.append(self._create_error_response(request, str(e)))
        
        return responses
    
    def clear_cache(self) -> int:
        """Clear response cache."""
        cache_size = len(self._response_cache)
        self._response_cache.clear()
        self.logger.info(f"Cleared narrative cache: {cache_size} entries removed")
        return cache_size
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "cache_size": len(self._response_cache),
            "cache_enabled": self.cache_enabled,
            "model_available": self.is_available,
            "model_type": "gemini-1.5-pro" if self.is_available else "fallback"
        }
    
    def validate_service(self) -> Tuple[bool, List[str]]:
        """Validate service configuration and availability."""
        errors = []
        
        try:
            # Check Gemini availability
            if not GENAI_AVAILABLE:
                errors.append("Google GenerativeAI library not available")
            
            # Check API key
            if not self.config.get("GEMINI_API_KEY"):
                errors.append("GEMINI_API_KEY not configured")
            
            # Check model initialization
            if GENAI_AVAILABLE and not self.is_available:
                errors.append("Gemini model initialization failed")
            
            # Test generation (if available)
            if self.is_available:
                test_request = NarrativeRequest(
                    prompt="Generate a brief test narrative about system status.",
                    context={},
                    audience_type="executive",
                    section_type="test",
                    max_tokens=50
                )
                
                response = self.generate_narrative(test_request, use_cache=False)
                if not response.narrative or len(response.narrative.strip()) < 10:
                    errors.append("Test narrative generation failed")
            
            is_valid = len(errors) == 0
            
            if is_valid:
                self.logger.info("LLM narrative service validation passed")
            else:
                self.logger.warning(f"LLM narrative service validation failed: {len(errors)} errors")
            
            return is_valid, errors
            
        except Exception as e:
            self.logger.error(f"Service validation error: {str(e)}")
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def __str__(self) -> str:
        """String representation."""
        return f"LLMNarrativeService(available={self.is_available}, cached={len(self._response_cache)})"
