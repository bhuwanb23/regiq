# Phase 3.3 Test Suite - Explainability Tools

This directory contains comprehensive tests for Phase 3.3 Explainability Tools implementation.

## 📁 Test Files

### Core Test Files
- `test_phase_3_3_comprehensive.py` - Full comprehensive test suite
- `test_phase_3_3_fast.py` - Quick test suite for development

## 🧪 Test Coverage

### SHAP Integration Tests
- ✅ SHAP explainer creation
- ✅ Model type detection
- ✅ Explanation generation
- ✅ Feature importance calculation
- ✅ Visualization creation
- ✅ Report generation

### LIME Implementation Tests
- ✅ LIME tabular explainer
- ✅ Local explanation generation
- ✅ Feature importance analysis
- ✅ Visualization creation
- ✅ Report generation

### Feature Attribution Tests
- ✅ Feature importance calculation
- ✅ Multiple attribution methods
- ✅ Feature ranking
- ✅ Attribution charts
- ✅ Explanation summaries

### Integration Tests
- ✅ Cross-tool compatibility
- ✅ Performance testing
- ✅ Error handling
- ✅ Configuration management

## 🚀 Running Tests

### Fast Tests (Development)
```bash
# Run quick tests
python tests/phase_3_3/test_phase_3_3_fast.py
```

### Comprehensive Tests (Full Validation)
```bash
# Run full test suite
python tests/phase_3_3/test_phase_3_3_comprehensive.py
```

### All Phase 3.3 Tests
```bash
# Run all explainability tests
python -m pytest tests/phase_3_3/ -v
```

## 📋 Test Requirements

### Dependencies
- `shap` - SHAP explainer library
- `lime` - LIME explainer library
- `scikit-learn` - Machine learning models
- `matplotlib` - Visualization (optional)
- `plotly` - Interactive visualization (optional)

### Installation
```bash
# Install required dependencies
pip install shap lime scikit-learn matplotlib plotly
```

## 🔍 Test Scenarios

### 1. SHAP Integration
- **Model Types**: Tree, Linear, Kernel, Deep
- **Data Types**: Tabular, Text, Image
- **Visualizations**: Bar charts, Waterfall plots, Summary plots
- **Reports**: JSON, HTML, Markdown

### 2. LIME Implementation
- **Explainer Types**: Tabular, Text, Image
- **Explanation Types**: Local, Global
- **Visualizations**: Feature importance, Local explanations
- **Reports**: Detailed explanations, Confidence scores

### 3. Feature Attribution
- **Methods**: Built-in, Permutation, Correlation
- **Ranking**: Importance-based, Statistical significance
- **Visualizations**: Attribution charts, Comparison plots
- **Reports**: Comprehensive analysis, Method comparison

## 📊 Expected Results

### Fast Tests
- **Duration**: < 30 seconds
- **Coverage**: Basic functionality
- **Dependencies**: Minimal requirements

### Comprehensive Tests
- **Duration**: 2-5 minutes
- **Coverage**: Full functionality
- **Dependencies**: All libraries

## 🐛 Troubleshooting

### Common Issues

1. **SHAP Import Error**
   ```bash
   pip install shap
   ```

2. **LIME Import Error**
   ```bash
   pip install lime
   ```

3. **Visualization Errors**
   ```bash
   pip install matplotlib plotly
   ```

4. **Memory Issues**
   - Reduce `max_samples` in configuration
   - Use smaller datasets for testing

### Performance Optimization

1. **SHAP Performance**
   - Use `TreeExplainer` for tree-based models
   - Reduce `background_samples` for faster execution
   - Use `max_samples` to limit data size

2. **LIME Performance**
   - Reduce `num_samples` for faster execution
   - Use `num_features` to limit explanation complexity
   - Cache explainers for repeated use

3. **Feature Attribution Performance**
   - Reduce `n_permutations` for faster execution
   - Use `top_k` to limit feature analysis
   - Cache results for repeated analysis

## 📈 Test Metrics

### Success Criteria
- ✅ All imports successful
- ✅ Basic functionality working
- ✅ Visualizations generated
- ✅ Reports created
- ✅ Error handling working

### Performance Benchmarks
- **SHAP**: < 10 seconds for 100 samples
- **LIME**: < 5 seconds for single instance
- **Feature Attribution**: < 15 seconds for 100 samples

## 🔧 Configuration

### Test Configuration
```python
# SHAP Configuration
SHAPConfig(
    max_samples=100,
    background_samples=50,
    max_display=10
)

# LIME Configuration
LIMEConfig(
    num_features=5,
    num_samples=1000,
    random_state=42
)

# Attribution Configuration
AttributionConfig(
    n_permutations=10,
    top_k=5,
    random_state=42
)
```

## 📝 Test Reports

### Generated Reports
- **SHAP Reports**: JSON format with explanations
- **LIME Reports**: JSON format with local explanations
- **Attribution Reports**: JSON format with feature rankings

### Report Locations
- `data/reports/shap/` - SHAP analysis reports
- `data/reports/lime/` - LIME analysis reports
- `data/reports/attribution/` - Feature attribution reports

## 🎯 Next Steps

After successful testing:
1. ✅ Verify all explainability tools working
2. ✅ Test with real model data
3. ✅ Validate visualization outputs
4. ✅ Check report generation
5. ✅ Move to Phase 3.4 implementation

## 📞 Support

For issues with Phase 3.3 tests:
1. Check dependency installation
2. Verify configuration settings
3. Review error messages
4. Test with minimal data
5. Check memory usage
