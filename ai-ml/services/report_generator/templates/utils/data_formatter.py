#!/usr/bin/env python3
"""
REGIQ AI/ML - Data Formatter
Data integration and formatting utilities for Phase 2-4 outputs.

This module provides:
- Data transformation from Phase 2-4 outputs
- Data validation and sanitization
- Format standardization
- Integration utilities

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from ..base.base_template import ReportData

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class FormattedData:
    """Formatted data container."""
    source_phase: str
    data_type: str
    formatted_data: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class DataFormatter:
    """
    Data formatter for integrating Phase 2-4 outputs into report templates.
    
    Handles data transformation, validation, and standardization for:
    - Phase 2: Regulatory Intelligence outputs
    - Phase 3: Bias Analysis outputs
    - Phase 4: Risk Simulation outputs
    """
    
    def __init__(self):
        """Initialize data formatter."""
        self.logger = logging.getLogger(__name__)
        self.supported_phases = ["phase_2", "phase_3", "phase_4"]
        self.data_cache: Dict[str, FormattedData] = {}
    
    def format_regulatory_data(self, raw_data: Dict[str, Any]) -> FormattedData:
        """
        Format Phase 2 regulatory intelligence data.
        
        Args:
            raw_data: Raw regulatory intelligence output
            
        Returns:
            Formatted regulatory data
        """
        try:
            formatted = {
                "summary": self._extract_regulatory_summary(raw_data),
                "regulations": self._extract_regulations_list(raw_data),
                "compliance_status": self._extract_compliance_status(raw_data),
                "deadlines": self._extract_deadlines(raw_data),
                "recommendations": self._extract_regulatory_recommendations(raw_data),
                "risk_assessment": self._extract_regulatory_risks(raw_data)
            }
            
            metadata = {
                "source": "regulatory_intelligence",
                "processed_at": datetime.utcnow().isoformat(),
                "data_quality": self._assess_data_quality(raw_data),
                "completeness": self._calculate_completeness(formatted)
            }
            
            result = FormattedData(
                source_phase="phase_2",
                data_type="regulatory_intelligence",
                formatted_data=formatted,
                metadata=metadata,
                timestamp=datetime.utcnow().isoformat()
            )
            
            self.logger.info("Regulatory data formatted successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to format regulatory data: {str(e)}")
            raise
    
    def format_bias_analysis_data(self, raw_data: Dict[str, Any]) -> FormattedData:
        """
        Format Phase 3 bias analysis data.
        
        Args:
            raw_data: Raw bias analysis output
            
        Returns:
            Formatted bias analysis data
        """
        try:
            formatted = {
                "model_info": self._extract_model_info(raw_data),
                "fairness_metrics": self._extract_fairness_metrics(raw_data),
                "bias_score": self._extract_bias_score(raw_data),
                "explainability": self._extract_explainability_data(raw_data),
                "mitigation_results": self._extract_mitigation_results(raw_data),
                "recommendations": self._extract_bias_recommendations(raw_data)
            }
            
            metadata = {
                "source": "bias_analysis",
                "processed_at": datetime.utcnow().isoformat(),
                "model_id": raw_data.get("model_id", "unknown"),
                "analysis_type": raw_data.get("analysis_type", "comprehensive"),
                "data_quality": self._assess_data_quality(raw_data),
                "completeness": self._calculate_completeness(formatted)
            }
            
            result = FormattedData(
                source_phase="phase_3",
                data_type="bias_analysis",
                formatted_data=formatted,
                metadata=metadata,
                timestamp=datetime.utcnow().isoformat()
            )
            
            self.logger.info("Bias analysis data formatted successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to format bias analysis data: {str(e)}")
            raise
    
    def format_risk_simulation_data(self, raw_data: Dict[str, Any]) -> FormattedData:
        """
        Format Phase 4 risk simulation data.
        
        Args:
            raw_data: Raw risk simulation output
            
        Returns:
            Formatted risk simulation data
        """
        try:
            formatted = {
                "simulation_results": self._extract_simulation_results(raw_data),
                "risk_metrics": self._extract_risk_metrics(raw_data),
                "scenarios": self._extract_scenarios(raw_data),
                "predictions": self._extract_predictions(raw_data),
                "financial_impact": self._extract_financial_impact(raw_data),
                "mitigation_strategies": self._extract_risk_mitigation(raw_data)
            }
            
            metadata = {
                "source": "risk_simulation",
                "processed_at": datetime.utcnow().isoformat(),
                "simulation_id": raw_data.get("simulation_id", "unknown"),
                "simulation_type": raw_data.get("simulation_type", "monte_carlo"),
                "data_quality": self._assess_data_quality(raw_data),
                "completeness": self._calculate_completeness(formatted)
            }
            
            result = FormattedData(
                source_phase="phase_4",
                data_type="risk_simulation",
                formatted_data=formatted,
                metadata=metadata,
                timestamp=datetime.utcnow().isoformat()
            )
            
            self.logger.info("Risk simulation data formatted successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to format risk simulation data: {str(e)}")
            raise
    
    def create_report_data(
        self,
        regulatory_data: Optional[Dict[str, Any]] = None,
        bias_data: Optional[Dict[str, Any]] = None,
        risk_data: Optional[Dict[str, Any]] = None,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> ReportData:
        """
        Create ReportData object from formatted inputs.
        
        Args:
            regulatory_data: Phase 2 regulatory intelligence data
            bias_data: Phase 3 bias analysis data
            risk_data: Phase 4 risk simulation data
            additional_metadata: Additional metadata
            
        Returns:
            ReportData object ready for template processing
        """
        try:
            # Format individual data sources
            formatted_regulatory = None
            formatted_bias = None
            formatted_risk = None
            
            if regulatory_data:
                formatted_regulatory = self.format_regulatory_data(regulatory_data)
            
            if bias_data:
                formatted_bias = self.format_bias_analysis_data(bias_data)
            
            if risk_data:
                formatted_risk = self.format_risk_simulation_data(risk_data)
            
            # Create combined metadata
            combined_metadata = {
                "created_at": datetime.utcnow().isoformat(),
                "data_sources": [],
                "processing_info": {
                    "formatter_version": "1.0.0",
                    "processing_timestamp": datetime.utcnow().isoformat()
                }
            }
            
            if formatted_regulatory:
                combined_metadata["data_sources"].append("regulatory_intelligence")
            if formatted_bias:
                combined_metadata["data_sources"].append("bias_analysis")
            if formatted_risk:
                combined_metadata["data_sources"].append("risk_simulation")
            
            if additional_metadata:
                combined_metadata.update(additional_metadata)
            
            # Create ReportData object
            report_data = ReportData(
                regulatory_data=formatted_regulatory.formatted_data if formatted_regulatory else None,
                bias_analysis_data=formatted_bias.formatted_data if formatted_bias else None,
                risk_simulation_data=formatted_risk.formatted_data if formatted_risk else None,
                metadata=combined_metadata
            )
            
            # Validate the created data
            is_valid, errors = report_data.validate()
            if not is_valid:
                raise ValueError(f"Report data validation failed: {', '.join(errors)}")
            
            self.logger.info(f"Report data created with {len(combined_metadata['data_sources'])} data sources")
            return report_data
            
        except Exception as e:
            self.logger.error(f"Failed to create report data: {str(e)}")
            raise
    
    # Helper methods for data extraction
    def _extract_regulatory_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract regulatory summary information."""
        return {
            "overview": data.get("summary", {}).get("overview", "No summary available"),
            "key_points": data.get("summary", {}).get("key_points", []),
            "total_regulations": len(data.get("regulations", [])),
            "compliance_score": data.get("compliance_score", 0.0)
        }
    
    def _extract_regulations_list(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract regulations list."""
        regulations = data.get("regulations", [])
        return [
            {
                "id": reg.get("id", "unknown"),
                "name": reg.get("name", "Unknown Regulation"),
                "jurisdiction": reg.get("jurisdiction", "Unknown"),
                "status": reg.get("status", "active"),
                "relevance_score": reg.get("relevance_score", 0.0)
            }
            for reg in regulations
        ]
    
    def _extract_compliance_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract compliance status."""
        return {
            "overall_status": data.get("compliance_status", "unknown"),
            "compliant_count": data.get("compliant_regulations", 0),
            "non_compliant_count": data.get("non_compliant_regulations", 0),
            "pending_review": data.get("pending_regulations", 0)
        }
    
    def _extract_deadlines(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract regulatory deadlines."""
        deadlines = data.get("deadlines", [])
        return [
            {
                "regulation": deadline.get("regulation", "Unknown"),
                "deadline_date": deadline.get("date", "Unknown"),
                "description": deadline.get("description", ""),
                "priority": deadline.get("priority", "medium")
            }
            for deadline in deadlines
        ]
    
    def _extract_regulatory_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Extract regulatory recommendations."""
        return data.get("recommendations", [])
    
    def _extract_regulatory_risks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract regulatory risk assessment."""
        return {
            "risk_level": data.get("risk_level", "unknown"),
            "risk_score": data.get("risk_score", 0.0),
            "risk_factors": data.get("risk_factors", [])
        }
    
    def _extract_model_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract model information."""
        return {
            "model_id": data.get("model_id", "unknown"),
            "model_type": data.get("model_type", "unknown"),
            "model_name": data.get("model_name", "Unknown Model"),
            "training_date": data.get("training_date", "unknown"),
            "performance_metrics": data.get("performance_metrics", {})
        }
    
    def _extract_fairness_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract fairness metrics."""
        metrics = data.get("fairness_metrics", {})
        return {
            "demographic_parity": metrics.get("demographic_parity", 0.0),
            "equalized_odds": metrics.get("equalized_odds", 0.0),
            "calibration": metrics.get("calibration", 0.0),
            "individual_fairness": metrics.get("individual_fairness", 0.0)
        }
    
    def _extract_bias_score(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract bias score information."""
        return {
            "overall_score": data.get("bias_score", 0.0),
            "risk_level": data.get("overall_fairness", "unknown"),
            "flagged_attributes": data.get("flagged_attributes", []),
            "score_interpretation": data.get("score_interpretation", "")
        }
    
    def _extract_explainability_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract explainability information."""
        return {
            "feature_importance": data.get("feature_importance", {}),
            "shap_values": data.get("shap_analysis", {}),
            "lime_explanations": data.get("lime_analysis", {}),
            "top_features": data.get("top_features", [])
        }
    
    def _extract_mitigation_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract mitigation results."""
        return {
            "applied_techniques": data.get("mitigation_techniques", []),
            "before_after_comparison": data.get("mitigation_results", {}),
            "effectiveness": data.get("mitigation_effectiveness", 0.0)
        }
    
    def _extract_bias_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Extract bias-related recommendations."""
        return data.get("recommendations", [])
    
    def _extract_simulation_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract simulation results."""
        return {
            "simulation_id": data.get("simulation_id", "unknown"),
            "simulation_type": data.get("simulation_type", "monte_carlo"),
            "iterations": data.get("iterations", 0),
            "convergence": data.get("convergence_status", "unknown")
        }
    
    def _extract_risk_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract risk metrics."""
        return {
            "risk_probability": data.get("risk_probability", 0.0),
            "confidence_interval": data.get("confidence_interval", []),
            "risk_level": data.get("risk_level", "unknown"),
            "expected_impact": data.get("expected_impact", 0.0)
        }
    
    def _extract_scenarios(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract scenario information."""
        scenarios = data.get("scenarios", [])
        return [
            {
                "scenario_id": scenario.get("id", "unknown"),
                "name": scenario.get("name", "Unknown Scenario"),
                "probability": scenario.get("probability", 0.0),
                "impact": scenario.get("impact", 0.0)
            }
            for scenario in scenarios
        ]
    
    def _extract_predictions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract prediction information."""
        return {
            "predicted_outcomes": data.get("predictions", []),
            "confidence_scores": data.get("confidence_scores", []),
            "time_horizon": data.get("time_horizon", "unknown")
        }
    
    def _extract_financial_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract financial impact assessment."""
        return {
            "potential_fines": data.get("potential_fines", {}),
            "remediation_costs": data.get("remediation_costs", 0.0),
            "business_disruption": data.get("business_disruption", {}),
            "total_impact": data.get("total_financial_impact", 0.0)
        }
    
    def _extract_risk_mitigation(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract risk mitigation strategies."""
        strategies = data.get("mitigation_strategies", [])
        return [
            {
                "strategy": strategy.get("name", "Unknown Strategy"),
                "effectiveness": strategy.get("effectiveness", 0.0),
                "cost": strategy.get("cost", 0.0),
                "timeline": strategy.get("timeline", "unknown")
            }
            for strategy in strategies
        ]
    
    def _assess_data_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess data quality metrics."""
        return {
            "completeness": len([v for v in data.values() if v is not None]) / len(data) if data else 0.0,
            "has_required_fields": bool(data.get("id") or data.get("model_id") or data.get("simulation_id")),
            "data_size": len(str(data)),
            "nested_depth": self._calculate_nested_depth(data)
        }
    
    def _calculate_completeness(self, formatted_data: Dict[str, Any]) -> float:
        """Calculate data completeness score."""
        total_fields = 0
        complete_fields = 0
        
        def count_fields(obj, path=""):
            nonlocal total_fields, complete_fields
            if isinstance(obj, dict):
                for key, value in obj.items():
                    total_fields += 1
                    if value is not None and value != "" and value != []:
                        complete_fields += 1
                    if isinstance(value, (dict, list)):
                        count_fields(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        count_fields(item, f"{path}[{i}]")
        
        count_fields(formatted_data)
        return complete_fields / total_fields if total_fields > 0 else 0.0
    
    def _calculate_nested_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calculate maximum nested depth of data structure."""
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._calculate_nested_depth(v, current_depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(self._calculate_nested_depth(item, current_depth + 1) for item in obj)
        else:
            return current_depth
    
    def get_formatter_stats(self) -> Dict[str, Any]:
        """Get formatter statistics."""
        return {
            "supported_phases": self.supported_phases,
            "cache_size": len(self.data_cache),
            "cached_data_types": list(set(data.data_type for data in self.data_cache.values()))
        }
    
    def clear_cache(self) -> None:
        """Clear data cache."""
        cache_size = len(self.data_cache)
        self.data_cache.clear()
        self.logger.info(f"Data cache cleared: {cache_size} items removed")
    
    def __str__(self) -> str:
        """String representation."""
        return f"DataFormatter(phases={len(self.supported_phases)}, cache={len(self.data_cache)})"
