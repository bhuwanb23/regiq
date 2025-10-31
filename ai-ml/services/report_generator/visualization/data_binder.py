#!/usr/bin/env python3
"""
REGIQ AI/ML - Data Binder
Data binding system for Phase 5.1/5.2 integration.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class DataBinding:
    """Data binding configuration."""
    binding_id: str
    source_path: str  # JSONPath expression
    chart_field: str
    data_type: str
    transformation: Optional[str] = None
    default_value: Any = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "binding_id": self.binding_id,
            "source_path": self.source_path,
            "chart_field": self.chart_field,
            "data_type": self.data_type,
            "transformation": self.transformation,
            "default_value": self.default_value
        }


class DataBinder:
    """
    Data binding system for visualization.
    
    Binds data from Phase 5.1 reports and Phase 5.2 narratives
    to chart configurations for visualization.
    """
    
    def __init__(self):
        """Initialize data binder."""
        self.logger = logging.getLogger(__name__)
        self.transformations = self._initialize_transformations()
        
    def _initialize_transformations(self) -> Dict[str, callable]:
        """Initialize data transformation functions."""
        return {
            "percentage": lambda x: x * 100 if isinstance(x, (int, float)) else x,
            "round_2": lambda x: round(x, 2) if isinstance(x, (int, float)) else x,
            "round_3": lambda x: round(x, 3) if isinstance(x, (int, float)) else x,
            "to_string": lambda x: str(x),
            "to_float": lambda x: float(x) if x is not None else 0.0,
            "to_int": lambda x: int(x) if x is not None else 0,
            "compliance_status": self._transform_compliance_status,
            "risk_level": self._transform_risk_level,
            "bias_score": self._transform_bias_score,
            "extract_keys": lambda x: list(x.keys()) if isinstance(x, dict) else [],
            "extract_values": lambda x: list(x.values()) if isinstance(x, dict) else [],
            "sort_desc": lambda x: sorted(x, reverse=True) if isinstance(x, list) else x,
            "top_n": lambda x, n=10: x[:n] if isinstance(x, list) else x
        }
    
    def bind_data(
        self,
        source_data: Dict[str, Any],
        bindings: List[DataBinding]
    ) -> Dict[str, Any]:
        """
        Bind data from source to chart fields.
        
        Args:
            source_data: Source data from Phase 5.1/5.2
            bindings: List of data bindings
            
        Returns:
            Bound data dictionary
        """
        try:
            bound_data = {}
            
            for binding in bindings:
                try:
                    # Extract data using JSONPath-like expression
                    value = self._extract_data(source_data, binding.source_path)
                    
                    # Apply transformation if specified
                    if binding.transformation and value is not None:
                        value = self._apply_transformation(value, binding.transformation)
                    
                    # Use default value if extraction failed
                    if value is None and binding.default_value is not None:
                        value = binding.default_value
                    
                    # Convert to specified data type
                    value = self._convert_data_type(value, binding.data_type)
                    
                    bound_data[binding.chart_field] = value
                    
                except Exception as e:
                    self.logger.warning(f"Failed to bind {binding.binding_id}: {str(e)}")
                    if binding.default_value is not None:
                        bound_data[binding.chart_field] = binding.default_value
            
            self.logger.debug(f"Bound {len(bound_data)} data fields")
            return bound_data
            
        except Exception as e:
            self.logger.error(f"Data binding failed: {str(e)}")
            return {}
    
    def _extract_data(self, source_data: Dict[str, Any], path: str) -> Any:
        """Extract data using JSONPath-like expression."""
        try:
            # Simple JSONPath implementation
            if path.startswith("$."):
                path = path[2:]  # Remove $.
            
            parts = path.split(".")
            current = source_data
            
            for part in parts:
                if "[" in part and "]" in part:
                    # Handle array access like "items[0]"
                    key, index_str = part.split("[")
                    index = int(index_str.rstrip("]"))
                    current = current[key][index]
                else:
                    current = current[part]
            
            return current
            
        except (KeyError, IndexError, TypeError, ValueError) as e:
            self.logger.debug(f"Failed to extract data at path {path}: {str(e)}")
            return None
    
    def _apply_transformation(self, value: Any, transformation: str) -> Any:
        """Apply data transformation."""
        try:
            if transformation in self.transformations:
                return self.transformations[transformation](value)
            else:
                self.logger.warning(f"Unknown transformation: {transformation}")
                return value
        except Exception as e:
            self.logger.error(f"Transformation {transformation} failed: {str(e)}")
            return value
    
    def _convert_data_type(self, value: Any, data_type: str) -> Any:
        """Convert value to specified data type."""
        try:
            if value is None:
                return None
            
            if data_type == "string":
                return str(value)
            elif data_type == "number":
                return float(value) if "." in str(value) else int(value)
            elif data_type == "integer":
                return int(value)
            elif data_type == "float":
                return float(value)
            elif data_type == "boolean":
                return bool(value)
            elif data_type == "list":
                return list(value) if not isinstance(value, list) else value
            elif data_type == "dict":
                return dict(value) if not isinstance(value, dict) else value
            else:
                return value
                
        except (ValueError, TypeError) as e:
            self.logger.warning(f"Data type conversion failed for {data_type}: {str(e)}")
            return value
    
    def _transform_compliance_status(self, score: float) -> str:
        """Transform compliance score to status."""
        if score >= 0.9:
            return "excellent"
        elif score >= 0.8:
            return "good"
        elif score >= 0.6:
            return "fair"
        elif score >= 0.4:
            return "poor"
        else:
            return "critical"
    
    def _transform_risk_level(self, risk_score: float) -> str:
        """Transform risk score to level."""
        if risk_score <= 0.2:
            return "low"
        elif risk_score <= 0.5:
            return "medium"
        elif risk_score <= 0.8:
            return "high"
        else:
            return "critical"
    
    def _transform_bias_score(self, bias_score: float) -> str:
        """Transform bias score to fairness level."""
        if bias_score >= 0.9:
            return "excellent"
        elif bias_score >= 0.8:
            return "good"
        elif bias_score >= 0.6:
            return "fair"
        else:
            return "needs_attention"
    
    def create_compliance_bindings(self) -> List[DataBinding]:
        """Create standard compliance data bindings."""
        return [
            DataBinding(
                binding_id="compliance_score",
                source_path="$.regulatory_data.summary.compliance_score",
                chart_field="value",
                data_type="float",
                transformation="round_3",
                default_value=0.0
            ),
            DataBinding(
                binding_id="compliance_status",
                source_path="$.regulatory_data.summary.compliance_score",
                chart_field="status",
                data_type="string",
                transformation="compliance_status",
                default_value="unknown"
            ),
            DataBinding(
                binding_id="total_regulations",
                source_path="$.regulatory_data.summary.total_regulations",
                chart_field="total",
                data_type="integer",
                default_value=0
            ),
            DataBinding(
                binding_id="compliant_count",
                source_path="$.regulatory_data.compliance_status.compliant_count",
                chart_field="compliant",
                data_type="integer",
                default_value=0
            ),
            DataBinding(
                binding_id="non_compliant_count",
                source_path="$.regulatory_data.compliance_status.non_compliant_count",
                chart_field="non_compliant",
                data_type="integer",
                default_value=0
            )
        ]
    
    def create_bias_analysis_bindings(self) -> List[DataBinding]:
        """Create bias analysis data bindings."""
        return [
            DataBinding(
                binding_id="bias_score",
                source_path="$.bias_analysis_data.bias_score.overall_score",
                chart_field="value",
                data_type="float",
                transformation="round_3",
                default_value=0.0
            ),
            DataBinding(
                binding_id="fairness_status",
                source_path="$.bias_analysis_data.bias_score.overall_score",
                chart_field="status",
                data_type="string",
                transformation="bias_score",
                default_value="unknown"
            ),
            DataBinding(
                binding_id="flagged_attributes",
                source_path="$.bias_analysis_data.bias_score.flagged_attributes",
                chart_field="flagged",
                data_type="list",
                default_value=[]
            ),
            DataBinding(
                binding_id="model_accuracy",
                source_path="$.bias_analysis_data.model_info.performance_metrics.accuracy",
                chart_field="accuracy",
                data_type="float",
                transformation="round_3",
                default_value=0.0
            ),
            DataBinding(
                binding_id="fairness_metrics",
                source_path="$.bias_analysis_data.fairness_metrics",
                chart_field="metrics",
                data_type="dict",
                default_value={}
            )
        ]
    
    def create_risk_simulation_bindings(self) -> List[DataBinding]:
        """Create risk simulation data bindings."""
        return [
            DataBinding(
                binding_id="risk_probability",
                source_path="$.risk_simulation_data.risk_metrics.risk_probability",
                chart_field="probability",
                data_type="float",
                transformation="round_3",
                default_value=0.0
            ),
            DataBinding(
                binding_id="risk_level",
                source_path="$.risk_simulation_data.risk_metrics.risk_probability",
                chart_field="level",
                data_type="string",
                transformation="risk_level",
                default_value="unknown"
            ),
            DataBinding(
                binding_id="expected_impact",
                source_path="$.risk_simulation_data.risk_metrics.expected_impact",
                chart_field="impact",
                data_type="float",
                transformation="round_3",
                default_value=0.0
            ),
            DataBinding(
                binding_id="scenarios",
                source_path="$.risk_simulation_data.scenarios",
                chart_field="scenarios",
                data_type="list",
                default_value=[]
            ),
            DataBinding(
                binding_id="financial_impact",
                source_path="$.risk_simulation_data.financial_impact.total_impact",
                chart_field="financial_impact",
                data_type="float",
                default_value=0.0
            )
        ]
    
    def create_narrative_bindings(self) -> List[DataBinding]:
        """Create narrative data bindings."""
        return [
            DataBinding(
                binding_id="executive_summary",
                source_path="$.narratives.executive_summary",
                chart_field="summary",
                data_type="string",
                default_value=""
            ),
            DataBinding(
                binding_id="key_insights",
                source_path="$.narratives.key_insights",
                chart_field="insights",
                data_type="list",
                default_value=[]
            ),
            DataBinding(
                binding_id="recommendations",
                source_path="$.narratives.recommendations",
                chart_field="recommendations",
                data_type="list",
                default_value=[]
            )
        ]
    
    def bind_compliance_dashboard_data(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Bind data for compliance dashboard."""
        try:
            # Combine all relevant bindings
            bindings = (
                self.create_compliance_bindings() +
                self.create_bias_analysis_bindings() +
                self.create_risk_simulation_bindings()
            )
            
            # Bind the data
            bound_data = self.bind_data(source_data, bindings)
            
            # Add computed fields
            bound_data["overall_health_score"] = self._calculate_health_score(bound_data)
            bound_data["compliance_distribution"] = self._calculate_compliance_distribution(bound_data)
            bound_data["risk_matrix_data"] = self._prepare_risk_matrix_data(bound_data)
            
            return bound_data
            
        except Exception as e:
            self.logger.error(f"Failed to bind compliance dashboard data: {str(e)}")
            return {}
    
    def _calculate_health_score(self, data: Dict[str, Any]) -> float:
        """Calculate overall health score."""
        try:
            scores = []
            
            if "value" in data:  # compliance score
                scores.append(data["value"])
            
            if "value" in data and "bias_score" in str(data):  # bias score
                scores.append(data.get("bias_score", 0.0))
            
            if "probability" in data:  # risk probability (inverted)
                scores.append(1.0 - data["probability"])
            
            return sum(scores) / len(scores) if scores else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate health score: {str(e)}")
            return 0.0
    
    def _calculate_compliance_distribution(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate compliance distribution for pie chart."""
        try:
            compliant = data.get("compliant", 0)
            non_compliant = data.get("non_compliant", 0)
            
            return {
                "categories": ["Compliant", "Non-Compliant"],
                "values": [compliant, non_compliant]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to calculate compliance distribution: {str(e)}")
            return {"categories": [], "values": []}
    
    def _prepare_risk_matrix_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare risk matrix data."""
        try:
            probability = data.get("probability", 0.0)
            impact = data.get("impact", 0.0)
            
            # Create simple 3x3 risk matrix
            return {
                "x_values": ["Low", "Medium", "High"],
                "y_values": ["Low Impact", "Medium Impact", "High Impact"],
                "z_values": [
                    [0.1, 0.2, 0.3],
                    [0.2, probability, 0.6],
                    [0.3, 0.6, impact]
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to prepare risk matrix data: {str(e)}")
            return {"x_values": [], "y_values": [], "z_values": []}
    
    def validate_bindings(self, bindings: List[DataBinding]) -> Tuple[bool, List[str]]:
        """Validate data bindings."""
        errors = []
        
        try:
            for binding in bindings:
                if not binding.binding_id:
                    errors.append("Binding ID is required")
                
                if not binding.source_path:
                    errors.append(f"Source path is required for binding {binding.binding_id}")
                
                if not binding.chart_field:
                    errors.append(f"Chart field is required for binding {binding.binding_id}")
                
                if binding.transformation and binding.transformation not in self.transformations:
                    errors.append(f"Unknown transformation: {binding.transformation}")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def __str__(self) -> str:
        """String representation."""
        return f"DataBinder({len(self.transformations)} transformations)"
