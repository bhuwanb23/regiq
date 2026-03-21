#!/usr/bin/env python3
"""
REGIQ AI/ML - Regulatory Intelligence Service Tests
Comprehensive test suite for regulatory intelligence service.

Tests cover:
    - NLP module (NER, classification, preprocessing)
    - RAG module (vector DB, retrieval, embeddings)
    - LLM module (Gemini client, summarization, Q&A)
    - Knowledge Graph module (entity extraction, compliance mapping)
    - Scrapers module (PDF processing, SEC EDGAR, EU regulations)
    - Integration tests for complete pipeline

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .test_nlp import *
from .test_rag import *
from .test_llm import *
from .test_knowledge_graph import *
from .test_scrapers import *
from .test_integration import *
