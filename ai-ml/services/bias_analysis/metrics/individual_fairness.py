#!/usr/bin/env python3
"""
REGIQ AI/ML - Individual Fairness Metrics
Implements individual fairness analysis, similarity metrics, and consistency scoring.
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
    from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
    from sklearn.preprocessing import StandardScaler
    from sklearn.neighbors import NearestNeighbors
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class IndividualFairnessResult:
    """Results of individual fairness analysis."""
    metric_name: str
    protected_attribute: str
    groups: List[str]
    consistency_scores: Dict[str, float]
    similarity_scores: Dict[str, float]
    fairness_maps: Dict[str, Dict[str, Any]]
    individual_reports: Dict[str, Dict[str, Any]]
    overall_consistency: float
    threshold_violation: bool
    threshold_value: float
    recommendations: List[str]
    metadata: Dict[str, Any]


@dataclass
class IndividualFairnessThreshold:
    """Threshold configuration for individual fairness."""
    consistency_threshold: float = 0.8  # Consistency score threshold
    similarity_threshold: float = 0.7  # Similarity score threshold
    min_group_size: int = 30
    n_neighbors: int = 5
    alert_enabled: bool = True


class IndividualFairnessAnalyzer:
    """Analyzes individual fairness across protected groups."""
    
    def __init__(self, threshold_config: Optional[IndividualFairnessThreshold] = None):
        self.threshold = threshold_config or IndividualFairnessThreshold()
        self.logger = self._setup_logger()
        self.env_config = get_env_config()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("individual_fairness")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def calculate_individual_fairness(self, X: np.ndarray, y_pred: np.ndarray, 
                                    protected_attribute: np.ndarray, 
                                    protected_groups: Optional[List[str]] = None) -> IndividualFairnessResult:
        """Calculate individual fairness metrics."""
        try:
            # Convert to numpy arrays if needed
            X = np.array(X)
            y_pred = np.array(y_pred)
            protected_attribute = np.array(protected_attribute)
            
            # Get unique groups
            if protected_groups is None:
                groups = np.unique(protected_attribute)
            else:
                groups = np.array(protected_groups)
            
            # Calculate metrics for each group
            consistency_scores = {}
            similarity_scores = {}
            fairness_maps = {}
            individual_reports = {}
            group_sizes = {}
            
            for group in groups:
                group_mask = protected_attribute == group
                group_size = np.sum(group_mask)
                
                if group_size < self.threshold.min_group_size:
                    self.logger.warning(f"Group {group} has only {group_size} samples (min: {self.threshold.min_group_size})")
                    continue
                
                group_X = X[group_mask]
                group_y_pred = y_pred[group_mask]
                
                # Calculate consistency score
                consistency_score = self._calculate_consistency_score(group_X, group_y_pred)
                consistency_scores[str(group)] = float(consistency_score)
                
                # Calculate similarity score
                similarity_score = self._calculate_similarity_score(group_X, group_y_pred)
                similarity_scores[str(group)] = float(similarity_score)
                
                # Generate fairness map
                fairness_map = self._generate_fairness_map(group_X, group_y_pred, str(group))
                fairness_maps[str(group)] = fairness_map
                
                # Generate individual report
                individual_report = self._generate_individual_report(
                    group_X, group_y_pred, str(group), consistency_score, similarity_score
                )
                individual_reports[str(group)] = individual_report
                
                group_sizes[str(group)] = int(group_size)
            
            # Calculate overall consistency
            overall_consistency = np.mean(list(consistency_scores.values())) if consistency_scores else 0.0
            
            # Check threshold violations
            threshold_violation = self._check_threshold_violations(consistency_scores, similarity_scores)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                consistency_scores, similarity_scores, overall_consistency, threshold_violation
            )
            
            return IndividualFairnessResult(
                metric_name="Individual Fairness",
                protected_attribute=str(protected_attribute[0]) if len(protected_attribute) > 0 else "unknown",
                groups=list(consistency_scores.keys()),
                consistency_scores=consistency_scores,
                similarity_scores=similarity_scores,
                fairness_maps=fairness_maps,
                individual_reports=individual_reports,
                overall_consistency=overall_consistency,
                threshold_violation=threshold_violation,
                threshold_value=self.threshold.consistency_threshold,
                recommendations=recommendations,
                metadata={
                    "group_sizes": group_sizes,
                    "total_samples": len(y_pred),
                    "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
        except Exception as e:
            self.logger.error(f"Individual fairness calculation failed: {e}")
            raise
    
    def _calculate_consistency_score(self, X: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate consistency score for a group."""
        try:
            if not SKLEARN_AVAILABLE or len(X) < 2:
                return 0.0
            
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Find k-nearest neighbors
            n_neighbors = min(self.threshold.n_neighbors, len(X) - 1)
            if n_neighbors < 1:
                return 0.0
            
            nbrs = NearestNeighbors(n_neighbors=n_neighbors + 1, algorithm='ball_tree')
            nbrs.fit(X_scaled)
            
            # Calculate consistency
            consistency_scores = []
            
            for i in range(len(X)):
                # Find neighbors
                distances, indices = nbrs.kneighbors([X_scaled[i]])
                neighbor_indices = indices[0][1:]  # Exclude self
                
                if len(neighbor_indices) == 0:
                    continue
                
                # Calculate prediction consistency
                current_pred = y_pred[i]
                neighbor_preds = y_pred[neighbor_indices]
                
                # Consistency is the proportion of neighbors with same prediction
                consistency = np.mean(neighbor_preds == current_pred)
                consistency_scores.append(consistency)
            
            return np.mean(consistency_scores) if consistency_scores else 0.0
            
        except Exception as e:
            self.logger.warning(f"Consistency score calculation failed: {e}")
            return 0.0
    
    def _calculate_similarity_score(self, X: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate similarity score for a group."""
        try:
            if not SKLEARN_AVAILABLE or len(X) < 2:
                return 0.0
            
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Calculate pairwise similarities
            cosine_sim = cosine_similarity(X_scaled)
            
            # Calculate prediction similarities
            pred_sim = np.abs(np.subtract.outer(y_pred, y_pred))
            pred_sim = 1 - pred_sim  # Convert to similarity
            
            # Combine feature and prediction similarities
            combined_sim = (cosine_sim + pred_sim) / 2
            
            # Calculate average similarity (excluding diagonal)
            mask = np.ones_like(combined_sim, dtype=bool)
            np.fill_diagonal(mask, False)
            
            return np.mean(combined_sim[mask]) if np.any(mask) else 0.0
            
        except Exception as e:
            self.logger.warning(f"Similarity score calculation failed: {e}")
            return 0.0
    
    def _generate_fairness_map(self, X: np.ndarray, y_pred: np.ndarray, group: str) -> Dict[str, Any]:
        """Generate fairness map for a group."""
        try:
            if not SKLEARN_AVAILABLE or len(X) < 2:
                return {"error": "Insufficient data for fairness map"}
            
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Perform clustering to identify similar individuals
            n_clusters = min(5, len(X) // 2)  # Adaptive number of clusters
            if n_clusters < 2:
                return {"error": "Insufficient data for clustering"}
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            # Calculate cluster-level fairness metrics
            cluster_metrics = {}
            for cluster_id in range(n_clusters):
                cluster_mask = cluster_labels == cluster_id
                cluster_preds = y_pred[cluster_mask]
                
                if len(cluster_preds) > 0:
                    cluster_metrics[f"cluster_{cluster_id}"] = {
                        "size": int(np.sum(cluster_mask)),
                        "positive_rate": float(np.mean(cluster_preds)),
                        "consistency": float(np.mean(cluster_preds == cluster_preds[0]) if len(cluster_preds) > 1 else 1.0)
                    }
            
            # Calculate pairwise distances
            distances = euclidean_distances(X_scaled)
            
            # Find fairness violations (similar individuals with different predictions)
            violations = []
            for i in range(len(X)):
                for j in range(i + 1, len(X)):
                    if distances[i, j] < np.percentile(distances[distances > 0], 10):  # Top 10% most similar
                        if y_pred[i] != y_pred[j]:
                            violations.append({
                                "individual_1": int(i),
                                "individual_2": int(j),
                                "distance": float(distances[i, j]),
                                "prediction_1": float(y_pred[i]),
                                "prediction_2": float(y_pred[j])
                            })
            
            return {
                "group": group,
                "total_individuals": len(X),
                "n_clusters": n_clusters,
                "cluster_metrics": cluster_metrics,
                "fairness_violations": violations,
                "violation_rate": len(violations) / (len(X) * (len(X) - 1) / 2) if len(X) > 1 else 0.0
            }
            
        except Exception as e:
            self.logger.warning(f"Fairness map generation failed: {e}")
            return {"error": str(e)}
    
    def _generate_individual_report(self, X: np.ndarray, y_pred: np.ndarray, 
                                  group: str, consistency_score: float, 
                                  similarity_score: float) -> Dict[str, Any]:
        """Generate individual report for a group."""
        try:
            # Calculate individual-level metrics
            individual_metrics = []
            
            for i in range(len(X)):
                # Find similar individuals
                distances = np.linalg.norm(X - X[i], axis=1)
                similar_indices = np.where(distances < np.percentile(distances[distances > 0], 20))[0]
                similar_indices = similar_indices[similar_indices != i]  # Exclude self
                
                if len(similar_indices) > 0:
                    similar_preds = y_pred[similar_indices]
                    consistency = np.mean(similar_preds == y_pred[i])
                    
                    individual_metrics.append({
                        "individual_id": int(i),
                        "prediction": float(y_pred[i]),
                        "n_similar": len(similar_indices),
                        "consistency": float(consistency),
                        "similar_predictions": similar_preds.tolist()
                    })
            
            # Calculate group-level statistics
            positive_rate = np.mean(y_pred)
            prediction_std = np.std(y_pred)
            
            # Identify outliers (individuals with very different predictions from similar ones)
            outliers = []
            for metric in individual_metrics:
                if metric["consistency"] < 0.5 and metric["n_similar"] > 0:
                    outliers.append(metric)
            
            return {
                "group": group,
                "group_size": len(X),
                "positive_rate": float(positive_rate),
                "prediction_std": float(prediction_std),
                "consistency_score": consistency_score,
                "similarity_score": similarity_score,
                "individual_metrics": individual_metrics,
                "outliers": outliers,
                "n_outliers": len(outliers),
                "outlier_rate": len(outliers) / len(X) if len(X) > 0 else 0.0
            }
            
        except Exception as e:
            self.logger.warning(f"Individual report generation failed: {e}")
            return {"error": str(e)}
    
    def _check_threshold_violations(self, consistency_scores: Dict[str, float], 
                                  similarity_scores: Dict[str, float]) -> bool:
        """Check if any group violates individual fairness thresholds."""
        try:
            # Check consistency violations
            consistency_violations = any(
                score < self.threshold.consistency_threshold 
                for score in consistency_scores.values()
            )
            
            # Check similarity violations
            similarity_violations = any(
                score < self.threshold.similarity_threshold 
                for score in similarity_scores.values()
            )
            
            return consistency_violations or similarity_violations
            
        except Exception as e:
            self.logger.warning(f"Threshold violation check failed: {e}")
            return False
    
    def _generate_recommendations(self, consistency_scores: Dict[str, float], 
                                similarity_scores: Dict[str, float],
                                overall_consistency: float, 
                                threshold_violation: bool) -> List[str]:
        """Generate recommendations based on individual fairness analysis."""
        recommendations = []
        
        recommendations.append(f"📊 Overall Consistency: {overall_consistency:.3f}")
        
        if threshold_violation:
            recommendations.append("⚠️ Individual fairness threshold violations detected")
            
            # Find worst performing groups
            worst_consistency_group = min(consistency_scores, key=consistency_scores.get)
            worst_similarity_group = min(similarity_scores, key=similarity_scores.get)
            
            recommendations.append(f"📊 Worst Consistency: {worst_consistency_group} ({consistency_scores[worst_consistency_group]:.3f})")
            recommendations.append(f"📊 Worst Similarity: {worst_similarity_group} ({similarity_scores[worst_similarity_group]:.3f})")
            
            recommendations.append("🔧 Recommendations:")
            recommendations.append("  • Review model for individual-level bias")
            recommendations.append("  • Implement similarity-based constraints")
            recommendations.append("  • Use adversarial training for fairness")
            recommendations.append("  • Apply post-processing techniques")
            recommendations.append("  • Increase training data for underrepresented groups")
        else:
            recommendations.append("✅ Individual fairness maintained within threshold")
            recommendations.append("📊 All groups show good individual fairness")
        
        return recommendations
    
    def create_visualization(self, result: IndividualFairnessResult, 
                           save_path: Optional[str] = None) -> Optional[str]:
        """Create individual fairness visualization."""
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
    
    def _create_plotly_visualization(self, result: IndividualFairnessResult, 
                                    save_path: Optional[str] = None) -> str:
        """Create Plotly visualization."""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Consistency Scores by Group', 'Similarity Scores by Group', 
                              'Fairness Map', 'Individual Fairness Overview'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "scatter"}, {"type": "indicator"}]]
            )
            
            groups = result.groups
            
            # Consistency scores bar chart
            consistency_values = [result.consistency_scores[group] for group in groups]
            colors = ['red' if score < result.threshold_value else 'green' for score in consistency_values]
            fig.add_trace(
                go.Bar(x=groups, y=consistency_values, name='Consistency Score', 
                      marker_color=colors),
                row=1, col=1
            )
            
            # Similarity scores bar chart
            similarity_values = [result.similarity_scores[group] for group in groups]
            colors = ['red' if score < self.threshold.similarity_threshold else 'green' for score in similarity_values]
            fig.add_trace(
                go.Bar(x=groups, y=similarity_values, name='Similarity Score', 
                      marker_color=colors),
                row=1, col=2
            )
            
            # Fairness map (violation rate by group)
            violation_rates = []
            for group in groups:
                if group in result.fairness_maps and "violation_rate" in result.fairness_maps[group]:
                    violation_rates.append(result.fairness_maps[group]["violation_rate"])
                else:
                    violation_rates.append(0.0)
            
            fig.add_trace(
                go.Scatter(x=groups, y=violation_rates, mode='markers+lines', 
                          name='Violation Rate', marker=dict(size=10)),
                row=2, col=1
            )
            
            # Individual fairness overview gauge
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=result.overall_consistency,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Overall Consistency"},
                    gauge={'axis': {'range': [None, 1]},
                          'bar': {'color': "darkblue"},
                          'steps': [{'range': [0, 0.5], 'color': "lightgray"},
                                   {'range': [0.5, 0.8], 'color': "yellow"},
                                   {'range': [0.8, 1], 'color': "green"}],
                          'threshold': {'line': {'color': "red", 'width': 4},
                                      'thickness': 0.75, 'value': 0.8}}
                ),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title=f"Individual Fairness Analysis - {result.protected_attribute}",
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
    
    def _create_matplotlib_visualization(self, result: IndividualFairnessResult, 
                                       save_path: Optional[str] = None) -> str:
        """Create Matplotlib visualization."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            groups = result.groups
            
            # Consistency scores bar chart
            consistency_values = [result.consistency_scores[group] for group in groups]
            colors = ['red' if score < result.threshold_value else 'green' for score in consistency_values]
            ax1.bar(groups, consistency_values, color=colors)
            ax1.axhline(y=result.threshold_value, color='red', linestyle='--', label='Threshold')
            ax1.set_title('Consistency Scores by Group')
            ax1.set_ylabel('Consistency Score')
            ax1.legend()
            
            # Similarity scores bar chart
            similarity_values = [result.similarity_scores[group] for group in groups]
            colors = ['red' if score < self.threshold.similarity_threshold else 'green' for score in similarity_values]
            ax2.bar(groups, similarity_values, color=colors)
            ax2.axhline(y=self.threshold.similarity_threshold, color='red', linestyle='--', label='Threshold')
            ax2.set_title('Similarity Scores by Group')
            ax2.set_ylabel('Similarity Score')
            ax2.legend()
            
            # Fairness map (violation rate by group)
            violation_rates = []
            for group in groups:
                if group in result.fairness_maps and "violation_rate" in result.fairness_maps[group]:
                    violation_rates.append(result.fairness_maps[group]["violation_rate"])
                else:
                    violation_rates.append(0.0)
            
            ax3.plot(groups, violation_rates, marker='o', linewidth=2, markersize=8)
            ax3.set_title('Fairness Violation Rate by Group')
            ax3.set_ylabel('Violation Rate')
            ax3.set_xlabel('Group')
            
            # Individual fairness overview
            ax4.bar(['Overall Consistency'], [result.overall_consistency], color='blue')
            ax4.set_ylim(0, 1)
            ax4.set_title('Overall Consistency')
            ax4.set_ylabel('Score')
            
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
    
    def generate_report(self, result: IndividualFairnessResult, 
                       output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive individual fairness report."""
        try:
            report = {
                "analysis_type": "Individual Fairness",
                "protected_attribute": result.protected_attribute,
                "analysis_date": result.metadata.get("analysis_date", ""),
                "summary": {
                    "overall_consistency": result.overall_consistency,
                    "threshold_violation": result.threshold_violation,
                    "avg_consistency": np.mean(list(result.consistency_scores.values())),
                    "avg_similarity": np.mean(list(result.similarity_scores.values()))
                },
                "group_analysis": {
                    "groups": result.groups,
                    "consistency_scores": result.consistency_scores,
                    "similarity_scores": result.similarity_scores,
                    "group_sizes": result.metadata.get("group_sizes", {})
                },
                "fairness_maps": result.fairness_maps,
                "individual_reports": result.individual_reports,
                "thresholds": {
                    "consistency_threshold": self.threshold.consistency_threshold,
                    "similarity_threshold": self.threshold.similarity_threshold,
                    "min_group_size": self.threshold.min_group_size,
                    "n_neighbors": self.threshold.n_neighbors
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
    """Test the individual fairness analyzer."""
    print("🧪 Testing Individual Fairness Analyzer")
    
    # Create test data
    np.random.seed(42)
    n_samples = 200
    
    # Create protected attribute (gender)
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    
    # Create features
    X = np.random.randn(n_samples, 5)
    
    # Create biased predictions
    y_pred = np.zeros(n_samples)
    
    # Male group: more consistent predictions
    male_mask = gender == 'male'
    y_pred[male_mask] = np.random.binomial(1, 0.7, np.sum(male_mask))
    
    # Female group: less consistent predictions
    female_mask = gender == 'female'
    y_pred[female_mask] = np.random.binomial(1, 0.5, np.sum(female_mask))
    
    # Test analyzer
    analyzer = IndividualFairnessAnalyzer()
    result = analyzer.calculate_individual_fairness(X, y_pred, gender)
    
    print("✅ Individual fairness analysis completed")
    print(f"✅ Overall consistency: {result.overall_consistency:.3f}")
    print(f"✅ Threshold violation: {result.threshold_violation}")
    print(f"✅ Groups: {result.groups}")
    print(f"✅ Consistency scores: {result.consistency_scores}")
    print(f"✅ Similarity scores: {result.similarity_scores}")
    
    # Test visualization
    if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
        viz_path = analyzer.create_visualization(result, "individual_fairness_viz.html")
        if viz_path:
            print(f"✅ Visualization created: {viz_path}")
    
    # Test report generation
    report = analyzer.generate_report(result)
    print(f"✅ Report generated with {len(report)} sections")


if __name__ == "__main__":
    main()
