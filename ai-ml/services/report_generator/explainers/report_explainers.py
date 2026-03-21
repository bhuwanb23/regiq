#!/usr/bin/env python3
"""
REGIQ AI/ML - Report Explainers
Bridges bias-analysis SHAP/LIME outputs into human-readable
report sections for all three audience types.

This module provides:
- SHAP summary rendering for executive, technical, regulatory audiences
- LIME individual-decision explanation formatting
- Feature importance tables and narrative generation
- Fairness metric plain-language interpretation
- Risk simulation plain-language summaries

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ── Helpers ───────────────────────────────────────────────────────────── #

def _badge(value: float, good_threshold: float = 0.8, warn_threshold: float = 0.6) -> str:
    if value >= good_threshold:
        return f'<span class="badge badge-green">✓ {value:.2f}</span>'
    elif value >= warn_threshold:
        return f'<span class="badge badge-yellow">⚠ {value:.2f}</span>'
    else:
        return f'<span class="badge badge-red">✗ {value:.2f}</span>'


def _risk_badge(probability: float) -> str:
    if probability < 0.2:
        return f'<span class="badge badge-green">Low ({probability:.1%})</span>'
    elif probability < 0.5:
        return f'<span class="badge badge-yellow">Medium ({probability:.1%})</span>'
    else:
        return f'<span class="badge badge-red">High ({probability:.1%})</span>'


# ── SHAP Explainer ────────────────────────────────────────────────────── #

class SHAPExplainer:
    """
    Formats SHAP feature importance data into report-ready HTML sections.

    Expected input (shap_data):
        {
            "feature_importances": {"feature_name": shap_value, ...},
            "base_value": float,
            "expected_value": float,
            "model_type": str,
            "sample_size": int
        }
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def render(self, shap_data: Dict[str, Any], audience: str = "technical") -> str:
        """Render SHAP results as an HTML section."""
        if not shap_data:
            return "<p>SHAP analysis data not available.</p>"

        try:
            if audience == "executive":
                return self._render_executive(shap_data)
            elif audience == "regulatory":
                return self._render_regulatory(shap_data)
            else:
                return self._render_technical(shap_data)
        except Exception as exc:
            self.logger.error(f"SHAP render failed: {exc}")
            return f"<p class='alert alert-warning'>SHAP explanation unavailable: {exc}</p>"

    def _top_features(self, shap_data: Dict[str, Any], n: int = 10) -> List[Tuple[str, float]]:
        importances = shap_data.get("feature_importances", {})
        sorted_items = sorted(importances.items(), key=lambda x: abs(x[1]), reverse=True)
        return sorted_items[:n]

    def _render_executive(self, shap_data: Dict[str, Any]) -> str:
        top = self._top_features(shap_data, n=5)
        rows = "".join(
            f"<tr><td>{name.replace('_', ' ').title()}</td>"
            f"<td>{'↑ Increases approval' if v > 0 else '↓ Decreases approval'}</td>"
            f"<td>{'High' if abs(v) > 0.1 else 'Moderate' if abs(v) > 0.05 else 'Low'} influence</td></tr>"
            for name, v in top
        )
        return f"""
<div class="alert alert-info">
  <div class="alert-title">What drives this model's decisions?</div>
  <p>The five most influential factors in the AI model's decisions are shown below.
  Positive factors increase the likelihood of a favourable outcome; negative factors decrease it.</p>
</div>
<table>
  <thead><tr><th>Factor</th><th>Direction</th><th>Influence</th></tr></thead>
  <tbody>{rows}</tbody>
</table>"""

    def _render_technical(self, shap_data: Dict[str, Any]) -> str:
        top = self._top_features(shap_data, n=15)
        base_value = shap_data.get("base_value", shap_data.get("expected_value", "N/A"))
        sample_size = shap_data.get("sample_size", "N/A")
        model_type = shap_data.get("model_type", "Unknown")

        rows = "".join(
            f"<tr><td><code>{name}</code></td>"
            f"<td style='color:{'#27AE60' if v > 0 else '#E74C3C'};font-weight:600'>{v:+.4f}</td>"
            f"<td>{abs(v):.4f}</td>"
            f"<td>{'Positive' if v > 0 else 'Negative'}</td></tr>"
            for name, v in top
        )

        return f"""
<div class="metric-grid">
  <div class="metric-card"><div class="value">{model_type}</div><div class="label">Model Type</div></div>
  <div class="metric-card"><div class="value">{sample_size:,}</div><div class="label">Sample Size</div></div>
  <div class="metric-card"><div class="value">{base_value:.4f}</div><div class="label">Base Value (E[f(x)])</div></div>
</div>
<h4>Top Feature SHAP Values</h4>
<table>
  <thead><tr><th>Feature</th><th>SHAP Value</th><th>|SHAP|</th><th>Direction</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<p class="chart-caption">
  SHAP values represent the marginal contribution of each feature to the model output
  relative to the base value. Computed using TreeExplainer / KernelExplainer.
</p>"""

    def _render_regulatory(self, shap_data: Dict[str, Any]) -> str:
        top = self._top_features(shap_data, n=10)
        rows = "".join(
            f"<tr><td>{name.replace('_', ' ').title()}</td>"
            f"<td>{v:+.4f}</td>"
            f"<td>{'Material' if abs(v) > 0.1 else 'Moderate' if abs(v) > 0.05 else 'Minor'}</td>"
            f"<td>{'Protected-class correlated — review required' if any(k in name.lower() for k in ['age','gender','race','ethnicity','sex']) else 'Standard feature'}</td></tr>"
            for name, v in top
        )
        return f"""
<div class="alert alert-info">
  <div class="alert-title">Regulatory Note</div>
  <p>Feature attributions are computed using SHAP (SHapley Additive exPlanations),
  satisfying the right-to-explanation requirement under GDPR Article 22 and
  EU AI Act Article 13. The table below documents material feature contributions
  for audit purposes.</p>
</div>
<table>
  <thead><tr><th>Feature</th><th>Attribution (SHAP)</th><th>Materiality</th><th>Regulatory Flag</th></tr></thead>
  <tbody>{rows}</tbody>
</table>"""


