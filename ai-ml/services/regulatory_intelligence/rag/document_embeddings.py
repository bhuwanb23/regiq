#!/usr/bin/env python3
"""
REGIQ AI/ML - Document Embeddings
Handles document embedding generation, storage, and similarity search for RAG system.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import numpy as np

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from services.regulatory_intelligence.rag.vector_database import (
    VectorDatabaseManager, VectorDBConfig, EmbeddingPipeline
)


@dataclass
class DocumentMetadata:
    """Metadata for a document in the vector database."""
    document_id: str
    title: str
    source: str
    document_type: str
    date: str
    content_length: int
    keywords: List[str]
    regulation_type: Optional[str] = None
    compliance_level: Optional[str] = None
    risk_level: Optional[str] = None


class DocumentEmbeddingService:
    """Service for managing document embeddings and similarity search."""
    
    def __init__(self, config: Optional[VectorDBConfig] = None):
        self.config = config or VectorDBConfig()
        self.logger = self._setup_logger()
        self.vector_db = VectorDatabaseManager(config)
        self.embedding_pipeline = EmbeddingPipeline(config)
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("document_embedding_service")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def process_document(self, document_id: str, content: str, metadata: DocumentMetadata) -> bool:
        """Process a single document and add it to the vector database."""
        try:
            # Prepare metadata for vector database
            db_metadata = {
                "document_id": metadata.document_id,
                "title": metadata.title,
                "source": metadata.source,
                "document_type": metadata.document_type,
                "date": metadata.date,
                "content_length": metadata.content_length,
                "keywords": json.dumps(metadata.keywords),
                "regulation_type": metadata.regulation_type or "",
                "compliance_level": metadata.compliance_level or "",
                "risk_level": metadata.risk_level or ""
            }
            
            # Add to vector database
            success = self.vector_db.add_documents(
                documents=[content],
                metadatas=[db_metadata],
                ids=[document_id]
            )
            
            if success:
                self.logger.info(f"Successfully processed document: {document_id}")
            else:
                self.logger.error(f"Failed to process document: {document_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error processing document {document_id}: {e}")
            return False
    
    def process_documents_batch(self, documents: List[Dict[str, Any]]) -> Dict[str, bool]:
        """Process multiple documents in batch."""
        results = {}
        
        for doc_data in documents:
            document_id = doc_data.get("document_id", "")
            content = doc_data.get("content", "")
            metadata = DocumentMetadata(**doc_data.get("metadata", {}))
            
            success = self.process_document(document_id, content, metadata)
            results[document_id] = success
        
        successful = sum(results.values())
        total = len(results)
        self.logger.info(f"Batch processing complete: {successful}/{total} documents successful")
        
        return results
    
    def search_similar_documents(self, query: str, n_results: int = None, 
                                filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for documents similar to the query."""
        n_results = n_results or self.config.default_top_k
        
        try:
            # Perform search
            search_results = self.vector_db.search_documents(query, n_results)
            
            # Format results
            similar_docs = []
            if search_results.get("documents") and search_results["documents"][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    search_results["documents"][0],
                    search_results["metadatas"][0],
                    search_results["distances"][0]
                )):
                    # Apply filters if provided
                    if filters and not self._apply_filters(metadata, filters):
                        continue
                    
                    similar_docs.append({
                        "document_id": metadata.get("document_id", ""),
                        "title": metadata.get("title", ""),
                        "source": metadata.get("source", ""),
                        "document_type": metadata.get("document_type", ""),
                        "date": metadata.get("date", ""),
                        "similarity_score": float(1 - distance),  # Convert distance to similarity
                        "content_preview": doc[:200] + "..." if len(doc) > 200 else doc,
                        "metadata": metadata
                    })
            
            self.logger.info(f"Found {len(similar_docs)} similar documents for query")
            return similar_docs
            
        except Exception as e:
            self.logger.error(f"Error searching similar documents: {e}")
            return []
    
    def _apply_filters(self, metadata: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Apply filters to metadata."""
        for key, value in filters.items():
            if key in metadata:
                if isinstance(value, list):
                    if metadata[key] not in value:
                        return False
                else:
                    if metadata[key] != value:
                        return False
        return True
    
    def get_document_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific document by ID."""
        try:
            # This would require additional implementation in the vector database
            # For now, return a placeholder
            self.logger.warning("get_document_by_id not fully implemented")
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving document {document_id}: {e}")
            return None
    
    def update_document(self, document_id: str, content: str, metadata: DocumentMetadata) -> bool:
        """Update an existing document."""
        try:
            # For now, we'll remove and re-add the document
            # This could be optimized in a production system
            self.logger.info(f"Updating document: {document_id}")
            return self.process_document(document_id, content, metadata)
        except Exception as e:
            self.logger.error(f"Error updating document {document_id}: {e}")
            return False
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from the vector database."""
        try:
            # This would require additional implementation in the vector database
            self.logger.warning("delete_document not fully implemented")
            return False
        except Exception as e:
            self.logger.error(f"Error deleting document {document_id}: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the document database."""
        try:
            stats = self.vector_db.get_stats()
            stats.update({
                "service": "DocumentEmbeddingService",
                "config": {
                    "embedding_model": self.config.embedding_model,
                    "embedding_dimension": self.config.embedding_dimension,
                    "default_top_k": self.config.default_top_k,
                    "similarity_threshold": self.config.similarity_threshold
                }
            })
            return stats
        except Exception as e:
            self.logger.error(f"Error getting database stats: {e}")
            return {}


class SimilaritySearchEngine:
    """Advanced similarity search with ranking and filtering."""
    
    def __init__(self, embedding_service: DocumentEmbeddingService):
        self.embedding_service = embedding_service
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("similarity_search_engine")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def search_with_ranking(self, query: str, n_results: int = 10, 
                           min_similarity: float = 0.7,
                           filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search with advanced ranking and filtering."""
        try:
            # Get initial results
            results = self.embedding_service.search_similar_documents(
                query, n_results * 2, filters  # Get more results for ranking
            )
            
            # Apply similarity threshold
            filtered_results = [
                r for r in results 
                if r.get("similarity_score", 0) >= min_similarity
            ]
            
            # Sort by similarity score
            ranked_results = sorted(
                filtered_results, 
                key=lambda x: x.get("similarity_score", 0), 
                reverse=True
            )
            
            # Return top results
            final_results = ranked_results[:n_results]
            
            self.logger.info(f"Ranked search returned {len(final_results)} results")
            return final_results
            
        except Exception as e:
            self.logger.error(f"Error in ranked search: {e}")
            return []
    
    def search_by_document_type(self, query: str, document_type: str, 
                               n_results: int = 5) -> List[Dict[str, Any]]:
        """Search within a specific document type."""
        filters = {"document_type": document_type}
        return self.search_with_ranking(query, n_results, filters=filters)
    
    def search_by_regulation_type(self, query: str, regulation_type: str, 
                                 n_results: int = 5) -> List[Dict[str, Any]]:
        """Search within a specific regulation type."""
        filters = {"regulation_type": regulation_type}
        return self.search_with_ranking(query, n_results, filters=filters)
    
    def search_by_risk_level(self, query: str, risk_level: str, 
                            n_results: int = 5) -> List[Dict[str, Any]]:
        """Search within a specific risk level."""
        filters = {"risk_level": risk_level}
        return self.search_with_ranking(query, n_results, filters=filters)


def main():
    """Test the document embedding service."""
    print("🧪 Testing Document Embedding Service")
    
    # Test configuration
    config = VectorDBConfig()
    service = DocumentEmbeddingService(config)
    
    # Test document processing
    test_metadata = DocumentMetadata(
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
    
    test_content = "The SEC requires enhanced disclosures for all public companies. These requirements include quarterly reporting, risk assessments, and compliance monitoring."
    
    print("✅ Test metadata created")
    print(f"✅ Test content: {test_content[:50]}...")
    
    # Test search engine
    search_engine = SimilaritySearchEngine(service)
    print("✅ Search engine initialized")
    
    # Get stats
    stats = service.get_database_stats()
    print(f"✅ Database stats: {stats}")


if __name__ == "__main__":
    main()
