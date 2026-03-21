#!/usr/bin/env python3
"""
REGIQ AI/ML - Bias Analysis Visualizer
Generates charts and plots for bias analysis results.

Provides:
    - Fairness metric bar charts (group comparisons)
    - Demographic parity plots
    - Equalized odds ROC plots
    - Calibration curves
    - SHAP summary plots (HTML-embeddable)
    - Before/after mitigation comparison charts
    - Risk score distribution plots

All outputs are returned as base64-encoded PNG strings for
embedding in HTML reports or saving to disk.

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import io
import base64
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend — safe for servers
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ── Colour palette aligned with REGIQ report CSS ──────────────────────── #
COLORS = {
    "primary":   "#1E3A5F",
    "accent":    "#2E86AB",
    "success":   "#27AE60",
    "warning":   "#F39C12",
    "danger":    "#E74C3C",
    "neutral":   "#718096",
    "light":     "#EBF8FF",
}

GROUP_PALETTE = [
    "#2E86AB", "#27AE60", "#F39C12", "#E74C3C",
    "#9B59B6", "#1ABC9C", "#E67E22", "#3498DB",
]


def _fig_to_base64(fig) -> str:
    """Convert a matplotlib figure to a base64 PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded


def _fallback_svg(title: str, message: str = "matplotlib not available") -> str:
    """Return a simple SVG placeholder when matplotlib is unavailable."""
    return (
        f'<svg width="600" height="120" xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="100%" height="100%" fill="#F8FAFC" rx="8"/>'
        f'<text x="50%" y="45%" text-anchor="middle" font-family="Arial" '
        f'font-size="14" fill="#1E3A5F" font-weight="bold">{title}</text>'
        f'<text x="50%" y="65%" text-anchor="middle" font-family="Arial" '
        f'font-size="11" fill="#718096">{message}</text>'
        f'</svg>'
    )