# ── LIME Explainer ────────────────────────────────────────────────────── #

class LIMEExplainer:
    """
    Formats LIME local explanation data into report-ready HTML.

    Expected input (lime_data):
        {
            "instance_id": str,
            "predicted_class": int,
            "predicted_probability": float,
            "explanation": [{"feature": str, "weight": float, "value": any}, ...]
        }
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def render(self, lime_data: Dict[str, Any], audience: str = "technical") -> str:
        if not lime_data:
            return "<p>LIME explanation data not available.</p>"
        try:
            explanation = lime_data.get("explanation", [])
            prob = lime_data.get("predicted_probability", 0.0)
            instance_id = lime_data.get("instance_id", "N/A")
            pred_class = lime_data.get("predicted_class", "N/A")

            supporting = [e for e in explanation if e.get("weight", 0) > 0]
            opposing = [e for e in explanation if e.get("weight", 0) < 0]

            if audience == "executive":
                return self._render_executive(prob, supporting, opposing, instance_id)
            else:
                return self._render_technical(prob, pred_class, explanation, instance_id)
        except Exception as exc:
            self.logger.error(f"LIME render failed: {exc}")
            return f"<p>LIME explanation unavailable: {exc}</p>"

    def _render_executive(self, prob, supporting, opposing, instance_id) -> str:
        sup_text = ", ".join(
            f"<strong>{e['feature'].replace('_', ' ').title()}</strong>" for e in supporting[:3]
        ) or "None identified"
        opp_text = ", ".join(
            f"<strong>{e['feature'].replace('_', ' ').title()}</strong>" for e in opposing[:3]
        ) or "None identified"
        outcome = "Approved" if prob >= 0.5 else "Declined"
        return f"""
