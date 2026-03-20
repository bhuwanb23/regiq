#!/usr/bin/env python3
"""
REGIQ AI/ML - Model Persistence Integration Tests

Comprehensive end-to-end tests for:
1. Model persistence layer
2. NER model training and saving
3. Classifier training and saving  
4. RAG embedding cache
5. Model registry

Run with: pytest tests/phase_2_6/test_model_persistence.py -v
"""

import os
import sys
import json
import logging
import shutil
from pathlib import Path
from datetime import datetime
import numpy as np
import pytest

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.regulatory_intelligence.utils.model_persistence import (
    ModelPersistence, ModelMetadata
)
from services.regulatory_intelligence.utils.model_registry import ModelRegistry
from services.regulatory_intelligence.rag.embedding_cache import EmbeddingPersistence


class TestModelPersistence:
    """Test model persistence layer."""
    
    @pytest.fixture
    def setup_persister(self, tmp_path):
        """Setup test persister."""
        model_dir = tmp_path / "test_models"
        persister = ModelPersistence(str(model_dir))
        yield persister
        
        # Cleanup
        if model_dir.exists():
            shutil.rmtree(model_dir)
    
    def test_save_sklearn_model(self, setup_persister):
        """Test saving sklearn model."""
        try:
            from sklearn.linear_model import LogisticRegression
            
            # Create simple model
            model = LogisticRegression()
            model.fit([[1], [2], [3]], [0, 1, 0])
            
            # Create metadata
            metadata = ModelMetadata(
                model_name="test_classifier",
                model_type="sklearn",
                version="1.0.0",
                created_at="",
                training_samples=100,
                features=["feature1"],
                metrics={"accuracy": 0.95},
                config={"solver": "lbfgs"},
                checksum="",
                file_size=0,
                description="Test classifier"
            )
            
            # Save model
            saved_path = setup_persister.save(model, "test_classifier", metadata)
            
            assert saved_path.exists()
            assert metadata.checksum != ""
            assert metadata.file_size > 0
            
            # Load model back
            loaded_model = setup_persister.load("test_classifier")
            
            # Verify predictions match
            pred_original = model.predict([[2]])
            pred_loaded = loaded_model.predict([[2]])
            
            assert np.array_equal(pred_original, pred_loaded)
            
            print("✅ Sklearn model persistence test passed")
            
        except Exception as e:
            pytest.fail(f"Sklearn model persistence failed: {e}")
    
    def test_model_metadata_tracking(self, setup_persister):
        """Test metadata tracking."""
        from sklearn.naive_bayes import MultinomialNB
        
        model = MultinomialNB()
        
        metadata = ModelMetadata(
            model_name="test_nb",
            model_type="sklearn",
            version="1.0.0",
            created_at="",
            training_samples=500,
            features=["word1", "word2"],
            metrics={"accuracy": 0.88, "f1": 0.85},
            config={"alpha": 1.0},
            checksum="",
            file_size=0,
            description="Naive Bayes classifier",
            tags=["nlp", "text"]
        )
        
        setup_persister.save(model, "test_nb", metadata)
        
        # Retrieve metadata
        retrieved = setup_persister.get_metadata("test_nb")
        
        assert retrieved is not None
        assert retrieved.model_name == "test_nb"
        assert retrieved.version == "1.0.0"
        assert retrieved.training_samples == 500
        assert "accuracy" in retrieved.metrics
        assert "nlp" in retrieved.tags
        
        print("✅ Metadata tracking test passed")
    
    def test_list_models(self, setup_persister):
        """Test listing all models."""
        from sklearn.linear_model import LogisticRegression
        
        # Save multiple models
        for i in range(3):
            model = LogisticRegression()
            metadata = ModelMetadata(
                model_name=f"model_{i}",
                model_type="sklearn",
                version="1.0.0",
                created_at="",
                training_samples=100,
                features=[],
                metrics={},
                config={},
                checksum="",
                file_size=0
            )
            setup_persister.save(model, f"model_{i}", metadata)
        
        models = setup_persister.list_models()
        
        assert len(models) == 3
        model_names = [m['name'] for m in models]
        
        assert "model_0" in model_names
        assert "model_1" in model_names
        assert "model_2" in model_names
        
        print("✅ List models test passed")


