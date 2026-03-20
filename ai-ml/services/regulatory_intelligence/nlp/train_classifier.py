#!/usr/bin/env python3
"""
REGIQ AI/ML - Text Classification Model Trainer

Trains custom text classification models for regulatory document categorization.
Supports multiple classification tasks:
- Regulation type detection
- Compliance category classification
- Risk level assessment
- Urgency classification

Includes automatic model selection, hyperparameter tuning, and persistence.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
from datetime import datetime
import pickle

# Add project root
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    classification_report, accuracy_score, 
    precision_recall_fscore_support, confusion_matrix
)
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
import joblib

from services.regulatory_intelligence.utils.model_persistence import (
    ModelPersistence, ModelMetadata
)


class RegulatoryTextClassifierTrainer:
    """
    Custom text classifier trainer for regulatory documents.
    
    Supports multiple classification tasks with automatic model selection.
    """
    
    def __init__(self):
        """Initialize classifier trainer."""
        self.logger = self._setup_logger()
        self.models = {}
        self.vectorizers = {}
        self.label_encoders = {}
        
        self.model_persister = ModelPersistence("models/nlp")
        
        # Available classifiers
        self.classifiers = {
            'logistic_regression': LogisticRegression(
                max_iter=1000,
                random_state=42,
                n_jobs=-1
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                random_state=42
            ),
            'naive_bayes': MultinomialNB(),
            'svm': SVC(kernel='rbf', probability=True, random_state=42)
        }
        
        # TF-IDF vectorizer configurations
        self.vectorizer_configs = {
            'default': TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8,
                sublinear_tf=True
            ),
            'lightweight': TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 1),
                min_df=1,
                max_df=0.9
            ),
            'advanced': TfidfVectorizer(
                max_features=15000,
                ngram_range=(1, 3),
                min_df=1,
                max_df=0.7,
                sublinear_tf=True,
                use_idf=True,
                smooth_idf=True
            )
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger."""
        logger = logging.getLogger('classifier_trainer')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def prepare_data(self,
                    texts: List[str],
                    labels: Union[List[str], List[List[str]]],
                    task_name: str) -> Tuple:
        """
        Prepare training data.
        
        Args:
            texts: Input texts
            labels: Labels (single or multi-label)
            task_name: Name of the classification task
            
        Returns:
            Prepared data splits
        """
        self.logger.info(f"Preparing data for task: {task_name}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels if len(set(labels)) > 1 else None
        )
        
        self.logger.info(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
        
        return X_train, X_test, y_train, y_test
    
    def train_classifier(self,
                        X_train: List[str],
                        y_train: List,
                        X_test: List[str],
                        y_test: List,
                        task_name: str,
                        classifier_type: str = 'logistic_regression',
                        vectorizer_type: str = 'default',
                        tune_hyperparameters: bool = False) -> Dict:
        """
        Train a text classifier.
        
        Args:
            X_train: Training texts
            y_train: Training labels
            X_test: Test texts
            y_test: Test labels
            task_name: Name of classification task
            classifier_type: Type of classifier to use
            vectorizer_type: Type of vectorizer to use
            tune_hyperparameters: Whether to perform hyperparameter tuning
            
        Returns:
            Training metrics
        """
        self.logger.info(f"Training {classifier_type} classifier for '{task_name}'...")
        
        # Create pipeline
        vectorizer = self.vectorizer_configs.get(vectorizer_type).clone()
        classifier = self.classifiers.get(classifier_type)
        
        if classifier is None:
            raise ValueError(f"Unknown classifier: {classifier_type}")
        
        # Create pipeline
        pipeline = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', classifier)
        ])
        
        # Hyperparameter tuning
        if tune_hyperparameters:
            self.logger.info("Performing hyperparameter tuning...")
            param_grid = self._get_param_grid(classifier_type)
            
            grid_search = GridSearchCV(
                pipeline, param_grid, cv=3, scoring='f1_macro',
                n_jobs=-1, verbose=1
            )
            grid_search.fit(X_train, y_train)
            
            best_params = grid_search.best_params_
            self.logger.info(f"Best parameters: {best_params}")
            
            # Use best model
            pipeline = grid_search.best_estimator_
        else:
            # Train without tuning
            pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = pipeline.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average='weighted', zero_division=0
        )
        
        metrics = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'classification_report': classification_report(
                y_test, y_pred, output_dict=True, zero_division=0
            ),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Classification Report for '{task_name}':")
        self.logger.info(f"{'='*60}")
        self.logger.info(classification_report(y_test, y_pred, zero_division=0))
        self.logger.info(f"Accuracy: {accuracy:.4f}")
        self.logger.info(f"F1-Score: {f1:.4f}")
        
        # Store model
        self.models[task_name] = pipeline
        self.vectorizers[task_name] = vectorizer
        
        return metrics
    
    def _get_param_grid(self, classifier_type: str) -> Dict:
        """Get hyperparameter grid for classifier."""
        grids = {
            'logistic_regression': {
                'classifier__C': [0.1, 1, 10],
                'classifier__penalty': ['l2'],
                'vectorizer__max_features': [5000, 10000]
            },
            'random_forest': {
                'classifier__n_estimators': [50, 100],
                'classifier__max_depth': [None, 10, 20],
            },
            'svm': {
                'classifier__C': [0.1, 1, 10],
                'classifier__gamma': ['scale', 'auto'],
            }
        }
        return grids.get(classifier_type, {})
    
    def save_model(self,
                  task_name: str,
                  model_name: str = None,
                  version: str = "1.0.0",
                  training_samples: int = 0,
                  evaluation_metrics: Dict = None) -> Path:
        """
        Save trained classifier.
        
        Args:
            task_name: Name of the classification task
            model_name: Custom model name (defaults to task_name)
            version: Model version
            training_samples: Number of training samples
            evaluation_metrics: Evaluation metrics
            
        Returns:
            Path to saved model
        """
        if task_name not in self.models:
            raise ValueError(f"No trained model found for task: {task_name}")
        
        model_name = model_name or f"{task_name}_classifier"
        model = self.models[task_name]
        
        # Create metadata
        metadata = ModelMetadata(
            model_name=model_name,
            model_type="sklearn",
            version=version,
            created_at="",
            training_samples=training_samples,
            features=list(model.named_steps['vectorizer'].get_feature_names_out())[:100],
            metrics=evaluation_metrics or {},
            config={
                'task_name': task_name,
                'classifier_type': type(model.named_steps['classifier']).__name__,
                'vectorizer_type': type(model.named_steps['vectorizer']).__name__,
                'pipeline_steps': list(model.named_steps.keys())
            },
            checksum="",
            file_size=0,
            description=f"Text classifier for {task_name}",
            tags=["text_classification", "regulatory", task_name]
        )
        
        # Save model
        saved_path = self.model_persister.save(
            model=model,
            model_name=model_name,
            metadata=metadata
        )
        
        self.logger.info(f"✅ Model '{model_name}' saved to {saved_path}")
        return saved_path
    
    def load_model(self, model_name: str) -> Pipeline:
        """
        Load a saved classifier.
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            Loaded pipeline
        """
        try:
            loaded_model = self.model_persister.load(model_name, model_type="sklearn")
            self.logger.info(f"✅ Loaded classifier '{model_name}'")
            return loaded_model
        except FileNotFoundError:
            self.logger.error(f"Model '{model_name}' not found")
            raise
    
    def predict(self, 
               texts: List[str], 
               task_name: str) -> Union[List, np.ndarray]:
        """
        Make predictions using trained model.
        
        Args:
            texts: Texts to classify
            task_name: Name of classification task
            
        Returns:
            Predictions
        """
        if task_name not in self.models:
            raise ValueError(f"No model found for task: {task_name}")
        
        model = self.models[task_name]
        predictions = model.predict(texts)
        
        return predictions
    
    def predict_proba(self,
                     texts: List[str],
                     task_name: str) -> np.ndarray:
        """
        Get prediction probabilities.
        
        Args:
            texts: Texts to classify
            task_name: Name of classification task
            
        Returns:
            Prediction probabilities
        """
        if task_name not in self.models:
            raise ValueError(f"No model found for task: {task_name}")
        
        model = self.models[task_name]
        probabilities = model.predict_proba(texts)
        
        return probabilities