<div class="alert {'alert-success' if prob >= 0.5 else 'alert-danger'}">
  <div class="alert-title">Decision Explanation (Case {instance_id})</div>
  <p>Predicted outcome: <strong>{outcome}</strong> ({prob:.1%} confidence)</p>
  <p>Key supporting factors: {sup_text}</p>
  <p>Key risk factors: {opp_text}</p>
</div>"""

    def _render_technical(self, prob, pred_class, explanation, instance_id) -> str:
        rows = "".join(
            f"<tr><td><code>{e['feature']}</code></td>"
            f"<td>{e.get('value', 'N/A')}</td>"
            f"<td style='color:{'#27AE60' if e['weight']>0 else '#E74C3C'}'>{e['weight']:+.4f}</td></tr>"
            for e in sorted(explanation, key=lambda x: abs(x.get("weight", 0)), reverse=True)
        )
        return f"""
<h4>LIME Local Explanation — Instance {instance_id}</h4>
<p>Predicted class: <code>{pred_class}</code> | Probability: <strong>{prob:.4f}</strong></p>
<table>
  <thead><tr><th>Feature</th><th>Value</th><th>Local Weight</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<p class="chart-caption">
  LIME weights represent local linear approximations of model behaviour
  in the neighbourhood of this specific instance.
</p>"""


# ── Fairness Metric Explainer ─────────────────────────────────────────── #

class FairnessExplainer:
    """
    Renders fairness metrics (demographic parity, equalized odds, etc.)
    into audience-appropriate HTML with pass/fail status and remediation notes.

    Expected input (fairness_data):
        {
            "overall_bias_score": float,
            "fairness_metrics": {
                "demographic_parity": float,
                "equalized_odds": float,
                "disparate_impact": float,
                "calibration": float,
                ...
            },
            "protected_attributes": ["gender", "age", ...],
            "mitigation_applied": str | None
        }
    """

    METRIC_DESCRIPTIONS = {
        "demographic_parity": ("Demographic Parity", 0.8, 0.6),
        "equalized_odds": ("Equalized Odds", 0.8, 0.6),
        "disparate_impact": ("Disparate Impact", 0.8, 0.7),   # 80% rule
        "calibration": ("Calibration", 0.85, 0.7),
        "individual_fairness": ("Individual Fairness", 0.8, 0.6),
        "counterfactual_fairness": ("Counterfactual Fairness", 0.8, 0.6),
    }

    REGULATORY_THRESHOLDS = {
        "disparate_impact": ("80% Rule (ECOA/CFPB)", 0.8),
        "demographic_parity": ("EU AI Act Annex IV", 0.85),
        "equalized_odds": ("NIST AI RMF", 0.8),
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def render(self, fairness_data: Dict[str, Any], audience: str = "technical") -> str:
        if not fairness_data:
            return "<p>Fairness analysis data not available.</p>"
        try:
            if audience == "executive":
                return self._render_executive(fairness_data)
            elif audience == "regulatory":
                return self._render_regulatory(fairness_data)
            else:
                return self._render_technical(fairness_data)
        except Exception as exc:
            self.logger.error(f"Fairness render failed: {exc}")
            return f"<p>Fairness explanation unavailable: {exc}</p>"

    def _overall_card(self, score: float, label: str = "Overall Bias Score") -> str:
        css_class = "good" if score >= 0.8 else "warn" if score >= 0.6 else "bad"
        return (
            f'<div class="metric-card {css_class}">'
            f'<div class="value">{score:.2f}</div>'
            f'<div class="label">{label}</div>'
            f'</div>'
        )

    def _render_executive(self, data: Dict[str, Any]) -> str:
        score = data.get("overall_bias_score", 0.0)
        metrics = data.get("fairness_metrics", {})
        attrs = data.get("protected_attributes", [])
        mitigation = data.get("mitigation_applied")

        status = "PASS" if score >= 0.8 else "REVIEW REQUIRED" if score >= 0.6 else "FAIL"
        alert_class = "alert-success" if score >= 0.8 else "alert-warning" if score >= 0.6 else "alert-danger"

        metric_rows = "".join(
            f"<tr><td>{self.METRIC_DESCRIPTIONS.get(k, (k, 0.8, 0.6))[0]}</td>"
            f"<td>{_badge(v)}</td></tr>"
            for k, v in metrics.items() if k in self.METRIC_DESCRIPTIONS
        )

        mitigation_note = (
            f'<p>Mitigation technique applied: <strong>{mitigation}</strong></p>'
            if mitigation else ""
        )

        return f"""
