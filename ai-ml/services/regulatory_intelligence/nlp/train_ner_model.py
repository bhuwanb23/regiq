#!/usr/bin/env python3
"""
REGIQ AI/ML - Custom NER Model Trainer

Trains a custom Named Entity Recognition model specifically for regulatory documents.
Handles entities like:
- Regulatory agencies (SEC, FINRA, ESMA)
- Regulations (GDPR, SOX, Basel III)
- Compliance terms (compliance, audit, enforcement)
- Monetary penalties
- Dates and deadlines

Saves trained models with full metadata tracking.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import random

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import numpy as np

from services.regulatory_intelligence.utils.model_persistence import (
    ModelPersistence, ModelMetadata
)


class RegulatoryNERTrainer:
    """
    Custom NER model trainer for regulatory documents.
    
    Fine-tunes spaCy models on regulatory-specific entities.
    """
    
    def __init__(self, base_model: str = "en_core_web_sm"):
        """
        Initialize NER trainer.
        
        Args:
            base_model: Base spaCy model to fine-tune
        """
        self.base_model = base_model
        self.logger = self._setup_logger()
        self.nlp = None
        self.ner = None
        
        # Regulatory entity types
        self.entity_types = [
            "REGULATORY_AGENCY",    # SEC, FINRA, ESMA
            "REGULATION",           # GDPR, SOX, Basel III
            "COMPLIANCE_TERM",      # compliance, audit, enforcement
            "PENALTY_AMOUNT",       # $10 million, €5M
            "DEADLINE",            # by Q4 2024, within 90 days
            "JURISDICTION",        # EU, US, UK
            "ENTITY_TYPE",         # bank, investment firm, credit institution
        ]
        
        self.model_persister = ModelPersistence("models/nlp")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger."""
        logger = logging.getLogger('ner_trainer')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def load_base_model(self):
        """Load base spaCy model."""
        try:
            self.nlp = spacy.load(self.base_model)
            self.logger.info(f"✅ Loaded base model: {self.base_model}")
            
            # Check if NER exists
            if "ner" not in self.nlp.pipe_names:
                # Add NER component with our labels
                ner = self.nlp.add_pipe("ner")
                for label in self.entity_types:
                    ner.add_label(label)
            else:
                # Use existing NER and add new labels
                ner = self.nlp.get_pipe("ner")
                for label in self.entity_types:
                    ner.add_label(label)
            
            self.ner = ner
            self.logger.info(f"✅ Added {len(self.entity_types)} regulatory entity labels")
            
        except OSError:
            self.logger.error(f"Base model '{self.base_model}' not found")
            self.logger.error("Install with: python -m spacy download en_core_web_sm")
            raise
    
    def prepare_training_data(self, 
                             training_texts: List[str],
                             training_annotations: List[Dict]) -> List[Example]:
        """
        Prepare training data in spaCy format.
        
        Args:
            training_texts: List of text documents
            training_annotations: List of annotations with entities
            
        Returns:
            List of spaCy Example objects
        """
        examples = []
        
        for text, annotation in zip(training_texts, training_annotations):
            # Create spaCy Example
            doc = self.nlp.make_doc(text)
            example = Example.from_dict(doc, annotation)
            examples.append(example)
        
        self.logger.info(f"Prepared {len(examples)} training examples")
        return examples
    
    def train(self,
              training_data: List[Example],
              n_epochs: int = 20,
              batch_size: int = 8,
              dropout: float = 0.35,
              learning_rate: float = 0.001) -> Dict:
        """
        Train the NER model.
        
        Args:
            training_data: Training examples
            n_epochs: Number of training epochs
            batch_size: Batch size
            dropout: Dropout rate
            learning_rate: Learning rate
            
        Returns:
            Training metrics
        """
        if self.nlp is None:
            raise RuntimeError("Model not loaded. Call load_base_model() first.")
        
        self.logger.info(f"Starting training for {n_epochs} epochs...")
        
        # Initialize with a simple get_examples function
        def get_examples():
            return training_data
        
        # Initialize the pipeline
        self.nlp.initialize(get_examples=get_examples)
        
        # Get optimizer
        optimizer = self.nlp.resume_training()
        optimizer.learn_rate = learning_rate
        
        # Disable other pipes during training
        pipe_exceptions = ["ner", "trf_wordpiecer"]
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe not in pipe_exceptions]
        
        losses = {}
        metrics = {
            'epochs': [],
            'losses': [],
            'best_loss': float('inf'),
            'best_epoch': 0
        }
        
        with self.nlp.disable_pipes(*other_pipes):
            for epoch in range(n_epochs):
                random.shuffle(training_data)
                batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
                
                epoch_loss = 0.0
                n_batches = 0
                
                for batch in batches:
                    # Update model
                    self.nlp.update(
                        batch,
                        drop=dropout,
                        losses=losses,
                        sgd=optimizer
                    )
                    epoch_loss += losses.get("ner", 0.0)
                    n_batches += 1
                
                avg_loss = epoch_loss / max(n_batches, 1)
                metrics['epochs'].append(epoch + 1)
                metrics['losses'].append(avg_loss)
                
                # Track best model
                if avg_loss < metrics['best_loss']:
                    metrics['best_loss'] = avg_loss
                    metrics['best_epoch'] = epoch + 1
                
                # Log progress
                if (epoch + 1) % 5 == 0 or epoch == 0:
                    self.logger.info(
                        f"Epoch {epoch + 1}/{n_epochs} - Loss: {avg_loss:.4f}"
                    )
        
        self.logger.info(
            f"✅ Training complete! Best loss: {metrics['best_loss']:.4f} "
            f"(epoch {metrics['best_epoch']})"
        )
        
        return metrics
    
    def evaluate(self, test_data: List[Example]) -> Dict:
        """
        Evaluate model on test data.
        
        Args:
            test_data: Test examples
            
        Returns:
            Evaluation metrics
        """
        from spacy.scorer import Scorer
        
        scorer = Scorer()
        scores = scorer.score(test_data)
        
        # Extract NER-specific metrics
        ner_metrics = {
            'precision': scores.get('ents_p', 0.0),
            'recall': scores.get('ents_r', 0.0),
            'f1_score': scores.get('ents_f', 0.0),
            'accuracy': scores.get('tags_acc', 0.0)
        }
        
        self.logger.info(f"Evaluation Results:")
        self.logger.info(f"  Precision: {ner_metrics['precision']:.4f}")
        self.logger.info(f"  Recall:    {ner_metrics['recall']:.4f}")
        self.logger.info(f"  F1-Score:  {ner_metrics['f1_score']:.4f}")
        
        return ner_metrics
    
    def save_model(self, 
                   model_name: str = "regulatory_ner",
                   version: str = "1.0.0",
                   training_samples: int = 0,
                   evaluation_metrics: Dict = None) -> Path:
        """
        Save trained model with metadata.
        
        Args:
            model_name: Name for the saved model
            version: Model version
            training_samples: Number of training samples used
            evaluation_metrics: Evaluation metrics
            
        Returns:
            Path to saved model
        """
        if self.nlp is None:
            raise RuntimeError("No model to save")
        
        # Create metadata
        metadata = ModelMetadata(
            model_name=model_name,
            model_type="spacy",
            version=version,
            created_at="",  # Will be set by persister
            training_samples=training_samples,
            features=self.entity_types,
            metrics=evaluation_metrics or {},
            config={
                'base_model': self.base_model,
                'entity_types': self.entity_types,
                'architecture': 'spaCy_transformer'
            },
            checksum="",  # Will be calculated
            file_size=0,  # Will be calculated
            description=f"Custom NER model for regulatory document analysis",
            tags=["regulatory", "ner", "compliance", "finance"]
        )
        
        # Save model
        saved_path = self.model_persister.save(
            model=self.nlp,
            model_name=model_name,
            metadata=metadata
        )
        
        self.logger.info(f"✅ Model saved to {saved_path}")
        return saved_path
    
    def load_model(self, model_name: str = "regulatory_ner") -> spacy.Language:
        """
        Load a saved NER model.
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            Loaded spaCy model
        """
        try:
            loaded_nlp = self.model_persister.load(model_name, model_type="spacy")
            self.logger.info(f"✅ Loaded model '{model_name}'")
            return loaded_nlp
        except FileNotFoundError:
            self.logger.error(f"Model '{model_name}' not found")
            raise


