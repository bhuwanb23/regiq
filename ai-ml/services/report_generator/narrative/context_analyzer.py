#!/usr/bin/env python3
"""
REGIQ AI/ML - Context Analyzer
Intelligent context analysis for narrative generation.

This module provides:
- Data significance analysis
- Trend detection and interpretation
- Anomaly identification
- Risk level assessment
- Performance benchmarking context

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
import statistics

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ContextInsight:
    """Context insight structure."""
    insight_type: str
    significance: str  # high, medium, low
    description: str
    impact: str
    recommendation: str
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "insight_type": self.insight_type,
            "significance": self.significance,
            "description": self.description,
            "impact": self.impact,
            "recommendation": self.recommendation,
            "confidence": self.confidence
        }


class ContextAnalyzer:
    """
    Intelligent context analyzer for narrative generation.
    
    Analyzes data to identify significant insights, trends, anomalies,
    and contextual information for narrative enhancement.
    """
    
    def __init__(self):
        """Initialize context analyzer."""
        self.logger = logging.getLogger(__name__)
        
        # Analysis thresholds
        self.significance_thresholds = {
            "high": 0.8,
            "medium": 0.6,
            "low": 0.4
        }
        
        # Benchmarks for comparison
        self.industry_benchmarks = {
            "compliance_rate": 0.85,
            "bias_score": 0.8,
            "risk_probability": 0.15,
            "health_score": 0.75
        }
    
    def analyze_context(self, section_data: Dict[str, Any], report_type: str) -> Dict[str, Any]:
        """
        Analyze context for narrative generation.
        
        Args:
            section_data: Data for the specific section
            report_type: Type of report (executive, technical, regulatory)
            
        Returns:
            Context analysis results
        """
        try:
            context = {
                "insights": [],
                "trends": [],
                "anomalies": [],
                "benchmarks": {},
                "risk_factors": [],
                "opportunities": [],
                "summary": {}
            }
            
            # Analyze different data types
            if "regulatory_data" in section_data:
                reg_context = self._analyze_regulatory_context(section_data["regulatory_data"])
                context.update(reg_context)
            
            if "bias_analysis_data" in section_data:
                bias_context = self._analyze_bias_context(section_data["bias_analysis_data"])
                context.update(bias_context)
            
            if "risk_simulation_data" in section_data:
                risk_context = self._analyze_risk_context(section_data["risk_simulation_data"])
                context.update(risk_context)
            
            # Generate overall insights
            context["insights"] = self._generate_insights(section_data)
            context["summary"] = self._generate_context_summary(context)
            
            self.logger.debug(f"Generated context analysis for {report_type} with {len(context['insights'])} insights")
            
            return context
            
        except Exception as e:
            self.logger.error(f"Context analysis failed: {str(e)}")
            return self._create_fallback_context(section_data)
    
    def _analyze_regulatory_context(self, regulatory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze regulatory compliance context."""
        context = {"regulatory_insights": [], "compliance_trends": []}
        
        try:
            summary = regulatory_data.get("summary", {})
            compliance_score = summary.get("compliance_score", 0.0)
            total_regulations = summary.get("total_regulations", 0)
            
            # Compliance performance analysis
            benchmark = self.industry_benchmarks["compliance_rate"]
            if compliance_score >= benchmark:
                context["regulatory_insights"].append(
                    ContextInsight(
                        insight_type="performance",
                        significance="high",
                        description=f"Compliance rate of {compliance_score:.1%} exceeds industry benchmark",
                        impact="Positive competitive positioning",
                        recommendation="Maintain current compliance practices",
                        confidence=0.9
                    )
                )
            else:
                gap = benchmark - compliance_score
                context["regulatory_insights"].append(
                    ContextInsight(
                        insight_type="gap",
                        significance="high" if gap > 0.1 else "medium",
                        description=f"Compliance gap of {gap:.1%} below industry standard",
                        impact="Regulatory risk exposure",
                        recommendation="Prioritize compliance improvement initiatives",
                        confidence=0.85
                    )
                )
            
            # Deadline analysis
            deadlines = regulatory_data.get("deadlines", [])
            urgent_deadlines = [d for d in deadlines if d.get("priority") == "high"]
            if urgent_deadlines:
                context["regulatory_insights"].append(
                    ContextInsight(
                        insight_type="urgency",
                        significance="high",
                        description=f"{len(urgent_deadlines)} high-priority regulatory deadlines approaching",
                        impact="Immediate action required",
                        recommendation="Establish deadline tracking and response protocols",
                        confidence=0.95
                    )
                )
            
        except Exception as e:
            self.logger.error(f"Regulatory context analysis failed: {str(e)}")
        
        return context
    
    def _analyze_bias_context(self, bias_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze AI bias context."""
        context = {"bias_insights": [], "fairness_trends": []}
        
        try:
            bias_score = bias_data.get("bias_score", {})
            overall_score = bias_score.get("overall_score", 0.0)
            flagged_attributes = bias_score.get("flagged_attributes", [])
            
            # Bias performance analysis
            benchmark = self.industry_benchmarks["bias_score"]
            if overall_score >= benchmark:
                context["bias_insights"].append(
                    ContextInsight(
                        insight_type="fairness",
                        significance="high",
                        description=f"AI fairness score of {overall_score:.3f} meets industry standards",
                        impact="Reduced discrimination risk",
                        recommendation="Continue monitoring and maintain fairness practices",
                        confidence=0.88
                    )
                )
            else:
                context["bias_insights"].append(
                    ContextInsight(
                        insight_type="bias_risk",
                        significance="high",
                        description=f"Bias score of {overall_score:.3f} indicates fairness concerns",
                        impact="Potential discrimination and regulatory risk",
                        recommendation="Implement bias mitigation strategies immediately",
                        confidence=0.92
                    )
                )
            
            # Flagged attributes analysis
            if flagged_attributes:
                context["bias_insights"].append(
                    ContextInsight(
                        insight_type="attribute_bias",
                        significance="medium",
                        description=f"Bias detected in {len(flagged_attributes)} protected attributes: {', '.join(flagged_attributes)}",
                        impact="Specific fairness violations requiring attention",
                        recommendation=f"Focus bias mitigation on {', '.join(flagged_attributes[:2])} attributes",
                        confidence=0.87
                    )
                )
            
            # Model performance context
            model_info = bias_data.get("model_info", {})
            performance_metrics = model_info.get("performance_metrics", {})
            if performance_metrics:
                accuracy = performance_metrics.get("accuracy", 0.0)
                if accuracy > 0.85:
                    context["bias_insights"].append(
                        ContextInsight(
                            insight_type="performance_balance",
                            significance="medium",
                            description=f"High model accuracy ({accuracy:.1%}) with bias concerns",
                            impact="Trade-off between performance and fairness",
                            recommendation="Optimize for fairness while maintaining performance",
                            confidence=0.8
                        )
                    )
            
        except Exception as e:
            self.logger.error(f"Bias context analysis failed: {str(e)}")
        
        return context
    
    def _analyze_risk_context(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk simulation context."""
        context = {"risk_insights": [], "risk_trends": []}
        
        try:
            risk_metrics = risk_data.get("risk_metrics", {})
            risk_probability = risk_metrics.get("risk_probability", 0.0)
            expected_impact = risk_metrics.get("expected_impact", 0.0)
            
            # Risk level analysis
            benchmark = self.industry_benchmarks["risk_probability"]
            if risk_probability <= benchmark:
                context["risk_insights"].append(
                    ContextInsight(
                        insight_type="risk_management",
                        significance="medium",
                        description=f"Risk probability of {risk_probability:.1%} within acceptable range",
                        impact="Controlled risk exposure",
                        recommendation="Maintain current risk management practices",
                        confidence=0.82
                    )
                )
            else:
                context["risk_insights"].append(
                    ContextInsight(
                        insight_type="elevated_risk",
                        significance="high",
                        description=f"Risk probability of {risk_probability:.1%} exceeds acceptable threshold",
                        impact="Significant compliance violation risk",
                        recommendation="Implement enhanced risk mitigation measures",
                        confidence=0.9
                    )
                )
            
            # Financial impact analysis
            financial_impact = risk_data.get("financial_impact", {})
            total_impact = financial_impact.get("total_impact", 0)
            if total_impact > 500000:  # $500K threshold
                context["risk_insights"].append(
                    ContextInsight(
                        insight_type="financial_exposure",
                        significance="high",
                        description=f"Potential financial impact of ${total_impact:,.0f}",
                        impact="Significant financial exposure requiring executive attention",
                        recommendation="Prioritize risk mitigation investments",
                        confidence=0.85
                    )
                )
            
            # Scenario analysis
            scenarios = risk_data.get("scenarios", [])
            high_impact_scenarios = [s for s in scenarios if s.get("impact", 0) > 0.7]
            if high_impact_scenarios:
                context["risk_insights"].append(
                    ContextInsight(
                        insight_type="scenario_risk",
                        significance="medium",
                        description=f"{len(high_impact_scenarios)} high-impact risk scenarios identified",
                        impact="Multiple risk vectors requiring attention",
                        recommendation="Develop scenario-specific mitigation strategies",
                        confidence=0.78
                    )
                )
            
        except Exception as e:
            self.logger.error(f"Risk context analysis failed: {str(e)}")
        
        return context
    
    def _generate_insights(self, section_data: Dict[str, Any]) -> List[ContextInsight]:
        """Generate overall insights from section data."""
        insights = []
        
        try:
            # Generate insights based on data analysis
            if "regulatory_data" in section_data:
                reg_data = section_data["regulatory_data"]
                summary = reg_data.get("summary", {})
                compliance_score = summary.get("compliance_score", 0.0)
                
                if compliance_score < 0.8:
                    insights.append(ContextInsight(
                        insight_type="compliance_gap",
                        significance="high",
                        description=f"Compliance score of {compliance_score:.1%} requires attention",
                        impact="Regulatory risk exposure",
                        recommendation="Prioritize compliance improvement",
                        confidence=0.9
                    ))
            
            if "bias_analysis_data" in section_data:
                bias_data = section_data["bias_analysis_data"]
                bias_score = bias_data.get("bias_score", {}).get("overall_score", 1.0)
                
                if bias_score < 0.8:
                    insights.append(ContextInsight(
                        insight_type="fairness_concern",
                        significance="high",
                        description=f"AI fairness score of {bias_score:.3f} indicates bias",
                        impact="Discrimination risk",
                        recommendation="Implement bias mitigation",
                        confidence=0.85
                    ))
            
            if "risk_simulation_data" in section_data:
                risk_data = section_data["risk_simulation_data"]
                risk_prob = risk_data.get("risk_metrics", {}).get("risk_probability", 0.0)
                
                if risk_prob > 0.2:
                    insights.append(ContextInsight(
                        insight_type="elevated_risk",
                        significance="medium",
                        description=f"Risk probability of {risk_prob:.1%} above threshold",
                        impact="Compliance violation risk",
                        recommendation="Enhance risk monitoring",
                        confidence=0.8
                    ))
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Insight generation failed: {str(e)}")
            return []
    
    def _generate_context_summary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate context summary."""
        try:
            summary = {
                "total_insights": len(context.get("insights", [])),
                "high_significance_count": 0,
                "primary_concerns": [],
                "key_opportunities": [],
                "overall_assessment": "stable"
            }
            
            # Count significance levels
            insights = context.get("insights", [])
            for insight in insights:
                if hasattr(insight, 'significance') and insight.significance == "high":
                    summary["high_significance_count"] += 1
            
            # Determine overall assessment
            if summary["high_significance_count"] >= 3:
                summary["overall_assessment"] = "attention_required"
            elif summary["high_significance_count"] >= 1:
                summary["overall_assessment"] = "monitoring_needed"
            else:
                summary["overall_assessment"] = "stable"
            
            # Extract primary concerns and opportunities
            for insight in insights[:3]:  # Top 3 insights
                if hasattr(insight, 'insight_type'):
                    if insight.insight_type in ["gap", "bias_risk", "elevated_risk"]:
                        summary["primary_concerns"].append(insight.description)
                    elif insight.insight_type in ["performance", "fairness", "risk_management"]:
                        summary["key_opportunities"].append(insight.description)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Context summary generation failed: {str(e)}")
            return {"total_insights": 0, "overall_assessment": "unknown"}
    
    def _create_fallback_context(self, section_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback context when analysis fails."""
        return {
            "insights": [
                ContextInsight(
                    insight_type="general",
                    significance="medium",
                    description="Analysis completed with available data",
                    impact="Standard operational status",
                    recommendation="Continue monitoring and regular assessment",
                    confidence=0.5
                )
            ],
            "trends": [],
            "anomalies": [],
            "benchmarks": {},
            "risk_factors": [],
            "opportunities": [],
            "summary": {
                "total_insights": 1,
                "overall_assessment": "stable"
            }
        }
    
    def identify_trends(self, historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify trends in historical data."""
        trends = []
        
        try:
            if len(historical_data) < 2:
                return trends
            
            # Analyze numerical trends
            for key in ["compliance_score", "bias_score", "risk_probability"]:
                values = []
                for data_point in historical_data:
                    if key in data_point and isinstance(data_point[key], (int, float)):
                        values.append(data_point[key])
                
                if len(values) >= 2:
                    trend = self._calculate_trend(values)
                    if abs(trend["change_rate"]) > 0.05:  # 5% threshold
                        trends.append({
                            "metric": key,
                            "direction": trend["direction"],
                            "change_rate": trend["change_rate"],
                            "significance": "high" if abs(trend["change_rate"]) > 0.15 else "medium"
                        })
            
        except Exception as e:
            self.logger.error(f"Trend identification failed: {str(e)}")
        
        return trends
    
    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend from numerical values."""
        if len(values) < 2:
            return {"direction": "stable", "change_rate": 0.0}
        
        # Simple linear trend calculation
        first_val = values[0]
        last_val = values[-1]
        change_rate = (last_val - first_val) / first_val if first_val != 0 else 0.0
        
        if change_rate > 0.02:
            direction = "improving"
        elif change_rate < -0.02:
            direction = "declining"
        else:
            direction = "stable"
        
        return {
            "direction": direction,
            "change_rate": change_rate,
            "first_value": first_val,
            "last_value": last_val
        }
    
    def detect_anomalies(self, data_points: List[float], threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Detect anomalies in data using statistical methods."""
        anomalies = []
        
        try:
            if len(data_points) < 3:
                return anomalies
            
            mean_val = statistics.mean(data_points)
            std_dev = statistics.stdev(data_points)
            
            for i, value in enumerate(data_points):
                z_score = abs((value - mean_val) / std_dev) if std_dev > 0 else 0
                
                if z_score > threshold:
                    anomalies.append({
                        "index": i,
                        "value": value,
                        "z_score": z_score,
                        "severity": "high" if z_score > 3.0 else "medium"
                    })
            
        except Exception as e:
            self.logger.error(f"Anomaly detection failed: {str(e)}")
        
        return anomalies
    
    def get_benchmark_comparison(self, metric_name: str, value: float) -> Dict[str, Any]:
        """Compare value against industry benchmark."""
        benchmark = self.industry_benchmarks.get(metric_name)
        
        if benchmark is None:
            return {"status": "no_benchmark", "comparison": "unknown"}
        
        difference = value - benchmark
        percentage_diff = (difference / benchmark) * 100 if benchmark != 0 else 0
        
        if abs(percentage_diff) < 5:
            status = "on_target"
        elif percentage_diff > 0:
            status = "above_benchmark"
        else:
            status = "below_benchmark"
        
        return {
            "status": status,
            "benchmark_value": benchmark,
            "actual_value": value,
            "difference": difference,
            "percentage_difference": percentage_diff,
            "comparison": f"{'Above' if percentage_diff > 0 else 'Below'} benchmark by {abs(percentage_diff):.1f}%"
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"ContextAnalyzer(benchmarks={len(self.industry_benchmarks)})"
