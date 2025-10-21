#!/usr/bin/env python3
"""
REGIQ AI/ML - Demographic Parity Metrics
Implements demographic parity calculation, visualization, and reporting.
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
    from scipy import stats
    from sklearn.metrics import confusion_matrix, classification_report
    SCIPY_AVAILABLE = True
    SKLEARN_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    SKLEARN_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class DemographicParityResult:
    """Results of demographic parity analysis."""
    metric_name: str
    protected_attribute: str
    groups: List[str]
    positive_rates: Dict[str, float]
    parity_score: float
    max_difference: float
    threshold_violation: bool
    threshold_value: float
    statistical_significance: Optional[float]
    recommendations: List[str]
    metadata: Dict[str, Any]


@dataclass
class ParityThreshold:
    """Threshold configuration for demographic parity."""
    threshold_value: float = 0.1  # 10% difference threshold
    significance_level: float = 0.05
    min_group_size: int = 30
    alert_enabled: bool = True


class DemographicParityAnalyzer:
    """Analyzes demographic parity across protected groups."""
    
    def __init__(self, threshold_config: Optional[ParityThreshold] = None):
        self.threshold = threshold_config or ParityThreshold()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("demographic_parity")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def calculate_demographic_parity(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                   protected_attribute: np.ndarray, 
                                   protected_groups: Optional[List[str]] = None) -> DemographicParityResult:
        """Calculate demographic parity metrics."""
        try:
            # Convert to numpy arrays if needed
            y_true = np.array(y_true)
            y_pred = np.array(y_pred)
            protected_attribute = np.array(protected_attribute)
            
            # Get unique groups
            if protected_groups is None:
                groups = np.unique(protected_attribute)
            else:
                groups = np.array(protected_groups)
            
            # Calculate positive rates for each group
            positive_rates = {}
            group_sizes = {}
            
            for group in groups:
                group_mask = protected_attribute == group
                group_size = np.sum(group_mask)
                
                if group_size < self.threshold.min_group_size:
                    self.logger.warning(f"Group {group} has only {group_size} samples (min: {self.threshold.min_group_size})")
                    continue
                
                group_predictions = y_pred[group_mask]
                positive_rate = np.mean(group_predictions)
                positive_rates[str(group)] = float(positive_rate)
                group_sizes[str(group)] = int(group_size)
            
            # Calculate parity metrics
            if len(positive_rates) < 2:
                raise ValueError("Need at least 2 groups for demographic parity analysis")
            
            rates = list(positive_rates.values())
            max_difference = max(rates) - min(rates)
            parity_score = 1.0 - max_difference  # Higher is better
            
            # Check threshold violation
            threshold_violation = max_difference > self.threshold.threshold_value
            
            # Statistical significance test
            statistical_significance = self._calculate_statistical_significance(
                y_pred, protected_attribute, groups
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                positive_rates, max_difference, threshold_violation
            )
            
            return DemographicParityResult(
                metric_name="Demographic Parity",
                protected_attribute=str(protected_attribute[0]) if len(protected_attribute) > 0 else "unknown",
                groups=list(positive_rates.keys()),
                positive_rates=positive_rates,
                parity_score=parity_score,
                max_difference=max_difference,
                threshold_violation=threshold_violation,
                threshold_value=self.threshold.threshold_value,
                statistical_significance=statistical_significance,
                recommendations=recommendations,
                metadata={
                    "group_sizes": group_sizes,
                    "total_samples": len(y_pred),
                    "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
        except Exception as e:
            self.logger.error(f"Demographic parity calculation failed: {e}")
            raise
    
    def _calculate_statistical_significance(self, y_pred: np.ndarray, 
                                          protected_attribute: np.ndarray, 
                                          groups: List[str]) -> Optional[float]:
        """Calculate statistical significance of group differences."""
        try:
            if not SCIPY_AVAILABLE:
                return None
            
            # Prepare data for chi-square test
            group_predictions = []
            for group in groups:
                group_mask = protected_attribute == group
                group_pred = y_pred[group_mask]
                if len(group_pred) >= self.threshold.min_group_size:
                    group_predictions.append(group_pred)
            
            if len(group_predictions) < 2:
                return None
            
            # Perform chi-square test
            contingency_table = []
            for group_pred in group_predictions:
                positive_count = np.sum(group_pred)
                negative_count = len(group_pred) - positive_count
                contingency_table.append([positive_count, negative_count])
            
            contingency_table = np.array(contingency_table)
            chi2, p_value = stats.chi2_contingency(contingency_table)[:2]
            
            return float(p_value)
            
        except Exception as e:
            self.logger.warning(f"Statistical significance calculation failed: {e}")
            return None
    
    def _generate_recommendations(self, positive_rates: Dict[str, float], 
                                max_difference: float, threshold_violation: bool) -> List[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []
        
        if threshold_violation:
            recommendations.append(f"⚠️ Demographic parity violation detected: {max_difference:.3f} > {self.threshold.threshold_value}")
            
            # Find groups with highest and lowest rates
            max_group = max(positive_rates, key=positive_rates.get)
            min_group = min(positive_rates, key=positive_rates.get)
            
            recommendations.append(f"📊 Highest positive rate: {max_group} ({positive_rates[max_group]:.3f})")
            recommendations.append(f"📊 Lowest positive rate: {min_group} ({positive_rates[min_group]:.3f})")
            
            recommendations.append("🔧 Recommendations:")
            recommendations.append("  • Review model training data for bias")
            recommendations.append("  • Consider fairness constraints in model training")
            recommendations.append("  • Implement bias mitigation techniques")
            recommendations.append("  • Increase sample size for underrepresented groups")
        else:
            recommendations.append("✅ Demographic parity maintained within threshold")
            recommendations.append(f"📊 Maximum difference: {max_difference:.3f} ≤ {self.threshold.threshold_value}")
        
        return recommendations
    
    def create_visualization(self, result: DemographicParityResult, 
                           save_path: Optional[str] = None) -> Optional[str]:
        """Create demographic parity visualization."""
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
    
    def _create_plotly_visualization(self, result: DemographicParityResult, 
                                    save_path: Optional[str] = None) -> str:
        """Create Plotly visualization."""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Positive Rates by Group', 'Parity Score', 
                              'Group Sizes', 'Threshold Analysis'),
                specs=[[{"type": "bar"}, {"type": "indicator"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Positive rates bar chart
            groups = result.groups
            rates = [result.positive_rates[group] for group in groups]
            
            fig.add_trace(
                go.Bar(x=groups, y=rates, name='Positive Rate', 
                      marker_color=['red' if rate > result.threshold_value else 'green' for rate in rates]),
                row=1, col=1
            )
            
            # Parity score gauge
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=result.parity_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Parity Score"},
                    gauge={'axis': {'range': [None, 1]},
                          'bar': {'color': "darkblue"},
                          'steps': [{'range': [0, 0.5], 'color': "lightgray"},
                                   {'range': [0.5, 0.8], 'color': "yellow"},
                                   {'range': [0.8, 1], 'color': "green"}],
                          'threshold': {'line': {'color': "red", 'width': 4},
                                      'thickness': 0.75, 'value': 0.9}}
                ),
                row=1, col=2
            )
            
            # Group sizes
            group_sizes = result.metadata.get('group_sizes', {})
            sizes = [group_sizes.get(group, 0) for group in groups]
            
            fig.add_trace(
                go.Bar(x=groups, y=sizes, name='Group Size', marker_color='lightblue'),
                row=2, col=1
            )
            
            # Threshold analysis
            threshold_line = [result.threshold_value] * len(groups)
            fig.add_trace(
                go.Bar(x=groups, y=rates, name='Actual Rate', marker_color='blue'),
                row=2, col=2
            )
            fig.add_trace(
                go.Scatter(x=groups, y=threshold_line, mode='lines', 
                          name='Threshold', line=dict(color='red', dash='dash')),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title=f"Demographic Parity Analysis - {result.protected_attribute}",
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
    
    def _create_matplotlib_visualization(self, result: DemographicParityResult, 
                                       save_path: Optional[str] = None) -> str:
        """Create Matplotlib visualization."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            groups = result.groups
            rates = [result.positive_rates[group] for group in groups]
            
            # Positive rates bar chart
            colors = ['red' if rate > result.threshold_value else 'green' for rate in rates]
            ax1.bar(groups, rates, color=colors)
            ax1.axhline(y=result.threshold_value, color='red', linestyle='--', label='Threshold')
            ax1.set_title('Positive Rates by Group')
            ax1.set_ylabel('Positive Rate')
            ax1.legend()
            
            # Parity score
            ax2.bar(['Parity Score'], [result.parity_score], color='blue')
            ax2.set_ylim(0, 1)
            ax2.set_title('Parity Score')
            ax2.set_ylabel('Score')
            
            # Group sizes
            group_sizes = result.metadata.get('group_sizes', {})
            sizes = [group_sizes.get(group, 0) for group in groups]
            ax3.bar(groups, sizes, color='lightblue')
            ax3.set_title('Group Sizes')
            ax3.set_ylabel('Sample Size')
            
            # Threshold analysis
            ax4.bar(groups, rates, color='blue', alpha=0.7, label='Actual Rate')
            ax4.axhline(y=result.threshold_value, color='red', linestyle='--', label='Threshold')
            ax4.set_title('Threshold Analysis')
            ax4.set_ylabel('Positive Rate')
            ax4.legend()
            
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
    
    def generate_report(self, result: DemographicParityResult, 
                       output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive demographic parity report."""
        try:
            report = {
                "analysis_type": "Demographic Parity",
                "protected_attribute": result.protected_attribute,
                "analysis_date": result.metadata.get("analysis_date", ""),
                "summary": {
                    "parity_score": result.parity_score,
                    "max_difference": result.max_difference,
                    "threshold_violation": result.threshold_violation,
                    "statistical_significance": result.statistical_significance
                },
                "group_analysis": {
                    "groups": result.groups,
                    "positive_rates": result.positive_rates,
                    "group_sizes": result.metadata.get("group_sizes", {})
                },
                "thresholds": {
                    "threshold_value": result.threshold_value,
                    "significance_level": self.threshold.significance_level,
                    "min_group_size": self.threshold.min_group_size
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
    """Test the demographic parity analyzer."""
    print("🧪 Testing Demographic Parity Analyzer")
    
    # Create test data
    np.random.seed(42)
    n_samples = 1000
    
    # Create protected attribute (gender)
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    
    # Create biased predictions
    y_pred = np.zeros(n_samples)
    y_pred[gender == 'male'] = np.random.binomial(1, 0.7, np.sum(gender == 'male'))
    y_pred[gender == 'female'] = np.random.binomial(1, 0.5, np.sum(gender == 'female'))
    
    # Create ground truth
    y_true = np.random.binomial(1, 0.6, n_samples)
    
    # Test analyzer
    analyzer = DemographicParityAnalyzer()
    result = analyzer.calculate_demographic_parity(y_true, y_pred, gender)
    
    print("✅ Demographic parity analysis completed")
    print(f"✅ Parity score: {result.parity_score:.3f}")
    print(f"✅ Max difference: {result.max_difference:.3f}")
    print(f"✅ Threshold violation: {result.threshold_violation}")
    print(f"✅ Groups: {result.groups}")
    print(f"✅ Positive rates: {result.positive_rates}")
    
    # Test visualization
    if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
        viz_path = analyzer.create_visualization(result, "demographic_parity_viz.html")
        if viz_path:
            print(f"✅ Visualization created: {viz_path}")
    
    # Test report generation
    report = analyzer.generate_report(result)
    print(f"✅ Report generated with {len(report)} sections")


if __name__ == "__main__":
    main()
