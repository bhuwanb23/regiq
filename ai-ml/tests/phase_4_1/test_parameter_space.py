"""
Tests for Parameter Space Definition and Validation.

This test suite covers:
- Parameter creation and validation
- Distribution types
- Constraint validation
- Correlation modeling
- JSON serialization
- Sensitivity analysis
"""

import pytest
import numpy as np
import json
import os
from pathlib import Path

from services.risk_simulator.simulation.parameter_space import (
    Parameter,
    ParameterSpace,
    DistributionType
)


# ============================================================================
# Test Parameter Class
# ============================================================================

class TestParameter:
    """Tests for Parameter class"""
    
    def test_parameter_creation(self):
        """Test creating a parameter"""
        param = Parameter(
            name='test_param',
            distribution=DistributionType.NORMAL,
            params={'mean': 0, 'std': 1},
            description='Test parameter'
        )
        
        assert param.name == 'test_param'
        assert param.distribution == DistributionType.NORMAL
        assert param.params == {'mean': 0, 'std': 1}
        assert param.description == 'Test parameter'
    
    def test_parameter_validation_normal(self):
        """Test validation of normal distribution"""
        # Valid
        param = Parameter(
            'x', DistributionType.NORMAL,
            {'mean': 0, 'std': 1}
        )
        assert param.validate()
        
        # Invalid: negative std
        param_invalid = Parameter(
            'x', DistributionType.NORMAL,
            {'mean': 0, 'std': -1}
        )
        assert not param_invalid.validate()
        
        # Invalid: missing parameters
        param_missing = Parameter(
            'x', DistributionType.NORMAL,
            {'mean': 0}
        )
        assert not param_missing.validate()
    
    def test_parameter_validation_uniform(self):
        """Test validation of uniform distribution"""
        # Valid
        param = Parameter(
            'x', DistributionType.UNIFORM,
            {'low': 0, 'high': 1}
        )
        assert param.validate()
        
        # Invalid: low >= high
        param_invalid = Parameter(
            'x', DistributionType.UNIFORM,
            {'low': 1, 'high': 0}
        )
        assert not param_invalid.validate()
    
    def test_parameter_validation_beta(self):
        """Test validation of beta distribution"""
        # Valid
        param = Parameter(
            'x', DistributionType.BETA,
            {'alpha': 2, 'beta': 5}
        )
        assert param.validate()
        
        # Invalid: negative alpha
        param_invalid = Parameter(
            'x', DistributionType.BETA,
            {'alpha': -1, 'beta': 5}
        )
        assert not param_invalid.validate()
    
    def test_parameter_serialization(self):
        """Test parameter to_dict and from_dict"""
        param = Parameter(
            'test_param',
            DistributionType.GAMMA,
            {'shape': 2, 'scale': 3},
            bounds=(0, 100),
            description='Test'
        )
        
        # To dict
        param_dict = param.to_dict()
        assert param_dict['name'] == 'test_param'
        assert param_dict['distribution'] == 'gamma'
        assert param_dict['params'] == {'shape': 2, 'scale': 3}
        
        # From dict
        param_restored = Parameter.from_dict(param_dict)
        assert param_restored.name == param.name
        assert param_restored.distribution == param.distribution
        assert param_restored.params == param.params


# ============================================================================
# Test ParameterSpace Class
# ============================================================================

