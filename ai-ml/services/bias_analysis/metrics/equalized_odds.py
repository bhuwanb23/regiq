#!/usr/bin/env python3
"""
REGIQ AI/ML - Equalized Odds Metrics
Implements equalized odds calculation, TPR/FPR analysis, and statistical tests.
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
    from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
    SCIPY_AVAILABLE = True
    SKLEARN_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    SKLEARN_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class EqualizedOddsResult:
    """Results of equalized odds analysis."""
    metric_name: str
    protected_attribute: str
    groups: List[str]
    tpr_by_group: Dict[str, float]  # True Positive Rate
    fpr_by_group: Dict[str, float]  # False Positive Rate
    tnr_by_group: Dict[str, float]  # True Negative Rate
    fnr_by_group: Dict[str, float]  # False Negative Rate
    tpr_difference: float
    fpr_difference: float
    equalized_odds_score: float
    threshold_violation: bool
    threshold_value: float
    statistical_tests: Dict[str, float]
    recommendations: List[str]
    metadata: Dict[str, Any]


@dataclass
class EqualizedOddsThreshold:
    """Threshold configuration for equalized odds."""
    tpr_threshold: float = 0.1  # 10% TPR difference threshold
    fpr_threshold: float = 0.1  # 10% FPR difference threshold
    significance_level: float = 0.05
    min_group_size: int = 30
    alert_enabled: bool = True


class EqualizedOddsAnalyzer:
    """Analyzes equalized odds across protected groups."""
    
    def __init__(self, threshold_config: Optional[EqualizedOddsThreshold] = None):
        self.threshold = threshold_config or EqualizedOddsThreshold()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("equalized_odds")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def calculate_equalized_odds(self, y_true: np.ndarray, y_pred: np.ndarray, 
                               protected_attribute: np.ndarray, 
                               protected_groups: Optional[List[str]] = None) -> EqualizedOddsResult:
        """Calculate equalized odds metrics."""
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
            
            # Calculate metrics for each group
            tpr_by_group = {}
            fpr_by_group = {}
            tnr_by_group = {}
            fnr_by_group = {}
            group_sizes = {}
            confusion_matrices = {}
            
            for group in groups:
                group_mask = protected_attribute == group
                group_size = np.sum(group_mask)
                
                if group_size < self.threshold.min_group_size:
                    self.logger.warning(f"Group {group} has only {group_size} samples (min: {self.threshold.min_group_size})")
                    continue
                
                group_y_true = y_true[group_mask]
                group_y_pred = y_pred[group_mask]
                
                # Calculate confusion matrix
                tn, fp, fn, tp = confusion_matrix(group_y_true, group_y_pred, labels=[0, 1]).ravel()
                confusion_matrices[str(group)] = {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}
                
                # Calculate rates
                tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
                tnr = tn / (tn + fp) if (tn + fp) > 0 else 0.0
                fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
                
                tpr_by_group[str(group)] = float(tpr)
                fpr_by_group[str(group)] = float(fpr)
                tnr_by_group[str(group)] = float(tnr)
                fnr_by_group[str(group)] = float(fnr)
                group_sizes[str(group)] = int(group_size)
            
            # Calculate differences
            if len(tpr_by_group) < 2:
                raise ValueError("Need at least 2 groups for equalized odds analysis")
            
            tpr_values = list(tpr_by_group.values())
            fpr_values = list(fpr_by_group.values())
            
            tpr_difference = max(tpr_values) - min(tpr_values)
            fpr_difference = max(fpr_values) - min(fpr_values)
            
            # Calculate equalized odds score
            equalized_odds_score = 1.0 - max(tpr_difference, fpr_difference)
            
            # Check threshold violation
            tpr_violation = tpr_difference > self.threshold.tpr_threshold
            fpr_violation = fpr_difference > self.threshold.fpr_threshold
            threshold_violation = tpr_violation or fpr_violation
            
            # Statistical tests
            statistical_tests = self._perform_statistical_tests(
                y_true, y_pred, protected_attribute, groups
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                tpr_by_group, fpr_by_group, tpr_difference, fpr_difference, 
                threshold_violation, tpr_violation, fpr_violation
            )
            
            return EqualizedOddsResult(
                metric_name="Equalized Odds",
                protected_attribute=str(protected_attribute[0]) if len(protected_attribute) > 0 else "unknown",
                groups=list(tpr_by_group.keys()),
                tpr_by_group=tpr_by_group,
                fpr_by_group=fpr_by_group,
                tnr_by_group=tnr_by_group,
                fnr_by_group=fnr_by_group,
                tpr_difference=tpr_difference,
                fpr_difference=fpr_difference,
                equalized_odds_score=equalized_odds_score,
                threshold_violation=threshold_violation,
                threshold_value=max(self.threshold.tpr_threshold, self.threshold.fpr_threshold),
                statistical_tests=statistical_tests,
                recommendations=recommendations,
                metadata={
                    "group_sizes": group_sizes,
                    "confusion_matrices": confusion_matrices,
                    "total_samples": len(y_pred),
                    "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
        except Exception as e:
            self.logger.error(f"Equalized odds calculation failed: {e}")
            raise
    
    def _perform_statistical_tests(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                 protected_attribute: np.ndarray, groups: List[str]) -> Dict[str, float]:
        """Perform statistical tests for equalized odds."""
        try:
            tests = {}
            
            if not SCIPY_AVAILABLE:
                return tests
            
            # Chi-square test for independence
            contingency_table = []
            for group in groups:
                group_mask = protected_attribute == group
                if np.sum(group_mask) < self.threshold.min_group_size:
                    continue
                
                group_y_true = y_true[group_mask]
                group_y_pred = y_pred[group_mask]
                
                # Create 2x2 contingency table
                tn, fp, fn, tp = confusion_matrix(group_y_true, group_y_pred, labels=[0, 1]).ravel()
                contingency_table.append([tn, fp, fn, tp])
            
            if len(contingency_table) >= 2:
                contingency_table = np.array(contingency_table)
                chi2, p_value = stats.chi2_contingency(contingency_table)[:2]
                tests["chi_square_p_value"] = float(p_value)
                tests["chi_square_statistic"] = float(chi2)
            
            # Mann-Whitney U test for TPR differences
            tpr_values = []
            group_labels = []
            for group in groups:
                group_mask = protected_attribute == group
                if np.sum(group_mask) < self.threshold.min_group_size:
                    continue
                
                group_y_true = y_true[group_mask]
                group_y_pred = y_pred[group_mask]
                
                # Calculate TPR for this group
                tn, fp, fn, tp = confusion_matrix(group_y_true, group_y_pred, labels=[0, 1]).ravel()
                tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                
                tpr_values.append(tpr)
                group_labels.append(group)
            
            if len(tpr_values) >= 2:
                # Compare first two groups
                group1_mask = protected_attribute == group_labels[0]
                group2_mask = protected_attribute == group_labels[1]
                
                group1_scores = y_pred[group1_mask]
                group2_scores = y_pred[group2_mask]
                
                if len(group1_scores) > 0 and len(group2_scores) > 0:
                    statistic, p_value = stats.mannwhitneyu(group1_scores, group2_scores, alternative='two-sided')
                    tests["mann_whitney_p_value"] = float(p_value)
                    tests["mann_whitney_statistic"] = float(statistic)
            
            return tests
            
        except Exception as e:
            self.logger.warning(f"Statistical tests failed: {e}")
            return {}
    
    def _generate_recommendations(self, tpr_by_group: Dict[str, float], 
                                fpr_by_group: Dict[str, float],
                                tpr_difference: float, fpr_difference: float,
                                threshold_violation: bool, tpr_violation: bool, 
                                fpr_violation: bool) -> List[str]:
        """Generate recommendations based on equalized odds analysis."""
        recommendations = []
        
        if threshold_violation:
            recommendations.append("⚠️ Equalized odds violation detected")
            
            if tpr_violation:
                recommendations.append(f"📊 TPR difference: {tpr_difference:.3f} > {self.threshold.tpr_threshold}")
                max_tpr_group = max(tpr_by_group, key=tpr_by_group.get)
                min_tpr_group = min(tpr_by_group, key=tpr_by_group.get)
                recommendations.append(f"  • Highest TPR: {max_tpr_group} ({tpr_by_group[max_tpr_group]:.3f})")
                recommendations.append(f"  • Lowest TPR: {min_tpr_group} ({tpr_by_group[min_tpr_group]:.3f})")
            
            if fpr_violation:
                recommendations.append(f"📊 FPR difference: {fpr_difference:.3f} > {self.threshold.fpr_threshold}")
                max_fpr_group = max(fpr_by_group, key=fpr_by_group.get)
                min_fpr_group = min(fpr_by_group, key=fpr_by_group.get)
                recommendations.append(f"  • Highest FPR: {max_fpr_group} ({fpr_by_group[max_fpr_group]:.3f})")
                recommendations.append(f"  • Lowest FPR: {min_fpr_group} ({fpr_by_group[min_fpr_group]:.3f})")
            
            recommendations.append("🔧 Recommendations:")
            recommendations.append("  • Review model training for group-specific bias")
            recommendations.append("  • Implement fairness constraints in model training")
            recommendations.append("  • Consider post-processing techniques")
            recommendations.append("  • Increase training data for underrepresented groups")
        else:
            recommendations.append("✅ Equalized odds maintained within threshold")
            recommendations.append(f"📊 TPR difference: {tpr_difference:.3f} ≤ {self.threshold.tpr_threshold}")
            recommendations.append(f"📊 FPR difference: {fpr_difference:.3f} ≤ {self.threshold.fpr_threshold}")
        
        return recommendations
    
    def create_visualization(self, result: EqualizedOddsResult, 
                           save_path: Optional[str] = None) -> Optional[str]:
        """Create equalized odds visualization."""
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
    
    def _create_plotly_visualization(self, result: EqualizedOddsResult, 
                                    save_path: Optional[str] = None) -> str:
        """Create Plotly visualization."""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('TPR by Group', 'FPR by Group', 
                              'Equalized Odds Score', 'Statistical Tests'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "indicator"}, {"type": "bar"}]]
            )
            
            groups = result.groups
            
            # TPR bar chart
            tpr_values = [result.tpr_by_group[group] for group in groups]
            fig.add_trace(
                go.Bar(x=groups, y=tpr_values, name='TPR', 
                      marker_color=['red' if tpr > result.threshold_value else 'green' for tpr in tpr_values]),
                row=1, col=1
            )
            
            # FPR bar chart
            fpr_values = [result.fpr_by_group[group] for group in groups]
            fig.add_trace(
                go.Bar(x=groups, y=fpr_values, name='FPR', 
                      marker_color=['red' if fpr > result.threshold_value else 'green' for fpr in fpr_values]),
                row=1, col=2
            )
            
            # Equalized odds score gauge
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=result.equalized_odds_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Equalized Odds Score"},
                    gauge={'axis': {'range': [None, 1]},
                          'bar': {'color': "darkblue"},
                          'steps': [{'range': [0, 0.5], 'color': "lightgray"},
                                   {'range': [0.5, 0.8], 'color': "yellow"},
                                   {'range': [0.8, 1], 'color': "green"}],
                          'threshold': {'line': {'color': "red", 'width': 4},
                                      'thickness': 0.75, 'value': 0.9}}
                ),
                row=2, col=1
            )
            
            # Statistical tests
            test_names = list(result.statistical_tests.keys())
            test_values = list(result.statistical_tests.values())
            fig.add_trace(
                go.Bar(x=test_names, y=test_values, name='P-values', marker_color='lightblue'),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title=f"Equalized Odds Analysis - {result.protected_attribute}",
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
    
    def _create_matplotlib_visualization(self, result: EqualizedOddsResult, 
                                       save_path: Optional[str] = None) -> str:
        """Create Matplotlib visualization."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            groups = result.groups
            
            # TPR bar chart
            tpr_values = [result.tpr_by_group[group] for group in groups]
            colors = ['red' if tpr > result.threshold_value else 'green' for tpr in tpr_values]
            ax1.bar(groups, tpr_values, color=colors)
            ax1.set_title('True Positive Rate by Group')
            ax1.set_ylabel('TPR')
            
            # FPR bar chart
            fpr_values = [result.fpr_by_group[group] for group in groups]
            colors = ['red' if fpr > result.threshold_value else 'green' for fpr in fpr_values]
            ax2.bar(groups, fpr_values, color=colors)
            ax2.set_title('False Positive Rate by Group')
            ax2.set_ylabel('FPR')
            
            # Equalized odds score
            ax3.bar(['Equalized Odds Score'], [result.equalized_odds_score], color='blue')
            ax3.set_ylim(0, 1)
            ax3.set_title('Equalized Odds Score')
            ax3.set_ylabel('Score')
            
            # Statistical tests
            test_names = list(result.statistical_tests.keys())
            test_values = list(result.statistical_tests.values())
            ax4.bar(test_names, test_values, color='lightblue')
            ax4.set_title('Statistical Tests (P-values)')
            ax4.set_ylabel('P-value')
            ax4.tick_params(axis='x', rotation=45)
            
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
    
    def generate_report(self, result: EqualizedOddsResult, 
                       output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive equalized odds report."""
        try:
            report = {
                "analysis_type": "Equalized Odds",
                "protected_attribute": result.protected_attribute,
                "analysis_date": result.metadata.get("analysis_date", ""),
                "summary": {
                    "equalized_odds_score": result.equalized_odds_score,
                    "tpr_difference": result.tpr_difference,
                    "fpr_difference": result.fpr_difference,
                    "threshold_violation": result.threshold_violation
                },
                "group_analysis": {
                    "groups": result.groups,
                    "tpr_by_group": result.tpr_by_group,
                    "fpr_by_group": result.fpr_by_group,
                    "group_sizes": result.metadata.get("group_sizes", {})
                },
                "statistical_tests": result.statistical_tests,
                "thresholds": {
                    "tpr_threshold": self.threshold.tpr_threshold,
                    "fpr_threshold": self.threshold.fpr_threshold,
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
    """Test the equalized odds analyzer."""
    print("🧪 Testing Equalized Odds Analyzer")
    
    # Create test data
    np.random.seed(42)
    n_samples = 1000
    
    # Create protected attribute (gender)
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    
    # Create biased predictions with different TPR/FPR by group
    y_pred = np.zeros(n_samples)
    y_true = np.random.binomial(1, 0.6, n_samples)
    
    # Male group: higher TPR, lower FPR
    male_mask = gender == 'male'
    y_pred[male_mask] = np.where(y_true[male_mask] == 1, 
                                np.random.binomial(1, 0.8, np.sum(male_mask)),
                                np.random.binomial(1, 0.2, np.sum(male_mask)))
    
    # Female group: lower TPR, higher FPR
    female_mask = gender == 'female'
    y_pred[female_mask] = np.where(y_true[female_mask] == 1,
                                  np.random.binomial(1, 0.6, np.sum(female_mask)),
                                  np.random.binomial(1, 0.4, np.sum(female_mask)))
    
    # Test analyzer
    analyzer = EqualizedOddsAnalyzer()
    result = analyzer.calculate_equalized_odds(y_true, y_pred, gender)
    
    print("✅ Equalized odds analysis completed")
    print(f"✅ Equalized odds score: {result.equalized_odds_score:.3f}")
    print(f"✅ TPR difference: {result.tpr_difference:.3f}")
    print(f"✅ FPR difference: {result.fpr_difference:.3f}")
    print(f"✅ Threshold violation: {result.threshold_violation}")
    print(f"✅ Groups: {result.groups}")
    print(f"✅ TPR by group: {result.tpr_by_group}")
    print(f"✅ FPR by group: {result.fpr_by_group}")
    
    # Test visualization
    if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
        viz_path = analyzer.create_visualization(result, "equalized_odds_viz.html")
        if viz_path:
            print(f"✅ Visualization created: {viz_path}")
    
    # Test report generation
    report = analyzer.generate_report(result)
    print(f"✅ Report generated with {len(report)} sections")


if __name__ == "__main__":
    main()
