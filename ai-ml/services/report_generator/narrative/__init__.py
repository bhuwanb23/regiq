#!/usr/bin/env python3
"""
REGIQ AI/ML - Narrative Generation System
Phase 5.2: Intelligent narrative generation for reports using LLM integration.

This module provides:
- LLM-powered narrative generation
- Context-aware content creation
- Audience-specific language optimization
- Intelligent story structuring

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .llm_service import LLMNarrativeService
from .prompt_engine import PromptEngine
from .context_analyzer import ContextAnalyzer
from .narrative_generator import NarrativeGenerator

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    "LLMNarrativeService",
    "PromptEngine", 
    "ContextAnalyzer",
    "NarrativeGenerator"
]