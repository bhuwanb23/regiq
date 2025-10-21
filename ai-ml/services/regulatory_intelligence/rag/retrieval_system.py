#!/usr/bin/env python3
"""
REGIQ AI/ML - Retrieval System
Implements context retrieval, ranking algorithms, relevance filtering, and response generation for RAG.
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

from services.regulatory_intelligence.rag.document_embeddings import (
    DocumentEmbeddingService, SimilaritySearchEngine, DocumentMetadata
)
from services.regulatory_intelligence.llm.gemini_client import GeminiClient, GeminiClientConfig


@dataclass
class RetrievalConfig:
    """Configuration for the retrieval system."""
    max_context_length: int = 4000
    min_similarity_threshold: float = 0.7
    max_documents: int = 10
    rerank_top_k: int = 5
    use_hybrid_search: bool = True
    enable_query_expansion: bool = True


class ContextRetriever:
    """Retrieves relevant context for queries using multiple strategies."""
    
    def __init__(self, embedding_service: DocumentEmbeddingService, 
                 config: Optional[RetrievalConfig] = None):
        self.embedding_service = embedding_service
        self.config = config or RetrievalConfig()
        self.logger = self._setup_logger()
        self.search_engine = SimilaritySearchEngine(embedding_service)
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("context_retriever")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def retrieve_context(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query."""
        try:
            # Get similar documents
            similar_docs = self.search_engine.search_with_ranking(
                query=query,
                n_results=self.config.max_documents,
                min_similarity=self.config.min_similarity_threshold,
                filters=filters
            )
            
            # Apply relevance filtering
            relevant_docs = self._filter_relevant_documents(similar_docs, query)
            
            # Limit context length
            context_docs = self._limit_context_length(relevant_docs)
            
            self.logger.info(f"Retrieved {len(context_docs)} relevant documents")
            return context_docs
            
        except Exception as e:
            self.logger.error(f"Error retrieving context: {e}")
            return []
    
    def _filter_relevant_documents(self, documents: List[Dict[str, Any]], 
                                  query: str) -> List[Dict[str, Any]]:
        """Filter documents based on relevance to the query."""
        relevant_docs = []
        
        for doc in documents:
            # Check similarity threshold
            if doc.get("similarity_score", 0) < self.config.min_similarity_threshold:
                continue
            
            # Check content relevance (simple keyword matching)
            content = doc.get("content_preview", "").lower()
            query_terms = query.lower().split()
            
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(content, query_terms)
            
            if relevance_score > 0.1:  # Minimum relevance threshold
                doc["relevance_score"] = relevance_score
                relevant_docs.append(doc)
        
        # Sort by combined similarity and relevance
        relevant_docs.sort(
            key=lambda x: (x.get("similarity_score", 0) + x.get("relevance_score", 0)) / 2,
            reverse=True
        )
        
        return relevant_docs
    
    def _calculate_relevance_score(self, content: str, query_terms: List[str]) -> float:
        """Calculate relevance score based on keyword matching."""
        if not content or not query_terms:
            return 0.0
        
        matches = sum(1 for term in query_terms if term in content)
        return matches / len(query_terms)
    
    def _limit_context_length(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limit the total context length to avoid token limits."""
        context_docs = []
        total_length = 0
        
        for doc in documents:
            content_length = len(doc.get("content_preview", ""))
            
            if total_length + content_length <= self.config.max_context_length:
                context_docs.append(doc)
                total_length += content_length
            else:
                break
        
        return context_docs


class RankingAlgorithm:
    """Advanced ranking algorithms for document retrieval."""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("ranking_algorithm")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def rank_documents(self, documents: List[Dict[str, Any]], 
                      query: str, ranking_method: str = "hybrid") -> List[Dict[str, Any]]:
        """Rank documents using specified algorithm."""
        try:
            if ranking_method == "similarity":
                return self._rank_by_similarity(documents)
            elif ranking_method == "relevance":
                return self._rank_by_relevance(documents, query)
            elif ranking_method == "hybrid":
                return self._rank_hybrid(documents, query)
            else:
                self.logger.warning(f"Unknown ranking method: {ranking_method}")
                return documents
                
        except Exception as e:
            self.logger.error(f"Error ranking documents: {e}")
            return documents
    
    def _rank_by_similarity(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank documents by similarity score."""
        return sorted(documents, key=lambda x: x.get("similarity_score", 0), reverse=True)
    
    def _rank_by_relevance(self, documents: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Rank documents by relevance to query."""
        query_terms = query.lower().split()
        
        for doc in documents:
            content = doc.get("content_preview", "").lower()
            relevance = sum(1 for term in query_terms if term in content) / len(query_terms)
            doc["relevance_score"] = relevance
        
        return sorted(documents, key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    def _rank_hybrid(self, documents: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Hybrid ranking combining similarity and relevance."""
        query_terms = query.lower().split()
        
        for doc in documents:
            # Calculate relevance score
            content = doc.get("content_preview", "").lower()
            relevance = sum(1 for term in query_terms if term in content) / len(query_terms)
            
            # Combine similarity and relevance
            similarity = doc.get("similarity_score", 0)
            hybrid_score = (similarity * 0.7) + (relevance * 0.3)
            doc["hybrid_score"] = hybrid_score
        
        return sorted(documents, key=lambda x: x.get("hybrid_score", 0), reverse=True)


class RelevanceFilter:
    """Filters documents based on relevance criteria."""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("relevance_filter")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def filter_by_similarity(self, documents: List[Dict[str, Any]], 
                           threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Filter documents by similarity threshold."""
        return [doc for doc in documents if doc.get("similarity_score", 0) >= threshold]
    
    def filter_by_document_type(self, documents: List[Dict[str, Any]], 
                               document_types: List[str]) -> List[Dict[str, Any]]:
        """Filter documents by document type."""
        return [doc for doc in documents 
                if doc.get("metadata", {}).get("document_type", "") in document_types]
    
    def filter_by_date_range(self, documents: List[Dict[str, Any]], 
                           start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Filter documents by date range."""
        filtered_docs = []
        
        for doc in documents:
            doc_date = doc.get("metadata", {}).get("date", "")
            if start_date <= doc_date <= end_date:
                filtered_docs.append(doc)
        
        return filtered_docs
    
    def filter_by_risk_level(self, documents: List[Dict[str, Any]], 
                            risk_levels: List[str]) -> List[Dict[str, Any]]:
        """Filter documents by risk level."""
        return [doc for doc in documents 
                if doc.get("metadata", {}).get("risk_level", "") in risk_levels]


class ResponseGenerator:
    """Generates responses using retrieved context and LLM."""
    
    def __init__(self, gemini_client: Optional[GeminiClient] = None):
        self.gemini_client = gemini_client or GeminiClient(GeminiClientConfig())
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("response_generator")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def generate_response(self, query: str, context_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a response using retrieved context."""
        try:
            # Prepare context
            context_text = self._prepare_context(context_documents)
            
            # Generate response using Gemini
            prompt = self._create_prompt(query, context_text)
            response = self.gemini_client.generate_text(prompt)
            
            # Calculate confidence based on context quality
            confidence = self._calculate_confidence(context_documents)
            
            # Extract citations
            citations = self._extract_citations(context_documents)
            
            return {
                "response": response,
                "confidence": confidence,
                "citations": citations,
                "context_used": len(context_documents),
                "sources": [doc.get("title", "") for doc in context_documents]
            }
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return {
                "response": "I apologize, but I encountered an error generating a response.",
                "confidence": 0.0,
                "citations": [],
                "context_used": 0,
                "sources": []
            }
    
    def _prepare_context(self, documents: List[Dict[str, Any]]) -> str:
        """Prepare context from retrieved documents."""
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            title = doc.get("title", "Unknown")
            content = doc.get("content_preview", "")
            source = doc.get("source", "Unknown")
            
            context_parts.append(f"Document {i}: {title}\nSource: {source}\nContent: {content}\n")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create a prompt for the LLM."""
        return f"""You are a regulatory compliance assistant. Answer the following question using only the provided context.

Context:
{context}

Question: {query}

Instructions:
- Use only information from the provided context
- If the context doesn't contain enough information, say so
- Provide specific citations when possible
- Be concise but comprehensive
- Focus on regulatory compliance aspects

Answer:"""
    
    def _calculate_confidence(self, documents: List[Dict[str, Any]]) -> float:
        """Calculate confidence based on context quality."""
        if not documents:
            return 0.0
        
        # Average similarity score
        avg_similarity = sum(doc.get("similarity_score", 0) for doc in documents) / len(documents)
        
        # Number of documents (more context = higher confidence)
        doc_factor = min(len(documents) / 5, 1.0)  # Normalize to 0-1
        
        # Combine factors
        confidence = (avg_similarity * 0.7) + (doc_factor * 0.3)
        return min(confidence, 1.0)
    
    def _extract_citations(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Extract citations from context documents."""
        citations = []
        
        for doc in documents:
            title = doc.get("title", "")
            source = doc.get("source", "")
            if title and source:
                citations.append(f"{title} ({source})")
        
        return citations


class RAGSystem:
    """Complete RAG system integrating retrieval and generation."""
    
    def __init__(self, embedding_service: DocumentEmbeddingService,
                 config: Optional[RetrievalConfig] = None):
        self.embedding_service = embedding_service
        self.config = config or RetrievalConfig()
        self.logger = self._setup_logger()
        
        # Initialize components
        self.context_retriever = ContextRetriever(embedding_service, config)
        self.ranking_algorithm = RankingAlgorithm()
        self.relevance_filter = RelevanceFilter()
        self.response_generator = ResponseGenerator()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("rag_system")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def query(self, question: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a query through the complete RAG pipeline."""
        try:
            # Step 1: Retrieve context
            context_docs = self.context_retriever.retrieve_context(question, filters)
            
            if not context_docs:
                return {
                    "response": "I couldn't find relevant information to answer your question.",
                    "confidence": 0.0,
                    "citations": [],
                    "context_used": 0,
                    "sources": []
                }
            
            # Step 2: Rank documents
            ranked_docs = self.ranking_algorithm.rank_documents(
                context_docs, question, "hybrid"
            )
            
            # Step 3: Apply relevance filtering
            relevant_docs = self.relevance_filter.filter_by_similarity(
                ranked_docs, self.config.min_similarity_threshold
            )
            
            # Step 4: Generate response
            response = self.response_generator.generate_response(question, relevant_docs)
            
            self.logger.info(f"RAG query processed: {len(relevant_docs)} documents used")
            return response
            
        except Exception as e:
            self.logger.error(f"Error in RAG query: {e}")
            return {
                "response": "I encountered an error processing your question.",
                "confidence": 0.0,
                "citations": [],
                "context_used": 0,
                "sources": []
            }


def main():
    """Test the RAG system components."""
    print("🧪 Testing RAG System Components")
    
    # Test configuration
    from services.regulatory_intelligence.rag.vector_database import VectorDBConfig
    from services.regulatory_intelligence.rag.document_embeddings import DocumentEmbeddingService
    
    config = VectorDBConfig()
    embedding_service = DocumentEmbeddingService(config)
    
    # Test retrieval config
    retrieval_config = RetrievalConfig()
    print(f"✅ Retrieval config: max_context={retrieval_config.max_context_length}")
    
    # Test context retriever
    retriever = ContextRetriever(embedding_service, retrieval_config)
    print("✅ Context retriever initialized")
    
    # Test ranking algorithm
    ranker = RankingAlgorithm()
    print("✅ Ranking algorithm initialized")
    
    # Test relevance filter
    filter_obj = RelevanceFilter()
    print("✅ Relevance filter initialized")
    
    # Test response generator
    generator = ResponseGenerator()
    print("✅ Response generator initialized")
    
    # Test complete RAG system
    rag_system = RAGSystem(embedding_service, retrieval_config)
    print("✅ RAG system initialized")
    
    print("🎉 All RAG components ready!")


if __name__ == "__main__":
    main()
