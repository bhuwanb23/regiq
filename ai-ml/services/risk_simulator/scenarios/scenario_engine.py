"""
Scenario Engine Module

This module provides unified scenario orchestration including:
- Coordinating all scenario types
- Running combined scenarios
- Aggregating results across domains
- Performance optimization
- Pre-built scenario templates

Central coordinator for Phase 4.3 scenario generation.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import numpy as np
import time

# Import all scenario generators
from .regulatory_scenarios import RegulationChangeScenario, JurisdictionScenarioGenerator
from .enforcement_scenarios import EnforcementPatternModel, PenaltyEscalationSimulator
from .market_scenarios import EconomicScenarioGenerator, CompetitiveLandscapeSimulator
from .external_factors import ExternalEventSimulator, BlackSwanEventGenerator
from .stress_scenarios import StressScenarioDesigner, HistoricalCrisisReplicator
from .extreme_conditions import ExtremeConditionSimulator, BreakingPointAnalyzer
from .resilience_tester import ResilienceAnalyzer, ContingencyValidator
from .stress_reporter import StressTestReportGenerator, ExecutiveSummaryGenerator


class IndustryTemplate(Enum):
    """Pre-built industry templates"""
    FINANCIAL_SERVICES = "financial_services"
    HEALTHCARE = "healthcare"
    TECHNOLOGY = "technology"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"


@dataclass
class CombinedScenarioResult:
    """Result from combined scenario execution"""
    scenario_id: str
    execution_time_seconds: float
    regulatory_results: List[Dict[str, Any]]
    enforcement_results: List[Dict[str, Any]]
    market_results: List[Dict[str, Any]]
    external_results: List[Dict[str, Any]]
    stress_results: List[Dict[str, Any]]
    aggregated_risk_score: float
    total_estimated_impact: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'scenario_id': self.scenario_id,
            'execution_time_seconds': float(self.execution_time_seconds),
            'regulatory_results': self.regulatory_results,
            'enforcement_results': self.enforcement_results,
            'market_results': self.market_results,
            'external_results': self.external_results,
            'stress_results': self.stress_results,
            'aggregated_risk_score': float(self.aggregated_risk_score),
            'total_estimated_impact': float(self.total_estimated_impact)
        }


class ScenarioOrchestrator:
    """Orchestrate and coordinate all scenario types"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        
        # Initialize all generators
        self.reg_generator = RegulationChangeScenario(random_state)
        self.jurisdiction_generator = JurisdictionScenarioGenerator(random_state)
        self.enforcement_generator = EnforcementPatternModel(random_state)
        self.penalty_simulator = PenaltyEscalationSimulator(random_state)
        self.economic_generator = EconomicScenarioGenerator(random_state)
        self.competitive_simulator = CompetitiveLandscapeSimulator(random_state)
        self.external_simulator = ExternalEventSimulator(random_state)
        self.black_swan_generator = BlackSwanEventGenerator(random_state)
        self.stress_designer = StressScenarioDesigner(random_state)
        self.crisis_replicator = HistoricalCrisisReplicator(random_state)
        self.extreme_simulator = ExtremeConditionSimulator(random_state)
        self.breaking_point_analyzer = BreakingPointAnalyzer(random_state)
        self.resilience_analyzer = ResilienceAnalyzer(random_state)
        self.contingency_validator = ContingencyValidator(random_state)
        self.report_generator = StressTestReportGenerator(random_state)
        self.executive_generator = ExecutiveSummaryGenerator()
    
    def run_combined_scenario(self,
                             scenario_config: Dict[str, Any],
                             include_stress_test: bool = True) -> CombinedScenarioResult:
        """
        Run combined scenario across all domains
        
        Args:
            scenario_config: Configuration for scenario
            include_stress_test: Whether to include stress testing
            
        Returns:
            CombinedScenarioResult object
        """
        start_time = time.time()
        
        # Extract configuration
        jurisdictions = scenario_config.get('jurisdictions', ['USA', 'EU'])
        time_horizon_years = scenario_config.get('time_horizon_years', 2)
        stress_level = scenario_config.get('stress_level', 'moderate')
        
        # Run regulatory scenarios
        regulatory_results = self._run_regulatory_scenarios(jurisdictions)
        
        # Run enforcement scenarios
        enforcement_results = self._run_enforcement_scenarios(time_horizon_years)
        
        # Run market scenarios
        market_results = self._run_market_scenarios()
        
        # Run external factor scenarios
        external_results = self._run_external_scenarios()
        
        # Run stress tests if requested
        stress_results = []
        if include_stress_test:
            stress_results = self._run_stress_scenarios(stress_level)
        
        # Aggregate results
        aggregated_risk = self._aggregate_risk_scores(
            regulatory_results, enforcement_results, market_results,
            external_results, stress_results
        )
        
        total_impact = self._calculate_total_impact(
            regulatory_results, enforcement_results, market_results,
            external_results, stress_results
        )
        
        execution_time = time.time() - start_time
        
        scenario_id = f"COMBINED-{int(time.time())}"
        
        return CombinedScenarioResult(
            scenario_id=scenario_id,
            execution_time_seconds=execution_time,
            regulatory_results=regulatory_results,
            enforcement_results=enforcement_results,
            market_results=market_results,
            external_results=external_results,
            stress_results=stress_results,
            aggregated_risk_score=aggregated_risk,
            total_estimated_impact=total_impact
        )
    
    def _run_regulatory_scenarios(self, jurisdictions: List[str]) -> List[Dict[str, Any]]:
        """Run regulatory scenarios"""
        results = []
        
        # Harmonization scenario
        from .regulatory_scenarios import RegulationSeverity
        harmonization = self.jurisdiction_generator.create_harmonization_scenario(
            jurisdictions=jurisdictions,
            severity=RegulationSeverity.HIGH
        )
        results.append(harmonization.to_dict())
        
        return results
    
    def _run_enforcement_scenarios(self, time_horizon_years: int) -> List[Dict[str, Any]]:
        """Run enforcement scenarios"""
        results = []
        
        # Escalating enforcement
        escalating = self.enforcement_generator.create_escalating_enforcement_scenario(
            time_horizon_years=time_horizon_years
        )
        results.append(escalating.to_dict())
        
        return results
    
    def _run_market_scenarios(self) -> List[Dict[str, Any]]:
        """Run market scenarios"""
        results = []
        
        # Recession scenario
        recession = self.economic_generator.create_recession_scenario()
        results.append(recession.to_dict())
        
        return results
    
    def _run_external_scenarios(self) -> List[Dict[str, Any]]:
        """Run external event scenarios"""
        results = []
        
        # Political change
        political = self.external_simulator.create_political_change_event()
        results.append(political.to_dict())
        
        return results
    
    def _run_stress_scenarios(self, stress_level: str) -> List[Dict[str, Any]]:
        """Run stress test scenarios"""
        results = []
        
        # Regulatory worst case
        worst_case = self.stress_designer.create_regulatory_worst_case()
        results.append(worst_case.to_dict())
        
        return results
    
    def _aggregate_risk_scores(self, *result_sets) -> float:
        """Aggregate risk scores from multiple domains"""
        all_scores = []
        
        for result_set in result_sets:
            for result in result_set:
                # Extract risk-related scores
                if 'total_impact_score' in result:
                    all_scores.append(result['total_impact_score'])
                elif 'overall_impact_score' in result:
                    all_scores.append(result['overall_impact_score'])
                elif 'regulatory_impact_score' in result:
                    all_scores.append(result['regulatory_impact_score'])
                elif 'combined_severity_score' in result:
                    all_scores.append(result['combined_severity_score'])
        
        return float(np.mean(all_scores)) if all_scores else 50.0
    
    def _calculate_total_impact(self, *result_sets) -> float:
        """Calculate total financial impact"""
        total = 0.0
        
        for result_set in result_sets:
            for result in result_set:
                if 'total_estimated_cost' in result:
                    total += result['total_estimated_cost']
                elif 'expected_financial_impact' in result:
                    total += result['expected_financial_impact']
        
        return total


