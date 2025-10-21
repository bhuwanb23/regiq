#!/usr/bin/env python3
"""
REGIQ AI/ML - Text Preprocessing Module
Advanced text preprocessing for regulatory documents.
Handles cleaning, normalization, tokenization, and segmentation.
"""

import os
import sys
import re
import logging
import unicodedata
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
import string

# NLP Libraries
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.env_config import get_env_config

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('omw-1.4', quiet=True)
except Exception as e:
    print(f"⚠️  NLTK data download warning: {e}")


@dataclass
class PreprocessingConfig:
    """Configuration for text preprocessing."""
    remove_stopwords: bool = True
    lemmatize: bool = True
    remove_punctuation: bool = False
    remove_numbers: bool = False
    min_word_length: int = 2
    max_word_length: int = 50
    preserve_regulatory_terms: bool = True
    custom_stopwords: List[str] = None


@dataclass
class ProcessedText:
    """Processed text data structure."""
    original_text: str
    cleaned_text: str
    tokens: List[str]
    sentences: List[str]
    lemmatized_tokens: List[str] = None
    pos_tags: List[Tuple[str, str]] = None
    metadata: Dict[str, Any] = None


class TextPreprocessor:
    """
    Advanced text preprocessing for regulatory documents.
    Handles cleaning, normalization, tokenization, and segmentation.
    """
    
    def __init__(self, config: PreprocessingConfig = None):
        """Initialize text preprocessor."""
        self.env_config = get_env_config()
        self.config = config or PreprocessingConfig()
        self.logger = self._setup_logging()
        
        # Initialize NLP components
        self._initialize_nlp_components()
        
        # Regulatory-specific terms to preserve
        self.regulatory_terms = {
            'SEC', 'CFTC', 'FDIC', 'FINRA', 'ESMA', 'EBA', 'ECB',
            'GDPR', 'SOX', 'Basel', 'MiFID', 'Dodd-Frank',
            'compliance', 'regulation', 'regulatory', 'supervision',
            'penalty', 'fine', 'sanction', 'violation', 'breach',
            'deadline', 'requirement', 'mandate', 'obligation'
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for text preprocessor."""
        logger = logging.getLogger('text_preprocessor')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_nlp_components(self):
        """Initialize NLP components."""
        try:
            # Initialize spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            self.logger.info("✅ spaCy model loaded successfully")
        except OSError:
            self.logger.warning("⚠️  spaCy model not found, using basic tokenization")
            self.nlp = None
        
        # Initialize NLTK components
        try:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            self.logger.info("✅ NLTK components initialized successfully")
        except Exception as e:
            self.logger.error(f"❌ NLTK initialization failed: {e}")
            self.stop_words = set()
            self.lemmatizer = None
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Convert to string and normalize unicode
        text = str(text)
        text = unicodedata.normalize('NFKD', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but preserve regulatory terms
        if self.config.preserve_regulatory_terms:
            # Preserve regulatory terms during cleaning
            preserved_terms = {}
            for i, term in enumerate(self.regulatory_terms):
                placeholder = f"__REGULATORY_TERM_{i}__"
                text = text.replace(term, placeholder)
                preserved_terms[placeholder] = term
        
        # Remove noise and formatting
        text = self._remove_noise(text)
        
        # Handle special characters
        text = self._handle_special_characters(text)
        
        # Restore regulatory terms
        if self.config.preserve_regulatory_terms:
            for placeholder, term in preserved_terms.items():
                text = text.replace(placeholder, term)
        
        # Final cleanup
        text = text.strip()
        
        return text
    
    def _remove_noise(self, text: str) -> str:
        """Remove noise and formatting from text."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        text = re.sub(r'[.]{2,}', '.', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _handle_special_characters(self, text: str) -> str:
        """Handle special characters in text."""
        # Replace smart quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('–', '-').replace('—', '-')
        
        # Handle currency symbols
        text = re.sub(r'[$€£¥]\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', r'$\1', text)
        
        # Handle percentages
        text = re.sub(r'(\d+(?:\.\d+)?)\s*%', r'\1 percent', text)
        
        # Handle fractions
        text = re.sub(r'(\d+)/(\d+)', r'\1 over \2', text)
        
        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        if not text:
            return []
        
        # Use spaCy if available, otherwise NLTK
        if self.nlp:
            doc = self.nlp(text)
            tokens = [token.text for token in doc if not token.is_space]
        else:
            tokens = word_tokenize(text)
        
        # Filter tokens by length
        tokens = [
            token for token in tokens 
            if self.config.min_word_length <= len(token) <= self.config.max_word_length
        ]
        
        return tokens
    
    def segment_sentences(self, text: str) -> List[str]:
        """
        Segment text into sentences.
        
        Args:
            text: Text to segment
            
        Returns:
            List of sentences
        """
        if not text:
            return []
        
        # Use spaCy if available, otherwise NLTK
        if self.nlp:
            doc = self.nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        else:
            sentences = sent_tokenize(text)
        
        return sentences
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Tokens with stopwords removed
        """
        if not self.config.remove_stopwords:
            return tokens
        
        # Create custom stopwords list
        custom_stopwords = self.stop_words.copy()
        
        # Add custom stopwords if provided
        if self.config.custom_stopwords:
            custom_stopwords.update(self.config.custom_stopwords)
        
        # Remove stopwords but preserve regulatory terms
        filtered_tokens = []
        for token in tokens:
            token_lower = token.lower()
            if (token_lower not in custom_stopwords or 
                token in self.regulatory_terms or
                any(term.lower() in token_lower for term in self.regulatory_terms)):
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Lemmatized tokens
        """
        if not self.config.lemmatize or not self.lemmatizer:
            return tokens
        
        lemmatized = []
        for token in tokens:
            # Preserve regulatory terms
            if token in self.regulatory_terms:
                lemmatized.append(token)
            else:
                lemmatized.append(self.lemmatizer.lemmatize(token))
        
        return lemmatized
    
    def get_pos_tags(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """
        Get part-of-speech tags for tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            List of (token, pos_tag) tuples
        """
        if not tokens:
            return []
        
        # Use spaCy if available, otherwise NLTK
        if self.nlp:
            doc = self.nlp(' '.join(tokens))
            pos_tags = [(token.text, token.pos_) for token in doc]
        else:
            pos_tags = pos_tag(tokens)
        
        return pos_tags
    
    def process_text(self, text: str) -> ProcessedText:
        """
        Complete text preprocessing pipeline.
        
        Args:
            text: Raw text to process
            
        Returns:
            ProcessedText object with all preprocessing results
        """
        self.logger.info("🧹 Starting text preprocessing")
        
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize_text(cleaned_text)
        
        # Segment sentences
        sentences = self.segment_sentences(cleaned_text)
        
        # Remove stopwords
        filtered_tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        lemmatized_tokens = self.lemmatize_tokens(filtered_tokens)
        
        # Get POS tags
        pos_tags = self.get_pos_tags(filtered_tokens)
        
        # Create metadata
        metadata = {
            'original_length': len(text),
            'cleaned_length': len(cleaned_text),
            'token_count': len(tokens),
            'filtered_token_count': len(filtered_tokens),
            'sentence_count': len(sentences),
            'regulatory_terms_found': [term for term in self.regulatory_terms if term in text],
            'processing_config': {
                'remove_stopwords': self.config.remove_stopwords,
                'lemmatize': self.config.lemmatize,
                'min_word_length': self.config.min_word_length,
                'max_word_length': self.config.max_word_length
            }
        }
        
        result = ProcessedText(
            original_text=text,
            cleaned_text=cleaned_text,
            tokens=filtered_tokens,
            sentences=sentences,
            lemmatized_tokens=lemmatized_tokens,
            pos_tags=pos_tags,
            metadata=metadata
        )
        
        self.logger.info(f"✅ Text preprocessing completed: {len(filtered_tokens)} tokens, {len(sentences)} sentences")
        
        return result
    
    def batch_process(self, texts: List[str]) -> List[ProcessedText]:
        """
        Process multiple texts in batch.
        
        Args:
            texts: List of texts to process
            
        Returns:
            List of ProcessedText objects
        """
        self.logger.info(f"🔄 Batch processing {len(texts)} texts")
        
        results = []
        for i, text in enumerate(texts):
            try:
                result = self.process_text(text)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error processing text {i}: {e}")
                # Create empty result for failed processing
                results.append(ProcessedText(
                    original_text=text,
                    cleaned_text="",
                    tokens=[],
                    sentences=[],
                    metadata={'error': str(e)}
                ))
        
        self.logger.info(f"✅ Batch processing completed: {len(results)} results")
        return results


def main():
    """Test the text preprocessing module."""
    print("🧪 Testing Text Preprocessing Module")
    print("="*50)
    
    # Sample regulatory text
    sample_text = """
    The Securities and Exchange Commission (SEC) has announced new regulations 
    regarding compliance requirements for financial institutions. These regulations 
    will take effect on January 1, 2024, and require all covered entities to 
    implement enhanced risk management procedures.
    
    Failure to comply with these requirements may result in penalties of up to 
    $1,000,000 per violation. The deadline for implementation is December 31, 2023.
    """
    
    # Initialize preprocessor
    config = PreprocessingConfig(
        remove_stopwords=True,
        lemmatize=True,
        min_word_length=2
    )
    
    preprocessor = TextPreprocessor(config)
    
    # Process text
    result = preprocessor.process_text(sample_text)
    
    # Display results
    print(f"📊 Processing Results:")
    print(f"   Original length: {result.metadata['original_length']}")
    print(f"   Cleaned length: {result.metadata['cleaned_length']}")
    print(f"   Tokens: {result.metadata['token_count']}")
    print(f"   Filtered tokens: {result.metadata['filtered_token_count']}")
    print(f"   Sentences: {result.metadata['sentence_count']}")
    print(f"   Regulatory terms: {result.metadata['regulatory_terms_found']}")
    
    print(f"\n📝 Sample tokens: {result.tokens[:10]}")
    print(f"📝 Sample sentences: {result.sentences[:2]}")
    
    print("\n✅ Text preprocessing test completed!")


if __name__ == "__main__":
    main()