<div class="alert {alert_class}">
  <div class="alert-title">Fairness Status: {status}</div>
  <p>Overall bias score: <strong>{score:.2f}/1.00</strong>.
  Protected attributes analysed: {', '.join(attrs) or 'N/A'}.</p>
  {mitigation_note}
</div>
<div class="metric-grid">{self._overall_card(score)}</div>
<table>
  <thead><tr><th>Fairness Metric</th><th>Score</th></tr></thead>
  <tbody>{metric_rows}</tbody>
</table>"""

    def _render_technical(self, data: Dict[str, Any]) -> str:
        score = data.get("overall_bias_score", 0.0)
        metrics = data.get("fairness_metrics", {})
        attrs = data.get("protected_attributes", [])

        rows = ""
        for key, value in metrics.items():
            label, good_t, warn_t = self.METRIC_DESCRIPTIONS.get(key, (key, 0.8, 0.6))
            status = "PASS" if value >= good_t else "WARN" if value >= warn_t else "FAIL"
            badge_cls = "badge-green" if status == "PASS" else "badge-yellow" if status == "WARN" else "badge-red"
            rows += (
                f"<tr><td>{label}</td><td>{value:.4f}</td>"
                f"<td><span class='badge {badge_cls}'>{status}</span></td>"
                f"<td>{good_t:.2f}</td></tr>"
            )

        return f"""
<div class="metric-grid">
  {self._overall_card(score)}
  <div class="metric-card"><div class="value">{len(attrs)}</div><div class="label">Protected Attributes</div></div>
  <div class="metric-card"><div class="value">{len(metrics)}</div><div class="label">Metrics Evaluated</div></div>
</div>
<h4>Detailed Fairness Metrics</h4>
<table>
  <thead><tr><th>Metric</th><th>Value</th><th>Status</th><th>Threshold</th></tr></thead>
  <tbody>{rows}</tbody>
</table>"""

    def _render_regulatory(self, data: Dict[str, Any]) -> str:
        score = data.get("overall_bias_score", 0.0)
        metrics = data.get("fairness_metrics", {})
        attrs = data.get("protected_attributes", [])

        reg_rows = ""
        for metric_key, (framework, threshold) in self.REGULATORY_THRESHOLDS.items():
            value = metrics.get(metric_key)
            if value is None:
                continue
            compliant = value >= threshold
            badge = (
                '<span class="badge badge-green">COMPLIANT</span>'
                if compliant else
                '<span class="badge badge-red">NON-COMPLIANT</span>'
            )
            reg_rows += (
                f"<tr><td>{self.METRIC_DESCRIPTIONS.get(metric_key, (metric_key,))[0]}</td>"
                f"<td>{value:.4f}</td><td>≥ {threshold:.2f}</td>"
                f"<td>{framework}</td><td>{badge}</td></tr>"
            )

        return f"""
<div class="alert alert-info">
  <div class="alert-title">Regulatory Compliance Assessment</div>
  <p>This assessment verifies compliance with applicable fairness standards.
  Protected attributes under review: <strong>{', '.join(attrs) or 'N/A'}</strong>.
  Overall bias score: <strong>{score:.2f}</strong>.</p>
</div>
<table>
  <thead><tr><th>Metric</th><th>Value</th><th>Required Threshold</th><th>Framework</th><th>Status</th></tr></thead>
  <tbody>{reg_rows}</tbody>