class TestParameterSpace:
    """Tests for ParameterSpace class"""
    
    def test_parameter_space_creation(self):
        """Test creating a parameter space"""
        space = ParameterSpace(name='test_space')
        
        assert space.name == 'test_space'
        assert len(space) == 0
        assert len(space.correlations) == 0
    
    def test_add_parameter(self):
        """Test adding parameters"""
        space = ParameterSpace()
        
        space.add_parameter(
            'param1',
            DistributionType.NORMAL,
            {'mean': 0, 'std': 1}
        )
        
        assert len(space) == 1
        assert 'param1' in space
        assert space['param1'].distribution == DistributionType.NORMAL
    
    def test_add_multiple_parameters(self):
        """Test adding multiple parameters"""
        space = ParameterSpace()
        
        space.add_parameter('p1', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        space.add_parameter('p2', DistributionType.UNIFORM, {'low': 0, 'high': 1})
        space.add_parameter('p3', DistributionType.BETA, {'alpha': 2, 'beta': 5})
        
        assert len(space) == 3
    
    def test_remove_parameter(self):
        """Test removing parameters"""
        space = ParameterSpace()
        space.add_parameter('p1', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        space.add_parameter('p2', DistributionType.UNIFORM, {'low': 0, 'high': 1})
        
        space.remove_parameter('p1')
        
        assert len(space) == 1
        assert 'p1' not in space
        assert 'p2' in space
    
    def test_add_correlation(self):
        """Test adding correlations"""
        space = ParameterSpace()
        space.add_parameter('p1', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        space.add_parameter('p2', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        
        space.add_correlation('p1', 'p2', 0.5)
        
        assert len(space.correlations) == 1
        # Check canonical ordering
        assert ('p1', 'p2') in space.correlations or ('p2', 'p1') in space.correlations
    
    def test_correlation_validation(self):
        """Test correlation matrix validation"""
        space = ParameterSpace()
        space.add_parameter('p1', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        space.add_parameter('p2', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        space.add_parameter('p3', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        
        # Valid correlations
        space.add_correlation('p1', 'p2', 0.5)
        space.add_correlation('p2', 'p3', 0.3)
        
        assert space.validate()
    
    def test_get_parameter_config(self):
        """Test getting Monte Carlo configuration"""
        space = ParameterSpace()
        space.add_parameter('p1', DistributionType.NORMAL, {'mean': 10, 'std': 2})
        space.add_parameter('p2', DistributionType.UNIFORM, {'low': 0, 'high': 1})
        
        config = space.get_parameter_config()
        
        assert 'p1' in config
        assert 'p2' in config
        assert config['p1']['distribution'] == 'normal'
        assert config['p1']['mean'] == 10
        assert config['p2']['distribution'] == 'uniform'
    
    def test_sensitivity_analysis(self):
        """Test sensitivity analysis"""
        space = ParameterSpace()
        space.add_parameter('p1', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        space.add_parameter('p2', DistributionType.UNIFORM, {'low': 0, 'high': 1})
        
        sensitivities = space.sensitivity_analysis()
        
        assert 'p1' in sensitivities
        assert 'p2' in sensitivities
        # Sensitivities should sum to 1
        assert abs(sum(sensitivities.values()) - 1.0) < 0.01
    
    def test_json_export_import(self, tmp_path):
        """Test JSON export and import"""
        space = ParameterSpace(name='test_space')
        space.add_parameter('p1', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        space.add_parameter('p2', DistributionType.BETA, {'alpha': 2, 'beta': 5})
        space.add_correlation('p1', 'p2', 0.3)
        
        # Export
        filepath = tmp_path / 'test_space.json'
        space.to_json(str(filepath))
        
        assert filepath.exists()
        
        # Import
        space_loaded = ParameterSpace.from_json(str(filepath))
        
        assert space_loaded.name == 'test_space'
        assert len(space_loaded) == 2
        assert 'p1' in space_loaded
        assert 'p2' in space_loaded
    
    def test_summary(self):
        """Test summary generation"""
        space = ParameterSpace(name='test_space')
        space.add_parameter('p1', DistributionType.NORMAL, {'mean': 0, 'std': 1})
        
        summary = space.summary()
        
        assert isinstance(summary, str)
        assert 'test_space' in summary
        assert 'p1' in summary
        assert 'normal' in summary


# ============================================================================
# Test Integration
# ============================================================================

class TestIntegration:
    """Integration tests for parameter space"""
    
    def test_compliance_risk_space(self):
        """Test creating a compliance risk parameter space"""
        space = ParameterSpace(name='compliance_risk')
        
        space.add_parameter(
            'violation_rate',
            DistributionType.BETA,
            {'alpha': 2, 'beta': 5},
            bounds=(0, 1),
            description='Compliance violation probability'
        )
        
        space.add_parameter(
            'penalty_amount',
            DistributionType.LOGNORMAL,
            {'mean': 10, 'std': 0.5},
            description='Financial penalty (log scale)'
        )
        
        space.add_parameter(
            'enforcement_prob',
            DistributionType.UNIFORM,
            {'low': 0.5, 'high': 0.9},
            description='Enforcement probability'
        )
        
        # Add correlation
        space.add_correlation('violation_rate', 'penalty_amount', 0.3)
        
        # Validate
        assert space.validate()
        assert len(space) == 3
        
        # Get config
        config = space.get_parameter_config()
        assert len(config) == 3
        
        # Sensitivity
        sens = space.sensitivity_analysis()
        assert len(sens) == 3
    
    def test_parameter_space_with_monte_carlo(self):
        """Test parameter space integration with Monte Carlo"""
        from services.risk_simulator.simulation.monte_carlo import MonteCarloSimulator
        
        # Create parameter space
        space = ParameterSpace()
        space.add_parameter('x', DistributionType.NORMAL, {'mean': 10, 'std': 2})
        space.add_parameter('y', DistributionType.UNIFORM, {'low': 0, 'high': 1})
        
        # Get config
        config = space.get_parameter_config()
        
        # Run Monte Carlo
        simulator = MonteCarloSimulator(n_simulations=1000, random_state=42)
        result = simulator.run(lambda p: p['x'] + p['y'], config)
        
        # Should work without errors
        assert result.n_simulations == 1000
        assert 9 < result.mean < 12  # x~N(10,2) + y~U(0,1) ≈ 10.5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
