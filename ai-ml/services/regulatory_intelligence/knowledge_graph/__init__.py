#!/usr/bin/env python3
"""
REGIQ AI/ML - Knowledge Graph Module
Regulatory entity extraction, compliance mapping, and graph database management.

Provides:
    - EntityExtractor: NLP-based regulatory entity and relationship extraction
    - ComplianceMapper: Maps regulations to compliance requirements and pathways
    - GraphDatabaseManager: NetworkX + Neo4j graph storage and querying
    - GraphQueryEngine: Compliance path traversal and relationship queries

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .entity_extraction import (
    EntityExtractor,
    RegulatoryEntity,
    EntityRelationship,
    KnowledgeGraphConfig,
)
from .compliance_mapping import (
    ComplianceMapper,
    ComplianceRequirement,
    CompliancePathway,
    RecommendationRule,
)
from .graph_database import (
    GraphDatabaseManager,
    GraphQueryEngine,
)

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    # Entity Extraction
    "EntityExtractor",
    "RegulatoryEntity",
    "EntityRelationship",
    "KnowledgeGraphConfig",
    # Compliance Mapping
    "ComplianceMapper",
    "ComplianceRequirement",
    "CompliancePathway",
    "RecommendationRule",
    # Graph Database
    "GraphDatabaseManager",
    "GraphQueryEngine",
]