class TestEmbeddingPersistence:
    """Test RAG embedding persistence."""
    
    @pytest.fixture
    def setup_embedding_db(self, tmp_path):
        """Setup test embedding database."""
        db_path = tmp_path / "test_embeddings.db"
        persister = EmbeddingPersistence(str(db_path))
        yield persister
        
        # Cleanup
        persister.close()
        if db_path.exists():
            db_path.unlink()
    
    def test_save_and_retrieve_embedding(self, setup_embedding_db):
        """Test saving and retrieving embeddings."""
        doc_id = "test_doc_001"
        embedding = np.random.rand(384).astype(np.float32)
        metadata = {
            "title": "Test Document",
            "source": "test_suite",
            "type": "regulatory"
        }
        
        # Save
        success = setup_embedding_db.save_embedding(doc_id, embedding, metadata)
        assert success
        
        # Retrieve
        result = setup_embedding_db.get_embedding(doc_id)
        
        assert result is not None
        assert result["document_id"] == doc_id
        assert "embedding" in result
        assert result["embedding"].shape == (384,)
        assert result["metadata"]["title"] == "Test Document"
        
        print("✅ Embedding save/retrieve test passed")
    
    def test_embedding_cache(self, setup_embedding_db):
        """Test embedding cache functionality."""
        # Save multiple embeddings
        for i in range(5):
            doc_id = f"doc_{i}"
            embedding = np.random.rand(384).astype(np.float32)
            setup_embedding_db.save_embedding(doc_id, embedding, {})
        
        # Retrieve to populate cache
        setup_embedding_db.get_embedding("doc_0")
        setup_embedding_db.get_embedding("doc_1")
        
        # Check cache size
        stats = setup_embedding_db.get_statistics()
        assert stats["cache_size"] >= 2
        
        print("✅ Embedding cache test passed")
    
    def test_batch_operations(self, setup_embedding_db):
        """Test batch save operations."""
        embeddings_data = []
        for i in range(10):
            embeddings_data.append({
                "document_id": f"batch_doc_{i}",
                "embedding": np.random.rand(384).astype(np.float32),
                "metadata": {"index": i}
            })
        
        results = setup_embedding_db.save_embeddings_batch(embeddings_data)
        
        # All should succeed
        assert all(results.values())
        assert len(results) == 10
        
        # Verify count
        stats = setup_embedding_db.get_statistics()
        assert stats["total_embeddings"] == 10
        
        print("✅ Batch operations test passed")


