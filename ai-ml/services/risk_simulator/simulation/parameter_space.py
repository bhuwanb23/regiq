"""
Parameter Space Definition and Validation.

This module provides tools for defining simulation parameter spaces with:
- Distribution specification
- Constraint validation
- Correlation modeling
- Sensitivity analysis
- JSON import/export
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class DistributionType(Enum):
    """Probability distribution types"""
    UNIFORM = "uniform"
    NORMAL = "normal"
    LOGNORMAL = "lognormal"
    BETA = "beta"
    GAMMA = "gamma"
    EXPONENTIAL = "exponential"
    TRIANGULAR = "triangular"
    WEIBULL = "weibull"


@dataclass
class Parameter:
    """
    Definition of a single parameter in the parameter space.
    
    Attributes:
        name: Parameter name
        distribution: Distribution type
        params: Distribution-specific parameters
        bounds: Optional (min, max) bounds
        description: Parameter description
    """
    name: str
    distribution: DistributionType
    params: Dict[str, float]
    bounds: Optional[Tuple[float, float]] = None
    description: str = ""
    
    def validate(self) -> bool:
        """Validate parameter configuration"""
        # Check required distribution parameters
        required_params = {
            DistributionType.UNIFORM: ['low', 'high'],
            DistributionType.NORMAL: ['mean', 'std'],
            DistributionType.LOGNORMAL: ['mean', 'std'],
            DistributionType.BETA: ['alpha', 'beta'],
            DistributionType.GAMMA: ['shape', 'scale'],
            DistributionType.EXPONENTIAL: ['rate'],
            DistributionType.TRIANGULAR: ['low', 'mode', 'high'],
            DistributionType.WEIBULL: ['shape', 'scale']
        }
        
        required = required_params.get(self.distribution, [])
        for param in required:
            if param not in self.params:
                logger.error(f"Missing required parameter '{param}' for {self.distribution.value}")
                return False
        
        # Validate distribution-specific constraints
        if self.distribution == DistributionType.UNIFORM:
            if self.params['low'] >= self.params['high']:
                logger.error("Uniform: low must be < high")
                return False
        
        elif self.distribution == DistributionType.NORMAL:
            if self.params['std'] <= 0:
                logger.error("Normal: std must be > 0")
                return False
        
        elif self.distribution == DistributionType.BETA:
            if self.params['alpha'] <= 0 or self.params['beta'] <= 0:
                logger.error("Beta: alpha and beta must be > 0")
                return False
        
        elif self.distribution == DistributionType.GAMMA:
            if self.params['shape'] <= 0 or self.params['scale'] <= 0:
                logger.error("Gamma: shape and scale must be > 0")
                return False
        
        elif self.distribution == DistributionType.EXPONENTIAL:
            if self.params['rate'] <= 0:
                logger.error("Exponential: rate must be > 0")
                return False
        
        elif self.distribution == DistributionType.TRIANGULAR:
            low, mode, high = self.params['low'], self.params['mode'], self.params['high']
            if not (low <= mode <= high):
                logger.error("Triangular: must have low <= mode <= high")
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'distribution': self.distribution.value,
            'params': self.params,
            'bounds': self.bounds,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Parameter':
        """Create Parameter from dictionary"""
        return cls(
            name=data['name'],
            distribution=DistributionType(data['distribution']),
            params=data['params'],
            bounds=tuple(data['bounds']) if data.get('bounds') else None,
            description=data.get('description', '')
        )


class ParameterSpace:
    """
    Collection of parameters defining the simulation space.
    
    Supports:
    - Parameter addition and removal
    - Constraint validation
    - Correlation modeling
    - Sensitivity analysis
    - JSON import/export
    
    Example:
        >>> space = ParameterSpace()
        >>> space.add_parameter(
        ...     'violation_rate',
        ...     DistributionType.BETA,
        ...     {'alpha': 2, 'beta': 5},
        ...     bounds=(0, 1),
        ...     description='Compliance violation rate'
        ... )
        >>> space.validate()
    """
    
    def __init__(self, name: str = "default"):
        """Initialize parameter space"""
        self.name = name
        self.parameters: Dict[str, Parameter] = {}
        self.correlations: Dict[Tuple[str, str], float] = {}
        self.constraints: List[Dict[str, Any]] = []
    
    def add_parameter(self,
                     name: str,
                     distribution: DistributionType,
                     params: Dict[str, float],
                     bounds: Optional[Tuple[float, float]] = None,
                     description: str = "") -> None:
        """
        Add a parameter to the space.
        
        Args:
            name: Parameter name (must be unique)
            distribution: Distribution type
            params: Distribution parameters
            bounds: Optional (min, max) bounds
            description: Parameter description
        """
        if name in self.parameters:
            logger.warning(f"Parameter '{name}' already exists, overwriting")
        
        param = Parameter(
            name=name,
            distribution=distribution,
            params=params,
            bounds=bounds,
            description=description
        )
        
        if not param.validate():
            raise ValueError(f"Invalid parameter configuration for '{name}'")
        
        self.parameters[name] = param
        logger.info(f"Added parameter '{name}' with {distribution.value} distribution")
    
    def remove_parameter(self, name: str) -> None:
        """Remove a parameter from the space"""
        if name not in self.parameters:
            raise KeyError(f"Parameter '{name}' not found")
        
        del self.parameters[name]
        
        # Remove associated correlations
        to_remove = [k for k in self.correlations.keys() if name in k]
        for k in to_remove:
            del self.correlations[k]
        
        logger.info(f"Removed parameter '{name}'")
    
    def add_correlation(self, param1: str, param2: str, correlation: float) -> None:
        """
        Add correlation between two parameters.
        
        Args:
            param1: First parameter name
            param2: Second parameter name
            correlation: Correlation coefficient [-1, 1]
        """
        if param1 not in self.parameters:
            raise KeyError(f"Parameter '{param1}' not found")
        if param2 not in self.parameters:
            raise KeyError(f"Parameter '{param2}' not found")
        if not -1 <= correlation <= 1:
            raise ValueError("Correlation must be in [-1, 1]")
        
        # Store in canonical order
        sorted_params = sorted([param1, param2])
        key: Tuple[str, str] = (sorted_params[0], sorted_params[1])
        self.correlations[key] = correlation
        
        logger.info(f"Added correlation between '{param1}' and '{param2}': {correlation}")
    
    def add_constraint(self, constraint_type: str, params: List[str], 
                      condition: str, value: float) -> None:
        """
        Add a constraint on parameters.
        
        Args:
            constraint_type: Type of constraint ('sum', 'ratio', 'difference')
            params: List of parameter names
            condition: Condition ('<=', '>=', '==')
            value: Constraint value
        """
        for param in params:
            if param not in self.parameters:
                raise KeyError(f"Parameter '{param}' not found")
        
        constraint = {
            'type': constraint_type,
            'params': params,
            'condition': condition,
            'value': value
        }
        
        self.constraints.append(constraint)
        logger.info(f"Added {constraint_type} constraint on {params}")
    
    def validate(self) -> bool:
        """Validate the entire parameter space"""
        # Validate each parameter
        for param in self.parameters.values():
            if not param.validate():
                return False
        
        # Check correlation matrix is valid
        if not self._validate_correlation_matrix():
            logger.error("Invalid correlation matrix")
            return False
        
        logger.info(f"Parameter space '{self.name}' validated successfully")
        return True
    
    def _validate_correlation_matrix(self) -> bool:
        """Validate that correlation matrix is positive semi-definite"""
        if not self.correlations:
            return True
        
        # Build correlation matrix
        param_names = list(self.parameters.keys())
        n = len(param_names)
        
        if n < 2:
            return True
        
        corr_matrix = np.eye(n)
        
        for (p1, p2), corr in self.correlations.items():
            i = param_names.index(p1)
            j = param_names.index(p2)
            corr_matrix[i, j] = corr
            corr_matrix[j, i] = corr
        
        # Check if positive semi-definite
        eigenvalues = np.linalg.eigvalsh(corr_matrix)
        return bool(np.all(eigenvalues >= -1e-10))  # Allow small numerical errors
    
    def get_parameter_config(self) -> Dict[str, Dict[str, Any]]:
        """Get parameter configuration for Monte Carlo simulator"""
        config = {}
        for name, param in self.parameters.items():
            config[name] = {
                'distribution': param.distribution.value,
                **param.params
            }
        return config
    
    def sensitivity_analysis(self, baseline_values: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        """
        Perform basic sensitivity analysis.
        
        Returns variance contribution for each parameter based on
        distribution properties.
        """
        if baseline_values is None:
            baseline_values = self._get_baseline_values()
        
        sensitivities = {}
        
        for name, param in self.parameters.items():
            # Estimate variance based on distribution
            if param.distribution == DistributionType.UNIFORM:
                low, high = param.params['low'], param.params['high']
                variance = (high - low) ** 2 / 12
            
            elif param.distribution == DistributionType.NORMAL:
                variance = param.params['std'] ** 2
            
            elif param.distribution == DistributionType.BETA:
                a, b = param.params['alpha'], param.params['beta']
                variance = (a * b) / ((a + b) ** 2 * (a + b + 1))
            
            elif param.distribution == DistributionType.GAMMA:
                variance = param.params['shape'] * param.params['scale'] ** 2
            
            elif param.distribution == DistributionType.EXPONENTIAL:
                variance = 1 / param.params['rate'] ** 2
            
            else:
                variance = 1.0  # Default
            
            sensitivities[name] = float(variance)
        
        # Normalize to sum to 1
        total = sum(sensitivities.values())
        if total > 0:
            sensitivities = {k: v/total for k, v in sensitivities.items()}
        
        return sensitivities
    
    def _get_baseline_values(self) -> Dict[str, float]:
        """Get baseline values (means) for each parameter"""
        baseline = {}
        
        for name, param in self.parameters.items():
            if param.distribution == DistributionType.UNIFORM:
                baseline[name] = (param.params['low'] + param.params['high']) / 2
            
            elif param.distribution == DistributionType.NORMAL:
                baseline[name] = param.params['mean']
            
            elif param.distribution == DistributionType.BETA:
                a, b = param.params['alpha'], param.params['beta']
                baseline[name] = a / (a + b)
            
            elif param.distribution == DistributionType.GAMMA:
                baseline[name] = param.params['shape'] * param.params['scale']
            
            elif param.distribution == DistributionType.EXPONENTIAL:
                baseline[name] = 1 / param.params['rate']
            
            elif param.distribution == DistributionType.TRIANGULAR:
                baseline[name] = param.params['mode']
            
            else:
                baseline[name] = 0.0
        
        return baseline
    
    def to_dict(self) -> Dict[str, Any]:
        """Export to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'parameters': {name: param.to_dict() for name, param in self.parameters.items()},
            'correlations': {f"{k[0]}_{k[1]}": v for k, v in self.correlations.items()},
            'constraints': self.constraints
        }
    
    def to_json(self, filepath: str) -> None:
        """Export parameter space to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Exported parameter space to {filepath}")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ParameterSpace':
        """Import from dictionary"""
        space = cls(name=data['name'])
        
        # Load parameters
        for name, param_data in data['parameters'].items():
            param = Parameter.from_dict(param_data)
            space.parameters[name] = param
        
        # Load correlations
        for key, value in data.get('correlations', {}).items():
            params = key.split('_')
            if len(params) == 2:
                space.correlations[tuple(sorted(params))] = value
        
        # Load constraints
        space.constraints = data.get('constraints', [])
        
        return space
    
    @classmethod
    def from_json(cls, filepath: str) -> 'ParameterSpace':
        """Import parameter space from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded parameter space from {filepath}")
        return cls.from_dict(data)
    
    def summary(self) -> str:
        """Generate text summary of parameter space"""
        lines = [
            f"Parameter Space: {self.name}",
            "=" * 60,
            f"Number of parameters: {len(self.parameters)}",
            f"Correlations defined: {len(self.correlations)}",
            f"Constraints: {len(self.constraints)}",
            "",
            "Parameters:",
            "-" * 60
        ]
        
        for name, param in self.parameters.items():
            lines.append(f"{name}:")
            lines.append(f"  Distribution: {param.distribution.value}")
            lines.append(f"  Parameters: {param.params}")
            if param.bounds:
                lines.append(f"  Bounds: {param.bounds}")
            if param.description:
                lines.append(f"  Description: {param.description}")
            lines.append("")
        
        if self.correlations:
            lines.append("Correlations:")
            lines.append("-" * 60)
            for (p1, p2), corr in self.correlations.items():
                lines.append(f"  {p1} <-> {p2}: {corr:.3f}")
        
        return '\n'.join(lines)
    
    def __len__(self) -> int:
        """Number of parameters in space"""
        return len(self.parameters)
    
    def __contains__(self, name: str) -> bool:
        """Check if parameter exists"""
        return name in self.parameters
    
    def __getitem__(self, name: str) -> Parameter:
        """Get parameter by name"""
        return self.parameters[name]


