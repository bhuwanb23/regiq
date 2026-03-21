#!/usr/bin/env python3
"""
REGIQ AI/ML - Regulatory Intelligence Service
Complete pipeline for regulatory document ingestion, NLP analysis,
RAG retrieval, Knowledge Graph management, and LLM summarization.

Pipeline:
    1. scrapers         → Ingest PDFs, SEC EDGAR, EU sources, regulatory APIs
    2. nlp              → SpaCy NER + sklearn classifier on document text
    3. llm              → Gemini 2.5 Flash summarization and Q&A
    4. rag              → ChromaDB/FAISS vector search + retrieval
    5. knowledge_graph  → Entity extraction, compliance mapping, graph queries
    6. utils            → Model persistence and registry

Quick Start — Populate RAG + Knowledge Graph:
    from services.regulatory_intelligence.rag.rag_data_seeder import RegulatoryDataSeeder
    seeder = RegulatoryDataSeeder()
    seeder.seed_all()

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

# ── NLP ───────────────────────────────────────────────────────────────── #
from .nlp import (
    TextPreprocessor,
    RegulatoryEntityRecognizer,
    RegulatoryTextClassifier,
)

# ── LLM ──────────────────────────────────────────────────────────────── #
from .llm import (
    GeminiClient,
    GeminiClientConfig,
    GeminiHelpers,
    RateLimiter,
    SummarizationService,
    QASystem,
)

# ── RAG ───────────────────────────────────────────────────────────────── #
from .rag import (
    VectorDatabaseManager,
    VectorDBConfig,
    EmbeddingPipeline,
    DocumentEmbeddingService,
    DocumentMetadata,
    RetrievalSystem,
    EmbeddingPersistence,
)

# ── Knowledge Graph ────────────────────────────────────────────────────── #
from .knowledge_graph import (
    EntityExtractor,
    RegulatoryEntity,
    EntityRelationship,
    KnowledgeGraphConfig,
    ComplianceMapper,
    ComplianceRequirement,
    CompliancePathway,
    RecommendationRule,
    GraphDatabaseManager,
    GraphQueryEngine,
)

# ── Scrapers ───────────────────────────────────────────────────────────── #
from .scrapers import (
    DocumentProcessingPipeline,
    PDFProcessor,
    PDFMetadata,
    ExtractedContent,
    SECEdgarScraper,
    SECFiling,
    ScrapingConfig,
    EURegulatoryScaper,
    EURegulatoryDocument,
    RegulatoryAPIConnector,
    APIConfig,
    RegulatoryAPIData,
)

# ── Utils ─────────────────────────────────────────────────────────────── #
from .utils import (
    ModelPersistence,
    ModelMetadata,
    ModelRegistry,
)

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    # NLP
    "TextPreprocessor", "RegulatoryEntityRecognizer", "RegulatoryTextClassifier",
    # LLM
    "GeminiClient", "GeminiClientConfig", "GeminiHelpers", "RateLimiter",
    "SummarizationService", "QASystem",
    # RAG
    "VectorDatabaseManager", "VectorDBConfig", "EmbeddingPipeline",
    "DocumentEmbeddingService", "DocumentMetadata",
    "RetrievalSystem", "EmbeddingPersistence",
    # Knowledge Graph
    "EntityExtractor", "RegulatoryEntity", "EntityRelationship", "KnowledgeGraphConfig",
    "ComplianceMapper", "ComplianceRequirement", "CompliancePathway", "RecommendationRule",
    "GraphDatabaseManager", "GraphQueryEngine",
    # Scrapers
    "DocumentProcessingPipeline", "PDFProcessor", "PDFMetadata", "ExtractedContent",
    "SECEdgarScraper", "SECFiling", "ScrapingConfig",
    "EURegulatoryScaper", "EURegulatoryDocument",
    "RegulatoryAPIConnector", "APIConfig", "RegulatoryAPIData",
    # Utils
    "ModelPersistence", "ModelMetadata", "ModelRegistry",
]
