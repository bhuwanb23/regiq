#!/usr/bin/env python3
"""
REGIQ AI/ML - RAG Embedding Cache & Persistence Layer

Provides persistent storage and caching for document embeddings to:
- Avoid re-computing embeddings for same documents
- Speed up RAG retrieval
- Support incremental updates
- Enable distributed deployment

Features:
- SQLite-based embedding storage
- LRU cache for hot embeddings
- Batch operations support
- Automatic cleanup of stale entries
"""

import os
import sys
import json
import logging
import hashlib
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import numpy as np
from collections import OrderedDict
import threading

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))


@dataclass
class EmbeddingRecord:
    """Represents a stored embedding."""
    document_id: str
    embedding: np.ndarray
    metadata: Dict[str, Any]
    created_at: datetime
    last_accessed: datetime
    access_count: int
    checksum: str


class EmbeddingCache:
    """
    LRU cache for frequently accessed embeddings.
    
    Keeps hot embeddings in memory for fast retrieval.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize cache.
        
        Args:
            max_size: Maximum number of embeddings to cache
        """
        self.max_size = max_size
        self.cache = OrderedDict()
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[np.ndarray]:
        """Get embedding from cache."""
        with self.lock:
            if key in self.cache:
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return self.cache[key]
            return None
    
    def put(self, key: str, value: np.ndarray):
        """Add embedding to cache."""
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            
            # Remove oldest if over capacity
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
    
    def clear(self):
        """Clear cache."""
        with self.lock:
            self.cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)


class EmbeddingPersistence:
    """
    Persistent storage for document embeddings using SQLite.
    """
    
    def __init__(self, db_path: str = "data/vector_db/embeddings.db"):
        """
        Initialize embedding database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger = self._setup_logger()
        self.conn = None
        self._initialize_database()
        
        # In-memory cache
        self.cache = EmbeddingCache(max_size=1000)
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger."""
        logger = logging.getLogger("embedding_persistence")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def _initialize_database(self):
        """Initialize SQLite database schema."""
        try:
            self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            cursor = self.conn.cursor()
            
            # Create embeddings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    document_id TEXT PRIMARY KEY,
                    embedding BLOB NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 0,
                    checksum TEXT NOT NULL
                )
            """)
            
            # Create indexes for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON embeddings(created_at)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_accessed 
                ON embeddings(last_accessed)
            """)
            
            self.conn.commit()
            self.logger.info(f"✅ Embedding database initialized at {self.db_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _calculate_checksum(self, embedding: np.ndarray) -> str:
        """Calculate checksum for embedding."""
        return hashlib.sha256(embedding.tobytes()).hexdigest()
    
    def save_embedding(self,
                      document_id: str,
                      embedding: np.ndarray,
                      metadata: Dict[str, Any]) -> bool:
        """
        Save embedding to database.
        
        Args:
            document_id: Unique document identifier
            embedding: Embedding vector
            metadata: Associated metadata
            
        Returns:
            Success status
        """
        try:
            checksum = self._calculate_checksum(embedding)
            
            # Check if already exists
            existing = self.get_embedding(document_id, include_embedding=False)
            if existing:
                self.logger.debug(f"Updating existing embedding for {document_id}")
                # Update existing record
                cursor = self.conn.cursor()
                cursor.execute("""
                    UPDATE embeddings 
                    SET embedding = ?, metadata = ?, checksum = ?
                    WHERE document_id = ?
                """, (
                    embedding.tobytes(),
                    json.dumps(metadata),
                    checksum,
                    document_id
                ))
            else:
                # Insert new record
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO embeddings 
                    (document_id, embedding, metadata, checksum)
                    VALUES (?, ?, ?, ?)
                """, (
                    document_id,
                    embedding.tobytes(),
                    json.dumps(metadata),
                    checksum
                ))
            
            self.conn.commit()
            
            # Update cache
            self.cache.put(document_id, embedding)
            
            self.logger.debug(f"Saved embedding for document: {document_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save embedding: {e}")
            self.conn.rollback()
            return False
    
    def get_embedding(self,
                     document_id: str,
                     include_embedding: bool = True) -> Optional[Dict[str, Any]]:
        """
        Retrieve embedding from database.
        
        Args:
            document_id: Document identifier
            include_embedding: Whether to return embedding vector
            
        Returns:
            Embedding record or None
        """
        try:
            # Check cache first
            cached = self.cache.get(document_id)
            if cached is not None:
                # Update access statistics
                self._update_access_stats(document_id)
                
                if include_embedding:
                    return {"document_id": document_id, "embedding": cached}
                return {"document_id": document_id}
            
            # Query database
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT document_id, embedding, metadata, 
                       created_at, last_accessed, access_count, checksum
                FROM embeddings
                WHERE document_id = ?
            """, (document_id,))
            
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            # Update access statistics
            self._update_access_stats(document_id)
            
            result = {
                "document_id": row["document_id"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                "created_at": row["created_at"],
                "last_accessed": row["last_accessed"],
                "access_count": row["access_count"] + 1,
                "checksum": row["checksum"]
            }
            
            if include_embedding:
                embedding = np.frombuffer(row["embedding"], dtype=np.float32)
                result["embedding"] = embedding
                
                # Add to cache
                self.cache.put(document_id, embedding)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve embedding: {e}")
            return None
    
    def _update_access_stats(self, document_id: str):
        """Update access statistics for a document."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE embeddings 
                SET last_accessed = CURRENT_TIMESTAMP,
                    access_count = access_count + 1
                WHERE document_id = ?
            """, (document_id,))
            self.conn.commit()
        except Exception as e:
            self.logger.warning(f"Failed to update access stats: {e}")
    
    def save_embeddings_batch(self,
                             embeddings_data: List[Dict[str, Any]]) -> Dict[str, bool]:
        """
        Save multiple embeddings in batch.
        
        Args:
            embeddings_data: List of {document_id, embedding, metadata} dicts
            
        Returns:
            Dictionary mapping document_id to success status
        """
        results = {}
        
        try:
            cursor = self.conn.cursor()
            
            for item in embeddings_data:
                document_id = item["document_id"]
                embedding = item["embedding"]
                metadata = item.get("metadata", {})
                checksum = self._calculate_checksum(embedding)
                
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO embeddings 
                        (document_id, embedding, metadata, checksum)
                        VALUES (?, ?, ?, ?)
                    """, (document_id, embedding.tobytes(), 
                          json.dumps(metadata), checksum))
                    
                    # Update cache
                    self.cache.put(document_id, embedding)
                    results[document_id] = True
                    
                except Exception as e:
                    self.logger.error(f"Failed to save {document_id}: {e}")
                    results[document_id] = False
            
            self.conn.commit()
            self.logger.info(f"Batch saved {sum(results.values())}/{len(results)} embeddings")
            
        except Exception as e:
            self.logger.error(f"Batch save failed: {e}")
            self.conn.rollback()
            return {doc["document_id"]: False for doc in embeddings_data}
        
        return results
    
    def delete_embedding(self, document_id: str) -> bool:
        """Delete an embedding."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM embeddings WHERE document_id = ?
            """, (document_id,))
            self.conn.commit()
            
            # Remove from cache
            self.cache.cache.pop(document_id, None)
            
            self.logger.info(f"Deleted embedding for {document_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete embedding: {e}")
            return False
    
    def list_embeddings(self,
                       limit: int = 100,
                       offset: int = 0) -> List[Dict[str, Any]]:
        """List all embeddings with pagination."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT document_id, created_at, last_accessed, 
                       access_count, length(embedding) as embedding_size
                FROM embeddings
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            rows = cursor.fetchall()
            return [
                {
                    "document_id": row["document_id"],
                    "created_at": row["created_at"],
                    "last_accessed": row["last_accessed"],
                    "access_count": row["access_count"],
                    "embedding_size": row["embedding_size"]
                }
                for row in rows
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to list embeddings: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            cursor = self.conn.cursor()
            
            # Total count
            cursor.execute("SELECT COUNT(*) FROM embeddings")
            total_count = cursor.fetchone()[0]
            
            # Total size
            cursor.execute("SELECT SUM(length(embedding)) FROM embeddings")
            total_size = cursor.fetchone()[0] or 0
            
            # Average access count
            cursor.execute("SELECT AVG(access_count) FROM embeddings")
            avg_access = cursor.fetchone()[0] or 0
            
            # Oldest and newest
            cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM embeddings")
            date_range = cursor.fetchone()
            
            return {
                "total_embeddings": total_count,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / 1024 / 1024, 2),
                "average_access_count": round(avg_access, 2),
                "cache_size": self.cache.size(),
                "oldest_embedding": date_range[0],
                "newest_embedding": date_range[1],
                "database_path": str(self.db_path)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {e}")
            return {}
    
    def cleanup_old_embeddings(self, days_old: int = 90) -> int:
        """Remove embeddings older than specified days."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM embeddings 
                WHERE created_at < ?
            """, (cutoff_date.isoformat(),))
            
            deleted_count = cursor.rowcount
            self.conn.commit()
            
            self.logger.info(f"Cleaned up {deleted_count} old embeddings")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return 0
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")


