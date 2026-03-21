#!/usr/bin/env python3
"""
REGIQ AI/ML - Risk Simulator Regulations Registry
Static regulatory framework definitions used by the risk simulation engine.

Provides:
    - RegulatoryFramework: Dataclass defining a regulation's risk parameters
    - REGULATORY_FRAMEWORKS: Registry of all supported regulations
    - Helper functions for querying frameworks by jurisdiction, type, etc.

These definitions feed directly into:
    - models/penalty_calculator.py  (fine ranges, penalty tiers)
    - models/regulatory_risk.py     (violation probability priors)
    - scenarios/regulatory_scenarios.py (scenario generation)
    - visualization/heatmap_generator.py (jurisdiction × regulation heatmaps)

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import logging
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ── Dataclasses ───────────────────────────────────────────────────────── #

@dataclass
class PenaltyRange:
    """Penalty range for a regulatory framework."""
    min_usd: float
    max_usd: float
    currency: str = "USD"
    basis: str = "per_violation"  # per_violation, per_day, annual_turnover_pct

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RegulatoryFramework:
    """
    Complete definition of a regulatory framework for risk simulation.

    Attributes:
        framework_id:        Unique identifier (e.g. 'eu_ai_act').
        name:                Human-readable name.
        regulation_type:     Category (AI_REGULATION, DATA_PRIVACY, etc.).
        jurisdiction:        Geographic scope.
        effective_date:      ISO date string when regulation took effect.
        risk_weight:         Base risk weight for simulation (0.0–1.0).
        violation_base_prob: Prior probability of violation per year (0.0–1.0).
        penalty_ranges:      List of penalty ranges (can have multiple tiers).
        compliance_domains:  List of compliance areas this regulation covers.
        enforcement_agency:  Primary enforcement body.
        applies_to_ai:       Whether this regulation specifically targets AI/ML.
        high_risk_flag:      Whether non-compliance is considered high-risk.
    """
    framework_id: str
    name: str
    regulation_type: str
    jurisdiction: str
    effective_date: str
    risk_weight: float
    violation_base_prob: float
    penalty_ranges: List[PenaltyRange]
    compliance_domains: List[str]
    enforcement_agency: str
    applies_to_ai: bool = False
    high_risk_flag: bool = False
    notes: str = ""

    @property
    def max_penalty_usd(self) -> float:
        """Return the maximum penalty across all tiers in USD."""
        if not self.penalty_ranges:
            return 0.0
        return max(p.max_usd for p in self.penalty_ranges)

    @property
    def min_penalty_usd(self) -> float:
        """Return the minimum penalty across all tiers in USD."""
        if not self.penalty_ranges:
            return 0.0
        return min(p.min_usd for p in self.penalty_ranges)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["max_penalty_usd"] = self.max_penalty_usd
        d["min_penalty_usd"] = self.min_penalty_usd
        return d


# ── Regulatory Framework Registry ─────────────────────────────────────── #

REGULATORY_FRAMEWORKS: Dict[str, RegulatoryFramework] = {

    "eu_ai_act": RegulatoryFramework(
        framework_id="eu_ai_act",
        name="EU Artificial Intelligence Act (2024/1689)",
        regulation_type="AI_REGULATION",
        jurisdiction="European Union",
        effective_date="2024-08-01",
        risk_weight=0.95,
        violation_base_prob=0.12,
        penalty_ranges=[
            PenaltyRange(min_usd=100_000,  max_usd=7_500_000,   basis="per_violation",      currency="EUR"),  # Tier 1
            PenaltyRange(min_usd=500_000,  max_usd=15_000_000,  basis="per_violation",      currency="EUR"),  # Tier 2 high-risk
            PenaltyRange(min_usd=1_000_000, max_usd=35_000_000, basis="per_violation",      currency="EUR"),  # Tier 3 prohibited
        ],
        compliance_domains=[
            "ai_risk_management", "data_governance", "technical_documentation",
            "transparency", "human_oversight", "conformity_assessment",
            "bias_testing", "model_explainability",
        ],
        enforcement_agency="European Commission / National Market Surveillance",
        applies_to_ai=True,
        high_risk_flag=True,
        notes="High-risk AI systems (Annex III) include credit scoring and loan approval models.",
    ),

    "gdpr": RegulatoryFramework(
        framework_id="gdpr",
        name="General Data Protection Regulation (EU) 2016/679",
        regulation_type="DATA_PRIVACY",
        jurisdiction="European Union",
        effective_date="2018-05-25",
        risk_weight=0.90,
        violation_base_prob=0.15,
        penalty_ranges=[
            PenaltyRange(min_usd=0,         max_usd=10_000_000,  basis="per_violation", currency="EUR"),  # Tier 1
            PenaltyRange(min_usd=100_000,   max_usd=20_000_000,  basis="per_violation", currency="EUR"),  # Tier 2
        ],
        compliance_domains=[
            "data_privacy", "consent_management", "data_subject_rights",
            "automated_decision_transparency", "breach_notification",
            "dpia_requirement", "data_minimisation",
        ],
        enforcement_agency="National Data Protection Authorities / EDPB",
        applies_to_ai=True,
        high_risk_flag=True,
        notes="Article 22 directly impacts AI credit models — right to explanation required.",
    ),

    "ecoa": RegulatoryFramework(
        framework_id="ecoa",
        name="Equal Credit Opportunity Act (ECOA) / Regulation B",
        regulation_type="FAIR_LENDING",
        jurisdiction="United States",
        effective_date="1974-10-28",
        risk_weight=0.85,
        violation_base_prob=0.10,
        penalty_ranges=[
            PenaltyRange(min_usd=0,         max_usd=10_000,      basis="per_violation"),   # Individual
            PenaltyRange(min_usd=0,         max_usd=500_000,     basis="per_violation"),   # Class action
            PenaltyRange(min_usd=0,         max_usd=1_000_000,   basis="per_day"),         # CFPB enforcement
        ],
        compliance_domains=[
            "fair_lending", "disparate_impact_testing", "adverse_action_notices",
            "model_explainability", "proxy_discrimination", "hmda_reporting",
        ],
        enforcement_agency="CFPB / Federal Reserve / OCC",
        applies_to_ai=True,
        high_risk_flag=True,
        notes="80% rule triggers regulatory review. AI models must provide SHAP explanations for adverse action.",
    ),

    "sr_11_7": RegulatoryFramework(
        framework_id="sr_11_7",
        name="SR 11-7: Guidance on Model Risk Management",
        regulation_type="MODEL_RISK",
        jurisdiction="United States",
        effective_date="2011-04-04",
        risk_weight=0.80,
        violation_base_prob=0.20,
        penalty_ranges=[
            PenaltyRange(min_usd=50_000,    max_usd=500_000,     basis="per_violation"),   # MRA
            PenaltyRange(min_usd=100_000,   max_usd=5_000_000,   basis="per_violation"),   # MRIA
        ],
        compliance_domains=[
            "model_validation", "model_documentation", "ongoing_monitoring",
            "model_inventory", "stress_testing", "drift_monitoring", "model_governance",
        ],
        enforcement_agency="Federal Reserve / OCC",
        applies_to_ai=True,
        high_risk_flag=False,
        notes="PSI > 0.25 triggers mandatory re-validation. AI/ML models rated high-risk require annual validation.",
    ),

    "nist_ai_rmf": RegulatoryFramework(
        framework_id="nist_ai_rmf",
        name="NIST AI Risk Management Framework 1.0",
        regulation_type="AI_GOVERNANCE",
        jurisdiction="United States",
        effective_date="2023-01-26",
        risk_weight=0.55,
        violation_base_prob=0.08,
        penalty_ranges=[
            PenaltyRange(min_usd=0, max_usd=0, basis="per_violation"),  # Voluntary — reputational risk
        ],
        compliance_domains=[
            "ai_risk_governance", "fairness_measurement", "explainability",
            "accountability", "bias_management", "robustness_testing",
        ],
        enforcement_agency="NIST (voluntary framework)",
        applies_to_ai=True,
        high_risk_flag=False,
        notes="Voluntary framework but increasingly referenced in procurement and litigation.",
    ),

    "bcbs_239": RegulatoryFramework(
        framework_id="bcbs_239",
        name="BCBS 239: Risk Data Aggregation and Risk Reporting",
        regulation_type="RISK_REPORTING",
        jurisdiction="International",
        effective_date="2016-01-01",
        risk_weight=0.70,
        violation_base_prob=0.18,
        penalty_ranges=[
            PenaltyRange(min_usd=100_000,   max_usd=10_000_000,  basis="per_violation"),
        ],
        compliance_domains=[
            "data_governance", "data_accuracy", "data_completeness",
            "risk_reporting", "audit_trail", "stress_testing_documentation",
        ],
        enforcement_agency="Basel Committee / National Banking Supervisors",
        applies_to_ai=False,
        high_risk_flag=False,
        notes="Applies to G-SIBs and D-SIBs. AI model outputs in risk reports must meet data quality standards.",
    ),

    "ccpa": RegulatoryFramework(
        framework_id="ccpa",
        name="California Consumer Privacy Act (CCPA/CPRA)",
        regulation_type="DATA_PRIVACY",
        jurisdiction="United States (California)",
        effective_date="2020-01-01",
        risk_weight=0.65,
        violation_base_prob=0.08,
        penalty_ranges=[
            PenaltyRange(min_usd=0,       max_usd=2_500,   basis="per_violation"),    # Unintentional
            PenaltyRange(min_usd=0,       max_usd=7_500,   basis="per_violation"),    # Intentional
        ],
        compliance_domains=[
            "data_privacy", "consumer_rights", "opt_out_rights",
            "data_subject_rights", "automated_decision_transparency",
        ],
        enforcement_agency="California Privacy Protection Agency (CPPA)",
        applies_to_ai=True,
        high_risk_flag=False,
        notes="CPRA (2023 amendments) expanded rights for automated decision-making.",
    ),

    "mifid_ii": RegulatoryFramework(
        framework_id="mifid_ii",
        name="MiFID II / MiFIR",
        regulation_type="FINANCIAL_MARKETS",
        jurisdiction="European Union",
        effective_date="2018-01-03",
        risk_weight=0.75,
        violation_base_prob=0.12,
        penalty_ranges=[
            PenaltyRange(min_usd=0,         max_usd=5_000_000,   basis="per_violation", currency="EUR"),
            PenaltyRange(min_usd=0,         max_usd=15_000_000,  basis="per_violation", currency="EUR"),
        ],
        compliance_domains=[
            "algorithmic_trading", "market_surveillance", "best_execution",
            "transaction_reporting", "product_governance",
        ],
        enforcement_agency="ESMA / National Competent Authorities",
        applies_to_ai=True,
        high_risk_flag=False,
        notes="Algorithmic trading models require pre/post-trade risk controls and kill switches.",
    ),
}


# ── Registry Helper Functions ──────────────────────────────────────────── #

def get_framework(framework_id: str) -> Optional[RegulatoryFramework]:
    """Return a regulatory framework by ID, or None if not found."""
    return REGULATORY_FRAMEWORKS.get(framework_id)


def get_frameworks_by_jurisdiction(jurisdiction: str) -> List[RegulatoryFramework]:
    """Return all frameworks for a given jurisdiction (case-insensitive partial match)."""
    j = jurisdiction.lower()
    return [f for f in REGULATORY_FRAMEWORKS.values() if j in f.jurisdiction.lower()]


def get_frameworks_by_type(regulation_type: str) -> List[RegulatoryFramework]:
    """Return all frameworks of a given regulation type."""
    rt = regulation_type.upper()
    return [f for f in REGULATORY_FRAMEWORKS.values() if f.regulation_type == rt]


def get_ai_frameworks() -> List[RegulatoryFramework]:
    """Return all frameworks that apply to AI/ML systems."""
    return [f for f in REGULATORY_FRAMEWORKS.values() if f.applies_to_ai]


def get_high_risk_frameworks() -> List[RegulatoryFramework]:
    """Return all frameworks flagged as high-risk for non-compliance."""
    return [f for f in REGULATORY_FRAMEWORKS.values() if f.high_risk_flag]


def get_framework_ids() -> List[str]:
    """Return all registered framework IDs."""
    return list(REGULATORY_FRAMEWORKS.keys())


def get_penalty_range(framework_id: str) -> Optional[Tuple[float, float]]:
    """Return (min_penalty_usd, max_penalty_usd) for a framework."""
    fw = REGULATORY_FRAMEWORKS.get(framework_id)
    if not fw:
        return None
    return fw.min_penalty_usd, fw.max_penalty_usd


def get_simulation_params(framework_id: str) -> Optional[Dict[str, Any]]:
    """
    Return a dict of simulation parameters for the risk models.
    Used by models/regulatory_risk.py and models/penalty_calculator.py.
    """
    fw = REGULATORY_FRAMEWORKS.get(framework_id)
    if not fw:
        return None
    return {
        "framework_id": fw.framework_id,
        "name": fw.name,
        "regulation_type": fw.regulation_type,
        "jurisdiction": fw.jurisdiction,
        "risk_weight": fw.risk_weight,
        "violation_base_prob": fw.violation_base_prob,
        "max_penalty_usd": fw.max_penalty_usd,
        "min_penalty_usd": fw.min_penalty_usd,
        "penalty_tiers": len(fw.penalty_ranges),
        "compliance_domains": fw.compliance_domains,
        "applies_to_ai": fw.applies_to_ai,
        "high_risk_flag": fw.high_risk_flag,
    }


def list_all_frameworks() -> List[Dict[str, Any]]:
    """Return a summary list of all registered frameworks."""
    return [
        {
            "framework_id": fw.framework_id,
            "name": fw.name,
            "regulation_type": fw.regulation_type,
            "jurisdiction": fw.jurisdiction,
            "risk_weight": fw.risk_weight,
            "max_penalty_usd": fw.max_penalty_usd,
            "applies_to_ai": fw.applies_to_ai,
            "high_risk_flag": fw.high_risk_flag,
        }
        for fw in sorted(REGULATORY_FRAMEWORKS.values(), key=lambda x: x.risk_weight, reverse=True)
    ]


def get_registry_stats() -> Dict[str, Any]:
    """Return statistics about the regulatory framework registry."""
    frameworks = list(REGULATORY_FRAMEWORKS.values())
    return {
        "total_frameworks": len(frameworks),
        "ai_applicable": sum(1 for f in frameworks if f.applies_to_ai),
        "high_risk": sum(1 for f in frameworks if f.high_risk_flag),
        "jurisdictions": list(set(f.jurisdiction for f in frameworks)),
        "regulation_types": list(set(f.regulation_type for f in frameworks)),
        "max_single_penalty_usd": max(f.max_penalty_usd for f in frameworks),
    }
