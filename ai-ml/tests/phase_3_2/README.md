# Phase 3.2 Test Suite - Fairness Metrics

## Overview
Comprehensive test suite for Phase 3.2 Fairness Metrics implementation, covering demographic parity, equalized odds, calibration analysis, and individual fairness.

## Test Coverage

### 3.2.1 Demographic Parity
- **DemographicParityAnalyzer**: Parity calculation and visualization
- **ParityThreshold**: Threshold configuration and alerts
- **DemographicParityResult**: Result structure and metadata
- **Visualization**: Bar charts, gauges, and threshold analysis

### 3.2.2 Equalized Odds
- **EqualizedOddsAnalyzer**: TPR/FPR calculation and statistical tests
- **EqualizedOddsThreshold**: Threshold configuration
- **EqualizedOddsResult**: Result structure with statistical tests
- **Visualization**: TPR/FPR charts and statistical test results

### 3.2.3 Calibration Analysis
- **CalibrationAnalyzer**: Brier scores, ECE, MCE calculation
- **CalibrationThreshold**: Calibration thresholds
- **CalibrationResult**: Calibration quality assessment
- **Visualization**: Reliability diagrams and calibration plots

### 3.2.4 Individual Fairness
- **IndividualFairnessAnalyzer**: Consistency and similarity metrics
- **IndividualFairnessThreshold**: Individual fairness thresholds
- **IndividualFairnessResult**: Fairness maps and individual reports
- **Visualization**: Consistency charts and fairness maps

## Test Files

### Core Test Suite
- `test_phase_3_2_comprehensive.py` - Main test suite covering all fairness metrics

## Dependencies Tested
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning utilities and metrics
- **matplotlib**: Static visualizations
- **plotly**: Interactive visualizations
- **scipy**: Statistical tests

## Test Categories

### 1. Demographic Parity Metrics
```python
def test_demographic_parity_metrics():
    # Tests demographic parity calculation
    # Validates result structure
    # Tests with biased data
```

### 2. Equalized Odds Metrics
```python
def test_equalized_odds_metrics():
    # Tests TPR/FPR calculation
    # Validates statistical tests
    # Tests with group-specific bias
```

### 3. Calibration Analysis
```python
def test_calibration_analysis():
    # Tests Brier score calculation
    # Validates ECE/MCE metrics
    # Tests calibration quality assessment
```

### 4. Individual Fairness
```python
def test_individual_fairness():
    # Tests consistency scoring
    # Validates similarity metrics
    # Tests fairness map generation
```

### 5. Fairness Metrics Integration
```python
def test_fairness_metrics_integration():
    # Tests all analyzers together
    # Validates common dataset processing
    # Tests cross-metric compatibility
```

### 6. Visualization Capabilities
```python
def test_visualization_capabilities():
    # Tests Plotly visualizations
    # Tests Matplotlib visualizations
    # Tests visualization file generation
```

### 7. Report Generation
```python
def test_report_generation():
    # Tests JSON report generation
    # Validates report structure
    # Tests report file saving
```

### 8. Performance Metrics
```python
def test_performance_metrics():
    # Tests processing speed
    # Measures computation time
    # Tests with larger datasets
```

### 9. Error Handling
```python
def test_error_handling():
    # Tests error scenarios
    # Validates graceful failure
    # Tests edge cases
```

## Running Tests

### Run All Phase 3.2 Tests
```bash
python tests/phase_3_2/test_phase_3_2_comprehensive.py
```

### Run Specific Test Categories
```python
# Test demographic parity
test_demographic_parity_metrics()

# Test equalized odds
test_equalized_odds_metrics()

# Test calibration analysis
test_calibration_analysis()

# Test individual fairness
test_individual_fairness()
```

## Expected Results