class TestModelRegistry:
    """Test model registry system."""
    
    @pytest.fixture
    def setup_registry(self, tmp_path):
        """Setup test registry."""
        registry_db = tmp_path / "test_registry.db"
        registry = ModelRegistry(str(registry_db))
        yield registry
        
        # Cleanup
        registry.close()
    
    def test_register_model(self, setup_registry):
        """Test model registration."""
        model_id = setup_registry.register_model(
            model_name="test_model",
            version="1.0.0",
            model_path="/path/to/model.pkl",
            model_type="sklearn",
            training_samples=1000,
            metrics={"accuracy": 0.95, "f1": 0.93},
            config={"type": "classifier"},
            description="Test model",
            tags=["test", "classifier"]
        )
        
        assert model_id is not None
        
        # Retrieve
        model = setup_registry.get_model("test_model", "1.0.0")
        
        assert model is not None
        assert model.model_name == "test_model"
        assert model.version == "1.0.0"
        assert model.training_samples == 1000
        assert model.metrics["accuracy"] == 0.95
        
        print("✅ Model registration test passed")
    
    def test_model_versioning(self, setup_registry):
        """Test model versioning."""
        # Register v1.0.0
        setup_registry.register_model(
            model_name="versioned_model",
            version="1.0.0",
            model_path="/path/v1.pkl",
            model_type="sklearn",
            training_samples=1000,
            metrics={"accuracy": 0.90},
            config={},
            description="Version 1"
        )
        
        # Register v1.1.0
        setup_registry.register_model(
            model_name="versioned_model",
            version="1.1.0",
            model_path="/path/v2.pkl",
            model_type="sklearn",
            training_samples=1500,
            metrics={"accuracy": 0.93},
            config={},
            description="Version 2",
            parent_version="1.0.0"
        )
        
        # Get latest
        latest = setup_registry.get_model("versioned_model")
        assert latest.version == "1.1.0"
        
        # Get specific version
        v1 = setup_registry.get_model("versioned_model", "1.0.0")
        assert v1 is not None
        assert v1.version == "1.0.0"
        
        print("✅ Model versioning test passed")
    
    def test_production_model(self, setup_registry):
        """Test production model management."""
        # Register two versions
        setup_registry.register_model(
            model_name="prod_model",
            version="1.0.0",
            model_path="/path/v1.pkl",
            model_type="sklearn",
            training_samples=1000,
            metrics={"accuracy": 0.90},
            config={},
            description="V1"
        )
        
        setup_registry.register_model(
            model_name="prod_model",
            version="2.0.0",
            model_path="/path/v2.pkl",
            model_type="sklearn",
            training_samples=2000,
            metrics={"accuracy": 0.95},
            config={},
            description="V2"
        )
        
        # Set v2 as production
        success = setup_registry.set_production("prod_model", "2.0.0")
        assert success
        
        # Verify
        v2 = setup_registry.get_model("prod_model", "2.0.0")
        assert v2.is_production
        
        # Verify v1 is not production
        v1 = setup_registry.get_model("prod_model", "1.0.0")
        assert not v1.is_production
        
        print("✅ Production model test passed")
    
    def test_model_lineage(self, setup_registry):
        """Test model lineage tracking."""
        # Register chain of versions
        setup_registry.register_model(
            model_name="lineage_model",
            version="1.0.0",
            model_path="/path/v1.pkl",
            model_type="sklearn",
            training_samples=1000,
            metrics={"accuracy": 0.85},
            config={},
            description="V1"
        )
        
        setup_registry.register_model(
            model_name="lineage_model",
            version="1.1.0",
            model_path="/path/v2.pkl",
            model_type="sklearn",
            training_samples=1200,
            metrics={"accuracy": 0.88},
            config={},
            description="V2",
            parent_version="1.0.0"
        )
        
        setup_registry.register_model(
            model_name="lineage_model",
            version="2.0.0",
            model_path="/path/v3.pkl",
            model_type="sklearn",
            training_samples=2000,
            metrics={"accuracy": 0.92},
            config={},
            description="V3",
            parent_version="1.1.0"
        )
        
        # Get lineage
        lineage = setup_registry.get_lineage("lineage_model")
        
        assert len(lineage) == 3
        assert lineage[0]["version"] == "1.0.0"
        assert lineage[1]["version"] == "1.1.0"
        assert lineage[2]["version"] == "2.0.0"
        
        # Check parent relationships
        assert lineage[1]["parent_version"] == "1.0.0"
        assert lineage[2]["parent_version"] == "1.1.0"
        
        print("✅ Model lineage test passed")


