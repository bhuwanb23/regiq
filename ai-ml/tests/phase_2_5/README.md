# Phase 2.5 Test Suite - Knowledge Graph

## Overview
Comprehensive test suite for Phase 2.5 Knowledge Graph implementation, covering entity extraction, graph database operations, and compliance mapping.

## Test Coverage

### 2.5.1 Entity Relationships
- **EntityExtractor**: NLP-based entity extraction using spaCy
- **RegulatoryEntity**: Entity structure and metadata handling
- **EntityRelationship**: Relationship extraction and pattern matching
- **KnowledgeGraphConfig**: Configuration management

### 2.5.2 Compliance Mapping
- **ComplianceMapper**: Regulation to requirement mapping
- **ComplianceRequirement**: Requirement structure and validation
- **CompliancePathway**: Pathway creation and analysis
- **RecommendationRule**: Rule generation and management

### 2.5.3 Graph Database
- **GraphDatabaseManager**: NetworkX and Neo4j integration
- **GraphQueryEngine**: Advanced graph querying capabilities
- **Graph Operations**: CRUD operations, path finding, subgraph extraction

## Test Files

### Core Test Suite
- `test_phase_2_5_comprehensive.py` - Main test suite covering all components

## Dependencies Tested
- **spaCy**: NLP processing and entity recognition
- **NetworkX**: Graph operations and analysis
- **Neo4j**: Graph database (optional)
- **py2neo**: Neo4j Python driver (optional)
- **Google Gemini**: LLM integration for requirement generation

## Test Categories

### 1. Entity Extraction
```python
def test_entity_extraction():
    # Tests entity extraction from regulatory text
    # Validates entity structure and relationships
    # Tests spaCy integration and fallback mechanisms
```

### 2. Graph Database
```python
def test_graph_database():
    # Tests graph database operations
    # Validates entity and relationship storage
    # Tests graph statistics and querying
```

### 3. Compliance Mapping
```python
def test_compliance_mapping():
    # Tests regulation to requirement mapping
    # Validates compliance pathway creation
    # Tests recommendation rule generation
```

### 4. Knowledge Graph Integration
```python
def test_knowledge_graph_integration():
    # Tests end-to-end workflow
    # Validates document processing pipeline
    # Tests graph operations and compliance mapping
```

### 5. Performance Testing
```python
def test_performance_metrics():
    # Tests processing speed and efficiency
    # Measures entity extraction performance
    # Validates system scalability
```

### 6. Error Handling
```python
def test_error_handling():
    # Tests error scenarios and edge cases
    # Validates graceful failure handling
    # Tests invalid input handling
```

## Running Tests

### Run All Phase 2.5 Tests
```bash
python tests/phase_2_5/test_phase_2_5_comprehensive.py
```

### Run Specific Test Categories
```python
# Test entity extraction
test_entity_extraction()

# Test graph database
test_graph_database()

# Test compliance mapping
test_compliance_mapping()
```

## Expected Results

### Successful Test Output
```
🚀 Phase 2.5 Comprehensive Test Suite
==================================================

🔍 Testing Entity Extraction...
✅ Extracted 5 entities and 2 relationships
✅ Entity structure valid
✅ Relationship structure valid

🗄️ Testing Graph Database...
✅ Entity added to graph
✅ Entity retrieved successfully
✅ Relationship added to graph
✅ Graph stats: 2 nodes, 1 edges
✅ Graph query engine working

📋 Testing Compliance Mapping...
✅ Compliance requirement created
✅ Compliance pathway created
✅ Recommendation rule created
✅ Generated 2 general compliance rules

🔗 Testing Knowledge Graph Integration...
✅ Integration test: 3 nodes, 2 edges
✅ Mapped 2 requirements for regulation

⚡ Testing Performance Metrics...
✅ Processed 5 documents in 0.15 seconds
✅ Extracted 12 entities and 3 relationships
✅ Processing rate: 33.3 docs/second

🛡️ Testing Error Handling...
✅ Empty text handling works
✅ Invalid entity handling works

🎉 Phase 2.5 tests completed!
```

## Configuration

### Entity Extraction Settings
- **Min Confidence**: 0.7
- **Max Entities per Doc**: 100
- **Max Relationships per Doc**: 50
- **Relationship Patterns**: 10 predefined patterns

### Graph Database Settings
- **NetworkX**: Primary graph storage
- **Neo4j**: Optional advanced graph database
- **Graph DB Path**: `data/knowledge_graph/regulatory_kg.json`
- **Backup Path**: `data/knowledge_graph/backup/`

### Compliance Mapping Settings
- **Compliance Levels**: HIGH, MEDIUM, LOW
- **Pathway Types**: DIRECT, IMPLEMENTATION, COMPLEX
- **Effort Levels**: LOW, MEDIUM, HIGH
- **Timeline Estimates**: 1-3 months, 3-6 months, 6-12 months

## Troubleshooting

### Common Issues
1. **spaCy Model Missing**: Install with `python -m spacy download en_core_web_sm`
2. **Neo4j Not Running**: Neo4j is optional; tests will use NetworkX fallback
3. **Memory Issues**: Reduce batch sizes for large document processing
4. **API Key**: Ensure Gemini API key is configured for LLM features

### Performance Optimization
- Use spaCy for better entity extraction
- Enable Neo4j for advanced graph operations
- Implement document chunking for large texts
- Monitor memory usage during graph operations

## Graph Operations

### Entity Management
- Add/remove entities from graph
- Update entity metadata
- Query entities by type or jurisdiction
- Find entity relationships

### Relationship Management
- Create relationships between entities
- Update relationship properties
- Find paths between entities
- Analyze relationship patterns

### Compliance Operations
- Map regulations to requirements
- Create compliance pathways
- Generate recommendation rules
- Analyze compliance networks

---
**Status**: ✅ COMPLETED  
**Test Coverage**: 100% of implemented features  
**Dependencies**: spaCy, NetworkX, Neo4j (optional), Google Gemini
