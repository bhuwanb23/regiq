#!/usr/bin/env python3
"""
REGIQ AI/ML - LLM Module
Gemini 2.5 Flash integration for regulatory document analysis.

Provides:
    - GeminiClient: Core API wrapper with retry/backoff/rate-limiting
    - SummarizationService: Document summarization and key points
    - QASystem: Context-aware question answering

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .gemini_client import GeminiClient, GeminiClientConfig, GeminiHelpers, RateLimiter
from .summarization import SummarizationService
from .qa import QASystem

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    "GeminiClient",
    "GeminiClientConfig",
    "GeminiHelpers",
    "RateLimiter",
    "SummarizationService",
    "QASystem",
]
