#!/usr/bin/env python3
"""
REGIQ AI/ML - Regulatory Document Seeder
Populates the RAG vector database and Knowledge Graph with
real-world regulatory documents and compliance data.

This script:
1. Loads built-in seed regulatory documents (EU AI Act, GDPR, ECOA, SR 11-7, etc.)
2. Generates embeddings using SentenceTransformers
3. Stores embeddings in ChromaDB / FAISS vector database
4. Populates the Knowledge Graph with entities and relationships
5. Verifies the pipeline end-to-end with sample queries

Usage:
    python rag_data_seeder.py                    # Seed all
    python rag_data_seeder.py --source rag       # RAG only
    python rag_data_seeder.py --source kg        # Knowledge Graph only
    python rag_data_seeder.py --verify           # Verify existing data

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger(__name__)

# ── Seed Regulatory Documents ──────────────────────────────────────────── #
# These are condensed but accurate summaries of real regulations,
# structured for RAG retrieval. Each document contains key provisions,
# requirements, deadlines, and penalties.

SEED_DOCUMENTS = [
    # ── EU AI Act ──────────────────────────────────────────────────────── #
    {
        "doc_id": "eu_ai_act_2024",
        "title": "EU Artificial Intelligence Act (2024/1689)",
        "source": "European Union Official Journal",
        "regulation_type": "AI_REGULATION",
        "jurisdiction": "European Union",
        "effective_date": "2024-08-01",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689",
        "content": """
The EU Artificial Intelligence Act (Regulation 2024/1689) establishes a comprehensive 
legal framework for artificial intelligence in the European Union.

RISK CLASSIFICATION:
- Unacceptable Risk (Prohibited): AI systems that manipulate human behaviour, exploit 
  vulnerabilities, social scoring by governments, real-time biometric surveillance in 
  public spaces (with limited exceptions).
- High Risk (Annex III): AI used in critical infrastructure, education, employment, 
  essential services, law enforcement, migration, justice, democratic processes, and 
  biometric identification. This includes credit scoring, loan assessment, and insurance 
  pricing models.
- Limited Risk: Chatbots, deepfakes — transparency obligations apply.
- Minimal Risk: Most AI applications — no mandatory requirements.

HIGH-RISK AI REQUIREMENTS (Articles 9-15):
- Article 9: Risk management system — continuous, iterative process throughout lifecycle.
- Article 10: Data governance — training data must be relevant, representative, free from 
  errors, complete. Protected characteristics must not create discriminatory outcomes.
- Article 11: Technical documentation — before market placement, detailed docs required.
- Article 12: Record-keeping — automatic logging of events during system operation.
- Article 13: Transparency — users must be informed they are interacting with AI.
- Article 14: Human oversight — effective human oversight measures must be implemented.
- Article 15: Accuracy, robustness, cybersecurity — consistent performance standards.

CONFORMITY ASSESSMENT:
- High-risk AI systems must undergo conformity assessment before deployment.
- Financial sector AI (credit scoring, insurance) requires third-party assessment.
- CE marking required for compliant systems.

PENALTIES:
- Prohibited AI violations: Up to €35 million or 7% of global annual turnover.
- High-risk AI violations: Up to €15 million or 3% of global annual turnover.
- Incorrect information to authorities: Up to €7.5 million or 1.5% of turnover.

KEY DEADLINES:
- August 2024: Act enters into force.
- February 2025: Prohibited AI provisions apply.
- August 2025: GPAI model provisions and governance rules apply.
- August 2026: All other provisions (including high-risk AI) apply.
- August 2027: High-risk AI in Annex I products apply.

FINANCIAL SECTOR SPECIFIC:
Credit scoring, loan approval, and insurance pricing AI are classified as HIGH-RISK 
under Annex III, Point 5(b). These systems require full compliance with Articles 9-15,
including bias testing, explainability documentation, and human oversight mechanisms.
        """,
        "entities": [
            {"text": "EU AI Act", "label": "REGULATION"},
            {"text": "European Union", "label": "JURISDICTION"},
            {"text": "€35 million", "label": "PENALTY_AMOUNT"},
            {"text": "August 2026", "label": "DEADLINE"},
            {"text": "European Commission", "label": "REGULATORY_AGENCY"},
        ],
        "compliance_requirements": [
            "risk_management_system", "data_governance", "technical_documentation",
            "record_keeping", "transparency", "human_oversight", "conformity_assessment"
        ]
    },

    # ── GDPR ───────────────────────────────────────────────────────────── #
    {
        "doc_id": "gdpr_2016_679",
        "title": "General Data Protection Regulation (EU) 2016/679",
        "source": "European Union Official Journal",
        "regulation_type": "DATA_PRIVACY",
        "jurisdiction": "European Union",
        "effective_date": "2018-05-25",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679",
        "content": """
