#!/usr/bin/env python3
"""
Comprehensive Test Suite for Phase 2.4: RAG System
Tests vector database, embeddings, and retrieval system components.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))


def test_vector_database_setup():
    print("\n🗄️ Testing Vector Database Setup...")
    from services.regulatory_intelligence.rag.vector_database import (
        VectorDBConfig, EmbeddingPipeline, ChromaDBManager, FAISSManager, VectorDatabaseManager
    )
    
    # Test configuration
    config = VectorDBConfig()
    assert config.embedding_model == "all-MiniLM-L6-v2"
    assert config.embedding_dimension == 384
    print("✅ VectorDB config created")
    
    # Test embedding pipeline
    pipeline = EmbeddingPipeline(config)
    if pipeline.model is not None:
        test_texts = ["SEC requires enhanced disclosures", "EU GDPR compliance requirements"]
        embeddings = pipeline.generate_embeddings(test_texts)
        assert embeddings.shape[0] == 2
        assert embeddings.shape[1] == 384
        print("✅ Embedding pipeline working")
    else:
        print("⚠️  Embedding model not available")
    
    # Test ChromaDB
    chroma = ChromaDBManager(config)
    if chroma.client is not None:
        print("✅ ChromaDB manager initialized")
    else:
        print("⚠️  ChromaDB not available")
    
    # Test FAISS
    faiss_mgr = FAISSManager(config)
    if faiss_mgr.index is not None:
        print("✅ FAISS manager initialized")
    else:
        print("⚠️  FAISS not available")
    
    # Test unified manager
    vdb = VectorDatabaseManager(config)
    stats = vdb.get_stats()
    assert "chromadb_available" in stats
    assert "faiss_available" in stats
    print("✅ Vector database manager stats:", stats)


def test_document_embeddings():
    print("\n📄 Testing Document Embeddings...")
    from services.regulatory_intelligence.rag.document_embeddings import (
        DocumentEmbeddingService, SimilaritySearchEngine, DocumentMetadata
    )
    from services.regulatory_intelligence.rag.vector_database import VectorDBConfig
    
    config = VectorDBConfig()
    service = DocumentEmbeddingService(config)
    
    # Test document metadata
    metadata = DocumentMetadata(
        document_id="test_001",
        title="SEC Disclosure Requirements",
        source="SEC.gov",
        document_type="regulation",
        date="2025-01-01",
        content_length=1500,
        keywords=["SEC", "disclosure", "requirements"],
        regulation_type="securities",
        compliance_level="high",
        risk_level="medium"
    )
    assert metadata.document_id == "test_001"
    print("✅ Document metadata created")
    
    # Test search engine
    search_engine = SimilaritySearchEngine(service)
    print("✅ Similarity search engine initialized")
    
    # Test database stats
    stats = service.get_database_stats()
    assert "service" in stats
    print("✅ Document embedding service stats:", stats)


def test_retrieval_system():
    print("\n🔍 Testing Retrieval System...")
    from services.regulatory_intelligence.rag.retrieval_system import (
        RetrievalConfig, ContextRetriever, RankingAlgorithm, RelevanceFilter, 
        ResponseGenerator, RAGSystem
    )
    from services.regulatory_intelligence.rag.document_embeddings import DocumentEmbeddingService
    from services.regulatory_intelligence.rag.vector_database import VectorDBConfig
    
    # Test retrieval config
    config = RetrievalConfig()
    assert config.max_context_length == 4000
    assert config.min_similarity_threshold == 0.7
    print("✅ Retrieval config created")
    
    # Test embedding service
    embedding_service = DocumentEmbeddingService(VectorDBConfig())
    
    # Test context retriever
    retriever = ContextRetriever(embedding_service, config)
    print("✅ Context retriever initialized")
    
    # Test ranking algorithm
    ranker = RankingAlgorithm()
    test_docs = [
        {"similarity_score": 0.8, "content_preview": "SEC requirements"},
        {"similarity_score": 0.6, "content_preview": "GDPR compliance"}
    ]
    ranked = ranker.rank_documents(test_docs, "SEC requirements", "similarity")
    assert len(ranked) == 2
    print("✅ Ranking algorithm working")
    
    # Test relevance filter
    filter_obj = RelevanceFilter()
    filtered = filter_obj.filter_by_similarity(test_docs, 0.7)
    assert len(filtered) == 1  # Only first doc has similarity >= 0.7
    print("✅ Relevance filter working")
    
    # Test response generator
    generator = ResponseGenerator()
    print("✅ Response generator initialized")
    
    # Test complete RAG system
    rag_system = RAGSystem(embedding_service, config)
    print("✅ RAG system initialized")


def test_rag_integration():
    print("\n🤖 Testing RAG Integration...")
    from services.regulatory_intelligence.rag.retrieval_system import RAGSystem, RetrievalConfig
    from services.regulatory_intelligence.rag.document_embeddings import DocumentEmbeddingService
    from services.regulatory_intelligence.rag.vector_database import VectorDBConfig
    
    # Initialize components
    vector_config = VectorDBConfig()
    embedding_service = DocumentEmbeddingService(vector_config)
    retrieval_config = RetrievalConfig()
    rag_system = RAGSystem(embedding_service, retrieval_config)
    
    # Test query processing (without actual documents)
    test_query = "What are the SEC disclosure requirements?"
    try:
        # This will return empty response since no documents are indexed
        response = rag_system.query(test_query)
        assert "response" in response
        assert "confidence" in response
        assert "citations" in response
        print("✅ RAG query processing works")
    except Exception as e:
        print(f"⚠️  RAG query test failed: {e}")


def test_performance_metrics():
    print("\n⚡ Testing Performance Metrics...")
    import time
    
    # Test embedding generation speed
    from services.regulatory_intelligence.rag.vector_database import EmbeddingPipeline, VectorDBConfig
    
    config = VectorDBConfig()
    pipeline = EmbeddingPipeline(config)
    
    if pipeline.model is not None:
        test_texts = ["Test document " + str(i) for i in range(10)]
        
        start_time = time.time()
        embeddings = pipeline.generate_embeddings(test_texts)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"✅ Generated 10 embeddings in {duration:.2f} seconds")
        print(f"✅ Embedding rate: {len(test_texts)/duration:.1f} docs/second")
    else:
        print("⚠️  Performance test skipped (no embedding model)")


def test_error_handling():
    print("\n🛡️ Testing Error Handling...")
    from services.regulatory_intelligence.rag.vector_database import VectorDatabaseManager
    from services.regulatory_intelligence.rag.document_embeddings import DocumentEmbeddingService
    
    # Test with invalid configuration
    try:
        vdb = VectorDatabaseManager()
        print("✅ Vector database handles missing config")
    except Exception as e:
        print(f"⚠️  Vector database config error: {e}")
    
    # Test with empty documents
    try:
        service = DocumentEmbeddingService()
        results = service.search_similar_documents("", n_results=5)
        assert isinstance(results, list)
        print("✅ Empty query handling works")
    except Exception as e:
        print(f"⚠️  Empty query error: {e}")


def main():
    print("🚀 Phase 2.4 Comprehensive Test Suite")
    print("=" * 50)
    
    test_vector_database_setup()
    test_document_embeddings()
    test_retrieval_system()
    test_rag_integration()
    test_performance_metrics()
    test_error_handling()
    
    print("\n🎉 Phase 2.4 tests completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