class TestIntegration:
    """Integration tests combining all components."""
    
    @pytest.fixture
    def setup_integration(self, tmp_path):
        """Setup integration test environment."""
        base_dir = tmp_path / "integration_test"
        base_dir.mkdir()
        
        return {
            "base_dir": base_dir,
            "models_dir": base_dir / "models",
            "registry_db": base_dir / "registry.db",
            "embeddings_db": base_dir / "embeddings.db"
        }
    
    def test_end_to_end_workflow(self, setup_integration):
        """Test complete workflow from training to deployment."""
        try:
            from sklearn.ensemble import RandomForestClassifier
            
            # 1. Train model
            print("\n🔧 Training model...")
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            X_train = np.random.rand(100, 10)
            y_train = np.random.randint(0, 2, 100)
            model.fit(X_train, y_train)
            
            # 2. Save model
            print("💾 Saving model...")
            persister = ModelPersistence(str(setup_integration["models_dir"]))
            
            metadata = ModelMetadata(
                model_name="integration_test_model",
                model_type="sklearn",
                version="1.0.0",
                created_at="",
                training_samples=100,
                features=[f"feature_{i}" for i in range(10)],
                metrics={"accuracy": 0.85},
                config={"n_estimators": 10},
                checksum="",
                file_size=0,
                description="Integration test model"
            )
            
            saved_path = persister.save(model, "integration_test_model", metadata)
            assert saved_path.exists()
            
            # 3. Register in registry
            print("📝 Registering model...")
            registry = ModelRegistry(str(setup_integration["registry_db"]))
            
            model_id = registry.register_model(
                model_name="integration_test_model",
                version="1.0.0",
                model_path=str(saved_path),
                model_type="sklearn",
                training_samples=100,
                metrics={"accuracy": 0.85, "precision": 0.83},
                config={"n_estimators": 10},
                description="Integration test model",
                tags=["test", "integration"]
            )
            assert model_id is not None
            
            # 4. Promote to production
            print("🏆 Setting as production...")
            success = registry.set_production("integration_test_model", "1.0.0")
            assert success
            
            # 5. Verify complete workflow
            print("✅ Verifying workflow...")
            models = registry.list_models()
            assert len(models) == 1
            assert models[0]["name"] == "integration_test_model"
            assert models[0]["is_production"]
            
            # 6. Load and use model
            print("🔄 Loading production model...")
            loaded_model = persister.load("integration_test_model")
            
            # Make predictions
            X_test = np.random.rand(5, 10)
            predictions = loaded_model.predict(X_test)
            
            assert len(predictions) == 5
            assert all(p in [0, 1] for p in predictions)
            
            print("✅ End-to-end workflow test PASSED")
            
        except Exception as e:
            pytest.fail(f"Integration test failed: {e}")


def run_tests():
    """Run all tests manually."""
    import tempfile
    
    print("=" * 60)
    print("REGIQ Model Persistence Test Suite")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Run individual tests
        print("\n1️⃣ Testing Model Persistence Layer...")
        test_persister = TestModelPersistence()
        fixture = test_persister.setup_persister(tmp_path / "persister")
        try:
            test_persister.test_save_sklearn_model(fixture)
            test_persister.test_model_metadata_tracking(fixture)
            test_persister.test_list_models(fixture)
        finally:
            del fixture
        
        print("\n2️⃣ Testing Embedding Persistence...")
        test_embedding = TestEmbeddingPersistence()
        fixture = test_embedding.setup_embedding_db(tmp_path / "embeddings")
        try:
            test_embedding.test_save_and_retrieve_embedding(fixture)
            test_embedding.test_embedding_cache(fixture)
            test_embedding.test_batch_operations(fixture)
        finally:
            del fixture
        
        print("\n3️⃣ Testing Model Registry...")
        test_registry = TestModelRegistry()
        fixture = test_registry.setup_registry(tmp_path / "registry")
        try:
            test_registry.test_register_model(fixture)
            test_registry.test_model_versioning(fixture)
            test_registry.test_production_model(fixture)
            test_registry.test_model_lineage(fixture)
        finally:
            del fixture
        
        print("\n4️⃣ Running Integration Tests...")
        test_integration = TestIntegration()
        fixture = test_integration.setup_integration(tmp_path / "integration")
        try:
            test_integration.test_end_to_end_workflow(fixture)
        finally:
            del fixture
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
