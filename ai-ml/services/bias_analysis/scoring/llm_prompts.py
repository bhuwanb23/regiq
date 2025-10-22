#!/usr/bin/env python3
"""
REGIQ AI/ML - LLM Prompt Templates for Bias Scoring
Gemini prompts for natural language interpretation of bias scores.
"""

from typing import Dict, Any, Optional


def get_score_interpretation_prompt(bias_score: float, metric_contributions: Dict[str, float],
                                    raw_metrics: Dict[str, float], dominant_metric: str) -> str:
    """
    Generate prompt for LLM to interpret bias score.
    
    Args:
        bias_score: Overall composite bias score
        metric_contributions: Contribution of each metric
        raw_metrics: Raw metric values
        dominant_metric: Metric contributing most to the score
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are an AI fairness expert analyzing a machine learning model for bias.

**Overall Bias Score**: {bias_score:.3f} (scale: 0.0 = perfectly fair, 1.0 = severely biased)

**Metric Breakdown**:
- Demographic Parity Violation: {raw_metrics.get('demographic_parity', 0):.3f}
- Equalized Odds Violation: {raw_metrics.get('equalized_odds', 0):.3f}
- Calibration Error: {raw_metrics.get('calibration', 0):.3f}
- Individual Fairness Inconsistency: {1.0 - raw_metrics.get('individual_fairness', 1.0):.3f}

**Metric Contributions** (how much each metric contributed to the overall score):
- Demographic Parity: {metric_contributions.get('demographic_parity', 0):.3f}
- Equalized Odds: {metric_contributions.get('equalized_odds', 0):.3f}
- Calibration: {metric_contributions.get('calibration', 0):.3f}
- Individual Fairness: {metric_contributions.get('individual_fairness', 0):.3f}

**Dominant Metric**: {dominant_metric}

Please provide a concise, professional interpretation of this bias score in 2-3 sentences. Focus on:
1. The severity level (e.g., minimal, moderate, significant, severe bias)
2. Which specific metric is most problematic
3. What this means practically for model fairness

Keep your response clear, non-technical, and actionable. Do not use jargon. Limit response to 100 words."""

    return prompt


def get_recommendations_prompt(bias_score: float, risk_level: str,
                              metric_breakdown: Dict[str, float],
                              regulatory_context: Optional[str] = None) -> str:
    """
    Generate prompt for LLM to create actionable recommendations.
    
    Args:
        bias_score: Overall bias score
        risk_level: Risk classification (LOW, MEDIUM, HIGH, CRITICAL)
        metric_breakdown: Individual metric scores
        regulatory_context: Relevant regulations (optional)
        
    Returns:
        Formatted prompt string
    """
    reg_context = f"\n**Regulatory Context**: {regulatory_context}" if regulatory_context else ""
    
    prompt = f"""You are an AI compliance advisor helping to mitigate model bias.

**Model Risk Assessment**:
- Overall Bias Score: {bias_score:.3f}
- Risk Level: {risk_level}
{reg_context}

**Metric Issues**:
- Demographic Parity: {metric_breakdown.get('demographic_parity', 0):.3f}
- Equalized Odds: {metric_breakdown.get('equalized_odds', 0):.3f}
- Calibration: {metric_breakdown.get('calibration', 0):.3f}
- Individual Fairness: {metric_breakdown.get('individual_fairness', 0):.3f}

Provide 3-5 specific, actionable recommendations to improve model fairness. For each recommendation:
1. State the action clearly
2. Indicate which metric it addresses
3. Specify timeline (immediate, short-term <30 days, long-term)

Format as a numbered list. Keep each recommendation to 1-2 sentences. Focus on practical steps."""

    return prompt


def get_executive_summary_prompt(model_id: str, bias_score: float,
                                 risk_level: str, key_findings: str) -> str:
    """
    Generate prompt for executive summary.
    
    Args:
        model_id: Model identifier
        bias_score: Bias score
        risk_level: Risk classification
        key_findings: Key findings text
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""Create a brief executive summary for model bias analysis.

**Model**: {model_id}
**Bias Score**: {bias_score:.3f}/1.0
**Risk Classification**: {risk_level}

**Key Findings**:
{key_findings}

Write a 3-4 sentence executive summary suitable for C-level executives. The summary should:
1. State the overall risk level in business terms
2. Highlight the most critical concern
3. Indicate the urgency of action needed
4. Reference any regulatory implications if risk is HIGH or CRITICAL

Use clear, non-technical language. No jargon."""

    return prompt


def get_comparison_prompt(model_a_score: float, model_b_score: float,
                         model_a_id: str, model_b_id: str) -> str:
    """
    Generate prompt for comparing two models.
    
    Args:
        model_a_score: First model's bias score
        model_b_score: Second model's bias score
        model_a_id: First model ID
        model_b_id: Second model ID
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""Compare the fairness of two machine learning models:

**Model A** ({model_a_id}):
- Bias Score: {model_a_score:.3f}

**Model B** ({model_b_id}):
- Bias Score: {model_b_score:.3f}

In 2-3 sentences, explain:
1. Which model is fairer and by how much
2. Whether the difference is significant (>0.1 is significant)
3. Which model should be preferred for deployment

Be concise and actionable."""

    return prompt


def get_trend_analysis_prompt(scores: list, timestamps: list, model_id: str) -> str:
    """
    Generate prompt for bias score trend analysis.
    
    Args:
        scores: List of historical bias scores
        timestamps: List of timestamps
        model_id: Model identifier
        
    Returns:
        Formatted prompt string
    """
    score_history = "\n".join([
        f"- {timestamp}: {score:.3f}"
        for score, timestamp in zip(scores, timestamps)
    ])
    
    prompt = f"""Analyze the bias score trend for model: {model_id}

**Historical Scores**:
{score_history}

**Latest Score**: {scores[-1]:.3f}
**Change from Previous**: {scores[-1] - scores[-2]:.3f if len(scores) > 1 else 0:.3f}

In 2-3 sentences, explain:
1. Whether bias is increasing, decreasing, or stable
2. If there's a concerning trend
3. What action (if any) is needed

Keep it concise and actionable."""

    return prompt
