#!/usr/bin/env python3
"""
REGIQ AI/ML - Feature Attribution
Implements feature attribution analysis, ranking, and explanation summaries.
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
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    from sklearn.model_selection import train_test_split
    from sklearn.inspection import permutation_importance
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class FeatureAttribution:
    """Feature attribution results."""
    attribution_type: str
    model_type: str
    feature_names: List[str]
    feature_importance: Dict[str, float]
    feature_rankings: List[Tuple[str, float]]
    attribution_scores: Dict[str, float]
    explanation_summary: str
    metadata: Dict[str, Any]


@dataclass
class AttributionConfig:
    """Configuration for feature attribution."""
    # Attribution settings
    n_permutations: int = 10
    random_state: int = 42
    scoring: str = "accuracy"  # accuracy, f1, roc_auc
    
    # Ranking settings
    rank_by: str = "importance"  # importance, permutation, correlation
    top_k: int = 10
    
    # Visualization settings
    show: bool = True
    save_plots: bool = True
    plot_format: str = "png"  # png, html, svg
    
    # Analysis settings
    correlation_threshold: float = 0.1
    importance_threshold: float = 0.01


class FeatureAttributionAnalyzer:
    """Feature attribution analyzer for model interpretability."""
    
    def __init__(self, config: Optional[AttributionConfig] = None):
        self.config = config or AttributionConfig()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("feature_attribution")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def calculate_feature_importance(self, model: Any, X: np.ndarray, y: np.ndarray,
                                   feature_names: Optional[List[str]] = None,
                                   method: str = "auto") -> FeatureAttribution:
        """Calculate feature importance using multiple methods."""
        try:
            if feature_names is None:
                feature_names = [f"feature_{i}" for i in range(X.shape[1])]
            
            attribution_scores = {}
            
            # Method 1: Built-in feature importance (if available)
            if hasattr(model, 'feature_importances_'):
                builtin_importance = model.feature_importances_
                attribution_scores["builtin"] = dict(zip(feature_names, builtin_importance))
                self.logger.info("Built-in feature importance calculated")
            
            # Method 2: Permutation importance
            if SKLEARN_AVAILABLE:
                perm_importance = permutation_importance(
                    model, X, y, n_repeats=self.config.n_permutations,
                    random_state=self.config.random_state, scoring=self.config.scoring
                )
                perm_scores = perm_importance.importances_mean
                attribution_scores["permutation"] = dict(zip(feature_names, perm_scores))
                self.logger.info("Permutation importance calculated")
            
            # Method 3: Correlation-based importance
            correlation_scores = self._calculate_correlation_importance(X, y, feature_names)
            attribution_scores["correlation"] = correlation_scores
            self.logger.info("Correlation importance calculated")
            
            # Combine methods for final importance
            combined_importance = self._combine_attribution_methods(attribution_scores)
            
            # Create feature rankings
            feature_rankings = sorted(combined_importance.items(), 
                                    key=lambda x: x[1], reverse=True)
            
            # Generate explanation summary
            explanation_summary = self._generate_attribution_summary(
                feature_rankings, attribution_scores
            )
            
            return FeatureAttribution(
                attribution_type="Feature Attribution",
                model_type=type(model).__name__,
                feature_names=feature_names,
                feature_importance=combined_importance,
                feature_rankings=feature_rankings,
                attribution_scores=attribution_scores,
                explanation_summary=explanation_summary,
                metadata={
                    "n_features": len(feature_names),
                    "n_samples": len(X),
                    "methods_used": list(attribution_scores.keys()),
                    "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
        except Exception as e:
            self.logger.error(f"Feature attribution calculation failed: {e}")
            raise
    
    def _calculate_correlation_importance(self, X: np.ndarray, y: np.ndarray, 
                                        feature_names: List[str]) -> Dict[str, float]:
        """Calculate correlation-based feature importance."""
        try:
            correlation_scores = {}
            
            for i, feature_name in enumerate(feature_names):
                if i < X.shape[1]:
                    # Calculate absolute correlation
                    correlation = abs(np.corrcoef(X[:, i], y)[0, 1])
                    if np.isnan(correlation):
                        correlation = 0.0
                    correlation_scores[feature_name] = float(correlation)
            
            return correlation_scores
            
        except Exception as e:
            self.logger.warning(f"Correlation importance calculation failed: {e}")
            return {name: 0.0 for name in feature_names}
    
    def _combine_attribution_methods(self, attribution_scores: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """Combine multiple attribution methods into final importance scores."""
        try:
            if not attribution_scores:
                return {}
            
            # Get all feature names
            all_features = set()
            for method_scores in attribution_scores.values():
                all_features.update(method_scores.keys())
            
            combined_scores = {}
            
            for feature in all_features:
                scores = []
                weights = []
                
                # Collect scores from all methods
                for method, method_scores in attribution_scores.items():
                    if feature in method_scores:
                        scores.append(method_scores[feature])
                        # Weight different methods
                        if method == "builtin":
                            weights.append(0.4)  # Built-in is most reliable
                        elif method == "permutation":
                            weights.append(0.4)  # Permutation is very reliable
                        elif method == "correlation":
                            weights.append(0.2)  # Correlation is less reliable
                        else:
                            weights.append(0.3)
                
                if scores:
                    # Weighted average
                    combined_score = np.average(scores, weights=weights)
                    combined_scores[feature] = float(combined_score)
                else:
                    combined_scores[feature] = 0.0
            
            return combined_scores
            
        except Exception as e:
            self.logger.warning(f"Attribution combination failed: {e}")
            return {}
    
    def _generate_attribution_summary(self, feature_rankings: List[Tuple[str, float]], 
                                    attribution_scores: Dict[str, Dict[str, float]]) -> str:
        """Generate human-readable attribution summary."""
        try:
            summary_parts = []
            
            # Top features
            top_features = feature_rankings[:3]
            for i, (feature, importance) in enumerate(top_features):
                summary_parts.append(f"Top {i+1}: {feature} ({importance:.3f})")
            
            # Method comparison
            if len(attribution_scores) > 1:
                methods = list(attribution_scores.keys())
                summary_parts.append(f"Methods: {', '.join(methods)}")
            
            # Importance distribution
            if feature_rankings:
                max_importance = max(score for _, score in feature_rankings)
                min_importance = min(score for _, score in feature_rankings)
                summary_parts.append(f"Range: {min_importance:.3f} - {max_importance:.3f}")
            
            return " | ".join(summary_parts)
            
        except Exception as e:
            self.logger.warning(f"Attribution summary generation failed: {e}")
            return "Attribution summary unavailable"
    
    def create_attribution_charts(self, attribution: FeatureAttribution, 
                                 save_path: Optional[str] = None) -> Optional[str]:
        """Create feature attribution visualization charts."""
        try:
            if not MATPLOTLIB_AVAILABLE and not PLOTLY_AVAILABLE:
                self.logger.warning("No visualization libraries available")
                return None
            
            # Set default save path if not provided
            if save_path is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_path = f"data/visualizations/attribution/attribution_analysis_{timestamp}.html"
            
            # Create visualization
            if PLOTLY_AVAILABLE:
                return self._create_plotly_attribution_charts(attribution, save_path)
            elif MATPLOTLIB_AVAILABLE:
                return self._create_matplotlib_attribution_charts(attribution, save_path)
            
        except Exception as e:
            self.logger.error(f"Attribution chart creation failed: {e}")
            return None
    
    def _create_plotly_attribution_charts(self, attribution: FeatureAttribution, 
                                         save_path: Optional[str] = None) -> str:
        """Create Plotly attribution charts."""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Feature Importance', 'Method Comparison', 
                              'Top Features', 'Attribution Summary'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "scatter"}, {"type": "indicator"}]]
            )
            
            # Feature importance bar chart
            features = list(attribution.feature_importance.keys())
            importance_values = list(attribution.feature_importance.values())
            
            fig.add_trace(
                go.Bar(x=features, y=importance_values, name='Importance', 
                      marker_color='lightblue'),
                row=1, col=1
            )
            
            # Method comparison
            if attribution.attribution_scores:
                methods = list(attribution.attribution_scores.keys())
                method_means = []
                
                for method in methods:
                    method_scores = list(attribution.attribution_scores[method].values())
                    method_means.append(np.mean(method_scores))
                
                fig.add_trace(
                    go.Bar(x=methods, y=method_means, name='Method Comparison',
                          marker_color='lightgreen'),
                    row=1, col=2
                )
            
            # Top features scatter
            top_features = attribution.feature_rankings[:10]
            if top_features:
                top_feature_names = [item[0] for item in top_features]
                top_feature_scores = [item[1] for item in top_features]
                
                fig.add_trace(
                    go.Scatter(x=top_feature_names, y=top_feature_scores, 
                             mode='markers+lines', name='Top Features',
                             marker=dict(size=10, color=top_feature_scores, 
                                       colorscale='Viridis', showscale=True)),
                    row=2, col=1
                )
            
            # Attribution summary gauge
            if importance_values:
                total_importance = sum(importance_values)
                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=total_importance,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Total Attribution"},
                        gauge={'axis': {'range': [None, total_importance * 1.2]},
                              'bar': {'color': "darkblue"},
                              'steps': [{'range': [0, total_importance * 0.5], 'color': "lightgray"},
                                       {'range': [total_importance * 0.5, total_importance], 'color': "green"}]}
                    ),
                    row=2, col=2
                )
            
            # Update layout
            fig.update_layout(
                title=f"Feature Attribution Analysis - {attribution.model_type}",
                height=800,
                showlegend=True
            )
            
            # Save or return
            if save_path:
                fig.write_html(save_path)
                self.logger.info(f"Attribution charts saved: {save_path}")
                return save_path
            else:
                return fig.to_html()
                
        except Exception as e:
            self.logger.error(f"Plotly attribution charts failed: {e}")
            return ""
    
    def _create_matplotlib_attribution_charts(self, attribution: FeatureAttribution, 
                                            save_path: Optional[str] = None) -> str:
        """Create Matplotlib attribution charts."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # Feature importance
            features = list(attribution.feature_importance.keys())
            importance_values = list(attribution.feature_importance.values())
            
            ax1.bar(features, importance_values, color='lightblue')
            ax1.set_title('Feature Importance')
            ax1.set_ylabel('Importance')
            ax1.tick_params(axis='x', rotation=45)
            
            # Method comparison
            if attribution.attribution_scores:
                methods = list(attribution.attribution_scores.keys())
                method_means = []
                
                for method in methods:
                    method_scores = list(attribution.attribution_scores[method].values())
                    method_means.append(np.mean(method_scores))
                
                ax2.bar(methods, method_means, color='lightgreen')
                ax2.set_title('Method Comparison')
                ax2.set_ylabel('Mean Score')
            
            # Top features
            top_features = attribution.feature_rankings[:10]
            if top_features:
                top_feature_names = [item[0] for item in top_features]
                top_feature_scores = [item[1] for item in top_features]
                
                ax3.plot(top_feature_names, top_feature_scores, marker='o', linewidth=2)
                ax3.set_title('Top Features Ranking')
                ax3.set_ylabel('Importance Score')
                ax3.tick_params(axis='x', rotation=45)
            
            # Attribution summary
            if importance_values:
                total_importance = sum(importance_values)
                ax4.bar(['Total Attribution'], [total_importance], color='blue')
                ax4.set_title('Total Attribution')
                ax4.set_ylabel('Total Score')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Attribution charts saved: {save_path}")
                return save_path
            else:
                return "matplotlib_figure"
                
        except Exception as e:
            self.logger.error(f"Matplotlib attribution charts failed: {e}")
            return ""
    
    def generate_explanation_summary(self, attribution: FeatureAttribution, 
                                   output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive feature attribution report."""
        try:
            report = {
                "analysis_type": "Feature Attribution",
                "model_type": attribution.model_type,
                "analysis_date": attribution.metadata.get("analysis_date", ""),
                "summary": {
                    "n_features": len(attribution.feature_names),
                    "n_samples": attribution.metadata.get("n_samples", 0),
                    "methods_used": attribution.metadata.get("methods_used", []),
                    "explanation_summary": attribution.explanation_summary
                },
                "feature_analysis": {
                    "feature_rankings": attribution.feature_rankings,
                    "top_features": attribution.feature_rankings[:5],
                    "feature_importance": attribution.feature_importance
                },
                "method_comparison": attribution.attribution_scores,
                "metadata": attribution.metadata
            }
            
            if output_path:
                with open(output_path, 'w') as f:
                    json.dump(report, f, indent=2)
                self.logger.info(f"Attribution report saved: {output_path}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Attribution report generation failed: {e}")
            return {}


def main():
    """Test the feature attribution analyzer."""
    print("🧪 Testing Feature Attribution Analyzer")
    
    if not SKLEARN_AVAILABLE:
        print("❌ scikit-learn not available")
        return
    
    # Create test data
    np.random.seed(42)
    n_samples = 200
    n_features = 5
    
    X = np.random.randn(n_samples, n_features)
    y = np.random.binomial(1, 0.6, n_samples)
    
    # Train a simple model
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    # Test feature attribution
    analyzer = FeatureAttributionAnalyzer()
    attribution = analyzer.calculate_feature_importance(model, X, y)
    
    print("✅ Feature attribution analysis completed")
    print(f"✅ Model type: {attribution.model_type}")
    print(f"✅ Methods used: {attribution.metadata['methods_used']}")
    print(f"✅ Top features: {[item[0] for item in attribution.feature_rankings[:3]]}")
    
    # Test visualization
    if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
        viz_path = analyzer.create_attribution_charts(attribution, "attribution_analysis.html")
        if viz_path:
            print(f"✅ Attribution charts created: {viz_path}")
    
    # Test report generation
    report = analyzer.generate_explanation_summary(attribution)
    print(f"✅ Report generated with {len(report)} sections")


if __name__ == "__main__":
    main()
