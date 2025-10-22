"""
Adversarial debiasing for bias mitigation.

Implements adversarial training where a classifier learns to predict
the target while an adversary tries to predict the protected attribute
from the classifier's predictions. This forces the classifier to learn
representations that are independent of the protected attribute.

Author: REGIQ AI/ML Team
Phase: 3.5.2 - In-processing Mitigation
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Optional, Dict, Tuple, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class AdversarialTrainingResult:
    """Result of adversarial debiasing training"""
    classifier_model: nn.Module
    adversary_model: nn.Module
    n_epochs: int
    final_classifier_loss: float
    final_adversary_loss: float
    training_history: Dict
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'n_epochs': self.n_epochs,
            'final_classifier_loss': float(self.final_classifier_loss),
            'final_adversary_loss': float(self.final_adversary_loss),
            'training_history': {
                k: [float(v) for v in vals] 
                for k, vals in self.training_history.items()
            },
            'metadata': self.metadata
        }


class ClassifierNetwork(nn.Module):
    """Neural network for classification task"""
    
    def __init__(self, input_dim: int, hidden_dims: Tuple[int, ...] = (64, 32), 
                 output_dim: int = 1, dropout: float = 0.3):
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)


class AdversaryNetwork(nn.Module):
    """Neural network for adversary (predicts protected attribute)"""
    
    def __init__(self, input_dim: int, hidden_dims: Tuple[int, ...] = (32,), 
                 output_dim: int = 1):
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)


class AdversarialDebiaser:
    """
    Adversarial debiasing for fairness.
    
    Trains a classifier to predict target labels while simultaneously
    training an adversary to predict protected attributes. The classifier
    is penalized if the adversary can successfully predict protected
    attributes, forcing it to learn fair representations.
    
    Based on AIF360's adversarial debiasing approach.
    """
    
    def __init__(self,
                 input_dim: int,
                 classifier_hidden: Tuple[int, ...] = (64, 32),
                 adversary_hidden: Tuple[int, ...] = (32,),
                 adversary_loss_weight: float = 1.0,
                 n_epochs: int = 50,
                 batch_size: int = 64,
                 learning_rate: float = 0.001,
                 dropout: float = 0.3,
                 device: Optional[str] = None):
        """
        Initialize adversarial debiaser.
        
        Args:
            input_dim: Number of input features
            classifier_hidden: Hidden layer sizes for classifier
            adversary_hidden: Hidden layer sizes for adversary
            adversary_loss_weight: Weight for adversary loss (higher = more fairness)
            n_epochs: Number of training epochs
            batch_size: Batch size for training
            learning_rate: Learning rate for optimizers
            dropout: Dropout rate for classifier
            device: Device to use ('cpu', 'cuda', or None for auto)
        """
        self.input_dim = input_dim
        self.classifier_hidden = classifier_hidden
        self.adversary_hidden = adversary_hidden
        self.adversary_loss_weight = adversary_loss_weight
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.dropout = dropout
        
        # Set device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        # Models will be initialized in fit()
        self.classifier_ = None
        self.adversary_ = None
        self.is_fitted_ = False
        self.training_result_: Optional[AdversarialTrainingResult] = None
    
    def fit(self, X: np.ndarray, y: np.ndarray, 
            protected_attr: np.ndarray) -> 'AdversarialDebiaser':
        """
        Train classifier with adversarial debiasing.
        
        Args:
            X: Training features
            y: Training labels (binary)
            protected_attr: Protected attributes (binary)
            
        Returns:
            self
        """
        logger.info(f"Starting adversarial debiasing training on {self.device}")
        
        # Initialize networks
        self.classifier_ = ClassifierNetwork(
            input_dim=self.input_dim,
            hidden_dims=self.classifier_hidden,
            output_dim=1,
            dropout=self.dropout
        ).to(self.device)
        
        self.adversary_ = AdversaryNetwork(
            input_dim=1,  # Takes classifier's output
            hidden_dims=self.adversary_hidden,
            output_dim=1
        ).to(self.device)
        
        # Optimizers
        classifier_optimizer = optim.Adam(
            self.classifier_.parameters(), 
            lr=self.learning_rate
        )
        adversary_optimizer = optim.Adam(
            self.adversary_.parameters(),
            lr=self.learning_rate
        )
        
        # Loss functions
        classifier_criterion = nn.BCEWithLogitsLoss()
        adversary_criterion = nn.BCEWithLogitsLoss()
        
        # Convert to tensors
        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).unsqueeze(1).to(self.device)
        protected_tensor = torch.FloatTensor(protected_attr).unsqueeze(1).to(self.device)
        
        # Training history
        history = {
            'classifier_loss': [],
            'adversary_loss': [],
            'total_loss': []
        }
        
        # Training loop
        n_samples = len(X)
        n_batches = (n_samples + self.batch_size - 1) // self.batch_size
        
        for epoch in range(self.n_epochs):
            epoch_clf_loss = 0.0
            epoch_adv_loss = 0.0
            epoch_total_loss = 0.0
            
            # Shuffle data
            indices = torch.randperm(n_samples)
            
            for batch_idx in range(n_batches):
                start_idx = batch_idx * self.batch_size
                end_idx = min((batch_idx + 1) * self.batch_size, n_samples)
                batch_indices = indices[start_idx:end_idx]
                
                X_batch = X_tensor[batch_indices]
                y_batch = y_tensor[batch_indices]
                protected_batch = protected_tensor[batch_indices]
                
                # === Train Classifier ===
                classifier_optimizer.zero_grad()
                
                # Forward pass through classifier
                clf_output = self.classifier_(X_batch)
                
                # Classifier loss (predict y)
                clf_loss = classifier_criterion(clf_output, y_batch)
                
                # Adversary loss (predict protected attribute from classifier output)
                adv_output = self.adversary_(torch.sigmoid(clf_output.detach()))
                adv_loss = adversary_criterion(adv_output, protected_batch)
                
                # Total classifier loss (minimize classification loss, maximize adversary loss)
                total_clf_loss = clf_loss - self.adversary_loss_weight * adv_loss
                
                total_clf_loss.backward()
                classifier_optimizer.step()
                
                # === Train Adversary ===
                adversary_optimizer.zero_grad()
                
                # Forward pass (adversary tries to predict protected attribute)
                clf_output_for_adv = self.classifier_(X_batch)
                adv_output = self.adversary_(torch.sigmoid(clf_output_for_adv.detach()))
                adv_loss_train = adversary_criterion(adv_output, protected_batch)
                
                adv_loss_train.backward()
                adversary_optimizer.step()
                
                # Track losses
                epoch_clf_loss += clf_loss.item()
                epoch_adv_loss += adv_loss_train.item()
                epoch_total_loss += total_clf_loss.item()
            
            # Average losses
            avg_clf_loss = epoch_clf_loss / n_batches
            avg_adv_loss = epoch_adv_loss / n_batches
            avg_total_loss = epoch_total_loss / n_batches
            
            history['classifier_loss'].append(avg_clf_loss)
            history['adversary_loss'].append(avg_adv_loss)
            history['total_loss'].append(avg_total_loss)
            
            if (epoch + 1) % 10 == 0:
                logger.info(
                    f"Epoch {epoch+1}/{self.n_epochs} - "
                    f"Clf Loss: {avg_clf_loss:.4f}, "
                    f"Adv Loss: {avg_adv_loss:.4f}, "
                    f"Total: {avg_total_loss:.4f}"
                )
        
        # Store training results
        self.training_result_ = AdversarialTrainingResult(
            classifier_model=self.classifier_,
            adversary_model=self.adversary_,
            n_epochs=self.n_epochs,
            final_classifier_loss=history['classifier_loss'][-1],
            final_adversary_loss=history['adversary_loss'][-1],
            training_history=history,
            metadata={
                'adversary_loss_weight': self.adversary_loss_weight,
                'batch_size': self.batch_size,
                'learning_rate': self.learning_rate,
                'device': str(self.device)
            }
        )
        
        self.is_fitted_ = True
        logger.info("Adversarial debiasing training complete")
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted before prediction")
        
        self.classifier_.eval()
        
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            logits = self.classifier_(X_tensor)
            predictions = (torch.sigmoid(logits) > 0.5).cpu().numpy().astype(int)
        
        return predictions.flatten()
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict probabilities"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted before prediction")
        
        self.classifier_.eval()
        
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            logits = self.classifier_(X_tensor)
            probas = torch.sigmoid(logits).cpu().numpy()
        
        # Return probabilities for both classes
        return np.hstack([1 - probas, probas])
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate accuracy"""
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)
        return float(accuracy)
    
    def get_training_summary(self) -> Dict:
        """Get summary of adversarial training"""
        if not self.is_fitted_:
            raise ValueError("Model must be fitted first")
        
        return self.training_result_.to_dict()