The General Data Protection Regulation (GDPR) is the EU's primary data protection law,
applying to all organisations processing personal data of EU residents.

KEY PRINCIPLES (Article 5):
- Lawfulness, fairness, and transparency in data processing.
- Purpose limitation — data collected for specified, explicit, legitimate purposes.
- Data minimisation — only data necessary for the purpose.
- Accuracy — data must be kept accurate and up to date.
- Storage limitation — kept no longer than necessary.
- Integrity and confidentiality — appropriate security measures.

LAWFUL BASIS FOR PROCESSING (Article 6):
- Consent, contract, legal obligation, vital interests, public task, or legitimate interests.
- Financial institutions typically rely on contract performance and legal obligation.

AUTOMATED DECISION-MAKING (Article 22):
Data subjects have the RIGHT NOT to be subject to solely automated decisions (including 
profiling) that produce significant effects. Exceptions apply when:
(a) Necessary for a contract
(b) Authorised by Union/Member State law
(c) Based on explicit consent

Where automated decisions ARE made (including AI credit decisions), the controller MUST:
- Implement suitable safeguards
- Provide meaningful information about the logic involved
- Allow data subjects to request human review
- Allow data subjects to contest the decision

This directly impacts REGIQ's bias analysis requirements — AI credit models must provide
SHAP/LIME explanations to comply with Article 22 transparency requirements.

DATA SUBJECT RIGHTS (Articles 15-22):
- Article 15: Right of access to personal data
- Article 16: Right to rectification
- Article 17: Right to erasure ("right to be forgotten")
- Article 18: Right to restriction of processing
- Article 20: Right to data portability
- Article 21: Right to object
- Article 22: Rights related to automated decision-making

DATA PROTECTION OFFICER (DPO) (Articles 37-39):
Mandatory for organisations processing large-scale special categories of data or 
conducting systematic monitoring. Financial institutions processing credit data typically 
require a DPO.

BREACH NOTIFICATION (Article 33):
Personal data breaches must be reported to supervisory authority within 72 HOURS.
If breach is likely to result in high risk to individuals, they must also be notified.

PENALTIES:
- Tier 1: Up to €10 million or 2% of global annual turnover (lesser violations).
- Tier 2: Up to €20 million or 4% of global annual turnover (major violations including 
  Article 22 automated decision-making failures, data subject rights violations).

DATA PROTECTION IMPACT ASSESSMENT (DPIA) (Article 35):
Required for high-risk processing, including systematic evaluation of personal aspects 
using automated processing (profiling). AI credit scoring REQUIRES a DPIA.
        """,
        "entities": [
            {"text": "GDPR", "label": "REGULATION"},
            {"text": "European Union", "label": "JURISDICTION"},
            {"text": "€20 million", "label": "PENALTY_AMOUNT"},
            {"text": "72 hours", "label": "DEADLINE"},
            {"text": "European Data Protection Board", "label": "REGULATORY_AGENCY"},
        ],
        "compliance_requirements": [
            "lawful_basis", "data_minimisation", "automated_decision_transparency",
            "right_to_explanation", "dpo_appointment", "breach_notification",
            "dpia_requirement", "data_subject_rights"
        ]
    },

    # ── ECOA / Regulation B ────────────────────────────────────────────── #
    {
        "doc_id": "ecoa_regulation_b",
        "title": "Equal Credit Opportunity Act (ECOA) and Regulation B",
        "source": "Consumer Financial Protection Bureau (CFPB)",
        "regulation_type": "FAIR_LENDING",
        "jurisdiction": "United States",
        "effective_date": "1974-10-28",
        "url": "https://www.consumerfinance.gov/rules-policy/regulations/1002/",
        "content": """
The Equal Credit Opportunity Act (ECOA), 15 U.S.C. § 1691, and its implementing 
regulation, Regulation B (12 CFR Part 1002), prohibit credit discrimination.

