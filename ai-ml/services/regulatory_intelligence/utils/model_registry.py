#!/usr/bin/env python3
"""
REGIQ AI/ML - Model Registry System

Provides comprehensive model versioning, metadata tracking, and lifecycle management.

Features:
- Model versioning with semantic versioning
- Performance metrics tracking
- Training data lineage
- Deployment status management
- Model comparison tools
- Automatic cleanup of deprecated versions
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import sqlite3
import threading

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))


@dataclass
class ModelVersion:
    """Represents a specific model version."""
    model_name: str
    version: str  # Semantic versioning: MAJOR.MINOR.PATCH
    created_at: datetime
    model_path: str
    model_type: str
    training_samples: int
    metrics: Dict[str, float]
    config: Dict[str, Any]
    description: str
    tags: List[str]
    parent_version: Optional[str] = None
    is_production: bool = False
    is_deprecated: bool = False


class ModelRegistry:
    """
    Central registry for all ML models with versioning support.
    
    Tracks model lineage, performance, and deployment status.
    """
    
    def __init__(self, registry_db: str = "models/registry.db"):
        """
        Initialize model registry.
        
        Args:
            registry_db: Path to SQLite registry database
        """
        self.registry_db = Path(registry_db)
        self.registry_db.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger = self._setup_logger()
        self.conn = None
        self.lock = threading.Lock()
        
        self._initialize_registry()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger."""
        logger = logging.getLogger("model_registry")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def _initialize_registry(self):
        """Initialize registry database schema."""
        try:
            self.conn = sqlite3.connect(str(self.registry_db), check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            cursor = self.conn.cursor()
            
            # Create models table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    model_path TEXT NOT NULL,
                    model_type TEXT NOT NULL,
                    training_samples INTEGER,
                    metrics TEXT,
                    config TEXT,
                    description TEXT,
                    tags TEXT,
                    parent_version TEXT,
                    is_production BOOLEAN DEFAULT FALSE,
                    is_deprecated BOOLEAN DEFAULT FALSE,
                    UNIQUE(model_name, version)
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_model_name 
                ON models(model_name)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_production 
                ON models(is_production)
            """)
            
            self.conn.commit()
            self.logger.info(f"✅ Model registry initialized at {self.registry_db}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize registry: {e}")
            raise
    
    def register_model(self,
                      model_name: str,
                      version: str,
                      model_path: str,
                      model_type: str,
                      training_samples: int,
                      metrics: Dict[str, Any],
                      config: Dict[str, Any],
                      description: str = "",
                      tags: List[str] = None,
                      parent_version: Optional[str] = None) -> int:
        """
        Register a new model version.
        
        Args:
            model_name: Name of the model
            version: Semantic version (e.g., "1.0.0")
            model_path: Path to model file
            model_type: Type of model (sklearn, pytorch, etc.)
            training_samples: Number of training samples
            metrics: Performance metrics
            config: Model configuration
            description: Model description
            tags: List of tags
            parent_version: Parent version for lineage tracking
            
        Returns:
            Model ID
        """
        try:
            with self.lock:
                cursor = self.conn.cursor()
                
                # Check if version already exists
                cursor.execute("""
                    SELECT id FROM models 
                    WHERE model_name = ? AND version = ?
                """, (model_name, version))
                
                if cursor.fetchone():
                    self.logger.warning(f"Model {model_name} v{version} already registered")
                    return None
                
                # Insert new record
                cursor.execute("""
                    INSERT INTO models (
                        model_name, version, model_path, model_type,
                        training_samples, metrics, config, description,
                        tags, parent_version
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    model_name,
                    version,
                    str(model_path),
                    model_type,
                    training_samples,
                    json.dumps(metrics),
                    json.dumps(config),
                    description,
                    json.dumps(tags or []),
                    parent_version
                ))
                
                self.conn.commit()
                
                model_id = cursor.lastrowid
                
                self.logger.info(
                    f"✅ Registered {model_name} v{version} (ID: {model_id})"
                )
                
                return model_id
                
        except Exception as e:
            self.logger.error(f"Failed to register model: {e}")
            self.conn.rollback()
            return None
    
    def get_model(self,
                 model_name: str,
                 version: Optional[str] = None) -> Optional[ModelVersion]:
        """
        Get model information.
        
        Args:
            model_name: Name of the model
            version: Specific version (latest if None)
            
        Returns:
            Model version info or None
        """
        try:
            cursor = self.conn.cursor()
            
            if version:
                cursor.execute("""
                    SELECT * FROM models 
                    WHERE model_name = ? AND version = ?
                """, (model_name, version))
            else:
                # Get latest non-deprecated version
                cursor.execute("""
                    SELECT * FROM models 
                    WHERE model_name = ? AND is_deprecated = FALSE
                    ORDER BY created_at DESC LIMIT 1
                """, (model_name,))
            
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            return ModelVersion(
                model_name=row["model_name"],
                version=row["version"],
                created_at=row["created_at"],
                model_path=row["model_path"],
                model_type=row["model_type"],
                training_samples=row["training_samples"],
                metrics=json.loads(row["metrics"]),
                config=json.loads(row["config"]),
                description=row["description"],
                tags=json.loads(row["tags"]),
                parent_version=row["parent_version"],
                is_production=bool(row["is_production"]),
                is_deprecated=bool(row["is_deprecated"])
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get model: {e}")
            return None
    
    def list_models(self,
                   model_type: Optional[str] = None,
                   include_deprecated: bool = False) -> List[Dict[str, Any]]:
        """
        List all registered models.
        
        Args:
            model_type: Filter by model type
            include_deprecated: Include deprecated models
            
        Returns:
            List of model summaries
        """
        try:
            cursor = self.conn.cursor()
            
            query = """
                SELECT DISTINCT model_name, model_type, 
                       MAX(created_at) as latest_version
                FROM models
                WHERE is_deprecated = FALSE
            """
            
            if model_type:
                query += f" AND model_type = '{model_type}'"
            
            query += " GROUP BY model_name ORDER BY latest_version DESC"
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            models = []
            for row in rows:
                # Get full details for latest version
                model = self.get_model(row["model_name"])
                if model:
                    models.append({
                        "name": model.model_name,
                        "type": model.model_type,
                        "version": model.version,
                        "created_at": model.created_at,
                        "is_production": model.is_production,
                        "metrics_summary": {
                            k: round(v, 4) if isinstance(v, float) else v
                            for k, v in model.metrics.items()
                        }
                    })
            
            return models
            
        except Exception as e:
            self.logger.error(f"Failed to list models: {e}")
            return []
    
    def set_production(self, model_name: str, version: str) -> bool:
        """
        Set a model version as production.
        
        Args:
            model_name: Name of the model
            version: Version to promote
            
        Returns:
            Success status
        """
        try:
            with self.lock:
                cursor = self.conn.cursor()
                
                # First, unset all production versions
                cursor.execute("""
                    UPDATE models SET is_production = FALSE
                    WHERE model_name = ?
                """, (model_name,))
                
                # Set new production version
                cursor.execute("""
                    UPDATE models SET is_production = TRUE
                    WHERE model_name = ? AND version = ?
                """, (model_name, version))
                
                self.conn.commit()
                
                self.logger.info(
                    f"✅ Set {model_name} v{version} as PRODUCTION"
                )
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to set production model: {e}")
            return False
    
    def deprecate_model(self, model_name: str, version: str) -> bool:
        """
        Deprecate a model version.
        
        Args:
            model_name: Name of the model
            version: Version to deprecate
            
        Returns:
            Success status
        """
        try:
            with self.lock:
                cursor = self.conn.cursor()
                
                cursor.execute("""
                    UPDATE models SET is_deprecated = TRUE
                    WHERE model_name = ? AND version = ?
                """, (model_name, version))
                
                self.conn.commit()
                
                self.logger.info(
                    f"⚠️  Deprecated {model_name} v{version}"
                )
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to deprecate model: {e}")
            return False
    
    def compare_versions(self,
                        model_name: str,
                        versions: List[str]) -> Dict[str, Any]:
        """
        Compare multiple versions of a model.
        
        Args:
            model_name: Name of the model
            versions: List of versions to compare
            
        Returns:
            Comparison results
        """
        comparisons = []
        
        for version in versions:
            model = self.get_model(model_name, version)
            if model:
                comparisons.append({
                    "version": model.version,
                    "created_at": model.created_at,
                    "metrics": model.metrics,
                    "training_samples": model.training_samples,
                    "is_production": model.is_production
                })
        
        # Sort by creation date
        comparisons.sort(key=lambda x: x["created_at"])
        
        return {
            "model_name": model_name,
            "versions_compared": len(comparisons),
            "comparison": comparisons
        }
    
    def get_lineage(self, model_name: str) -> List[Dict[str, Any]]:
        """
        Get model version lineage (version history).
        
        Args:
            model_name: Name of the model
            
        Returns:
            List of versions in chronological order
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT version, created_at, parent_version, 
                       is_production, is_deprecated,
                       json_extract(metrics, '$.accuracy') as accuracy
                FROM models
                WHERE model_name = ?
                ORDER BY created_at ASC
            """, (model_name,))
            
            rows = cursor.fetchall()
            
            lineage = []
            for row in rows:
                lineage.append({
                    "version": row["version"],
                    "created_at": row["created_at"],
                    "parent_version": row["parent_version"],
                    "is_production": bool(row["is_production"]),
                    "is_deprecated": bool(row["is_deprecated"]),
                    "accuracy": row["accuracy"]
                })
            
            return lineage
            
        except Exception as e:
            self.logger.error(f"Failed to get lineage: {e}")
            return []
    
    def delete_model(self, model_name: str, version: str) -> bool:
        """Delete a model registration."""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                
                cursor.execute("""
                    DELETE FROM models 
                    WHERE model_name = ? AND version = ?
                """, (model_name, version))
                
                self.conn.commit()
                
                self.logger.info(
                    f"🗑️  Deleted {model_name} v{version}"
                )
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to delete model: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        try:
            cursor = self.conn.cursor()
            
            # Total models
            cursor.execute("""
                SELECT COUNT(DISTINCT model_name) FROM models
                WHERE is_deprecated = FALSE
            """)
            total_models = cursor.fetchone()[0]
            
            # Total versions
            cursor.execute("""
                SELECT COUNT(*) FROM models
                WHERE is_deprecated = FALSE
            """)
            total_versions = cursor.fetchone()[0]
            
            # Production models
            cursor.execute("""
                SELECT COUNT(*) FROM models WHERE is_production = TRUE
            """)
            production_count = cursor.fetchone()[0]
            
            # Model types
            cursor.execute("""
                SELECT model_type, COUNT(*) as count
                FROM models
                WHERE is_deprecated = FALSE
                GROUP BY model_type
            """)
            types = {row["model_type"]: row["count"] for row in cursor.fetchall()}
            
            return {
                "total_models": total_models,
                "total_versions": total_versions,
                "production_models": production_count,
                "model_types": types
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {e}")
            return {}
    
    def close(self):
        """Close registry connection."""
        if self.conn:
            self.conn.close()


def main():
    """Test model registry."""
    print("=" * 60)
    print("Testing REGIQ Model Registry")
    print("=" * 60)
    
    # Initialize registry
    registry = ModelRegistry()
    
    # Test registration
    print("\n📝 Registering test models...")
    
    test_models = [
        {
            "model_name": "test_classifier",
            "version": "1.0.0",
            "model_path": "/path/to/model.pkl",
            "model_type": "sklearn",
            "training_samples": 1000,
            "metrics": {"accuracy": 0.92, "f1": 0.91},
            "config": {"type": "logistic_regression"},
            "description": "Test classifier v1"
        },
        {
            "model_name": "test_classifier",
            "version": "1.1.0",
            "model_path": "/path/to/model_v2.pkl",
            "model_type": "sklearn",
            "training_samples": 1500,
            "metrics": {"accuracy": 0.94, "f1": 0.93},
            "config": {"type": "random_forest"},
            "description": "Test classifier v2 with improvements",
            "parent_version": "1.0.0"
        }
    ]
    
    for model_data in test_models:
        model_id = registry.register_model(**model_data)
        print(f"  {'✓' if model_id else '✗'} Registered {model_data['model_name']} v{model_data['version']}")
    
    # Test listing
    print("\n📋 Listing models:")
    models = registry.list_models()
    for model in models:
        print(f"  - {model['name']} v{model['version']} ({model['type']})")
    
    # Test getting specific model
    print("\n🔍 Getting model details:")
    model = registry.get_model("test_classifier", "1.1.0")
    if model:
        print(f"  Name: {model.model_name}")
        print(f"  Version: {model.version}")
        print(f"  Metrics: {model.metrics}")
        print(f"  Training samples: {model.training_samples}")
    
    # Test setting production
    print("\n🏆 Setting production model:")
    success = registry.set_production("test_classifier", "1.1.0")
    print(f"  {'✓' if success else '✗'} Set v1.1.0 as production")
    
    # Test lineage
    print("\n🌳 Model lineage:")
    lineage = registry.get_lineage("test_classifier")
    for version in lineage:
        status = "🏆 PROD" if version["is_production"] else ""
        status += " ⚠️ DEP" if version["is_deprecated"] else ""
        print(f"  v{version['version']} ({version['created_at']}) {status}")
    
    # Test statistics
    print("\n📊 Registry statistics:")
    stats = registry.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ All tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