def create_sample_training_data() -> Tuple[List[str], List[Dict]]:
    """
    Create sample training data for demonstration.
    
    Returns:
        Tuple of (texts, annotations)
    """
    texts = [
        "The SEC announced new compliance requirements for investment firms under SOX Section 404.",
        "FINRA fined the bank $5 million for violations of anti-money laundering regulations.",
        "Under GDPR Article 17, organizations must respond to data deletion requests within 30 days.",
        "Basel III capital requirements mandate a minimum leverage ratio of 3%.",
        "The European Banking Authority issued guidelines on IT security and cloud outsourcing.",
        "Compliance officers must ensure adherence to Dodd-Frank Act provisions by Q4 2024.",
        "The Financial Conduct Authority requires enhanced due diligence for high-risk customers.",
        "Penalties for non-compliance can reach up to €20 million or 4% of global annual turnover.",
        "Credit institutions must implement robust AML/KYC procedures according to FinCEN guidelines.",
        "The Prudential Regulation Authority conducts regular stress tests on major banks."
    ]
    
    annotations = [
        {
            "entities": [
                (0, 3, "REGULATORY_AGENCY"),  # SEC
                (60, 64, "REGULATION"),  # SOX
            ]
        },
        {
            "entities": [
                (0, 6, "REGULATORY_AGENCY"),  # FINRA
                (17, 25, "PENALTY_AMOUNT"),  # $5 million
                (55, 85, "REGULATION"),  # anti-money laundering regulations
            ]
        },
        {
            "entities": [
                (5, 9, "REGULATION"),  # GDPR
                (68, 80, "DEADLINE"),  # within 30 days
            ]
        },
        {
            "entities": [
                (0, 8, "REGULATION"),  # Basel III
            ]
        },
        {
            "entities": [
                (4, 28, "REGULATORY_AGENCY"),  # European Banking Authority
            ]
        },
        {
            "entities": [
                (66, 78, "DEADLINE"),  # by Q4 2024
                (42, 52, "REGULATION"),  # Dodd-Frank
            ]
        },
        {
            "entities": [
                (4, 25, "REGULATORY_AGENCY"),  # Financial Conduct Authority
            ]
        },
        {
            "entities": [
                (32, 48, "PENALTY_AMOUNT"),  # €20 million
            ]
        },
        {
            "entities": [
                (70, 76, "REGULATORY_AGENCY"),  # FinCEN
            ]
        },
        {
            "entities": [
                (4, 33, "REGULATORY_AGENCY"),  # Prudential Regulation Authority
            ]
        }
    ]
    
    return texts, annotations


