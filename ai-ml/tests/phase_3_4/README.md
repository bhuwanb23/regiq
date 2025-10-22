# Phase 3.4: Bias Scoring System - Tests

## Overview
Comprehensive test suite for the bias scoring system (Phase 3.4).

## Test Structure

### Unit Tests
- `test_scoring_algorithm.py` - Core scoring algorithm tests
- `test_composite_calculator.py` - Composite score calculation tests
- `test_score_interpreter.py` - Score interpretation tests
- `test_classification_engine.py` - Risk classification tests
- `test_alert_system.py` - Alert management tests
- `test_report_generator.py` - Report generation tests

### Integration Tests
- `test_phase_3_4_comprehensive.py` - Full pipeline integration test
- Tests integration with Phase 3.2 fairness metrics

## Running Tests

### Run all Phase 3.4 tests
```bash
cd ai-ml
pytest tests/phase_3_4/ -v
```

### Run specific test file
```bash
pytest tests/phase_3_4/test_composite_calculator.py -v
```

### Run with coverage
```bash
pytest tests/phase_3_4/ --cov=services.bias_analysis.scoring --cov-report=html
```

### Run fast tests only (skip LLM tests)
```bash
pytest tests/phase_3_4/ -m "not llm" -v
```

## Test Coverage Goals
- **Overall Coverage**: >85%
- **Critical Paths**: >95%
- **Performance**: Score calculation <500ms, Report generation <2s

## Dependencies
- Phase 3.2 fairness metrics (demographic_parity, equalized_odds, calibration_analysis, individual_fairness)
- Gemini LLM API (optional, graceful fallback)

## Test Data
Test datasets with controlled bias levels are included for validation.
