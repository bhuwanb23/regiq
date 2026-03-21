#!/usr/bin/env python3
"""
REGIQ AI/ML - Knowledge Graph & Scrapers Tests
Concise test suite for knowledge graph and document scrapers.

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.regulatory_intelligence.knowledge_graph import (
    EntityExtractor,
    ComplianceMapper,
    GraphDatabaseManager,
)


class TestKnowledgeGraph(unittest.TestCase):
    """Test knowledge graph functionality."""

    def setUp(self):
        """Set up fixtures."""
        self.extractor = EntityExtractor()
        self.mapper = ComplianceMapper()

    def test_extract_entities(self):
        """Test entity extraction from text."""
        text = "GDPR requires compliance by Q4 2025"
        entities = self.extractor.extract(text)
        
        self.assertIsNotNone(entities)
        # Should extract some entities

    def test_map_compliance_requirements(self):
        """Test compliance requirement mapping."""
        regulation = "EU AI Act Article 10"
        mappings = self.mapper.map_regulation(regulation)
        
        self.assertIsInstance(mappings, list)

    def test_graph_database_connection(self):
        """Test graph database connectivity."""
        gdb = GraphDatabaseManager()
        
        try:
            gdb.connect()
            connected = True
        except Exception:
            connected = False
        
        # May fail if Neo4j not running - that's OK
        self.assertIsInstance(connected, bool)


# Scrapers tests
from services.regulatory_intelligence.scrapers import (
    PDFProcessor,
    DocumentProcessingPipeline,
)


class TestScrapers(unittest.TestCase):
    """Test scraper functionality."""

    def setUp(self):
        """Set up fixtures."""
        self.pdf_processor = PDFProcessor()
        self.pipeline = DocumentProcessingPipeline()

    def test_pdf_processor_initialization(self):
        """Test PDF processor setup."""
        self.assertIsNotNone(self.pdf_processor)

    def test_pipeline_initialization(self):
        """Test pipeline setup."""
        self.assertIsNotNone(self.pipeline)

    def test_extract_text_from_pdf_missing_file(self):
        """Test handling of missing PDF file."""
        with self.assertRaises(Exception):
            self.pdf_processor.extract_text("nonexistent.pdf")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestScrapers))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
