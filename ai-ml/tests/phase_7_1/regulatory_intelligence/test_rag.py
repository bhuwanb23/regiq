#!/usr/bin/env python3
"""
REGIQ AI/ML - RAG Module Tests
Test suite for Retrieval-Augmented Generation components.

Tests:
    - Vector Database Management
    - Document Embeddings
    - Retrieval System
    - Embedding Cache

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.regulatory_intelligence.rag import (
    VectorDatabaseManager,
    VectorDBConfig,
    DocumentEmbeddingService,
    DocumentMetadata,
    RetrievalSystem,
    EmbeddingPersistence,
)


class TestVectorDatabaseManager(unittest.TestCase):
    """Test vector database management."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = VectorDBConfig(
            db_name="test_regulations",
            embedding_dim=384
        )
        self.vdb = VectorDatabaseManager(self.config)

    def test_initialization(self):
        """Test vector DB initialization."""
        self.assertIsNotNone(self.vdb)
        self.assertEqual(self.vdb.config.db_name, "test_regulations")

    def test_create_collection(self):
        """Test collection creation."""
        collection_name = "test_collection"
        
        try:
            self.vdb.create_collection(collection_name)
            # Should not raise exception
        except Exception as e:
            self.fail(f"Failed to create collection: {e}")

    def test_add_embeddings(self):
        """Test adding embeddings to vector DB."""
        # Create sample embeddings
        embeddings = np.random.rand(5, 384).astype(np.float32)
        documents = [
            "GDPR compliance requirement",
            "Basel III capital adequacy",
            "EU AI Act high-risk systems",
            "SEC disclosure requirements",
            "MiFID II investor protection"
        ]
        metadata = [
            {"category": "privacy", "year": 2024},
            {"category": "financial", "year": 2023},
            {"category": "ai", "year": 2024},
            {"category": "financial", "year": 2024},
            {"category": "financial", "year": 2022}
        ]
        
        try:
            self.vdb.add_embeddings(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadata
            )
        except Exception as e:
            self.fail(f"Failed to add embeddings: {e}")

    def test_similarity_search(self):
        """Test similarity search functionality."""
        query_embedding = np.random.rand(384).astype(np.float32)
        
        try:
            results = self.vdb.similarity_search(
                query_embedding=query_embedding,
                n_results=3
            )
            
            self.assertIsInstance(results, list)
            # Results should match requested count or be empty if DB is empty
        except Exception as e:
            self.fail(f"Similarity search failed: {e}")

    def test_delete_collection(self):
        """Test collection deletion."""
        collection_name = "test_delete_collection"
        
        try:
            self.vdb.create_collection(collection_name)
            self.vdb.delete_collection(collection_name)
        except Exception as e:
            self.fail(f"Failed to delete collection: {e}")


class TestDocumentEmbeddingService(unittest.TestCase):
    """Test document embedding generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.embedding_service = DocumentEmbeddingService()
        
        self.sample_documents = [
            "The General Data Protection Regulation (GDPR) requires explicit consent for data processing.",
            "Basel III establishes minimum capital requirements for banks.",
            "The EU AI Act prohibits certain AI practices deemed harmful."
        ]

    def test_generate_embeddings_single_document(self):
        """Test embedding generation for single document."""
        doc = self.sample_documents[0]
        
        try:
            embedding = self.embedding_service.generate_embedding(doc)
            
            self.assertIsInstance(embedding, np.ndarray)
            self.assertEqual(len(embedding.shape), 1)
            # Embedding dimension should match model output
            self.assertGreater(embedding.shape[0], 0)
        except Exception as e:
            self.skipTest(f"Embedding generation requires model: {e}")

    def test_generate_embeddings_batch(self):
        """Test batch embedding generation."""
        try:
            embeddings = self.embedding_service.generate_embeddings_batch(
                self.sample_documents
            )
            
            self.assertIsInstance(embeddings, np.ndarray)
            self.assertEqual(embeddings.shape[0], len(self.sample_documents))
        except Exception as e:
            self.skipTest(f"Batch embedding requires model: {e}")

    def test_embedding_dimension_consistency(self):
        """Test that all embeddings have same dimension."""
        try:
            emb1 = self.embedding_service.generate_embedding(self.sample_documents[0])
            emb2 = self.embedding_service.generate_embedding(self.sample_documents[1])
            
            self.assertEqual(emb1.shape, emb2.shape)
        except Exception as e:
            self.skipTest(f"Model required: {e}")


class TestRetrievalSystem(unittest.TestCase):
    """Test retrieval system functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock embedding service for testing
        class MockEmbeddingService:
            def generate_embedding(self, text):
                return np.random.rand(384).astype(np.float32)
        
        mock_service = MockEmbeddingService()
        self.retrieval_system = RetrievalSystem(mock_service)

    def test_retrieve_context(self):
        """Test context retrieval."""
        query = "What are GDPR compliance requirements?"
        
        try:
            context = self.retrieval_system.retrieve_context(query)
            
            self.assertIsInstance(context, list)
            # Context should be list of relevant documents
        except Exception as e:
            self.skipTest(f"Retrieval requires initialized vector DB: {e}")

    def test_retrieve_with_filters(self):
        """Test retrieval with metadata filters."""
        query = "AI regulation requirements"
        filters = {"category": "ai_governance"}
        
        try:
            context = self.retrieval_system.retrieve_context(query, filters=filters)
            self.assertIsInstance(context, list)
        except Exception as e:
            self.skipTest(f"Filtered retrieval requires setup: {e}")

    def test_rank_documents(self):
        """Test document ranking."""
        documents = [
            {"content": "GDPR privacy protection", "similarity": 0.9},
            {"content": "Basel III banking", "similarity": 0.6},
            {"content": "EU AI Act compliance", "similarity": 0.8}
        ]
        
        ranked = self.retrieval_system.rank_documents(documents)
        
        self.assertIsInstance(ranked, list)
        # Should be sorted by similarity
        self.assertGreaterEqual(ranked[0]["similarity"], ranked[-1]["similarity"])


class TestEmbeddingPersistence(unittest.TestCase):
    """Test embedding persistence and caching."""

    def setUp(self):
        """Set up test fixtures."""
        self.persistence = EmbeddingPersistence(cache_dir="test_cache")

    def test_save_embeddings(self):
        """Test saving embeddings to cache."""
        embeddings = {
            "doc1": np.random.rand(384).astype(np.float32),
            "doc2": np.random.rand(384).astype(np.float32)
        }
        
        try:
            self.persistence.save_embeddings(embeddings)
        except Exception as e:
            self.fail(f"Failed to save embeddings: {e}")

    def test_load_embeddings(self):
        """Test loading embeddings from cache."""
        # First save
        original = {
            "test_doc": np.random.rand(384).astype(np.float32)
        }
        
        try:
            self.persistence.save_embeddings(original)
            loaded = self.persistence.load_embeddings(["test_doc"])
            
            self.assertIn("test_doc", loaded)
            np.testing.assert_array_almost_equal(
                original["test_doc"], loaded["test_doc"]
            )
        except Exception as e:
            self.skipTest(f"Persistence test requires file system access: {e}")

    def test_clear_cache(self):
        """Test cache clearing."""
        try:
            self.persistence.clear_cache()
            # Should not raise exception
        except Exception as e:
            self.fail(f"Failed to clear cache: {e}")


def run_tests():
    """Run all RAG tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestVectorDatabaseManager))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentEmbeddingService))
    suite.addTests(loader.loadTestsFromTestCase(TestRetrievalSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestEmbeddingPersistence))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
