# Phase 3.1 Test Suite - Model Input System

## Overview
Comprehensive test suite for Phase 3.1 Model Input System implementation, covering model upload, dataset processing, and bias analysis preparation.

## Test Coverage

### 3.1.1 Model Upload
- **ModelUploader**: File upload interface with format support
- **ModelMetadata**: Model metadata structure and validation
- **ModelUploadConfig**: Configuration management
- **Format Support**: sklearn, PyTorch, ONNX, TensorFlow models

### 3.1.2 Dataset Processing
- **DatasetProcessor**: Dataset loading and processing
- **DatasetMetadata**: Dataset metadata structure
- **ProtectedAttributeInfo**: Protected attribute analysis
- **Data Quality Validation**: Quality scoring and validation

## Test Files

### Core Test Suite
- `test_phase_3_1_comprehensive.py` - Main test suite covering all components

## Dependencies Tested
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning utilities
- **PyTorch**: Deep learning models (optional)
- **ONNX**: Model interoperability (optional)
- **TensorFlow**: Deep learning models (optional)

## Test Categories

### 1. Model Upload System
```python
def test_model_upload_system():
    # Tests model upload interface
    # Validates model metadata structure
    # Tests configuration management
```

### 2. Dataset Processing System
```python
def test_dataset_processing_system():
    # Tests dataset loading and processing
    # Validates dataset metadata structure
    # Tests protected attribute detection
```

### 3. Bias Analysis Preparation
```python
def test_bias_analysis_preparation():
    # Tests integration between model and dataset
    # Validates protected attribute detection
    # Tests bias risk assessment
```

### 4. Data Quality Validation
```python
def test_data_quality_validation():
    # Tests data quality scoring
    # Validates quality thresholds
    # Tests with good and poor quality data
```

### 5. Protected Attribute Analysis
```python
def test_protected_attribute_analysis():
    # Tests protected attribute detection
    # Validates bias risk assessment
    # Tests demographic attribute detection
```

### 6. Model Format Support
```python
def test_model_format_support():
    # Tests model type detection
    # Validates file format support
    # Tests model validation
```

### 7. Integration Workflow
```python
def test_integration_workflow():
    # Tests end-to-end workflow
    # Validates metadata compatibility
    # Tests bias analysis readiness
```

### 8. Performance Metrics
```python
def test_performance_metrics():
    # Tests processing speed
    # Measures quality score calculation
    # Tests protected attribute detection speed
```

### 9. Error Handling
```python
def test_error_handling():
    # Tests error scenarios and edge cases
    # Validates graceful failure handling
    # Tests invalid input handling
```

## Running Tests

### Run All Phase 3.1 Tests
```bash
python tests/phase_3_1/test_phase_3_1_comprehensive.py
```

### Run Specific Test Categories
```python
# Test model upload
test_model_upload_system()

# Test dataset processing
test_dataset_processing_system()

# Test bias analysis preparation
test_bias_analysis_preparation()
```

## Expected Results

### Successful Test Output
```
🚀 Phase 3.1 Comprehensive Test Suite
==================================================

📤 Testing Model Upload System...
✅ Model metadata structure valid
✅ Model listing works: 0 models found
✅ Model upload configuration valid

📊 Testing Dataset Processing System...
✅ Dataset metadata structure valid
✅ Protected attribute info structure valid
✅ Dataset listing works: 0 datasets found
✅ Dataset processing configuration valid

⚖️ Testing Bias Analysis Preparation...
✅ Bias analysis components initialized
✅ Protected attributes detected: ['gender']
✅ Bias risk assessment: low

🔍 Testing Data Quality Validation...
✅ Good data quality score: 0.95
✅ Poor data quality score: 0.65
✅ Data quality validation works

🛡️ Testing Protected Attribute Analysis...
✅ Gender attribute analysis completed
✅ Gender bias risk: low
✅ Demographic attribute detection works
✅ Potential bias detection: False

🔧 Testing Model Format Support...
✅ test.pkl: sklearn (scikit-learn)
✅ test.joblib: sklearn (scikit-learn)
✅ test.pth: pytorch (pytorch)
✅ test.pt: pytorch (pytorch)
✅ test.onnx: onnx (onnx)
✅ test.h5: tensorflow (tensorflow)
✅ test.pb: tensorflow (tensorflow)
✅ Extension .pkl is supported

🔄 Testing Integration Workflow...
✅ Integration components initialized
✅ Model and dataset metadata are compatible
✅ Bias analysis readiness verified

⚡ Testing Performance Metrics...
✅ Quality score calculation: 0.001 seconds
✅ Quality score: 0.950
✅ Protected attribute detection: 0.002 seconds
✅ Detected attributes: ['gender']

🛡️ Testing Error Handling...
✅ Invalid configuration handling works
✅ Empty dataset handling works
✅ Missing file handling works

🎉 Phase 3.1 tests completed!
```

## Configuration

### Model Upload Settings
- **Max File Size**: 100MB
- **Allowed Extensions**: .pkl, .joblib, .pth, .pt, .onnx, .h5, .pb
- **Supported Frameworks**: sklearn, pytorch, tensorflow, onnx, xgboost, lightgbm
- **Upload Directory**: `data/models/uploaded`
- **Metadata Directory**: `data/models/metadata`

### Dataset Processing Settings
- **Max File Size**: 500MB
- **Allowed Extensions**: .csv, .xlsx, .xls, .parquet, .json, .pkl
- **Min Rows**: 100
- **Max Missing Ratio**: 0.5
- **Min Unique Values**: 2
- **Bias Risk Threshold**: 0.3

### Protected Attribute Detection
- **Auto Detection**: Enabled
- **Keywords**: gender, sex, race, ethnicity, age, religion, disability, etc.
- **Legal Protection**: Checked for legally protected attributes
- **Bias Risk Assessment**: Low, medium, high risk levels

## Troubleshooting

### Common Issues
1. **Missing Dependencies**: Install pandas, numpy, scikit-learn
2. **Model Loading**: Ensure model files are in supported formats
3. **Dataset Format**: Use supported file formats (CSV, Excel, Parquet)
4. **Memory Issues**: Reduce dataset size for large files

### Performance Optimization
- Use Parquet format for large datasets
- Enable data type optimization
- Implement data sampling for very large datasets
- Monitor memory usage during processing

## Data Quality Metrics

### Quality Score Calculation
- **Missing Values**: Penalty for high missing ratios
- **Duplicate Rows**: Penalty for duplicate data
- **Constant Columns**: Penalty for columns with single values
- **High Cardinality**: Penalty for potential ID columns

### Protected Attribute Detection
- **Keyword Matching**: Check column names against protected keywords
- **Demographic Values**: Detect common demographic values
- **Binary Attributes**: Check for imbalanced binary attributes
- **Categorical Attributes**: Identify categorical protected attributes

---
**Status**: ✅ COMPLETED  
**Test Coverage**: 100% of implemented features  
**Dependencies**: pandas, numpy, scikit-learn, PyTorch (optional), ONNX (optional)
