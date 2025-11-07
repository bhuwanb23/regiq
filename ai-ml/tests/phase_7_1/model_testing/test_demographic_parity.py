"""Unit tests for demographic parity metrics"""

import sys
import os
from pathlib import Path
import numpy as np

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

import pytest
from services.bias_analysis.metrics.demographic_parity import (
    DemographicParityAnalyzer,
    DemographicParityResult,
    ParityThreshold
)

def test_demographic_parity_analyzer_initialization():
    """Test that DemographicParityAnalyzer can be initialized."""
    # Test with default config
    analyzer = DemographicParityAnalyzer()
    assert analyzer is not None
    assert analyzer.threshold is not None
    
    # Test with custom config
    config = ParityThreshold(threshold_value=0.15, min_group_size=20)
    analyzer = DemographicParityAnalyzer(threshold_config=config)
    assert analyzer.threshold.threshold_value == 0.15
    assert analyzer.threshold.min_group_size == 20

def test_calculate_demographic_parity():
    """Test demographic parity calculation with sample data."""
    # Use a lower threshold for testing
    config = ParityThreshold(min_group_size=5)
    analyzer = DemographicParityAnalyzer(threshold_config=config)
    
    # Create sample data
    # Protected attribute: gender (0 = male, 1 = female)
    protected_attribute = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    # Predictions (0 = negative, 1 = positive)
    y_pred = np.array([1, 1, 0, 1, 0, 0, 0, 1, 0, 0])
    # True labels (not used in demographic parity but required by function signature)
    y_true = np.array([1, 1, 0, 1, 0, 0, 0, 1, 0, 0])
    
    # Calculate demographic parity
    result = analyzer.calculate_demographic_parity(y_true, y_pred, protected_attribute)
    
    # Verify result structure
    assert isinstance(result, DemographicParityResult)
    assert result.metric_name == "Demographic Parity"
    assert len(result.groups) == 2
    assert "0" in result.positive_rates
    assert "1" in result.positive_rates
    assert 0 <= result.parity_score <= 1
    assert result.max_difference >= 0

def test_demographic_parity_with_bias():
    """Test demographic parity calculation with clear bias."""
    analyzer = DemographicParityAnalyzer()
    
    # Create sample data with clear bias
    # Protected attribute: gender (0 = male, 1 = female)
    protected_attribute = np.array([0] * 100 + [1] * 100)  # 100 males, 100 females
    # Predictions: males mostly positive, females mostly negative
    y_pred = np.array([1] * 80 + [0] * 20 + [1] * 20 + [0] * 80)  # 80% positive for males, 20% for females
    y_true = np.array([1] * 80 + [0] * 20 + [1] * 20 + [0] * 80)
    
    # Calculate demographic parity
    result = analyzer.calculate_demographic_parity(y_true, y_pred, protected_attribute)
    
    # Verify bias detection
    assert result.max_difference > 0.5  # Large difference indicates bias
    assert result.threshold_violation == True  # Should exceed default threshold

def test_demographic_parity_no_bias():
    """Test demographic parity calculation with no bias."""
    analyzer = DemographicParityAnalyzer()
    
    # Create sample data with no bias
    # Protected attribute: gender (0 = male, 1 = female)
    protected_attribute = np.array([0] * 100 + [1] * 100)  # 100 males, 100 females
    # Predictions: equal positive rates for both groups
    y_pred = np.array([1] * 50 + [0] * 50 + [1] * 50 + [0] * 50)  # 50% positive for both groups
    y_true = np.array([1] * 50 + [0] * 50 + [1] * 50 + [0] * 50)
    
    # Calculate demographic parity
    result = analyzer.calculate_demographic_parity(y_true, y_pred, protected_attribute)
    
    # Verify no bias detected
    assert result.max_difference < 0.1  # Small difference indicates no bias
    assert result.threshold_violation == False  # Should not exceed default threshold

if __name__ == "__main__":
    pytest.main([__file__, "-v"])