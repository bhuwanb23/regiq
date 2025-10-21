#!/usr/bin/env python3
"""
REGIQ AI/ML - Knowledge Graph Database
Manages graph database operations, storage, and queries for regulatory knowledge graph.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
import time

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
    from py2neo.database import Database
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

from services.regulatory_intelligence.knowledge_graph.entity_extraction import (
    RegulatoryEntity, EntityRelationship, KnowledgeGraphConfig
)


class GraphDatabaseManager:
    """Manages knowledge graph database operations."""
    
    def __init__(self, config: Optional[KnowledgeGraphConfig] = None):
        self.config = config or KnowledgeGraphConfig()
        self.logger = self._setup_logger()
        self.graph = self._init_graph()
        self.neo4j_graph = self._init_neo4j()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("graph_database_manager")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def _init_graph(self):
        """Initialize NetworkX graph."""
        if not NETWORKX_AVAILABLE:
            self.logger.warning("NetworkX not available")
            return None
        
        try:
            graph = nx.DiGraph()
            self.logger.info("NetworkX graph initialized")
            return graph
        except Exception as e:
            self.logger.error(f"Failed to initialize NetworkX graph: {e}")
            return None
    
    def _init_neo4j(self):
        """Initialize Neo4j connection."""
        if not NEO4J_AVAILABLE:
            self.logger.warning("Neo4j not available")
            return None
        
        try:
            # Try to connect to Neo4j (will fail if not running)
            graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
            self.logger.info("Neo4j connection established")
            return graph
        except Exception as e:
            self.logger.warning(f"Neo4j not available: {e}")
            return None
    
    def add_entity(self, entity: RegulatoryEntity) -> bool:
        """Add an entity to the graph database."""
        try:
            # Add to NetworkX graph
            if self.graph is not None:
                self.graph.add_node(
                    entity.entity_id,
                    **{
                        "name": entity.name,
                        "entity_type": entity.entity_type,
                        "jurisdiction": entity.jurisdiction,
                        "description": entity.description,
                        "confidence": entity.confidence,
                        "metadata": entity.metadata
                    }
                )
            
            # Add to Neo4j if available
            if self.neo4j_graph is not None:
                node = Node(
                    "Entity",
                    entity_id=entity.entity_id,
                    name=entity.name,
                    entity_type=entity.entity_type,
                    jurisdiction=entity.jurisdiction,
                    description=entity.description,
                    confidence=entity.confidence,
                    **entity.metadata
                )
                self.neo4j_graph.create(node)
            
            self.logger.info(f"Added entity: {entity.entity_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add entity {entity.entity_id}: {e}")
            return False
    
    def add_relationship(self, relationship: EntityRelationship) -> bool:
        """Add a relationship to the graph database."""
        try:
            # Add to NetworkX graph
            if self.graph is not None:
                self.graph.add_edge(
                    relationship.source_entity_id,
                    relationship.target_entity_id,
                    **{
                        "relationship_type": relationship.relationship_type,
                        "confidence": relationship.confidence,
                        "context": relationship.context,
                        "metadata": relationship.metadata
                    }
                )
            
            # Add to Neo4j if available
            if self.neo4j_graph is not None:
                matcher = NodeMatcher(self.neo4j_graph)
                source_node = matcher.match("Entity", entity_id=relationship.source_entity_id).first()
                target_node = matcher.match("Entity", entity_id=relationship.target_entity_id).first()
                
                if source_node and target_node:
                    rel = Relationship(
                        source_node,
                        relationship.relationship_type,
                        target_node,
                        confidence=relationship.confidence,
                        context=relationship.context,
                        **relationship.metadata
                    )
                    self.neo4j_graph.create(rel)
            
            self.logger.info(f"Added relationship: {relationship.relationship_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add relationship {relationship.relationship_id}: {e}")
            return False
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get an entity by ID."""
        try:
            if self.graph is not None and entity_id in self.graph.nodes:
                return dict(self.graph.nodes[entity_id])
            return None
        except Exception as e:
            self.logger.error(f"Failed to get entity {entity_id}: {e}")
            return None
    
    def get_entities_by_type(self, entity_type: str) -> List[Dict[str, Any]]:
        """Get all entities of a specific type."""
        try:
            entities = []
            
            if self.graph is not None:
                for node_id, data in self.graph.nodes(data=True):
                    if data.get("entity_type") == entity_type:
                        entities.append({"entity_id": node_id, **data})
            
            return entities
        except Exception as e:
            self.logger.error(f"Failed to get entities by type {entity_type}: {e}")
            return []
    
    def get_relationships(self, entity_id: str) -> List[Dict[str, Any]]:
        """Get all relationships for an entity."""
        try:
            relationships = []
            
            if self.graph is not None:
                # Outgoing relationships
                for target_id in self.graph.successors(entity_id):
                    edge_data = self.graph[entity_id][target_id]
                    relationships.append({
                        "source": entity_id,
                        "target": target_id,
                        "direction": "outgoing",
                        **edge_data
                    })
                
                # Incoming relationships
                for source_id in self.graph.predecessors(entity_id):
                    edge_data = self.graph[source_id][entity_id]
                    relationships.append({
                        "source": source_id,
                        "target": entity_id,
                        "direction": "incoming",
                        **edge_data
                    })
            
            return relationships
        except Exception as e:
            self.logger.error(f"Failed to get relationships for {entity_id}: {e}")
            return []
    
    def find_path(self, source_entity_id: str, target_entity_id: str, 
                  max_length: int = 5) -> List[List[str]]:
        """Find paths between two entities."""
        try:
            if self.graph is None:
                return []
            
            try:
                paths = list(nx.all_simple_paths(
                    self.graph, source_entity_id, target_entity_id, 
                    cutoff=max_length
                ))
                return paths
            except nx.NetworkXNoPath:
                return []
        except Exception as e:
            self.logger.error(f"Failed to find path: {e}")
            return []
    
    def get_subgraph(self, entity_ids: List[str]) -> Optional[nx.DiGraph]:
        """Get subgraph containing specified entities."""
        try:
            if self.graph is None:
                return None
            
            return self.graph.subgraph(entity_ids)
        except Exception as e:
            self.logger.error(f"Failed to get subgraph: {e}")
            return None
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Get statistics about the graph."""
        try:
            stats = {
                "networkx_available": NETWORKX_AVAILABLE,
                "neo4j_available": NEO4J_AVAILABLE,
                "total_nodes": 0,
                "total_edges": 0,
                "entity_types": {},
                "relationship_types": {}
            }
            
            if self.graph is not None:
                stats["total_nodes"] = self.graph.number_of_nodes()
                stats["total_edges"] = self.graph.number_of_edges()
                
                # Count entity types
                for node_id, data in self.graph.nodes(data=True):
                    entity_type = data.get("entity_type", "UNKNOWN")
                    stats["entity_types"][entity_type] = stats["entity_types"].get(entity_type, 0) + 1
                
                # Count relationship types
                for source, target, data in self.graph.edges(data=True):
                    rel_type = data.get("relationship_type", "UNKNOWN")
                    stats["relationship_types"][rel_type] = stats["relationship_types"].get(rel_type, 0) + 1
            
            return stats
        except Exception as e:
            self.logger.error(f"Failed to get graph stats: {e}")
            return {}
    
    def save_graph(self, filepath: str = None) -> bool:
        """Save graph to file."""
        try:
            filepath = filepath or self.config.graph_db_path
            
            # Create directory
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            if self.graph is not None:
                # Convert to JSON-serializable format
                graph_data = {
                    "nodes": [
                        {"id": node_id, **data} 
                        for node_id, data in self.graph.nodes(data=True)
                    ],
                    "edges": [
                        {"source": source, "target": target, **data}
                        for source, target, data in self.graph.edges(data=True)
                    ]
                }
                
                with open(filepath, 'w') as f:
                    json.dump(graph_data, f, indent=2)
                
                self.logger.info(f"Graph saved to {filepath}")
                return True
            
            return False
        except Exception as e:
            self.logger.error(f"Failed to save graph: {e}")
            return False
    
    def load_graph(self, filepath: str = None) -> bool:
        """Load graph from file."""
        try:
            filepath = filepath or self.config.graph_db_path
            
            if not os.path.exists(filepath):
                self.logger.warning(f"Graph file not found: {filepath}")
                return False
            
            with open(filepath, 'r') as f:
                graph_data = json.load(f)
            
            if self.graph is not None:
                # Clear existing graph
                self.graph.clear()
                
                # Add nodes
                for node_data in graph_data.get("nodes", []):
                    node_id = node_data.pop("id")
                    self.graph.add_node(node_id, **node_data)
                
                # Add edges
                for edge_data in graph_data.get("edges", []):
                    source = edge_data.pop("source")
                    target = edge_data.pop("target")
                    self.graph.add_edge(source, target, **edge_data)
                
                self.logger.info(f"Graph loaded from {filepath}")
                return True
            
            return False
        except Exception as e:
            self.logger.error(f"Failed to load graph: {e}")
            return False


class GraphQueryEngine:
    """Advanced graph querying capabilities."""
    
    def __init__(self, graph_manager: GraphDatabaseManager):
        self.graph_manager = graph_manager
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("graph_query_engine")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(h)
        return logger
    
    def find_compliance_paths(self, regulation_id: str, requirement_id: str) -> List[List[str]]:
        """Find compliance pathways between regulation and requirement."""
        try:
            paths = self.graph_manager.find_path(regulation_id, requirement_id)
            self.logger.info(f"Found {len(paths)} compliance paths")
            return paths
        except Exception as e:
            self.logger.error(f"Failed to find compliance paths: {e}")
            return []
    
    def find_related_regulations(self, entity_id: str, max_depth: int = 2) -> List[Dict[str, Any]]:
        """Find regulations related to an entity within max_depth."""
        try:
            if self.graph_manager.graph is None:
                return []
            
            # Get entities within max_depth
            related_entities = []
            visited = set()
            queue = [(entity_id, 0)]
            
            while queue:
                current_id, depth = queue.pop(0)
                if current_id in visited or depth > max_depth:
                    continue
                
                visited.add(current_id)
                
                # Get entity data
                entity_data = self.graph_manager.get_entity(current_id)
                if entity_data and entity_data.get("entity_type") == "REGULATION":
                    related_entities.append({
                        "entity_id": current_id,
                        "depth": depth,
                        **entity_data
                    })
                
                # Add neighbors to queue
                if depth < max_depth:
                    for neighbor in self.graph_manager.graph.neighbors(current_id):
                        if neighbor not in visited:
                            queue.append((neighbor, depth + 1))
            
            return related_entities
        except Exception as e:
            self.logger.error(f"Failed to find related regulations: {e}")
            return []
    
    def get_compliance_network(self, jurisdiction: str) -> Optional[nx.DiGraph]:
        """Get compliance network for a specific jurisdiction."""
        try:
            if self.graph_manager.graph is None:
                return None
            
            # Find all entities in jurisdiction
            jurisdiction_entities = []
            for node_id, data in self.graph_manager.graph.nodes(data=True):
                if data.get("jurisdiction") == jurisdiction:
                    jurisdiction_entities.append(node_id)
            
            # Get subgraph
            return self.graph_manager.get_subgraph(jurisdiction_entities)
        except Exception as e:
            self.logger.error(f"Failed to get compliance network: {e}")
            return None
    
    def analyze_graph_metrics(self) -> Dict[str, Any]:
        """Analyze graph metrics and properties."""
        try:
            if self.graph_manager.graph is None:
                return {}
            
            graph = self.graph_manager.graph
            
            metrics = {
                "basic_stats": {
                    "nodes": graph.number_of_nodes(),
                    "edges": graph.number_of_edges(),
                    "density": nx.density(graph)
                },
                "connectivity": {
                    "is_weakly_connected": nx.is_weakly_connected(graph),
                    "number_weakly_connected_components": nx.number_weakly_connected_components(graph)
                },
                "centrality": {}
            }
            
            # Calculate centrality measures for small graphs
            if graph.number_of_nodes() < 1000:
                try:
                    metrics["centrality"]["betweenness"] = nx.betweenness_centrality(graph)
                    metrics["centrality"]["closeness"] = nx.closeness_centrality(graph)
                    metrics["centrality"]["degree"] = nx.degree_centrality(graph)
                except Exception as e:
                    self.logger.warning(f"Failed to calculate centrality: {e}")
            
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to analyze graph metrics: {e}")
            return {}


def main():
    """Test the graph database functionality."""
    print("🧪 Testing Graph Database")
    
    # Test configuration
    config = KnowledgeGraphConfig()
    graph_manager = GraphDatabaseManager(config)
    
    # Test entity
    from services.regulatory_intelligence.knowledge_graph.entity_extraction import RegulatoryEntity
    entity = RegulatoryEntity(
        entity_id="test_entity_001",
        name="SEC Regulation",
        entity_type="REGULATION",
        jurisdiction="US",
        description="Test regulation",
        confidence=0.9,
        metadata={"test": True}
    )
    
    # Test adding entity
    success = graph_manager.add_entity(entity)
    print(f"✅ Added entity: {success}")
    
    # Test getting entity
    retrieved = graph_manager.get_entity("test_entity_001")
    print(f"✅ Retrieved entity: {retrieved is not None}")
    
    # Test graph stats
    stats = graph_manager.get_graph_stats()
    print(f"✅ Graph stats: {stats}")
    
    # Test query engine
    query_engine = GraphQueryEngine(graph_manager)
    metrics = query_engine.analyze_graph_metrics()
    print(f"✅ Graph metrics: {metrics}")


if __name__ == "__main__":
    main()
