"""
Stress Reporter Module

This module implements stress test report generation including:
- Vulnerability assessment reports
- Resilience scorecards
- Risk heatmap data generation
- Mitigation recommendations
- Executive summaries

All outputs are JSON-serializable for backend-only implementation.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import numpy as np


class ReportType(Enum):
    """Types of stress test reports"""
    VULNERABILITY_ASSESSMENT = "vulnerability_assessment"
    RESILIENCE_SCORECARD = "resilience_scorecard"
    EXECUTIVE_SUMMARY = "executive_summary"
    DETAILED_ANALYSIS = "detailed_analysis"
    ACTION_PLAN = "action_plan"


class Priority(Enum):
    """Priority levels for recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class VulnerabilityReport:
    """Vulnerability assessment report"""
    report_id: str
    generation_date: str
    vulnerabilities: List[Dict[str, Any]]
    risk_score: float
    critical_count: int
    high_count: int
    recommendations: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'report_id': self.report_id,
            'generation_date': self.generation_date,
            'vulnerabilities': self.vulnerabilities,
            'risk_score': float(self.risk_score),
            'critical_count': int(self.critical_count),
            'high_count': int(self.high_count),
            'recommendations': self.recommendations
        }


class StressTestReportGenerator:
    """Generate comprehensive stress test reports"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def generate_vulnerability_assessment(self,
                                         stress_test_results: List[Dict[str, Any]],
                                         breaking_points: List[Dict[str, Any]]) -> VulnerabilityReport:
        """
        Generate vulnerability assessment report
        
        Args:
            stress_test_results: Results from stress testing
            breaking_points: Identified breaking points
            
        Returns:
            VulnerabilityReport object
        """
        vulnerabilities = []
        critical_count = 0
        high_count = 0
        
        # Analyze stress test results
        for result in stress_test_results:
            severity = result.get('stress_level', 'moderate')
            failed = result.get('failed', False)
            
            if failed or severity in ['extreme', 'catastrophic']:
                vuln = {
                    'vulnerability_id': f"VULN-{self.rng.randint(1000, 9999)}",
                    'description': result.get('description', 'Stress test failure'),
                    'severity': 'critical' if failed else 'high',
                    'affected_systems': result.get('impact_areas', []),
                    'likelihood': result.get('probability', 0.1),
                    'impact_score': result.get('severity_score', 50)
                }
                vulnerabilities.append(vuln)
                
                if vuln['severity'] == 'critical':
                    critical_count += 1
                else:
                    high_count += 1
        
        # Analyze breaking points
        for bp in breaking_points:
            if bp.get('safety_margin', 1.0) < 0.2:
                vuln = {
                    'vulnerability_id': f"VULN-BP-{self.rng.randint(1000, 9999)}",
                    'description': f"Resource breaking point: {bp.get('resource_type')}",
                    'severity': 'critical' if bp.get('safety_margin', 0) < 0.1 else 'high',
                    'affected_systems': [bp.get('resource_type')],
                    'likelihood': 0.3,
                    'impact_score': (1 - bp.get('safety_margin', 0)) * 100
                }
                vulnerabilities.append(vuln)
                
                if vuln['severity'] == 'critical':
                    critical_count += 1
                else:
                    high_count += 1
        
        # Calculate overall risk score
        if vulnerabilities:
            risk_scores = [v['impact_score'] * v['likelihood'] for v in vulnerabilities]
            overall_risk = float(np.mean(risk_scores))
        else:
            overall_risk = 0.0
        
        # Generate recommendations
        recommendations = self._generate_vulnerability_recommendations(vulnerabilities)
        
        report_id = f"VULN-RPT-{datetime.now().strftime('%Y%m%d')}-{self.rng.randint(100, 999)}"
        
        return VulnerabilityReport(
            report_id=report_id,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            vulnerabilities=vulnerabilities,
            risk_score=overall_risk,
            critical_count=critical_count,
            high_count=high_count,
            recommendations=recommendations
        )
    
    def _generate_vulnerability_recommendations(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommendations for vulnerabilities"""
        recommendations = []
        
        # Group by severity
        critical_vulns = [v for v in vulnerabilities if v['severity'] == 'critical']
        high_vulns = [v for v in vulnerabilities if v['severity'] == 'high']
        
        if critical_vulns:
            recommendations.append({
                'priority': Priority.CRITICAL.value,
                'recommendation': f"Address {len(critical_vulns)} critical vulnerabilities immediately",
                'action': "Implement emergency mitigation measures",
                'timeline_days': 7,
                'estimated_cost': len(critical_vulns) * 100000
            })
        
        if high_vulns:
            recommendations.append({
                'priority': Priority.HIGH.value,
                'recommendation': f"Mitigate {len(high_vulns)} high-severity vulnerabilities",
                'action': "Develop and implement remediation plans",
                'timeline_days': 30,
                'estimated_cost': len(high_vulns) * 50000
            })
        
        return recommendations
    
    def generate_resilience_scorecard(self,
                                     resilience_scores: Dict[str, float],
                                     historical_scores: Optional[List[Dict[str, float]]] = None) -> Dict[str, Any]:
        """
        Generate resilience scorecard
        
        Args:
            resilience_scores: Current resilience scores
            historical_scores: Historical scores for trending
            
        Returns:
            Dictionary with scorecard data
        """
        overall_score = resilience_scores.get('overall_score', 0)
        
        # Determine grade
        if overall_score >= 90:
            grade = 'A'
        elif overall_score >= 80:
            grade = 'B'
        elif overall_score >= 70:
            grade = 'C'
        elif overall_score >= 60:
            grade = 'D'
        else:
            grade = 'F'
        
        # Calculate trend
        trend = "stable"
        if historical_scores and len(historical_scores) > 0:
            prev_score = historical_scores[-1].get('overall_score', overall_score)
            if overall_score > prev_score + 5:
                trend = "improving"
            elif overall_score < prev_score - 5:
                trend = "declining"
        
        # Component breakdown
        components = {
            'adaptive_capacity': {
                'score': resilience_scores.get('adaptive_capacity', 0),
                'status': self._get_status(resilience_scores.get('adaptive_capacity', 0))
            },
            'recovery_capability': {
                'score': resilience_scores.get('recovery_capability', 0),
                'status': self._get_status(resilience_scores.get('recovery_capability', 0))
            },
            'stress_absorption': {
                'score': resilience_scores.get('stress_absorption', 0),
                'status': self._get_status(resilience_scores.get('stress_absorption', 0))
            }
        }
        
        return {
            'scorecard_id': f"SCORECARD-{datetime.now().strftime('%Y%m%d')}",
            'generation_date': datetime.now().strftime("%Y-%m-%d"),
            'overall_score': float(overall_score),
            'grade': grade,
            'trend': trend,
            'components': components,
            'strengths': resilience_scores.get('strengths', []),
            'weaknesses': resilience_scores.get('weaknesses', []),
            'next_review_date': self._calculate_next_review_date(overall_score)
        }
    
    def _get_status(self, score: float) -> str:
        """Get status label for score"""
        if score >= 75:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 45:
            return "needs_improvement"
        else:
            return "critical"
    
    def _calculate_next_review_date(self, score: float) -> str:
        """Calculate next review date based on score"""
        from datetime import timedelta
        
        if score < 60:
            days = 30  # Monthly for low scores
        elif score < 75:
            days = 90  # Quarterly for moderate scores
        else:
            days = 180  # Semi-annual for high scores
        
        next_date = datetime.now() + timedelta(days=days)
        return next_date.strftime("%Y-%m-%d")
    
    def generate_risk_heatmap_data(self,
                                   scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate data for risk heatmap visualization
        
        Args:
            scenarios: List of stress test scenarios
            
        Returns:
            Dictionary with heatmap data
        """
        heatmap_cells = []
        
        for scenario in scenarios:
            probability = scenario.get('probability', 0.1)
            impact = scenario.get('expected_financial_impact', 0) / 1000000  # Convert to millions
            severity_score = scenario.get('combined_severity_score', 50)
            
            # Categorize
            if probability > 0.3:
                prob_category = "high"
            elif probability > 0.1:
                prob_category = "medium"
            else:
                prob_category = "low"
            
            if impact > 5:
                impact_category = "high"
            elif impact > 1:
                impact_category = "medium"
            else:
                impact_category = "low"
            
            cell = {
                'scenario_id': scenario.get('scenario_id', ''),
                'scenario_name': scenario.get('scenario_name', ''),
                'probability': float(probability),
                'impact_millions': float(impact),
                'severity_score': float(severity_score),
                'probability_category': prob_category,
                'impact_category': impact_category,
                'risk_level': self._calculate_risk_level(probability, impact)
            }
            heatmap_cells.append(cell)
        
        return {
            'heatmap_data': heatmap_cells,
            'total_scenarios': len(scenarios),
            'high_risk_count': sum(1 for c in heatmap_cells if c['risk_level'] == 'high'),
            'medium_risk_count': sum(1 for c in heatmap_cells if c['risk_level'] == 'medium'),
            'low_risk_count': sum(1 for c in heatmap_cells if c['risk_level'] == 'low')
        }
    
    def _calculate_risk_level(self, probability: float, impact: float) -> str:
        """Calculate risk level from probability and impact"""
        risk_score = probability * impact
        
        if risk_score > 2.0:
            return "high"
        elif risk_score > 0.5:
            return "medium"
        else:
            return "low"


class ExecutiveSummaryGenerator:
    """Generate executive summaries of stress testing"""
    
    def __init__(self):
        pass
    
    def generate_executive_summary(self,
                                   vulnerability_report: Dict[str, Any],
                                   resilience_scorecard: Dict[str, Any],
                                   key_scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate executive summary
        
        Args:
            vulnerability_report: Vulnerability assessment
            resilience_scorecard: Resilience scores
            key_scenarios: Key stress scenarios tested
            
        Returns:
            Dictionary with executive summary
        """
        # Key findings
        critical_vulns = vulnerability_report.get('critical_count', 0)
        high_vulns = vulnerability_report.get('high_count', 0)
        resilience_score = resilience_scorecard.get('overall_score', 0)
        resilience_grade = resilience_scorecard.get('grade', 'C')
        
        # Determine overall status
        if critical_vulns > 0 or resilience_score < 60:
            overall_status = "critical_action_required"
        elif high_vulns > 2 or resilience_score < 75:
            overall_status = "improvements_needed"
        else:
            overall_status = "satisfactory"
        
        # Key findings
        findings = []
        if critical_vulns > 0:
            findings.append(f"{critical_vulns} critical vulnerabilities identified requiring immediate action")
        if resilience_score < 70:
            findings.append(f"Resilience score of {resilience_score:.1f} (Grade {resilience_grade}) indicates systemic weaknesses")
        if len(key_scenarios) > 0:
            worst_scenario = max(key_scenarios, key=lambda x: x.get('combined_severity_score', 0))
            findings.append(f"Worst-case scenario: {worst_scenario.get('scenario_name')} with severity score {worst_scenario.get('combined_severity_score', 0):.0f}")
        
        # Critical recommendations
        recommendations = vulnerability_report.get('recommendations', [])
        critical_recs = [r for r in recommendations if r.get('priority') == 'critical']
        high_recs = [r for r in recommendations if r.get('priority') == 'high']
        
        # Investment requirements
        total_investment = sum(r.get('estimated_cost', 0) for r in recommendations)
        
        # Action priorities
        action_priorities = []
        for rec in critical_recs[:3]:  # Top 3 critical
            action_priorities.append({
                'priority': rec.get('priority'),
                'action': rec.get('action'),
                'timeline_days': rec.get('timeline_days'),
                'estimated_cost': rec.get('estimated_cost')
            })
        
        return {
            'summary_id': f"EXEC-SUM-{datetime.now().strftime('%Y%m%d')}",
            'generation_date': datetime.now().strftime("%Y-%m-%d"),
            'overall_status': overall_status,
            'key_metrics': {
                'resilience_score': float(resilience_score),
                'resilience_grade': resilience_grade,
                'critical_vulnerabilities': int(critical_vulns),
                'high_vulnerabilities': int(high_vulns),
                'scenarios_tested': len(key_scenarios)
            },
            'key_findings': findings,
            'action_priorities': action_priorities,
            'investment_required': float(total_investment),
            'recommended_timeline_days': min([r.get('timeline_days', 90) for r in critical_recs]) if critical_recs else 90,
            'bottom_line': self._generate_bottom_line(overall_status, resilience_score, critical_vulns)
        }
    
    def _generate_bottom_line(self, status: str, score: float, critical_vulns: int) -> str:
        """Generate bottom-line message"""
        if status == "critical_action_required":
            return f"Immediate action required to address {critical_vulns} critical vulnerabilities and improve resilience score of {score:.0f}"
        elif status == "improvements_needed":
            return f"System resilience (score: {score:.0f}) requires improvements to handle extreme stress scenarios"
        else:
            return f"System demonstrates adequate resilience (score: {score:.0f}) with continuous monitoring recommended"