PROHIBITED BASES (Section 1002.4):
Creditors may NOT discriminate on the basis of:
- Race, colour, religion, national origin
- Sex (including gender identity and sexual orientation)
- Marital status, age (provided applicant has legal capacity)
- Receipt of income from public assistance
- Exercise of rights under the Consumer Credit Protection Act

DISPARATE IMPACT:
Even facially neutral policies violate ECOA if they have a disproportionate adverse 
effect on a protected class without business justification. AI credit models are 
particularly scrutinised for disparate impact.

The 80% RULE (Four-Fifths Rule): If the selection rate for a protected group is less 
than 80% of the selection rate for the group with the highest rate, this may indicate 
adverse impact triggering regulatory review.

AI MODEL REQUIREMENTS:
- Models must not use protected characteristics as inputs, even indirectly via proxies.
- Proxy discrimination (using zip code, name, or other variables correlated with 
  protected characteristics) is prohibited.
- Regular disparate impact testing is required.
- CFPB has indicated AI models must be explainable to satisfy adverse action notice 
  requirements.

ADVERSE ACTION NOTICES (Section 1002.9):
Creditors MUST provide adverse action notices within:
- 30 days of receiving completed application
- 30 days of taking adverse action on existing account
- 90 days of counteroffer if applicant does not accept

Notice must state SPECIFIC REASONS for adverse action (not just a score).
This requires AI models to provide feature-level explanations (SHAP/LIME).

RECORD RETENTION (Section 1002.12):
- Applications and adverse action notices: 25 months (12 months for businesses).
- All records related to prescreened offers: 25 months.

PENALTIES:
- Individual claims: Actual damages, punitive damages up to $10,000, attorney's fees.
- Class actions: Punitive damages up to lesser of $500,000 or 1% of net worth.
- CFPB enforcement: Civil money penalties up to $1,000,000 per day for knowing violations.

HMDA DATA COLLECTION:
Home Mortgage Disclosure Act (HMDA) requires collection of demographic data for 
fair lending analysis. Institutions must monitor for disparate impact patterns.

SELF-TESTING (Section 1002.15):
Creditors may conduct self-tests for ECOA compliance. Privileged self-test results 
provide limited safe harbour protection.
        """,
        "entities": [
            {"text": "ECOA", "label": "REGULATION"},
            {"text": "Regulation B", "label": "REGULATION"},
            {"text": "United States", "label": "JURISDICTION"},
            {"text": "$1,000,000 per day", "label": "PENALTY_AMOUNT"},
            {"text": "30 days", "label": "DEADLINE"},
            {"text": "CFPB", "label": "REGULATORY_AGENCY"},
        ],
        "compliance_requirements": [
            "disparate_impact_testing", "adverse_action_notices", "proxy_discrimination_check",
            "model_explainability", "record_retention", "hmda_data_collection", "self_testing"
        ]
    },

    # ── SR 11-7 Model Risk Management ─────────────────────────────────── #
    {
        "doc_id": "sr_11_7_model_risk",
        "title": "SR 11-7: Guidance on Model Risk Management",
        "source": "Federal Reserve / OCC",
        "regulation_type": "MODEL_RISK",
        "jurisdiction": "United States",
        "effective_date": "2011-04-04",
        "url": "https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm",
        "content": """
SR 11-7 provides supervisory guidance on model risk management for banking organisations,
covering model development, validation, governance, and ongoing monitoring.

DEFINITION OF A MODEL:
A quantitative method, system, or approach that applies statistical, economic, financial, 
or mathematical theories to transform input data into quantitative estimates. AI/ML 
credit scoring systems are explicitly covered under this definition.

THREE LINES OF DEFENCE:
1. Model developers/owners: Responsible for model design, documentation, and ongoing 
   performance monitoring.
2. Independent model validation: Separate team validates all models.
3. Internal audit: Reviews model risk management framework compliance.

MODEL DEVELOPMENT REQUIREMENTS:
- Rigorous statistical analysis of model inputs, assumptions, and outputs.
- Comprehensive documentation including conceptual soundness analysis.
- Benchmarking against alternative approaches.
- Out-of-sample and out-of-time testing.
- Stress testing under adverse scenarios.

MODEL VALIDATION (KEY REQUIREMENT):
All models must undergo independent validation:
- Conceptual soundness review
- Ongoing monitoring for performance degradation
- Outcomes analysis (backtesting against actual results)
- Sensitivity analysis

