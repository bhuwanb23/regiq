#!/usr/bin/env python3
"""
REGIQ AI/ML - Model Input System
Handles model upload, validation, and metadata storage for bias analysis.
"""

import os
import sys
import json
import logging
import pickle
import joblib
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
import hashlib
import time

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import pandas as pd
    import numpy as np
    from sklearn.base import BaseEstimator
    from sklearn.model_selection import train_test_split
    PANDAS_AVAILABLE = True
    SKLEARN_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    SKLEARN_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import onnx
    import onnxruntime as ort
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class ModelMetadata:
    """Metadata for uploaded models."""
    model_id: str
    name: str
    model_type: str  # sklearn, pytorch, onnx, custom
    framework: str
    version: str
    upload_date: str
    file_size: int
    file_hash: str
    description: str
    target_variable: str
    feature_columns: List[str]
    protected_attributes: List[str]
    training_data_size: int
    model_parameters: Dict[str, Any]
    performance_metrics: Dict[str, float]
    bias_analysis_status: str  # pending, in_progress, completed, failed
    metadata: Dict[str, Any]


@dataclass
class ModelUploadConfig:
    """Configuration for model upload system."""
    # Upload settings
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_extensions: List[str] = None
    upload_directory: str = "data/models/uploaded"
    metadata_directory: str = "data/models/metadata"
    
    # Model validation settings
    validate_structure: bool = True
    validate_predictions: bool = True
    test_sample_size: int = 100
    
    # Supported formats
    supported_frameworks: List[str] = None
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = ['.pkl', '.joblib', '.pth', '.pt', '.onnx', '.h5', '.pb']
        
        if self.supported_frameworks is None:
            self.supported_frameworks = ['sklearn', 'pytorch', 'tensorflow', 'onnx', 'xgboost', 'lightgbm']


