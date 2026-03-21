#!/usr/bin/env python3
"""
REGIQ AI/ML - Terminology Manager
Domain-specific terminology management for financial compliance reports.

This module provides:
- Regulatory and AI/ML term definitions
- Audience-specific language adaptation (executive, technical, regulatory)
- Abbreviation and acronym expansion
- Glossary generation for reports
- Term standardization across report sections

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class Term:
    """A domain term with context-aware definitions."""
    term: str
    abbreviation: Optional[str]
    executive_definition: str
    technical_definition: str
    regulatory_definition: str
    category: str  # fairness, risk, regulatory, general
    related_terms: List[str]

    def get_definition(self, audience: str = "technical") -> str:
        """Return definition appropriate for the given audience."""
        mapping = {
            "executive": self.executive_definition,
            "technical": self.technical_definition,
            "regulatory": self.regulatory_definition,
        }
        return mapping.get(audience, self.technical_definition)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TerminologyManager:
    """
    Manages domain-specific terminology for REGIQ compliance reports.

    Provides audience-aware definitions, glossary generation,
    and term standardization for all four services' outputs.
    """

    # ------------------------------------------------------------------ #
    # Master term registry                                                 #
    # ------------------------------------------------------------------ #
    TERMS: Dict[str, Term] = {
        # ── Fairness / Bias ──────────────────────────────────────────── #
        "demographic_parity": Term(
            term="Demographic Parity",
            abbreviation="DP",
            executive_definition=(
                "A fairness standard ensuring the AI model approves or rejects "
                "applications at similar rates across different customer groups "
                "(e.g., age, gender, ethnicity)."
            ),
            technical_definition=(
                "A fairness criterion requiring P(Ŷ=1|A=0) ≈ P(Ŷ=1|A=1), where "
                "Ŷ is the predicted outcome and A is the protected attribute. "
                "Measured as the ratio of positive prediction rates between groups."
            ),
            regulatory_definition=(
                "Demographic Parity (DP) is a fairness metric mandated under EU AI "
                "Act Article 10 and ECOA guidelines, verifying that protected-class "
                "membership does not disproportionately influence model outcomes."
            ),
            category="fairness",
            related_terms=["equalized_odds", "disparate_impact", "individual_fairness"],
        ),
        "equalized_odds": Term(
            term="Equalized Odds",
            abbreviation="EO",
            executive_definition=(
                "A fairness measure ensuring the model makes equally accurate "
                "predictions for all customer groups — catching both approvals "
                "and rejections at similar rates regardless of demographics."
            ),
            technical_definition=(
                "A fairness criterion requiring equal true positive rates and false "
                "positive rates across protected groups: "
                "P(Ŷ=1|Y=y,A=0) = P(Ŷ=1|Y=y,A=1) for y ∈ {0,1}."
            ),
            regulatory_definition=(
                "Equalized Odds is a fairness standard referenced in NIST AI RMF "
                "and EU AI Act Annex IV, requiring that error rates are balanced "
                "across demographic groups to prevent discriminatory outcomes."
            ),
            category="fairness",
            related_terms=["demographic_parity", "calibration", "false_positive_rate"],
        ),
        "disparate_impact": Term(
            term="Disparate Impact",
            abbreviation="DI",
            executive_definition=(
                "A legal and ethical measure that flags when one customer group "
                "is approved or denied at a significantly lower rate than another, "
                "even without intentional discrimination."
            ),
            technical_definition=(
                "The ratio of positive outcome rates between the unprivileged and "
                "privileged groups: DI = P(Ŷ=1|A=unprivileged) / P(Ŷ=1|A=privileged). "
                "Values below 0.8 indicate potential adverse impact (80% rule)."
            ),
            regulatory_definition=(
                "Disparate Impact (DI) is a legal doctrine under Title VII and the "
                "Equal Credit Opportunity Act (ECOA). A DI ratio below 0.8 triggers "
                "mandatory review under CFPB and FFIEC guidelines."
            ),
            category="fairness",
            related_terms=["demographic_parity", "adverse_impact", "80_percent_rule"],
        ),
        "calibration": Term(
            term="Calibration",
            abbreviation=None,
            executive_definition=(
                "How accurately the model's confidence scores reflect real-world "
                "outcomes — if the model says 70% approval likelihood, "
                "roughly 70% of those applicants should actually be approved."
            ),
            technical_definition=(
                "A model property where predicted probabilities match empirical "
                "outcome frequencies: P(Y=1|f(X)=p) ≈ p. Measured via calibration "
                "curves, Expected Calibration Error (ECE), and reliability diagrams."
            ),
            regulatory_definition=(
                "Model calibration is required under SR 11-7 (Model Risk Management) "
                "and BCBS 239. Miscalibrated models may produce systematically biased "
                "risk scores, violating fair lending and model governance standards."
            ),
            category="fairness",
            related_terms=["equalized_odds", "reliability", "expected_calibration_error"],
        ),
        # ── Explainability ───────────────────────────────────────────── #
        "shap": Term(
            term="SHAP Values",
            abbreviation="SHAP",
            executive_definition=(
                "A technique that explains why the AI made a specific decision "
                "by showing how much each data point (e.g., credit score, income) "
                "contributed to the final outcome."
            ),
            technical_definition=(
                "SHapley Additive exPlanations (SHAP) assign each feature an "
                "importance value based on cooperative game theory. The SHAP value "
                "φᵢ for feature i is the weighted average of marginal contributions "
                "across all feature subsets."
            ),
            regulatory_definition=(
                "SHAP-based explanations fulfil the 'right to explanation' under "
                "GDPR Article 22, EU AI Act Article 13, and SR 11-7 model "
                "documentation requirements for high-risk automated decisions."
            ),
            category="explainability",
            related_terms=["lime", "feature_importance", "model_explainability"],
        ),
        "lime": Term(
            term="LIME",
            abbreviation="LIME",
            executive_definition=(
                "A technique that creates simple, human-readable explanations "
                "for individual AI decisions by testing slightly varied inputs "
                "and observing how predictions change."
            ),
            technical_definition=(
                "Local Interpretable Model-agnostic Explanations (LIME) approximate "
                "a complex model locally with an interpretable surrogate: "
                "ξ(x) = argmin L(f, g, πₓ) + Ω(g), where g is a linear model "
                "and πₓ is a locality kernel."
            ),
            regulatory_definition=(
                "LIME-generated explanations support compliance with GDPR Article 22 "
                "and EBA Guidelines on Internal Governance, providing local "
                "decision-level transparency for individual applicant outcomes."
            ),
            category="explainability",
            related_terms=["shap", "feature_importance", "surrogate_model"],
        ),
        # ── Risk ─────────────────────────────────────────────────────── #
        "monte_carlo": Term(
            term="Monte Carlo Simulation",
            abbreviation="MCS",
            executive_definition=(
                "A computational method that runs thousands of 'what-if' scenarios "
                "to estimate the likelihood and financial impact of different "
                "compliance risk outcomes."
            ),
            technical_definition=(
                "A stochastic simulation technique using repeated random sampling "
                "to approximate probability distributions of model outputs. "
                "REGIQ implements Latin Hypercube Sampling (LHS) and Sobol "
                "quasi-random sequences for variance reduction."
            ),
            regulatory_definition=(
                "Monte Carlo methods are recognised stress-testing tools under "
                "BCBS 239, EBA stress-testing guidelines, and the Fed's CCAR "
                "framework for estimating tail risk and capital adequacy."
            ),
            category="risk",
            related_terms=["bayesian_inference", "stress_testing", "var"],
        ),
        "bayesian_inference": Term(
            term="Bayesian Inference",
            abbreviation=None,
            executive_definition=(
                "A statistical approach that continuously updates compliance risk "
                "estimates as new data arrives, providing probability-based "
                "predictions rather than single-point estimates."
            ),
            technical_definition=(
                "A probabilistic framework applying Bayes' theorem: "
                "P(θ|X) ∝ P(X|θ)P(θ). REGIQ uses MCMC with NUTS sampler "
                "(via PyMC5) for posterior inference over compliance risk parameters."
            ),
            regulatory_definition=(
                "Bayesian models are accepted by BCBS for internal model validation "
                "and align with EBA's model uncertainty quantification requirements, "
                "providing credible intervals for risk probability estimates."
            ),
            category="risk",
            related_terms=["monte_carlo", "mcmc", "posterior_distribution"],
        ),
        "value_at_risk": Term(
            term="Value at Risk",
            abbreviation="VaR",
            executive_definition=(
                "The maximum potential financial loss from a compliance violation "
                "over a specified period, stated with a given level of confidence "
                "(e.g., 95% confidence that losses won't exceed $X)."
            ),
            technical_definition=(
                "VaR at confidence level α is defined as the α-quantile of the "
                "loss distribution: VaR_α = inf{l : P(L > l) ≤ 1-α}. "
                "REGIQ computes parametric, historical, and Monte Carlo VaR."
            ),
            regulatory_definition=(
                "VaR is a mandatory risk metric under Basel III/IV (FRTB), "
                "BCBS 239, and MiFID II. Regulatory VaR is typically computed "
                "at 99% confidence over a 10-day holding period."
            ),
            category="risk",
            related_terms=["monte_carlo", "expected_shortfall", "stress_testing"],
        ),
        # ── Regulatory ───────────────────────────────────────────────── #
        "gdpr": Term(
            term="General Data Protection Regulation",
            abbreviation="GDPR",
            executive_definition=(
                "The EU's data privacy law that gives individuals control over their "
                "personal data and requires organisations to process data lawfully, "
                "transparently, and securely."
            ),
            technical_definition=(
                "EU Regulation 2016/679 establishing data processing requirements "
                "including lawful basis (Art. 6), data subject rights (Art. 15-22), "
                "automated decision-making restrictions (Art. 22), and DPO obligations."
            ),
            regulatory_definition=(
                "GDPR (EU) 2016/679 mandates explainability for automated decisions "
                "(Article 22), data minimisation (Article 5), purpose limitation, "
                "and breach notification within 72 hours. Non-compliance risks fines "
                "up to €20M or 4% of global annual turnover."
            ),
            category="regulatory",
            related_terms=["eu_ai_act", "ccpa", "data_privacy", "right_to_explanation"],
        ),
        "eu_ai_act": Term(
            term="EU AI Act",
            abbreviation="EU AIA",
            executive_definition=(
                "The EU's landmark law regulating artificial intelligence, "
                "classifying AI systems by risk level and imposing stricter "
                "requirements on high-risk applications like credit scoring."
            ),
            technical_definition=(
                "EU Regulation 2024/1689 categorising AI systems as unacceptable "
                "risk (prohibited), high-risk (Annex III — including credit scoring "
                "and employment), limited risk, and minimal risk. High-risk systems "
                "require conformity assessments, logging, and human oversight."
            ),
            regulatory_definition=(
                "The EU AI Act (2024/1689) mandates risk management systems (Art. 9), "
                "data governance (Art. 10), technical documentation (Art. 11), "
                "transparency (Art. 13), and human oversight (Art. 14) for "
                "high-risk AI systems including financial credit models."
            ),
            category="regulatory",
            related_terms=["gdpr", "ecoa", "model_risk_management"],
        ),
        "ecoa": Term(
            term="Equal Credit Opportunity Act",
            abbreviation="ECOA",
            executive_definition=(
                "A US federal law prohibiting credit discrimination based on race, "
                "colour, religion, national origin, sex, marital status, age, "
                "or receipt of public assistance."
            ),
            technical_definition=(
                "15 U.S.C. § 1691 et seq., implemented by Regulation B (12 CFR 202). "
                "Requires creditors to provide adverse action notices with specific "
                "reasons, prohibits use of protected characteristics in credit models, "
                "and mandates data collection for fair lending analysis."
            ),
            regulatory_definition=(
                "ECOA (15 U.S.C. § 1691) and Regulation B require creditors to "
                "provide adverse action notices within 30 days, prohibit proxy "
                "discrimination via correlated variables, and mandate HMDA data "
                "collection. CFPB enforces ECOA with penalties up to $10,000/violation."
            ),
            category="regulatory",
            related_terms=["disparate_impact", "fair_lending", "adverse_action", "cfpb"],
        ),
        # ── General AI/ML ─────────────────────────────────────────────── #
        "model_drift": Term(
            term="Model Drift",
            abbreviation=None,
            executive_definition=(
                "When an AI model's accuracy or fairness gradually degrades over "
                "time because real-world patterns change, requiring the model "
                "to be retrained or updated."
            ),
            technical_definition=(
                "Degradation of model performance due to covariate shift "
                "(P(X) changes), concept drift (P(Y|X) changes), or label drift. "
                "Detected via PSI (Population Stability Index), KS tests, "
                "and performance monitoring dashboards."
            ),
            regulatory_definition=(
                "Model drift monitoring is required under SR 11-7 Model Risk "
                "Management guidance, requiring ongoing performance monitoring, "
                "periodic model validation, and drift-triggered re-validation "
                "for models used in regulated financial decisions."
            ),
            category="general",
            related_terms=["model_validation", "psi", "performance_monitoring"],
        ),
        "rag": Term(
            term="Retrieval-Augmented Generation",
            abbreviation="RAG",
            executive_definition=(
                "A technique that enhances AI responses by first searching a "
                "knowledge base of regulatory documents, then using that context "
                "to generate accurate, citation-backed compliance answers."
            ),
            technical_definition=(
                "A hybrid architecture combining dense retrieval (via vector "
                "embeddings in ChromaDB/FAISS) with generative LLMs. Given query q, "
                "retrieves top-k documents D* = argmax sim(q,d) and conditions "
                "generation on the retrieved context: P(answer|q, D*)."
            ),
            regulatory_definition=(
                "RAG-based systems maintain traceable citations to source regulatory "
                "documents, supporting audit trail requirements under SR 11-7 and "
                "providing evidence-based compliance assessments with source attribution."
            ),
            category="general",
            related_terms=["vector_database", "embeddings", "llm", "knowledge_graph"],
        ),
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"TerminologyManager initialised with {len(self.TERMS)} terms")

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def get_definition(self, term_key: str, audience: str = "technical") -> Optional[str]:
        """
        Return the audience-appropriate definition for a term.

        Args:
            term_key: Snake_case term key (e.g. 'demographic_parity').
            audience: One of 'executive', 'technical', 'regulatory'.

        Returns:
            Definition string, or None if term not found.
        """
        term = self.TERMS.get(term_key)
        if not term:
            self.logger.warning(f"Term not found: {term_key}")
            return None
        return term.get_definition(audience)

    def get_term(self, term_key: str) -> Optional[Term]:
        """Return the full Term object."""
        return self.TERMS.get(term_key)

    def get_abbreviation(self, term_key: str) -> Optional[str]:
        """Return the abbreviation for a term, if any."""
        term = self.TERMS.get(term_key)
        return term.abbreviation if term else None

    def expand_abbreviation(self, abbreviation: str) -> Optional[str]:
        """Find the full term name for a given abbreviation."""
        abbr_upper = abbreviation.upper()
        for term in self.TERMS.values():
            if term.abbreviation and term.abbreviation.upper() == abbr_upper:
                return term.term
        return None

    def get_terms_by_category(self, category: str) -> List[Term]:
        """
        Return all terms in a given category.

        Categories: 'fairness', 'explainability', 'risk', 'regulatory', 'general'
        """
        return [t for t in self.TERMS.values() if t.category == category]

    def get_related_terms(self, term_key: str) -> List[str]:
        """Return list of related term keys for a given term."""
        term = self.TERMS.get(term_key)
        return term.related_terms if term else []

    def generate_glossary(
        self,
        term_keys: Optional[List[str]] = None,
        audience: str = "technical",
        categories: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate a glossary list for inclusion in a report.

        Args:
            term_keys:  Specific keys to include. If None, uses categories or all terms.
            audience:   Definition style — 'executive', 'technical', or 'regulatory'.
            categories: Filter by one or more categories if term_keys is None.

        Returns:
            List of dicts with 'term', 'abbreviation', 'definition', 'category'.
        """
        if term_keys:
            terms = [self.TERMS[k] for k in term_keys if k in self.TERMS]
        elif categories:
            terms = [t for t in self.TERMS.values() if t.category in categories]
        else:
            terms = list(self.TERMS.values())

        glossary = []
        for t in sorted(terms, key=lambda x: x.term):
            entry: Dict[str, Any] = {
                "term": t.term,
                "abbreviation": t.abbreviation,
                "definition": t.get_definition(audience),
                "category": t.category,
            }
            glossary.append(entry)

        self.logger.info(f"Generated glossary with {len(glossary)} entries for audience={audience}")
        return glossary

    def generate_glossary_html(
        self,
        term_keys: Optional[List[str]] = None,
        audience: str = "technical",
        categories: Optional[List[str]] = None,
    ) -> str:
        """
        Render the glossary as an HTML section suitable for embedding in reports.
        """
        glossary = self.generate_glossary(term_keys, audience, categories)
        if not glossary:
            return "<p>No glossary terms available.</p>"

        html_parts = ["<section class='regiq-glossary'>",
                      "<h2>Glossary of Terms</h2>",
                      "<dl class='regiq-glossary-list'>"]

        for entry in glossary:
            abbr_text = f" ({entry['abbreviation']})" if entry["abbreviation"] else ""
            html_parts.append(
                f"  <dt><strong>{entry['term']}{abbr_text}</strong></dt>"
            )
            html_parts.append(
                f"  <dd>{entry['definition']}</dd>"
            )

        html_parts += ["</dl>", "</section>"]
        return "\n".join(html_parts)

    def standardize_term(self, raw_term: str) -> str:
        """
        Convert a raw term string to its canonical form.
        Handles common aliases and abbreviations.
        """
        normalised = raw_term.strip().lower().replace(" ", "_").replace("-", "_")

        # Direct key match
        if normalised in self.TERMS:
            return self.TERMS[normalised].term

        # Abbreviation match
        expanded = self.expand_abbreviation(raw_term)
        if expanded:
            return expanded

        # Partial match
        for key, term in self.TERMS.items():
            if normalised in key or key in normalised:
                return term.term

        return raw_term  # Return as-is if no match found

    def adapt_for_audience(self, text: str, source_audience: str, target_audience: str) -> str:
        """
        Replace technical jargon in text with audience-appropriate terminology.

        Scans text for known abbreviations and replaces them with
        the target-audience-appropriate full terms on first occurrence.
        """
        if source_audience == target_audience:
            return text

        adapted = text
        first_seen = set()

        for term in self.TERMS.values():
            if not term.abbreviation:
                continue
            abbr = term.abbreviation
            if abbr in adapted and abbr not in first_seen:
                first_seen.add(abbr)
                definition = term.get_definition(target_audience)
                # Replace first occurrence with "ABBR (full definition)" pattern
                adapted = adapted.replace(
                    abbr,
                    f"{term.term} ({abbr})",
                    1,  # only first occurrence
                )

        return adapted

    def list_all_terms(self) -> List[Dict[str, Any]]:
        """Return a summary list of all registered terms."""
        return [
            {
                "key": key,
                "term": t.term,
                "abbreviation": t.abbreviation,
                "category": t.category,
            }
            for key, t in sorted(self.TERMS.items())
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Return statistics about the terminology registry."""
        categories: Dict[str, int] = {}
        for t in self.TERMS.values():
            categories[t.category] = categories.get(t.category, 0) + 1

        return {
            "total_terms": len(self.TERMS),
            "terms_with_abbreviations": sum(
                1 for t in self.TERMS.values() if t.abbreviation
            ),
            "terms_by_category": categories,
        }

    def __repr__(self) -> str:
        return f"TerminologyManager({len(self.TERMS)} terms)"