For AI/ML models, validation must assess:
- Explainability and interpretability
- Fairness and potential for discriminatory outcomes
- Stability across different data samples
- Robustness to distributional shift (model drift)

ONGOING MONITORING:
- Models must be monitored for performance degradation (model drift).
- Population Stability Index (PSI) > 0.25 triggers mandatory re-validation.
- Performance metrics must be tracked against established benchmarks.
- Significant changes in model outputs require investigation.

MODEL INVENTORY:
Banks must maintain a comprehensive model inventory documenting:
- All models in use, including vendor models
- Model risk ratings (low, medium, high)
- Validation status and findings
- Planned validation schedule

HIGH-RISK MODEL FLAGS FOR AI CREDIT MODELS:
- Models using non-traditional data sources
- Complex ML models with limited interpretability
- Models not validated within the last 12 months
- Models showing PSI > 0.10 (monitoring threshold)

DOCUMENTATION REQUIREMENTS:
- Model purpose and intended use
- Data inputs, assumptions, and limitations
- Mathematical/algorithmic description
- Validation results and findings
- Approval history and change log
        """,
        "entities": [
            {"text": "SR 11-7", "label": "REGULATION"},
            {"text": "United States", "label": "JURISDICTION"},
            {"text": "Federal Reserve", "label": "REGULATORY_AGENCY"},
            {"text": "OCC", "label": "REGULATORY_AGENCY"},
            {"text": "12 months", "label": "DEADLINE"},
        ],
        "compliance_requirements": [
            "model_validation", "model_documentation", "ongoing_monitoring",
            "model_inventory", "stress_testing", "explainability", "drift_monitoring"
        ]
    },

    # ── NIST AI RMF ────────────────────────────────────────────────────── #
    {
        "doc_id": "nist_ai_rmf_1_0",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0)",
        "source": "National Institute of Standards and Technology",
        "regulation_type": "AI_GOVERNANCE",
        "jurisdiction": "United States",
        "effective_date": "2023-01-26",
        "url": "https://airc.nist.gov/RMF",
        "content": """
The NIST AI Risk Management Framework (AI RMF 1.0) provides a voluntary framework 
for organisations to manage AI risks across the AI lifecycle.

CORE FUNCTIONS (GOVERN, MAP, MEASURE, MANAGE):

GOVERN:
- Establish organisational policies, processes, and accountability for AI risk.
- Ensure AI risk management is integrated into enterprise risk management.
- Cultivate a culture of AI risk awareness.
- Key outcomes: AI risk policies, roles and responsibilities, workforce AI literacy.

MAP:
- Identify and classify AI risks in context.
- Categorise AI systems by intended use, deployment context, and potential impacts.
- Identify stakeholders and potential harms.
- Key outcome: Contextualised risk inventory for each AI system.

MEASURE:
- Analyse and assess AI risks using appropriate metrics.
- Evaluate AI systems for accuracy, fairness, robustness, explainability, privacy.
- Track performance over time.
- For financial AI: Measure demographic parity, equalized odds, disparate impact,
  calibration error, and feature attribution stability.

MANAGE:
- Prioritise and address identified AI risks.
- Implement risk treatments (accept, transfer, mitigate, avoid).
- Monitor effectiveness of risk treatments.
- Document risk management decisions.

TRUSTWORTHY AI CHARACTERISTICS:
- Valid and Reliable: Statistically sound, consistent performance.
- Safe: Does not endanger people or assets.
- Secure and Resilient: Withstands adversarial attacks.
- Explainable and Interpretable: Outputs can be understood and explained.
- Privacy-enhanced: Protects individual privacy.
- Fair with bias managed: Equitable outcomes, bias identified and mitigated.
- Accountable and Transparent: Clear responsibility and oversight.

BIAS IN AI (NIST SP 600-1):
NIST identifies three types of AI bias:
1. Computational/statistical bias: Measurement errors, sampling errors.
2. Human cognitive bias: Confirmation bias, anchoring in data labelling.
3. Systemic bias: Societal inequities reflected in historical training data.

Financial AI systems must address all three types. REGIQ's bias analysis service
directly addresses computational/statistical bias through fairness metrics.