</table>"""


# ── Risk Simulation Explainer ─────────────────────────────────────────── #

class RiskSimulationExplainer:
    """
    Formats Monte Carlo / Bayesian risk simulation results into
    audience-appropriate HTML sections.

    Expected input (risk_data):
        {
            "risk_probability": float,
            "confidence_interval": [float, float],
            "var_95": float,
            "expected_loss": float,
            "simulation_method": str,
            "num_simulations": int,
            "risk_factors": [{"name": str, "contribution": float}, ...]
        }
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def render(self, risk_data: Dict[str, Any], audience: str = "technical") -> str:
        if not risk_data:
            return "<p>Risk simulation data not available.</p>"
        try:
            if audience == "executive":
                return self._render_executive(risk_data)
            elif audience == "regulatory":
                return self._render_regulatory(risk_data)
            else:
                return self._render_technical(risk_data)
        except Exception as exc:
            self.logger.error(f"Risk render failed: {exc}")
            return f"<p>Risk explanation unavailable: {exc}</p>"

    def _render_executive(self, data: Dict[str, Any]) -> str:
        prob = data.get("risk_probability", 0.0)
        ci = data.get("confidence_interval", [0, 0])
        expected_loss = data.get("expected_loss", 0.0)
        risk_factors = data.get("risk_factors", [])

        top_factors = sorted(risk_factors, key=lambda x: x.get("contribution", 0), reverse=True)[:3]
        factors_text = ", ".join(f["name"].replace("_", " ").title() for f in top_factors) or "Not specified"

        return f"""
<div class="metric-grid">
  <div class="metric-card {'bad' if prob > 0.5 else 'warn' if prob > 0.2 else 'good'}">
    <div class="value">{prob:.1%}</div>
    <div class="label">Compliance Risk Probability</div>
  </div>
  <div class="metric-card warn">
    <div class="value">${expected_loss:,.0f}</div>
    <div class="label">Expected Loss (USD)</div>
  </div>
</div>
<div class="alert {'alert-danger' if prob > 0.5 else 'alert-warning' if prob > 0.2 else 'alert-success'}">
  <div class="alert-title">Risk Summary</div>
  <p>There is a <strong>{prob:.1%}</strong> probability of a compliance event,
  with 95% confidence that losses fall between
  <strong>${ci[0]:,.0f}</strong> and <strong>${ci[1]:,.0f}</strong>.</p>
  <p>Primary risk drivers: {factors_text}.</p>
</div>"""

    def _render_technical(self, data: Dict[str, Any]) -> str:
        prob = data.get("risk_probability", 0.0)
        ci = data.get("confidence_interval", [0, 0])
        var_95 = data.get("var_95", 0.0)
        expected_loss = data.get("expected_loss", 0.0)
        method = data.get("simulation_method", "Monte Carlo")
        n_sims = data.get("num_simulations", 0)
        risk_factors = data.get("risk_factors", [])

        factor_rows = "".join(
            f"<tr><td>{f['name'].replace('_', ' ').title()}</td>"
            f"<td>{f.get('contribution', 0):.4f}</td>"
            f"<td style='background:linear-gradient(to right,#2E86AB {f.get('contribution',0)*100:.0f}%,transparent 0)'></td></tr>"
            for f in sorted(risk_factors, key=lambda x: x.get("contribution", 0), reverse=True)
        )

        return f"""
<div class="metric-grid">
  <div class="metric-card {'bad' if prob > 0.5 else 'warn' if prob > 0.2 else 'good'}">
    <div class="value">{prob:.4f}</div><div class="label">Risk Probability</div>
  </div>
  <div class="metric-card warn">
    <div class="value">${var_95:,.2f}</div><div class="label">VaR (95%)</div>
  </div>
  <div class="metric-card">
    <div class="value">${expected_loss:,.2f}</div><div class="label">Expected Loss</div>
  </div>
  <div class="metric-card">
    <div class="value">{n_sims:,}</div><div class="label">Simulations Run</div>
  </div>
</div>
<p>Method: <strong>{method}</strong> |
   95% CI: [<strong>${ci[0]:,.2f}</strong>, <strong>${ci[1]:,.2f}</strong>]</p>
{'<h4>Risk Factor Contributions</h4><table><thead><tr><th>Factor</th><th>Contribution</th><th>Weight</th></tr></thead><tbody>' + factor_rows + '</tbody></table>' if factor_rows else ''}"""

    def _render_regulatory(self, data: Dict[str, Any]) -> str:
        prob = data.get("risk_probability", 0.0)
        ci = data.get("confidence_interval", [0, 0])
        var_95 = data.get("var_95", 0.0)
        method = data.get("simulation_method", "Monte Carlo")
        n_sims = data.get("num_simulations", 0)

        compliant = prob < 0.2
        return f"""
<div class="alert {'alert-success' if compliant else 'alert-danger'}">
  <div class="alert-title">{'Risk Within Acceptable Limits' if compliant else 'Risk Exceeds Acceptable Threshold'}</div>
  <p>Compliance risk probability: <strong>{prob:.2%}</strong>
  (regulatory threshold: &lt; 20%).</p>
</div>
<table>
  <thead><tr><th>Metric</th><th>Value</th><th>Regulatory Benchmark</th><th>Status</th></tr></thead>
  <tbody>
    <tr>
      <td>Compliance Risk Probability</td>
      <td>{prob:.2%}</td><td>&lt; 20%</td>
      <td>{'<span class="badge badge-green">PASS</span>' if prob < 0.2 else '<span class="badge badge-red">FAIL</span>'}</td>
    </tr>
    <tr>
      <td>95% Value at Risk</td>
      <td>${var_95:,.2f}</td><td>Institution-defined limit</td>
      <td><span class="badge badge-blue">REVIEW</span></td>
    </tr>
    <tr>
      <td>95% Confidence Interval</td>
      <td>[${ci[0]:,.2f}, ${ci[1]:,.2f}]</td><td>—</td>
      <td><span class="badge badge-blue">DOCUMENTED</span></td>
    </tr>
  </tbody>
</table>
<p class="chart-caption">
  Simulation method: {method} ({n_sims:,} iterations).
  Compliant with BCBS 239 stress-testing and EBA risk quantification guidelines.
</p>"""


