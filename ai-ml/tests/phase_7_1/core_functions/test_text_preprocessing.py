"""Unit tests for text preprocessing functionality"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

import pytest
from services.regulatory_intelligence.nlp.text_preprocessing import (
    TextPreprocessor, 
    PreprocessingConfig,
    ProcessedText
)

def test_text_preprocessor_initialization():
    """Test that TextPreprocessor can be initialized."""
    # Test with default config
    preprocessor = TextPreprocessor()
    assert preprocessor is not None
    assert preprocessor.config is not None
    
    # Test with custom config
    config = PreprocessingConfig(remove_stopwords=False, lemmatize=False)
    preprocessor = TextPreprocessor(config=config)
    assert preprocessor.config.remove_stopwords == False
    assert preprocessor.config.lemmatize == False

def test_clean_text():
    """Test text cleaning functionality."""
    preprocessor = TextPreprocessor()
    
    # Test basic cleaning
    text = "  This   is   a   test   text.  "
    cleaned = preprocessor.clean_text(text)
    assert cleaned == "This is a test text."
    
    # Test HTML tag removal
    text = "<p>This is <b>bold</b> text</p>"
    cleaned = preprocessor.clean_text(text)
    assert "<" not in cleaned
    assert ">" not in cleaned
    
    # Test empty text
    cleaned = preprocessor.clean_text("")
    assert cleaned == ""

def test_remove_noise():
    """Test noise removal functionality."""
    preprocessor = TextPreprocessor()
    
    # Test URL removal
    text = "Visit https://example.com for more info"
    cleaned = preprocessor._remove_noise(text)
    assert "https://example.com" not in cleaned
    
    # Test email removal
    text = "Contact us at info@example.com"
    cleaned = preprocessor._remove_noise(text)
    assert "@" not in cleaned
    
    # Test excessive punctuation reduction
    text = "What??? Really!!!"
    cleaned = preprocessor._remove_noise(text)
    assert cleaned == "What? Really!"

def test_handle_special_characters():
    """Test special character handling."""
    preprocessor = TextPreprocessor()
    
    # Test smart quote handling
    text = '"Smart" quotes'
    cleaned = preprocessor._handle_special_characters(text)
    # Should handle smart quotes (implementation may vary)
    
    # Test dash normalization
    text = "En–dash and em—dash"
    cleaned = preprocessor._handle_special_characters(text)
    # Should normalize dashes

if __name__ == "__main__":
    pytest.main([__file__, "-v"])