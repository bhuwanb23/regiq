#!/usr/bin/env python3
"""
REGIQ AI/ML - Data Processor
Utilities for handling and processing datasets for bias mitigation.
"""

import logging
import numpy as np
import pandas as pd
from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass


logger = logging.getLogger("data_processor")


@dataclass
class DatasetStatistics:
    """Statistics about a dataset."""
    n_samples: int
    n_features: int
    n_classes: int
    class_distribution: Dict[Any, int]
    group_distribution: Dict[Any, int]
    group_class_distribution: Dict[Tuple[Any, Any], int]


class DataProcessor:
    """
    Utility class for data processing operations.
    
    Provides:
    - Data validation
    - Train/test splitting with stratification
    - Group statistics calculation
    - Data format conversion
    """
    
    def __init__(self):
        """Initialize data processor."""
        self.logger = logger
    
    def validate_data(self, X: np.ndarray, y: np.ndarray, 
                     protected_attr: np.ndarray) -> Tuple[bool, List[str]]:
        """
        Validate dataset for bias mitigation.
        
        Args:
            X: Features
            y: Labels
            protected_attr: Protected attribute values
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check shapes
        if len(X) != len(y):
            errors.append(f"X and y have different lengths: {len(X)} vs {len(y)}")
        
        if len(y) != len(protected_attr):
            errors.append(f"y and protected_attr have different lengths: {len(y)} vs {len(protected_attr)}")
        
        # Check for NaN values
        if np.isnan(X).any():
            errors.append("X contains NaN values")
        
        if np.isnan(y).any():
            errors.append("y contains NaN values")
        
        # Check minimum samples per group
        unique_groups, group_counts = np.unique(protected_attr, return_counts=True)
        for group, count in zip(unique_groups, group_counts):
            if count < 10:
                errors.append(f"Group '{group}' has only {count} samples (minimum 10 recommended)")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def calculate_statistics(self, X: np.ndarray, y: np.ndarray,
                            protected_attr: np.ndarray) -> DatasetStatistics:
        """
        Calculate dataset statistics.
        
        Args:
            X: Features
            y: Labels
            protected_attr: Protected attribute values
            
        Returns:
            DatasetStatistics object
        """
        try:
            n_samples = len(X)
            n_features = X.shape[1] if len(X.shape) > 1 else 1
            
            # Class distribution
            unique_classes, class_counts = np.unique(y, return_counts=True)
            n_classes = len(unique_classes)
            class_distribution = dict(zip(unique_classes, class_counts.tolist()))
            
            # Group distribution
            unique_groups, group_counts = np.unique(protected_attr, return_counts=True)
            group_distribution = dict(zip(unique_groups, group_counts.tolist()))
            
            # Group-class distribution
            group_class_distribution = {}
            for group in unique_groups:
                group_mask = protected_attr == group
                group_y = y[group_mask]
                unique_classes_in_group, counts = np.unique(group_y, return_counts=True)
                for cls, count in zip(unique_classes_in_group, counts):
                    group_class_distribution[(group, cls)] = int(count)
            
            return DatasetStatistics(
                n_samples=n_samples,
                n_features=n_features,
                n_classes=n_classes,
                class_distribution=class_distribution,
                group_distribution=group_distribution,
                group_class_distribution=group_class_distribution
            )
            
        except Exception as e:
            self.logger.error(f"Statistics calculation failed: {e}")
            raise
    
    def split_by_groups(self, X: np.ndarray, y: np.ndarray,
                       protected_attr: np.ndarray) -> Dict[Any, Tuple[np.ndarray, np.ndarray]]:
        """
        Split dataset by protected groups.
        
        Args:
            X: Features
            y: Labels
            protected_attr: Protected attribute values
            
        Returns:
            Dictionary mapping group -> (X_group, y_group)
        """
        groups = {}
        unique_groups = np.unique(protected_attr)
        
        for group in unique_groups:
            group_mask = protected_attr == group
            groups[group] = (X[group_mask], y[group_mask])
        
        return groups
    
    def merge_groups(self, group_data: Dict[Any, Tuple[np.ndarray, np.ndarray]],
                    protected_attr_values: Dict[Any, Any]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Merge group-separated data back into unified dataset.
        
        Args:
            group_data: Dictionary mapping group -> (X_group, y_group)
            protected_attr_values: Dictionary mapping group -> protected_attr_value
            
        Returns:
            Tuple of (X, y, protected_attr)
        """
        X_list = []
        y_list = []
        attr_list = []
        
        for group, (X_group, y_group) in group_data.items():
            X_list.append(X_group)
            y_list.append(y_group)
            attr_value = protected_attr_values.get(group, group)
            attr_list.append(np.full(len(X_group), attr_value))
        
        X = np.vstack(X_list)
        y = np.concatenate(y_list)
        protected_attr = np.concatenate(attr_list)
        
        return X, y, protected_attr
    
    def to_dataframe(self, X: np.ndarray, y: np.ndarray,
                    protected_attr: np.ndarray,
                    feature_names: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Convert arrays to pandas DataFrame.
        
        Args:
            X: Features
            y: Labels
            protected_attr: Protected attribute values
            feature_names: Optional feature names
            
        Returns:
            DataFrame with features, label, and protected attribute
        """
        if feature_names is None:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        df = pd.DataFrame(X, columns=feature_names)
        df['target'] = y
        df['protected_attribute'] = protected_attr
        
        return df
    
    def from_dataframe(self, df: pd.DataFrame,
                      target_col: str = 'target',
                      protected_col: str = 'protected_attribute') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Convert DataFrame to arrays.
        
        Args:
            df: DataFrame
            target_col: Name of target column
            protected_col: Name of protected attribute column
            
        Returns:
            Tuple of (X, y, protected_attr)
        """
        feature_cols = [col for col in df.columns if col not in [target_col, protected_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        protected_attr = df[protected_col].values
        
        return X, y, protected_attr


def main():
    """Test the data processor."""
    print("🧪 Testing Data Processor")
    
    # Create test data
    np.random.seed(42)
    n_samples = 1000
    n_features = 20
    
    X = np.random.randn(n_samples, n_features)
    y = np.random.binomial(1, 0.5, n_samples)
    protected_attr = np.random.choice(['A', 'B'], n_samples, p=[0.6, 0.4])
    
    processor = DataProcessor()
    
    # Test validation
    is_valid, errors = processor.validate_data(X, y, protected_attr)
    print(f"✅ Data validation: {is_valid}, Errors: {errors}")
    
    # Test statistics
    stats = processor.calculate_statistics(X, y, protected_attr)
    print(f"✅ Statistics: {stats.n_samples} samples, {stats.n_features} features, {stats.n_classes} classes")
    print(f"✅ Class distribution: {stats.class_distribution}")
    print(f"✅ Group distribution: {stats.group_distribution}")
    
    # Test split by groups
    groups = processor.split_by_groups(X, y, protected_attr)
    print(f"✅ Split into {len(groups)} groups")
    for group, (X_g, y_g) in groups.items():
        print(f"   Group {group}: {len(X_g)} samples")
    
    # Test merge
    X_merged, y_merged, attr_merged = processor.merge_groups(groups, {'A': 'A', 'B': 'B'})
    print(f"✅ Merged back: {len(X_merged)} samples")
    
    # Test DataFrame conversion
    df = processor.to_dataframe(X[:10], y[:10], protected_attr[:10])
    print(f"✅ DataFrame shape: {df.shape}")
    
    X_back, y_back, attr_back = processor.from_dataframe(df)
    print(f"✅ Converted back: X shape {X_back.shape}, y shape {y_back.shape}")


if __name__ == "__main__":
    main()
