"""
Bias Mitigation Model Training Demo

Demonstrates saving and loading of bias mitigation models.
Uses simple sklearn models to show the persistence workflow.
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.fairness_model_persistence import FairnessModelPersistence


class BiasMitigationDemo:
    """Demonstrate bias mitigation model persistence."""
    
    def __init__(self):
        """Initialize demo."""
        self.fp = FairnessModelPersistence()
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger."""
        import logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def create_biased_dataset(self) -> Tuple:
        """Create dataset with realistic bias patterns."""
        np.random.seed(42)
        n_samples = 1000
        
        # Protected attribute (e.g., gender: 0=Female, 1=Male)
        protected = np.random.binomial(1, 0.5, n_samples)
        
        # Features
        education = np.random.normal(12 + protected * 2, 3, n_samples)
        experience = np.random.normal(8 + protected * 1, 2, n_samples)
        age = np.random.normal(35 + protected * 3, 10, n_samples)
        
        # Biased outcome
        base_prob = 0.3 + 0.3 * protected + 0.02 * education + 0.01 * experience
        outcome = np.random.binomial(1, np.clip(base_prob, 0, 1), n_samples)
        
        X = np.column_stack([education, experience, age])
        y = outcome
        feature_names = ['education', 'experience', 'age']
        
        return X, y, protected, feature_names
    
    def evaluate_fairness(self, y_true: np.ndarray, y_pred: np.ndarray, protected: np.ndarray) -> Dict[str, float]:
        """Calculate fairness metrics."""
        metrics = {}
        
        group_0 = protected == 0
        group_1 = protected == 1
        
        # Positive rates
        p_rate_0 = y_true[group_0].mean()
        p_rate_1 = y_true[group_1].mean()
        
        # Demographic parity
        if p_rate_0 > 0:
            metrics['demographic_parity_ratio'] = p_rate_1 / p_rate_0
        else:
            metrics['demographic_parity_ratio'] = float('inf')
        
        metrics['statistical_parity_diff'] = abs(p_rate_1 - p_rate_0)
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        
        return metrics
    
    def train_and_save_reweighting(self) -> Path:
        """Train model with sample reweighting and save."""
        self.logger.info("\n" + "="*60)
        self.logger.info("Training REWEIGHTING Model")
        self.logger.info("="*60)
        
        X, y, protected, _ = self.create_biased_dataset()
        
        # Prepare data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test, prot_train, prot_test = train_test_split(
            X_scaled, y, protected, test_size=0.3, random_state=42
        )
        
        # Baseline
        baseline = LogisticRegression(random_state=42, max_iter=1000)
        baseline.fit(X_train, y_train)
        y_pred_base = baseline.predict(X_test)
        metrics_before = self.evaluate_fairness(y_test, y_pred_base, prot_test)
        
        self.logger.info("\n📊 Baseline:")
        for k, v in metrics_before.items():
            self.logger.info(f"   {k}: {v:.4f}")
        
        # Calculate reweighting factors
        # Give more weight to underprivileged group
        weights = np.where(prot_train == 0, 1.5, 1.0)
        
        # Train with weights
        weighted_model = LogisticRegression(random_state=42, max_iter=1000)
        weighted_model.fit(X_train, y_train, sample_weight=weights)
        
        y_pred_weighted = weighted_model.predict(X_test)
        metrics_after = self.evaluate_fairness(y_test, y_pred_weighted, prot_test)
        
        self.logger.info("\n📊 After Reweighting:")
        for k, v in metrics_after.items():
            self.logger.info(f"   {k}: {v:.4f}")
        
        # Save model (store both the classifier and weights strategy)
        model_data = {
            'model': weighted_model,
            'scaler': scaler,
            'weights_strategy': 'protected_group_balancing',
            'weight_factor': 1.5,  # Weight for group 0
            'weight_type': 'group_specific'
        }
        
        self.logger.info("\n💾 Saving model...")
        model_path = self.fp.save_mitigation_model(
            model=model_data,
            technique_name='sample_reweighting',
            category='preprocessing',
            dataset_name='demo_bias_dataset',
            protected_attributes=['protected_binary'],
            metrics_before=metrics_before,
            metrics_after=metrics_after,
            version='1.0.0',
            description='Sample reweighting for demographic parity',
            tags=['preprocessing', 'reweighting', 'demo']
        )
        
        self.logger.info(f"✅ Saved to: {model_path}")
        
        return model_path
    
    def train_and_save_threshold_adjustment(self) -> Path:
        """Train post-processing threshold adjuster and save."""
        self.logger.info("\n" + "="*60)
        self.logger.info("Training THRESHOLD ADJUSTMENT Model")
        self.logger.info("="*60)
        
        X, y, protected, _ = self.create_biased_dataset()
        
        # Prepare data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test, prot_train, prot_test = train_test_split(
            X_scaled, y, protected, test_size=0.3, random_state=42
        )
        
        # Base model
        base = LogisticRegression(random_state=42, max_iter=1000)
        base.fit(X_train, y_train)
        
        # Get probabilities
        y_proba = base.predict_proba(X_test)[:, 1]
        
        # Baseline with 0.5 threshold
        y_pred_base = (y_proba > 0.5).astype(int)
        metrics_before = self.evaluate_fairness(y_test, y_pred_base, prot_test)
        
        self.logger.info("\n📊 Baseline (threshold=0.5):")
        for k, v in metrics_before.items():
            self.logger.info(f"   {k}: {v:.4f}")
        
        # Find optimal thresholds per group
        # Lower threshold for underprivileged group
        threshold_0 = 0.4  # Group 0
        threshold_1 = 0.6  # Group 1
        
        y_pred_adjusted = np.where(
            prot_test == 0,
            (y_proba > threshold_0).astype(int),
            (y_proba > threshold_1).astype(int)
        )
        
        metrics_after = self.evaluate_fairness(y_test, y_pred_adjusted, prot_test)
        
        self.logger.info("\n📊 After Threshold Adjustment:")
        for k, v in metrics_after.items():
            self.logger.info(f"   {k}: {v:.4f}")
        
        # Save threshold strategy
        threshold_model = {
            'base_model': base,
            'scaler': scaler,
            'thresholds': {0: threshold_0, 1: threshold_1},
            'strategy': 'group_specific_thresholds'
        }
        
        self.logger.info("\n💾 Saving model...")
        model_path = self.fp.save_mitigation_model(
            model=threshold_model,
            technique_name='threshold_adjustment',
            category='post_processing',
            dataset_name='demo_bias_dataset',
            protected_attributes=['protected_binary'],
            metrics_before=metrics_before,
            metrics_after=metrics_after,
            version='1.0.0',
            description='Group-specific threshold adjustment for fairness',
            tags=['post_processing', 'threshold', 'demo']
        )
        
        self.logger.info(f"✅ Saved to: {model_path}")
        
        return model_path
    
    def run_demo(self):
        """Run complete demo."""
        self.logger.info("\n" + "="*70)
        self.logger.info("BIAS MITIGATION MODEL TRAINING DEMO")
        self.logger.info("="*70)
        
        # Train models
        results = {}
        results['sample_reweighting'] = self.train_and_save_reweighting()
        results['threshold_adjustment'] = self.train_and_save_threshold_adjustment()
        
        self.logger.info("\n" + "="*70)
        self.logger.info("✅ MODELS TRAINED AND SAVED")
        self.logger.info("="*70)
        
        # List available
        available = self.fp.list_available_models()
        self.logger.info("\n📂 Available Models:")
        for category, models in available.items():
            if models:
                self.logger.info(f"   {category}: {models}")
        
        # Test loading
        self.logger.info("\n🧪 Testing Model Loading...")
        
        try:
            model_data, metadata = self.fp.load_mitigation_model(
                'sample_reweighting', 'preprocessing', '1.0.0'
            )
            self.logger.info(f"✅ Loaded sample_reweighting (improvement: {metadata.get('improvement', 0):.2%})")
        except Exception as e:
            self.logger.error(f"❌ Failed to load: {e}")
        
        try:
            model_data, metadata = self.fp.load_mitigation_model(
                'threshold_adjustment', 'post_processing', '1.0.0'
            )
            self.logger.info(f"✅ Loaded threshold_adjustment (improvement: {metadata.get('improvement', 0):.2%})")
        except Exception as e:
            self.logger.error(f"❌ Failed to load: {e}")
        
        self.logger.info("\n" + "="*70)
        self.logger.info("DEMO COMPLETE")
        self.logger.info("="*70)
        
        return results


def main():
    """Main function."""
    print("\n" + "="*70)
    print("BIAS MITIGATION MODEL TRAINING")
    print("="*70)
    
    demo = BiasMitigationDemo()
    results = demo.run_demo()
    
    print("\n📊 Summary:")
    print(f"   Models trained: {len(results)}")
    print(f"   Techniques: {list(results.keys())}")


if __name__ == "__main__":
    main()