def main():
    """Test embedding persistence."""
    print("=" * 60)
    print("Testing RAG Embedding Persistence Layer")
    print("=" * 60)
    
    # Initialize
    persister = EmbeddingPersistence()
    
    # Test saving embeddings
    print("\n💾 Testing save operations...")
    
    test_embeddings = []
    for i in range(10):
        doc_id = f"test_doc_{i}"
        embedding = np.random.rand(384).astype(np.float32)
        metadata = {
            "title": f"Test Document {i}",
            "source": "test_suite",
            "type": "regulatory"
        }
        
        success = persister.save_embedding(doc_id, embedding, metadata)
        test_embeddings.append({"document_id": doc_id, "success": success})
        print(f"  {'✓' if success else '✗'} Saved {doc_id}")
    
    # Test retrieval
    print("\n📖 Testing retrieval...")
    for i in range(3):
        doc_id = f"test_doc_{i}"
        result = persister.get_embedding(doc_id)
        if result:
            print(f"  ✓ Retrieved {doc_id} (size: {result['embedding'].shape})")
        else:
            print(f"  ✗ Failed to retrieve {doc_id}")
    
    # Test cache
    print(f"\n🔍 Cache statistics:")
    print(f"  Cache size: {persister.cache.size()} embeddings")
    
    # Test database statistics
    print("\n📊 Database statistics:")
    stats = persister.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test listing
    print("\n📋 Recent embeddings:")
    embeddings = persister.list_embeddings(limit=5)
    for emb in embeddings:
        print(f"  - {emb['document_id']} (accessed: {emb['access_count']} times)")
    
    print("\n✅ All tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