def main():
    """Main training function."""
    print("=" * 60)
    print("REGIQ - Regulatory NER Model Training")
    print("=" * 60)
    
    # Initialize trainer
    trainer = RegulatoryNERTrainer(base_model="en_core_web_sm")
    
    # Load base model
    print("\n📚 Loading base model...")
    trainer.load_base_model()
    
    # Create sample training data
    print("\n📝 Preparing training data...")
    texts, annotations = create_sample_training_data()
    training_examples = trainer.prepare_training_data(texts, annotations)
    
    # Train model
    print("\n🔧 Training model...")
    training_metrics = trainer.train(
        training_data=training_examples,
        n_epochs=20,
        batch_size=4,
        dropout=0.35
    )
    
    # Evaluate (using same data for demo - should use separate test set)
    print("\n📊 Evaluating model...")
    eval_metrics = trainer.evaluate(training_examples)
    
    # Save model
    print("\n💾 Saving model...")
    saved_path = trainer.save_model(
        model_name="regulatory_ner",
        version="1.0.0",
        training_samples=len(training_examples),
        evaluation_metrics=eval_metrics
    )
    
    # List available models
    print("\n📋 Available models:")
    persister = ModelPersistence("models/nlp")
    models = persister.list_models()
    for model in models:
        print(f"  - {model['name']} ({model['type']}) v{model['version']}")
    
    print("\n✅ Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
