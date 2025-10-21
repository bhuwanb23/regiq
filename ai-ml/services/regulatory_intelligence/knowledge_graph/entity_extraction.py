#!/usr/bin/env python3
"""
REGIQ AI/ML - Entity Relationship Extraction
Extracts regulatory entities, relationships, and builds knowledge graph structures.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
import re

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import spacy
    from spacy import displacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

from config.env_config import get_env_config


@dataclass
class RegulatoryEntity:
    """Represents a regulatory entity in the knowledge graph."""
    entity_id: str
    name: str
    entity_type: str  # REGULATION, ORGANIZATION, REQUIREMENT, PENALTY, DEADLINE, etc.
    jurisdiction: str
    description: str
    confidence: float
    metadata: Dict[str, Any]


@dataclass
class EntityRelationship:
    """Represents a relationship between entities."""
    relationship_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str  # IMPLEMENTS, VIOLATES, REQUIRES, PENALIZES, etc.
    confidence: float
    context: str
    metadata: Dict[str, Any]


@dataclass
class KnowledgeGraphConfig:
    """Configuration for knowledge graph operations."""
    # Entity extraction settings
    min_confidence: float = 0.7
    max_entities_per_doc: int = 100
    
    # Relationship extraction settings
    relationship_patterns: List[str] = None
    max_relationships_per_doc: int = 50
    
    # Graph database settings
    graph_db_path: str = "data/knowledge_graph/regulatory_kg.json"
    backup_path: str = "data/knowledge_graph/backup/"
    
    def __post_init__(self):
        if self.relationship_patterns is None:
            self.relationship_patterns = [
                r"requires?\s+",
                r"implements?\s+",
                r"violates?\s+",
                r"penalizes?\s+",
                r"governs?\s+",
                r"regulates?\s+",
                r"applies?\s+to",
                r"affects?\s+",
                r"relates?\s+to",
                r"depends?\s+on"
            ]


class EntityExtractor:
    """Extracts regulatory entities from text using NLP techniques."""
    
    def __init__(self, config: Optional[KnowledgeGraphConfig] = None):
        self.config = config or KnowledgeGraphConfig()
        self.logger = self._setup_logger()
        self.nlp = self._load_spacy_model()
        self.entity_counter = 0
        self.relationship_counter = 0
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("entity_extractor")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def _load_spacy_model(self):
        """Load spaCy model for NLP processing."""
        if not SPACY_AVAILABLE:
            self.logger.warning("spaCy not available")
            return None
        
        try:
            # Try to load English model
            nlp = spacy.load("en_core_web_sm")
            self.logger.info("Loaded spaCy English model")
            return nlp
        except OSError:
            self.logger.warning("spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
            return None
    
    def extract_entities(self, text: str, document_id: str = None) -> List[RegulatoryEntity]:
        """Extract regulatory entities from text."""
        entities = []
        
        if not self.nlp:
            self.logger.warning("spaCy model not available, using basic extraction")
            return self._basic_entity_extraction(text, document_id)
        
        try:
            doc = self.nlp(text)
            
            # Extract named entities
            for ent in doc.ents:
                if ent.label_ in ["ORG", "PERSON", "GPE", "LAW", "EVENT"]:
                    entity = self._create_entity_from_spacy(ent, document_id)
                    if entity and entity.confidence >= self.config.min_confidence:
                        entities.append(entity)
            
            # Extract custom regulatory entities
            custom_entities = self._extract_custom_regulatory_entities(text, document_id)
            entities.extend(custom_entities)
            
            # Limit entities per document
            entities = entities[:self.config.max_entities_per_doc]
            
            self.logger.info(f"Extracted {len(entities)} entities from document")
            return entities
            
        except Exception as e:
            self.logger.error(f"Error extracting entities: {e}")
            return []
    
    def _create_entity_from_spacy(self, ent, document_id: str = None) -> Optional[RegulatoryEntity]:
        """Create RegulatoryEntity from spaCy entity."""
        try:
            entity_type = self._map_spacy_label_to_entity_type(ent.label_)
            jurisdiction = self._extract_jurisdiction_from_entity(ent.text)
            
            self.entity_counter += 1
            return RegulatoryEntity(
                entity_id=f"entity_{self.entity_counter}_{document_id or 'unknown'}",
                name=ent.text.strip(),
                entity_type=entity_type,
                jurisdiction=jurisdiction,
                description=f"Extracted from {ent.label_}",
                confidence=0.8,  # Default confidence for spaCy entities
                metadata={
                    "spacy_label": ent.label_,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char,
                    "document_id": document_id
                }
            )
        except Exception as e:
            self.logger.error(f"Error creating entity from spaCy: {e}")
            return None
    
    def _map_spacy_label_to_entity_type(self, spacy_label: str) -> str:
        """Map spaCy labels to regulatory entity types."""
        mapping = {
            "ORG": "ORGANIZATION",
            "PERSON": "PERSON",
            "GPE": "JURISDICTION",
            "LAW": "REGULATION",
            "EVENT": "EVENT"
        }
        return mapping.get(spacy_label, "UNKNOWN")
    
    def _extract_jurisdiction_from_entity(self, text: str) -> str:
        """Extract jurisdiction from entity text."""
        jurisdiction_keywords = {
            "US": ["United States", "USA", "US", "America"],
            "EU": ["European Union", "EU", "Europe"],
            "UK": ["United Kingdom", "UK", "Britain"],
            "India": ["India", "Indian", "RBI"],
            "Singapore": ["Singapore", "MAS"],
            "Canada": ["Canada", "Canadian"]
        }
        
        text_lower = text.lower()
        for jurisdiction, keywords in jurisdiction_keywords.items():
            if any(keyword.lower() in text_lower for keyword in keywords):
                return jurisdiction
        
        return "UNKNOWN"
    
    def _extract_custom_regulatory_entities(self, text: str, document_id: str = None) -> List[RegulatoryEntity]:
        """Extract custom regulatory entities using pattern matching."""
        entities = []
        
        # Regulation patterns
        regulation_patterns = [
            r"(?:EU AI Act|GDPR|SOX|Basel III|MiFID II|PCI DSS)",
            r"(?:Article \d+|Section \d+|Clause \d+)",
            r"(?:Regulation|Directive|Guideline|Standard)\s+\d+",
        ]
        
        for pattern in regulation_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                self.entity_counter += 1
                entity = RegulatoryEntity(
                    entity_id=f"entity_{self.entity_counter}_{document_id or 'unknown'}",
                    name=match.group().strip(),
                    entity_type="REGULATION",
                    jurisdiction="UNKNOWN",
                    description="Regulatory reference",
                    confidence=0.9,
                    metadata={
                        "pattern": pattern,
                        "start_char": match.start(),
                        "end_char": match.end(),
                        "document_id": document_id
                    }
                )
                entities.append(entity)
        
        # Penalty patterns
        penalty_patterns = [
            r"(?:fine|penalty|sanction)\s+of\s+\$?[\d,]+",
            r"(?:up to|maximum)\s+\$?[\d,]+",
        ]
        
        for pattern in penalty_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                self.entity_counter += 1
                entity = RegulatoryEntity(
                    entity_id=f"entity_{self.entity_counter}_{document_id or 'unknown'}",
                    name=match.group().strip(),
                    entity_type="PENALTY",
                    jurisdiction="UNKNOWN",
                    description="Penalty amount",
                    confidence=0.8,
                    metadata={
                        "pattern": pattern,
                        "start_char": match.start(),
                        "end_char": match.end(),
                        "document_id": document_id
                    }
                )
                entities.append(entity)
        
        return entities
    
    def _basic_entity_extraction(self, text: str, document_id: str = None) -> List[RegulatoryEntity]:
        """Basic entity extraction without spaCy."""
        entities = []
        
        # Simple keyword-based extraction
        regulatory_keywords = [
            "SEC", "FCA", "RBI", "MAS", "FINMA", "ASIC",
            "GDPR", "SOX", "Basel III", "MiFID II",
            "compliance", "regulation", "requirement"
        ]
        
        for keyword in regulatory_keywords:
            if keyword.lower() in text.lower():
                self.entity_counter += 1
                entity = RegulatoryEntity(
                    entity_id=f"entity_{self.entity_counter}_{document_id or 'unknown'}",
                    name=keyword,
                    entity_type="ORGANIZATION" if keyword in ["SEC", "FCA", "RBI", "MAS"] else "REGULATION",
                    jurisdiction="UNKNOWN",
                    description="Keyword-based extraction",
                    confidence=0.6,
                    metadata={
                        "extraction_method": "keyword",
                        "document_id": document_id
                    }
                )
                entities.append(entity)
        
        return entities
    
    def extract_relationships(self, text: str, entities: List[RegulatoryEntity], 
                           document_id: str = None) -> List[EntityRelationship]:
        """Extract relationships between entities."""
        relationships = []
        
        if not entities:
            return relationships
        
        try:
            # Find relationships using pattern matching
            for pattern in self.config.relationship_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Find nearby entities
                    start_pos = max(0, match.start() - 100)
                    end_pos = min(len(text), match.end() + 100)
                    context = text[start_pos:end_pos]
                    
                    # Find entities in context
                    context_entities = [e for e in entities 
                                      if e.metadata.get("start_char", 0) >= start_pos 
                                      and e.metadata.get("end_char", 0) <= end_pos]
                    
                    if len(context_entities) >= 2:
                        # Create relationship between first two entities
                        source = context_entities[0]
                        target = context_entities[1]
                        
                        self.relationship_counter += 1
                        relationship = EntityRelationship(
                            relationship_id=f"rel_{self.relationship_counter}_{document_id or 'unknown'}",
                            source_entity_id=source.entity_id,
                            target_entity_id=target.entity_id,
                            relationship_type=self._extract_relationship_type(pattern),
                            confidence=0.7,
                            context=context,
                            metadata={
                                "pattern": pattern,
                                "match_start": match.start(),
                                "match_end": match.end(),
                                "document_id": document_id
                            }
                        )
                        relationships.append(relationship)
            
            # Limit relationships per document
            relationships = relationships[:self.config.max_relationships_per_doc]
            
            self.logger.info(f"Extracted {len(relationships)} relationships")
            return relationships
            
        except Exception as e:
            self.logger.error(f"Error extracting relationships: {e}")
            return []
    
    def _extract_relationship_type(self, pattern: str) -> str:
        """Extract relationship type from pattern."""
        if "requires" in pattern:
            return "REQUIRES"
        elif "implements" in pattern:
            return "IMPLEMENTS"
        elif "violates" in pattern:
            return "VIOLATES"
        elif "penalizes" in pattern:
            return "PENALIZES"
        elif "governs" in pattern or "regulates" in pattern:
            return "GOVERNS"
        elif "applies" in pattern:
            return "APPLIES_TO"
        elif "affects" in pattern:
            return "AFFECTS"
        elif "relates" in pattern:
            return "RELATES_TO"
        elif "depends" in pattern:
            return "DEPENDS_ON"
        else:
            return "RELATED_TO"
    
    def process_document(self, text: str, document_id: str = None) -> Tuple[List[RegulatoryEntity], List[EntityRelationship]]:
        """Process a document to extract entities and relationships."""
        try:
            # Extract entities
            entities = self.extract_entities(text, document_id)
            
            # Extract relationships
            relationships = self.extract_relationships(text, entities, document_id)
            
            self.logger.info(f"Processed document {document_id}: {len(entities)} entities, {len(relationships)} relationships")
            return entities, relationships
            
        except Exception as e:
            self.logger.error(f"Error processing document: {e}")
            return [], []


def main():
    """Test the entity extraction functionality."""
    print("🧪 Testing Entity Extraction")
    
    # Test configuration
    config = KnowledgeGraphConfig()
    extractor = EntityExtractor(config)
    
    # Test text
    test_text = """
    The SEC requires enhanced disclosures for AI models. The EU AI Act Article 13 mandates 
    transparency requirements. Non-compliance may result in penalties up to $50,000.
    """
    
    # Extract entities and relationships
    entities, relationships = extractor.process_document(test_text, "test_doc_001")
    
    print(f"✅ Extracted {len(entities)} entities:")
    for entity in entities:
        print(f"  - {entity.name} ({entity.entity_type}) - {entity.confidence}")
    
    print(f"✅ Extracted {len(relationships)} relationships:")
    for rel in relationships:
        print(f"  - {rel.source_entity_id} -> {rel.target_entity_id} ({rel.relationship_type})")


if __name__ == "__main__":
    main()