class ModelUploader:
    """Handles model upload, validation, and storage."""
    
    def __init__(self, config: Optional[ModelUploadConfig] = None):
        self.config = config or ModelUploadConfig()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        self._create_directories()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("model_uploader")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def _create_directories(self):
        """Create necessary directories for model storage."""
        try:
            os.makedirs(self.config.upload_directory, exist_ok=True)
            os.makedirs(self.config.metadata_directory, exist_ok=True)
            self.logger.info(f"Created directories: {self.config.upload_directory}, {self.config.metadata_directory}")
        except Exception as e:
            self.logger.error(f"Failed to create directories: {e}")
    
    def upload_model(self, file_path: str, model_name: str, 
                    description: str = "", target_variable: str = "",
                    protected_attributes: List[str] = None) -> Optional[ModelMetadata]:
        """Upload and validate a model file."""
        try:
            # Validate file
            if not self._validate_file(file_path):
                return None
            
            # Generate model ID and metadata
            model_id = self._generate_model_id(model_name)
            file_hash = self._calculate_file_hash(file_path)
            file_size = os.path.getsize(file_path)
            
            # Detect model type and framework
            model_type, framework = self._detect_model_type(file_path)
            
            # Load and validate model
            model = self._load_model(file_path, model_type)
            if model is None:
                return None
            
            # Extract model information
            model_info = self._extract_model_info(model, model_type)
            
            # Create metadata
            metadata = ModelMetadata(
                model_id=model_id,
                name=model_name,
                model_type=model_type,
                framework=framework,
                version=model_info.get("version", "1.0.0"),
                upload_date=time.strftime("%Y-%m-%d %H:%M:%S"),
                file_size=file_size,
                file_hash=file_hash,
                description=description,
                target_variable=target_variable,
                feature_columns=model_info.get("feature_columns", []),
                protected_attributes=protected_attributes or [],
                training_data_size=model_info.get("training_data_size", 0),
                model_parameters=model_info.get("parameters", {}),
                performance_metrics=model_info.get("performance_metrics", {}),
                bias_analysis_status="pending",
                metadata=model_info.get("metadata", {})
            )
            
            # Save model and metadata
            self._save_model_file(file_path, model_id)
            self._save_metadata(metadata)
            
            self.logger.info(f"Successfully uploaded model: {model_id}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Failed to upload model: {e}")
            return None
    
    def _validate_file(self, file_path: str) -> bool:
        """Validate uploaded file."""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return False
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.config.max_file_size:
                self.logger.error(f"File too large: {file_size} bytes (max: {self.config.max_file_size})")
                return False
            
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in self.config.allowed_extensions:
                self.logger.error(f"Unsupported file extension: {file_ext}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"File validation failed: {e}")
            return False
    
    def _generate_model_id(self, model_name: str) -> str:
        """Generate unique model ID."""
        timestamp = str(int(time.time()))
        name_hash = hashlib.md5(model_name.encode()).hexdigest()[:8]
        return f"model_{name_hash}_{timestamp}"
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Failed to calculate file hash: {e}")
            return ""
    
    def _detect_model_type(self, file_path: str) -> Tuple[str, str]:
        """Detect model type and framework from file."""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in ['.pkl', '.joblib']:
            return 'sklearn', 'scikit-learn'
        elif file_ext in ['.pth', '.pt']:
            return 'pytorch', 'pytorch'
        elif file_ext == '.onnx':
            return 'onnx', 'onnx'
        elif file_ext in ['.h5', '.pb']:
            return 'tensorflow', 'tensorflow'
        else:
            return 'unknown', 'unknown'
    
    def _load_model(self, file_path: str, model_type: str) -> Optional[Any]:
        """Load model from file based on type."""
        try:
            if model_type == 'sklearn':
                return self._load_sklearn_model(file_path)
            elif model_type == 'pytorch':
                return self._load_pytorch_model(file_path)
            elif model_type == 'onnx':
                return self._load_onnx_model(file_path)
            else:
                self.logger.warning(f"Unsupported model type: {model_type}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return None
    
    def _load_sklearn_model(self, file_path: str) -> Optional[Any]:
        """Load scikit-learn model."""
        try:
            if not SKLEARN_AVAILABLE:
                self.logger.error("scikit-learn not available")
                return None
            
            # Try different loading methods
            if file_path.endswith('.pkl'):
                with open(file_path, 'rb') as f:
                    model = pickle.load(f)
            elif file_path.endswith('.joblib'):
                model = joblib.load(file_path)
            else:
                return None
            
            # Validate model structure
            if self.config.validate_structure:
                if not hasattr(model, 'predict'):
                    self.logger.error("Model does not have predict method")
                    return None
            
            return model
        except Exception as e:
            self.logger.error(f"Failed to load sklearn model: {e}")
            return None
    
    def _load_pytorch_model(self, file_path: str) -> Optional[Any]:
        """Load PyTorch model."""
        try:
            if not TORCH_AVAILABLE:
                self.logger.error("PyTorch not available")
                return None
            
            model = torch.load(file_path, map_location='cpu')
            
            # Validate model structure
            if self.config.validate_structure:
                if not isinstance(model, (nn.Module, dict)):
                    self.logger.error("Invalid PyTorch model structure")
                    return None
            
            return model
        except Exception as e:
            self.logger.error(f"Failed to load PyTorch model: {e}")
            return None
    
    def _load_onnx_model(self, file_path: str) -> Optional[Any]:
        """Load ONNX model."""
        try:
            if not ONNX_AVAILABLE:
                self.logger.error("ONNX not available")
                return None
            
            # Load ONNX model
            model = onnx.load(file_path)
            
            # Validate model
            if self.config.validate_structure:
                onnx.checker.check_model(model)
            
            return model
        except Exception as e:
            self.logger.error(f"Failed to load ONNX model: {e}")
            return None
    
    def _extract_model_info(self, model: Any, model_type: str) -> Dict[str, Any]:
        """Extract information from loaded model."""
        info = {
            "version": "1.0.0",
            "feature_columns": [],
            "training_data_size": 0,
            "parameters": {},
            "performance_metrics": {},
            "metadata": {}
        }
        
        try:
            if model_type == 'sklearn' and hasattr(model, 'get_params'):
                info["parameters"] = model.get_params()
                
                # Extract feature names if available
                if hasattr(model, 'feature_names_in_'):
                    info["feature_columns"] = list(model.feature_names_in_)
                elif hasattr(model, 'feature_importances_'):
                    info["feature_columns"] = [f"feature_{i}" for i in range(len(model.feature_importances_))]
            
            elif model_type == 'pytorch':
                if isinstance(model, nn.Module):
                    info["parameters"] = {
                        "num_parameters": sum(p.numel() for p in model.parameters()),
                        "trainable_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad)
                    }
            
            elif model_type == 'onnx':
                info["parameters"] = {
                    "input_shapes": [input.type.tensor_type.shape for input in model.graph.input],
                    "output_shapes": [output.type.tensor_type.shape for output in model.graph.output]
                }
            
        except Exception as e:
            self.logger.warning(f"Failed to extract model info: {e}")
        
        return info
    
    def _save_model_file(self, source_path: str, model_id: str):
        """Save model file to storage directory."""
        try:
            dest_path = os.path.join(self.config.upload_directory, f"{model_id}.model")
            import shutil
            shutil.copy2(source_path, dest_path)
            self.logger.info(f"Model file saved: {dest_path}")
        except Exception as e:
            self.logger.error(f"Failed to save model file: {e}")
    
    def _save_metadata(self, metadata: ModelMetadata):
        """Save model metadata to file."""
        try:
            metadata_path = os.path.join(self.config.metadata_directory, f"{metadata.model_id}.json")
            with open(metadata_path, 'w') as f:
                json.dump(asdict(metadata), f, indent=2)
            self.logger.info(f"Metadata saved: {metadata_path}")
        except Exception as e:
            self.logger.error(f"Failed to save metadata: {e}")
    
    def get_model_metadata(self, model_id: str) -> Optional[ModelMetadata]:
        """Retrieve model metadata by ID."""
        try:
            metadata_path = os.path.join(self.config.metadata_directory, f"{model_id}.json")
            if not os.path.exists(metadata_path):
                return None
            
            with open(metadata_path, 'r') as f:
                data = json.load(f)
            
            return ModelMetadata(**data)
        except Exception as e:
            self.logger.error(f"Failed to get model metadata: {e}")
            return None
    
    def list_models(self) -> List[ModelMetadata]:
        """List all uploaded models."""
        try:
            models = []
            for filename in os.listdir(self.config.metadata_directory):
                if filename.endswith('.json'):
                    model_id = filename[:-5]  # Remove .json extension
                    metadata = self.get_model_metadata(model_id)
                    if metadata:
                        models.append(metadata)
            
            return sorted(models, key=lambda x: x.upload_date, reverse=True)
        except Exception as e:
            self.logger.error(f"Failed to list models: {e}")
            return []


def main():
    """Test the model upload system."""
    print("🧪 Testing Model Upload System")
    
    # Test configuration
    config = ModelUploadConfig()
    uploader = ModelUploader(config)
    
    # Test metadata creation
    metadata = ModelMetadata(
        model_id="test_model_001",
        name="Test Model",
        model_type="sklearn",
        framework="scikit-learn",
        version="1.0.0",
        upload_date="2025-01-01",
        file_size=1024,
        file_hash="test_hash",
        description="Test model for bias analysis",
        target_variable="target",
        feature_columns=["feature1", "feature2"],
        protected_attributes=["gender", "age"],
        training_data_size=1000,
        model_parameters={},
        performance_metrics={},
        bias_analysis_status="pending",
        metadata={}
    )
    
    print("✅ Model metadata created")
    print(f"✅ Model ID: {metadata.model_id}")
    print(f"✅ Framework: {metadata.framework}")
    print(f"✅ Protected attributes: {metadata.protected_attributes}")
    
    # Test model listing
    models = uploader.list_models()
    print(f"✅ Found {len(models)} models in storage")


if __name__ == "__main__":
    main()
