#!/usr/bin/env python3
"""
REGIQ AI/ML - Entity Recognition Module
Advanced entity recognition for regulatory documents.
Extracts regulatory entities, dates, deadlines, and penalty amounts.
"""

import os
import sys
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

# NLP Libraries
import spacy
from spacy import displacy
import dateutil.parser
from dateutil.relativedelta import relativedelta

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.env_config import get_env_config


@dataclass
class RegulatoryEntity:
    """Regulatory entity data structure."""
    text: str
    label: str
    start: int
    end: int
    confidence: float
    context: str = None
    metadata: Dict[str, Any] = None


@dataclass
class DateEntity:
    """Date entity data structure."""
    text: str
    parsed_date: datetime
    start: int
    end: int
    confidence: float
    is_deadline: bool = False
    context: str = None


@dataclass
class PenaltyEntity:
    """Penalty amount entity data structure."""
    text: str
    amount: float
    currency: str
    start: int
    end: int
    confidence: float
    context: str = None


@dataclass
class EntityRecognitionResult:
    """Complete entity recognition result."""
    regulatory_entities: List[RegulatoryEntity]
    date_entities: List[DateEntity]
    penalty_entities: List[PenaltyEntity]
    all_entities: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class RegulatoryEntityRecognizer:
    """
    Advanced entity recognition for regulatory documents.
    Extracts regulatory entities, dates, deadlines, and penalty amounts.
    """
    
    def __init__(self):
        """Initialize entity recognizer."""
        self.env_config = get_env_config()
        self.logger = self._setup_logging()
        
        # Initialize spaCy model
        self._initialize_spacy_model()
        
        # Regulatory entity patterns
        self._setup_regulatory_patterns()
        
        # Date patterns
        self._setup_date_patterns()
        
        # Penalty patterns
        self._setup_penalty_patterns()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for entity recognizer."""
        logger = logging.getLogger('entity_recognizer')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_spacy_model(self):
        """Initialize spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.logger.info("✅ spaCy model loaded successfully")
        except OSError:
            try:
                self.nlp = spacy.load("en_core_web_md")
                self.logger.info("✅ spaCy medium model loaded successfully")
            except OSError:
                self.logger.error("❌ No spaCy model found. Please install: python -m spacy download en_core_web_sm")
                self.nlp = None
    
    def _setup_regulatory_patterns(self):
        """Setup regulatory entity patterns."""
        # Regulatory agencies
        self.regulatory_agencies = {
            'SEC': ['Securities and Exchange Commission', 'SEC'],
            'CFTC': ['Commodity Futures Trading Commission', 'CFTC'],
            'FDIC': ['Federal Deposit Insurance Corporation', 'FDIC'],
            'FINRA': ['Financial Industry Regulatory Authority', 'FINRA'],
            'ESMA': ['European Securities and Markets Authority', 'ESMA'],
            'EBA': ['European Banking Authority', 'EBA'],
            'ECB': ['European Central Bank', 'ECB'],
            'FCA': ['Financial Conduct Authority', 'FCA'],
            'PRA': ['Prudential Regulation Authority', 'PRA']
        }
        
        # Regulatory frameworks
        self.regulatory_frameworks = {
            'GDPR': ['General Data Protection Regulation', 'GDPR'],
            'SOX': ['Sarbanes-Oxley Act', 'SOX', 'Sarbanes-Oxley'],
            'Basel': ['Basel III', 'Basel II', 'Basel I', 'Basel'],
            'MiFID': ['Markets in Financial Instruments Directive', 'MiFID'],
            'Dodd-Frank': ['Dodd-Frank Act', 'Dodd-Frank'],
            'CCPA': ['California Consumer Privacy Act', 'CCPA']
        }
        
        # Compliance terms
        self.compliance_terms = [
            'compliance', 'regulatory', 'supervision', 'oversight',
            'violation', 'breach', 'penalty', 'fine', 'sanction',
            'requirement', 'mandate', 'obligation', 'deadline',
            'audit', 'examination', 'enforcement', 'investigation'
        ]
    
    def _setup_date_patterns(self):
        """Setup date extraction patterns."""
        # Date patterns
        self.date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY/MM/DD or YYYY-MM-DD
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2},?\s+\d{4}\b',  # Mon DD, YYYY
            r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{4}\b'  # DD Mon YYYY
        ]
        
        # Deadline indicators
        self.deadline_indicators = [
            'deadline', 'due date', 'expires', 'expiration',
            'must be completed by', 'required by', 'effective date',
            'implementation date', 'compliance date'
        ]
    
    def _setup_penalty_patterns(self):
        """Setup penalty amount extraction patterns."""
        # Currency symbols and codes
        self.currency_patterns = [
            r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $1,000,000.00
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*dollars?',  # 1,000,000.00 dollars
            r'€(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # €1,000,000.00
            r'£(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # £1,000,000.00
            r'¥(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # ¥1,000,000.00
        ]
        
        # Penalty indicators
        self.penalty_indicators = [
            'penalty', 'fine', 'sanction', 'monetary penalty',
            'civil penalty', 'administrative penalty', 'criminal penalty',
            'forfeiture', 'disgorgement', 'restitution'
        ]
    
    def extract_regulatory_entities(self, text: str) -> List[RegulatoryEntity]:
        """
        Extract regulatory entities from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of regulatory entities
        """
        entities = []
        
        if not self.nlp:
            self.logger.warning("⚠️  spaCy model not available, using pattern matching")
            return self._extract_entities_pattern_based(text)
        
        doc = self.nlp(text)
        
        # Extract using spaCy NER
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PERSON', 'GPE']:
                # Check if it's a regulatory entity
                if self._is_regulatory_entity(ent.text):
                    entity = RegulatoryEntity(
                        text=ent.text,
                        label=ent.label_,
                        start=ent.start_char,
                        end=ent.end_char,
                        confidence=0.8,  # Default confidence for spaCy
                        context=self._get_context(text, ent.start_char, ent.end_char),
                        metadata={'source': 'spacy_ner'}
                    )
                    entities.append(entity)
        
        # Extract using pattern matching
        pattern_entities = self._extract_entities_pattern_based(text)
        entities.extend(pattern_entities)
        
        # Remove duplicates
        entities = self._remove_duplicate_entities(entities)
        
        return entities
    
    def _extract_entities_pattern_based(self, text: str) -> List[RegulatoryEntity]:
        """Extract entities using pattern matching."""
        entities = []
        
        # Extract regulatory agencies
        for agency, variations in self.regulatory_agencies.items():
            for variation in variations:
                pattern = re.compile(re.escape(variation), re.IGNORECASE)
                for match in pattern.finditer(text):
                    entity = RegulatoryEntity(
                        text=match.group(),
                        label='REGULATORY_AGENCY',
                        start=match.start(),
                        end=match.end(),
                        confidence=0.9,
                        context=self._get_context(text, match.start(), match.end()),
                        metadata={'agency': agency, 'source': 'pattern_matching'}
                    )
                    entities.append(entity)
        
        # Extract regulatory frameworks
        for framework, variations in self.regulatory_frameworks.items():
            for variation in variations:
                pattern = re.compile(re.escape(variation), re.IGNORECASE)
                for match in pattern.finditer(text):
                    entity = RegulatoryEntity(
                        text=match.group(),
                        label='REGULATORY_FRAMEWORK',
                        start=match.start(),
                        end=match.end(),
                        confidence=0.9,
                        context=self._get_context(text, match.start(), match.end()),
                        metadata={'framework': framework, 'source': 'pattern_matching'}
                    )
                    entities.append(entity)
        
        return entities
    
    def _is_regulatory_entity(self, text: str) -> bool:
        """Check if text is a regulatory entity."""
        text_lower = text.lower()
        
        # Check against known regulatory terms
        for agency_variations in self.regulatory_agencies.values():
            if any(term.lower() in text_lower for term in agency_variations):
                return True
        
        for framework_variations in self.regulatory_frameworks.values():
            if any(term.lower() in text_lower for term in framework_variations):
                return True
        
        return any(term.lower() in text_lower for term in self.compliance_terms)
    
    def extract_dates(self, text: str) -> List[DateEntity]:
        """
        Extract dates from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of date entities
        """
        dates = []
        
        # Extract using pattern matching
        for pattern in self.date_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                try:
                    parsed_date = dateutil.parser.parse(match.group())
                    
                    # Check if it's a deadline
                    is_deadline = self._is_deadline(text, match.start(), match.end())
                    
                    date_entity = DateEntity(
                        text=match.group(),
                        parsed_date=parsed_date,
                        start=match.start(),
                        end=match.end(),
                        confidence=0.8,
                        is_deadline=is_deadline,
                        context=self._get_context(text, match.start(), match.end())
                    )
                    dates.append(date_entity)
                    
                except Exception as e:
                    self.logger.debug(f"Failed to parse date '{match.group()}': {e}")
        
        # Use spaCy if available
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == 'DATE':
                    try:
                        parsed_date = dateutil.parser.parse(ent.text)
                        is_deadline = self._is_deadline(text, ent.start_char, ent.end_char)
                        
                        date_entity = DateEntity(
                            text=ent.text,
                            parsed_date=parsed_date,
                            start=ent.start_char,
                            end=ent.end_char,
                            confidence=0.9,
                            is_deadline=is_deadline,
                            context=self._get_context(text, ent.start_char, ent.end_char),
                            metadata={'source': 'spacy_ner'}
                        )
                        dates.append(date_entity)
                        
                    except Exception as e:
                        self.logger.debug(f"Failed to parse spaCy date '{ent.text}': {e}")
        
        # Remove duplicates
        dates = self._remove_duplicate_dates(dates)
        
        return dates
    
    def _is_deadline(self, text: str, start: int, end: int) -> bool:
        """Check if a date is a deadline."""
        # Get context around the date
        context_start = max(0, start - 50)
        context_end = min(len(text), end + 50)
        context = text[context_start:context_end].lower()
        
        # Check for deadline indicators
        return any(indicator in context for indicator in self.deadline_indicators)
    
    def extract_penalties(self, text: str) -> List[PenaltyEntity]:
        """
        Extract penalty amounts from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of penalty entities
        """
        penalties = []
        
        # Extract using pattern matching
        for pattern in self.currency_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Check if it's in a penalty context
                if self._is_penalty_context(text, match.start(), match.end()):
                    try:
                        amount = float(match.group(1).replace(',', ''))
                        currency = self._extract_currency(match.group())
                        
                        penalty_entity = PenaltyEntity(
                            text=match.group(),
                            amount=amount,
                            currency=currency,
                            start=match.start(),
                            end=match.end(),
                            confidence=0.8,
                            context=self._get_context(text, match.start(), match.end())
                        )
                        penalties.append(penalty_entity)
                        
                    except Exception as e:
                        self.logger.debug(f"Failed to parse penalty amount '{match.group()}': {e}")
        
        return penalties
    
    def _is_penalty_context(self, text: str, start: int, end: int) -> bool:
        """Check if amount is in a penalty context."""
        # Get context around the amount
        context_start = max(0, start - 100)
        context_end = min(len(text), end + 100)
        context = text[context_start:context_end].lower()
        
        # Check for penalty indicators
        return any(indicator in context for indicator in self.penalty_indicators)
    
    def _extract_currency(self, text: str) -> str:
        """Extract currency from text."""
        if '$' in text:
            return 'USD'
        elif '€' in text:
            return 'EUR'
        elif '£' in text:
            return 'GBP'
        elif '¥' in text:
            return 'JPY'
        else:
            return 'USD'  # Default
    
    def _get_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Get context around an entity."""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end].strip()
    
    def _remove_duplicate_entities(self, entities: List[RegulatoryEntity]) -> List[RegulatoryEntity]:
        """Remove duplicate entities."""
        seen = set()
        unique_entities = []
        
        for entity in entities:
            key = (entity.text.lower(), entity.start, entity.end)
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities
    
    def _remove_duplicate_dates(self, dates: List[DateEntity]) -> List[DateEntity]:
        """Remove duplicate dates."""
        seen = set()
        unique_dates = []
        
        for date in dates:
            key = (date.text.lower(), date.start, date.end)
            if key not in seen:
                seen.add(key)
                unique_dates.append(date)
        
        return unique_dates
    
    def recognize_entities(self, text: str) -> EntityRecognitionResult:
        """
        Complete entity recognition pipeline.
        
        Args:
            text: Text to analyze
            
        Returns:
            Complete entity recognition result
        """
        self.logger.info("🔍 Starting entity recognition")
        
        # Extract all entity types
        regulatory_entities = self.extract_regulatory_entities(text)
        date_entities = self.extract_dates(text)
        penalty_entities = self.extract_penalties(text)
        
        # Combine all entities
        all_entities = []
        for entity in regulatory_entities:
            all_entities.append({
                'text': entity.text,
                'label': entity.label,
                'start': entity.start,
                'end': entity.end,
                'confidence': entity.confidence,
                'type': 'regulatory',
                'context': entity.context
            })
        
        for entity in date_entities:
            all_entities.append({
                'text': entity.text,
                'label': 'DATE',
                'start': entity.start,
                'end': entity.end,
                'confidence': entity.confidence,
                'type': 'date',
                'is_deadline': entity.is_deadline,
                'parsed_date': entity.parsed_date.isoformat(),
                'context': entity.context
            })
        
        for entity in penalty_entities:
            all_entities.append({
                'text': entity.text,
                'label': 'MONEY',
                'start': entity.start,
                'end': entity.end,
                'confidence': entity.confidence,
                'type': 'penalty',
                'amount': entity.amount,
                'currency': entity.currency,
                'context': entity.context
            })
        
        # Create metadata
        metadata = {
            'total_entities': len(all_entities),
            'regulatory_entities': len(regulatory_entities),
            'date_entities': len(date_entities),
            'penalty_entities': len(penalty_entities),
            'deadlines': len([d for d in date_entities if d.is_deadline]),
            'processing_timestamp': datetime.now().isoformat()
        }
        
        result = EntityRecognitionResult(
            regulatory_entities=regulatory_entities,
            date_entities=date_entities,
            penalty_entities=penalty_entities,
            all_entities=all_entities,
            metadata=metadata
        )
        
        self.logger.info(f"✅ Entity recognition completed: {len(all_entities)} entities found")
        
        return result


def main():
    """Test the entity recognition module."""
    print("🧪 Testing Entity Recognition Module")
    print("="*50)
    
    # Sample regulatory text
    sample_text = """
    The Securities and Exchange Commission (SEC) has announced new regulations 
    under the Dodd-Frank Act that will take effect on January 1, 2024. 
    Financial institutions must comply with these requirements by December 31, 2023.
    
    Failure to comply may result in penalties of up to $1,000,000 per violation.
    The European Securities and Markets Authority (ESMA) has similar requirements
    under MiFID II with a deadline of March 15, 2024.
    """
    
    # Initialize recognizer
    recognizer = RegulatoryEntityRecognizer()
    
    # Extract entities
    result = recognizer.recognize_entities(sample_text)
    
    # Display results
    print(f"📊 Recognition Results:")
    print(f"   Total entities: {result.metadata['total_entities']}")
    print(f"   Regulatory entities: {result.metadata['regulatory_entities']}")
    print(f"   Date entities: {result.metadata['date_entities']}")
    print(f"   Penalty entities: {result.metadata['penalty_entities']}")
    print(f"   Deadlines: {result.metadata['deadlines']}")
    
    print(f"\n🏛️ Regulatory Entities:")
    for entity in result.regulatory_entities:
        print(f"   - {entity.text} ({entity.label}) - {entity.context}")
    
    print(f"\n📅 Dates:")
    for date in result.date_entities:
        deadline_text = " (DEADLINE)" if date.is_deadline else ""
        print(f"   - {date.text} -> {date.parsed_date.strftime('%Y-%m-%d')}{deadline_text}")
    
    print(f"\n💰 Penalties:")
    for penalty in result.penalty_entities:
        print(f"   - {penalty.text} ({penalty.currency})")
    
    print("\n✅ Entity recognition test completed!")


if __name__ == "__main__":
    main()
