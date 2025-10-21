#!/usr/bin/env python3
"""
REGIQ AI/ML - Compliance Mapping
Maps regulations to requirements, links related regulations, and creates compliance pathways.
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

from services.regulatory_intelligence.knowledge_graph.entity_extraction import (
    RegulatoryEntity, EntityRelationship, KnowledgeGraphConfig
)
from services.regulatory_intelligence.knowledge_graph.graph_database import (
    GraphDatabaseManager, GraphQueryEngine
)
from services.regulatory_intelligence.llm.gemini_client import GeminiClient, GeminiClientConfig


@dataclass
class ComplianceRequirement:
    """Represents a compliance requirement."""
    requirement_id: str
    title: str
    description: str
    regulation_id: str
    jurisdiction: str
    compliance_level: str  # HIGH, MEDIUM, LOW
    deadline: Optional[str] = None
    penalty_amount: Optional[str] = None
    affected_systems: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.affected_systems is None:
            self.affected_systems = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CompliancePathway:
    """Represents a compliance pathway between regulations."""
    pathway_id: str
    source_regulation: str
    target_regulation: str
    pathway_type: str  # IMPLEMENTATION, DEPENDENCY, CONFLICT, SUPPLEMENT
    steps: List[str]
    estimated_effort: str  # LOW, MEDIUM, HIGH
    timeline: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RecommendationRule:
    """Represents a recommendation rule for compliance."""
    rule_id: str
    name: str
    description: str
    conditions: List[str]
    recommendations: List[str]
    priority: str  # HIGH, MEDIUM, LOW
    applicable_jurisdictions: List[str]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ComplianceMapper:
    """Maps regulations to requirements and creates compliance pathways."""
    
    def __init__(self, graph_manager: GraphDatabaseManager, 
                 config: Optional[KnowledgeGraphConfig] = None):
        self.graph_manager = graph_manager
        self.config = config or KnowledgeGraphConfig()
        self.logger = self._setup_logger()
        self.query_engine = GraphQueryEngine(graph_manager)
        self.gemini_client = GeminiClient(GeminiClientConfig())
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("compliance_mapper")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def map_regulation_to_requirements(self, regulation_id: str) -> List[ComplianceRequirement]:
        """Map a regulation to its compliance requirements."""
        try:
            # Get regulation entity
            regulation = self.graph_manager.get_entity(regulation_id)
            if not regulation:
                self.logger.warning(f"Regulation {regulation_id} not found")
                return []
            
            # Find related entities
            relationships = self.graph_manager.get_relationships(regulation_id)
            
            requirements = []
            for rel in relationships:
                if rel.get("relationship_type") in ["REQUIRES", "MANDATES", "GOVERNS"]:
                    target_entity = self.graph_manager.get_entity(rel["target"])
                    if target_entity and target_entity.get("entity_type") == "REQUIREMENT":
                        requirement = self._create_compliance_requirement(
                            target_entity, regulation, rel
                        )
                        requirements.append(requirement)
            
            # Use LLM to generate additional requirements if needed
            if not requirements:
                llm_requirements = self._generate_requirements_with_llm(regulation)
                requirements.extend(llm_requirements)
            
            self.logger.info(f"Mapped {len(requirements)} requirements for regulation {regulation_id}")
            return requirements
            
        except Exception as e:
            self.logger.error(f"Error mapping regulation to requirements: {e}")
            return []
    
    def _create_compliance_requirement(self, entity: Dict[str, Any], 
                                     regulation: Dict[str, Any], 
                                     relationship: Dict[str, Any]) -> ComplianceRequirement:
        """Create a compliance requirement from entity data."""
        return ComplianceRequirement(
            requirement_id=f"req_{entity['entity_id']}",
            title=entity.get("name", "Unknown Requirement"),
            description=entity.get("description", ""),
            regulation_id=regulation["entity_id"],
            jurisdiction=entity.get("jurisdiction", "UNKNOWN"),
            compliance_level=self._determine_compliance_level(entity),
            deadline=self._extract_deadline(entity),
            penalty_amount=self._extract_penalty(entity),
            affected_systems=self._extract_affected_systems(entity),
            metadata={
                "source_entity": entity,
                "relationship": relationship,
                "regulation": regulation
            }
        )
    
    def _determine_compliance_level(self, entity: Dict[str, Any]) -> str:
        """Determine compliance level based on entity data."""
        description = entity.get("description", "").lower()
        name = entity.get("name", "").lower()
        
        high_keywords = ["mandatory", "required", "must", "shall", "critical"]
        medium_keywords = ["should", "recommended", "advisory"]
        
        if any(keyword in description or keyword in name for keyword in high_keywords):
            return "HIGH"
        elif any(keyword in description or keyword in name for keyword in medium_keywords):
            return "MEDIUM"
        else:
            return "LOW"
    
    def _extract_deadline(self, entity: Dict[str, Any]) -> Optional[str]:
        """Extract deadline from entity data."""
        description = entity.get("description", "")
        deadline_patterns = [
            r"by\s+(\d{4}-\d{2}-\d{2})",
            r"deadline\s+(\d{4}-\d{2}-\d{2})",
            r"before\s+(\d{4}-\d{2}-\d{2})",
            r"until\s+(\d{4}-\d{2}-\d{2})"
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_penalty(self, entity: Dict[str, Any]) -> Optional[str]:
        """Extract penalty amount from entity data."""
        description = entity.get("description", "")
        penalty_patterns = [
            r"penalty\s+of\s+\$?[\d,]+",
            r"fine\s+of\s+\$?[\d,]+",
            r"up\s+to\s+\$?[\d,]+"
        ]
        
        for pattern in penalty_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_affected_systems(self, entity: Dict[str, Any]) -> List[str]:
        """Extract affected systems from entity data."""
        description = entity.get("description", "").lower()
        systems = []
        
        system_keywords = {
            "ai_models": ["ai", "artificial intelligence", "machine learning", "model"],
            "data_processing": ["data", "processing", "storage", "privacy"],
            "reporting": ["report", "disclosure", "transparency"],
            "governance": ["governance", "oversight", "management"],
            "security": ["security", "cybersecurity", "protection"]
        }
        
        for system, keywords in system_keywords.items():
            if any(keyword in description for keyword in keywords):
                systems.append(system)
        
        return systems
    
    def _generate_requirements_with_llm(self, regulation: Dict[str, Any]) -> List[ComplianceRequirement]:
        """Generate compliance requirements using LLM."""
        try:
            prompt = f"""
            Analyze this regulation and generate compliance requirements:
            
            Regulation: {regulation.get('name', '')}
            Description: {regulation.get('description', '')}
            Jurisdiction: {regulation.get('jurisdiction', '')}
            
            Generate 3-5 specific compliance requirements in JSON format:
            {{
                "requirements": [
                    {{
                        "title": "Requirement Title",
                        "description": "Detailed description",
                        "compliance_level": "HIGH|MEDIUM|LOW",
                        "deadline": "YYYY-MM-DD or null",
                        "penalty_amount": "Amount or null",
                        "affected_systems": ["system1", "system2"]
                    }}
                ]
            }}
            """
            
            response = self.gemini_client.generate_structured_json(prompt)
            requirements = []
            
            if "requirements" in response:
                for i, req_data in enumerate(response["requirements"]):
                    requirement = ComplianceRequirement(
                        requirement_id=f"llm_req_{regulation['entity_id']}_{i}",
                        title=req_data.get("title", ""),
                        description=req_data.get("description", ""),
                        regulation_id=regulation["entity_id"],
                        jurisdiction=regulation.get("jurisdiction", "UNKNOWN"),
                        compliance_level=req_data.get("compliance_level", "MEDIUM"),
                        deadline=req_data.get("deadline"),
                        penalty_amount=req_data.get("penalty_amount"),
                        affected_systems=req_data.get("affected_systems", []),
                        metadata={"generated_by": "llm", "regulation": regulation}
                    )
                    requirements.append(requirement)
            
            return requirements
            
        except Exception as e:
            self.logger.error(f"Error generating requirements with LLM: {e}")
            return []
    
    def link_related_regulations(self, regulation_id: str) -> List[EntityRelationship]:
        """Link related regulations to a given regulation."""
        try:
            # Get regulation entity
            regulation = self.graph_manager.get_entity(regulation_id)
            if not regulation:
                return []
            
            # Find similar regulations
            similar_regulations = self._find_similar_regulations(regulation)
            
            relationships = []
            for similar_reg in similar_regulations:
                relationship = EntityRelationship(
                    relationship_id=f"rel_{regulation_id}_{similar_reg['entity_id']}",
                    source_entity_id=regulation_id,
                    target_entity_id=similar_reg["entity_id"],
                    relationship_type="RELATED_TO",
                    confidence=similar_reg.get("similarity_score", 0.7),
                    context=f"Similar regulation in {similar_reg.get('jurisdiction', 'UNKNOWN')}",
                    metadata={
                        "similarity_score": similar_reg.get("similarity_score", 0.7),
                        "jurisdiction": similar_reg.get("jurisdiction", "UNKNOWN")
                    }
                )
                relationships.append(relationship)
            
            # Add relationships to graph
            for rel in relationships:
                self.graph_manager.add_relationship(rel)
            
            self.logger.info(f"Linked {len(relationships)} related regulations")
            return relationships
            
        except Exception as e:
            self.logger.error(f"Error linking related regulations: {e}")
            return []
    
    def _find_similar_regulations(self, regulation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find regulations similar to the given regulation."""
        try:
            # Get all regulations
            all_regulations = self.graph_manager.get_entities_by_type("REGULATION")
            
            similar_regs = []
            regulation_name = regulation.get("name", "").lower()
            regulation_jurisdiction = regulation.get("jurisdiction", "")
            
            for reg in all_regulations:
                if reg["entity_id"] == regulation["entity_id"]:
                    continue
                
                # Calculate similarity based on name and jurisdiction
                similarity_score = self._calculate_similarity(regulation_name, reg.get("name", "").lower())
                
                # Boost similarity for same jurisdiction
                if reg.get("jurisdiction") == regulation_jurisdiction:
                    similarity_score += 0.2
                
                if similarity_score > 0.3:  # Threshold for similarity
                    reg["similarity_score"] = min(similarity_score, 1.0)
                    similar_regs.append(reg)
            
            # Sort by similarity score
            similar_regs.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)
            
            return similar_regs[:5]  # Return top 5 similar regulations
            
        except Exception as e:
            self.logger.error(f"Error finding similar regulations: {e}")
            return []
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        if not text1 or not text2:
            return 0.0
        
        # Simple word overlap similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def create_compliance_pathways(self, source_regulation_id: str, 
                                 target_regulation_id: str) -> List[CompliancePathway]:
        """Create compliance pathways between regulations."""
        try:
            # Find paths between regulations
            paths = self.graph_manager.find_path(source_regulation_id, target_regulation_id)
            
            pathways = []
            for i, path in enumerate(paths):
                pathway = CompliancePathway(
                    pathway_id=f"pathway_{source_regulation_id}_{target_regulation_id}_{i}",
                    source_regulation=source_regulation_id,
                    target_regulation=target_regulation_id,
                    pathway_type=self._determine_pathway_type(path),
                    steps=self._extract_pathway_steps(path),
                    estimated_effort=self._estimate_effort(path),
                    timeline=self._estimate_timeline(path),
                    metadata={"path": path, "path_length": len(path)}
                )
                pathways.append(pathway)
            
            self.logger.info(f"Created {len(pathways)} compliance pathways")
            return pathways
            
        except Exception as e:
            self.logger.error(f"Error creating compliance pathways: {e}")
            return []
    
    def _determine_pathway_type(self, path: List[str]) -> str:
        """Determine the type of compliance pathway."""
        if len(path) <= 2:
            return "DIRECT"
        elif len(path) <= 4:
            return "IMPLEMENTATION"
        else:
            return "COMPLEX"
    
    def _extract_pathway_steps(self, path: List[str]) -> List[str]:
        """Extract steps from a compliance pathway."""
        steps = []
        for i, entity_id in enumerate(path):
            entity = self.graph_manager.get_entity(entity_id)
            if entity:
                step = f"Step {i+1}: {entity.get('name', entity_id)}"
                steps.append(step)
        return steps
    
    def _estimate_effort(self, path: List[str]) -> str:
        """Estimate effort required for compliance pathway."""
        if len(path) <= 2:
            return "LOW"
        elif len(path) <= 4:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _estimate_timeline(self, path: List[str]) -> str:
        """Estimate timeline for compliance pathway."""
        if len(path) <= 2:
            return "1-3 months"
        elif len(path) <= 4:
            return "3-6 months"
        else:
            return "6-12 months"
    
    def generate_recommendation_rules(self, jurisdiction: str = None) -> List[RecommendationRule]:
        """Generate recommendation rules for compliance."""
        try:
            # Get regulations for jurisdiction
            if jurisdiction:
                regulations = [reg for reg in self.graph_manager.get_entities_by_type("REGULATION")
                              if reg.get("jurisdiction") == jurisdiction]
            else:
                regulations = self.graph_manager.get_entities_by_type("REGULATION")
            
            rules = []
            
            # Generate rules based on regulation patterns
            for reg in regulations:
                rule = self._create_recommendation_rule(reg)
                if rule:
                    rules.append(rule)
            
            # Generate general compliance rules
            general_rules = self._generate_general_compliance_rules()
            rules.extend(general_rules)
            
            self.logger.info(f"Generated {len(rules)} recommendation rules")
            return rules
            
        except Exception as e:
            self.logger.error(f"Error generating recommendation rules: {e}")
            return []
    
    def _create_recommendation_rule(self, regulation: Dict[str, Any]) -> Optional[RecommendationRule]:
        """Create a recommendation rule from a regulation."""
        try:
            jurisdiction = regulation.get("jurisdiction", "UNKNOWN")
            name = regulation.get("name", "")
            
            # Create rule based on regulation type
            if "AI" in name.upper() or "ARTIFICIAL INTELLIGENCE" in name.upper():
                return RecommendationRule(
                    rule_id=f"rule_ai_{regulation['entity_id']}",
                    name=f"AI Compliance for {name}",
                    description=f"Ensure AI systems comply with {name}",
                    conditions=[
                        "AI model is deployed in production",
                        f"Operating in {jurisdiction}",
                        "Model affects human decisions"
                    ],
                    recommendations=[
                        "Implement explainability features",
                        "Conduct bias testing",
                        "Maintain audit logs",
                        "Provide user notifications"
                    ],
                    priority="HIGH",
                    applicable_jurisdictions=[jurisdiction],
                    metadata={"regulation": regulation}
                )
            elif "DATA" in name.upper() or "PRIVACY" in name.upper():
                return RecommendationRule(
                    rule_id=f"rule_data_{regulation['entity_id']}",
                    name=f"Data Privacy for {name}",
                    description=f"Ensure data handling complies with {name}",
                    conditions=[
                        "Processing personal data",
                        f"Operating in {jurisdiction}",
                        "Data crosses borders"
                    ],
                    recommendations=[
                        "Implement data encryption",
                        "Obtain user consent",
                        "Enable data portability",
                        "Conduct privacy impact assessment"
                    ],
                    priority="HIGH",
                    applicable_jurisdictions=[jurisdiction],
                    metadata={"regulation": regulation}
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error creating recommendation rule: {e}")
            return None
    
    def _generate_general_compliance_rules(self) -> List[RecommendationRule]:
        """Generate general compliance rules."""
        return [
            RecommendationRule(
                rule_id="rule_general_001",
                name="Regular Compliance Monitoring",
                description="Monitor compliance status regularly",
                conditions=[
                    "System is in production",
                    "Regulations may change"
                ],
                recommendations=[
                    "Set up automated monitoring",
                    "Schedule quarterly reviews",
                    "Track regulation updates",
                    "Maintain compliance dashboard"
                ],
                priority="MEDIUM",
                applicable_jurisdictions=["ALL"],
                metadata={"type": "general"}
            ),
            RecommendationRule(
                rule_id="rule_general_002",
                name="Documentation Requirements",
                description="Maintain proper documentation",
                conditions=[
                    "System handles regulated data",
                    "Audit requirements exist"
                ],
                recommendations=[
                    "Document all processes",
                    "Maintain audit trails",
                    "Create compliance reports",
                    "Store evidence of compliance"
                ],
                priority="HIGH",
                applicable_jurisdictions=["ALL"],
                metadata={"type": "general"}
            )
        ]


def main():
    """Test the compliance mapping functionality."""
    print("🧪 Testing Compliance Mapping")
    
    # Test configuration
    from services.regulatory_intelligence.knowledge_graph.graph_database import GraphDatabaseManager
    from services.regulatory_intelligence.knowledge_graph.entity_extraction import KnowledgeGraphConfig
    
    config = KnowledgeGraphConfig()
    graph_manager = GraphDatabaseManager(config)
    mapper = ComplianceMapper(graph_manager, config)
    
    # Test compliance mapping
    print("✅ Compliance mapper initialized")
    
    # Test recommendation rules
    rules = mapper.generate_recommendation_rules()
    print(f"✅ Generated {len(rules)} recommendation rules")
    
    # Test general rules
    general_rules = mapper._generate_general_compliance_rules()
    print(f"✅ Generated {len(general_rules)} general rules")


if __name__ == "__main__":
    main()
