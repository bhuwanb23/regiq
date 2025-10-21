#!/usr/bin/env python3
"""
REGIQ AI/ML - Calibration Analysis
Implements calibration metrics, Brier scores, and calibration plots.
"""

import os
import sys
import json
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import time

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    MATPLOTLIB_AVAILABLE = True
    PLOTLY_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    PLOTLY_AVAILABLE = False

try:
    from sklearn.calibration import calibration_curve
    from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
    from sklearn.isotonic import IsotonicRegression
    from sklearn.linear_model import LogisticRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class CalibrationResult:
    """Results of calibration analysis."""
    metric_name: str
    protected_attribute: str
    groups: List[str]
    brier_scores: Dict[str, float]
    log_loss_scores: Dict[str, float]
    ece_scores: Dict[str, float]  # Expected Calibration Error
    mce_scores: Dict[str, float]  # Maximum Calibration Error
    reliability_diagrams: Dict[str, Dict[str, List[float]]]
    calibration_quality: str  # excellent, good, fair, poor
    threshold_violation: bool
    threshold_value: float
    recommendations: List[str]
    metadata: Dict[str, Any]


@dataclass
class CalibrationThreshold:
    """Threshold configuration for calibration analysis."""
    brier_threshold: float = 0.25  # Brier score threshold
    ece_threshold: float = 0.1    # ECE threshold
    mce_threshold: float = 0.2    # MCE threshold
    min_group_size: int = 30
    n_bins: int = 10
    alert_enabled: bool = True


