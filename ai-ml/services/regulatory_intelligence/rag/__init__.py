"""
REGIQ AI/ML - RAG (Retrieval-Augmented Generation) Module

Provides document embedding, storage, and retrieval:
- Vector database management (ChromaDB, FAISS)
- Document embeddings
- Retrieval system
- Embedding cache for performance
"""

from .vector_database import VectorDatabaseManager, VectorDBConfig, EmbeddingPipeline
from .document_embeddings import DocumentEmbeddingService, DocumentMetadata
from .retrieval_system import ContextRetriever, RAGSystem
from .embedding_cache import EmbeddingPersistence

__all__ = [
    'VectorDatabaseManager',
    'VectorDBConfig',
    'EmbeddingPipeline',
    'DocumentEmbeddingService',
    'DocumentMetadata',
    'ContextRetriever',
    'RAGSystem',
    'EmbeddingPersistence',
]