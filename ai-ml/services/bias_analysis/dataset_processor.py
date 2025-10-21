#!/usr/bin/env python3
"""
REGIQ AI/ML - Dataset Processing
Handles dataset loading, protected attribute identification, and data quality validation.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
import time

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    PANDAS_AVAILABLE = True
    SKLEARN_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    SKLEARN_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class DatasetMetadata:
    """Metadata for processed datasets."""
    dataset_id: str
    name: str
    file_path: str
    file_size: int
    file_hash: str
    upload_date: str
    total_rows: int
    total_columns: int
    feature_columns: List[str]
    target_column: str
    protected_attributes: List[str]
    data_types: Dict[str, str]
    missing_values: Dict[str, int]
    unique_values: Dict[str, int]
    data_quality_score: float
    bias_analysis_ready: bool
    metadata: Dict[str, Any]


@dataclass
class ProtectedAttributeInfo:
    """Information about a protected attribute."""
    attribute_name: str
    attribute_type: str  # categorical, numerical, binary
    unique_values: List[Any]
    value_counts: Dict[str, int]
    missing_count: int
    bias_risk_level: str  # high, medium, low
    legal_protection: bool
    description: str
    metadata: Dict[str, Any]


@dataclass
class DatasetProcessingConfig:
    """Configuration for dataset processing."""
    # File settings
    max_file_size: int = 500 * 1024 * 1024  # 500MB
    allowed_extensions: List[str] = None
    upload_directory: str = "data/datasets/uploaded"
    processed_directory: str = "data/datasets/processed"
    metadata_directory: str = "data/datasets/metadata"
    
    # Data quality settings
    min_rows: int = 100
    max_missing_ratio: float = 0.5
    min_unique_values: int = 2
    
    # Protected attribute detection
    auto_detect_protected: bool = True
    protected_attribute_keywords: List[str] = None
    bias_risk_threshold: float = 0.3
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = ['.csv', '.xlsx', '.xls', '.parquet', '.json', '.pkl']
        
        if self.protected_attribute_keywords is None:
            self.protected_attribute_keywords = [
                'gender', 'sex', 'race', 'ethnicity', 'age', 'religion', 'disability',
                'marital_status', 'nationality', 'sexual_orientation', 'gender_identity',
                'pregnancy', 'veteran_status', 'immigration_status', 'language',
                'education_level', 'income_level', 'zip_code', 'postal_code'
            ]


class DatasetProcessor:
    """Processes datasets for bias analysis."""
    
    def __init__(self, config: Optional[DatasetProcessingConfig] = None):
        self.config = config or DatasetProcessingConfig()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        self._create_directories()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("dataset_processor")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def _create_directories(self):
        """Create necessary directories for dataset storage."""
        try:
            os.makedirs(self.config.upload_directory, exist_ok=True)
            os.makedirs(self.config.processed_directory, exist_ok=True)
            os.makedirs(self.config.metadata_directory, exist_ok=True)
            self.logger.info("Created dataset directories")
        except Exception as e:
            self.logger.error(f"Failed to create directories: {e}")
    
    def process_dataset(self, file_path: str, dataset_name: str, 
                       target_column: str = "", description: str = "") -> Optional[DatasetMetadata]:
        """Process a dataset for bias analysis."""
        try:
            # Validate file
            if not self._validate_file(file_path):
                return None
            
            # Load dataset
            df = self._load_dataset(file_path)
            if df is None:
                return None
            
            # Validate data quality
            if not self._validate_data_quality(df):
                return None
            
            # Generate dataset ID and metadata
            dataset_id = self._generate_dataset_id(dataset_name)
            file_hash = self._calculate_file_hash(file_path)
            file_size = os.path.getsize(file_path)
            
            # Analyze dataset
            analysis_results = self._analyze_dataset(df, target_column)
            
            # Detect protected attributes
            protected_attributes = self._detect_protected_attributes(df)
            
            # Create metadata
            metadata = DatasetMetadata(
                dataset_id=dataset_id,
                name=dataset_name,
                file_path=file_path,
                file_size=file_size,
                file_hash=file_hash,
                upload_date=time.strftime("%Y-%m-%d %H:%M:%S"),
                total_rows=len(df),
                total_columns=len(df.columns),
                feature_columns=analysis_results["feature_columns"],
                target_column=target_column,
                protected_attributes=protected_attributes,
                data_types=analysis_results["data_types"],
                missing_values=analysis_results["missing_values"],
                unique_values=analysis_results["unique_values"],
                data_quality_score=analysis_results["quality_score"],
                bias_analysis_ready=len(protected_attributes) > 0,
                metadata=analysis_results["metadata"]
            )
            
            # Save processed dataset and metadata
            self._save_processed_dataset(df, dataset_id)
            self._save_metadata(metadata)
            
            self.logger.info(f"Successfully processed dataset: {dataset_id}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Failed to process dataset: {e}")
            return None
    
    def _validate_file(self, file_path: str) -> bool:
        """Validate dataset file."""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return False
            
            file_size = os.path.getsize(file_path)
            if file_size > self.config.max_file_size:
                self.logger.error(f"File too large: {file_size} bytes")
                return False
            
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in self.config.allowed_extensions:
                self.logger.error(f"Unsupported file extension: {file_ext}")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"File validation failed: {e}")
            return False
    
    def _load_dataset(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load dataset from file."""
        try:
            if not PANDAS_AVAILABLE:
                self.logger.error("Pandas not available")
                return None
            
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_ext == '.parquet':
                df = pd.read_parquet(file_path)
            elif file_ext == '.json':
                df = pd.read_json(file_path)
            elif file_ext == '.pkl':
                df = pd.read_pickle(file_path)
            else:
                self.logger.error(f"Unsupported file format: {file_ext}")
                return None
            
            self.logger.info(f"Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to load dataset: {e}")
            return None
    
    def _validate_data_quality(self, df: pd.DataFrame) -> bool:
        """Validate data quality requirements."""
        try:
            # Check minimum rows
            if len(df) < self.config.min_rows:
                self.logger.error(f"Dataset too small: {len(df)} rows (min: {self.config.min_rows})")
                return False
            
            # Check for excessive missing values
            missing_ratio = df.isnull().sum().max() / len(df)
            if missing_ratio > self.config.max_missing_ratio:
                self.logger.error(f"Too many missing values: {missing_ratio:.2f} (max: {self.config.max_missing_ratio})")
                return False
            
            # Check for columns with insufficient unique values
            for col in df.columns:
                unique_count = df[col].nunique()
                if unique_count < self.config.min_unique_values:
                    self.logger.warning(f"Column '{col}' has only {unique_count} unique values")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Data quality validation failed: {e}")
            return False
    
    def _analyze_dataset(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Analyze dataset structure and statistics."""
        try:
            analysis = {
                "feature_columns": [],
                "data_types": {},
                "missing_values": {},
                "unique_values": {},
                "quality_score": 0.0,
                "metadata": {}
            }
            
            # Get feature columns (exclude target if specified)
            feature_columns = [col for col in df.columns if col != target_column]
            analysis["feature_columns"] = feature_columns
            
            # Analyze each column
            for col in df.columns:
                analysis["data_types"][col] = str(df[col].dtype)
                analysis["missing_values"][col] = int(df[col].isnull().sum())
                analysis["unique_values"][col] = int(df[col].nunique())
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(df)
            analysis["quality_score"] = quality_score
            
            # Add statistical metadata
            analysis["metadata"] = {
                "shape": df.shape,
                "memory_usage": df.memory_usage(deep=True).sum(),
                "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
                "categorical_columns": len(df.select_dtypes(include=['object']).columns),
                "datetime_columns": len(df.select_dtypes(include=['datetime']).columns)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Dataset analysis failed: {e}")
            return {}
    
    def _calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate data quality score (0-1)."""
        try:
            score = 1.0
            
            # Penalize for missing values
            missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
            score -= missing_ratio * 0.3
            
            # Penalize for duplicate rows
            duplicate_ratio = df.duplicated().sum() / len(df)
            score -= duplicate_ratio * 0.2
            
            # Penalize for columns with all same values
            constant_columns = (df.nunique() == 1).sum()
            score -= (constant_columns / len(df.columns)) * 0.3
            
            # Penalize for columns with too many unique values (potential ID columns)
            high_cardinality = (df.nunique() > len(df) * 0.9).sum()
            score -= (high_cardinality / len(df.columns)) * 0.2
            
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            self.logger.error(f"Quality score calculation failed: {e}")
            return 0.0
    
    def _detect_protected_attributes(self, df: pd.DataFrame) -> List[str]:
        """Detect protected attributes in the dataset."""
        try:
            protected_attributes = []
            
            if not self.config.auto_detect_protected:
                return protected_attributes
            
            for col in df.columns:
                col_lower = col.lower()
                
                # Check against keyword list
                if any(keyword in col_lower for keyword in self.config.protected_attribute_keywords):
                    protected_attributes.append(col)
                    continue
                
                # Check for demographic indicators
                if self._is_demographic_attribute(df[col]):
                    protected_attributes.append(col)
                    continue
                
                # Check for binary attributes with potential bias
                if self._is_potential_bias_attribute(df[col]):
                    protected_attributes.append(col)
            
            self.logger.info(f"Detected {len(protected_attributes)} protected attributes: {protected_attributes}")
            return protected_attributes
            
        except Exception as e:
            self.logger.error(f"Protected attribute detection failed: {e}")
            return []
    
    def _is_demographic_attribute(self, series: pd.Series) -> bool:
        """Check if attribute is demographic."""
        try:
            # Check for common demographic values
            demographic_values = [
                'male', 'female', 'm', 'f', 'man', 'woman',
                'white', 'black', 'asian', 'hispanic', 'latino',
                'married', 'single', 'divorced', 'widowed',
                'employed', 'unemployed', 'retired', 'student'
            ]
            
            unique_values = series.dropna().astype(str).str.lower().unique()
            demographic_matches = sum(1 for val in unique_values if val in demographic_values)
            
            return demographic_matches > len(unique_values) * 0.3
            
        except Exception as e:
            return False
    
    def _is_potential_bias_attribute(self, series: pd.Series) -> bool:
        """Check if attribute has potential for bias."""
        try:
            # Check for binary attributes with imbalanced distribution
            if series.nunique() == 2:
                value_counts = series.value_counts()
                min_count = value_counts.min()
                max_count = value_counts.max()
                
                # Check for significant imbalance
                imbalance_ratio = min_count / max_count
                if imbalance_ratio < self.config.bias_risk_threshold:
                    return True
            
            # Check for categorical attributes with few values
            if series.nunique() <= 5 and series.dtype == 'object':
                return True
            
            return False
            
        except Exception as e:
            return False
    
    def analyze_protected_attribute(self, df: pd.DataFrame, attribute_name: str) -> Optional[ProtectedAttributeInfo]:
        """Analyze a specific protected attribute."""
        try:
            if attribute_name not in df.columns:
                return None
            
            series = df[attribute_name]
            
            # Basic statistics
            unique_values = series.dropna().unique().tolist()
            value_counts = series.value_counts().to_dict()
            missing_count = series.isnull().sum()
            
            # Determine attribute type
            if series.nunique() == 2:
                attr_type = "binary"
            elif series.dtype in ['int64', 'float64']:
                attr_type = "numerical"
            else:
                attr_type = "categorical"
            
            # Assess bias risk
            bias_risk = self._assess_bias_risk(series)
            
            # Check legal protection status
            legal_protection = self._check_legal_protection(attribute_name)
            
            return ProtectedAttributeInfo(
                attribute_name=attribute_name,
                attribute_type=attr_type,
                unique_values=unique_values,
                value_counts=value_counts,
                missing_count=missing_count,
                bias_risk_level=bias_risk,
                legal_protection=legal_protection,
                description=f"Protected attribute: {attribute_name}",
                metadata={"analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")}
            )
            
        except Exception as e:
            self.logger.error(f"Protected attribute analysis failed: {e}")
            return None
    
    def _assess_bias_risk(self, series: pd.Series) -> str:
        """Assess bias risk level for an attribute."""
        try:
            # Check for imbalanced distribution
            if series.nunique() == 2:
                value_counts = series.value_counts()
                min_count = value_counts.min()
                max_count = value_counts.max()
                imbalance_ratio = min_count / max_count
                
                if imbalance_ratio < 0.1:
                    return "high"
                elif imbalance_ratio < 0.3:
                    return "medium"
                else:
                    return "low"
            
            # Check for high cardinality (potential ID leakage)
            if series.nunique() > len(series) * 0.8:
                return "high"
            
            return "low"
            
        except Exception as e:
            return "unknown"
    
    def _check_legal_protection(self, attribute_name: str) -> bool:
        """Check if attribute has legal protection status."""
        legally_protected = [
            'gender', 'sex', 'race', 'ethnicity', 'age', 'religion',
            'disability', 'marital_status', 'nationality', 'sexual_orientation'
        ]
        
        return any(protected in attribute_name.lower() for protected in legally_protected)
    
    def _generate_dataset_id(self, dataset_name: str) -> str:
        """Generate unique dataset ID."""
        timestamp = str(int(time.time()))
        name_hash = hashlib.md5(dataset_name.encode()).hexdigest()[:8]
        return f"dataset_{name_hash}_{timestamp}"
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file."""
        try:
            import hashlib
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Failed to calculate file hash: {e}")
            return ""
    
    def _save_processed_dataset(self, df: pd.DataFrame, dataset_id: str):
        """Save processed dataset."""
        try:
            processed_path = os.path.join(self.config.processed_directory, f"{dataset_id}.parquet")
            df.to_parquet(processed_path, index=False)
            self.logger.info(f"Processed dataset saved: {processed_path}")
        except Exception as e:
            self.logger.error(f"Failed to save processed dataset: {e}")
    
    def _save_metadata(self, metadata: DatasetMetadata):
        """Save dataset metadata."""
        try:
            metadata_path = os.path.join(self.config.metadata_directory, f"{metadata.dataset_id}.json")
            with open(metadata_path, 'w') as f:
                json.dump(asdict(metadata), f, indent=2)
            self.logger.info(f"Metadata saved: {metadata_path}")
        except Exception as e:
            self.logger.error(f"Failed to save metadata: {e}")
    
    def get_dataset_metadata(self, dataset_id: str) -> Optional[DatasetMetadata]:
        """Retrieve dataset metadata by ID."""
        try:
            metadata_path = os.path.join(self.config.metadata_directory, f"{dataset_id}.json")
            if not os.path.exists(metadata_path):
                return None
            
            with open(metadata_path, 'r') as f:
                data = json.load(f)
            
            return DatasetMetadata(**data)
        except Exception as e:
            self.logger.error(f"Failed to get dataset metadata: {e}")
            return None
    
    def list_datasets(self) -> List[DatasetMetadata]:
        """List all processed datasets."""
        try:
            datasets = []
            for filename in os.listdir(self.config.metadata_directory):
                if filename.endswith('.json'):
                    dataset_id = filename[:-5]  # Remove .json extension
                    metadata = self.get_dataset_metadata(dataset_id)
                    if metadata:
                        datasets.append(metadata)
            
            return sorted(datasets, key=lambda x: x.upload_date, reverse=True)
        except Exception as e:
            self.logger.error(f"Failed to list datasets: {e}")
            return []


def main():
    """Test the dataset processing system."""
    print("🧪 Testing Dataset Processing System")
    
    # Test configuration
    config = DatasetProcessingConfig()
    processor = DatasetProcessor(config)
    
    # Test metadata creation
    metadata = DatasetMetadata(
        dataset_id="test_dataset_001",
        name="Test Dataset",
        file_path="test.csv",
        file_size=1024,
        file_hash="test_hash",
        upload_date="2025-01-01",
        total_rows=1000,
        total_columns=10,
        feature_columns=["feature1", "feature2"],
        target_column="target",
        protected_attributes=["gender", "age"],
        data_types={},
        missing_values={},
        unique_values={},
        data_quality_score=0.9,
        bias_analysis_ready=True,
        metadata={}
    )
    
    print("✅ Dataset metadata created")
    print(f"✅ Dataset ID: {metadata.dataset_id}")
    print(f"✅ Protected attributes: {metadata.protected_attributes}")
    print(f"✅ Bias analysis ready: {metadata.bias_analysis_ready}")
    
    # Test dataset listing
    datasets = processor.list_datasets()
    print(f"✅ Found {len(datasets)} datasets in storage")


if __name__ == "__main__":
    main()
