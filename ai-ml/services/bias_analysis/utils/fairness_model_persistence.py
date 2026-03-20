"""
Bias & Fairness Model Persistence

Handles saving and loading of:
- Fairness assessment models
- Bias mitigation models (preprocessing, in-processing, post-processing)
- Explanation models (SHAP, LIME)
- Precomputed fairness metrics
"""

import os
import sys
import joblib
import numpy as np
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json
import hashlib

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from regulatory_intelligence.utils.model_persistence import ModelPersistence
except ImportError:
    # Fallback if regulatory_intelligence not available
    ModelPersistence = object


class FairnessModelPersistence:
    """
    Specialized persistence for bias & fairness models.
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize fairness model persistence."""
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # Go up to ai-ml root, then to models/fairness
            self.base_dir = Path(__file__).parent.parent.parent.parent / "models" / "fairness"
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Subdirectories for different model types
        self.subdirs = {
            'preprocessing': self.base_dir / "preprocessing",
            'in_processing': self.base_dir / "in_processing",
            'post_processing': self.base_dir / "post_processing",
            'explanation': self.base_dir / "explanation",
            'metrics': self.base_dir / "metrics",
        }
        
        for subdir in self.subdirs.values():
            subdir.mkdir(parents=True, exist_ok=True)
        
        self.mp = ModelPersistence()
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger."""
        import logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def save_mitigation_model(
        self,
        model: Any,
        technique_name: str,
        category: str,
        dataset_name: str,
        protected_attributes: List[str],
        metrics_before: Dict[str, float],
        metrics_after: Dict[str, float],
        version: str = "1.0.0",
        description: str = "",
        tags: Optional[List[str]] = None
    ) -> Path:
        """
        Save bias mitigation model with metadata.
        
        Args:
            model: Trained mitigation model (Reweighing, FairnessThroughAwareness, etc.)
            technique_name: Name of technique (e.g., 'reweighing', 'adversarial_debiasing')
            category: Category ('preprocessing', 'in_processing', 'post_processing')
            dataset_name: Name of dataset used for training
            protected_attributes: List of protected attributes used
            metrics_before: Fairness metrics before mitigation
            metrics_after: Fairness metrics after mitigation
            version: Model version
            description: Model description
            tags: List of tags
            
        Returns:
            Path to saved model
        """
        if category not in self.subdirs:
            raise ValueError(f"Invalid category: {category}")
        
        model_dir = self.subdirs[category] / technique_name / version
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model
        model_path = model_dir / f"{technique_name}.pkl"
        joblib.dump(model, model_path)
        
        # Calculate checksum
        checksum = self._calculate_checksum(model_path)
        
        # Create metadata
        metadata = {
            'model_type': 'fairness_mitigation',
            'technique_name': technique_name,
            'category': category,
            'dataset_name': dataset_name,
            'protected_attributes': protected_attributes,
            'metrics_before': metrics_before,
            'metrics_after': metrics_after,
            'improvement': self._calculate_improvement(metrics_before, metrics_after),
            'version': version,
            'description': description,
            'tags': tags or [],
            'checksum': checksum,
            'framework': 'sklearn' if hasattr(model, 'predict') else 'custom',
        }
        
        # Save metadata
        metadata_path = model_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        self.logger.info(f"✅ Saved {category} mitigation model: {technique_name} v{version}")
        self.logger.info(f"   Improvement: {metadata['improvement']:.2%}")
        
        return model_path
    
    def load_mitigation_model(
        self,
        technique_name: str,
        category: str,
        version: str = "1.0.0"
    ) -> tuple:
        """
        Load bias mitigation model.
        
        Args:
            technique_name: Name of technique
            category: Category ('preprocessing', 'in_processing', 'post_processing')
            version: Model version
            
        Returns:
            Tuple of (model, metadata)
        """
        if category not in self.subdirs:
            raise ValueError(f"Invalid category: {category}")
        
        model_dir = self.subdirs[category] / technique_name / version
        model_path = model_dir / f"{technique_name}.pkl"
        metadata_path = model_dir / "metadata.json"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Load model
        model = joblib.load(model_path)
        
        # Load metadata
        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        
        # Verify checksum
        if metadata.get('checksum'):
            current_checksum = self._calculate_checksum(model_path)
            if current_checksum != metadata['checksum']:
                self.logger.warning(f"⚠️ Checksum mismatch for {technique_name}")
        
        self.logger.info(f"✅ Loaded {category} mitigation model: {technique_name}")
        
        return model, metadata
    
    def save_explanation_model(
        self,
        explainer: Any,
        explainer_type: str,
        model_name: str,
        dataset_name: str,
        feature_names: List[str],
        version: str = "1.0.0",
        description: str = ""
    ) -> Path:
        """
        Save explanation model (SHAP/LIME).
        
        Args:
            explainer: SHAP or LIME explainer object
            explainer_type: Type ('shap', 'lime')
            model_name: Name of model being explained
            dataset_name: Name of background dataset
            feature_names: List of feature names
            version: Explainer version
            description: Description
            
        Returns:
            Path to saved explainer
        """
        explainer_dir = self.subdirs['explanation'] / explainer_type / model_name / version
        explainer_dir.mkdir(parents=True, exist_ok=True)
        
        # Save explainer
        explainer_path = explainer_dir / f"{explainer_type}_explainer.pkl"
        joblib.dump(explainer, explainer_path)
        
        # Create metadata
        metadata = {
            'model_type': 'explanation',
            'explainer_type': explainer_type,
            'model_name': model_name,
            'dataset_name': dataset_name,
            'feature_names': feature_names,
            'version': version,
            'description': description,
            'n_features': len(feature_names),
        }
        
        # Save metadata
        metadata_path = explainer_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        self.logger.info(f"✅ Saved {explainer_type.upper()} explainer for {model_name}")
        
        return explainer_path
    
    def load_explanation_model(
        self,
        explainer_type: str,
        model_name: str,
        version: str = "1.0.0"
    ) -> tuple:
        """
        Load explanation model.
        
        Args:
            explainer_type: Type ('shap', 'lime')
            model_name: Name of model
            version: Explainer version
            
        Returns:
            Tuple of (explainer, metadata)
        """
        explainer_dir = self.subdirs['explanation'] / explainer_type / model_name / version
        explainer_path = explainer_dir / f"{explainer_type}_explainer.pkl"
        metadata_path = explainer_dir / "metadata.json"
        
        if not explainer_path.exists():
            raise FileNotFoundError(f"Explainer not found: {explainer_path}")
        
        # Load explainer
        explainer = joblib.load(explainer_path)
        
        # Load metadata
        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        
        self.logger.info(f"✅ Loaded {explainer_type.upper()} explainer for {model_name}")
        
        return explainer, metadata
    
    def save_fairness_metrics(
        self,
        metrics: Dict[str, Any],
        model_name: str,
        dataset_name: str,
        protected_attributes: List[str],
        evaluation_type: str = 'fairness_assessment'
    ) -> Path:
        """
        Save precomputed fairness metrics.
        
        Args:
            metrics: Dictionary of fairness metrics
            model_name: Name of evaluated model
            dataset_name: Name of test dataset
            protected_attributes: List of protected attributes
            evaluation_type: Type of evaluation
            
        Returns:
            Path to saved metrics
        """
        metrics_dir = self.subdirs['metrics'] / model_name
        metrics_dir.mkdir(parents=True, exist_ok=True)
        
        metrics_path = metrics_dir / f"{evaluation_type}_metrics.json"
        
        # Add timestamp
        from datetime import datetime
        metrics_with_meta = {
            'metrics': metrics,
            'metadata': {
                'model_name': model_name,
                'dataset_name': dataset_name,
                'protected_attributes': protected_attributes,
                'evaluation_type': evaluation_type,
                'timestamp': datetime.now().isoformat(),
            }
        }
        
        with open(metrics_path, 'w') as f:
            json.dump(metrics_with_meta, f, indent=2, default=float)
        
        self.logger.info(f"✅ Saved fairness metrics for {model_name}")
        
        return metrics_path
    
    def load_fairness_metrics(
        self,
        model_name: str,
        evaluation_type: str = 'fairness_assessment'
    ) -> Dict[str, Any]:
        """
        Load precomputed fairness metrics.
        
        Args:
            model_name: Name of model
            evaluation_type: Type of evaluation
            
        Returns:
            Dictionary of metrics with metadata
        """
        metrics_dir = self.subdirs['metrics'] / model_name
        metrics_path = metrics_dir / f"{evaluation_type}_metrics.json"
        
        if not metrics_path.exists():
            raise FileNotFoundError(f"Metrics not found: {metrics_path}")
        
        with open(metrics_path, 'r') as f:
            metrics_data = json.load(f)
        
        self.logger.info(f"✅ Loaded fairness metrics for {model_name}")
        
        return metrics_data
    
    def list_available_models(self) -> Dict[str, List[str]]:
        """List all available fairness models."""
        available = {
            'preprocessing': [],
            'in_processing': [],
            'post_processing': [],
            'explanation': [],
            'metrics': [],
        }
        
        # Check each category
        for category, subdir in self.subdirs.items():
            if category in ['preprocessing', 'in_processing', 'post_processing']:
                if subdir.exists():
                    available[category] = [
                        d.name for d in subdir.iterdir() 
                        if d.is_dir() and not d.name.startswith('.')
                    ]
            
            elif category == 'explanation':
                if subdir.exists():
                    for model_dir in subdir.iterdir():
                        if model_dir.is_dir():
                            for explainer_dir in model_dir.iterdir():
                                if explainer_dir.is_dir():
                                    available[category].append(
                                        f"{model_dir.name}/{explainer_dir.name}"
                                    )
            
            elif category == 'metrics':
                if subdir.exists():
                    available[category] = [
                        d.name for d in subdir.iterdir()
                        if d.is_dir() and not d.name.startswith('.')
                    ]
        
        return available
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def _calculate_improvement(
        self,
        metrics_before: Dict[str, float],
        metrics_after: Dict[str, float]
    ) -> float:
        """
        Calculate overall improvement in fairness metrics.
        
        Args:
            metrics_before: Metrics before mitigation
            metrics_after: Metrics after mitigation
            
        Returns:
            Improvement ratio (higher is better)
        """
        # Calculate average improvement across metrics
        improvements = []
        
        for key in metrics_before.keys():
            if key in metrics_after and key not in ['accuracy', 'f1_score']:
                before = metrics_before[key]
                after = metrics_after[key]
                
                # For disparity metrics, lower is better
                if 'disparity' in key.lower() or 'difference' in key.lower():
                    if before > 0:
                        imp = (before - after) / before
                    else:
                        imp = 0
                # For parity metrics, higher is better
                elif 'parity' in key.lower() or 'ratio' in key.lower():
                    if before > 0:
                        imp = (after - before) / before
                    else:
                        imp = 0
                else:
                    # Generic: assume lower is better
                    if before > 0:
                        imp = (before - after) / before
                    else:
                        imp = 0
                
                improvements.append(imp)
        
        return np.mean(improvements) if improvements else 0.0


# Convenience functions
def save_mitigation_model(model, **kwargs) -> Path:
    """Save a bias mitigation model."""
    fp = FairnessModelPersistence()
    return fp.save_mitigation_model(model, **kwargs)


def load_mitigation_model(technique_name: str, category: str, version: str = "1.0.0"):
    """Load a bias mitigation model."""
    fp = FairnessModelPersistence()
    return fp.load_mitigation_model(technique_name, category, version)


def save_explanation_model(explainer, **kwargs) -> Path:
    """Save an explanation model."""
    fp = FairnessModelPersistence()
    return fp.save_explanation_model(explainer, **kwargs)


def load_explanation_model(explainer_type: str, model_name: str, version: str = "1.0.0"):
    """Load an explanation model."""
    fp = FairnessModelPersistence()
    return fp.load_explanation_model(explainer_type, model_name, version)