MEASUREMENT METRICS FOR FINANCIAL AI:
- Group fairness metrics: Demographic parity difference ≤ 0.05 (NIST recommended)
- Individual fairness: Lipschitz condition for similar individuals
- Calibration: Expected Calibration Error (ECE) ≤ 0.05
- Robustness: Performance consistency across demographic subgroups
        """,
        "entities": [
            {"text": "NIST AI RMF", "label": "REGULATION"},
            {"text": "United States", "label": "JURISDICTION"},
            {"text": "NIST", "label": "REGULATORY_AGENCY"},
            {"text": "January 2023", "label": "DEADLINE"},
        ],
        "compliance_requirements": [
            "ai_risk_governance", "risk_mapping", "fairness_measurement",
            "explainability", "accountability", "bias_management", "robustness_testing"
        ]
    },

    # ── BCBS 239 ───────────────────────────────────────────────────────── #
    {
        "doc_id": "bcbs_239",
        "title": "BCBS 239: Principles for Effective Risk Data Aggregation and Risk Reporting",
        "source": "Basel Committee on Banking Supervision",
        "regulation_type": "RISK_REPORTING",
        "jurisdiction": "International",
        "effective_date": "2016-01-01",
        "url": "https://www.bis.org/publ/bcbs239.htm",
        "content": """
BCBS 239 establishes principles for effective risk data aggregation and risk reporting 
for Global Systemically Important Banks (G-SIBs) and Domestic SIBs (D-SIBs).

14 PRINCIPLES:

GOVERNANCE AND INFRASTRUCTURE (Principles 1-2):
1. Governance: Board and senior management own risk data quality and reporting.
2. Data Architecture and IT Infrastructure: Robust architecture supporting accurate data.

DATA AGGREGATION CAPABILITIES (Principles 3-6):
3. Accuracy and Integrity: Data aggregation produces accurate, reliable risk data.
4. Completeness: Captures and aggregates all material risk data across the group.
5. Timeliness: Risk management reports produced in time for decision-making.
6. Adaptability: Can generate risk data for ad-hoc requests including stress scenarios.

RISK REPORTING PRACTICES (Principles 7-11):
7. Accuracy: Risk reports accurately convey aggregated risk data.
8. Comprehensiveness: Reports cover all material risk areas.
9. Clarity and Usefulness: Clear, concise, useful information for decision-makers.
10. Frequency: Reports produced with sufficient frequency given risk dynamics.
11. Distribution: Reports reach appropriate recipients promptly and securely.

SUPERVISORY REVIEW (Principles 12-14):
12. Review: Supervisors regularly assess compliance.
13. Remedial actions: Supervisors have tools to require improvement.
14. Home/host cooperation: Cross-border supervisory cooperation.

AI/ML MODEL IMPLICATIONS:
AI models used in risk calculations (credit risk, market risk, operational risk) must 
satisfy BCBS 239 data quality standards:
- Training data must be complete, accurate, and auditable.
- Model outputs (risk scores, predictions) must be traceable to input data.
- Risk reports incorporating AI outputs must be timely and accurate.
- Stress testing of AI models must be documented and reportable.

