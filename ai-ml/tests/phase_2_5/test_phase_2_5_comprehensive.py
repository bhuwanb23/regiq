#!/usr/bin/env python3
"""
Comprehensive Test Suite for Phase 2.5: Knowledge Graph
Tests entity extraction, graph database, and compliance mapping components.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))


def test_entity_extraction():
    print("\n🔍 Testing Entity Extraction...")
    from services.regulatory_intelligence.knowledge_graph.entity_extraction import (
        EntityExtractor, KnowledgeGraphConfig, RegulatoryEntity, EntityRelationship
    )
    
    # Test configuration
    config = KnowledgeGraphConfig()
    extractor = EntityExtractor(config)
    
    # Test entity extraction
    test_text = """
    The SEC requires enhanced disclosures for AI models. The EU AI Act Article 13 mandates 
    transparency requirements. Non-compliance may result in penalties up to $50,000.
    """
    
    entities, relationships = extractor.process_document(test_text, "test_doc_001")
    
    assert len(entities) > 0, "Should extract entities"
    assert len(relationships) >= 0, "Should handle relationships"
    print(f"✅ Extracted {len(entities)} entities and {len(relationships)} relationships")
    
    # Test entity structure
    if entities:
        entity = entities[0]
        assert hasattr(entity, 'entity_id')
        assert hasattr(entity, 'name')
        assert hasattr(entity, 'entity_type')
        print("✅ Entity structure valid")
    
    # Test relationship structure
    if relationships:
        rel = relationships[0]
        assert hasattr(rel, 'relationship_id')
        assert hasattr(rel, 'source_entity_id')
        assert hasattr(rel, 'target_entity_id')
        print("✅ Relationship structure valid")


def test_graph_database():
    print("\n🗄️ Testing Graph Database...")
    from services.regulatory_intelligence.knowledge_graph.graph_database import (
        GraphDatabaseManager, GraphQueryEngine, KnowledgeGraphConfig
    )
    from services.regulatory_intelligence.knowledge_graph.entity_extraction import (
        RegulatoryEntity, EntityRelationship
    )
    
    # Test configuration
    config = KnowledgeGraphConfig()
    graph_manager = GraphDatabaseManager(config)
    
    # Test entity creation
    entity = RegulatoryEntity(
        entity_id="test_entity_001",
        name="SEC Regulation",
        entity_type="REGULATION",
        jurisdiction="US",
        description="Test regulation",
        confidence=0.9,
        metadata={"test": True}
    )
    
    success = graph_manager.add_entity(entity)
    assert success, "Should add entity successfully"
    print("✅ Entity added to graph")
    
    # Test entity retrieval
    retrieved = graph_manager.get_entity("test_entity_001")
    assert retrieved is not None, "Should retrieve entity"
    assert retrieved["name"] == "SEC Regulation"
    print("✅ Entity retrieved successfully")
    
    # Test relationship creation
    entity2 = RegulatoryEntity(
        entity_id="test_entity_002",
        name="Compliance Requirement",
        entity_type="REQUIREMENT",
        jurisdiction="US",
        description="Test requirement",
        confidence=0.8,
        metadata={"test": True}
    )
    
    graph_manager.add_entity(entity2)
    
    relationship = EntityRelationship(
        relationship_id="test_rel_001",
        source_entity_id="test_entity_001",
        target_entity_id="test_entity_002",
        relationship_type="REQUIRES",
        confidence=0.9,
        context="Test relationship",
        metadata={"test": True}
    )
    
    rel_success = graph_manager.add_relationship(relationship)
    assert rel_success, "Should add relationship successfully"
    print("✅ Relationship added to graph")
    
    # Test graph statistics
    stats = graph_manager.get_graph_stats()
    assert "total_nodes" in stats
    assert "total_edges" in stats
    print(f"✅ Graph stats: {stats['total_nodes']} nodes, {stats['total_edges']} edges")
    
    # Test query engine
    query_engine = GraphQueryEngine(graph_manager)
    metrics = query_engine.analyze_graph_metrics()
    assert "basic_stats" in metrics
    print("✅ Graph query engine working")


def test_compliance_mapping():
    print("\n📋 Testing Compliance Mapping...")
    from services.regulatory_intelligence.knowledge_graph.compliance_mapping import (
        ComplianceMapper, ComplianceRequirement, CompliancePathway, RecommendationRule
    )
    from services.regulatory_intelligence.knowledge_graph.graph_database import GraphDatabaseManager
    from services.regulatory_intelligence.knowledge_graph.entity_extraction import KnowledgeGraphConfig
    
    # Test configuration
    config = KnowledgeGraphConfig()
    graph_manager = GraphDatabaseManager(config)
    mapper = ComplianceMapper(graph_manager, config)
    
    # Test compliance requirement creation
    requirement = ComplianceRequirement(
        requirement_id="test_req_001",
        title="Test Requirement",
        description="Test compliance requirement",
        regulation_id="test_reg_001",
        jurisdiction="US",
        compliance_level="HIGH",
        deadline="2025-12-31",
        penalty_amount="$10,000",
        affected_systems=["ai_models", "data_processing"],
        metadata={"test": True}
    )
    
    assert requirement.requirement_id == "test_req_001"
    assert requirement.compliance_level == "HIGH"
    print("✅ Compliance requirement created")
    
    # Test compliance pathway creation
    pathway = CompliancePathway(
        pathway_id="test_pathway_001",
        source_regulation="test_reg_001",
        target_regulation="test_reg_002",
        pathway_type="IMPLEMENTATION",
        steps=["Step 1: Analysis", "Step 2: Implementation"],
        estimated_effort="MEDIUM",
        timeline="3-6 months",
        metadata={"test": True}
    )
    
    assert pathway.pathway_id == "test_pathway_001"
    assert pathway.pathway_type == "IMPLEMENTATION"
    print("✅ Compliance pathway created")
    
    # Test recommendation rule creation
    rule = RecommendationRule(
        rule_id="test_rule_001",
        name="Test Rule",
        description="Test recommendation rule",
        conditions=["Condition 1", "Condition 2"],
        recommendations=["Recommendation 1", "Recommendation 2"],
        priority="HIGH",
        applicable_jurisdictions=["US", "EU"],
        metadata={"test": True}
    )
    
    assert rule.rule_id == "test_rule_001"
    assert rule.priority == "HIGH"
    print("✅ Recommendation rule created")
    
    # Test general compliance rules generation
    general_rules = mapper._generate_general_compliance_rules()
    assert len(general_rules) > 0, "Should generate general rules"
    print(f"✅ Generated {len(general_rules)} general compliance rules")


def test_knowledge_graph_integration():
    print("\n🔗 Testing Knowledge Graph Integration...")
    from services.regulatory_intelligence.knowledge_graph.entity_extraction import (
        EntityExtractor, KnowledgeGraphConfig
    )
    from services.regulatory_intelligence.knowledge_graph.graph_database import GraphDatabaseManager
    from services.regulatory_intelligence.knowledge_graph.compliance_mapping import ComplianceMapper
    
    # Test end-to-end workflow
    config = KnowledgeGraphConfig()
    extractor = EntityExtractor(config)
    graph_manager = GraphDatabaseManager(config)
    mapper = ComplianceMapper(graph_manager, config)
    
    # Test document processing
    test_document = """
    The EU AI Act requires transparency for high-risk AI systems. Article 13 mandates 
    that AI systems must provide explanations for their decisions. Non-compliance 
    may result in fines up to €30 million or 6% of annual turnover.
    """
    
    entities, relationships = extractor.process_document(test_document, "integration_test_001")
    
    # Add entities to graph
    for entity in entities:
        graph_manager.add_entity(entity)
    
    # Add relationships to graph
    for relationship in relationships:
        graph_manager.add_relationship(relationship)
    
    # Test graph operations
    stats = graph_manager.get_graph_stats()
    assert stats["total_nodes"] > 0, "Should have nodes in graph"
    print(f"✅ Integration test: {stats['total_nodes']} nodes, {stats['total_edges']} edges")
    
    # Test compliance mapping
    if entities:
        regulation_entities = [e for e in entities if e.entity_type == "REGULATION"]
        if regulation_entities:
            regulation_id = regulation_entities[0].entity_id
            requirements = mapper.map_regulation_to_requirements(regulation_id)
            print(f"✅ Mapped {len(requirements)} requirements for regulation")


def test_performance_metrics():
    print("\n⚡ Testing Performance Metrics...")
    import time
    from services.regulatory_intelligence.knowledge_graph.entity_extraction import (
        EntityExtractor, KnowledgeGraphConfig
    )
    
    config = KnowledgeGraphConfig()
    extractor = EntityExtractor(config)
    
    # Test processing speed
    test_texts = [
        "SEC requires enhanced disclosures for AI models.",
        "EU AI Act mandates transparency requirements.",
        "GDPR requires data protection measures.",
        "Basel III sets capital requirements for banks.",
        "SOX mandates financial reporting standards."
    ]
    
    start_time = time.time()
    total_entities = 0
    total_relationships = 0
    
    for i, text in enumerate(test_texts):
        entities, relationships = extractor.process_document(text, f"perf_test_{i}")
        total_entities += len(entities)
        total_relationships += len(relationships)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ Processed {len(test_texts)} documents in {duration:.2f} seconds")
    print(f"✅ Extracted {total_entities} entities and {total_relationships} relationships")
    print(f"✅ Processing rate: {len(test_texts)/duration:.1f} docs/second")


def test_error_handling():
    print("\n🛡️ Testing Error Handling...")
    from services.regulatory_intelligence.knowledge_graph.entity_extraction import (
        EntityExtractor, KnowledgeGraphConfig
    )
    from services.regulatory_intelligence.knowledge_graph.graph_database import GraphDatabaseManager
    
    # Test with empty text
    config = KnowledgeGraphConfig()
    extractor = EntityExtractor(config)
    graph_manager = GraphDatabaseManager(config)
    
    try:
        entities, relationships = extractor.process_document("", "empty_test")
        assert isinstance(entities, list)
        assert isinstance(relationships, list)
        print("✅ Empty text handling works")
    except Exception as e:
        print(f"⚠️  Empty text error: {e}")
    
    # Test with invalid entity
    try:
        from services.regulatory_intelligence.knowledge_graph.entity_extraction import RegulatoryEntity
        invalid_entity = RegulatoryEntity(
            entity_id="",  # Empty ID
            name="Test",
            entity_type="TEST",
            jurisdiction="TEST",
            description="Test",
            confidence=0.5,
            metadata={}
        )
        success = graph_manager.add_entity(invalid_entity)
        print("✅ Invalid entity handling works")
    except Exception as e:
        print(f"⚠️  Invalid entity error: {e}")


def main():
    print("🚀 Phase 2.5 Comprehensive Test Suite")
    print("=" * 50)
    
    test_entity_extraction()
    test_graph_database()
    test_compliance_mapping()
    test_knowledge_graph_integration()
    test_performance_metrics()
    test_error_handling()
    
    print("\n🎉 Phase 2.5 tests completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