if __name__ == "__main__":
    # Example usage
    print("="*60)
    print("Parameter Space - Example Usage")
    print("="*60)
    
    # Create parameter space for compliance risk
    space = ParameterSpace(name="compliance_risk")
    
    # Add parameters
    space.add_parameter(
        'violation_rate',
        DistributionType.BETA,
        {'alpha': 2, 'beta': 5},
        bounds=(0, 1),
        description='Probability of compliance violation'
    )
    
    space.add_parameter(
        'penalty_amount',
        DistributionType.LOGNORMAL,
        {'mean': 10, 'std': 0.5},
        description='Financial penalty amount (log scale)'
    )
    
    space.add_parameter(
        'enforcement_prob',
        DistributionType.UNIFORM,
        {'low': 0.5, 'high': 0.9},
        description='Probability of enforcement action'
    )
    
    # Add correlation
    space.add_correlation('violation_rate', 'penalty_amount', 0.3)
    
    # Validate
    if space.validate():
        print("\n✅ Parameter space validated successfully!")
    
    # Print summary
    print(f"\n{space.summary()}")
    
    # Sensitivity analysis
    print("\nSensitivity Analysis:")
    print("-" * 60)
    sensitivities = space.sensitivity_analysis()
    for param, sens in sensitivities.items():
        print(f"  {param}: {sens:.3f}")
    
    # Export to JSON
    space.to_json('test_parameter_space.json')
    print("\n📁 Exported to test_parameter_space.json")
    
    # Get config for Monte Carlo
    config = space.get_parameter_config()
    print("\n⚙️  Monte Carlo Config:")
    print(json.dumps(config, indent=2))
    
    print(f"\n{'='*60}")
    print("Parameter space example completed!")
    print('='*60)