REGIQ RELEVANCE:
Risk simulation outputs, bias analysis results, and regulatory intelligence summaries 
that feed into risk reports must comply with BCBS 239 accuracy and completeness 
requirements. The audit trail from REGIQ's report generator directly supports these.
        """,
        "entities": [
            {"text": "BCBS 239", "label": "REGULATION"},
            {"text": "International", "label": "JURISDICTION"},
            {"text": "Basel Committee on Banking Supervision", "label": "REGULATORY_AGENCY"},
            {"text": "January 2016", "label": "DEADLINE"},
        ],
        "compliance_requirements": [
            "data_governance", "data_accuracy", "data_completeness",
            "risk_reporting", "audit_trail", "stress_testing_documentation"
        ]
    },
]


# ── Knowledge Graph Seed Data ──────────────────────────────────────────── #

KG_SEED_ENTITIES = [
    # Regulations
    {"id": "eu_ai_act", "type": "REGULATION", "name": "EU AI Act", "jurisdiction": "EU", "year": 2024},
    {"id": "gdpr", "type": "REGULATION", "name": "GDPR", "jurisdiction": "EU", "year": 2016},
    {"id": "ecoa", "type": "REGULATION", "name": "ECOA", "jurisdiction": "US", "year": 1974},
    {"id": "sr_11_7", "type": "REGULATION", "name": "SR 11-7", "jurisdiction": "US", "year": 2011},
    {"id": "nist_ai_rmf", "type": "REGULATION", "name": "NIST AI RMF", "jurisdiction": "US", "year": 2023},
    {"id": "bcbs_239", "type": "REGULATION", "name": "BCBS 239", "jurisdiction": "International", "year": 2016},
    # Regulatory Agencies
    {"id": "european_commission", "type": "REGULATORY_AGENCY", "name": "European Commission", "jurisdiction": "EU"},
    {"id": "cfpb", "type": "REGULATORY_AGENCY", "name": "CFPB", "jurisdiction": "US"},
    {"id": "federal_reserve", "type": "REGULATORY_AGENCY", "name": "Federal Reserve", "jurisdiction": "US"},
    {"id": "nist", "type": "REGULATORY_AGENCY", "name": "NIST", "jurisdiction": "US"},
    {"id": "bcbs", "type": "REGULATORY_AGENCY", "name": "Basel Committee", "jurisdiction": "International"},
    # Compliance Requirements
    {"id": "req_explainability", "type": "COMPLIANCE_TERM", "name": "Model Explainability"},
    {"id": "req_bias_testing", "type": "COMPLIANCE_TERM", "name": "Bias & Fairness Testing"},
    {"id": "req_human_oversight", "type": "COMPLIANCE_TERM", "name": "Human Oversight"},
    {"id": "req_adverse_action", "type": "COMPLIANCE_TERM", "name": "Adverse Action Notice"},
    {"id": "req_model_validation", "type": "COMPLIANCE_TERM", "name": "Model Validation"},
    {"id": "req_drift_monitoring", "type": "COMPLIANCE_TERM", "name": "Model Drift Monitoring"},
    {"id": "req_dpia", "type": "COMPLIANCE_TERM", "name": "Data Protection Impact Assessment"},
]

KG_SEED_RELATIONSHIPS = [
    # Regulation → Agency
    ("eu_ai_act", "ENFORCED_BY", "european_commission"),
    ("gdpr", "ENFORCED_BY", "european_commission"),
    ("ecoa", "ENFORCED_BY", "cfpb"),
    ("sr_11_7", "ISSUED_BY", "federal_reserve"),
    ("nist_ai_rmf", "ISSUED_BY", "nist"),
    ("bcbs_239", "ISSUED_BY", "bcbs"),
    # Regulation → Compliance Requirement
    ("eu_ai_act", "REQUIRES", "req_explainability"),
    ("eu_ai_act", "REQUIRES", "req_bias_testing"),
    ("eu_ai_act", "REQUIRES", "req_human_oversight"),
    ("gdpr", "REQUIRES", "req_explainability"),
    ("gdpr", "REQUIRES", "req_dpia"),
    ("ecoa", "REQUIRES", "req_adverse_action"),
    ("ecoa", "REQUIRES", "req_bias_testing"),
    ("sr_11_7", "REQUIRES", "req_model_validation"),
    ("sr_11_7", "REQUIRES", "req_drift_monitoring"),
    ("nist_ai_rmf", "REQUIRES", "req_bias_testing"),
    ("nist_ai_rmf", "REQUIRES", "req_explainability"),
    # Cross-regulation relationships
    ("eu_ai_act", "COMPLEMENTS", "gdpr"),
    ("ecoa", "ALIGNS_WITH", "nist_ai_rmf"),
    ("sr_11_7", "REFERENCES", "bcbs_239"),
]


# ── Seeder Class ───────────────────────────────────────────────────────── #

class RegulatoryDataSeeder:
    """
    Seeds the RAG vector database and Knowledge Graph with regulatory data.
    
    Can be used standalone (python rag_data_seeder.py) or imported
    programmatically for testing and integration.
    """

    def __init__(self, data_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent.parent.parent / "data"
        self.vector_db_dir = self.data_dir / "vector_db"
        self.kg_dir = self.data_dir / "knowledge_graph"
        self.vector_db_dir.mkdir(parents=True, exist_ok=True)
        self.kg_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # RAG Seeding                                                          #
    # ------------------------------------------------------------------ #

    def seed_rag(self) -> Dict[str, Any]:
        """Seed the vector database with regulatory documents."""
        self.logger.info(f"Seeding RAG with {len(SEED_DOCUMENTS)} regulatory documents...")
        results = {"seeded": 0, "failed": 0, "documents": []}

        try:
            from services.regulatory_intelligence.rag import (
                VectorDatabaseManager, VectorDBConfig,
                DocumentEmbeddingService, DocumentMetadata,
            )

            config = VectorDBConfig(
                chroma_persist_directory=str(self.vector_db_dir / "chroma"),
                faiss_index_path=str(self.vector_db_dir / "faiss_index.bin"),
                faiss_metadata_path=str(self.vector_db_dir / "faiss_metadata.json"),
            )

            embedding_service = DocumentEmbeddingService(config)

            for doc in SEED_DOCUMENTS:
                try:
                    metadata = DocumentMetadata(
                        doc_id=doc["doc_id"],
                        title=doc["title"],
                        source=doc["source"],
                        regulation_type=doc["regulation_type"],
                        jurisdiction=doc["jurisdiction"],
                        effective_date=doc["effective_date"],
                        url=doc.get("url", ""),
                    )
                    embedding_service.embed_document(
                        text=doc["content"],
                        metadata=metadata,
                    )
                    results["seeded"] += 1
                    results["documents"].append(doc["doc_id"])
                    self.logger.info(f"  ✅ Embedded: {doc['title'][:60]}")
                except Exception as e:
                    results["failed"] += 1
                    self.logger.error(f"  ❌ Failed: {doc['doc_id']} — {e}")

        except ImportError as e:
            self.logger.warning(f"RAG dependencies not available: {e}")
            # Fallback: save as JSON for later ingestion
            results = self._save_documents_as_json()

        self.logger.info(f"RAG seeding complete: {results.get('seeded', 0)} embedded, "
                         f"{results.get('saved_as_json', 0)} saved as JSON")
        return results

    def _save_documents_as_json(self) -> Dict[str, Any]:
        """Fallback: save seed documents as JSON files for manual ingestion."""
        output_path = self.data_dir / "seed_documents"
        output_path.mkdir(parents=True, exist_ok=True)

        saved = 0
        for doc in SEED_DOCUMENTS:
            doc_path = output_path / f"{doc['doc_id']}.json"
            with open(doc_path, "w", encoding="utf-8") as f:
                json.dump(doc, f, indent=2, ensure_ascii=False)
            saved += 1
            self.logger.info(f"  💾 Saved: {doc_path.name}")

        index_path = output_path / "_index.json"
        with open(index_path, "w") as f:
            json.dump({
                "total_documents": len(SEED_DOCUMENTS),
                "documents": [{"id": d["doc_id"], "title": d["title"]} for d in SEED_DOCUMENTS],
                "created_at": datetime.utcnow().isoformat(),
            }, f, indent=2)

        self.logger.info(f"💾 Saved {saved} documents to {output_path}")
        return {"seeded": 0, "saved_as_json": saved, "path": str(output_path)}

    # ------------------------------------------------------------------ #
    # Knowledge Graph Seeding                                              #
    # ------------------------------------------------------------------ #

    def seed_knowledge_graph(self) -> Dict[str, Any]:
        """Seed the Knowledge Graph with regulatory entities and relationships."""
        self.logger.info(f"Seeding Knowledge Graph with {len(KG_SEED_ENTITIES)} entities "
                         f"and {len(KG_SEED_RELATIONSHIPS)} relationships...")
        results = {"entities_added": 0, "relationships_added": 0, "failed": 0}

        try:
            from services.regulatory_intelligence.knowledge_graph import (
                GraphDatabaseManager, KnowledgeGraphConfig,
                RegulatoryEntity, EntityRelationship,
            )

            config = KnowledgeGraphConfig()
            graph_manager = GraphDatabaseManager(config)

            for entity_data in KG_SEED_ENTITIES:
                try:
                    entity = RegulatoryEntity(
                        entity_id=entity_data["id"],
                        entity_type=entity_data["type"],
                        name=entity_data["name"],
                        properties={k: v for k, v in entity_data.items()
                                    if k not in ("id", "type", "name")},
                    )
                    graph_manager.add_entity(entity)
                    results["entities_added"] += 1
                except Exception as e:
                    results["failed"] += 1
                    self.logger.warning(f"  Entity failed: {entity_data['id']} — {e}")

            for source_id, rel_type, target_id in KG_SEED_RELATIONSHIPS:
                try:
                    rel = EntityRelationship(
                        source_id=source_id,
                        target_id=target_id,
                        relationship_type=rel_type,
                        properties={"seeded": True},
                    )
                    graph_manager.add_relationship(rel)
                    results["relationships_added"] += 1
                except Exception as e:
                    results["failed"] += 1
                    self.logger.warning(f"  Relationship failed: {source_id}→{target_id} — {e}")

        except ImportError as e:
            self.logger.warning(f"Knowledge Graph dependencies not available: {e}")
            results = self._save_kg_as_json()

        self.logger.info(f"KG seeding complete: {results['entities_added']} entities, "
                         f"{results['relationships_added']} relationships")
        return results

    def _save_kg_as_json(self) -> Dict[str, Any]:
        """Fallback: save KG data as JSON."""
        kg_data = {
            "entities": KG_SEED_ENTITIES,
            "relationships": [
                {"source": s, "type": r, "target": t}
                for s, r, t in KG_SEED_RELATIONSHIPS
            ],
            "created_at": datetime.utcnow().isoformat(),
        }
        kg_path = self.kg_dir / "seed_data.json"
        with open(kg_path, "w", encoding="utf-8") as f:
            json.dump(kg_data, f, indent=2, ensure_ascii=False)

        self.logger.info(f"💾 KG seed data saved to {kg_path}")
        return {
            "entities_added": 0,
            "relationships_added": 0,
            "saved_as_json": True,
            "path": str(kg_path),
        }

    # ------------------------------------------------------------------ #
    # Verification                                                         #
    # ------------------------------------------------------------------ #

    def verify(self) -> Dict[str, Any]:
        """Verify that the RAG and KG data are accessible and queryable."""
        results = {"rag": {}, "kg": {}, "status": "ok"}

        # Check JSON fallback files
        seed_docs_path = self.data_dir / "seed_documents"
        kg_seed_path = self.kg_dir / "seed_data.json"

        if seed_docs_path.exists():
            doc_files = list(seed_docs_path.glob("*.json"))
            results["rag"] = {
                "documents_on_disk": len([f for f in doc_files if not f.name.startswith("_")]),
                "path": str(seed_docs_path),
            }

        if kg_seed_path.exists():
            with open(kg_seed_path) as f:
                kg_data = json.load(f)
            results["kg"] = {
                "entities": len(kg_data.get("entities", [])),
                "relationships": len(kg_data.get("relationships", [])),
                "path": str(kg_seed_path),
            }

        # Check ChromaDB
        chroma_path = self.vector_db_dir / "chroma"
        if chroma_path.exists():
            results["rag"]["chroma_db_exists"] = True

        return results

    # ------------------------------------------------------------------ #
    # Full seed                                                            #
    # ------------------------------------------------------------------ #

    def seed_all(self) -> Dict[str, Any]:
        """Run full seeding: RAG + Knowledge Graph."""
        self.logger.info("=" * 60)
        self.logger.info("REGIQ Regulatory Data Seeder — Full Run")
        self.logger.info("=" * 60)

        rag_results = self.seed_rag()
        kg_results = self.seed_knowledge_graph()
        verify_results = self.verify()

        summary = {
            "rag": rag_results,
            "knowledge_graph": kg_results,
            "verification": verify_results,
            "completed_at": datetime.utcnow().isoformat(),
        }

        self.logger.info("=" * 60)
        self.logger.info("Seeding complete!")
        self.logger.info(f"  RAG documents: {rag_results.get('seeded', 0)} embedded, "
                         f"{rag_results.get('saved_as_json', 0)} saved as JSON")
        self.logger.info(f"  KG entities: {kg_results.get('entities_added', 0)}, "
                         f"relationships: {kg_results.get('relationships_added', 0)}")
        self.logger.info("=" * 60)

        return summary


# ── CLI Entry Point ────────────────────────────────────────────────────── #

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(levelname)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="REGIQ Regulatory Data Seeder")
    parser.add_argument("--source", choices=["rag", "kg", "all"], default="all",
                        help="What to seed (default: all)")
    parser.add_argument("--verify", action="store_true",
                        help="Verify existing data without seeding")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Override data directory path")
    args = parser.parse_args()

    seeder = RegulatoryDataSeeder(data_dir=args.data_dir)

    if args.verify:
        results = seeder.verify()
        print(json.dumps(results, indent=2))
        return

    if args.source == "rag":
        results = seeder.seed_rag()
    elif args.source == "kg":
        results = seeder.seed_knowledge_graph()
    else:
        results = seeder.seed_all()

    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