def create_sample_training_data() -> Dict[str, Tuple[List[str], List[str]]]:
    """
    Create sample training data for different classification tasks.
    
    Returns:
        Dictionary of task_name -> (texts, labels)
    """
    data = {}
    
    # Task 1: Regulation Type Classification
    regulation_texts = [
        "New SEC filing requirements for public companies",
        "Basel III capital adequacy framework implementation",
        "GDPR data protection and privacy compliance guidelines",
        "AML/KYC anti-money laundering procedures",
        "Dodd-Frank financial reform provisions",
        "SOX internal controls and audit requirements",
        "MiFID II investor protection rules",
        "CCPA consumer privacy rights enforcement",
        "FDIC deposit insurance regulations",
        "CFTC derivatives trading oversight"
    ]
    regulation_labels = [
        "SECURITIES", "BANKING", "PRIVACY", "AML", "FINANCIAL_REFORM",
        "AUDIT", "MARKETS", "PRIVACY", "BANKING", "DERIVATIVES"
    ]
    data['regulation_type'] = (regulation_texts, regulation_labels)
    
    # Task 2: Risk Level Classification
    risk_texts = [
        "Critical violation requiring immediate remediation",
        "High-risk finding with potential regulatory penalties",
        "Moderate compliance gap needing attention",
        "Low-risk observation with minor impact",
        "Severe breach with enforcement action likely",
        "Significant deficiency in control framework",
        "Minor procedural deviation easily corrected",
        "Material weakness requiring board attention"
    ]
    risk_labels = [
        "CRITICAL", "HIGH", "MEDIUM", "LOW",
        "CRITICAL", "HIGH", "LOW", "HIGH"
    ]
    data['risk_level'] = (risk_texts, risk_labels)
    
    # Task 3: Urgency Classification
    urgency_texts = [
        "Immediate action required within 24 hours",
        "Submit response by end of quarter",
        "Annual compliance certification due next month",
        "Emergency regulatory notice effective immediately",
        "Routine update scheduled for next review cycle",
        "Urgent: Potential violation detected",
        "Standard reporting requirement Q4 2024"
    ]
    urgency_labels = [
        "IMMEDIATE", "SHORT_TERM", "MEDIUM_TERM",
        "IMMEDIATE", "LONG_TERM", "IMMEDIATE", "MEDIUM_TERM"
    ]
    data['urgency_level'] = (urgency_texts, urgency_labels)
    
    return data