class CalibrationAnalyzer:
    """Analyzes model calibration across protected groups."""
    
    def __init__(self, threshold_config: Optional[CalibrationThreshold] = None):
        self.threshold = threshold_config or CalibrationThreshold()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("calibration_analysis")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def calculate_calibration_metrics(self, y_true: np.ndarray, y_prob: np.ndarray, 
                                    protected_attribute: np.ndarray, 
                                    protected_groups: Optional[List[str]] = None) -> CalibrationResult:
        """Calculate calibration metrics."""
        try:
            # Convert to numpy arrays if needed
            y_true = np.array(y_true)
            y_prob = np.array(y_prob)
            protected_attribute = np.array(protected_attribute)
            
            # Get unique groups
            if protected_groups is None:
                groups = np.unique(protected_attribute)
            else:
                groups = np.array(protected_groups)
            
            # Calculate metrics for each group
            brier_scores = {}
            log_loss_scores = {}
            ece_scores = {}
            mce_scores = {}
            reliability_diagrams = {}
            group_sizes = {}
            
            for group in groups:
                group_mask = protected_attribute == group
                group_size = np.sum(group_mask)
                
                if group_size < self.threshold.min_group_size:
                    self.logger.warning(f"Group {group} has only {group_size} samples (min: {self.threshold.min_group_size})")
                    continue
                
                group_y_true = y_true[group_mask]
                group_y_prob = y_prob[group_mask]
                
                # Calculate Brier score
                brier_score = self._calculate_brier_score(group_y_true, group_y_prob)
                brier_scores[str(group)] = float(brier_score)
                
                # Calculate log loss
                log_loss_score = self._calculate_log_loss(group_y_true, group_y_prob)
                log_loss_scores[str(group)] = float(log_loss_score)
                
                # Calculate ECE and MCE
                ece, mce = self._calculate_calibration_errors(group_y_true, group_y_prob)
                ece_scores[str(group)] = float(ece)
                mce_scores[str(group)] = float(mce)
                
                # Calculate reliability diagram
                reliability_diagram = self._calculate_reliability_diagram(group_y_true, group_y_prob)
                reliability_diagrams[str(group)] = reliability_diagram
                
                group_sizes[str(group)] = int(group_size)
            
            # Determine calibration quality
            calibration_quality = self._assess_calibration_quality(brier_scores, ece_scores, mce_scores)
            
            # Check threshold violations
            threshold_violation = self._check_threshold_violations(brier_scores, ece_scores, mce_scores)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                brier_scores, ece_scores, mce_scores, calibration_quality, threshold_violation
            )
            
            return CalibrationResult(
                metric_name="Calibration Analysis",
                protected_attribute=str(protected_attribute[0]) if len(protected_attribute) > 0 else "unknown",
                groups=list(brier_scores.keys()),
                brier_scores=brier_scores,
                log_loss_scores=log_loss_scores,
                ece_scores=ece_scores,
                mce_scores=mce_scores,
                reliability_diagrams=reliability_diagrams,
                calibration_quality=calibration_quality,
                threshold_violation=threshold_violation,
                threshold_value=self.threshold.brier_threshold,
                recommendations=recommendations,
                metadata={
                    "group_sizes": group_sizes,
                    "total_samples": len(y_prob),
                    "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
        except Exception as e:
            self.logger.error(f"Calibration analysis failed: {e}")
            raise
    
    def _calculate_brier_score(self, y_true: np.ndarray, y_prob: np.ndarray) -> float:
        """Calculate Brier score."""
        try:
            if not SKLEARN_AVAILABLE:
                # Manual calculation
                return np.mean((y_prob - y_true) ** 2)
            else:
                return brier_score_loss(y_true, y_prob)
        except Exception as e:
            self.logger.warning(f"Brier score calculation failed: {e}")
            return float('inf')
    
    def _calculate_log_loss(self, y_true: np.ndarray, y_prob: np.ndarray) -> float:
        """Calculate log loss."""
        try:
            if not SKLEARN_AVAILABLE:
                # Manual calculation with epsilon for numerical stability
                epsilon = 1e-15
                y_prob = np.clip(y_prob, epsilon, 1 - epsilon)
                return -np.mean(y_true * np.log(y_prob) + (1 - y_true) * np.log(1 - y_prob))
            else:
                return log_loss(y_true, y_prob)
        except Exception as e:
            self.logger.warning(f"Log loss calculation failed: {e}")
            return float('inf')
    
    def _calculate_calibration_errors(self, y_true: np.ndarray, y_prob: np.ndarray) -> Tuple[float, float]:
        """Calculate Expected Calibration Error (ECE) and Maximum Calibration Error (MCE)."""
        try:
            n_bins = self.threshold.n_bins
            bin_boundaries = np.linspace(0, 1, n_bins + 1)
            bin_lowers = bin_boundaries[:-1]
            bin_uppers = bin_boundaries[1:]
            
            ece = 0
            mce = 0
            total_samples = len(y_true)
            
            for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
                in_bin = (y_prob > bin_lower) & (y_prob <= bin_upper)
                prop_in_bin = in_bin.mean()
                
                if prop_in_bin > 0:
                    accuracy_in_bin = y_true[in_bin].mean()
                    avg_confidence_in_bin = y_prob[in_bin].mean()
                    calibration_error = abs(avg_confidence_in_bin - accuracy_in_bin)
                    
                    ece += prop_in_bin * calibration_error
                    mce = max(mce, calibration_error)
            
            return float(ece), float(mce)
            
        except Exception as e:
            self.logger.warning(f"Calibration error calculation failed: {e}")
            return float('inf'), float('inf')
    
    def _calculate_reliability_diagram(self, y_true: np.ndarray, y_prob: np.ndarray) -> Dict[str, List[float]]:
        """Calculate reliability diagram data."""
        try:
            n_bins = self.threshold.n_bins
            
            if SKLEARN_AVAILABLE:
                fraction_of_positives, mean_predicted_value = calibration_curve(
                    y_true, y_prob, n_bins=n_bins
                )
            else:
                # Manual calculation
                bin_boundaries = np.linspace(0, 1, n_bins + 1)
                bin_lowers = bin_boundaries[:-1]
                bin_uppers = bin_boundaries[1:]
                
                fraction_of_positives = []
                mean_predicted_value = []
                
                for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
                    in_bin = (y_prob > bin_lower) & (y_prob <= bin_upper)
                    prop_in_bin = in_bin.mean()
                    
                    if prop_in_bin > 0:
                        accuracy_in_bin = y_true[in_bin].mean()
                        avg_confidence_in_bin = y_prob[in_bin].mean()
                        fraction_of_positives.append(accuracy_in_bin)
                        mean_predicted_value.append(avg_confidence_in_bin)
                    else:
                        fraction_of_positives.append(0)
                        mean_predicted_value.append(0)
            
            return {
                "fraction_of_positives": fraction_of_positives.tolist() if hasattr(fraction_of_positives, 'tolist') else list(fraction_of_positives),
                "mean_predicted_value": mean_predicted_value.tolist() if hasattr(mean_predicted_value, 'tolist') else list(mean_predicted_value)
            }
            
        except Exception as e:
            self.logger.warning(f"Reliability diagram calculation failed: {e}")
            return {"fraction_of_positives": [], "mean_predicted_value": []}
    
    def _assess_calibration_quality(self, brier_scores: Dict[str, float], 
                                   ece_scores: Dict[str, float], 
                                   mce_scores: Dict[str, float]) -> str:
        """Assess overall calibration quality."""
        try:
            # Get average scores
            avg_brier = np.mean(list(brier_scores.values()))
            avg_ece = np.mean(list(ece_scores.values()))
            avg_mce = np.mean(list(mce_scores.values()))
            
            # Determine quality based on thresholds
            if avg_brier <= 0.1 and avg_ece <= 0.05 and avg_mce <= 0.1:
                return "excellent"
            elif avg_brier <= 0.2 and avg_ece <= 0.1 and avg_mce <= 0.2:
                return "good"
            elif avg_brier <= 0.3 and avg_ece <= 0.15 and avg_mce <= 0.3:
                return "fair"
            else:
                return "poor"
                
        except Exception as e:
            self.logger.warning(f"Calibration quality assessment failed: {e}")
            return "unknown"
    
    def _check_threshold_violations(self, brier_scores: Dict[str, float], 
                                   ece_scores: Dict[str, float], 
                                   mce_scores: Dict[str, float]) -> bool:
        """Check if any group violates calibration thresholds."""
        try:
            # Check Brier score violations
            brier_violations = any(score > self.threshold.brier_threshold for score in brier_scores.values())
            
            # Check ECE violations
            ece_violations = any(score > self.threshold.ece_threshold for score in ece_scores.values())
            
            # Check MCE violations
            mce_violations = any(score > self.threshold.mce_threshold for score in mce_scores.values())
            
            return brier_violations or ece_violations or mce_violations
            
        except Exception as e:
            self.logger.warning(f"Threshold violation check failed: {e}")
            return False
    
    def _generate_recommendations(self, brier_scores: Dict[str, float], 
                                ece_scores: Dict[str, float], 
                                mce_scores: Dict[str, float],
                                calibration_quality: str, 
                                threshold_violation: bool) -> List[str]:
        """Generate recommendations based on calibration analysis."""
        recommendations = []
        
        recommendations.append(f"📊 Calibration Quality: {calibration_quality.upper()}")
        
        if threshold_violation:
            recommendations.append("⚠️ Calibration threshold violations detected")
            
            # Find worst performing groups
            worst_brier_group = max(brier_scores, key=brier_scores.get)
            worst_ece_group = max(ece_scores, key=ece_scores.get)
            worst_mce_group = max(mce_scores, key=mce_scores.get)
            
            recommendations.append(f"📊 Worst Brier Score: {worst_brier_group} ({brier_scores[worst_brier_group]:.3f})")
            recommendations.append(f"📊 Worst ECE: {worst_ece_group} ({ece_scores[worst_ece_group]:.3f})")
            recommendations.append(f"📊 Worst MCE: {worst_mce_group} ({mce_scores[worst_mce_group]:.3f})")
            
            recommendations.append("🔧 Recommendations:")
            recommendations.append("  • Apply Platt scaling or isotonic regression")
            recommendations.append("  • Use temperature scaling for neural networks")
            recommendations.append("  • Implement group-specific calibration")
            recommendations.append("  • Increase training data for poorly calibrated groups")
            recommendations.append("  • Consider ensemble methods for better calibration")
        else:
            recommendations.append("✅ Calibration within acceptable thresholds")
            recommendations.append("📊 All groups show good calibration performance")
        
        return recommendations
    
    def create_visualization(self, result: CalibrationResult, 
                           save_path: Optional[str] = None) -> Optional[str]:
        """Create calibration visualization."""
        try:
            if not MATPLOTLIB_AVAILABLE and not PLOTLY_AVAILABLE:
                self.logger.warning("No visualization libraries available")
                return None
            
            # Create visualization
            if PLOTLY_AVAILABLE:
                return self._create_plotly_visualization(result, save_path)
            elif MATPLOTLIB_AVAILABLE:
                return self._create_matplotlib_visualization(result, save_path)
            
        except Exception as e:
            self.logger.error(f"Visualization creation failed: {e}")
            return None
    
    def _create_plotly_visualization(self, result: CalibrationResult, 
                                    save_path: Optional[str] = None) -> str:
        """Create Plotly visualization."""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Brier Scores by Group', 'ECE Scores by Group', 
                              'Reliability Diagram', 'Calibration Quality'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "scatter"}, {"type": "indicator"}]]
            )
            
            groups = result.groups
            
            # Brier scores bar chart
            brier_values = [result.brier_scores[group] for group in groups]
            colors = ['red' if score > result.threshold_value else 'green' for score in brier_values]
            fig.add_trace(
                go.Bar(x=groups, y=brier_values, name='Brier Score', 
                      marker_color=colors),
                row=1, col=1
            )
            
            # ECE scores bar chart
            ece_values = [result.ece_scores[group] for group in groups]
            colors = ['red' if score > self.threshold.ece_threshold else 'green' for score in ece_values]
            fig.add_trace(
                go.Bar(x=groups, y=ece_values, name='ECE Score', 
                      marker_color=colors),
                row=1, col=2
            )
            
            # Reliability diagram
            for group in groups:
                if group in result.reliability_diagrams:
                    diagram = result.reliability_diagrams[group]
                    fig.add_trace(
                        go.Scatter(x=diagram["mean_predicted_value"], 
                                 y=diagram["fraction_of_positives"],
                                 mode='markers+lines', name=f'Group {group}'),
                        row=2, col=1
                    )
            
            # Perfect calibration line
            fig.add_trace(
                go.Scatter(x=[0, 1], y=[0, 1], mode='lines', 
                          name='Perfect Calibration', line=dict(dash='dash', color='red')),
                row=2, col=1
            )
            
            # Calibration quality gauge
            quality_scores = {"excellent": 1.0, "good": 0.8, "fair": 0.6, "poor": 0.4}
            quality_score = quality_scores.get(result.calibration_quality, 0.5)
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=quality_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Calibration Quality"},
                    gauge={'axis': {'range': [None, 1]},
                          'bar': {'color': "darkblue"},
                          'steps': [{'range': [0, 0.4], 'color': "red"},
                                   {'range': [0.4, 0.6], 'color': "orange"},
                                   {'range': [0.6, 0.8], 'color': "yellow"},
                                   {'range': [0.8, 1], 'color': "green"}],
                          'threshold': {'line': {'color': "red", 'width': 4},
                                      'thickness': 0.75, 'value': 0.8}}
                ),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title=f"Calibration Analysis - {result.protected_attribute}",
                height=800,
                showlegend=True
            )
            
            # Save or return
            if save_path:
                fig.write_html(save_path)
                self.logger.info(f"Visualization saved: {save_path}")
                return save_path
            else:
                return fig.to_html()
                
        except Exception as e:
            self.logger.error(f"Plotly visualization failed: {e}")
            return ""
    
    def _create_matplotlib_visualization(self, result: CalibrationResult, 
                                       save_path: Optional[str] = None) -> str:
        """Create Matplotlib visualization."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            groups = result.groups
            
            # Brier scores bar chart
            brier_values = [result.brier_scores[group] for group in groups]
            colors = ['red' if score > result.threshold_value else 'green' for score in brier_values]
            ax1.bar(groups, brier_values, color=colors)
            ax1.axhline(y=result.threshold_value, color='red', linestyle='--', label='Threshold')
            ax1.set_title('Brier Scores by Group')
            ax1.set_ylabel('Brier Score')
            ax1.legend()
            
            # ECE scores bar chart
            ece_values = [result.ece_scores[group] for group in groups]
            colors = ['red' if score > self.threshold.ece_threshold else 'green' for score in ece_values]
            ax2.bar(groups, ece_values, color=colors)
            ax2.axhline(y=self.threshold.ece_threshold, color='red', linestyle='--', label='Threshold')
            ax2.set_title('ECE Scores by Group')
            ax2.set_ylabel('ECE Score')
            ax2.legend()
            
            # Reliability diagram
            for group in groups:
                if group in result.reliability_diagrams:
                    diagram = result.reliability_diagrams[group]
                    ax3.plot(diagram["mean_predicted_value"], diagram["fraction_of_positives"], 
                            marker='o', label=f'Group {group}')
            
            # Perfect calibration line
            ax3.plot([0, 1], [0, 1], 'r--', label='Perfect Calibration')
            ax3.set_xlabel('Mean Predicted Value')
            ax3.set_ylabel('Fraction of Positives')
            ax3.set_title('Reliability Diagram')
            ax3.legend()
            
            # Calibration quality
            quality_scores = {"excellent": 1.0, "good": 0.8, "fair": 0.6, "poor": 0.4}
            quality_score = quality_scores.get(result.calibration_quality, 0.5)
            ax4.bar(['Calibration Quality'], [quality_score], color='blue')
            ax4.set_ylim(0, 1)
            ax4.set_title('Calibration Quality')
            ax4.set_ylabel('Quality Score')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Visualization saved: {save_path}")
                return save_path
            else:
                return "matplotlib_figure"
                
        except Exception as e:
            self.logger.error(f"Matplotlib visualization failed: {e}")
            return ""
    
    def generate_report(self, result: CalibrationResult, 
                       output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive calibration report."""
        try:
            report = {
                "analysis_type": "Calibration Analysis",
                "protected_attribute": result.protected_attribute,
                "analysis_date": result.metadata.get("analysis_date", ""),
                "summary": {
                    "calibration_quality": result.calibration_quality,
                    "threshold_violation": result.threshold_violation,
                    "avg_brier_score": np.mean(list(result.brier_scores.values())),
                    "avg_ece_score": np.mean(list(result.ece_scores.values())),
                    "avg_mce_score": np.mean(list(result.mce_scores.values()))
                },
                "group_analysis": {
                    "groups": result.groups,
                    "brier_scores": result.brier_scores,
                    "ece_scores": result.ece_scores,
                    "mce_scores": result.mce_scores,
                    "group_sizes": result.metadata.get("group_sizes", {})
                },
                "thresholds": {
                    "brier_threshold": self.threshold.brier_threshold,
                    "ece_threshold": self.threshold.ece_threshold,
                    "mce_threshold": self.threshold.mce_threshold,
                    "min_group_size": self.threshold.min_group_size,
                    "n_bins": self.threshold.n_bins
                },
                "recommendations": result.recommendations,
                "metadata": result.metadata
            }
            
            if output_path:
                with open(output_path, 'w') as f:
                    json.dump(report, f, indent=2)
                self.logger.info(f"Report saved: {output_path}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return {}


def main():
    """Test the calibration analyzer."""
    print("🧪 Testing Calibration Analyzer")
    
    # Create test data
    np.random.seed(42)
    n_samples = 1000
    
    # Create protected attribute (gender)
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    
    # Create biased probability predictions
    y_true = np.random.binomial(1, 0.6, n_samples)
    y_prob = np.random.beta(2, 3, n_samples)  # Biased towards lower probabilities
    
    # Add group-specific bias
    male_mask = gender == 'male'
    female_mask = gender == 'female'
    
    # Male group: better calibrated
    y_prob[male_mask] = np.random.beta(3, 2, np.sum(male_mask))
    
    # Female group: poorly calibrated
    y_prob[female_mask] = np.random.beta(1, 4, np.sum(female_mask))
    
    # Test analyzer
    analyzer = CalibrationAnalyzer()
    result = analyzer.calculate_calibration_metrics(y_true, y_prob, gender)
    
    print("✅ Calibration analysis completed")
    print(f"✅ Calibration quality: {result.calibration_quality}")
    print(f"✅ Threshold violation: {result.threshold_violation}")
    print(f"✅ Groups: {result.groups}")
    print(f"✅ Brier scores: {result.brier_scores}")
    print(f"✅ ECE scores: {result.ece_scores}")
    
    # Test visualization
    if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
        viz_path = analyzer.create_visualization(result, "calibration_analysis_viz.html")
        if viz_path:
            print(f"✅ Visualization created: {viz_path}")
    
    # Test report generation
    report = analyzer.generate_report(result)
    print(f"✅ Report generated with {len(report)} sections")


if __name__ == "__main__":
    main()
