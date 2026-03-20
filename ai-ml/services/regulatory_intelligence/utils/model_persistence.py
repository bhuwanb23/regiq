"""
REGIQ AI/ML - Model Persistence Layer

This module provides a unified interface for saving and loading ML models
with support for multiple frameworks (scikit-learn, PyTorch, TensorFlow, spaCy).

Features:
- Automatic format detection
- Compression support
- Metadata storage
- Version control
- Checksum validation
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
import pickle
import joblib

logger = logging.getLogger(__name__)


@dataclass
class ModelMetadata:
    """Metadata for a saved model."""
    model_name: str
    model_type: str  # sklearn, pytorch, tensorflow, spacy
    version: str
    created_at: str
    training_samples: int
    features: list
    metrics: Dict[str, float]
    config: Dict[str, Any]
    checksum: str
    file_size: int
    description: str = ""
    tags: list = None


class ModelPersistence:
    """
    Unified model persistence layer supporting multiple frameworks.
    
    Example:
        >>> persister = ModelPersistence("models/nlp")
        >>> persister.save(model, "ner_model", metadata)
        >>> loaded_model = persister.load("ner_model")
    """
    
    def __init__(self, base_dir: str = "models"):
        """
        Initialize model persister.
        
        Args:
            base_dir: Base directory for storing models
        """
        self.base_dir = Path(base_dir)
        self._ensure_directories()
        logger.info(f"Model persistence initialized at {self.base_dir}")
    
    def _ensure_directories(self):
        """Create necessary directories."""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        (self.base_dir / "sklearn").mkdir(exist_ok=True)
        (self.base_dir / "pytorch").mkdir(exist_ok=True)
        (self.base_dir / "tensorflow").mkdir(exist_ok=True)
        (self.base_dir / "spacy").mkdir(exist_ok=True)
        (self.base_dir / "metadata").mkdir(exist_ok=True)
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file or directory."""
        sha256_hash = hashlib.sha256()
        
        if file_path.is_dir():
            # For directories (like spaCy models), hash all files
            for root, dirs, files in sorted(os.walk(file_path)):
                for filename in sorted(files):
                    filepath = Path(root) / filename
                    with open(filepath, "rb") as f:
                        sha256_hash.update(filename.encode())
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(chunk)
        else:
            # For single files
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def _get_model_path(self, model_name: str, model_type: str) -> Path:
        """Get path for model file."""
        extension_map = {
            'sklearn': '.pkl',
            'pytorch': '.pth',
            'tensorflow': '.keras',
            'spacy': ''
        }
        ext = extension_map.get(model_type, '.pkl')
        return self.base_dir / model_type / f"{model_name}{ext}"
    
    def _get_metadata_path(self, model_name: str) -> Path:
        """Get path for metadata file."""
        return self.base_dir / "metadata" / f"{model_name}_metadata.json"
    
    def save(self, 
             model: Any, 
             model_name: str, 
             metadata: ModelMetadata,
             compress: bool = True) -> Path:
        """
        Save model to disk.
        
        Args:
            model: Model object to save
            model_name: Name of the model
            metadata: Model metadata
            compress: Whether to compress the file
            
        Returns:
            Path to saved model
        """
        try:
            model_path = self._get_model_path(model_name, metadata.model_type)
            
            # Save model based on type
            if metadata.model_type == 'sklearn':
                joblib.dump(model, model_path, compress=compress)
            elif metadata.model_type == 'pytorch':
                import torch
                torch.save(model.state_dict(), model_path)
            elif metadata.model_type == 'tensorflow':
                model.save(str(model_path))
            elif metadata.model_type == 'spacy':
                model.to_disk(model_path)
            else:
                # Fallback to pickle
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)
            
            # Calculate checksum and file size
            metadata.checksum = self._calculate_checksum(model_path)
            metadata.file_size = model_path.stat().st_size
            metadata.created_at = datetime.now().isoformat()
            
            # Save metadata
            metadata_path = self._get_metadata_path(model_name)
            with open(metadata_path, 'w') as f:
                json.dump(asdict(metadata), f, indent=2)
            
            logger.info(f"✅ Saved model '{model_name}' to {model_path}")
            logger.info(f"   Size: {metadata.file_size:,} bytes")
            logger.info(f"   Checksum: {metadata.checksum[:16]}...")
            
            return model_path
            
        except Exception as e:
            logger.error(f"❌ Failed to save model '{model_name}': {e}")
            raise
    
    def load(self, model_name: str, model_type: str = None) -> Any:
        """
        Load model from disk.
        
        Args:
            model_name: Name of the model
            model_type: Type of model (auto-detected if None)
            
        Returns:
            Loaded model
        """
        try:
            # Auto-detect model type if not provided
            if model_type is None:
                model_type = self._detect_model_type(model_name)
            
            model_path = self._get_model_path(model_name, model_type)
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model '{model_name}' not found at {model_path}")
            
            # Verify checksum
            self._verify_checksum(model_name, model_path)
            
            # Load model based on type
            if model_type == 'sklearn':
                model = joblib.load(model_path)
            elif model_type == 'pytorch':
                import torch
                # Need to reconstruct model architecture first
                logger.warning("PyTorch models require manual reconstruction")
                model = torch.load(model_path)
            elif model_type == 'tensorflow':
                from tensorflow.keras.models import load_model
                model = load_model(str(model_path))
            elif model_type == 'spacy':
                import spacy
                model = spacy.load(str(model_path))
            else:
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
            
            logger.info(f"✅ Loaded model '{model_name}' from {model_path}")
            return model
            
        except Exception as e:
            logger.error(f"❌ Failed to load model '{model_name}': {e}")
            raise
    
    def _detect_model_type(self, model_name: str) -> str:
        """Detect model type by checking which files exist."""
        for model_type in ['sklearn', 'pytorch', 'tensorflow', 'spacy']:
            path = self._get_model_path(model_name, model_type)
            if path.exists() or (model_type == 'spacy' and (path / "meta.json").exists()):
                return model_type
        return 'sklearn'  # Default
    
    def _verify_checksum(self, model_name: str, model_path: Path):
        """Verify model file integrity."""
        metadata_path = self._get_metadata_path(model_name)
        if not metadata_path.exists():
            logger.warning(f"No metadata found for '{model_name}', skipping checksum")
            return
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        expected_checksum = metadata.get('checksum')
        if expected_checksum:
            actual_checksum = self._calculate_checksum(model_path)
            if expected_checksum != actual_checksum:
                logger.error(f"Checksum mismatch for '{model_name}'")
                raise ValueError("Model file corrupted or modified")
    
    def get_metadata(self, model_name: str) -> Optional[ModelMetadata]:
        """Get metadata for a model."""
        metadata_path = self._get_metadata_path(model_name)
        if not metadata_path.exists():
            return None
        
        with open(metadata_path, 'r') as f:
            data = json.load(f)
        return ModelMetadata(**data)
    
    def list_models(self) -> List[Dict[str, str]]:
        """List all available models."""
        models = []
        metadata_dir = self.base_dir / "metadata"
        
        for metadata_file in metadata_dir.glob("*_metadata.json"):
            model_name = metadata_file.stem.replace("_metadata", "")
            metadata = self.get_metadata(model_name)
            if metadata:
                models.append({
                    'name': metadata.model_name,
                    'type': metadata.model_type,
                    'version': metadata.version,
                    'created_at': metadata.created_at,
                    'size_mb': round(metadata.file_size / 1024 / 1024, 2)
                })
        
        return sorted(models, key=lambda x: x['created_at'], reverse=True)
    
    def delete(self, model_name: str) -> bool:
        """Delete a model and its metadata."""
        try:
            metadata = self.get_metadata(model_name)
            if not metadata:
                logger.warning(f"Model '{model_name}' not found")
                return False
            
            model_path = self._get_model_path(model_name, metadata.model_type)
            metadata_path = self._get_metadata_path(model_name)
            
            # Delete model file
            if model_path.exists():
                if metadata.model_type == 'spacy':
                    import shutil
                    shutil.rmtree(model_path)
                else:
                    model_path.unlink()
            
            # Delete metadata
            if metadata_path.exists():
                metadata_path.unlink()
            
            logger.info(f"✅ Deleted model '{model_name}'")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete model '{model_name}': {e}")
            return False
