#!/usr/bin/env python3
"""
REGIQ AI/ML - LIME Implementation
Implements LIME explainer for local explanations and interactive visualizations.
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
    import lime
    import lime.lime_tabular
    import lime.lime_text
    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False

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
class LIMEExplanation:
    """LIME explanation results."""
    explanation_type: str
    model_type: str
    feature_names: List[str]
    feature_importance: Dict[str, float]
    local_explanation: Dict[str, Any]
    prediction: float
    confidence: float
    explanation_summary: str
    metadata: Dict[str, Any]


@dataclass
class LIMEConfig:
    """Configuration for LIME explainers."""
    # Explainer settings
    num_features: int = 10
    num_samples: int = 5000
    random_state: int = 42
    
    # Explanation settings
    mode: str = "classification"  # classification, regression
    discretize_continuous: bool = True
    discretizer: str = "quartile"  # quartile, decile, entropy
    
    # Visualization settings
    show: bool = True
    save_plots: bool = True
    plot_format: str = "png"  # png, html, svg
    
    # Model-specific settings
    tabular_explainer: bool = True
    text_explainer: bool = False
    image_explainer: bool = False


class LIMEExplainer:
    """LIME explainer for local model interpretability."""
    
    def __init__(self, config: Optional[LIMEConfig] = None):
        self.config = config or LIMEConfig()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        
        if not LIME_AVAILABLE:
            self.logger.error("LIME library not available. Install with: pip install lime")
            raise ImportError("LIME library is required")
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("lime_explainer")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def create_tabular_explainer(self, X: np.ndarray, 
                               feature_names: Optional[List[str]] = None,
                               class_names: Optional[List[str]] = None) -> Any:
        """Create LIME tabular explainer."""
        try:
            if feature_names is None:
                feature_names = [f"feature_{i}" for i in range(X.shape[1])]
            
            if class_names is None:
                class_names = ["class_0", "class_1"]
            
            explainer = lime.lime_tabular.LimeTabularExplainer(
                X,
                feature_names=feature_names,
                class_names=class_names,
                mode=self.config.mode,
                discretize_continuous=self.config.discretize_continuous,
                discretizer=self.config.discretizer,
                random_state=self.config.random_state
            )
            
            self.logger.info("LIME tabular explainer created")
            return explainer
            
        except Exception as e:
            self.logger.error(f"Failed to create LIME tabular explainer: {e}")
            raise
    
    def create_text_explainer(self, class_names: Optional[List[str]] = None) -> Any:
        """Create LIME text explainer."""
        try:
            if class_names is None:
                class_names = ["class_0", "class_1"]
            
            explainer = lime.lime_text.LimeTextExplainer(
                class_names=class_names,
                random_state=self.config.random_state
            )
            
            self.logger.info("LIME text explainer created")
            return explainer
            
        except Exception as e:
            self.logger.error(f"Failed to create LIME text explainer: {e}")
            raise
    
    def explain_instance(self, explainer: Any, model: Any, instance: np.ndarray,
                        feature_names: Optional[List[str]] = None,
                        num_features: Optional[int] = None) -> LIMEExplanation:
        """Generate LIME explanation for a single instance."""
        try:
            if num_features is None:
                num_features = self.config.num_features
            
            # Generate explanation
            explanation = explainer.explain_instance(
                instance,
                model.predict_proba,
                num_features=num_features,
                num_samples=self.config.num_samples
            )
            
            # Extract explanation data
            explanation_list = explanation.as_list()
            feature_importance = {item[0]: item[1] for item in explanation_list}
            
            # Get prediction and confidence
            prediction = model.predict(instance.reshape(1, -1))[0]
            prediction_proba = model.predict_proba(instance.reshape(1, -1))[0]
            confidence = float(np.max(prediction_proba))
            
            # Generate explanation summary
            explanation_summary = self._generate_explanation_summary(
                explanation_list, prediction, confidence
            )
            
            # Create local explanation dictionary
            local_explanation = {
                "explanation_list": explanation_list,
                "prediction_proba": prediction_proba.tolist(),
                "top_features": explanation_list[:5],  # Top 5 features
                "feature_weights": {item[0]: item[1] for item in explanation_list}
            }
            
            return LIMEExplanation(
                explanation_type="LIME",
                model_type=type(model).__name__,
                feature_names=feature_names or [f"feature_{i}" for i in range(len(instance))],
                feature_importance=feature_importance,
                local_explanation=local_explanation,
                prediction=float(prediction),
                confidence=confidence,
                explanation_summary=explanation_summary,
                metadata={
                    "num_features": num_features,
                    "num_samples": self.config.num_samples,
                    "explainer_type": type(explainer).__name__,
                    "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
        except Exception as e:
            self.logger.error(f"LIME explanation generation failed: {e}")
            raise
    
    def _generate_explanation_summary(self, explanation_list: List[Tuple[str, float]], 
                                    prediction: float, confidence: float) -> str:
        """Generate human-readable explanation summary."""
        try:
            summary_parts = []
            
            # Prediction and confidence
            summary_parts.append(f"Prediction: {prediction:.0f} (confidence: {confidence:.3f})")
            
            # Top contributing features
            top_features = explanation_list[:3]
            for i, (feature, weight) in enumerate(top_features):
                direction = "increases" if weight > 0 else "decreases"
                summary_parts.append(f"Top {i+1}: {feature} {direction} prediction by {abs(weight):.3f}")
            
            return " | ".join(summary_parts)
            
        except Exception as e:
            self.logger.warning(f"Explanation summary generation failed: {e}")
            return "Explanation summary unavailable"
    
    def create_visualization(self, explanation: LIMEExplanation, 
                           save_path: Optional[str] = None) -> Optional[str]:
        """Create LIME visualization."""
        try:
            if not MATPLOTLIB_AVAILABLE and not PLOTLY_AVAILABLE:
                self.logger.warning("No visualization libraries available")
                return None
            
            # Set default save path if not provided
            if save_path is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_path = f"data/visualizations/lime/lime_analysis_{timestamp}.html"
            
            # Create visualization
            if PLOTLY_AVAILABLE:
                return self._create_plotly_visualization(explanation, save_path)
            elif MATPLOTLIB_AVAILABLE:
                return self._create_matplotlib_visualization(explanation, save_path)
            
        except Exception as e:
            self.logger.error(f"Visualization creation failed: {e}")
            return None
    
    def _create_plotly_visualization(self, explanation: LIMEExplanation, 
                                    save_path: Optional[str] = None) -> str:
        """Create Plotly LIME visualization."""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Feature Importance', 'Local Explanation', 
                              'Prediction Confidence', 'Feature Weights'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "indicator"}, {"type": "scatter"}]]
            )
            
            # Feature importance bar chart
            features = list(explanation.feature_importance.keys())
            importance_values = list(explanation.feature_importance.values())
            
            fig.add_trace(
                go.Bar(x=features, y=importance_values, name='Importance', 
                      marker_color=['red' if v < 0 else 'green' for v in importance_values]),
                row=1, col=1
            )
            
            # Local explanation (top features)
            top_features = explanation.local_explanation.get("top_features", [])
            if top_features:
                top_feature_names = [item[0] for item in top_features]
                top_feature_weights = [item[1] for item in top_features]
                
                fig.add_trace(
                    go.Bar(x=top_feature_names, y=top_feature_weights, name='Top Features',
                          marker_color=['red' if v < 0 else 'green' for v in top_feature_weights]),
                    row=1, col=2
                )
            
            # Prediction confidence gauge
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=explanation.confidence,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Prediction Confidence"},
                    gauge={'axis': {'range': [None, 1]},
                          'bar': {'color': "darkblue"},
                          'steps': [{'range': [0, 0.5], 'color': "lightgray"},
                                   {'range': [0.5, 0.8], 'color': "yellow"},
                                   {'range': [0.8, 1], 'color': "green"}],
                          'threshold': {'line': {'color': "red", 'width': 4},
                                      'thickness': 0.75, 'value': 0.8}}
                ),
                row=2, col=1
            )
            
            # Feature weights scatter
            if features and importance_values:
                fig.add_trace(
                    go.Scatter(x=features, y=importance_values, mode='markers', 
                             name='Feature Weights',
                             marker=dict(size=10, color=importance_values, 
                                       colorscale='RdBu', showscale=True)),
                    row=2, col=2
                )
            
            # Update layout
            fig.update_layout(
                title=f"LIME Analysis - {explanation.model_type}",
                height=800,
                showlegend=True
            )
            
            # Save or return
            if save_path:
                fig.write_html(save_path)
                self.logger.info(f"LIME visualization saved: {save_path}")
                return save_path
            else:
                return fig.to_html()
                
        except Exception as e:
            self.logger.error(f"Plotly LIME visualization failed: {e}")
            return ""
    
    def _create_matplotlib_visualization(self, explanation: LIMEExplanation, 
                                       save_path: Optional[str] = None) -> str:
        """Create Matplotlib LIME visualization."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # Feature importance
            features = list(explanation.feature_importance.keys())
            importance_values = list(explanation.feature_importance.values())
            
            colors = ['red' if v < 0 else 'green' for v in importance_values]
            ax1.bar(features, importance_values, color=colors)
            ax1.set_title('Feature Importance')
            ax1.set_ylabel('Importance')
            ax1.tick_params(axis='x', rotation=45)
            
            # Local explanation (top features)
            top_features = explanation.local_explanation.get("top_features", [])
            if top_features:
                top_feature_names = [item[0] for item in top_features]
                top_feature_weights = [item[1] for item in top_features]
                
                colors = ['red' if v < 0 else 'green' for v in top_feature_weights]
                ax2.bar(top_feature_names, top_feature_weights, color=colors)
                ax2.set_title('Top Features (Local Explanation)')
                ax2.set_ylabel('Weight')
                ax2.tick_params(axis='x', rotation=45)
            
            # Prediction confidence
            ax3.bar(['Confidence'], [explanation.confidence], color='blue')
            ax3.set_ylim(0, 1)
            ax3.set_title('Prediction Confidence')
            ax3.set_ylabel('Confidence')
            
            # Feature weights scatter
            if features and importance_values:
                ax4.scatter(features, importance_values, 
                           c=importance_values, cmap='RdBu', s=100)
                ax4.set_title('Feature Weights')
                ax4.set_ylabel('Weight')
                ax4.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"LIME visualization saved: {save_path}")
                return save_path
            else:
                return "matplotlib_figure"
                
        except Exception as e:
            self.logger.error(f"Matplotlib LIME visualization failed: {e}")
            return ""
    
    def generate_report(self, explanation: LIMEExplanation, 
                       output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive LIME report."""
        try:
            report = {
                "analysis_type": "LIME Explanation",
                "model_type": explanation.model_type,
                "analysis_date": explanation.metadata.get("analysis_date", ""),
                "summary": {
                    "prediction": explanation.prediction,
                    "confidence": explanation.confidence,
                    "explanation_summary": explanation.explanation_summary,
                    "n_features": len(explanation.feature_names),
                    "num_samples": explanation.metadata.get("num_samples", 0)
                },
                "local_explanation": explanation.local_explanation,
                "feature_analysis": {
                    "feature_names": explanation.feature_names,
                    "feature_importance": explanation.feature_importance,
                    "top_features": explanation.local_explanation.get("top_features", [])[:5]
                },
                "metadata": explanation.metadata
            }
            
            if output_path:
                with open(output_path, 'w') as f:
                    json.dump(report, f, indent=2)
                self.logger.info(f"LIME report saved: {output_path}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"LIME report generation failed: {e}")
            return {}


def main():
    """Test the LIME explainer."""
    print("🧪 Testing LIME Explainer")
    
    if not LIME_AVAILABLE:
        print("❌ LIME library not available. Install with: pip install lime")
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
    
    # Test LIME explainer
    explainer = LIMEExplainer()
    lime_explainer = explainer.create_tabular_explainer(X)
    
    # Generate explanation for a single instance
    instance = X[0]
    explanation = explainer.explain_instance(lime_explainer, model, instance)
    
    print("✅ LIME explanation generated")
    print(f"✅ Model type: {explanation.model_type}")
    print(f"✅ Prediction: {explanation.prediction:.0f}")
    print(f"✅ Confidence: {explanation.confidence:.3f}")
    print(f"✅ Top features: {list(explanation.feature_importance.keys())[:3]}")
    
    # Test visualization
    if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
        viz_path = explainer.create_visualization(explanation, "lime_analysis.html")
        if viz_path:
            print(f"✅ Visualization created: {viz_path}")
    
    # Test report generation
    report = explainer.generate_report(explanation)
    print(f"✅ Report generated with {len(report)} sections")


if __name__ == "__main__":
    main()
