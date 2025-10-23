"""
Tests for Uncertainty Quantification Models

Test coverage:
- SensitivityAnalyzer (6 tests)
- ScenarioAnalyzer (3 tests)
- UncertaintyPropagator (4 tests)

Total: 13 tests
"""

import pytest
import numpy as np
from services.risk_simulator.models.uncertainty_quantification import (
    SensitivityAnalyzer,
    ScenarioAnalyzer,
    UncertaintyPropagator,
    SensitivityMethod,
    ScenarioType,
    SensitivityResult,
    ScenarioResult,
    UncertaintyResult
)


class TestSensitivityAnalyzer:
    """Test suite for SensitivityAnalyzer"""
    
    def test_initialization(self):
        """Test initialization"""
        analyzer = SensitivityAnalyzer(method=SensitivityMethod.SOBOL, random_state=42)
        assert analyzer.method == SensitivityMethod.SOBOL
        assert analyzer.random_state == 42
    
    def test_sobol_sensitivity(self):
        """Test Sobol sensitivity analysis"""
        analyzer = SensitivityAnalyzer(method=SensitivityMethod.SOBOL, random_state=42)
        
        def model_func(params):
            return params['x'] * 2 + params['y'] * 3
        
        parameters = {'x': (0.0, 10.0), 'y': (0.0, 5.0)}
        results = analyzer.analyze(model_func, parameters, n_samples=1000)
        
        assert len(results) == 2
        assert all(isinstance(r, SensitivityResult) for r in results)
        assert all(r.rank is not None for r in results)
    
    def test_morris_sensitivity(self):
        """Test Morris screening method"""
        analyzer = SensitivityAnalyzer(method=SensitivityMethod.MORRIS, random_state=42)
        
        def model_func(params):
            return params['a'] + params['b'] ** 2
        
        parameters = {'a': (1.0, 10.0), 'b': (1.0, 5.0)}
        results = analyzer.analyze(model_func, parameters, n_samples=100)
        
        assert len(results) == 2
        # Morris provides both mean and std measures
        assert results[0].total_sensitivity_index is not None
    
    def test_correlation_sensitivity(self):
        """Test correlation-based sensitivity"""
        analyzer = SensitivityAnalyzer(method=SensitivityMethod.CORRELATION, random_state=42)
        
        def model_func(params):
            return params['p1'] * 5 + params['p2'] * 0.1
        
        parameters = {'p1': (0.0, 100.0), 'p2': (0.0, 100.0)}
        results = analyzer.analyze(model_func, parameters, n_samples=1000)
        
        assert len(results) == 2
        # p1 should have higher sensitivity
        assert results[0].sensitivity_index > results[1].sensitivity_index
    
    def test_variance_based_sensitivity(self):
        """Test variance-based sensitivity"""
        analyzer = SensitivityAnalyzer(method=SensitivityMethod.VARIANCE_BASED, random_state=42)
        
        def model_func(params):
            return params['v1'] * 10 + params['v2']
        
        parameters = {'v1': (0.0, 10.0), 'v2': (0.0, 10.0)}
        results = analyzer.analyze(model_func, parameters, n_samples=500)
        
        assert len(results) == 2
        assert all(0 <= r.sensitivity_index <= 1 for r in results)
    
    def test_sensitivity_result_serialization(self):
        """Test SensitivityResult to_dict"""
        result = SensitivityResult(
            parameter_name='test_param',
            sensitivity_index=0.75,
            rank=1
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict['parameter_name'] == 'test_param'
        assert result_dict['sensitivity_index'] == 0.75


class TestScenarioAnalyzer:
    """Test suite for ScenarioAnalyzer"""
    
    def test_initialization(self):
        """Test initialization"""
        analyzer = ScenarioAnalyzer(random_state=42)
        assert analyzer.random_state == 42
    
    def test_analyze_scenarios(self):
        """Test scenario analysis"""
        analyzer = ScenarioAnalyzer(random_state=42)
        
        def model_func(params):
            return params['risk_factor'] * 1000
        
        parameters = {'risk_factor': (1.0, 10.0)}
        scenarios = analyzer.analyze_scenarios(model_func, parameters)
        
        assert len(scenarios) == 3  # Best, Expected, Worst
        assert any(s.scenario_type == 'best_case' for s in scenarios)
        assert any(s.scenario_type == 'expected' for s in scenarios)
        assert any(s.scenario_type == 'worst_case' for s in scenarios)
    
    def test_custom_scenarios(self):
        """Test with custom scenarios"""
        analyzer = ScenarioAnalyzer(random_state=42)
        
        def model_func(params):
            return params['value'] * 100
        
        parameters = {'value': (1.0, 10.0)}
        custom = [
            {'value': 3.0},
            {'value': 7.0}
        ]
        
        scenarios = analyzer.analyze_scenarios(model_func, parameters, custom_scenarios=custom)
        
        assert len(scenarios) == 5  # 3 default + 2 custom
        custom_scenarios = [s for s in scenarios if s.scenario_type == 'custom']
        assert len(custom_scenarios) == 2
    
    def test_scenario_result_serialization(self):
        """Test ScenarioResult to_dict"""
        result = ScenarioResult(
            scenario_type='best_case',
            risk_value=100.0,
            probability=0.1,
            parameter_values={'x': 1.0},
            description='Test scenario'
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        import json
        json.dumps(result_dict)  # Ensure JSON serializable


class TestUncertaintyPropagator:
    """Test suite for UncertaintyPropagator"""
    
    def test_initialization(self):
        """Test initialization"""
        propagator = UncertaintyPropagator(random_state=42)
        assert propagator.random_state == 42
    
    def test_propagate_normal_distribution(self):
        """Test uncertainty propagation with normal distribution"""
        propagator = UncertaintyPropagator(random_state=42)
        
        def model_func(params):
            return params['a'] + params['b']
        
        parameter_distributions = {
            'a': ('normal', {'mean': 10.0, 'std': 2.0}),
            'b': ('normal', {'mean': 5.0, 'std': 1.0})
        }
        
        result = propagator.propagate(model_func, parameter_distributions, n_simulations=1000)
        
        assert isinstance(result, UncertaintyResult)
        assert result.mean > 0
        assert result.std > 0
        assert 'p50' in result.percentiles
    
    def test_propagate_uniform_distribution(self):
        """Test with uniform distribution"""
        propagator = UncertaintyPropagator(random_state=42)
        
        def model_func(params):
            return params['x'] * 2
        
        parameter_distributions = {
            'x': ('uniform', {'min': 0.0, 'max': 10.0})
        }
        
        result = propagator.propagate(model_func, parameter_distributions, n_simulations=1000)
        
        assert result.mean > 0
        assert '90%' in result.confidence_bands
    
    def test_multiple_distribution_types(self):
        """Test with multiple distribution types"""
        propagator = UncertaintyPropagator(random_state=42)
        
        def model_func(params):
            return params['norm'] + params['unif'] + params['tri']
        
        parameter_distributions = {
            'norm': ('normal', {'mean': 10.0, 'std': 2.0}),
            'unif': ('uniform', {'min': 0.0, 'max': 5.0}),
            'tri': ('triangular', {'left': 0.0, 'mode': 2.0, 'right': 4.0})
        }
        
        result = propagator.propagate(model_func, parameter_distributions, n_simulations=1000)
        
        assert result.mean > 0
        assert result.skewness is not None
        assert result.kurtosis is not None
    
    def test_result_serialization(self):
        """Test UncertaintyResult to_dict"""
        propagator = UncertaintyPropagator(random_state=42)
        
        def model_func(params):
            return params['val']
        
        parameter_distributions = {
            'val': ('normal', {'mean': 100.0, 'std': 10.0})
        }
        
        result = propagator.propagate(model_func, parameter_distributions, n_simulations=500)
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'mean' in result_dict
        assert 'confidence_bands' in result_dict
        
        import json
        json.dumps(result_dict)


class TestUncertaintyIntegration:
    """Integration tests"""
    
    def test_complete_uncertainty_analysis(self):
        """Test complete uncertainty analysis workflow"""
        # Define model
        def risk_model(params):
            return (params['base_risk'] * params['multiplier'] + 
                   params['fixed_cost'])
        
        # Parameters
        parameters = {
            'base_risk': (100.0, 500.0),
            'multiplier': (1.0, 3.0),
            'fixed_cost': (50.0, 150.0)
        }
        
        # Sensitivity analysis
        sens_analyzer = SensitivityAnalyzer(
            method=SensitivityMethod.CORRELATION,
            random_state=42
        )
        sensitivity = sens_analyzer.analyze(risk_model, parameters, n_samples=500)
        
        # Scenario analysis
        scen_analyzer = ScenarioAnalyzer(random_state=42)
        scenarios = scen_analyzer.analyze_scenarios(risk_model, parameters)
        
        # Uncertainty propagation
        propagator = UncertaintyPropagator(random_state=42)
        param_dists = {
            'base_risk': ('uniform', {'min': 100.0, 'max': 500.0}),
            'multiplier': ('normal', {'mean': 2.0, 'std': 0.5}),
            'fixed_cost': ('triangular', {'left': 50.0, 'mode': 100.0, 'right': 150.0})
        }
        uncertainty = propagator.propagate(risk_model, param_dists, n_simulations=500)
        
        # Verify all analyses complete
        assert len(sensitivity) == 3
        assert len(scenarios) >= 3
        assert uncertainty.mean > 0
        
        # Verify serialization
        sens_dicts = [s.to_dict() for s in sensitivity]
        scen_dicts = [s.to_dict() for s in scenarios]
        unc_dict = uncertainty.to_dict()
        
        import json
        json.dumps({'sensitivity': sens_dicts, 'scenarios': scen_dicts, 'uncertainty': unc_dict})


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