class ScenarioLibrary:
    """Library of pre-built scenario templates"""
    
    def __init__(self, random_state: Optional[int] = None):
        self.random_state = random_state
        self.orchestrator = ScenarioOrchestrator(random_state)
    
    def get_industry_template(self, industry: IndustryTemplate) -> Dict[str, Any]:
        """
        Get pre-built industry scenario template
        
        Args:
            industry: Industry template type
            
        Returns:
            Dictionary with scenario configuration
        """
        templates = {
            IndustryTemplate.FINANCIAL_SERVICES: {
                'name': 'Financial Services Compliance Stress Test',
                'jurisdictions': ['USA', 'EU', 'UK'],
                'key_regulations': ['Basel III', 'Dodd-Frank', 'MiFID II', 'GDPR'],
                'time_horizon_years': 3,
                'stress_level': 'severe',
                'focus_areas': [
                    'capital_requirements',
                    'liquidity_management',
                    'data_privacy',
                    'algorithmic_trading'
                ],
                'expected_severity': 'high'
            },
            IndustryTemplate.HEALTHCARE: {
                'name': 'Healthcare Compliance Stress Test',
                'jurisdictions': ['USA', 'EU'],
                'key_regulations': ['HIPAA', 'HITECH', 'GDPR', 'FDA 21 CFR Part 11'],
                'time_horizon_years': 2,
                'stress_level': 'moderate',
                'focus_areas': [
                    'patient_data_privacy',
                    'medical_device_compliance',
                    'clinical_trial_regulations',
                    'pharmaceutical_tracking'
                ],
                'expected_severity': 'moderate'
            },
            IndustryTemplate.TECHNOLOGY: {
                'name': 'Technology Sector Compliance Stress Test',
                'jurisdictions': ['EU', 'USA', 'China'],
                'key_regulations': ['AI Act', 'DSA', 'DMA', 'GDPR'],
                'time_horizon_years': 2,
                'stress_level': 'extreme',
                'focus_areas': [
                    'ai_governance',
                    'data_protection',
                    'platform_regulation',
                    'cybersecurity'
                ],
                'expected_severity': 'high'
            },
            IndustryTemplate.RETAIL: {
                'name': 'Retail Compliance Stress Test',
                'jurisdictions': ['USA', 'EU'],
                'key_regulations': ['CCPA', 'GDPR', 'PCI DSS'],
                'time_horizon_years': 2,
                'stress_level': 'moderate',
                'focus_areas': [
                    'consumer_privacy',
                    'payment_security',
                    'product_safety',
                    'advertising_compliance'
                ],
                'expected_severity': 'moderate'
            },
            IndustryTemplate.MANUFACTURING: {
                'name': 'Manufacturing Compliance Stress Test',
                'jurisdictions': ['USA', 'EU', 'China'],
                'key_regulations': ['ISO 9001', 'ISO 14001', 'OSHA', 'REACH'],
                'time_horizon_years': 3,
                'stress_level': 'moderate',
                'focus_areas': [
                    'quality_management',
                    'environmental_compliance',
                    'worker_safety',
                    'supply_chain_regulations'
                ],
                'expected_severity': 'moderate'
            }
        }
        
        return templates.get(industry, templates[IndustryTemplate.TECHNOLOGY])
    
    def run_industry_scenario(self, industry: IndustryTemplate) -> CombinedScenarioResult:
        """
        Run pre-built industry scenario
        
        Args:
            industry: Industry type
            
        Returns:
            CombinedScenarioResult
        """
        template = self.get_industry_template(industry)
        
        scenario_config = {
            'jurisdictions': template['jurisdictions'],
            'time_horizon_years': template['time_horizon_years'],
            'stress_level': template['stress_level']
        }
        
        return self.orchestrator.run_combined_scenario(
            scenario_config=scenario_config,
            include_stress_test=True
        )
    
    def list_available_templates(self) -> List[Dict[str, str]]:
        """List all available templates"""
        return [
            {
                'industry': industry.value,
                'name': self.get_industry_template(industry)['name'],
                'severity': self.get_industry_template(industry)['expected_severity']
            }
            for industry in IndustryTemplate
        ]
