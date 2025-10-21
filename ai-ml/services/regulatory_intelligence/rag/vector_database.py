#!/usr/bin/env python3
"""
REGIQ AI/ML - Vector Database Setup
Provides ChromaDB and FAISS integration for RAG system with embedding pipeline.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class VectorDBConfig:
    """Configuration for vector database operations."""
    # ChromaDB settings
    chroma_persist_directory: str = "data/vector_db/chroma"
    chroma_collection_name: str = "regulatory_documents"
    
    # FAISS settings
    faiss_index_path: str = "data/vector_db/faiss_index.bin"
    faiss_metadata_path: str = "data/vector_db/faiss_metadata.json"
    
    # Embedding settings
    embedding_model: str = "all-MiniLM-L6-v2"  # Fast, good quality
    embedding_dimension: int = 384
    batch_size: int = 32
    
    # Search settings
    default_top_k: int = 5
    similarity_threshold: float = 0.7


class EmbeddingPipeline:
    """Handles document embedding generation and management."""
    
    def __init__(self, config: Optional[VectorDBConfig] = None):
        self.config = config or VectorDBConfig()
        self.logger = self._setup_logger()
        self.model = self._load_embedding_model()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("embedding_pipeline")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def _load_embedding_model(self) -> Optional[SentenceTransformer]:
        """Load the sentence transformer model."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            self.logger.warning("sentence-transformers not available")
            return None
        
        try:
            model = SentenceTransformer(self.config.embedding_model)
            self.logger.info(f"Loaded embedding model: {self.config.embedding_model}")
            return model
        except Exception as e:
            self.logger.error(f"Failed to load embedding model: {e}")
            return None
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        if self.model is None:
            raise RuntimeError("Embedding model not loaded")
        
        if not texts:
            return np.array([])
        
        try:
            embeddings = self.model.encode(texts, batch_size=self.config.batch_size)
            self.logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            self.logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    def generate_single_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        return self.generate_embeddings([text])[0]


