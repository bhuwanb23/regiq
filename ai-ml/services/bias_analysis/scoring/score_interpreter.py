#!/usr/bin/env python3
"""
REGIQ AI/ML - Score Interpreter
Interprets bias scores and generates natural language explanations using Gemini.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Optional, List, Any

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.gemini_config import GeminiAPIManager
from .llm_prompts import (
    get_score_interpretation_prompt,
    get_recommendations_prompt,
    get_executive_summary_prompt
)


logger = logging.getLogger("score_interpreter")


class ScoreInterpreter:
    """
    Interprets bias scores into human-readable explanations.
    
    Uses:
    - Severity level classification
    - Natural language generation (Gemini)
    - Benchmark comparisons
    - Actionable insights
    """
    
    # Score range definitions
    SEVERITY_RANGES = {
        "EXCELLENT": (0.00, 0.15),
        "GOOD": (0.16, 0.35),
        "MODERATE": (0.36, 0.60),
        "POOR": (0.61, 0.80),
        "CRITICAL": (0.81, 1.00)
    }
    
    # Industry benchmarks (approximate)
    INDUSTRY_BENCHMARKS = {
        "lending": 0.38,
        "hiring": 0.35,
        "insurance": 0.40,
        "banking": 0.36,
        "general": 0.40
    }
    
    def __init__(self, use_llm: bool = True):
        """
        Initialize score interpreter.
        
        Args:
            use_llm: Whether to use LLM for natural language generation
        """
        self.logger = logger
        self.use_llm = use_llm
        
        if use_llm:
            try:
                self.llm_manager = GeminiAPIManager()
                self.logger.info("Initialized Gemini LLM for score interpretation")
            except Exception as e:
                self.logger.warning(f"Failed to initialize LLM: {e}, falling back to template-based interpretation")
                self.use_llm = False
    
    def interpret_score(self,
                       bias_score: float,
                       metric_contributions: Dict[str, float],
                       raw_metrics: Dict[str, float],
                       dominant_metric: str) -> Dict[str, Any]:
        """
        Interpret bias score and generate explanation.
        
        Args:
            bias_score: Overall composite bias score
            metric_contributions: Contribution of each metric
            raw_metrics: Raw metric values
            dominant_metric: Metric contributing most
            
        Returns:
            Dictionary with interpretation data
        """
        try:
            # Classify severity
            severity_level, severity_desc, score_range = self._classify_severity(bias_score)
            
            # Generate LLM explanation if available
            llm_explanation = None
            if self.use_llm:
                llm_explanation = self._generate_llm_interpretation(
                    bias_score, metric_contributions, raw_metrics, dominant_metric
                )
            
            # Generate fallback explanation
            template_explanation = self._generate_template_interpretation(
                bias_score, dominant_metric, severity_level
            )
            
            # Identify key concerns
            key_concerns = self._identify_key_concerns(
                metric_contributions, raw_metrics
            )
            
            # Get benchmark comparison
            benchmark_comp = self._compare_to_benchmark(bias_score, "general")
            
            return {
                "severity_level": severity_level,
                "severity_description": severity_desc,
                "score_range": list(score_range),
                "interpretation": llm_explanation if llm_explanation else template_explanation,
                "key_concerns": key_concerns,
                "llm_explanation": llm_explanation,
                "template_explanation": template_explanation,
                "benchmark_comparison": benchmark_comp
            }
            
        except Exception as e:
            self.logger.error(f"Score interpretation failed: {e}")
            return {
                "severity_level": "UNKNOWN",
                "severity_description": "Unable to interpret score",
                "score_range": [0.0, 0.0],
                "interpretation": "Error interpreting bias score",
                "key_concerns": [],
                "error": str(e)
            }
    
    def _classify_severity(self, bias_score: float) -> tuple:
        """
        Classify bias score into severity level.
        
        Args:
            bias_score: Composite bias score
            
        Returns:
            Tuple of (level, description, range)
        """
        for level, (min_score, max_score) in self.SEVERITY_RANGES.items():
            if min_score <= bias_score <= max_score:
                descriptions = {
                    "EXCELLENT": "Minimal bias detected - Excellent fairness",
                    "GOOD": "Minor fairness concerns - Good overall",
                    "MODERATE": "Requires attention - Moderate bias",
                    "POOR": "Significant bias detected - Action required",
                    "CRITICAL": "Severe bias - Immediate action required"
                }
                return (level, descriptions[level], (min_score, max_score))
        
        return ("UNKNOWN", "Unable to classify", (0.0, 0.0))
    
    def _generate_llm_interpretation(self,
                                    bias_score: float,
                                    metric_contributions: Dict[str, float],
                                    raw_metrics: Dict[str, float],
                                    dominant_metric: str) -> Optional[str]:
        """Generate natural language interpretation using Gemini."""
        try:
            prompt = get_score_interpretation_prompt(
                bias_score, metric_contributions, raw_metrics, dominant_metric
            )
            
            response = self.llm_manager.generate_content(
                prompt,
                temperature=0.3,
                max_tokens=200
            )
            
            return response.strip() if response else None
            
        except Exception as e:
            self.logger.warning(f"LLM interpretation failed: {e}")
            return None
    
    def _generate_template_interpretation(self,
                                         bias_score: float,
                                         dominant_metric: str,
                                         severity_level: str) -> str:
        """Generate template-based interpretation (fallback)."""
        metric_names = {
            "demographic_parity": "demographic parity violations",
            "equalized_odds": "unequal error rates across groups",
            "calibration": "poor model calibration",
            "individual_fairness": "inconsistent treatment of similar individuals"
        }
        
        dominant_name = metric_names.get(dominant_metric, "fairness issues")
        
        templates = {
            "EXCELLENT": f"The model shows excellent fairness with minimal bias (score: {bias_score:.3f}). {dominant_name.capitalize()} contribute most to the score, but remain within acceptable thresholds.",
            "GOOD": f"The model demonstrates good fairness with minor concerns (score: {bias_score:.3f}). The primary issue is {dominant_name}, which should be monitored but does not require immediate action.",
            "MODERATE": f"The model shows moderate bias requiring attention (score: {bias_score:.3f}). {dominant_name.capitalize()} are the primary driver, indicating the need for bias mitigation within 30 days.",
            "POOR": f"The model exhibits significant bias (score: {bias_score:.3f}). {dominant_name.capitalize()} are severe and require immediate remediation to ensure compliance and fairness.",
            "CRITICAL": f"The model has critical bias levels (score: {bias_score:.3f}). {dominant_name.capitalize()} represent severe violations. Immediate action is required before deployment or continued use."
        }
        
        return templates.get(severity_level, f"Bias score: {bias_score:.3f}")
    
    def _identify_key_concerns(self,
                              metric_contributions: Dict[str, float],
                              raw_metrics: Dict[str, float]) -> List[str]:
        """Identify key concerns from metric breakdown."""
        concerns = []
        
        # Check each metric against thresholds
        thresholds = {
            "demographic_parity": 0.20,
            "equalized_odds": 0.20,
            "calibration": 0.15,
            "individual_fairness": 0.15
        }
        
        metric_names = {
            "demographic_parity": "Demographic parity violation ({:.1%}) exceeds threshold",
            "equalized_odds": "Equalized odds violation ({:.1%}) exceeds threshold",
            "calibration": "Calibration error ({:.1%}) is high",
            "individual_fairness": "Individual fairness inconsistency ({:.1%}) detected"
        }
        
        for metric, contrib in metric_contributions.items():
            if contrib > thresholds.get(metric, 0.15):
                raw_val = raw_metrics.get(metric, 0)
                # Invert individual fairness for display
                if metric == "individual_fairness":
                    raw_val = 1.0 - raw_val
                concerns.append(metric_names[metric].format(raw_val))
        
        return concerns if concerns else ["All metrics within acceptable ranges"]
    
    def _compare_to_benchmark(self, bias_score: float, industry: str) -> Dict[str, Any]:
        """Compare score to industry benchmark."""
        benchmark = self.INDUSTRY_BENCHMARKS.get(industry, 0.40)
        diff = bias_score - benchmark
        percentile = self._estimate_percentile(bias_score, benchmark)
        
        if diff < -0.10:
            performance = "significantly better than"
        elif diff < 0:
            performance = "better than"
        elif diff < 0.10:
            performance = "comparable to"
        else:
            performance = "worse than"
        
        return {
            "industry": industry,
            "industry_average": benchmark,
            "difference": diff,
            "percentile": percentile,
            "performance": performance
        }
    
    def _estimate_percentile(self, score: float, benchmark: float) -> int:
        """Estimate percentile based on score vs benchmark."""
        # Simplified estimation
        if score < benchmark - 0.15:
            return 90
        elif score < benchmark - 0.05:
            return 75
        elif score < benchmark + 0.05:
            return 50
        elif score < benchmark + 0.15:
            return 25
        else:
            return 10


def main():
    """Test the score interpreter."""
    print("🧪 Testing Score Interpreter")
    
    # Create interpreter
    interpreter = ScoreInterpreter(use_llm=True)
    
    # Test data
    bias_score = 0.45
    metric_contributions = {
        "demographic_parity": 0.105,
        "equalized_odds": 0.182,
        "calibration": 0.056,
        "individual_fairness": 0.107
    }
    raw_metrics = {
        "demographic_parity": 0.35,
        "equalized_odds": 0.52,
        "calibration": 0.28,
        "individual_fairness": 0.60
    }
    dominant_metric = "equalized_odds"
    
    # Interpret score
    result = interpreter.interpret_score(
        bias_score, metric_contributions, raw_metrics, dominant_metric
    )
    
    print("✅ Score interpretation completed")
    print(f"✅ Severity: {result['severity_level']} - {result['severity_description']}")
    print(f"✅ Interpretation: {result['interpretation']}")
    print(f"✅ Key concerns: {result['key_concerns']}")
    print(f"✅ Benchmark: {result['benchmark_comparison']['performance']} industry average")


if __name__ == "__main__":
    main()