def main():
    """Main training function."""
    print("=" * 60)
    print("REGIQ - Regulatory Text Classifier Training")
    print("=" * 60)
    
    # Initialize trainer
    trainer = RegulatoryTextClassifierTrainer()
    
    # Create sample training data
    print("\n📝 Preparing training data...")
    training_data = create_sample_training_data()
    
    # Train classifiers for each task
    trained_models = {}
    
    for task_name, (texts, labels) in training_data.items():
        print(f"\n{'='*60}")
        print(f"Training classifier for: {task_name}")
        print(f"{'='*60}")
        
        # Prepare data
        X_train, X_test, y_train, y_test = trainer.prepare_data(
            texts, labels, task_name
        )
        
        # Train model
        metrics = trainer.train_classifier(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            task_name=task_name,
            classifier_type='logistic_regression',
            vectorizer_type='default',
            tune_hyperparameters=False
        )
        
        # Save model
        print(f"\n💾 Saving model...")
        saved_path = trainer.save_model(
            task_name=task_name,
            model_name=f"regulatory_{task_name}",
            version="1.0.0",
            training_samples=len(texts),
            evaluation_metrics={
                'accuracy': metrics['accuracy'],
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'f1_score': metrics['f1_score']
            }
        )
        
        trained_models[task_name] = {
            'path': saved_path,
            'metrics': metrics
        }
    
    # List all saved models
    print(f"\n{'='*60}")
    print("Saved Models:")
    print(f"{'='*60}")
    
    persister = ModelPersistence("models/nlp")
    models = persister.list_models()
    
    for model in models:
        print(f"  ✓ {model['name']} ({model['type']}) v{model['version']} - {model['size_mb']} MB")
    
    print("\n✅ Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