class ChromaDBManager:
    """Manages ChromaDB operations for document storage and retrieval."""
    
    def __init__(self, config: Optional[VectorDBConfig] = None):
        self.config = config or VectorDBConfig()
        self.logger = self._setup_logger()
        self.client = self._init_client()
        self.collection = self._get_collection()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("chromadb_manager")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def _init_client(self):
        """Initialize ChromaDB client."""
        if not CHROMADB_AVAILABLE:
            self.logger.warning("ChromaDB not available")
            return None
        
        try:
            # Create persist directory
            os.makedirs(self.config.chroma_persist_directory, exist_ok=True)
            
            client = chromadb.PersistentClient(
                path=self.config.chroma_persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            self.logger.info(f"ChromaDB client initialized at {self.config.chroma_persist_directory}")
            return client
        except Exception as e:
            self.logger.error(f"Failed to initialize ChromaDB client: {e}")
            return None
    
    def _get_collection(self):
        """Get or create the document collection."""
        if self.client is None:
            return None
        
        try:
            collection = self.client.get_or_create_collection(
                name=self.config.chroma_collection_name,
                metadata={"description": "Regulatory documents for RAG"}
            )
            self.logger.info(f"Collection '{self.config.chroma_collection_name}' ready")
            return collection
        except Exception as e:
            self.logger.error(f"Failed to get collection: {e}")
            return None
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> bool:
        """Add documents to the collection."""
        if self.collection is None:
            return False
        
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            self.logger.info(f"Added {len(documents)} documents to ChromaDB")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add documents: {e}")
            return False
    
    def search_documents(self, query: str, n_results: int = None) -> Dict[str, Any]:
        """Search for similar documents."""
        if self.collection is None:
            return {"documents": [], "metadatas": [], "distances": []}
        
        n_results = n_results or self.config.default_top_k
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            self.logger.info(f"Found {len(results['documents'][0])} similar documents")
            return results
        except Exception as e:
            self.logger.error(f"Failed to search documents: {e}")
            return {"documents": [], "metadatas": [], "distances": []}


class FAISSManager:
    """Manages FAISS index for fast similarity search."""
    
    def __init__(self, config: Optional[VectorDBConfig] = None):
        self.config = config or VectorDBConfig()
        self.logger = self._setup_logger()
        self.index = None
        self.metadata = []
        self._load_index()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("faiss_manager")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def _load_index(self):
        """Load existing FAISS index or create new one."""
        if not FAISS_AVAILABLE:
            self.logger.warning("FAISS not available")
            return
        
        try:
            if os.path.exists(self.config.faiss_index_path):
                self.index = faiss.read_index(self.config.faiss_index_path)
                self._load_metadata()
                self.logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
            else:
                # Create new index
                self.index = faiss.IndexFlatIP(self.config.embedding_dimension)  # Inner product for cosine similarity
                self.logger.info("Created new FAISS index")
        except Exception as e:
            self.logger.error(f"Failed to load FAISS index: {e}")
            self.index = None
    
    def _load_metadata(self):
        """Load metadata for the index."""
        try:
            if os.path.exists(self.config.faiss_metadata_path):
                with open(self.config.faiss_metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                self.logger.info(f"Loaded metadata for {len(self.metadata)} documents")
        except Exception as e:
            self.logger.error(f"Failed to load metadata: {e}")
            self.metadata = []
    
    def _save_index(self):
        """Save the FAISS index and metadata."""
        if self.index is None:
            return
        
        try:
            # Create directory
            os.makedirs(os.path.dirname(self.config.faiss_index_path), exist_ok=True)
            
            # Save index
            faiss.write_index(self.index, self.config.faiss_index_path)
            
            # Save metadata
            with open(self.config.faiss_metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            self.logger.info("Saved FAISS index and metadata")
        except Exception as e:
            self.logger.error(f"Failed to save FAISS index: {e}")
    
    def add_vectors(self, vectors: np.ndarray, metadatas: List[Dict[str, Any]]) -> bool:
        """Add vectors to the FAISS index."""
        if self.index is None:
            return False
        
        try:
            # Normalize vectors for cosine similarity
            faiss.normalize_L2(vectors)
            
            # Add to index
            self.index.add(vectors)
            
            # Add metadata
            self.metadata.extend(metadatas)
            
            # Save index
            self._save_index()
            
            self.logger.info(f"Added {len(vectors)} vectors to FAISS index")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add vectors to FAISS: {e}")
            return False
    
    def search_vectors(self, query_vector: np.ndarray, k: int = None) -> Tuple[np.ndarray, np.ndarray]:
        """Search for similar vectors."""
        if self.index is None:
            return np.array([]), np.array([])
        
        k = k or self.config.default_top_k
        
        try:
            # Normalize query vector
            query_vector = query_vector.reshape(1, -1)
            faiss.normalize_L2(query_vector)
            
            # Search
            distances, indices = self.index.search(query_vector, k)
            
            self.logger.info(f"Found {len(indices[0])} similar vectors")
            return distances[0], indices[0]
        except Exception as e:
            self.logger.error(f"Failed to search FAISS index: {e}")
            return np.array([]), np.array([])


class VectorDatabaseManager:
    """Unified interface for vector database operations."""
    
    def __init__(self, config: Optional[VectorDBConfig] = None):
        self.config = config or VectorDBConfig()
        self.logger = self._setup_logger()
        self.embedding_pipeline = EmbeddingPipeline(config)
        self.chromadb_manager = ChromaDBManager(config)
        self.faiss_manager = FAISSManager(config)
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("vector_db_manager")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> bool:
        """Add documents to both ChromaDB and FAISS."""
        if not documents:
            return False
        
        # Generate embeddings
        try:
            embeddings = self.embedding_pipeline.generate_embeddings(documents)
        except Exception as e:
            self.logger.error(f"Failed to generate embeddings: {e}")
            return False
        
        # Add to ChromaDB
        chroma_success = self.chromadb_manager.add_documents(documents, metadatas, ids)
        
        # Add to FAISS
        faiss_success = self.faiss_manager.add_vectors(embeddings, metadatas)
        
        success = chroma_success and faiss_success
        if success:
            self.logger.info(f"Successfully added {len(documents)} documents to vector databases")
        else:
            self.logger.warning("Partial failure in adding documents to vector databases")
        
        return success
    
    def search_documents(self, query: str, n_results: int = None, use_chromadb: bool = True) -> Dict[str, Any]:
        """Search for similar documents using ChromaDB or FAISS."""
        n_results = n_results or self.config.default_top_k
        
        if use_chromadb:
            return self.chromadb_manager.search_documents(query, n_results)
        else:
            # Use FAISS for search
            try:
                query_embedding = self.embedding_pipeline.generate_single_embedding(query)
                distances, indices = self.faiss_manager.search_vectors(query_embedding, n_results)
                
                # Get documents and metadata
                documents = []
                metadatas = []
                for idx in indices:
                    if idx < len(self.faiss_manager.metadata):
                        metadatas.append(self.faiss_manager.metadata[idx])
                        # Note: FAISS doesn't store documents, only vectors
                        documents.append("")  # Placeholder
                
                return {
                    "documents": [documents],
                    "metadatas": [metadatas],
                    "distances": [distances.tolist()]
                }
            except Exception as e:
                self.logger.error(f"Failed to search with FAISS: {e}")
                return {"documents": [], "metadatas": [], "distances": []}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector database."""
        stats = {
            "chromadb_available": CHROMADB_AVAILABLE,
            "faiss_available": FAISS_AVAILABLE,
            "sentence_transformers_available": SENTENCE_TRANSFORMERS_AVAILABLE,
            "embedding_model": self.config.embedding_model,
            "embedding_dimension": self.config.embedding_dimension,
        }
        
        if self.faiss_manager.index is not None:
            stats["faiss_total_vectors"] = self.faiss_manager.index.ntotal
        
        return stats


def main():
    """Test the vector database setup."""
    print("🧪 Testing Vector Database Setup")
    
    # Test configuration
    config = VectorDBConfig()
    print(f"✅ Config: {config.embedding_model}, dim={config.embedding_dimension}")
    
    # Test embedding pipeline
    pipeline = EmbeddingPipeline(config)
    if pipeline.model is not None:
        test_texts = ["SEC requires enhanced disclosures", "EU GDPR compliance deadline"]
        embeddings = pipeline.generate_embeddings(test_texts)
        print(f"✅ Generated embeddings shape: {embeddings.shape}")
    else:
        print("⚠️  Embedding model not available")
    
    # Test ChromaDB
    chroma = ChromaDBManager(config)
    if chroma.client is not None:
        print("✅ ChromaDB client initialized")
    else:
        print("⚠️  ChromaDB not available")
    
    # Test FAISS
    faiss_mgr = FAISSManager(config)
    if faiss_mgr.index is not None:
        print("✅ FAISS index ready")
    else:
        print("⚠️  FAISS not available")
    
    # Test unified manager
    vdb = VectorDatabaseManager(config)
    stats = vdb.get_stats()
    print(f"✅ Vector DB stats: {stats}")


if __name__ == "__main__":
    main()
