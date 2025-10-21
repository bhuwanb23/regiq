#!/usr/bin/env python3
"""
REGIQ AI/ML - SHAP Integration
Implements SHAP explainers, feature importance, and visualizations for model explainability.
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
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

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
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class SHAPExplanation:
    """SHAP explanation results."""
    explanation_type: str
    model_type: str
    feature_names: List[str]
    feature_importance: Dict[str, float]
    shap_values: np.ndarray
    base_value: float
    prediction: float
    explanation_summary: str
    metadata: Dict[str, Any]


@dataclass
class SHAPConfig:
    """Configuration for SHAP explainers."""
    # Explainer settings
    max_samples: int = 1000
    background_samples: int = 100
    feature_perturbation: str = "interventional"
    
    # Visualization settings
    max_display: int = 10
    show: bool = True
    save_plots: bool = True
    plot_format: str = "png"  # png, html, svg
    
    # Model-specific settings
    tree_explainer: bool = True
    linear_explainer: bool = True
    kernel_explainer: bool = True
    deep_explainer: bool = False  # Requires TensorFlow/PyTorch


class SHAPExplainer:
    """SHAP explainer for model interpretability."""
    
    def __init__(self, config: Optional[SHAPConfig] = None):
        self.config = config or SHAPConfig()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        
        if not SHAP_AVAILABLE:
            self.logger.error("SHAP library not available. Install with: pip install shap")
            raise ImportError("SHAP library is required")
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("shap_explainer")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def create_explainer(self, model: Any, X: np.ndarray, 
                        model_type: str = "auto") -> Any:
        """Create appropriate SHAP explainer for the model."""
        try:
            if model_type == "auto":
                model_type = self._detect_model_type(model)
            
            self.logger.info(f"Creating SHAP explainer for {model_type} model")
            
            if model_type == "tree":
                explainer = shap.TreeExplainer(model)
            elif model_type == "linear":
                explainer = shap.LinearExplainer(model, X)
            elif model_type == "kernel":
                # Use subset of data for background
                background = X[np.random.choice(X.shape[0], 
                                              min(self.config.background_samples, X.shape[0]), 
                                              replace=False)]
                explainer = shap.KernelExplainer(model.predict, background)
            elif model_type == "deep":
                explainer = shap.DeepExplainer(model, X[:100])  # Use subset for deep models
            else:
                # Default to kernel explainer
                background = X[np.random.choice(X.shape[0], 
                                              min(self.config.background_samples, X.shape[0]), 
                                              replace=False)]
                explainer = shap.KernelExplainer(model.predict, background)
            
            self.logger.info(f"SHAP explainer created: {type(explainer).__name__}")
            return explainer
            
        except Exception as e:
            self.logger.error(f"Failed to create SHAP explainer: {e}")
            raise
    
    def _detect_model_type(self, model: Any) -> str:
        """Detect model type for appropriate explainer selection."""
        try:
            model_name = type(model).__name__.lower()
            
            if any(tree_type in model_name for tree_type in ['tree', 'forest', 'gradient', 'xgb', 'lgb']):
                return "tree"
            elif any(linear_type in model_name for linear_type in ['linear', 'logistic', 'ridge', 'lasso']):
                return "linear"
            elif any(deep_type in model_name for deep_type in ['neural', 'mlp', 'sequential']):
                return "deep"
            else:
                return "kernel"
                
        except Exception as e:
            self.logger.warning(f"Could not detect model type: {e}")
            return "kernel"
    
    def explain_prediction(self, explainer: Any, X: np.ndarray, 
                          feature_names: Optional[List[str]] = None,
                          sample_idx: Optional[int] = None) -> SHAPExplanation:
        """Generate SHAP explanation for predictions."""
        try:
            # Use single sample or all samples
            if sample_idx is not None:
                X_sample = X[sample_idx:sample_idx+1]
            else:
                X_sample = X
            
            # Limit samples for performance
            if X_sample.shape[0] > self.config.max_samples:
                indices = np.random.choice(X_sample.shape[0], self.config.max_samples, replace=False)
                X_sample = X_sample[indices]
            
            # Generate SHAP values
            shap_values = explainer.shap_values(X_sample)
            
            # Handle different explainer outputs
            if isinstance(shap_values, list):
                # Multi-class case, use first class
                shap_values = shap_values[0]
            
            # Get base value
            base_value = explainer.expected_value
            if isinstance(base_value, (list, np.ndarray)):
                base_value = base_value[0] if len(base_value) > 0 else 0.0
            elif not isinstance(base_value, (int, float)):
                base_value = 0.0
            
            # Calculate feature importance
            feature_importance = self._calculate_feature_importance(shap_values, feature_names)
            
            # Generate explanation summary
            explanation_summary = self._generate_explanation_summary(
                shap_values, feature_names, base_value
            )
            
            # Get prediction
            try:
                if hasattr(explainer, 'model'):
                    pred_result = explainer.model.predict(X_sample[0:1])
                    if isinstance(pred_result, np.ndarray):
                        prediction = float(pred_result[0]) if len(pred_result) > 0 else 0.0
                    else:
                        prediction = float(pred_result) if pred_result is not None else 0.0
                else:
                    prediction = 0.0
            except Exception:
                prediction = 0.0
            
            return SHAPExplanation(
                explanation_type="SHAP",
                model_type=type(explainer).__name__,
                feature_names=feature_names or [f"feature_{i}" for i in range(X.shape[1])],
                feature_importance=feature_importance,
                shap_values=shap_values,
                base_value=float(base_value),
                prediction=float(prediction),
                explanation_summary=explanation_summary,
                metadata={
                    "n_samples": X_sample.shape[0],
                    "n_features": X_sample.shape[1],
                    "explainer_type": type(explainer).__name__,
                    "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
        except Exception as e:
            self.logger.error(f"SHAP explanation generation failed: {e}")
            raise
    
    def _calculate_feature_importance(self, shap_values: np.ndarray, 
                                   feature_names: Optional[List[str]] = None) -> Dict[str, float]:
        """Calculate feature importance from SHAP values."""
        try:
            # Handle different SHAP value shapes
            if len(shap_values.shape) == 1:
                mean_shap = np.abs(shap_values)
            elif len(shap_values.shape) == 2:
                mean_shap = np.mean(np.abs(shap_values), axis=0)
            else:
                # For higher dimensions, flatten and take mean
                mean_shap = np.mean(np.abs(shap_values.reshape(-1, shap_values.shape[-1])), axis=0)
            
            # Create feature names if not provided
            if feature_names is None:
                feature_names = [f"feature_{i}" for i in range(len(mean_shap))]
            
            # Create importance dictionary
            importance = {}
            for i, name in enumerate(feature_names):
                if i < len(mean_shap):
                    importance[name] = float(mean_shap[i])
            
            return importance
            
        except Exception as e:
            self.logger.warning(f"Feature importance calculation failed: {e}")
            return {}
    
    def _generate_explanation_summary(self, shap_values: np.ndarray, 
                                    feature_names: Optional[List[str]] = None,
                                    base_value: float = 0.0) -> str:
        """Generate human-readable explanation summary."""
        try:
            # Handle different SHAP value shapes
            if len(shap_values.shape) == 1:
                shap_values = shap_values.reshape(1, -1)
            elif len(shap_values.shape) > 2:
                # Flatten to 2D
                shap_values = shap_values.reshape(-1, shap_values.shape[-1])
            
            # Get top contributing features
            mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
            top_indices = np.argsort(mean_abs_shap)[-3:][::-1]  # Top 3 features
            
            summary_parts = []
            
            # Base value explanation
            if base_value != 0 and not np.isnan(base_value):
                summary_parts.append(f"Base prediction: {base_value:.3f}")
            
            # Top contributing features
            for i, idx in enumerate(top_indices):
                if idx < len(mean_abs_shap):
                    feature_name = feature_names[idx] if feature_names and idx < len(feature_names) else f"Feature {idx}"
                    importance = mean_abs_shap[idx]
                    summary_parts.append(f"Top {i+1} contributor: {feature_name} ({importance:.3f})")
            
            return " | ".join(summary_parts)
            
        except Exception as e:
            self.logger.warning(f"Explanation summary generation failed: {e}")
            return "Explanation summary unavailable"
    
    def create_visualization(self, explanation: SHAPExplanation, 
                           save_path: Optional[str] = None) -> Optional[str]:
        """Create SHAP visualizations."""
        try:
            if not MATPLOTLIB_AVAILABLE and not PLOTLY_AVAILABLE:
                self.logger.warning("No visualization libraries available")
                return None
            
            # Set default save path if not provided
            if save_path is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_path = f"data/visualizations/shap/shap_analysis_{timestamp}.html"
            
            # Create visualization
            if PLOTLY_AVAILABLE:
                return self._create_plotly_visualization(explanation, save_path)
            elif MATPLOTLIB_AVAILABLE:
                return self._create_matplotlib_visualization(explanation, save_path)
            
        except Exception as e:
            self.logger.error(f"Visualization creation failed: {e}")
            return None
    
    def _create_plotly_visualization(self, explanation: SHAPExplanation, 
                                    save_path: Optional[str] = None) -> str:
        """Create Plotly SHAP visualization."""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Feature Importance', 'SHAP Values', 
                              'Feature Contributions', 'Summary'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "scatter"}, {"type": "indicator"}]]
            )
            
            # Feature importance bar chart
            features = list(explanation.feature_importance.keys())
            importance_values = list(explanation.feature_importance.values())
            
            fig.add_trace(
                go.Bar(x=features, y=importance_values, name='Importance', 
                      marker_color='lightblue'),
                row=1, col=1
            )
            
            # SHAP values (if available)
            if len(explanation.shap_values.shape) == 1:
                shap_vals = explanation.shap_values
            else:
                shap_vals = explanation.shap_values[0] if len(explanation.shap_values) > 0 else np.array([])
            
            if len(shap_vals) > 0:
                fig.add_trace(
                    go.Bar(x=features[:len(shap_vals)], y=shap_vals, name='SHAP Values',
                          marker_color=['red' if v < 0 else 'green' for v in shap_vals]),
                    row=1, col=2
                )
            
            # Feature contributions scatter
            if len(shap_vals) > 0:
                fig.add_trace(
                    go.Scatter(x=features[:len(shap_vals)], y=shap_vals, 
                             mode='markers', name='Contributions',
                             marker=dict(size=10, color=shap_vals, 
                                       colorscale='RdBu', showscale=True)),
                    row=2, col=1
                )
            
            # Summary gauge
            total_importance = sum(importance_values) if importance_values else 0
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=total_importance,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Total Importance"},
                    gauge={'axis': {'range': [None, total_importance * 1.2]},
                          'bar': {'color': "darkblue"},
                          'steps': [{'range': [0, total_importance * 0.5], 'color': "lightgray"},
                                   {'range': [total_importance * 0.5, total_importance], 'color': "green"}]}
                ),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title=f"SHAP Analysis - {explanation.model_type}",
                height=800,
                showlegend=True
            )
            
            # Save or return
            if save_path:
                fig.write_html(save_path)
                self.logger.info(f"SHAP visualization saved: {save_path}")
                return save_path
            else:
                return fig.to_html()
                
        except Exception as e:
            self.logger.error(f"Plotly SHAP visualization failed: {e}")
            return ""
    
    def _create_matplotlib_visualization(self, explanation: SHAPExplanation, 
                                       save_path: Optional[str] = None) -> str:
        """Create Matplotlib SHAP visualization."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # Feature importance
            features = list(explanation.feature_importance.keys())
            importance_values = list(explanation.feature_importance.values())
            
            ax1.bar(features, importance_values, color='lightblue')
            ax1.set_title('Feature Importance')
            ax1.set_ylabel('Importance')
            ax1.tick_params(axis='x', rotation=45)
            
            # SHAP values
            if len(explanation.shap_values.shape) == 1:
                shap_vals = explanation.shap_values
            else:
                shap_vals = explanation.shap_values[0] if len(explanation.shap_values) > 0 else np.array([])
            
            if len(shap_vals) > 0:
                colors = ['red' if v < 0 else 'green' for v in shap_vals]
                ax2.bar(features[:len(shap_vals)], shap_vals, color=colors)
                ax2.set_title('SHAP Values')
                ax2.set_ylabel('SHAP Value')
                ax2.tick_params(axis='x', rotation=45)
            
            # Feature contributions scatter
            if len(shap_vals) > 0:
                ax3.scatter(features[:len(shap_vals)], shap_vals, 
                           c=shap_vals, cmap='RdBu', s=100)
                ax3.set_title('Feature Contributions')
                ax3.set_ylabel('SHAP Value')
                ax3.tick_params(axis='x', rotation=45)
            
            # Summary
            total_importance = sum(importance_values) if importance_values else 0
            ax4.bar(['Total Importance'], [total_importance], color='blue')
            ax4.set_title('Summary')
            ax4.set_ylabel('Total Importance')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"SHAP visualization saved: {save_path}")
                return save_path
            else:
                return "matplotlib_figure"
                
        except Exception as e:
            self.logger.error(f"Matplotlib SHAP visualization failed: {e}")
            return ""
    
    def generate_report(self, explanation: SHAPExplanation, 
                       output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive SHAP report."""
        try:
            report = {
                "analysis_type": "SHAP Explanation",
                "model_type": explanation.model_type,
                "analysis_date": explanation.metadata.get("analysis_date", ""),
                "summary": {
                    "base_value": explanation.base_value,
                    "prediction": explanation.prediction,
                    "explanation_summary": explanation.explanation_summary,
                    "n_features": len(explanation.feature_names),
                    "n_samples": explanation.metadata.get("n_samples", 0)
                },
                "feature_analysis": {
                    "feature_names": explanation.feature_names,
                    "feature_importance": explanation.feature_importance,
                    "top_features": sorted(explanation.feature_importance.items(), 
                                         key=lambda x: x[1], reverse=True)[:5]
                },
                "shap_values": {
                    "shape": explanation.shap_values.shape,
                    "mean_abs_value": float(np.mean(np.abs(explanation.shap_values))),
                    "max_abs_value": float(np.max(np.abs(explanation.shap_values))),
                    "min_abs_value": float(np.min(np.abs(explanation.shap_values)))
                },
                "metadata": explanation.metadata
            }
            
            if output_path:
                with open(output_path, 'w') as f:
                    json.dump(report, f, indent=2)
                self.logger.info(f"SHAP report saved: {output_path}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"SHAP report generation failed: {e}")
            return {}


def main():
    """Test the SHAP explainer."""
    print("🧪 Testing SHAP Explainer")
    
    if not SHAP_AVAILABLE:
        print("❌ SHAP library not available. Install with: pip install shap")
        return
    
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
    
    # Test SHAP explainer
    explainer = SHAPExplainer()
    shap_explainer = explainer.create_explainer(model, X)
    
    # Generate explanation
    explanation = explainer.explain_prediction(shap_explainer, X[:10])
    
    print("✅ SHAP explanation generated")
    print(f"✅ Model type: {explanation.model_type}")
    print(f"✅ Base value: {explanation.base_value:.3f}")
    print(f"✅ Prediction: {explanation.prediction:.3f}")
    print(f"✅ Top features: {list(explanation.feature_importance.keys())[:3]}")
    
    # Test visualization
    if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
        viz_path = explainer.create_visualization(explanation, "shap_analysis.html")
        if viz_path:
            print(f"✅ Visualization created: {viz_path}")
    
    # Test report generation
    report = explainer.generate_report(explanation)
    print(f"✅ Report generated with {len(report)} sections")


if __name__ == "__main__":
    main()