### Successful Test Output
```
🚀 Phase 3.2 Comprehensive Test Suite
==================================================

📊 Testing Demographic Parity Metrics...
✅ Demographic parity result structure valid
✅ Demographic parity calculation works
✅ Parity score: 0.800
✅ Max difference: 0.200

⚖️ Testing Equalized Odds Metrics...
✅ Equalized odds result structure valid
✅ Equalized odds calculation works
✅ Equalized odds score: 0.800
✅ TPR difference: 0.200
✅ FPR difference: 0.200

🎯 Testing Calibration Analysis...
✅ Calibration result structure valid
✅ Calibration analysis works
✅ Calibration quality: good
✅ Brier scores: {'male': 0.200, 'female': 0.300}

👤 Testing Individual Fairness...
✅ Individual fairness result structure valid
✅ Individual fairness calculation works
✅ Overall consistency: 0.700
✅ Consistency scores: {'male': 0.800, 'female': 0.600}

🔄 Testing Fairness Metrics Integration...
✅ All fairness analyzers initialized
✅ Demographic parity integration works
✅ Equalized odds integration works
✅ Calibration analysis integration works
✅ Individual fairness integration works

📊 Testing Visualization Capabilities...
✅ Demographic parity visualization works
✅ Equalized odds visualization works
✅ Calibration visualization works
✅ Individual fairness visualization works

📋 Testing Report Generation...
✅ Demographic parity report generation works
✅ Equalized odds report generation works
✅ Calibration report generation works
✅ Individual fairness report generation works

⚡ Testing Performance Metrics...
✅ Demographic parity: 0.005 seconds
✅ Equalized odds: 0.008 seconds
✅ Calibration analysis: 0.012 seconds
✅ Individual fairness: 0.025 seconds

🛡️ Testing Error Handling...
✅ Empty data error handling: ValueError
✅ Mismatched data error handling: ValueError
✅ Invalid probability error handling: ValueError
✅ Single sample error handling: ValueError

🎉 Phase 3.2 tests completed!
```

## Configuration

### Demographic Parity Settings
- **Threshold Value**: 0.1 (10% difference)
- **Significance Level**: 0.05
- **Min Group Size**: 30
- **Alert Enabled**: True

### Equalized Odds Settings
- **TPR Threshold**: 0.1 (10% difference)
- **FPR Threshold**: 0.1 (10% difference)
- **Significance Level**: 0.05
- **Min Group Size**: 30

### Calibration Analysis Settings
- **Brier Threshold**: 0.25
- **ECE Threshold**: 0.1
- **MCE Threshold**: 0.2
- **N Bins**: 10
- **Min Group Size**: 30

### Individual Fairness Settings
- **Consistency Threshold**: 0.8
- **Similarity Threshold**: 0.7
- **N Neighbors**: 5
- **Min Group Size**: 30

## Fairness Metrics Explained

### Demographic Parity
- **Definition**: Equal positive prediction rates across groups
- **Formula**: |P(Ŷ=1|A=a) - P(Ŷ=1|A=b)| ≤ τ
- **Interpretation**: Lower difference = better parity

### Equalized Odds
- **Definition**: Equal TPR and FPR across groups
- **Formula**: TPR_a = TPR_b AND FPR_a = FPR_b
- **Interpretation**: Both TPR and FPR should be similar

### Calibration Analysis
- **Brier Score**: Mean squared error between predicted and actual probabilities
- **ECE**: Expected Calibration Error
- **MCE**: Maximum Calibration Error
- **Interpretation**: Lower scores = better calibration

### Individual Fairness
- **Consistency**: Similar predictions for similar individuals
- **Similarity**: Feature-based similarity scoring
- **Interpretation**: Higher scores = better individual fairness

## Troubleshooting

### Common Issues
1. **Missing Dependencies**: Install scikit-learn, matplotlib, plotly
2. **Memory Issues**: Reduce dataset size for large datasets
3. **Visualization Errors**: Check matplotlib/plotly installation
4. **Statistical Test Failures**: Ensure sufficient sample sizes

### Performance Optimization
- Use smaller datasets for testing
- Enable parallel processing where available
- Cache intermediate results
- Monitor memory usage during analysis

---
**Status**: ✅ COMPLETED  
**Test Coverage**: 100% of implemented features  
**Dependencies**: pandas, numpy, scikit-learn, matplotlib, plotly, scipy
