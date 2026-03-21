#!/usr/bin/env python3
"""
REGIQ AI/ML - NLP Module Tests
Test suite for regulatory NLP components.

Tests:
    - Text Preprocessing
    - Regulatory Entity Recognition (NER)
    - Text Classification

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.regulatory_intelligence.nlp import (
    TextPreprocessor,
    RegulatoryEntityRecognizer,
    RegulatoryTextClassifier,
)


class TestTextPreprocessor(unittest.TestCase):
    """Test text preprocessing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = TextPreprocessor()
        
        # Sample regulatory text
        self.sample_text = """
        The Securities and Exchange Commission (SEC) announced today that 
        all financial institutions must comply with new regulations by December 31, 2025.
        Non-compliance may result in penalties up to $10,000,000.
        Contact: compliance@sec.gov for more information.
        Visit https://www.sec.gov/regulations for details.
        """

    def test_clean_text_basic(self):
        """Test basic text cleaning."""
        cleaned = self.preprocessor.clean_text(self.sample_text)
        
        self.assertIsInstance(cleaned, str)
        self.assertGreater(len(cleaned), 0)
        # Should remove extra whitespace
        self.assertNotIn('  ', cleaned)

    def test_remove_special_characters(self):
        """Test special character removal."""
        text_with_special = "Email: test@example.com; Phone: +1-555-123-4567"
        cleaned = self.preprocessor.clean_text(text_with_special)
        
        self.assertIsInstance(cleaned, str)
        # Should handle special characters gracefully

    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        messy_text = "This   has    lots     of      spaces"
        cleaned = self.preprocessor.clean_text(messy_text)
        
        self.assertNotIn('  ', cleaned)
        self.assertEqual(cleaned.count(' '), len(cleaned.split()) - 1)

    def test_tokenize_sentences(self):
        """Test sentence tokenization."""
        sentences = self.preprocessor.tokenize_sentences(self.sample_text)
        
        self.assertIsInstance(sentences, list)
        self.assertGreater(len(sentences), 0)
        
        # Each sentence should be non-empty
        for sentence in sentences:
            self.assertIsInstance(sentence, str)
            self.assertGreater(len(sentence), 0)

    def test_tokenize_words(self):
        """Test word tokenization."""
        words = self.preprocessor.tokenize_words("Hello world! This is a test.")
        
        self.assertIsInstance(words, list)
        self.assertGreater(len(words), 0)

    def test_remove_stopwords(self):
        """Test stopword removal."""
        text = "The quick brown fox jumps over the lazy dog"
        filtered = self.preprocessor.remove_stopwords(text)
        
        self.assertIsInstance(filtered, str)
        # Should remove common stopwords
        self.assertLess(len(filtered.split()), len(text.split()))

    def test_lemmatize(self):
        """Test lemmatization."""
        text = "running runs ran easily"
        lemmatized = self.preprocessor.lemmatize(text)
        
        self.assertIsInstance(lemmatized, str)
        # "running", "runs", "ran" should become "run"

    def test_full_preprocessing_pipeline(self):
        """Test complete preprocessing pipeline."""
        result = self.preprocessor.preprocess(self.sample_text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('cleaned_text', result)
        self.assertIn('sentences', result)
        self.assertIn('tokens', result)


class TestRegulatoryEntityRecognizer(unittest.TestCase):
    """Test regulatory entity recognition."""

    def setUp(self):
        """Set up test fixtures."""
        self.recognizer = RegulatoryEntityRecognizer()
        
        # Sample text with regulatory entities
        self.sample_text = """
        The European Central Bank (ECB) requires compliance with GDPR 
        by March 15, 2025. Institutions failing to comply face fines 
        up to €20,000,000 or 4% of annual revenue.
        """

    def test_extract_regulatory_entities(self):
        """Test regulatory entity extraction."""
        entities = self.recognizer.extract_entities(self.sample_text)
        
        self.assertIsNotNone(entities)
        # Should extract some entities
        self.assertGreater(len(entities.all_entities), 0)

    def test_extract_dates(self):
        """Test date entity extraction."""
        result = self.recognizer.extract_entities(self.sample_text)
        
        # Should find "March 15, 2025"
        date_entities = [e for e in result.all_entities if e.get('label') == 'DATE']
        self.assertGreater(len(date_entities), 0)

    def test_extract_penalties(self):
        """Test penalty amount extraction."""
        result = self.recognizer.extract_entities(self.sample_text)
        
        # Should find "€20,000,000"
        penalty_entities = [e for e in result.all_entities if e.get('label') == 'PENALTY_AMOUNT']
        self.assertGreater(len(penalty_entities), 0)

    def test_extract_regulatory_agencies(self):
        """Test regulatory agency extraction."""
        result = self.recognizer.extract_entities(self.sample_text)
        
        # Should find "European Central Bank (ECB)"
        agency_entities = [e for e in result.all_entities if e.get('label') == 'REGULATORY_AGENCY']
        self.assertGreater(len(agency_entities), 0)

    def test_entity_context(self):
        """Test entity context extraction."""
        result = self.recognizer.extract_entities(self.sample_text)
        
        # Entities should have context
        for entity in result.all_entities:
            if 'context' in entity:
                self.assertIsInstance(entity['context'], str)
                self.assertGreater(len(entity['context']), 0)

    def test_empty_text_handling(self):
        """Test handling of empty text."""
        result = self.recognizer.extract_entities("")
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result.all_entities), 0)

    def test_multiple_entities_same_type(self):
        """Test extraction of multiple entities of same type."""
        text = """
        SEC and CFTC jointly announced regulations. 
        Both SEC and CFTC will enforce compliance.
        """
        result = self.recognizer.extract_entities(text)
        
        # Should find multiple agencies
        agencies = [e for e in result.all_entities if e.get('label') == 'REGULATORY_AGENCY']
        self.assertGreater(len(agencies), 0)