class BiasVisualizer:
    """
    Generates publication-quality visualizations for bias analysis results.

    All chart methods return a base64 PNG string (or SVG fallback string)
    suitable for embedding directly in HTML reports via:
        <img src="data:image/png;base64,{result}"/>
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    # ------------------------------------------------------------------ #
    # Fairness Metrics Bar Chart                                           #
    # ------------------------------------------------------------------ #

    def plot_fairness_metrics(
        self,
        metrics: Dict[str, float],
        title: str = "Fairness Metrics Overview",
        threshold: float = 0.8,
    ) -> str:
        """
        Horizontal bar chart of all fairness metrics with pass/fail colouring.

        Args:
            metrics:   Dict of {metric_name: score_0_to_1}.
            title:     Chart title.
            threshold: Score below which a metric is flagged (red).

        Returns:
            Base64 PNG string.
        """
        if not MATPLOTLIB_AVAILABLE:
            return _fallback_svg(title)

        labels = [k.replace("_", " ").title() for k in metrics.keys()]
        values = list(metrics.values())
        colors = [
            COLORS["success"] if v >= threshold else
            COLORS["warning"] if v >= 0.6 else
            COLORS["danger"]
            for v in values
        ]

        fig, ax = plt.subplots(figsize=(9, max(3, len(labels) * 0.6 + 1)))
        bars = ax.barh(labels, values, color=colors, edgecolor="white", height=0.6)

        # Threshold line
        ax.axvline(threshold, color=COLORS["primary"], linestyle="--",
                   linewidth=1.2, alpha=0.7, label=f"Threshold ({threshold})")

        # Value labels
        for bar, val in zip(bars, values):
            ax.text(min(val + 0.01, 0.97), bar.get_y() + bar.get_height() / 2,
                    f"{val:.3f}", va="center", ha="left",
                    fontsize=9, color=COLORS["primary"], fontweight="600")

        ax.set_xlim(0, 1.05)
        ax.set_xlabel("Score", fontsize=10, color=COLORS["neutral"])
        ax.set_title(title, fontsize=12, fontweight="bold",
                     color=COLORS["primary"], pad=12)
        ax.legend(fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9)
        fig.tight_layout()

        return _fig_to_base64(fig)

    # ------------------------------------------------------------------ #
    # Group Comparison Chart                                               #
    # ------------------------------------------------------------------ #

    def plot_group_comparison(
        self,
        group_rates: Dict[str, float],
        metric_name: str = "Positive Prediction Rate",
        protected_attribute: str = "Protected Attribute",
    ) -> str:
        """
        Bar chart comparing prediction rates across demographic groups.

        Args:
            group_rates: Dict of {group_name: rate}.
            metric_name: Label for the y-axis.
            protected_attribute: Label for the x-axis / chart subtitle.

        Returns:
            Base64 PNG string.
        """
        if not MATPLOTLIB_AVAILABLE:
            return _fallback_svg(f"{metric_name} by Group")

        groups = list(group_rates.keys())
        rates = list(group_rates.values())
        bar_colors = GROUP_PALETTE[:len(groups)]

        fig, ax = plt.subplots(figsize=(max(6, len(groups) * 1.2), 4.5))
        bars = ax.bar(groups, rates, color=bar_colors, edgecolor="white",
                      width=0.6, zorder=3)

        # 80% rule reference line
        if rates:
            max_rate = max(rates)
            ax.axhline(max_rate * 0.8, color=COLORS["danger"], linestyle="--",
                       linewidth=1.2, alpha=0.8, label="80% Rule threshold")

        # Value labels on top of bars
        for bar, val in zip(bars, rates):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f"{val:.3f}", ha="center", va="bottom",
                    fontsize=9, fontweight="600", color=COLORS["primary"])

        ax.set_ylabel(metric_name, fontsize=10, color=COLORS["neutral"])
        ax.set_xlabel(protected_attribute, fontsize=10, color=COLORS["neutral"])
        ax.set_title(
            f"{metric_name} by {protected_attribute}",
            fontsize=12, fontweight="bold", color=COLORS["primary"], pad=12,
        )
        ax.set_ylim(0, min(1.15, max(rates) * 1.25) if rates else 1.15)
        ax.legend(fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.3, zorder=0)
        ax.tick_params(labelsize=9)
        fig.tight_layout()

        return _fig_to_base64(fig)

    # ------------------------------------------------------------------ #
    # Before / After Mitigation Comparison                                 #
    # ------------------------------------------------------------------ #

    def plot_mitigation_comparison(
        self,
        before_metrics: Dict[str, float],
        after_metrics: Dict[str, float],
        title: str = "Bias Mitigation: Before vs After",
    ) -> str:
        """
        Grouped bar chart comparing fairness metrics before and after mitigation.

        Args:
            before_metrics: Metric scores before mitigation.
            after_metrics:  Metric scores after mitigation.
            title:          Chart title.

        Returns:
            Base64 PNG string.
        """
        if not MATPLOTLIB_AVAILABLE:
            return _fallback_svg(title)

        common_keys = [k for k in before_metrics if k in after_metrics]
        labels = [k.replace("_", " ").title() for k in common_keys]
        before_vals = [before_metrics[k] for k in common_keys]
        after_vals = [after_metrics[k] for k in common_keys]

        x = range(len(labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(max(7, len(labels) * 1.4), 4.5))
        b1 = ax.bar([i - width / 2 for i in x], before_vals, width,
                    label="Before Mitigation", color=COLORS["danger"],
                    alpha=0.85, edgecolor="white")
        b2 = ax.bar([i + width / 2 for i in x], after_vals, width,
                    label="After Mitigation", color=COLORS["success"],
                    alpha=0.85, edgecolor="white")

        ax.axhline(0.8, color=COLORS["primary"], linestyle="--",
                   linewidth=1.2, alpha=0.6, label="Threshold (0.80)")

        for bar, val in zip(list(b1) + list(b2), before_vals + after_vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.01,
                    f"{val:.2f}", ha="center", va="bottom",
                    fontsize=8, fontweight="600")

        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_ylabel("Score", fontsize=10, color=COLORS["neutral"])
        ax.set_ylim(0, 1.15)
        ax.set_title(title, fontsize=12, fontweight="bold",
                     color=COLORS["primary"], pad=12)
        ax.legend(fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        ax.tick_params(labelsize=9)
        fig.tight_layout()

        return _fig_to_base64(fig)

    # ------------------------------------------------------------------ #
    # Calibration Curve                                                    #
    # ------------------------------------------------------------------ #

    def plot_calibration_curve(
        self,
        fraction_of_positives: List[float],
        mean_predicted_values: List[float],
        group_name: str = "Overall",
    ) -> str:
        """
        Plot calibration curve (reliability diagram).

        Args:
            fraction_of_positives: Empirical positive fraction per bin.
            mean_predicted_values: Mean predicted probability per bin.
            group_name:            Label for the curve.

        Returns:
            Base64 PNG string.
        """
        if not MATPLOTLIB_AVAILABLE:
            return _fallback_svg("Calibration Curve")

        fig, ax = plt.subplots(figsize=(6, 5))

        # Perfect calibration diagonal
        ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5, label="Perfect calibration")
        # Actual calibration
        ax.plot(mean_predicted_values, fraction_of_positives,
                "o-", color=COLORS["accent"], linewidth=2,
                markersize=6, label=group_name)

        ax.fill_between(mean_predicted_values, fraction_of_positives,
                        mean_predicted_values,
                        alpha=0.08, color=COLORS["danger"])

        ax.set_xlabel("Mean Predicted Probability", fontsize=10)
        ax.set_ylabel("Fraction of Positives", fontsize=10)
        ax.set_title("Calibration Curve (Reliability Diagram)",
                     fontsize=12, fontweight="bold", color=COLORS["primary"])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.legend(fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.25)
        fig.tight_layout()

        return _fig_to_base64(fig)

    # ------------------------------------------------------------------ #
    # Feature Importance / SHAP Bar Chart                                  #
    # ------------------------------------------------------------------ #

    def plot_feature_importance(
        self,
        feature_importances: Dict[str, float],
        title: str = "Feature Importance (SHAP)",
        top_n: int = 15,
    ) -> str:
        """
        Horizontal bar chart of feature importances (SHAP or permutation).

        Args:
            feature_importances: Dict of {feature_name: importance_value}.
            title:               Chart title.
            top_n:               Number of top features to display.

        Returns:
            Base64 PNG string.
        """
        if not MATPLOTLIB_AVAILABLE:
            return _fallback_svg(title)

        sorted_items = sorted(
            feature_importances.items(), key=lambda x: abs(x[1]), reverse=True
        )[:top_n]

        labels = [k.replace("_", " ").title() for k, _ in sorted_items]
        values = [v for _, v in sorted_items]
        colors = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in values]

        fig, ax = plt.subplots(figsize=(9, max(3, len(labels) * 0.55 + 1)))
        ax.barh(labels[::-1], values[::-1], color=colors[::-1],
                edgecolor="white", height=0.65)

        ax.axvline(0, color=COLORS["neutral"], linewidth=0.8)
        ax.set_xlabel("SHAP Value (impact on model output)", fontsize=10)
        ax.set_title(title, fontsize=12, fontweight="bold",
                     color=COLORS["primary"], pad=12)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9)
        fig.tight_layout()

        return _fig_to_base64(fig)

    # ------------------------------------------------------------------ #
    # Risk Score Distribution                                              #
    # ------------------------------------------------------------------ #

    def plot_score_distribution(
        self,
        scores_by_group: Dict[str, List[float]],
        title: str = "Risk Score Distribution by Group",
    ) -> str:
        """
        Overlapping histogram of risk scores per demographic group.

        Args:
            scores_by_group: Dict of {group_name: [score, ...]}.
            title:           Chart title.

        Returns:
            Base64 PNG string.
        """
        if not MATPLOTLIB_AVAILABLE:
            return _fallback_svg(title)

        fig, ax = plt.subplots(figsize=(9, 4.5))

        for idx, (group, scores) in enumerate(scores_by_group.items()):
            color = GROUP_PALETTE[idx % len(GROUP_PALETTE)]
            ax.hist(scores, bins=30, alpha=0.55, color=color,
                    label=group, edgecolor="white", linewidth=0.4)

        ax.set_xlabel("Predicted Score", fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.set_title(title, fontsize=12, fontweight="bold",
                     color=COLORS["primary"], pad=12)
        ax.legend(fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()

        return _fig_to_base64(fig)

    # ------------------------------------------------------------------ #
    # Bias Analysis Summary Dashboard                                      #
    # ------------------------------------------------------------------ #

    def plot_summary_dashboard(
        self,
        overall_score: float,
        metrics: Dict[str, float],
        group_rates: Optional[Dict[str, float]] = None,
        before_metrics: Optional[Dict[str, float]] = None,
        after_metrics: Optional[Dict[str, float]] = None,
    ) -> str:
        """
        Composite 2×2 dashboard: overall score gauge, metrics bar,
        group comparison, and mitigation comparison.

        Returns:
            Base64 PNG string.
        """
        if not MATPLOTLIB_AVAILABLE:
            return _fallback_svg("Bias Analysis Dashboard")

        fig = plt.figure(figsize=(14, 10))
        fig.suptitle("REGIQ Bias Analysis Dashboard",
                     fontsize=14, fontweight="bold",
                     color=COLORS["primary"], y=0.98)

        # ── Top left: Overall score gauge (simple) ── #
        ax1 = fig.add_subplot(2, 2, 1)
        score_color = (
            COLORS["success"] if overall_score >= 0.8 else
            COLORS["warning"] if overall_score >= 0.6 else
            COLORS["danger"]
        )
        ax1.pie(
            [overall_score, 1 - overall_score],
            colors=[score_color, "#E2E8F0"],
            startangle=90,
            wedgeprops={"linewidth": 0},
        )
        ax1.text(0, 0, f"{overall_score:.2f}", ha="center", va="center",
                 fontsize=22, fontweight="bold", color=score_color)
        ax1.set_title("Overall Bias Score", fontsize=11,
                      fontweight="bold", color=COLORS["primary"])

        # ── Top right: Fairness metrics ── #
        ax2 = fig.add_subplot(2, 2, 2)
        if metrics:
            labels = [k.replace("_", " ").title() for k in metrics]
            vals = list(metrics.values())
            bar_colors = [
                COLORS["success"] if v >= 0.8 else
                COLORS["warning"] if v >= 0.6 else COLORS["danger"]
                for v in vals
            ]
            ax2.barh(labels, vals, color=bar_colors, edgecolor="white")
            ax2.axvline(0.8, color=COLORS["primary"], linestyle="--",
                        linewidth=1, alpha=0.6)
            ax2.set_xlim(0, 1.1)
        ax2.set_title("Fairness Metrics", fontsize=11,
                      fontweight="bold", color=COLORS["primary"])
        ax2.spines[["top", "right"]].set_visible(False)

        # ── Bottom left: Group comparison ── #
        ax3 = fig.add_subplot(2, 2, 3)
        if group_rates:
            groups = list(group_rates.keys())
            rates = list(group_rates.values())
            ax3.bar(groups, rates,
                    color=GROUP_PALETTE[:len(groups)], edgecolor="white")
            if rates:
                ax3.axhline(max(rates) * 0.8, color=COLORS["danger"],
                            linestyle="--", linewidth=1, alpha=0.7)
        ax3.set_title("Group Prediction Rates", fontsize=11,
                      fontweight="bold", color=COLORS["primary"])
        ax3.spines[["top", "right"]].set_visible(False)

        # ── Bottom right: Before/after mitigation ── #
        ax4 = fig.add_subplot(2, 2, 4)
        if before_metrics and after_metrics:
            keys = [k for k in before_metrics if k in after_metrics]
            x = range(len(keys))
            w = 0.35
            ax4.bar([i - w / 2 for i in x],
                    [before_metrics[k] for k in keys],
                    w, label="Before", color=COLORS["danger"], alpha=0.8)
            ax4.bar([i + w / 2 for i in x],
                    [after_metrics[k] for k in keys],
                    w, label="After", color=COLORS["success"], alpha=0.8)
            ax4.set_xticks(list(x))
            ax4.set_xticklabels(
                [k.replace("_", " ").title()[:12] for k in keys],
                fontsize=8, rotation=20, ha="right",
            )
            ax4.legend(fontsize=8)
            ax4.axhline(0.8, color=COLORS["primary"], linestyle="--",
                        linewidth=1, alpha=0.5)
        ax4.set_title("Mitigation Comparison", fontsize=11,
                      fontweight="bold", color=COLORS["primary"])
        ax4.spines[["top", "right"]].set_visible(False)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        return _fig_to_base64(fig)