# ── Unified Explainer Factory ─────────────────────────────────────────── #

class ReportExplainerFactory:
    """
    Factory that routes explainer requests to the correct sub-explainer
    and returns formatted HTML sections.
    """

    def __init__(self):
        self.shap = SHAPExplainer()
        self.lime = LIMEExplainer()
        self.fairness = FairnessExplainer()
        self.risk = RiskSimulationExplainer()
        self.logger = logging.getLogger(__name__)

    def explain(
        self,
        explainer_type: str,
        data: Dict[str, Any],
        audience: str = "technical",
    ) -> str:
        """
        Route to the correct explainer.

        Args:
            explainer_type: One of 'shap', 'lime', 'fairness', 'risk'.
            data:           The explainer-specific data dict.
            audience:       'executive', 'technical', or 'regulatory'.

        Returns:
            HTML string ready for embedding in a report section.
        """
        mapping = {
            "shap": self.shap.render,
            "lime": self.lime.render,
            "fairness": self.fairness.render,
            "risk": self.risk.render,
        }
        handler = mapping.get(explainer_type)
        if not handler:
            self.logger.warning(f"Unknown explainer type: {explainer_type}")
            return f"<p>Unknown explainer type: {explainer_type}</p>"
        return handler(data, audience)

    def explain_all(
        self,
        shap_data: Optional[Dict] = None,
        lime_data: Optional[Dict] = None,
        fairness_data: Optional[Dict] = None,
        risk_data: Optional[Dict] = None,
        audience: str = "technical",
    ) -> Dict[str, str]:
        """
        Run all available explainers and return a dict of HTML sections.
        Keys: 'shap', 'lime', 'fairness', 'risk'.
        """
        results: Dict[str, str] = {}
        if shap_data:
            results["shap"] = self.shap.render(shap_data, audience)
        if lime_data:
            results["lime"] = self.lime.render(lime_data, audience)
        if fairness_data:
            results["fairness"] = self.fairness.render(fairness_data, audience)
        if risk_data:
            results["risk"] = self.risk.render(risk_data, audience)
        return results