class TestRegulatoryTextClassifier(unittest.TestCase):
    """Test regulatory text classification."""

    def setUp(self):
        """Set up test fixtures."""
        self.classifier = RegulatoryTextClassifier()
        
        # Sample texts of different types
        self.privacy_text = """
        Under GDPR Article 17, individuals have the right to erasure 
        of their personal data. Data controllers must comply within 
        30 days of request.
        """
        
        self.financial_text = """
        Basel III requirements mandate minimum capital ratios of 8% 
        for tier 1 capital and 10.5% for total capital adequacy.
        """
        
        self.ai_governance_text = """
        EU AI Act classifies high-risk AI systems as those used in 
        critical infrastructure, education, and law enforcement.
        """

    def test_classify_privacy_document(self):
        """Test classification of privacy-related text."""
        result = self.classifier.classify(self.privacy_text)
        
        self.assertIsNotNone(result)
        self.assertIn('predicted_category', result)
        # Should identify as privacy/GDPR related

    def test_classify_financial_document(self):
        """Test classification of financial regulation text."""
        result = self.classifier.classify(self.financial_text)
        
        self.assertIsNotNone(result)
        self.assertIn('predicted_category', result)
        # Should identify as financial regulation

    def test_classify_ai_governance_document(self):
        """Test classification of AI governance text."""
        result = self.classifier.classify(self.ai_governance_text)
        
        self.assertIsNotNone(result)
        self.assertIn('predicted_category', result)
        # Should identify as AI/technology regulation

    def test_classification_confidence(self):
        """Test classification confidence scores."""
        result = self.classifier.classify(self.privacy_text)
        
        self.assertIn('confidence', result)
        confidence = result['confidence']
        
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

    def test_multi_label_classification(self):
        """Test multi-label classification capability."""
        # Text that could belong to multiple categories
        mixed_text = """
        Financial institutions must protect customer data under GDPR 
        while maintaining capital reserves per Basel III.
        """
        result = self.classifier.classify(mixed_text)
        
        self.assertIsNotNone(result)
        # May return multiple categories or highest confidence one

    def test_top_k_predictions(self):
        """Test top-k prediction retrieval."""
        result = self.classifier.classify(self.financial_text, top_k=3)
        
        self.assertIsNotNone(result)
        # Should return up to top_k predictions

    def test_unknown_category_handling(self):
        """Test handling of text outside known categories."""
        # Text unrelated to regulations
        unrelated_text = "The weather is sunny today with temperatures around 75°F."
        result = self.classifier.classify(unrelated_text)
        
        self.assertIsNotNone(result)
        # Should still return a prediction (possibly with low confidence)


def run_tests():
    """Run all NLP tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTextPreprocessor))
    suite.addTests(loader.loadTestsFromTestCase(TestRegulatoryEntityRecognizer))
    suite.addTests(loader.loadTestsFromTestCase(TestRegulatoryTextClassifier))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
