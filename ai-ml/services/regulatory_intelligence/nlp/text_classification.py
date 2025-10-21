#!/usr/bin/env python3
"""
REGIQ AI/ML - Text Classification Module
Advanced text classification for regulatory documents.
Classifies regulation types, compliance categories, risk levels, and urgency.
"""

import os
import sys
import logging
import pickle
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import json

# ML Libraries
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib

# NLP Libraries
import spacy
from transformers import pipeline

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.env_config import get_env_config


@dataclass
class ClassificationResult:
    """Text classification result."""
    regulation_type: str
    compliance_category: str
    risk_level: str
    urgency_level: str
    confidence_scores: Dict[str, float]
    metadata: Dict[str, Any]


@dataclass
class ClassificationConfig:
    """Configuration for text classification."""
    model_type: str = "logistic_regression"  # logistic_regression, random_forest, naive_bayes
    use_transformer: bool = False
    confidence_threshold: float = 0.7
    max_features: int = 10000
    n_estimators: int = 100  # For Random Forest


class RegulatoryTextClassifier:
    """
    Advanced text classification for regulatory documents.
    Classifies regulation types, compliance categories, risk levels, and urgency.
    """
    
    def __init__(self, config: ClassificationConfig = None):
        """Initialize text classifier."""
        self.env_config = get_env_config()
        self.config = config or ClassificationConfig()
        self.logger = self._setup_logging()
        
        # Initialize models
        self._initialize_models()
        
        # Setup classification categories
        self._setup_classification_categories()
        
        # Initialize transformer pipeline if enabled
        if self.config.use_transformer:
            self._initialize_transformer_pipeline()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for text classifier."""
        logger = logging.getLogger('text_classifier')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_models(self):
        """Initialize classification models."""
        self.models = {}
        self.vectorizers = {}
        
        # Initialize spaCy for text preprocessing
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.logger.info("✅ spaCy model loaded for classification")
        except OSError:
            self.logger.warning("⚠️  spaCy model not found, using basic preprocessing")
            self.nlp = None
    
    def _initialize_transformer_pipeline(self):
        """Initialize transformer pipeline for classification."""
        try:
            self.transformer_pipeline = pipeline(
                "text-classification",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=True
            )
            self.logger.info("✅ Transformer pipeline initialized")
        except Exception as e:
            self.logger.warning(f"⚠️  Transformer pipeline failed: {e}")
            self.transformer_pipeline = None
    
    def _setup_classification_categories(self):
        """Setup classification categories and training data."""
        
        # Regulation types
        self.regulation_types = {
            'SECURITIES': [
                'securities regulation', 'SEC filing', '10-K', '10-Q', '8-K',
                'proxy statement', 'insider trading', 'market manipulation'
            ],
            'BANKING': [
                'banking regulation', 'capital requirements', 'liquidity rules',
                'Basel III', 'stress testing', 'CCAR', 'banking supervision'
            ],
            'PRIVACY': [
                'privacy regulation', 'GDPR', 'CCPA', 'data protection',
                'personal information', 'consent management', 'privacy policy'
            ],
            'ANTI_MONEY_LAUNDERING': [
                'AML', 'anti-money laundering', 'KYC', 'suspicious activity',
                'money laundering', 'terrorist financing', 'BSA'
            ],
            'MARKET_CONDUCT': [
                'market conduct', 'best execution', 'fiduciary duty',
                'conflicts of interest', 'market abuse', 'insider dealing'
            ],
            'CYBERSECURITY': [
                'cybersecurity', 'information security', 'data breach',
                'cyber risk', 'IT security', 'network security'
            ]
        }
        
        # Compliance categories
        self.compliance_categories = {
            'REPORTING': [
                'reporting requirement', 'filing deadline', 'disclosure',
                'quarterly report', 'annual report', 'regulatory filing'
            ],
            'OPERATIONAL': [
                'operational compliance', 'internal controls', 'procedures',
                'process improvement', 'operational risk', 'business process'
            ],
            'TECHNICAL': [
                'technical compliance', 'system requirements', 'IT compliance',
                'data management', 'system integration', 'technical standards'
            ],
            'LEGAL': [
                'legal compliance', 'regulatory change', 'legal requirement',
                'statutory compliance', 'regulatory update', 'legal obligation'
            ],
            'RISK_MANAGEMENT': [
                'risk management', 'risk assessment', 'risk mitigation',
                'risk monitoring', 'risk framework', 'risk controls'
            ]
        }
        
        # Risk levels
        self.risk_levels = {
            'LOW': [
                'low risk', 'minimal impact', 'routine compliance',
                'standard procedure', 'low priority', 'minor violation'
            ],
            'MEDIUM': [
                'medium risk', 'moderate impact', 'significant compliance',
                'important requirement', 'medium priority', 'substantial violation'
            ],
            'HIGH': [
                'high risk', 'significant impact', 'critical compliance',
                'major requirement', 'high priority', 'serious violation'
            ],
            'CRITICAL': [
                'critical risk', 'severe impact', 'urgent compliance',
                'immediate requirement', 'critical priority', 'major violation'
            ]
        }
        
        # Urgency levels
        self.urgency_levels = {
            'LOW': [
                'no immediate action', 'routine update', 'standard timeline',
                'normal priority', 'low urgency', 'flexible deadline'
            ],
            'MEDIUM': [
                'moderate urgency', 'important timeline', 'significant priority',
                'medium urgency', 'reasonable deadline', 'important action'
            ],
            'HIGH': [
                'high urgency', 'immediate attention', 'urgent priority',
                'quick action', 'tight deadline', 'urgent requirement'
            ],
            'CRITICAL': [
                'critical urgency', 'immediate action', 'emergency priority',
                'urgent deadline', 'critical timeline', 'emergency requirement'
            ]
        }
    
    def _create_training_data(self):
        """Create training data for classification models."""
        training_data = {
            'regulation_type': [],
            'compliance_category': [],
            'risk_level': [],
            'urgency_level': []
        }
        
        # Create training examples for each category
        for category, examples in self.regulation_types.items():
            for example in examples:
                training_data['regulation_type'].append((example, category))
        
        for category, examples in self.compliance_categories.items():
            for example in examples:
                training_data['compliance_category'].append((example, category))
        
        for level, examples in self.risk_levels.items():
            for example in examples:
                training_data['risk_level'].append((example, level))
        
        for level, examples in self.urgency_levels.items():
            for example in examples:
                training_data['urgency_level'].append((example, level))
        
        return training_data
    
    def _train_model(self, training_data: List[Tuple[str, str]], model_name: str):
        """Train a classification model."""
        if not training_data:
            self.logger.warning(f"No training data for {model_name}")
            return None
        
        texts, labels = zip(*training_data)
        
        # Create vectorizer
        vectorizer = TfidfVectorizer(
            max_features=self.config.max_features,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Create model based on config
        if self.config.model_type == "logistic_regression":
            model = LogisticRegression(random_state=42, max_iter=1000)
        elif self.config.model_type == "random_forest":
            model = RandomForestClassifier(
                n_estimators=self.config.n_estimators,
                random_state=42
            )
        elif self.config.model_type == "naive_bayes":
            model = MultinomialNB()
        else:
            model = LogisticRegression(random_state=42, max_iter=1000)
        
        # Create pipeline
        pipeline_model = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', model)
        ])
        
        # Train model
        pipeline_model.fit(texts, labels)
        
        # Store model and vectorizer
        self.models[model_name] = pipeline_model
        self.vectorizers[model_name] = vectorizer
        
        self.logger.info(f"✅ {model_name} model trained successfully")
        return pipeline_model
    
    def train_all_models(self):
        """Train all classification models."""
        self.logger.info("🎓 Training all classification models")
        
        # Create training data
        training_data = self._create_training_data()
        
        # Train each model
        for model_name, data in training_data.items():
            self._train_model(data, model_name)
        
        self.logger.info("✅ All models trained successfully")
    
    def _classify_with_rule_based(self, text: str) -> Dict[str, str]:
        """Classify text using rule-based approach."""
        text_lower = text.lower()
        
        # Regulation type classification
        regulation_type = 'UNKNOWN'
        max_matches = 0
        for reg_type, keywords in self.regulation_types.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            if matches > max_matches:
                max_matches = matches
                regulation_type = reg_type
        
        # Compliance category classification
        compliance_category = 'UNKNOWN'
        max_matches = 0
        for category, keywords in self.compliance_categories.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            if matches > max_matches:
                max_matches = matches
                compliance_category = category
        
        # Risk level classification
        risk_level = 'LOW'
        max_matches = 0
        for level, keywords in self.risk_levels.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            if matches > max_matches:
                max_matches = matches
                risk_level = level
        
        # Urgency level classification
        urgency_level = 'LOW'
        max_matches = 0
        for level, keywords in self.urgency_levels.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            if matches > max_matches:
                max_matches = matches
                urgency_level = level
        
        return {
            'regulation_type': regulation_type,
            'compliance_category': compliance_category,
            'risk_level': risk_level,
            'urgency_level': urgency_level
        }
    
    def _classify_with_ml_models(self, text: str) -> Dict[str, Tuple[str, float]]:
        """Classify text using trained ML models."""
        results = {}
        
        for model_name, model in self.models.items():
            try:
                # Get prediction and probability
                prediction = model.predict([text])[0]
                probabilities = model.predict_proba([text])[0]
                confidence = max(probabilities)
                
                results[model_name] = (prediction, confidence)
            except Exception as e:
                self.logger.error(f"Error in {model_name} classification: {e}")
                results[model_name] = ('UNKNOWN', 0.0)
        
        return results
    
    def _classify_with_transformer(self, text: str) -> Dict[str, str]:
        """Classify text using transformer model."""
        if not hasattr(self, 'transformer_pipeline') or not self.transformer_pipeline:
            return {}
        
        try:
            # Use transformer for sentiment analysis as proxy for urgency/risk
            results = self.transformer_pipeline(text)
            
            # Map sentiment to urgency/risk
            sentiment = results[0]['label']
            confidence = results[0]['score']
            
            if sentiment == 'POSITIVE':
                urgency = 'LOW'
                risk = 'LOW'
            elif sentiment == 'NEGATIVE':
                urgency = 'HIGH'
                risk = 'HIGH'
            else:
                urgency = 'MEDIUM'
                risk = 'MEDIUM'
            
            return {
                'urgency_level': urgency,
                'risk_level': risk
            }
        except Exception as e:
            self.logger.error(f"Transformer classification error: {e}")
            return {}
    
    def classify_text(self, text: str) -> ClassificationResult:
        """
        Classify text for regulation type, compliance category, risk level, and urgency.
        
        Args:
            text: Text to classify
            
        Returns:
            Classification result
        """
        self.logger.info("🔍 Starting text classification")
        
        # Rule-based classification
        rule_based_results = self._classify_with_rule_based(text)
        
        # ML model classification
        ml_results = {}
        if self.models:
            ml_results = self._classify_with_ml_models(text)
        
        # Transformer classification
        transformer_results = {}
        if hasattr(self, 'transformer_pipeline') and self.transformer_pipeline:
            transformer_results = self._classify_with_transformer(text)
        
        # Combine results
        final_results = rule_based_results.copy()
        confidence_scores = {}
        
        # Update with ML results if available
        for model_name, (prediction, confidence) in ml_results.items():
            if confidence > self.config.confidence_threshold:
                final_results[model_name] = prediction
                confidence_scores[model_name] = confidence
        
        # Update with transformer results if available
        for key, value in transformer_results.items():
            if key in final_results:
                final_results[key] = value
                confidence_scores[key] = 0.8  # Default confidence for transformer
        
        # Create metadata
        metadata = {
            'classification_method': 'hybrid',
            'rule_based_results': rule_based_results,
            'ml_results': ml_results,
            'transformer_results': transformer_results,
            'processing_timestamp': datetime.now().isoformat()
        }
        
        result = ClassificationResult(
            regulation_type=final_results.get('regulation_type', 'UNKNOWN'),
            compliance_category=final_results.get('compliance_category', 'UNKNOWN'),
            risk_level=final_results.get('risk_level', 'LOW'),
            urgency_level=final_results.get('urgency_level', 'LOW'),
            confidence_scores=confidence_scores,
            metadata=metadata
        )
        
        self.logger.info(f"✅ Text classification completed: {result.regulation_type}, {result.risk_level}")
        
        return result
    
    def save_models(self, model_dir: str = "models/nlp_classification"):
        """Save trained models to disk."""
        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)
        
        for model_name, model in self.models.items():
            model_file = model_path / f"{model_name}_model.pkl"
            joblib.dump(model, model_file)
            self.logger.info(f"💾 {model_name} model saved to {model_file}")
    
    def load_models(self, model_dir: str = "models/nlp_classification"):
        """Load trained models from disk."""
        model_path = Path(model_dir)
        
        for model_file in model_path.glob("*_model.pkl"):
            model_name = model_file.stem.replace("_model", "")
            try:
                model = joblib.load(model_file)
                self.models[model_name] = model
                self.logger.info(f"📂 {model_name} model loaded from {model_file}")
            except Exception as e:
                self.logger.error(f"Error loading {model_name} model: {e}")


def main():
    """Test the text classification module."""
    print("🧪 Testing Text Classification Module")
    print("="*50)
    
    # Sample regulatory texts
    sample_texts = [
        "The SEC has issued new regulations requiring immediate compliance with enhanced reporting requirements for all financial institutions.",
        "GDPR compliance deadline is approaching for data protection requirements in the European Union.",
        "Banking institutions must implement Basel III capital requirements by the end of the fiscal year."
    ]
    
    # Initialize classifier
    config = ClassificationConfig(
        model_type="logistic_regression",
        use_transformer=False
    )
    
    classifier = RegulatoryTextClassifier(config)
    
    # Train models
    classifier.train_all_models()
    
    # Classify texts
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📄 Sample Text {i}:")
        print(f"   {text[:100]}...")
        
        result = classifier.classify_text(text)
        
        print(f"   📊 Classification Results:")
        print(f"      Regulation Type: {result.regulation_type}")
        print(f"      Compliance Category: {result.compliance_category}")
        print(f"      Risk Level: {result.risk_level}")
        print(f"      Urgency Level: {result.urgency_level}")
        print(f"      Confidence Scores: {result.confidence_scores}")
    
    print("\n✅ Text classification test completed!")


if __name__ == "__main__":
    main()