def main():
    """Test adversarial debiaser"""
    print("🧪 Testing Adversarial Debiaser")
    
    from sklearn.datasets import make_classification
    
    # Create test data
    X, y = make_classification(
        n_samples=1000, n_features=20, n_classes=2, random_state=42
    )
    
    # Create protected attribute
    protected_attr = np.random.choice([0, 1], size=1000, p=[0.7, 0.3])
    
    # Create debiaser
    debiaser = AdversarialDebiaser(
        input_dim=20,
        classifier_hidden=(64, 32),
        adversary_hidden=(32,),
        adversary_loss_weight=1.0,
        n_epochs=20,
        batch_size=64
    )
    
    # Train
    print("\n✅ Training adversarial debiaser...")
    debiaser.fit(X[:800], y[:800], protected_attr[:800])
    
    # Evaluate
    accuracy = debiaser.score(X[800:], y[800:])
    print(f"✅ Test accuracy: {accuracy:.3f}")
    
    # Get summary
    summary = debiaser.get_training_summary()
    print(f"✅ Final classifier loss: {summary['final_classifier_loss']:.4f}")
    print(f"✅ Final adversary loss: {summary['final_adversary_loss']:.4f}")
    
    print("\n✅ Adversarial debiaser test complete!")


if __name__ == '__main__':
    main()
