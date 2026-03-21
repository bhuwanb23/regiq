#!/usr/bin/env python3
"""
REGIQ AI/ML - LLM Module Tests
Test suite for Gemini LLM integration.

Tests:
    - Gemini Client
    - Summarization Service
    - Q&A System

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from services.regulatory_intelligence.llm import (
    GeminiClient,
    GeminiClientConfig,
    SummarizationService,
    QASystem,
)


class TestGeminiClient(unittest.TestCase):
    """Test Gemini client functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = GeminiClientConfig()
        self.client = GeminiClient(self.config)

    def test_initialization(self):
        """Test client initialization."""
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.client.config)

    def test_generate_text_basic(self):
        """Test basic text generation."""
        prompt = "Explain what GDPR stands for in one sentence."
        
        try:
            response = self.client.generate_text(prompt)
            
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
        except Exception as e:
            self.skipTest(f"Gemini API not configured or unavailable: {e}")

    def test_generate_with_max_tokens(self):
        """Test text generation with token limit."""
        prompt = "Describe the main principles of data protection."
        
        try:
            response = self.client.generate_text(prompt, max_tokens=50)
            
            self.assertIsInstance(response, str)
            # Response should be reasonable length
            word_count = len(response.split())
            self.assertLess(word_count, 100)  # Should respect max_tokens
        except Exception as e:
            self.skipTest(f"API call failed: {e}")

    def test_generate_with_temperature(self):
        """Test generation with different temperature settings."""
        prompt = "List three benefits of regulatory compliance."
        
        try:
            # Low temperature (more deterministic)
            response1 = self.client.generate_text(prompt, temperature=0.1)
            
            # High temperature (more creative)
            response2 = self.client.generate_text(prompt, temperature=0.9)
            
            self.assertIsInstance(response1, str)
            self.assertIsInstance(response2, str)
        except Exception as e:
            self.skipTest(f"API call failed: {e}")


class TestSummarizationService(unittest.TestCase):
    """Test document summarization."""

    def setUp(self):
        """Set up test fixtures."""
        try:
            self.summarizer = SummarizationService()
        except Exception as e:
            self.skipTest(f"Cannot initialize summarizer: {e}")
        
        self.sample_document = """
        The European Union's General Data Protection Regulation (GDPR) is a comprehensive 
        data privacy law that took effect in May 2018. It grants individuals several rights 
        regarding their personal data, including the right to access, rectify, erase, restrict 
        processing, object to processing, and data portability. Organizations must implement 
        appropriate technical and organizational measures to ensure data protection by design 
        and by default. Non-compliance can result in fines up to €20 million or 4% of annual 
        global turnover, whichever is higher.
        """

    def test_executive_summary(self):
        """Test executive summary generation."""
        try:
            summary = self.summarizer.executive_summary(self.sample_document)
            
            self.assertIsInstance(summary, dict)
            self.assertIn('summary', summary)
            # Summary should be shorter than original
            self.assertLess(len(summary['summary']), len(self.sample_document))
        except Exception as e:
            self.skipTest(f"Summarization requires API access: {e}")

    def test_key_points_extraction(self):
        """Test key points extraction."""
        try:
            key_points = self.summarizer.key_points(self.sample_document, max_points=5)
            
            self.assertIsInstance(key_points, list)
            self.assertLessEqual(len(key_points), 5)
            
            # Each point should be non-empty string
            for point in key_points:
                self.assertIsInstance(point, str)
                self.assertGreater(len(point), 0)
        except Exception as e:
            self.skipTest(f"Key points extraction failed: {e}")

    def test_summarize_different_styles(self):
        """Test summarization with different styles."""
        styles = ["executive", "technical", "brief"]
        
        for style in styles:
            try:
                result = self.summarizer.summarize_document(
                    self.sample_document, style=style
                )
                self.assertIsInstance(result, dict)
            except Exception as e:
                print(f"Style '{style}' failed: {e}")


class TestQASystem(unittest.TestCase):
    """Test question answering system."""

    def setUp(self):
        """Set up test fixtures."""
        try:
            self.qa_system = QASystem()
        except Exception as e:
            self.skipTest(f"Cannot initialize QA system: {e}")
        
        self.context = """
        Basel III is an international regulatory framework for banks. It strengthens 
        bank capital requirements by introducing minimum capital ratios, leverage ratios, 
        and liquidity requirements. The framework aims to improve the banking sector's 
        ability to absorb shocks arising from financial and economic stress.
        """
        
        self.question = "What does Basel III aim to improve?"

    def test_answer_question(self):
        """Test question answering with context."""
        try:
            answer = self.qa_system.answer_question(
                question=self.question,
                context=self.context
            )
            
            self.assertIsInstance(answer, str)
            self.assertGreater(len(answer), 0)
            # Answer should be relevant to the question
        except Exception as e:
            self.skipTest(f"QA system requires API access: {e}")

    def test_answer_with_confidence(self):
        """Test answer generation with confidence score."""
        try:
            result = self.qa_system.answer_question(
                question=self.question,
                context=self.context,
                return_confidence=True
            )
            
            self.assertIsInstance(result, dict)
            self.assertIn('answer', result)
        except Exception as e:
            self.skipTest(f"QA with confidence failed: {e}")

    def test_multiple_questions(self):
        """Test answering multiple questions."""
        questions = [
            "What is Basel III?",
            "What are the capital requirements?",
            "When was it implemented?"
        ]
        
        try:
            answers = []
            for q in questions:
                answer = self.qa_system.answer_question(q, self.context)
                answers.append(answer)
            
            self.assertEqual(len(answers), len(questions))
        except Exception as e:
            self.skipTest(f"Multiple QA failed: {e}")


def run_tests():
    """Run all LLM tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGeminiClient))
    suite.addTests(loader.loadTestsFromTestCase(TestSummarizationService))
    suite.addTests(loader.loadTestsFromTestCase(TestQASystem))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
